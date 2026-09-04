import inspect
import re

from math_engine.registry import math_registry
from math_engine.executor import execute_math_operation


def _requested_result_score(query, operation_name):
    """
    Give extra routing weight to the quantity the user
    appears to be asking NOVA to calculate.

    Example:

        "Find the area of a circle with radius 7"

    should prefer:

        circle_area

    over:

        circle_radius_from_area
    """

    query = str(query).lower()
    operation_name = str(operation_name).lower()

    result_terms = [
        "area",
        "volume",
        "perimeter",
        "circumference",
        "radius",
        "diameter",
        "length",
        "width",
        "height",
        "distance",
        "slope",
        "midpoint",
        "angle",
        "derivative",
        "integral",
        "limit",
        "root",
        "roots",
    ]

    requested_terms = []

    for term in result_terms:

        patterns = [
            f"what is the {term}",
            f"find the {term}",
            f"calculate the {term}",
            f"determine the {term}",
            f"compute the {term}",
        ]

        if any(
            pattern in query
            for pattern in patterns
        ):
            requested_terms.append(
                term
            )

    score = 0

    for term in requested_terms:

        name_words = (
            operation_name
            .replace("_", " ")
            .split()
        )

        # Reward operations whose output appears to match
        # the quantity the user is requesting.
        if term in name_words:
            score += 30

        # Penalize inverse-style operations where the
        # requested quantity is actually being used as input.
        #
        # Example:
        # circle_radius_from_area
        #
        # should not beat circle_area when the user asks
        # "What is the area...?"
        if f"from_{term}" in operation_name:
            score -= 35

    return score


def _argument_compatibility_score(
    operation,
    arguments
):
    """
    Score how well supplied arguments match an operation's
    actual Python function signature.

    Argument compatibility only affects routing when the
    caller has supplied one or more arguments.

    Returns:
        Integer score adjustment.
    """

    if not arguments:
        return 0

    function = operation["function"]

    signature = inspect.signature(
        function
    )

    parameters = signature.parameters

    required_parameters = []

    accepts_kwargs = False

    for parameter_name, parameter in parameters.items():

        if parameter.kind == inspect.Parameter.VAR_KEYWORD:
            accepts_kwargs = True
            continue

        if parameter.kind == inspect.Parameter.VAR_POSITIONAL:
            continue

        if (
            parameter.default
            is inspect.Parameter.empty
        ):
            required_parameters.append(
                parameter_name
            )

    score = 0

    # --------------------------------------------------------
    # REWARD SUPPLIED ARGUMENTS THAT THE FUNCTION ACCEPTS
    # --------------------------------------------------------

    for argument_name in arguments:

        if (
            argument_name in parameters
            or accepts_kwargs
        ):
            score += 15

        else:
            score -= 20

    # --------------------------------------------------------
    # CHECK REQUIRED ARGUMENTS
    # --------------------------------------------------------

    missing_required = [
        parameter_name
        for parameter_name
        in required_parameters
        if parameter_name not in arguments
    ]

    if not missing_required:
        score += 20

    else:
        score -= (
            len(missing_required)
            * 25
        )

    return score


def find_math_operations(
    query,
    subsystem=None,
    max_results=10,
    arguments=None
):
    """
    Find likely NOVA math operations based on a text query.

    This function does not automatically execute anything.
    It searches the registry and returns ranked candidate
    operations.

    Parameters:
        query:
            Text describing the desired math operation.

        subsystem:
            Optional subsystem filter such as:
            "arithmetic"
            "algebra"
            "geometry"
            "trigonometry"
            "calculus"

        max_results:
            Maximum number of candidate operations to return.

    Returns:
        A list of candidate operation metadata dictionaries.
    """

    query = str(query).strip().lower()
    arguments = arguments or {}

    if not query:
        return []

    # --------------------------------------------------------
    # GET CANDIDATES
    # --------------------------------------------------------

    if subsystem is None:
        candidates = math_registry.all_operations()

    else:
        candidates = math_registry.by_subsystem(
            subsystem
        )

    # --------------------------------------------------------
    # SCORE CANDIDATES
    # --------------------------------------------------------

    scored_candidates = []

    query_words = set(
        re.findall(
            r"[a-zA-Z0-9]+",
            query.replace("_", " ")
        )
    )

    for operation in candidates:

        name = operation[
            "name"
        ].lower()

        description = operation[
            "description"
        ].lower()

        category = (
            operation["category"] or ""
        ).lower()

        keywords = [
            str(keyword).lower()
            for keyword
            in operation["keywords"]
        ]

        score = 0

        # ----------------------------------------------------
        # EXACT NAME MATCH
        # ----------------------------------------------------

        if query == name:
            score += 100

        # ----------------------------------------------------
        # QUERY APPEARS IN OPERATION NAME
        # ----------------------------------------------------

        normalized_name = name.replace(
            "_",
            " "
        )

        if query in normalized_name:
            score += 50

        # ----------------------------------------------------
        # OPERATION NAME APPEARS IN QUERY
        # ----------------------------------------------------

        if normalized_name in query:
            score += 40

        # ----------------------------------------------------
        # WORD OVERLAP WITH NAME
        # ----------------------------------------------------

        name_words = set(
            normalized_name.split()
        )

        score += (
            len(
                query_words
                & name_words
            )
            * 10
        )

        # ----------------------------------------------------
        # WORD OVERLAP WITH KEYWORDS
        # ----------------------------------------------------

        keyword_words = set()

        for keyword in keywords:
            keyword_words.update(
                keyword.replace(
                    "_",
                    " "
                ).split()
            )

        score += (
            len(
                query_words
                & keyword_words
            )
            * 6
        )

        # ----------------------------------------------------
        # WORD OVERLAP WITH CATEGORY
        # ----------------------------------------------------

        category_words = set(
            category.replace(
                "_",
                " "
            ).split()
        )

        score += (
            len(
                query_words
                & category_words
            )
            * 4
        )

        # ----------------------------------------------------
        # WORD OVERLAP WITH DESCRIPTION
        # ----------------------------------------------------

        description_words = set(
            description.replace(
                "_",
                " "
            ).split()
        )

        score += (
            len(
                query_words
                & description_words
            )
            * 2
        )

        # ----------------------------------------------------
        # REQUESTED RESULT / OUTPUT INTENT
        # ----------------------------------------------------

        score += _requested_result_score(
            query,
            operation["name"]
        )

        # ----------------------------------------------------
        # ARGUMENT COMPATIBILITY
        # ----------------------------------------------------

        score += _argument_compatibility_score(
            operation,
            arguments
        )

        # ----------------------------------------------------
        # ONLY KEEP ACTUAL MATCHES
        # ----------------------------------------------------

        if score > 0:
            scored_candidates.append(
                {
                    "score": score,
                    "name": operation[
                        "name"
                    ],
                    "subsystem": operation[
                        "subsystem"
                    ],
                    "category": operation[
                        "category"
                    ],
                    "description": operation[
                        "description"
                    ],
                    "parameters": operation[
                        "parameters"
                    ],
                    "keywords": operation[
                        "keywords"
                    ]
                }
            )

    # --------------------------------------------------------
    # SORT BEST MATCHES FIRST
    # --------------------------------------------------------

    scored_candidates.sort(
        key=lambda candidate:
        candidate["score"],
        reverse=True
    )

    return scored_candidates[
        :max_results
    ]


def select_math_operation(
    query,
    subsystem=None,
    arguments=None,
    minimum_score=20,
    minimum_lead=10
):
    """
    Select a math operation when the router has
    a sufficiently strong and unambiguous match.

    This function does not execute the operation.
    """

    candidates = find_math_operations(
        query=query,
        subsystem=subsystem,
        max_results=5,
        arguments=arguments
    )

    # --------------------------------------------------------
    # NO MATCHES
    # --------------------------------------------------------

    if not candidates:
        return {
            "success": False,
            "operation": None,
            "candidate": None,
            "alternatives": [],
            "reason": (
                "No matching math operations were found."
            )
        }

    best = candidates[0]

    # --------------------------------------------------------
    # BEST MATCH IS TOO WEAK
    # --------------------------------------------------------

    if best["score"] < minimum_score:
        return {
            "success": False,
            "operation": None,
            "candidate": best,
            "alternatives": candidates[1:],
            "reason": (
                "The best match did not meet the "
                "minimum confidence score."
            )
        }

    # --------------------------------------------------------
    # CHECK FOR AMBIGUITY
    # --------------------------------------------------------

    if len(candidates) > 1:

        second_best = candidates[1]

        lead = (
            best["score"]
            - second_best["score"]
        )

        if lead < minimum_lead:
            return {
                "success": False,
                "operation": None,
                "candidate": best,
                "alternatives": candidates[1:],
                "reason": (
                    "The request is ambiguous between "
                    "multiple math operations."
                )
            }

    # --------------------------------------------------------
    # CLEAR WINNER
    # --------------------------------------------------------

    return {
        "success": True,
        "operation": best["name"],
        "candidate": best,
        "alternatives": candidates[1:],
        "reason": (
            "A sufficiently strong operation match "
            "was found."
        )
    }


def route_and_execute_math(
    query,
    arguments=None,
    subsystem=None,
    minimum_score=20,
    minimum_lead=10
):
    """
    Route a math request to a registered operation
    and execute it through NOVA's standardized executor.
    """

    arguments = arguments or {}

    # --------------------------------------------------------
    # SELECT OPERATION
    # --------------------------------------------------------

    selection = select_math_operation(
        query=query,
        subsystem=subsystem,
        arguments=arguments,
        minimum_score=minimum_score,
        minimum_lead=minimum_lead
    )

    # --------------------------------------------------------
    # ROUTING FAILED
    # --------------------------------------------------------

    if not selection["success"]:
        return {
            "success": False,
            "stage": "routing",
            "query": query,
            "operation": None,
            "routing": selection,
            "execution": None,
            "error": selection["reason"]
        }

    operation_name = selection[
        "operation"
    ]

    # --------------------------------------------------------
    # EXECUTE SELECTED OPERATION
    # --------------------------------------------------------

    execution = execute_math_operation(
        operation_name,
        arguments
    )

    # --------------------------------------------------------
    # EXECUTION FAILED
    # --------------------------------------------------------

    if not execution["success"]:
        return {
            "success": False,
            "stage": "execution",
            "query": query,
            "operation": operation_name,
            "routing": selection,
            "execution": execution,
            "error": execution["error"]
        }

    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    return {
        "success": True,
        "stage": "complete",
        "query": query,
        "operation": operation_name,
        "routing": selection,
        "execution": execution,
        "error": None
    }
import inspect
import re

from math_engine.registry import math_registry
from math_engine.executor import execute_math_operation


def _requested_result_score(query, operation_name):
    """
    Give extra routing weight to the quantity the user
    appears to be asking SATURN to calculate.

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
            f"what is its {term}",
            f"what's the {term}",
            f"what's its {term}",
            f"find the {term}",
            f"find its {term}",
            f"calculate the {term}",
            f"calculate its {term}",
            f"determine the {term}",
            f"determine its {term}",
            f"compute the {term}",
            f"compute its {term}",
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



def _equation_structure_score(query, operation_name):
    """
    Score equation-solving operations using structural clues
    present in the user's language.

    This helps distinguish a normal equation such as:

        solve 3*x + 5 = 20 for x

    from systems, inequalities, logarithmic equations,
    exponential equations, absolute-value equations, etc.
    """

    text = str(query).lower()
    operation_name = str(operation_name).lower()

    # --------------------------------------------------------
    # DETECT BROAD MATHEMATICAL STRUCTURES
    # --------------------------------------------------------

    has_equals = "=" in text

    has_inequality = any(
        symbol in text
        for symbol in (
            "<=",
            ">=",
            "≤",
            "≥",
            "<",
            ">",
        )
    )

    has_system_cue = any(
        cue in text
        for cue in (
            "system",
            "simultaneous",
            ";",
            "\n",
        )
    )

    has_log_cue = any(
        cue in text
        for cue in (
            "log(",
            "ln(",
            "logarithm",
            "logarithmic",
        )
    )

    has_exponential_cue = any(
        cue in text
        for cue in (
            "exponential",
            "^x",
            "**x",
        )
    )

    has_absolute_value_cue = any(
        cue in text
        for cue in (
            "absolute value",
            "abs(",
        )
    )

    has_piecewise_cue = "piecewise" in text

    # --------------------------------------------------------
    # ORDINARY SINGLE-EQUATION SOLVE
    # --------------------------------------------------------

    is_plain_equation = (
        "solve" in text
        and has_equals
        and not has_inequality
        and not has_system_cue
        and not has_log_cue
        and not has_exponential_cue
        and not has_absolute_value_cue
        and not has_piecewise_cue
    )

    if is_plain_equation:

        if operation_name == "solve_equation":
            return 25

        if operation_name in (
            "solve_system",
            "solve_system_advanced",
            "solve_inequality",
            "solve_exponential",
            "solve_logarithmic",
            "solve_absolute_value",
            "solve_piecewise",
        ):
            return -15

    # --------------------------------------------------------
    # STRUCTURAL PENALTIES FOR CLEARLY MISMATCHED SOLVERS
    # --------------------------------------------------------

    if has_inequality and operation_name == "solve_equation":
        return -10

    if has_system_cue and operation_name == "solve_equation":
        return -10

    return 0



def _contains_symbolic_variable_structure(text):
    """
    Detect variable-bearing algebraic syntax so direct arithmetic
    scoring does not steal numeric fragments from expressions.

    Example:
        x**2 + 3*x + 2

    must not be interpreted as the standalone arithmetic "2 + 3".
    """

    text = str(text)

    patterns = [
        r"\b[A-Za-z]\b\s*(?:\*\*|\^|[+\-*/=])",
        r"(?:\*\*|\^|[+\-*/=])\s*\b[A-Za-z]\b",
        r"\b\d+(?:\.\d+)?\s*\*\s*[A-Za-z]\b",
    ]

    return any(
        re.search(pattern, text)
        for pattern in patterns
    )


def _direct_arithmetic_score(query, operation_name):
    """
    Score direct binary arithmetic operations from explicit
    mathematical operators in the routing query.

    Examples:
        17 + 28  -> add
        17 - 8   -> subtract
        6 * 4    -> multiply
        20 / 5   -> divide

    This only scores clear binary arithmetic syntax. More
    complicated expressions continue through normal routing.
    """

    text = str(query).strip().lower()
    operation_name = str(operation_name).lower()

    # A symbolic expression may contain numeric substrings that look
    # like standalone arithmetic. Do not score those fragments.
    if _contains_symbolic_variable_structure(
        text
    ):
        return 0

    operation_patterns = {
        "add": r"-?\d+(?:\.\d+)?\s*\+\s*-?\d+(?:\.\d+)?",
        "subtract": r"-?\d+(?:\.\d+)?\s*-\s*-?\d+(?:\.\d+)?",
        "multiply": r"-?\d+(?:\.\d+)?\s*\*\s*-?\d+(?:\.\d+)?",
        "divide": r"-?\d+(?:\.\d+)?\s*/\s*-?\d+(?:\.\d+)?",
    }

    detected_operation = None

    for target_operation, pattern in operation_patterns.items():
        if re.search(pattern, text):
            detected_operation = target_operation
            break

    if detected_operation is None:
        return 0

    if operation_name == detected_operation:
        return 50

    if operation_name in operation_patterns:
        return -20

    return -10


def _direct_trig_function_score(query, operation_name):
    """
    Score direct trigonometric function evaluations.

    Examples:
        sin(pi/6)   -> sine
        cos(pi/3)   -> cosine
        tan(pi/4)   -> tangent
        asin(1/2)   -> arcsine

    This scorer is intentionally disabled for equation-solving
    requests so that expressions such as "solve sin(x) = 1/2"
    remain available to trig-equation solvers.
    """

    text = str(query).strip().lower()
    operation_name = str(operation_name).lower()

    if (
        "solve" in text
        or "=" in text
        or any(
            symbol in text
            for symbol in ("<=", ">=", "≤", "≥", "<", ">")
        )
    ):
        return 0

    trig_aliases = {
        "sine": ("sin",),
        "cosine": ("cos",),
        "tangent": ("tan",),
        "secant": ("sec",),
        "cosecant": ("csc",),
        "cotangent": ("cot",),
        "arcsine": ("asin", "arcsin"),
        "arccosine": ("acos", "arccos"),
        "arctangent": ("atan", "arctan"),
    }

    detected_operation = None

    ordered_operations = (
        "arcsine",
        "arccosine",
        "arctangent",
        "sine",
        "cosine",
        "tangent",
        "secant",
        "cosecant",
        "cotangent",
    )

    for target_operation in ordered_operations:

        for alias in trig_aliases[target_operation]:

            if re.search(
                rf"\b{re.escape(alias)}\s*\(",
                text
            ):
                detected_operation = target_operation
                break

        if detected_operation is not None:
            break

    if detected_operation is None:
        return 0

    if operation_name == detected_operation:
        return 50

    if operation_name in trig_aliases:
        return -20

    return -15

def _explicit_operation_intent_score(
    query,
    operation_name,
):
    """
    Strongly score clear natural-language operation requests.

    These patterns describe complete mathematical intentions rather
    than isolated words, preventing unrelated registry operations
    from winning because of generic words such as "of".
    """

    text = str(query).strip().lower()
    operation_name = str(operation_name).lower()

    number = r"[-+]?\d+(?:\.\d+)?"

    intent_patterns = {
        "subtract": [
            (
                rf"\bdifference\s+between\s+"
                rf"{number}\s+and\s+{number}\b"
            ),
        ],
        "factor_expression": [
            (
                r"\bfactor\s+"
                r"(?:(?:the\s+)?(?:expression|polynomial)\s+)?"
                r".*[a-z].*(?:\^|\*\*|[+\-*/])"
            ),
        ],
        "arithmetic_mean": [
            (
                r"\b(?:mean|average)\s+of\s+"
                r"[-+]?\d"
            ),
        ],
    }

    detected_operation = None

    for target_operation, patterns in intent_patterns.items():
        if any(
            re.search(pattern, text)
            for pattern in patterns
        ):
            detected_operation = target_operation
            break

    if detected_operation is None:
        return 0

    if operation_name == detected_operation:
        return 80

    if operation_name in intent_patterns:
        return -20

    return -10


def find_math_operations(
    query,
    subsystem=None,
    max_results=10,
    arguments=None
):
    """
    Find likely SATURN math operations based on a text query.

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
        # EQUATION STRUCTURE / SOLVER INTENT
        # ----------------------------------------------------

        score += _equation_structure_score(
            query,
            operation["name"]
        )

        # ----------------------------------------------------
        # EXPLICIT NATURAL-LANGUAGE OPERATION INTENT
        # ----------------------------------------------------

        score += _explicit_operation_intent_score(
            query,
            operation["name"]
        )

        # ----------------------------------------------------
        # DIRECT ARITHMETIC EVALUATION
        # ----------------------------------------------------

        score += _direct_arithmetic_score(
            query,
            operation["name"]
        )

        # ----------------------------------------------------
        # DIRECT TRIG FUNCTION EVALUATION
        # ----------------------------------------------------

        score += _direct_trig_function_score(
            query,
            operation["name"]
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
    and execute it through SATURN's standardized executor.
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
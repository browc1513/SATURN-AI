"""
N.O.V.A. Problem Planner v1.3

Fixes in v1.3
-------------
1. Preserve symbolic givens exactly:
       circumference of 20*pi
   stays "20*pi" instead of being reduced to 20.

2. Save each step under the result the user actually requested:
       circle_radius_from_circumference -> save_as "radius"

3. Prefer prior computed results over accidental language matches:
       "find its area" now receives radius="$radius"
   instead of incorrectly extracting a word such as "and".

4. Only search declarative setup/given text for named givens.
   Action phrases are not treated as data.
"""

import re

from math_engine.argument_extractor import (
    extract_arguments_for_operation,
)
from math_engine.interpreter import interpret_math_request
from math_engine.router import select_math_operation


KNOWN_ENTITIES = (
    "circle",
    "sphere",
    "triangle",
    "rectangle",
    "square",
    "parallelogram",
    "trapezoid",
    "rhombus",
    "ellipse",
    "cylinder",
    "cone",
    "cube",
    "prism",
    "pyramid",
    "polygon",
    "vector",
    "line",
    "plane",
)


def _split_problem_into_clauses(text):
    text = str(text).strip()

    if not text:
        return []

    sentence_parts = re.split(
        r"(?<=[.!?])\s+",
        text,
    )

    clauses = []

    for sentence in sentence_parts:

        sentence = sentence.strip()

        if not sentence:
            continue

        parts = re.split(
            r"\s+(?:and\s+then|then)\s+",
            sentence,
            flags=re.IGNORECASE,
        )

        for part in parts:

            part = part.strip(
                " \t\r\n,.;"
            )

            if part:
                clauses.append(part)

    return clauses


def _requested_result_from_clause(clause):
    """
    Extract the noun/result explicitly requested by an action clause.
    """

    text = str(clause).lower()

    candidates = (
        "surface area",
        "circumference",
        "diameter",
        "perimeter",
        "volume",
        "radius",
        "area",
        "length",
        "width",
        "height",
        "slope",
        "midpoint",
        "distance",
        "angle",
        "side",
        "derivative",
        "integral",
        "roots",
        "root",
        "solution",
    )

    for candidate in candidates:

        if re.search(
            rf"\b{re.escape(candidate)}\b",
            text,
        ):
            return candidate.replace(
                " ",
                "_",
            )

    return None


def _infer_result_name(
    operation_name,
    clause=None,
):
    """
    Prefer the result explicitly requested by the user.
    Fall back to operation-name inference only when needed.
    """

    requested = (
        _requested_result_from_clause(
            clause or ""
        )
    )

    if requested:
        return requested

    operation_name = str(operation_name)

    known_result_names = [
        "surface_area",
        "radius",
        "area",
        "circumference",
        "diameter",
        "perimeter",
        "volume",
        "length",
        "width",
        "height",
        "slope",
        "midpoint",
        "distance",
        "angle",
        "side",
        "derivative",
        "integral",
        "roots",
        "root",
        "solution",
    ]

    for name in known_result_names:

        if name in operation_name:
            return name

    return "step_result"


def _extract_symbolic_named_value(
    text,
    parameter_name,
):
    """
    Recover a named given that may be symbolic.

    Examples:
        circumference of 20*pi
        radius = 3*sqrt(2)
        angle pi/2

    This function is intended for declarative setup/given text only.
    """

    alias = re.escape(
        str(parameter_name).replace(
            "_",
            " ",
        )
    )

    # A compact symbolic token/expression. This intentionally allows
    # common SymPy-style syntax such as 20*pi, pi/2, sqrt(2), x**2.
    value_pattern = (
        r"[+\-]?"
        r"(?:"
        r"\d+(?:\.\d+)?"
        r"|[A-Za-z_][A-Za-z0-9_]*"
        r"|[A-Za-z_][A-Za-z0-9_]*\([^)]*\)"
        r")"
        r"(?:"
        r"\s*(?:\*\*|\*|/|\+|-)\s*"
        r"(?:"
        r"\d+(?:\.\d+)?"
        r"|[A-Za-z_][A-Za-z0-9_]*"
        r"|[A-Za-z_][A-Za-z0-9_]*\([^)]*\)"
        r")"
        r")*"
    )

    patterns = [
        rf"\b{alias}\b"
        rf"\s+(?:of|is|equals)?\s*"
        rf"({value_pattern})",
        rf"\b{alias}\b"
        rf"\s*=\s*"
        rf"({value_pattern})",
    ]

    stopwords = {
        "and",
        "then",
        "the",
        "its",
        "from",
        "using",
        "with",
        "find",
        "calculate",
        "compute",
    }

    for pattern in patterns:

        match = re.search(
            pattern,
            str(text),
            flags=re.IGNORECASE,
        )

        if match is None:
            continue

        value = match.group(
            1
        ).strip()

        if not value:
            continue

        if value.lower() in stopwords:
            continue

        return value

    return None


def _find_previous_result_reference(
    parameter_name,
    previous_steps,
):
    """
    Match a required argument to a previously saved result.
    """

    for step in reversed(
        previous_steps
    ):

        save_as = step.get(
            "save_as"
        )

        if not save_as:
            continue

        if save_as == parameter_name:
            return f"${save_as}"

        if parameter_name in save_as:
            return f"${save_as}"

        if save_as in parameter_name:
            return f"${save_as}"

    return None


def _looks_like_action_clause(text):
    text = str(text).strip().lower()

    action_starters = (
        "find ",
        "calculate ",
        "compute ",
        "solve ",
        "determine ",
        "evaluate ",
        "differentiate ",
        "integrate ",
        "simplify ",
        "factor ",
        "expand ",
        "convert ",
        "use ",
        "apply ",
    )

    return text.startswith(
        action_starters
    )


def _infer_entity(setup_context):
    combined = " ".join(
        setup_context
    ).lower()

    for entity in KNOWN_ENTITIES:

        if re.search(
            rf"\b{re.escape(entity)}\b",
            combined,
        ):
            return entity

    return None


def _infer_given_names(setup_context):
    combined = " ".join(
        setup_context
    ).lower()

    candidates = (
        "circumference",
        "radius",
        "diameter",
        "area",
        "perimeter",
        "volume",
        "surface area",
        "length",
        "width",
        "height",
        "slope",
        "angle",
        "side",
    )

    found = []

    for candidate in candidates:

        if re.search(
            rf"\b{re.escape(candidate)}\b",
            combined,
        ):
            found.append(candidate)

    return found


def _build_routing_clause(
    clause,
    setup_context,
    previous_steps,
):
    """
    Build a compact phrase for the router.

    Example:
        find circle radius from circumference
        find circle area using radius
    """

    entity = _infer_entity(
        setup_context
    )

    requested_result = (
        _requested_result_from_clause(
            clause
        )
    )

    given_names = _infer_given_names(
        setup_context
    )

    prior_names = [
        step.get("save_as")
        for step in previous_steps
        if step.get("save_as")
    ]

    parts = ["find"]

    if entity:
        parts.append(entity)

    if requested_result:
        parts.append(
            requested_result.replace(
                "_",
                " ",
            )
        )

    useful_sources = [
        name
        for name in prior_names
        if name != requested_result
    ]

    if useful_sources:
        parts.append("using")
        parts.extend(
            name.replace("_", " ")
            for name in useful_sources
        )

    elif given_names:
        sources = [
            name
            for name in given_names
            if (
                name.replace(" ", "_")
                != requested_result
            )
        ]

        if sources:
            parts.append("from")
            parts.extend(sources)

    if (
        entity is None
        and requested_result is None
    ):
        return clause

    return " ".join(parts)


def _build_extraction_clause(
    setup_context,
    clause,
):
    if not setup_context:
        return clause

    return (
        ". ".join(
            setup_context
        )
        + ". "
        + clause
    )


def _route_clause(text):
    interpretation = interpret_math_request(
        text
    )

    if not interpretation.get(
        "success"
    ):

        return {
            "success": False,
            "interpretation": interpretation,
            "routing": None,
            "error": interpretation.get(
                "error"
            ),
        }

    routing = select_math_operation(
        query=interpretation[
            "query"
        ],
        subsystem=interpretation[
            "subsystem"
        ],
    )

    if not routing.get(
        "success"
    ):

        return {
            "success": False,
            "interpretation": interpretation,
            "routing": routing,
            "error": routing.get(
                "reason"
            ),
        }

    return {
        "success": True,
        "interpretation": interpretation,
        "routing": routing,
        "error": None,
    }


def plan_math_problem(text):
    """
    Build a deterministic multi-step execution plan.
    """

    result = {
        "success": False,
        "goal": str(text),
        "steps": [],
        "warnings": [],
        "error": None,
    }

    clauses = (
        _split_problem_into_clauses(
            text
        )
    )

    if not clauses:

        result["error"] = (
            "No problem steps could be identified."
        )

        return result

    previous_steps = []
    setup_context = []

    for clause in clauses:

        if not _looks_like_action_clause(
            clause
        ):

            setup_context.append(
                clause
            )

            continue

        routing_clause = (
            _build_routing_clause(
                clause,
                setup_context,
                previous_steps,
            )
        )

        extraction_clause = (
            _build_extraction_clause(
                setup_context,
                clause,
            )
        )

        routed = _route_clause(
            routing_clause
        )

        if not routed["success"]:

            step_number = (
                len(previous_steps) + 1
            )

            result["error"] = (
                f"Could not route step "
                f"{step_number}: "
                f"{routed['error']}"
            )

            return result

        operation_name = (
            routed["routing"][
                "operation"
            ]
        )

        extraction = (
            extract_arguments_for_operation(
                extraction_clause,
                operation_name,
            )
        )

        if extraction.get(
            "error"
        ):

            step_number = (
                len(previous_steps) + 1
            )

            result["error"] = (
                f"Argument extraction "
                f"failed for step "
                f"{step_number}: "
                f"{extraction['error']}"
            )

            return result

        arguments = dict(
            extraction.get(
                "arguments",
                {},
            )
        )

        required_parameters = [
            parameter["name"]
            for parameter
            in extraction.get(
                "parameters",
                [],
            )
            if parameter.get(
                "required"
            )
        ]

        setup_text = ". ".join(
            setup_context
        )

        for parameter_name in (
            required_parameters
        ):

            # ------------------------------------------------
            # 1. Prefer explicit declarative givens from setup.
            #    This intentionally overrides a weaker numeric
            #    extractor result such as 20 from "20*pi".
            # ------------------------------------------------

            symbolic_value = (
                _extract_symbolic_named_value(
                    setup_text,
                    parameter_name,
                )
            )

            if symbolic_value is not None:

                arguments[
                    parameter_name
                ] = symbolic_value

                continue

            # ------------------------------------------------
            # 2. Prefer prior computed results for dependencies.
            # ------------------------------------------------

            reference = (
                _find_previous_result_reference(
                    parameter_name,
                    previous_steps,
                )
            )

            if reference is not None:

                arguments[
                    parameter_name
                ] = reference

                continue

            # ------------------------------------------------
            # 3. Otherwise keep any value already recovered by
            #    the universal argument extractor.
            # ------------------------------------------------

            if (
                parameter_name
                in arguments
            ):
                continue

        missing_required = [
            parameter_name
            for parameter_name
            in required_parameters
            if (
                parameter_name
                not in arguments
            )
        ]

        if missing_required:

            step_number = (
                len(previous_steps) + 1
            )

            result["error"] = (
                f"Step {step_number} is "
                f"missing required "
                f"argument(s): "
                + ", ".join(
                    missing_required
                )
            )

            return result

        save_as = (
            _infer_result_name(
                operation_name,
                clause,
            )
        )

        existing_names = {
            step.get(
                "save_as"
            )
            for step
            in previous_steps
        }

        if save_as in existing_names:

            save_as = (
                f"{save_as}_"
                f"{len(previous_steps) + 1}"
            )

        step = {
            "step": (
                len(previous_steps) + 1
            ),
            "source_text": clause,
            "routing_text": routing_clause,
            "extraction_text": extraction_clause,
            "operation": operation_name,
            "arguments": arguments,
            "save_as": save_as,
        }

        previous_steps.append(
            step
        )

    if not previous_steps:

        result["error"] = (
            "No executable math operations "
            "could be planned."
        )

        return result

    result["steps"] = (
        previous_steps
    )

    result["success"] = True

    return result

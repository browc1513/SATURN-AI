from math_engine.step_engine import generate_steps
from math_engine.interpreter import interpret_math_request
from math_engine.router import select_math_operation
from math_engine.executor import execute_math_operation
from math_engine.argument_extractor import (
    extract_arguments_for_operation,
)


def interpret_and_execute_math(text):
    """
    Run a natural-language math request through NOVA's
    complete deterministic math pipeline.

    Pipeline:

        Natural Language
            ↓
        Interpreter
            ↓
        Router
            ↓
        Operation Signature Inspection
            ↓
        Universal Argument Extraction
            ↓
        Executor
            ↓
        Math Subsystem
            ↓
        Step Engine

    The universal operation-driven extractor is the authoritative
    source of executable arguments. The interpreter is responsible
    for language normalization, query construction, subsystem hints,
    warnings, and interpretation status — not deterministic math
    argument recovery.

    Returns a standardized dictionary containing the
    interpretation, routing result, extracted arguments,
    execution result, and solution steps.
    """

    result = {
        "success": False,
        "stage": None,
        "original_text": str(text),
        "interpretation": None,
        "routing_execution": None,
        "argument_extraction": None,
        "arguments": {},
        "operation": None,
        "exact_result": None,
        "decimal_result": None,
        "steps": [],
        "warnings": [],
        "error": None
    }

    # ========================================================
    # STAGE 1 — LANGUAGE INTERPRETATION
    # ========================================================

    interpretation = interpret_math_request(
        text
    )

    result[
        "interpretation"
    ] = interpretation

    result[
        "warnings"
    ].extend(
        interpretation.get(
            "warnings",
            []
        )
    )

    if not interpretation["success"]:

        result["stage"] = "interpretation"

        result["error"] = (
            interpretation["error"]
        )

        return result

    # ========================================================
    # STAGE 2 — ROUTE FIRST
    # ========================================================
    #
    # The router determines which mathematical operation the
    # user is asking for before NOVA extracts operation-specific
    # arguments.
    # ========================================================

    # Route using normalized user text rather than the interpreter's
    # compressed query. The normalized text preserves mathematical
    # structure such as "=", inequalities, operators, and function
    # notation that the router can use for structural disambiguation.
    routing_query = interpretation.get(
        "normalized_text",
        interpretation["query"]
    )

    routing = select_math_operation(
        query=routing_query,
        subsystem=interpretation["subsystem"]
    )

    if not routing["success"]:

        result["stage"] = "routing"

        result["routing_execution"] = {
            "success": False,
            "stage": "routing",
            "query": routing_query,
            "operation": None,
            "routing": routing,
            "execution": None,
            "error": routing["reason"]
        }

        result["error"] = routing["reason"]

        return result

    operation_name = routing[
        "operation"
    ]

    result[
        "operation"
    ] = operation_name

    # ========================================================
    # STAGE 3 — OPERATION-DRIVEN UNIVERSAL ARGUMENT EXTRACTION
    # ========================================================
    #
    # NOVA now knows the selected operation and can inspect that
    # function's real Python signature. The universal extractor
    # is the authoritative source of executable arguments.
    # ========================================================

    argument_extraction = (
        extract_arguments_for_operation(
            text,
            operation_name
        )
    )

    result[
        "argument_extraction"
    ] = argument_extraction

    if argument_extraction["error"]:

        result["stage"] = "argument_extraction"

        result["error"] = (
            argument_extraction["error"]
        )

        return result

    # ========================================================
    # STAGE 4 — USE UNIVERSAL EXTRACTED ARGUMENTS
    # ========================================================
    #
    # IMPORTANT:
    #
    # We no longer merge interpreter-generated arguments into
    # this dictionary. Universal extraction has structural
    # coverage across the registry and is now responsible for
    # executable function arguments.
    # ========================================================

    arguments = dict(
        argument_extraction.get(
            "arguments",
            {}
        )
    )

    result[
        "arguments"
    ] = arguments

    # ========================================================
    # STAGE 5 — CHECK REQUIRED ARGUMENTS
    # ========================================================
    #
    # Validate against the selected deterministic function's
    # actual signature.
    # ========================================================

    required_parameters = [
        parameter["name"]
        for parameter
        in argument_extraction["parameters"]
        if parameter["required"]
    ]

    missing_required = [
        parameter_name
        for parameter_name
        in required_parameters
        if parameter_name not in arguments
    ]

    if missing_required:

        result["stage"] = "argument_extraction"

        result["error"] = (
            "Missing required argument(s): "
            + ", ".join(
                missing_required
            )
        )

        result["routing_execution"] = {
            "success": False,
            "stage": "argument_extraction",
            "query": interpretation["query"],
            "operation": operation_name,
            "routing": routing,
            "execution": None,
            "error": result["error"]
        }

        return result

    # ========================================================
    # STAGE 6 — EXECUTION
    # ========================================================

    execution = execute_math_operation(
        operation_name,
        arguments
    )

    result[
        "routing_execution"
    ] = {
        "success": execution["success"],
        "stage": (
            "complete"
            if execution["success"]
            else "execution"
        ),
        "query": interpretation["query"],
        "operation": operation_name,
        "routing": routing,
        "execution": execution,
        "error": execution["error"]
    }

    if not execution["success"]:

        result["stage"] = "execution"

        result["error"] = (
            execution["error"]
        )

        return result

    # ========================================================
    # STAGE 7 — EXECUTION SUCCESS
    # ========================================================

    result[
        "exact_result"
    ] = execution[
        "exact_result"
    ]

    result[
        "decimal_result"
    ] = execution[
        "decimal_result"
    ]

    result[
        "warnings"
    ].extend(
        execution.get(
            "warnings",
            []
        )
    )

    # ========================================================
    # STAGE 8 — STEP GENERATION
    # ========================================================
    #
    # The Step Engine receives the same final arguments that
    # were actually sent to the deterministic executor.
    # ========================================================

    step_result = generate_steps(
        operation_name=operation_name,
        arguments=arguments,
        exact_result=result[
            "exact_result"
        ]
    )

    if step_result["success"]:

        result[
            "steps"
        ] = step_result[
            "steps"
        ]

    else:

        result[
            "warnings"
        ].append(
            "The calculation succeeded, but solution "
            "steps could not be generated."
        )

    result[
        "warnings"
    ].extend(
        step_result.get(
            "warnings",
            []
        )
    )

    # ========================================================
    # STAGE 9 — PIPELINE COMPLETE
    # ========================================================

    result["success"] = True
    result["stage"] = "complete"

    return result

import inspect

from sympy import N

from math_engine.registry import math_registry


def validate_arguments(function, arguments):
    """
    Validate supplied arguments against a function signature.

    Returns:
        {
            "valid": bool,
            "missing": [],
            "unexpected": []
        }
    """

    signature = inspect.signature(function)

    parameters = signature.parameters

    missing = []
    unexpected = []

    # --------------------------------------------------------
    # CHECK FOR MISSING REQUIRED PARAMETERS
    # --------------------------------------------------------

    for parameter_name, parameter in parameters.items():

        # Ignore *args and **kwargs.
        if parameter.kind in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD
        ):
            continue

        required = (
            parameter.default
            is inspect.Parameter.empty
        )

        if (
            required
            and parameter_name not in arguments
        ):
            missing.append(parameter_name)

    # --------------------------------------------------------
    # CHECK FOR UNEXPECTED PARAMETERS
    # --------------------------------------------------------

    accepts_kwargs = any(
        parameter.kind
        == inspect.Parameter.VAR_KEYWORD
        for parameter in parameters.values()
    )

    if not accepts_kwargs:

        for argument_name in arguments:

            if argument_name not in parameters:
                unexpected.append(
                    argument_name
                )

    return {
        "valid": (
            len(missing) == 0
            and len(unexpected) == 0
        ),
        "missing": missing,
        "unexpected": unexpected
    }


def execute_math_operation(operation_name, arguments=None):
    """
    Execute any registered SATURN math operation
    and return a standardized result dictionary.
    """

    arguments = arguments or {}

    result_data = {
        "success": False,
        "operation": operation_name,
        "subsystem": None,
        "exact_result": None,
        "decimal_result": None,
        "steps": [],
        "warnings": [],
        "error": None
    }

    # --------------------------------------------------------
    # FIND OPERATION
    # --------------------------------------------------------

    operation = math_registry.get(
        operation_name
    )

    if operation is None:
        result_data["error"] = (
            f"Unknown math operation: "
            f"'{operation_name}'"
        )

        return result_data

    result_data["subsystem"] = operation[
        "subsystem"
    ]

    # --------------------------------------------------------
    # GET FUNCTION
    # --------------------------------------------------------

    function = operation["function"]

    # --------------------------------------------------------
    # VALIDATE ARGUMENTS
    # --------------------------------------------------------

    validation = validate_arguments(
        function,
        arguments
    )

    if not validation["valid"]:

        error_parts = []

        if validation["missing"]:
            error_parts.append(
                "Missing required argument(s): "
                + ", ".join(
                    validation["missing"]
                )
            )

        if validation["unexpected"]:
            error_parts.append(
                "Unexpected argument(s): "
                + ", ".join(
                    validation["unexpected"]
                )
            )

        result_data["error"] = (
            "; ".join(error_parts)
        )

        return result_data

    # --------------------------------------------------------
    # EXECUTE OPERATION
    # --------------------------------------------------------

    try:
        result = function(
            **arguments
        )

        result_data["exact_result"] = result
        result_data["success"] = True

    except TypeError as error:
        result_data["error"] = (
            f"Invalid arguments for "
            f"'{operation_name}': {error}"
        )

        return result_data

    except Exception as error:
        result_data["error"] = (
            f"{type(error).__name__}: "
            f"{error}"
        )

        return result_data

    # --------------------------------------------------------
    # DECIMAL APPROXIMATION
    # --------------------------------------------------------

    try:
        decimal_result = N(result)

        # Only store a decimal form when SymPy
        # produces something meaningfully different.
        if decimal_result != result:
            result_data[
                "decimal_result"
            ] = decimal_result

    except Exception:
        # Some operations return lists, dictionaries,
        # strings, booleans, tuples, matrices, etc.
        # These may not have a useful decimal form.
        pass

    return result_data
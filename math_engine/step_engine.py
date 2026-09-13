def _base_step_result(operation_name):
    """
    Create the standard Step Engine result structure.
    """

    return {
        "success": False,
        "operation": operation_name,
        "steps": [],
        "warnings": [],
        "error": None
    }


def _format_value(value):
    """
    Convert values to a readable string for solution steps.
    """

    return str(value)


def _format_solution(variable, exact_result):
    """
    Format a deterministic solver result for human-readable steps.

    Examples:
        [5]      -> x = 5
        [-2, 2]  -> x = -2 or x = 2
        []       -> no solution
    """

    if isinstance(exact_result, (list, tuple)):

        if len(exact_result) == 0:
            return "no solution"

        if len(exact_result) == 1:
            return f"{variable} = {exact_result[0]}"

        return " or ".join(
            f"{variable} = {value}"
            for value in exact_result
        )

    return f"{variable} = {exact_result}"


# ============================================================
# ARITHMETIC
# ============================================================

def _steps_add(arguments, exact_result):
    """
    Generate steps for addition.
    """

    values = list(arguments.values())

    if len(values) < 2:
        return None

    left = values[0]
    right = values[1]

    return [
        f"Add the two values: {left} and {right}.",
        f"{left} + {right} = {exact_result}.",
        f"Therefore, the result is {exact_result}."
    ]


def _steps_subtract(arguments, exact_result):
    """
    Generate steps for subtraction.
    """

    a = arguments.get("a")
    b = arguments.get("b")

    if a is None or b is None:
        return None

    return [
        f"Subtract {b} from {a}.",
        f"{a} - {b} = {exact_result}.",
        f"Therefore, the result is {exact_result}."
    ]


def _steps_multiply(arguments, exact_result):
    """
    Generate steps for multiplication.
    """

    a = arguments.get("a")
    b = arguments.get("b")

    if a is None or b is None:
        return None

    return [
        f"Multiply {a} by {b}.",
        f"{a} * {b} = {exact_result}.",
        f"Therefore, the result is {exact_result}."
    ]


def _steps_divide(arguments, exact_result):
    """
    Generate steps for division.
    """

    a = arguments.get("a")
    b = arguments.get("b")

    if a is None or b is None:
        return None

    return [
        f"Divide {a} by {b}.",
        f"{a} / {b} = {exact_result}.",
        f"Therefore, the result is {exact_result}."
    ]


# ============================================================
# ALGEBRA
# ============================================================

def _steps_solve_equation(arguments, exact_result):
    """
    Generate conservative steps for equation solving.

    The universal argument extractor supplies:
        left_side
        right_side
        variable

    SATURN does not invent intermediate algebraic transformations
    unless they were explicitly produced by a deterministic
    symbolic step solver.
    """

    left_side = arguments.get(
        "left_side"
    )

    right_side = arguments.get(
        "right_side",
        0
    )

    variable = arguments.get(
        "variable",
        "x"
    )

    if left_side is None:
        return None

    equation = (
        f"{left_side} = {right_side}"
    )

    solution_text = _format_solution(
        variable,
        exact_result
    )

    return [
        f"Start with the equation {equation}.",
        f"Solve the equation for {variable} using SATURN's deterministic algebra solver.",
        f"The solution set is {exact_result}.",
        f"Therefore, {solution_text}."
    ]


# ============================================================
# GEOMETRY
# ============================================================

def _steps_circle_area(arguments, exact_result):
    """
    Generate steps for the area of a circle.
    """

    radius = arguments.get(
        "radius"
    )

    if radius is None:
        return None

    return [
        "Use the circle area formula A = pi*r**2.",
        f"Substitute r = {radius}.",
        f"A = pi*({radius})**2.",
        f"Therefore, A = {exact_result}."
    ]


def _steps_sphere_volume(arguments, exact_result):
    """
    Generate steps for the volume of a sphere.
    """

    radius = arguments.get(
        "radius"
    )

    if radius is None:
        return None

    return [
        "Use the sphere volume formula V = (4/3)*pi*r**3.",
        f"Substitute r = {radius}.",
        f"V = (4/3)*pi*({radius})**3.",
        f"Therefore, V = {exact_result}."
    ]


# ============================================================
# TRIGONOMETRY
# ============================================================

def _steps_direct_trig(arguments, exact_result, operation_name):
    """
    Generate steps for direct trigonometric function evaluation.

    This generator does not calculate independently. It explains
    the exact result already produced by SATURN's deterministic
    trigonometry subsystem.
    """

    trig_metadata = {
        "sine": {
            "display_name": "sin",
            "parameter": "angle",
            "inverse": False,
        },
        "cosine": {
            "display_name": "cos",
            "parameter": "angle",
            "inverse": False,
        },
        "tangent": {
            "display_name": "tan",
            "parameter": "angle",
            "inverse": False,
        },
        "secant": {
            "display_name": "sec",
            "parameter": "angle",
            "inverse": False,
        },
        "cosecant": {
            "display_name": "csc",
            "parameter": "angle",
            "inverse": False,
        },
        "cotangent": {
            "display_name": "cot",
            "parameter": "angle",
            "inverse": False,
        },
        "arcsine": {
            "display_name": "arcsin",
            "parameter": "value",
            "inverse": True,
        },
        "arccosine": {
            "display_name": "arccos",
            "parameter": "value",
            "inverse": True,
        },
        "arctangent": {
            "display_name": "arctan",
            "parameter": "value",
            "inverse": True,
        },
    }

    metadata = trig_metadata.get(
        operation_name
    )

    if metadata is None:
        return None

    input_value = arguments.get(
        metadata["parameter"]
    )

    if input_value is None:
        return None

    display_name = metadata["display_name"]
    expression = (
        f"{display_name}({input_value})"
    )

    if metadata["inverse"]:

        return [
            f"Evaluate {expression}.",
            f"Find the angle whose corresponding trigonometric value is {input_value}.",
            f"{expression} = {exact_result}.",
            f"Therefore, the result is {exact_result}."
        ]

    return [
        f"Evaluate {expression}.",
        "Use the exact trigonometric value for the given angle.",
        f"{expression} = {exact_result}.",
        f"Therefore, the result is {exact_result}."
    ]


def _make_direct_trig_generator(operation_name):
    """
    Create a registry-compatible wrapper for one direct trig operation.
    """

    def generator(arguments, exact_result):
        return _steps_direct_trig(
            arguments,
            exact_result,
            operation_name,
        )

    return generator


# ============================================================
# CALCULUS
# ============================================================

def _steps_derivative(arguments, exact_result):
    """
    Generate basic derivative steps.

    This generator remains conservative and does not invent
    a detailed symbolic derivation.
    """

    expression = arguments.get(
        "expression"
    )

    variable = arguments.get(
        "variable",
        "x"
    )

    if expression is None:
        return None

    return [
        f"Differentiate {expression} with respect to {variable}.",
        "Apply the appropriate differentiation rule.",
        f"d/d{variable}({expression}) = {exact_result}.",
        f"Therefore, the derivative is {exact_result}."
    ]


# ============================================================
# STEP GENERATOR REGISTRY
# ============================================================

STEP_GENERATORS = {
    "add": _steps_add,
    "subtract": _steps_subtract,
    "multiply": _steps_multiply,
    "divide": _steps_divide,
    "solve_equation": _steps_solve_equation,
    "circle_area": _steps_circle_area,
    "sphere_volume": _steps_sphere_volume,
    "derivative": _steps_derivative,

    "sine": _make_direct_trig_generator("sine"),
    "cosine": _make_direct_trig_generator("cosine"),
    "tangent": _make_direct_trig_generator("tangent"),
    "secant": _make_direct_trig_generator("secant"),
    "cosecant": _make_direct_trig_generator("cosecant"),
    "cotangent": _make_direct_trig_generator("cotangent"),
    "arcsine": _make_direct_trig_generator("arcsine"),
    "arccosine": _make_direct_trig_generator("arccosine"),
    "arctangent": _make_direct_trig_generator("arctangent"),
}


# ============================================================
# MAIN STEP ENGINE
# ============================================================

def generate_steps(
    operation_name,
    arguments=None,
    exact_result=None
):
    """
    Generate human-readable mathematical solution steps for
    a completed deterministic SATURN math operation.

    The Step Engine does not calculate the answer itself.
    It receives the already-computed exact result from the
    executor and explains the operation conservatively.

    Returns:
        {
            "success": bool,
            "operation": str,
            "steps": list,
            "warnings": list,
            "error": str or None
        }
    """

    arguments = arguments or {}

    result = _base_step_result(
        operation_name
    )

    # --------------------------------------------------------
    # UNKNOWN STEP GENERATOR
    # --------------------------------------------------------

    generator = STEP_GENERATORS.get(
        operation_name
    )

    if generator is None:

        result["warnings"].append(
            "No dedicated step generator exists for "
            f"'{operation_name}'."
        )

        result["steps"] = [
            f"Execute the deterministic operation "
            f"'{operation_name}'.",
            f"The result is {exact_result}."
        ]

        result["success"] = True

        return result

    # --------------------------------------------------------
    # GENERATE STEPS
    # --------------------------------------------------------

    try:

        steps = generator(
            arguments,
            exact_result
        )

    except Exception as error:

        result["error"] = (
            f"{type(error).__name__}: "
            f"{error}"
        )

        return result

    # --------------------------------------------------------
    # STEP GENERATION FAILED
    # --------------------------------------------------------

    if not steps:

        result["error"] = (
            "The Step Engine did not receive enough "
            "information to generate solution steps."
        )

        return result

    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    result["steps"] = steps
    result["success"] = True

    return result

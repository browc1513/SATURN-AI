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


# ============================================================
# ALGEBRA
# ============================================================

def _steps_solve_equation(arguments, exact_result):
    """
    Generate conservative steps for equation solving.

    NOVA does not claim intermediate symbolic transformations
    unless they were explicitly produced by a deterministic
    solver.
    """

    equation = arguments.get(
        "equation"
    )

    variable = arguments.get(
        "variable",
        "x"
    )

    if equation is None:
        return None

    return [
        f"Solve the equation {equation} for {variable}.",
        "Use NOVA's deterministic algebra solver to find the solution set.",
        f"The solution is {exact_result}."
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
# CALCULUS
# ============================================================

def _steps_derivative(arguments, exact_result):
    """
    Generate basic derivative steps.

    Interpreter v1 currently handles simple derivative
    expressions. This generator remains conservative and
    does not invent a detailed symbolic derivation.
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
    "solve_equation": _steps_solve_equation,
    "circle_area": _steps_circle_area,
    "sphere_volume": _steps_sphere_volume,
    "derivative": _steps_derivative,
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
    a completed deterministic NOVA math operation.

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
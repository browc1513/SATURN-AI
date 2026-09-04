from sympy import (
    sympify,
    symbols,
    pi,
    sin,
    cos,
    tan,
    asin,
    acos,
    atan,
    atan2,
    sqrt,
    simplify,
    trigsimp,
    expand_trig,
    solveset,
    S,
    Interval,
    Union,
    Eq,
    Abs,
    N
)


# ============================================================
# ANGLE FUNDAMENTALS
# ============================================================

def parse_angle(value):
    """
    Convert input into a SymPy expression.
    """
    return sympify(value)


def degrees_to_radians(degrees):
    """
    Convert degrees to radians.

    Formula:
        radians = degrees * pi / 180
    """
    degrees = parse_angle(degrees)

    return simplify(
        degrees * pi / 180
    )


def radians_to_degrees(radians):
    """
    Convert radians to degrees.

    Formula:
        degrees = radians * 180 / pi
    """
    radians = parse_angle(radians)

    return simplify(
        radians * 180 / pi
    )


def normalize_degrees(degrees):
    """
    Normalize an angle to:

        0 <= angle < 360
    """
    degrees = parse_angle(degrees)

    return simplify(
        degrees % 360
    )


def normalize_radians(radians):
    """
    Normalize an angle to:

        0 <= angle < 2*pi
    """
    radians = parse_angle(radians)

    return simplify(
        radians % (2 * pi)
    )


def coterminal_angle_degrees(
    degrees,
    rotations=1
):
    """
    Generate positive and negative coterminal angles.

    Returns:
        (positive, negative)
    """
    degrees = parse_angle(degrees)
    rotations = sympify(rotations)

    offset = 360 * rotations

    return (
        simplify(degrees + offset),
        simplify(degrees - offset)
    )


def coterminal_angle_radians(
    radians,
    rotations=1
):
    """
    Generate positive and negative coterminal angles.
    """
    radians = parse_angle(radians)
    rotations = sympify(rotations)

    offset = 2 * pi * rotations

    return (
        simplify(radians + offset),
        simplify(radians - offset)
    )


def angle_quadrant_degrees(degrees):
    """
    Determine the quadrant of an angle.

    Returns:
        1, 2, 3, 4,
        or an axis description.
    """
    angle = normalize_degrees(degrees)

    if angle == 0:
        return "positive x-axis"

    if angle == 90:
        return "positive y-axis"

    if angle == 180:
        return "negative x-axis"

    if angle == 270:
        return "negative y-axis"

    if 0 < angle < 90:
        return 1

    if 90 < angle < 180:
        return 2

    if 180 < angle < 270:
        return 3

    return 4


def reference_angle_degrees(degrees):
    """
    Calculate the reference angle in degrees.
    """
    angle = normalize_degrees(degrees)

    if angle <= 90:
        return angle

    if angle <= 180:
        return simplify(
            180 - angle
        )

    if angle <= 270:
        return simplify(
            angle - 180
        )

    return simplify(
        360 - angle
    )


def reference_angle_radians(radians):
    """
    Calculate the reference angle in radians.
    """
    normalized = normalize_radians(radians)

    if normalized <= pi / 2:
        return normalized

    if normalized <= pi:
        return simplify(
            pi - normalized
        )

    if normalized <= 3 * pi / 2:
        return simplify(
            normalized - pi
        )

    return simplify(
        2 * pi - normalized
    )


# ============================================================
# BASIC TRIGONOMETRIC FUNCTIONS
# ============================================================

def sine(angle, unit="radians"):
    """
    Calculate sine.
    """
    angle = parse_angle(angle)

    if unit == "degrees":
        angle = degrees_to_radians(angle)

    return simplify(
        sin(angle)
    )


def cosine(angle, unit="radians"):
    """
    Calculate cosine.
    """
    angle = parse_angle(angle)

    if unit == "degrees":
        angle = degrees_to_radians(angle)

    return simplify(
        cos(angle)
    )


def tangent(angle, unit="radians"):
    """
    Calculate tangent.
    """
    angle = parse_angle(angle)

    if unit == "degrees":
        angle = degrees_to_radians(angle)

    return simplify(
        tan(angle)
    )


def cosecant(angle, unit="radians"):
    """
    Calculate cosecant.

    csc(theta) = 1 / sin(theta)
    """
    result = sine(
        angle,
        unit
    )

    if result == 0:
        raise ValueError(
            "Cosecant is undefined when sine is zero."
        )

    return simplify(
        1 / result
    )


def secant(angle, unit="radians"):
    """
    Calculate secant.

    sec(theta) = 1 / cos(theta)
    """
    result = cosine(
        angle,
        unit
    )

    if result == 0:
        raise ValueError(
            "Secant is undefined when cosine is zero."
        )

    return simplify(
        1 / result
    )


def cotangent(angle, unit="radians"):
    """
    Calculate cotangent.

    cot(theta) = cos(theta) / sin(theta)
    """
    sine_value = sine(
        angle,
        unit
    )

    cosine_value = cosine(
        angle,
        unit
    )

    if sine_value == 0:
        raise ValueError(
            "Cotangent is undefined when sine is zero."
        )

    return simplify(
        cosine_value /
        sine_value
    )


# ============================================================
# INVERSE TRIGONOMETRIC FUNCTIONS
# ============================================================

def _inverse_output(
    radians_value,
    output_unit
):
    """
    Convert inverse trig result to desired unit.
    """
    if output_unit == "degrees":
        return simplify(
            radians_to_degrees(
                radians_value
            )
        )

    return simplify(
        radians_value
    )


def arcsine(
    value,
    output_unit="radians"
):
    """
    Calculate inverse sine.
    """
    value = sympify(value)

    return _inverse_output(
        asin(value),
        output_unit
    )


def arccosine(
    value,
    output_unit="radians"
):
    """
    Calculate inverse cosine.
    """
    value = sympify(value)

    return _inverse_output(
        acos(value),
        output_unit
    )


def arctangent(
    value,
    output_unit="radians"
):
    """
    Calculate inverse tangent.
    """
    value = sympify(value)

    return _inverse_output(
        atan(value),
        output_unit
    )


def arccosecant(
    value,
    output_unit="radians"
):
    """
    Calculate inverse cosecant.
    """
    value = sympify(value)

    if value == 0:
        raise ValueError(
            "Inverse cosecant is undefined for zero."
        )

    return _inverse_output(
        asin(1 / value),
        output_unit
    )


def arcsecant(
    value,
    output_unit="radians"
):
    """
    Calculate inverse secant.
    """
    value = sympify(value)

    if value == 0:
        raise ValueError(
            "Inverse secant is undefined for zero."
        )

    return _inverse_output(
        acos(1 / value),
        output_unit
    )


def arccotangent(
    value,
    output_unit="radians"
):
    """
    Principal inverse cotangent.

    Range:
        0 < angle < pi
    """
    value = sympify(value)

    if value > 0:
        result = atan(
            1 / value
        )

    elif value < 0:
        result = atan(
            1 / value
        ) + pi

    else:
        result = pi / 2

    return _inverse_output(
        result,
        output_unit
    )


# ============================================================
# UNIT CIRCLE
# ============================================================

def unit_circle_coordinates(
    angle,
    unit="radians"
):
    """
    Return the point on the unit circle:

        (cos(theta), sin(theta))
    """
    return (
        cosine(angle, unit),
        sine(angle, unit)
    )


def unit_circle_values(
    angle,
    unit="radians"
):
    """
    Return exact trig values for an angle.
    """
    sin_value = sine(
        angle,
        unit
    )

    cos_value = cosine(
        angle,
        unit
    )

    if cos_value == 0:
        tan_value = "undefined"
    else:
        tan_value = simplify(
            sin_value /
            cos_value
        )

    return {
        "sin": sin_value,
        "cos": cos_value,
        "tan": tan_value
    }


def trig_signs_by_quadrant(
    quadrant
):
    """
    Return signs of sine, cosine,
    and tangent in a quadrant.
    """
    quadrant = int(quadrant)

    signs = {
        1: {
            "sin": 1,
            "cos": 1,
            "tan": 1
        },
        2: {
            "sin": 1,
            "cos": -1,
            "tan": -1
        },
        3: {
            "sin": -1,
            "cos": -1,
            "tan": 1
        },
        4: {
            "sin": -1,
            "cos": 1,
            "tan": -1
        }
    }

    if quadrant not in signs:
        raise ValueError(
            "Quadrant must be 1, 2, 3, or 4."
        )

    return signs[quadrant]


def standard_unit_circle_angles():
    """
    Return common unit-circle angles
    in degrees and radians.
    """
    degrees = [
        0,
        30,
        45,
        60,
        90,
        120,
        135,
        150,
        180,
        210,
        225,
        240,
        270,
        300,
        315,
        330,
        360
    ]

    return [
        {
            "degrees": angle,
            "radians": degrees_to_radians(
                angle
            )
        }
        for angle in degrees
    ]


# ============================================================
# RIGHT-TRIANGLE TRIGONOMETRY
# ============================================================

def right_triangle_sine(
    opposite,
    hypotenuse
):
    """
    sin(theta) = opposite / hypotenuse
    """
    opposite = sympify(opposite)
    hypotenuse = sympify(hypotenuse)

    if hypotenuse <= 0:
        raise ValueError(
            "Hypotenuse must be positive."
        )

    return simplify(
        opposite /
        hypotenuse
    )


def right_triangle_cosine(
    adjacent,
    hypotenuse
):
    """
    cos(theta) = adjacent / hypotenuse
    """
    adjacent = sympify(adjacent)
    hypotenuse = sympify(hypotenuse)

    if hypotenuse <= 0:
        raise ValueError(
            "Hypotenuse must be positive."
        )

    return simplify(
        adjacent /
        hypotenuse
    )


def right_triangle_tangent(
    opposite,
    adjacent
):
    """
    tan(theta) = opposite / adjacent
    """
    opposite = sympify(opposite)
    adjacent = sympify(adjacent)

    if adjacent == 0:
        raise ValueError(
            "Adjacent side cannot be zero."
        )

    return simplify(
        opposite /
        adjacent
    )


def right_triangle_angle_from_sides(
    opposite,
    adjacent,
    output_unit="degrees"
):
    """
    Find an acute angle from opposite
    and adjacent sides.
    """
    opposite = sympify(opposite)
    adjacent = sympify(adjacent)

    if opposite <= 0 or adjacent <= 0:
        raise ValueError(
            "Side lengths must be positive."
        )

    angle = atan2(
        opposite,
        adjacent
    )

    return _inverse_output(
        angle,
        output_unit
    )


def right_triangle_opposite(
    angle,
    hypotenuse,
    unit="degrees"
):
    """
    Find opposite side.

    opposite = hypotenuse * sin(theta)
    """
    hypotenuse = sympify(hypotenuse)

    if hypotenuse <= 0:
        raise ValueError(
            "Hypotenuse must be positive."
        )

    return simplify(
        hypotenuse *
        sine(angle, unit)
    )


def right_triangle_adjacent(
    angle,
    hypotenuse,
    unit="degrees"
):
    """
    Find adjacent side.

    adjacent = hypotenuse * cos(theta)
    """
    hypotenuse = sympify(hypotenuse)

    if hypotenuse <= 0:
        raise ValueError(
            "Hypotenuse must be positive."
        )

    return simplify(
        hypotenuse *
        cosine(angle, unit)
    )


def solve_right_triangle(
    opposite,
    adjacent
):
    """
    Solve a right triangle from
    opposite and adjacent legs.
    """
    opposite = sympify(opposite)
    adjacent = sympify(adjacent)

    if opposite <= 0 or adjacent <= 0:
        raise ValueError(
            "Side lengths must be positive."
        )

    hypotenuse = simplify(
        sqrt(
            opposite**2 +
            adjacent**2
        )
    )

    angle_1 = right_triangle_angle_from_sides(
        opposite,
        adjacent,
        "degrees"
    )

    angle_2 = simplify(
        90 - angle_1
    )

    return {
        "opposite": opposite,
        "adjacent": adjacent,
        "hypotenuse": hypotenuse,
        "angle_1_degrees": angle_1,
        "angle_2_degrees": angle_2
    }


def angle_of_elevation(
    vertical_height,
    horizontal_distance
):
    """
    Find angle of elevation.
    """
    return right_triangle_angle_from_sides(
        vertical_height,
        horizontal_distance,
        "degrees"
    )


def angle_of_depression(
    vertical_drop,
    horizontal_distance
):
    """
    Find angle of depression.
    """
    return right_triangle_angle_from_sides(
        vertical_drop,
        horizontal_distance,
        "degrees"
    )


# ============================================================
# TRIGONOMETRIC IDENTITIES
# ============================================================

def simplify_trig(expression):
    """
    Simplify a trigonometric expression.
    """
    expression = sympify(expression)

    return trigsimp(
        expression
    )


def verify_trig_identity(
    left_side,
    right_side
):
    """
    Determine whether two trig expressions
    are symbolically equivalent.
    """
    left_side = sympify(left_side)
    right_side = sympify(right_side)

    difference = trigsimp(
        left_side -
        right_side
    )

    return difference == 0


def reciprocal_identity(
    function_name,
    angle
):
    """
    Return the reciprocal identity value.
    """
    angle = sympify(angle)

    identities = {
        "csc": 1 / sin(angle),
        "sec": 1 / cos(angle),
        "cot": cos(angle) / sin(angle)
    }

    if function_name not in identities:
        raise ValueError(
            "Function must be csc, sec, or cot."
        )

    return simplify(
        identities[function_name]
    )


def quotient_identity(
    function_name,
    angle
):
    """
    Return tangent or cotangent
    using sine and cosine.
    """
    angle = sympify(angle)

    if function_name == "tan":
        return simplify(
            sin(angle) /
            cos(angle)
        )

    if function_name == "cot":
        return simplify(
            cos(angle) /
            sin(angle)
        )

    raise ValueError(
        "Function must be tan or cot."
    )


def pythagorean_identity_sin_cos(
    angle
):
    """
    Evaluate:

        sin^2(theta) + cos^2(theta)
    """
    angle = sympify(angle)

    return trigsimp(
        sin(angle)**2 +
        cos(angle)**2
    )


def pythagorean_identity_tan_sec(
    angle
):
    """
    Evaluate:

        1 + tan^2(theta) = sec^2(theta)
    """
    angle = sympify(angle)

    return trigsimp(
        1 +
        tan(angle)**2
    )


def even_odd_identity(
    function_name,
    angle
):
    """
    Evaluate trig function at -theta.
    """
    angle = sympify(angle)

    functions = {
        "sin": sin,
        "cos": cos,
        "tan": tan
    }

    if function_name not in functions:
        raise ValueError(
            "Function must be sin, cos, or tan."
        )

    return simplify(
        functions[function_name](
            -angle
        )
    )


def cofunction_sine(angle):
    """
    sin(pi/2 - theta) = cos(theta)
    """
    angle = sympify(angle)

    return trigsimp(
        sin(
            pi / 2 - angle
        )
    )


def cofunction_cosine(angle):
    """
    cos(pi/2 - theta) = sin(theta)
    """
    angle = sympify(angle)

    return trigsimp(
        cos(
            pi / 2 - angle
        )
    )


# ============================================================
# ANGLE IDENTITIES
# ============================================================

def sine_sum(angle_a, angle_b):
    """
    sin(A + B)
    """
    angle_a = sympify(angle_a)
    angle_b = sympify(angle_b)

    return expand_trig(
        sin(angle_a + angle_b)
    )


def sine_difference(angle_a, angle_b):
    """
    sin(A - B)
    """
    angle_a = sympify(angle_a)
    angle_b = sympify(angle_b)

    return expand_trig(
        sin(angle_a - angle_b)
    )


def cosine_sum(angle_a, angle_b):
    """
    cos(A + B)
    """
    angle_a = sympify(angle_a)
    angle_b = sympify(angle_b)

    return expand_trig(
        cos(angle_a + angle_b)
    )


def cosine_difference(angle_a, angle_b):
    """
    cos(A - B)
    """
    angle_a = sympify(angle_a)
    angle_b = sympify(angle_b)

    return expand_trig(
        cos(angle_a - angle_b)
    )


def tangent_sum(angle_a, angle_b):
    """
    tan(A + B)
    """
    angle_a = sympify(angle_a)
    angle_b = sympify(angle_b)

    return simplify(
        (
            tan(angle_a) +
            tan(angle_b)
        ) /
        (
            1 -
            tan(angle_a) *
            tan(angle_b)
        )
    )


def tangent_difference(angle_a, angle_b):
    """
    tan(A - B)
    """
    angle_a = sympify(angle_a)
    angle_b = sympify(angle_b)

    return simplify(
        (
            tan(angle_a) -
            tan(angle_b)
        ) /
        (
            1 +
            tan(angle_a) *
            tan(angle_b)
        )
    )


def sine_double_angle(angle):
    """
    sin(2theta)
    """
    angle = sympify(angle)

    return expand_trig(
        sin(2 * angle)
    )


def cosine_double_angle(angle):
    """
    cos(2theta)
    """
    angle = sympify(angle)

    return expand_trig(
        cos(2 * angle)
    )


def tangent_double_angle(angle):
    """
    tan(2theta)
    """
    angle = sympify(angle)

    return simplify(
        2 * tan(angle) /
        (
            1 -
            tan(angle)**2
        )
    )


def sine_half_angle(angle):
    """
    Principal positive half-angle form.
    """
    angle = sympify(angle)

    return simplify(
        sqrt(
            (
                1 -
                cos(angle)
            ) / 2
        )
    )


def cosine_half_angle(angle):
    """
    Principal positive half-angle form.
    """
    angle = sympify(angle)

    return simplify(
        sqrt(
            (
                1 +
                cos(angle)
            ) / 2
        )
    )


def sine_power_reduction(angle):
    """
    sin^2(theta) power-reduction identity.
    """
    angle = sympify(angle)

    return simplify(
        (
            1 -
            cos(2 * angle)
        ) / 2
    )


def cosine_power_reduction(angle):
    """
    cos^2(theta) power-reduction identity.
    """
    angle = sympify(angle)

    return simplify(
        (
            1 +
            cos(2 * angle)
        ) / 2
    )


def product_to_sum_sin_sin(
    angle_a,
    angle_b
):
    """
    Convert sin(A)sin(B) to a sum.
    """
    angle_a = sympify(angle_a)
    angle_b = sympify(angle_b)

    return simplify(
        (
            cos(angle_a - angle_b) -
            cos(angle_a + angle_b)
        ) / 2
    )


def product_to_sum_cos_cos(
    angle_a,
    angle_b
):
    """
    Convert cos(A)cos(B) to a sum.
    """
    angle_a = sympify(angle_a)
    angle_b = sympify(angle_b)

    return simplify(
        (
            cos(angle_a - angle_b) +
            cos(angle_a + angle_b)
        ) / 2
    )


def sum_to_product_sine(
    angle_a,
    angle_b
):
    """
    Convert sin(A) + sin(B) to product form.
    """
    angle_a = sympify(angle_a)
    angle_b = sympify(angle_b)

    return simplify(
        2 *
        sin(
            (angle_a + angle_b) / 2
        ) *
        cos(
            (angle_a - angle_b) / 2
        )
    )


def sum_to_product_cosine(
    angle_a,
    angle_b
):
    """
    Convert cos(A) + cos(B) to product form.
    """
    angle_a = sympify(angle_a)
    angle_b = sympify(angle_b)

    return simplify(
        2 *
        cos(
            (angle_a + angle_b) / 2
        ) *
        cos(
            (angle_a - angle_b) / 2
        )
    )


# ============================================================
# TRIGONOMETRIC EQUATIONS
# ============================================================

def solve_trig_equation(
    left_side,
    right_side=0,
    variable="x",
    domain=S.Reals
):
    """
    Solve a trigonometric equation.

    Example:
        sin(x) = 1/2
    """
    variable_symbol = symbols(
        str(variable),
        real=True
    )

    locals_dict = {
        str(variable): variable_symbol
    }

    left_side = sympify(
        left_side,
        locals=locals_dict
    )

    right_side = sympify(
        right_side,
        locals=locals_dict
    )

    return solveset(
        Eq(
            left_side,
            right_side
        ),
        variable_symbol,
        domain=domain
    )


def solve_trig_interval(
    left_side,
    right_side,
    start,
    end,
    variable="x"
):
    """
    Solve a trig equation over a
    specified closed interval.
    """
    start = sympify(start)
    end = sympify(end)

    domain = Interval(
        start,
        end
    )

    return solve_trig_equation(
        left_side,
        right_side,
        variable,
        domain
    )


def solve_sine_equation(
    value,
    variable="x",
    domain=S.Reals
):
    """
    Solve:

        sin(x) = value
    """
    variable_symbol = symbols(
        str(variable),
        real=True
    )

    value = sympify(value)

    return solveset(
        Eq(
            sin(variable_symbol),
            value
        ),
        variable_symbol,
        domain=domain
    )


def solve_cosine_equation(
    value,
    variable="x",
    domain=S.Reals
):
    """
    Solve:

        cos(x) = value
    """
    variable_symbol = symbols(
        str(variable),
        real=True
    )

    value = sympify(value)

    return solveset(
        Eq(
            cos(variable_symbol),
            value
        ),
        variable_symbol,
        domain=domain
    )


def solve_tangent_equation(
    value,
    variable="x",
    domain=S.Reals
):
    """
    Solve:

        tan(x) = value
    """
    variable_symbol = symbols(
        str(variable),
        real=True
    )

    value = sympify(value)

    return solveset(
        Eq(
            tan(variable_symbol),
            value
        ),
        variable_symbol,
        domain=domain
    )


# ============================================================
# TRIG FUNCTION / GRAPH PROPERTIES
# ============================================================

def sine_graph_properties(
    A,
    B,
    C=0,
    D=0
):
    """
    Analyze:

        y = A*sin(Bx - C) + D
    """
    A = sympify(A)
    B = sympify(B)
    C = sympify(C)
    D = sympify(D)

    if B == 0:
        raise ValueError(
            "B cannot be zero."
        )

    amplitude = Abs(A)

    period = simplify(
        2 * pi /
        Abs(B)
    )

    phase_shift = simplify(
        C / B
    )

    return {
        "amplitude": amplitude,
        "period": period,
        "phase_shift": phase_shift,
        "vertical_shift": D,
        "midline": D,
        "minimum": simplify(
            D - Abs(A)
        ),
        "maximum": simplify(
            D + Abs(A)
        ),
        "domain": S.Reals,
        "range": Interval(
            D - Abs(A),
            D + Abs(A)
        )
    }


def cosine_graph_properties(
    A,
    B,
    C=0,
    D=0
):
    """
    Analyze:

        y = A*cos(Bx - C) + D
    """
    return sine_graph_properties(
        A,
        B,
        C,
        D
    )


def tangent_graph_properties(
    A,
    B,
    C=0,
    D=0
):
    """
    Analyze:

        y = A*tan(Bx - C) + D
    """
    A = sympify(A)
    B = sympify(B)
    C = sympify(C)
    D = sympify(D)

    if B == 0:
        raise ValueError(
            "B cannot be zero."
        )

    return {
        "vertical_scale": A,
        "period": simplify(
            pi /
            Abs(B)
        ),
        "phase_shift": simplify(
            C / B
        ),
        "vertical_shift": D,
        "range": S.Reals
    }


def trig_frequency(B):
    """
    Return angular frequency coefficient |B|.
    """
    B = sympify(B)

    return simplify(
        Abs(B)
    )


def evaluate_trig_function(
    function_name,
    angle,
    unit="radians",
    decimal=False
):
    """
    Evaluate a named trig function.
    """
    functions = {
        "sin": sine,
        "cos": cosine,
        "tan": tangent,
        "csc": cosecant,
        "sec": secant,
        "cot": cotangent
    }

    if function_name not in functions:
        raise ValueError(
            "Unknown trig function."
        )

    result = functions[
        function_name
    ](
        angle,
        unit
    )

    if decimal:
        return N(result)

    return result


# ============================================================
# LAW OF SINES
# ============================================================

def law_of_sines_side(
    known_side,
    known_angle,
    target_angle,
    unit="degrees"
):
    """
    Find a missing side using:

        a / sin(A) = b / sin(B)
    """
    known_side = sympify(
        known_side
    )

    if known_side <= 0:
        raise ValueError(
            "Side length must be positive."
        )

    numerator = sine(
        target_angle,
        unit
    )

    denominator = sine(
        known_angle,
        unit
    )

    if denominator == 0:
        raise ValueError(
            "Known angle produces an invalid sine value."
        )

    return simplify(
        known_side *
        numerator /
        denominator
    )


def law_of_sines_angle(
    target_side,
    known_side,
    known_angle,
    output_unit="degrees"
):
    """
    Find an angle using the Law of Sines.
    """
    target_side = sympify(
        target_side
    )

    known_side = sympify(
        known_side
    )

    ratio = simplify(
        target_side *
        sine(
            known_angle,
            "degrees"
        ) /
        known_side
    )

    angle = asin(
        ratio
    )

    return _inverse_output(
        angle,
        output_unit
    )


def law_of_sines_ssa_solutions(
    known_side,
    known_angle,
    target_side
):
    """
    Determine possible SSA angle solutions.

    Angles are interpreted in degrees.

    Returns zero, one, or two possible angles.
    """
    known_side = sympify(
        known_side
    )

    known_angle = sympify(
        known_angle
    )

    target_side = sympify(
        target_side
    )

    ratio = simplify(
        target_side *
        sine(
            known_angle,
            "degrees"
        ) /
        known_side
    )

    numeric_ratio = float(
        N(ratio)
    )

    if numeric_ratio < -1 or numeric_ratio > 1:
        return []

    angle_1 = simplify(
        radians_to_degrees(
            asin(ratio)
        )
    )

    angle_2 = simplify(
        180 - angle_1
    )

    possible = []

    if simplify(
        known_angle +
        angle_1
    ) < 180:
        possible.append(
            angle_1
        )

    if (
        angle_2 != angle_1
        and simplify(
            known_angle +
            angle_2
        ) < 180
    ):
        possible.append(
            angle_2
        )

    return possible


# ============================================================
# LAW OF COSINES
# ============================================================

def law_of_cosines_side(
    side_a,
    side_b,
    included_angle,
    unit="degrees"
):
    """
    Find the side opposite the
    included angle.

    Formula:
        c^2 = a^2 + b^2 - 2ab*cos(C)
    """
    side_a = sympify(side_a)
    side_b = sympify(side_b)

    if side_a <= 0 or side_b <= 0:
        raise ValueError(
            "Side lengths must be positive."
        )

    return simplify(
        sqrt(
            side_a**2 +
            side_b**2 -
            2 *
            side_a *
            side_b *
            cosine(
                included_angle,
                unit
            )
        )
    )


def law_of_cosines_angle(
    opposite_side,
    adjacent_side_1,
    adjacent_side_2,
    output_unit="degrees"
):
    """
    Find an angle using the Law of Cosines.
    """
    opposite_side = sympify(
        opposite_side
    )

    adjacent_side_1 = sympify(
        adjacent_side_1
    )

    adjacent_side_2 = sympify(
        adjacent_side_2
    )

    numerator = simplify(
        adjacent_side_1**2 +
        adjacent_side_2**2 -
        opposite_side**2
    )

    denominator = simplify(
        2 *
        adjacent_side_1 *
        adjacent_side_2
    )

    angle = acos(
        numerator /
        denominator
    )

    return _inverse_output(
        angle,
        output_unit
    )


# ============================================================
# GENERAL TRIANGLE SOLVER
# ============================================================

def solve_triangle_sss(
    side_a,
    side_b,
    side_c
):
    """
    Solve a triangle from SSS.
    """
    side_a = sympify(side_a)
    side_b = sympify(side_b)
    side_c = sympify(side_c)

    if (
        side_a + side_b <= side_c
        or side_a + side_c <= side_b
        or side_b + side_c <= side_a
    ):
        raise ValueError(
            "The side lengths do not form a valid triangle."
        )

    angle_a = law_of_cosines_angle(
        side_a,
        side_b,
        side_c
    )

    angle_b = law_of_cosines_angle(
        side_b,
        side_a,
        side_c
    )

    angle_c = simplify(
        180 -
        angle_a -
        angle_b
    )

    return {
        "side_a": side_a,
        "side_b": side_b,
        "side_c": side_c,
        "angle_a": angle_a,
        "angle_b": angle_b,
        "angle_c": angle_c
    }


def solve_triangle_sas(
    side_a,
    side_b,
    included_angle
):
    """
    Solve a triangle from SAS.

    included_angle is opposite the
    unknown third side.
    """
    side_c = law_of_cosines_side(
        side_a,
        side_b,
        included_angle
    )

    result = solve_triangle_sss(
        side_a,
        side_b,
        side_c
    )

    return result


def solve_triangle_asa(
    angle_a,
    angle_b,
    included_side
):
    """
    Solve ASA when included_side is side C.
    """
    angle_a = sympify(angle_a)
    angle_b = sympify(angle_b)
    included_side = sympify(
        included_side
    )

    angle_c = simplify(
        180 -
        angle_a -
        angle_b
    )

    if angle_c <= 0:
        raise ValueError(
            "Angles do not form a valid triangle."
        )

    side_a = law_of_sines_side(
        included_side,
        angle_c,
        angle_a
    )

    side_b = law_of_sines_side(
        included_side,
        angle_c,
        angle_b
    )

    return {
        "side_a": side_a,
        "side_b": side_b,
        "side_c": included_side,
        "angle_a": angle_a,
        "angle_b": angle_b,
        "angle_c": angle_c
    }


def solve_triangle_aas(
    angle_a,
    angle_b,
    side_a
):
    """
    Solve AAS from angles A, B and side A.
    """
    angle_a = sympify(angle_a)
    angle_b = sympify(angle_b)
    side_a = sympify(side_a)

    angle_c = simplify(
        180 -
        angle_a -
        angle_b
    )

    if angle_c <= 0:
        raise ValueError(
            "Angles do not form a valid triangle."
        )

    side_b = law_of_sines_side(
        side_a,
        angle_a,
        angle_b
    )

    side_c = law_of_sines_side(
        side_a,
        angle_a,
        angle_c
    )

    return {
        "side_a": side_a,
        "side_b": side_b,
        "side_c": side_c,
        "angle_a": angle_a,
        "angle_b": angle_b,
        "angle_c": angle_c
    }


def solve_triangle_ssa(
    known_side,
    known_angle,
    second_side
):
    """
    Solve the ambiguous SSA case.

    Returns all valid triangles.
    """
    possible_angles = (
        law_of_sines_ssa_solutions(
            known_side,
            known_angle,
            second_side
        )
    )

    solutions = []

    for second_angle in possible_angles:
        third_angle = simplify(
            180 -
            known_angle -
            second_angle
        )

        third_side = law_of_sines_side(
            known_side,
            known_angle,
            third_angle
        )

        solutions.append(
            {
                "side_a": known_side,
                "angle_a": known_angle,
                "side_b": second_side,
                "angle_b": second_angle,
                "side_c": third_side,
                "angle_c": third_angle
            }
        )

    return solutions


# ============================================================
# TRIANGLE AREA WITH TRIGONOMETRY
# ============================================================

def triangle_area_sas(
    side_a,
    side_b,
    included_angle,
    unit="degrees"
):
    """
    Calculate triangle area:

        A = 1/2 * a * b * sin(C)
    """
    side_a = sympify(side_a)
    side_b = sympify(side_b)

    if side_a <= 0 or side_b <= 0:
        raise ValueError(
            "Side lengths must be positive."
        )

    return simplify(
        side_a *
        side_b *
        sine(
            included_angle,
            unit
        ) /
        2
    )


# ============================================================
# POLAR COORDINATES
# ============================================================

def cartesian_to_polar(
    x,
    y,
    angle_unit="radians"
):
    """
    Convert Cartesian coordinates to polar.

    Returns:
        (r, theta)
    """
    x = sympify(x)
    y = sympify(y)

    radius = simplify(
        sqrt(
            x**2 +
            y**2
        )
    )

    angle = atan2(
        y,
        x
    )

    if angle_unit == "degrees":
        angle = radians_to_degrees(
            angle
        )

    return (
        radius,
        simplify(angle)
    )


def polar_to_cartesian(
    radius,
    angle,
    angle_unit="radians"
):
    """
    Convert polar coordinates
    to Cartesian coordinates.
    """
    radius = sympify(radius)
    angle = sympify(angle)

    if radius < 0:
        raise ValueError(
            "Radius must be nonnegative."
        )

    if angle_unit == "degrees":
        angle = degrees_to_radians(
            angle
        )

    x = simplify(
        radius *
        cos(angle)
    )

    y = simplify(
        radius *
        sin(angle)
    )

    return (
        x,
        y
    )


def polar_radius(x, y):
    """
    Calculate polar radius.
    """
    x = sympify(x)
    y = sympify(y)

    return simplify(
        sqrt(
            x**2 +
            y**2
        )
    )


def polar_angle(
    x,
    y,
    output_unit="radians"
):
    """
    Calculate polar angle using atan2.
    """
    x = sympify(x)
    y = sympify(y)

    result = atan2(
        y,
        x
    )

    if output_unit == "degrees":
        return simplify(
            radians_to_degrees(
                result
            )
        )

    return simplify(
        result
    )


# ============================================================
# VECTORS WITH TRIGONOMETRY
# ============================================================

def vector_magnitude(
    x_component,
    y_component
):
    """
    Calculate vector magnitude.
    """
    x_component = sympify(
        x_component
    )

    y_component = sympify(
        y_component
    )

    return simplify(
        sqrt(
            x_component**2 +
            y_component**2
        )
    )


def vector_direction(
    x_component,
    y_component,
    output_unit="degrees"
):
    """
    Calculate vector direction using atan2.
    """
    x_component = sympify(
        x_component
    )

    y_component = sympify(
        y_component
    )

    angle = atan2(
        y_component,
        x_component
    )

    if output_unit == "degrees":
        return simplify(
            radians_to_degrees(
                angle
            )
        )

    return simplify(
        angle
    )


def vector_components(
    magnitude,
    angle,
    angle_unit="degrees"
):
    """
    Resolve a vector into x and y components.
    """
    magnitude = sympify(magnitude)

    if magnitude < 0:
        raise ValueError(
            "Magnitude cannot be negative."
        )

    x_component = simplify(
        magnitude *
        cosine(
            angle,
            angle_unit
        )
    )

    y_component = simplify(
        magnitude *
        sine(
            angle,
            angle_unit
        )
    )

    return (
        x_component,
        y_component
    )


def vector_from_components(
    x_component,
    y_component
):
    """
    Return magnitude and direction
    from vector components.
    """
    return {
        "magnitude": vector_magnitude(
            x_component,
            y_component
        ),
        "direction_degrees": vector_direction(
            x_component,
            y_component,
            "degrees"
        ),
        "direction_radians": vector_direction(
            x_component,
            y_component,
            "radians"
        )
    }


# ============================================================
# BEARINGS AND DIRECTION ANGLES
# ============================================================

def direction_angle_to_bearing(
    direction_angle
):
    """
    Convert a standard mathematical
    direction angle to a compass bearing.

    Standard angle:
        0 degrees = East
        90 degrees = North

    Bearing:
        0 degrees = North
        increases clockwise
    """
    direction_angle = normalize_degrees(
        direction_angle
    )

    return normalize_degrees(
        90 -
        direction_angle
    )


def bearing_to_direction_angle(
    bearing
):
    """
    Convert compass bearing to standard
    mathematical direction angle.
    """
    bearing = normalize_degrees(
        bearing
    )

    return normalize_degrees(
        90 -
        bearing
    )


def vector_from_bearing(
    magnitude,
    bearing
):
    """
    Resolve a magnitude and compass bearing
    into Cartesian x/y components.
    """
    direction_angle = (
        bearing_to_direction_angle(
            bearing
        )
    )

    return vector_components(
        magnitude,
        direction_angle,
        "degrees"
    )


def bearing_from_vector(
    x_component,
    y_component
):
    """
    Calculate compass bearing
    from vector components.
    """
    direction_angle = vector_direction(
        x_component,
        y_component,
        "degrees"
    )

    return direction_angle_to_bearing(
        direction_angle
    )


# ============================================================
# TRIGONOMETRIC EXPRESSION UTILITIES
# ============================================================

def detect_trig_functions(expression):
    """
    Detect trig functions used in an expression.
    """
    expression = sympify(expression)

    detected = []

    checks = {
        "sin": sin,
        "cos": cos,
        "tan": tan
    }

    for name, function in checks.items():
        if expression.has(function):
            detected.append(name)

    return detected


def expand_trig_expression(expression):
    """
    Expand trig expressions using
    angle identities.
    """
    expression = sympify(expression)

    return expand_trig(
        expression
    )


def rewrite_trig_as_sin_cos(expression):
    """
    Rewrite trigonometric expressions
    entirely using sine and cosine.
    """
    expression = sympify(expression)

    return expression.rewrite(sin)


def exact_trig_value(
    function_name,
    angle,
    unit="degrees"
):
    """
    Return an exact trig value.
    """
    return evaluate_trig_function(
        function_name,
        angle,
        unit,
        decimal=False
    )


def decimal_trig_value(
    function_name,
    angle,
    unit="degrees",
    digits=10
):
    """
    Return numerical trig value.
    """
    exact = evaluate_trig_function(
        function_name,
        angle,
        unit,
        decimal=False
    )

    return N(
        exact,
        digits
    )


def exact_trig_value(
    function_name,
    angle,
    unit="degrees"
):
    """
    Return an exact trig value.
    """
    return evaluate_trig_function(
        function_name,
        angle,
        unit,
        decimal=False
    )


def decimal_trig_value(
    function_name,
    angle,
    unit="degrees",
    digits=10
):
    """
    Return numerical trig value.
    """
    exact = evaluate_trig_function(
        function_name,
        angle,
        unit,
        decimal=False
    )

    return N(
        exact,
        digits
    )


def rewrite_trig_as_sin_cos(expression):
    """
    Rewrite trigonometric expressions
    entirely using sine and cosine.
    """
    expression = sympify(expression)

    return expression.replace(
        lambda expr: expr.func == tan,
        lambda expr: sin(expr.args[0]) / cos(expr.args[0])
    )


def trig_expression_value(
    expression,
    substitutions=None,
    decimal=False
):
    """
    Evaluate an arbitrary trig expression.

    substitutions:
        {"x": pi/4}
    """
    expression = sympify(expression)

    if substitutions:
        for variable, value in substitutions.items():

            matching_symbols = [
                symbol
                for symbol in expression.free_symbols
                if symbol.name == str(variable)
            ]

            for symbol in matching_symbols:
                expression = expression.subs(
                    symbol,
                    sympify(value)
                )

    result = trigsimp(
        expression
    )

    if decimal:
        return N(result)

    return result
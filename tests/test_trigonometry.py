# ============================================================
# N.O.V.A. TRIGONOMETRY TEST SUITE
# ============================================================

from sympy import (
    pi,
    sqrt,
    sin,
    cos,
    tan,
    symbols,
    S,
    Interval
)

from math_engine.trigonometry import (
    # Angle fundamentals
    parse_angle,
    degrees_to_radians,
    radians_to_degrees,
    normalize_degrees,
    normalize_radians,
    coterminal_angle_degrees,
    coterminal_angle_radians,
    angle_quadrant_degrees,
    reference_angle_degrees,
    reference_angle_radians,

    # Basic trig
    sine,
    cosine,
    tangent,
    cosecant,
    secant,
    cotangent,

    # Inverse trig
    arcsine,
    arccosine,
    arctangent,
    arccosecant,
    arcsecant,
    arccotangent,

    # Unit circle
    unit_circle_coordinates,
    unit_circle_values,
    trig_signs_by_quadrant,
    standard_unit_circle_angles,

    # Right triangles
    right_triangle_sine,
    right_triangle_cosine,
    right_triangle_tangent,
    right_triangle_angle_from_sides,
    right_triangle_opposite,
    right_triangle_adjacent,
    solve_right_triangle,
    angle_of_elevation,
    angle_of_depression,

    # Identities
    simplify_trig,
    verify_trig_identity,
    reciprocal_identity,
    quotient_identity,
    pythagorean_identity_sin_cos,
    pythagorean_identity_tan_sec,
    even_odd_identity,
    cofunction_sine,
    cofunction_cosine,

    # Angle identities
    sine_sum,
    sine_difference,
    cosine_sum,
    cosine_difference,
    tangent_sum,
    tangent_difference,
    sine_double_angle,
    cosine_double_angle,
    tangent_double_angle,
    sine_half_angle,
    cosine_half_angle,
    sine_power_reduction,
    cosine_power_reduction,
    product_to_sum_sin_sin,
    product_to_sum_cos_cos,
    sum_to_product_sine,
    sum_to_product_cosine,

    # Equations
    solve_trig_equation,
    solve_trig_interval,
    solve_sine_equation,
    solve_cosine_equation,
    solve_tangent_equation,

    # Graph properties
    sine_graph_properties,
    cosine_graph_properties,
    tangent_graph_properties,
    trig_frequency,
    evaluate_trig_function,

    # Law of Sines
    law_of_sines_side,
    law_of_sines_angle,
    law_of_sines_ssa_solutions,

    # Law of Cosines
    law_of_cosines_side,
    law_of_cosines_angle,

    # Triangle solvers
    solve_triangle_sss,
    solve_triangle_sas,
    solve_triangle_asa,
    solve_triangle_aas,
    solve_triangle_ssa,

    # Triangle area
    triangle_area_sas,

    # Polar coordinates
    cartesian_to_polar,
    polar_to_cartesian,
    polar_radius,
    polar_angle,

    # Vectors
    vector_magnitude,
    vector_direction,
    vector_components,
    vector_from_components,

    # Bearings
    direction_angle_to_bearing,
    bearing_to_direction_angle,
    vector_from_bearing,
    bearing_from_vector,

    # Utilities
    detect_trig_functions,
    expand_trig_expression,
    rewrite_trig_as_sin_cos,
    exact_trig_value,
    decimal_trig_value,
    trig_expression_value
)


print("\n==============================")
print("N.O.V.A. Trigonometry Test")
print("==============================")


# ============================================================
# 1. ANGLE FUNDAMENTALS
# ============================================================

print("\nAngle Fundamentals:")

print(
    "180 degrees -> radians:",
    degrees_to_radians(180)
)

print(
    "45 degrees -> radians:",
    degrees_to_radians(45)
)

print(
    "pi radians -> degrees:",
    radians_to_degrees(pi)
)

print(
    "pi/4 radians -> degrees:",
    radians_to_degrees(pi / 4)
)

print(
    "Normalize 450 degrees ->",
    normalize_degrees(450)
)

print(
    "Normalize -90 degrees ->",
    normalize_degrees(-90)
)

print(
    "Normalize 5*pi/2 radians ->",
    normalize_radians(5 * pi / 2)
)

print(
    "Coterminal angles for 45 degrees ->",
    coterminal_angle_degrees(45)
)

print(
    "Coterminal angles for pi/4 ->",
    coterminal_angle_radians(pi / 4)
)

print(
    "Quadrant of 135 degrees ->",
    angle_quadrant_degrees(135)
)

print(
    "Quadrant of 225 degrees ->",
    angle_quadrant_degrees(225)
)

print(
    "90 degrees lies on ->",
    angle_quadrant_degrees(90)
)

print(
    "Reference angle of 150 degrees ->",
    reference_angle_degrees(150)
)

print(
    "Reference angle of 225 degrees ->",
    reference_angle_degrees(225)
)

print(
    "Reference angle of 5*pi/4 ->",
    reference_angle_radians(5 * pi / 4)
)


# ============================================================
# 2. BASIC TRIGONOMETRIC FUNCTIONS
# ============================================================

print("\nBasic Trigonometric Functions:")

print(
    "sin(30°) ->",
    sine(30, "degrees")
)

print(
    "cos(60°) ->",
    cosine(60, "degrees")
)

print(
    "tan(45°) ->",
    tangent(45, "degrees")
)

print(
    "csc(30°) ->",
    cosecant(30, "degrees")
)

print(
    "sec(60°) ->",
    secant(60, "degrees")
)

print(
    "cot(45°) ->",
    cotangent(45, "degrees")
)


# ============================================================
# 3. INVERSE TRIG
# ============================================================

print("\nInverse Trigonometric Functions:")

print(
    "arcsin(1/2) radians ->",
    arcsine("1/2")
)

print(
    "arcsin(1/2) degrees ->",
    arcsine("1/2", "degrees")
)

print(
    "arccos(1/2) degrees ->",
    arccosine("1/2", "degrees")
)

print(
    "arctan(1) degrees ->",
    arctangent(1, "degrees")
)

print(
    "arccsc(2) degrees ->",
    arccosecant(2, "degrees")
)

print(
    "arcsec(2) degrees ->",
    arcsecant(2, "degrees")
)

print(
    "arccot(1) degrees ->",
    arccotangent(1, "degrees")
)


# ============================================================
# 4. UNIT CIRCLE
# ============================================================

print("\nUnit Circle:")

print(
    "Coordinates at 0° ->",
    unit_circle_coordinates(0, "degrees")
)

print(
    "Coordinates at 30° ->",
    unit_circle_coordinates(30, "degrees")
)

print(
    "Coordinates at 45° ->",
    unit_circle_coordinates(45, "degrees")
)

print(
    "Coordinates at 90° ->",
    unit_circle_coordinates(90, "degrees")
)

print(
    "Values at 60° ->",
    unit_circle_values(60, "degrees")
)

print(
    "Values at 90° ->",
    unit_circle_values(90, "degrees")
)

print(
    "Signs in Quadrant I ->",
    trig_signs_by_quadrant(1)
)

print(
    "Signs in Quadrant II ->",
    trig_signs_by_quadrant(2)
)

print(
    "Signs in Quadrant III ->",
    trig_signs_by_quadrant(3)
)

print(
    "Signs in Quadrant IV ->",
    trig_signs_by_quadrant(4)
)

print(
    "Number of standard unit-circle entries ->",
    len(standard_unit_circle_angles())
)


# ============================================================
# 5. RIGHT-TRIANGLE TRIGONOMETRY
# ============================================================

print("\nRight-Triangle Trigonometry:")

print(
    "sin ratio opposite=3, hypotenuse=5 ->",
    right_triangle_sine(3, 5)
)

print(
    "cos ratio adjacent=4, hypotenuse=5 ->",
    right_triangle_cosine(4, 5)
)

print(
    "tan ratio opposite=3, adjacent=4 ->",
    right_triangle_tangent(3, 4)
)

print(
    "Angle with opposite=3, adjacent=3 ->",
    right_triangle_angle_from_sides(3, 3)
)

print(
    "Opposite side, hypotenuse=10, angle=30° ->",
    right_triangle_opposite(30, 10)
)

print(
    "Adjacent side, hypotenuse=10, angle=60° ->",
    right_triangle_adjacent(60, 10)
)

print(
    "Solve right triangle with legs 3 and 4 ->",
    solve_right_triangle(3, 4)
)

print(
    "Angle of elevation, height=10, distance=10 ->",
    angle_of_elevation(10, 10)
)

print(
    "Angle of depression, drop=5, distance=5 ->",
    angle_of_depression(5, 5)
)


# ============================================================
# 6. TRIG IDENTITIES
# ============================================================

print("\nTrig Identities:")

x = symbols("x", real=True)

print(
    "Simplify sin(x)^2 + cos(x)^2 ->",
    simplify_trig(
        sin(x)**2 +
        cos(x)**2
    )
)

print(
    "Verify sin^2 + cos^2 = 1 ->",
    verify_trig_identity(
        sin(x)**2 + cos(x)**2,
        1
    )
)

print(
    "csc reciprocal identity ->",
    reciprocal_identity("csc", x)
)

print(
    "sec reciprocal identity ->",
    reciprocal_identity("sec", x)
)

print(
    "cot reciprocal identity ->",
    reciprocal_identity("cot", x)
)

print(
    "tan quotient identity ->",
    quotient_identity("tan", x)
)

print(
    "cot quotient identity ->",
    quotient_identity("cot", x)
)

print(
    "Pythagorean sin/cos identity ->",
    pythagorean_identity_sin_cos(x)
)

print(
    "Pythagorean tan/sec expression ->",
    pythagorean_identity_tan_sec(x)
)

print(
    "sin(-x) ->",
    even_odd_identity("sin", x)
)

print(
    "cos(-x) ->",
    even_odd_identity("cos", x)
)

print(
    "tan(-x) ->",
    even_odd_identity("tan", x)
)

print(
    "sin(pi/2 - x) ->",
    cofunction_sine(x)
)

print(
    "cos(pi/2 - x) ->",
    cofunction_cosine(x)
)


# ============================================================
# 7. ANGLE IDENTITIES
# ============================================================

print("\nAngle Identities:")

a, b = symbols("a b", real=True)

print(
    "sin(a+b) ->",
    sine_sum(a, b)
)

print(
    "sin(a-b) ->",
    sine_difference(a, b)
)

print(
    "cos(a+b) ->",
    cosine_sum(a, b)
)

print(
    "cos(a-b) ->",
    cosine_difference(a, b)
)

print(
    "tan(a+b) ->",
    tangent_sum(a, b)
)

print(
    "tan(a-b) ->",
    tangent_difference(a, b)
)

print(
    "sin(2x) ->",
    sine_double_angle(x)
)

print(
    "cos(2x) ->",
    cosine_double_angle(x)
)

print(
    "tan(2x) ->",
    tangent_double_angle(x)
)

print(
    "sin half-angle form ->",
    sine_half_angle(x)
)

print(
    "cos half-angle form ->",
    cosine_half_angle(x)
)

print(
    "sin^2 power reduction ->",
    sine_power_reduction(x)
)

print(
    "cos^2 power reduction ->",
    cosine_power_reduction(x)
)

print(
    "sin(a)sin(b) product-to-sum ->",
    product_to_sum_sin_sin(a, b)
)

print(
    "cos(a)cos(b) product-to-sum ->",
    product_to_sum_cos_cos(a, b)
)

print(
    "sin(a)+sin(b) sum-to-product ->",
    sum_to_product_sine(a, b)
)

print(
    "cos(a)+cos(b) sum-to-product ->",
    sum_to_product_cosine(a, b)
)


# ============================================================
# 8. TRIGONOMETRIC EQUATIONS
# ============================================================

print("\nTrigonometric Equations:")

print(
    "Solve sin(x)=1/2 over all reals ->",
    solve_sine_equation("1/2")
)

print(
    "Solve cos(x)=1/2 over all reals ->",
    solve_cosine_equation("1/2")
)

print(
    "Solve tan(x)=1 over all reals ->",
    solve_tangent_equation(1)
)

print(
    "Solve sin(x)=0 from 0 to 2*pi ->",
    solve_trig_interval(
        "sin(x)",
        0,
        0,
        2 * pi
    )
)

print(
    "Solve cos(x)=0 from 0 to 2*pi ->",
    solve_trig_interval(
        "cos(x)",
        0,
        0,
        2 * pi
    )
)

print(
    "General solver: sin(x)^2=1 ->",
    solve_trig_equation(
        "sin(x)**2",
        1
    )
)


# ============================================================
# 9. GRAPH PROPERTIES
# ============================================================

print("\nTrig Graph Properties:")

print(
    "y = 2sin(3x-pi)+4 ->",
    sine_graph_properties(
        2,
        3,
        pi,
        4
    )
)

print(
    "y = 5cos(2x)+1 ->",
    cosine_graph_properties(
        5,
        2,
        0,
        1
    )
)

print(
    "y = 2tan(4x-pi)+3 ->",
    tangent_graph_properties(
        2,
        4,
        pi,
        3
    )
)

print(
    "Frequency coefficient B=-5 ->",
    trig_frequency(-5)
)

print(
    "Exact sin(45°) ->",
    evaluate_trig_function(
        "sin",
        45,
        "degrees"
    )
)

print(
    "Decimal sin(45°) ->",
    evaluate_trig_function(
        "sin",
        45,
        "degrees",
        decimal=True
    )
)


# ============================================================
# 10. LAW OF SINES
# ============================================================

print("\nLaw of Sines:")

print(
    "Known side=10 at 30°, target angle=90° ->",
    law_of_sines_side(
        10,
        30,
        90
    )
)

print(
    "Target side=10, known side=10, known angle=30° ->",
    law_of_sines_angle(
        10,
        10,
        30
    )
)

print(
    "SSA possible angles: a=10, A=30°, b=15 ->",
    law_of_sines_ssa_solutions(
        10,
        30,
        15
    )
)


# ============================================================
# 11. LAW OF COSINES
# ============================================================

print("\nLaw of Cosines:")

print(
    "Sides 3,4 with included 90° ->",
    law_of_cosines_side(
        3,
        4,
        90
    )
)

print(
    "Angle opposite side 5 in 3-4-5 triangle ->",
    law_of_cosines_angle(
        5,
        3,
        4
    )
)


# ============================================================
# 12. GENERAL TRIANGLE SOLVERS
# ============================================================

print("\nGeneral Triangle Solvers:")

print(
    "SSS 3-4-5 ->",
    solve_triangle_sss(
        3,
        4,
        5
    )
)

print(
    "SAS sides 3,4, included angle 90° ->",
    solve_triangle_sas(
        3,
        4,
        90
    )
)

print(
    "ASA angles 30°,60°, included side 10 ->",
    solve_triangle_asa(
        30,
        60,
        10
    )
)

print(
    "AAS angles 30°,60°, side A=5 ->",
    solve_triangle_aas(
        30,
        60,
        5
    )
)

print(
    "SSA a=10, A=30°, b=15 ->",
    solve_triangle_ssa(
        10,
        30,
        15
    )
)


# ============================================================
# 13. TRIANGLE AREA USING TRIG
# ============================================================

print("\nTriangle Area with Trigonometry:")

print(
    "Sides 6 and 8 with included angle 30° ->",
    triangle_area_sas(
        6,
        8,
        30
    )
)


# ============================================================
# 14. POLAR COORDINATES
# ============================================================

print("\nPolar Coordinates:")

print(
    "Cartesian (3,4) -> polar ->",
    cartesian_to_polar(
        3,
        4
    )
)

print(
    "Cartesian (1,1) -> polar degrees ->",
    cartesian_to_polar(
        1,
        1,
        "degrees"
    )
)

print(
    "Polar r=2, theta=60° -> Cartesian ->",
    polar_to_cartesian(
        2,
        60,
        "degrees"
    )
)

print(
    "Polar radius of (3,4) ->",
    polar_radius(
        3,
        4
    )
)

print(
    "Polar angle of (1,1) in degrees ->",
    polar_angle(
        1,
        1,
        "degrees"
    )
)


# ============================================================
# 15. VECTOR TRIGONOMETRY
# ============================================================

print("\nVector Trigonometry:")

print(
    "Magnitude of vector (3,4) ->",
    vector_magnitude(
        3,
        4
    )
)

print(
    "Direction of vector (1,1) ->",
    vector_direction(
        1,
        1
    )
)

print(
    "Components of magnitude 10 at 30° ->",
    vector_components(
        10,
        30
    )
)

print(
    "Vector information from components (3,4) ->",
    vector_from_components(
        3,
        4
    )
)


# ============================================================
# 16. BEARINGS AND DIRECTION ANGLES
# ============================================================

print("\nBearings and Direction Angles:")

print(
    "Direction angle 0° -> bearing ->",
    direction_angle_to_bearing(0)
)

print(
    "Direction angle 90° -> bearing ->",
    direction_angle_to_bearing(90)
)

print(
    "Bearing 0° -> direction angle ->",
    bearing_to_direction_angle(0)
)

print(
    "Bearing 90° -> direction angle ->",
    bearing_to_direction_angle(90)
)

print(
    "Vector magnitude 10 at bearing 0° ->",
    vector_from_bearing(
        10,
        0
    )
)

print(
    "Bearing of vector (0,10) ->",
    bearing_from_vector(
        0,
        10
    )
)


# ============================================================
# 17. TRIG EXPRESSION UTILITIES
# ============================================================

print("\nTrig Expression Utilities:")

print(
    "Detect functions in sin(x)+cos(x)+tan(x) ->",
    detect_trig_functions(
        sin(x) +
        cos(x) +
        tan(x)
    )
)

print(
    "Expand sin(2*x) ->",
    expand_trig_expression(
        sin(2 * x)
    )
)

print(
    "Rewrite tan(x) using sine/cosine ->",
    rewrite_trig_as_sin_cos(
        tan(x)
    )
)

print(
    "Exact cos(60°) ->",
    exact_trig_value(
        "cos",
        60
    )
)

print(
    "Decimal cos(60°) ->",
    decimal_trig_value(
        "cos",
        60
    )
)

print(
    "Evaluate sin(x)+cos(x) at x=pi/4 ->",
    trig_expression_value(
        sin(x) + cos(x),
        {
            "x": pi / 4
        }
    )
)


# ============================================================
# ERROR / VALIDATION TESTS
# ============================================================

print("\nValidation Error Tests:")

try:
    cosecant(0)
except ValueError as error:
    print(
        "Correctly caught undefined cosecant:",
        error
    )


try:
    secant(pi / 2)
except ValueError as error:
    print(
        "Correctly caught undefined secant:",
        error
    )


try:
    cotangent(0)
except ValueError as error:
    print(
        "Correctly caught undefined cotangent:",
        error
    )


try:
    trig_signs_by_quadrant(5)
except ValueError as error:
    print(
        "Correctly caught invalid quadrant:",
        error
    )


try:
    right_triangle_sine(
        3,
        -5
    )
except ValueError as error:
    print(
        "Correctly caught invalid hypotenuse:",
        error
    )


try:
    solve_triangle_sss(
        1,
        2,
        10
    )
except ValueError as error:
    print(
        "Correctly caught invalid triangle:",
        error
    )


try:
    polar_to_cartesian(
        -5,
        30,
        "degrees"
    )
except ValueError as error:
    print(
        "Correctly caught negative polar radius:",
        error
    )


try:
    trig_frequency(0)
    print(
        "Frequency coefficient of zero ->",
        trig_frequency(0)
    )
except ValueError as error:
    print(
        "Frequency error:",
        error
    )


print("\n==============================")
print("Trigonometry Test Complete")
print("==============================")
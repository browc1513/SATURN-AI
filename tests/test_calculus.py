# ============================================================
# S.A.T.U.R.N. CALCULUS TEST SUITE
# ============================================================

from sympy import (
    symbols,
    pi,
    oo,
    sin,
    cos,
    exp,
    log,
    sqrt,
    Matrix,
    Rational
)

from math_engine.calculus import (
    # Core helpers
    parse_expression,
    parse_variable,

    # Limits
    evaluate_limit,
    left_hand_limit,
    right_hand_limit,
    limit_at_infinity,
    numerical_limit,
    limit_exists,

    # Continuity
    is_continuous_at,
    discontinuity_type,

    # Derivatives
    derivative,
    first_derivative,
    second_derivative,
    nth_derivative,

    # Derivative rules
    product_rule,
    quotient_rule,
    chain_rule,

    # Special derivatives
    trig_derivative,
    exponential_derivative,
    logarithmic_derivative,
    hyperbolic_derivative,

    # Implicit / parametric
    implicit_derivative,
    parametric_derivative,
    parametric_second_derivative,

    # Derivative applications
    tangent_line,
    normal_line,
    critical_points,
    inflection_candidates,
    second_derivative_test,

    # Optimization
    optimization_candidates,
    absolute_extrema,

    # Related rates
    related_rate,

    # Linearization / differentials
    linearization,
    differential,
    differential_approximation,
    relative_error,
    percentage_error,

    # Antiderivatives
    antiderivative,
    indefinite_integral,
    check_antiderivative,

    # Definite integrals
    definite_integral,
    average_function_value,
    signed_area,

    # Integration techniques
    substitution_integral,
    integration_by_parts,
    rational_integral,
    trig_integral,

    # Improper integrals
    improper_integral,
    improper_integral_converges,

    # Numerical integration
    left_riemann_sum,
    right_riemann_sum,
    midpoint_rule,
    trapezoidal_rule,
    simpsons_rule,

    # Areas
    area_under_curve,
    area_between_curves,
    curve_intersections,

    # Volumes
    disk_volume,
    washer_volume,
    shell_volume,

    # Arc length / surface area
    arc_length,
    parametric_arc_length,
    surface_area_x_axis,

    # Sequences
    sequence_term,
    sequence_limit,
    sequence_converges,

    # Series
    partial_sum,
    infinite_series_sum,
    geometric_series_sum,
    nth_term_test,

    # Power series
    power_series_expansion,
    differentiate_power_series,
    integrate_power_series,

    # Taylor / Maclaurin
    taylor_series,
    maclaurin_series,
    taylor_polynomial,

    # Parametric calculus
    parametric_tangent_slope,
    parametric_area,

    # Polar calculus
    polar_area,
    polar_arc_length,
    polar_slope,

    # Multivariable
    evaluate_multivariable,
    level_curve,

    # Partial derivatives
    partial_derivative,
    mixed_partial_derivative,

    # Gradient
    gradient_vector,
    directional_derivative,
    tangent_plane,

    # Multivariable optimization
    multivariable_critical_points,
    hessian_matrix,
    lagrange_multipliers,

    # Multiple integrals
    double_integral,
    triple_integral,

    # Coordinate system integration
    polar_double_integral,
    cylindrical_jacobian,
    spherical_jacobian,

    # Vector calculus
    vector_function_derivative,
    vector_function_integral,
    velocity_vector,
    acceleration_vector,
    vector_divergence,
    vector_curl,

    # Line integrals
    scalar_line_integral,
    vector_line_integral,

    # Vector calculus theorem utilities
    is_conservative_field,
    fundamental_line_integral,

    # Utilities
    detect_variables,
    exact_calculus_value,
    decimal_calculus_value,
    simplify_calculus_result,
    check_derivative,
    evaluate_piecewise_calculus
)


print("\n==============================")
print("S.A.T.U.R.N. Calculus Test")
print("==============================")


x = symbols("x", real=True)
y = symbols("y", real=True)
z = symbols("z", real=True)
t = symbols("t", real=True)


# ============================================================
# 1. LIMITS
# ============================================================

print("\nLimits:")

print(
    "lim x->2 of x^2 ->",
    evaluate_limit(
        "x**2",
        "x",
        2
    )
)

print(
    "lim x->0 sin(x)/x ->",
    evaluate_limit(
        "sin(x)/x",
        "x",
        0
    )
)

print(
    "Left-hand limit 1/x at 0 ->",
    left_hand_limit(
        "1/x",
        "x",
        0
    )
)

print(
    "Right-hand limit 1/x at 0 ->",
    right_hand_limit(
        "1/x",
        "x",
        0
    )
)

print(
    "Limit at infinity of 1/x ->",
    limit_at_infinity(
        "1/x",
        "x"
    )
)

print(
    "Numerical limit sin(x)/x ->",
    numerical_limit(
        "sin(x)/x",
        "x",
        0
    )
)

print(
    "Does limit of x^2 at 2 exist? ->",
    limit_exists(
        "x**2",
        "x",
        2
    )
)

print(
    "Does limit of 1/x at 0 exist? ->",
    limit_exists(
        "1/x",
        "x",
        0
    )
)


# ============================================================
# 2. CONTINUITY
# ============================================================

print("\nContinuity:")

print(
    "x^2 continuous at x=2 ->",
    is_continuous_at(
        "x**2",
        2
    )
)

print(
    "(x^2-1)/(x-1) continuous at x=1 ->",
    is_continuous_at(
        "(x**2 - 1)/(x - 1)",
        1
    )
)

print(
    "Discontinuity type of (x^2-1)/(x-1) at 1 ->",
    discontinuity_type(
        "(x**2 - 1)/(x - 1)",
        1
    )
)

print(
    "Discontinuity type of 1/x at 0 ->",
    discontinuity_type(
        "1/x",
        0
    )
)


# ============================================================
# 3. BASIC DERIVATIVES
# ============================================================

print("\nBasic Derivatives:")

print(
    "d/dx x^3 ->",
    first_derivative(
        "x**3"
    )
)

print(
    "d²/dx² x^3 ->",
    second_derivative(
        "x**3"
    )
)

print(
    "4th derivative of x^5 ->",
    nth_derivative(
        "x**5",
        4
    )
)

print(
    "Generic derivative of x^4 order 2 ->",
    derivative(
        "x**4",
        "x",
        2
    )
)


# ============================================================
# 4. DERIVATIVE RULES
# ============================================================

print("\nDerivative Rules:")

print(
    "Product rule x^2 * sin(x) ->",
    product_rule(
        "x**2",
        "sin(x)"
    )
)

print(
    "Quotient rule x^2 / (x+1) ->",
    quotient_rule(
        "x**2",
        "x + 1"
    )
)

print(
    "Chain rule sin(x^2) ->",
    chain_rule(
        "sin(u)",
        "x**2"
    )
)


# ============================================================
# 5. SPECIAL-FUNCTION DERIVATIVES
# ============================================================

print("\nSpecial-Function Derivatives:")

print(
    "Derivative of sin(x) ->",
    trig_derivative(
        "sin(x)"
    )
)

print(
    "Derivative of exp(x) ->",
    exponential_derivative(
        "exp(x)"
    )
)

print(
    "Derivative of log(x) ->",
    logarithmic_derivative(
        "log(x)"
    )
)

print(
    "Derivative of sinh(x) ->",
    hyperbolic_derivative(
        "sinh(x)"
    )
)


# ============================================================
# 6. IMPLICIT / PARAMETRIC DIFFERENTIATION
# ============================================================

print("\nImplicit / Parametric Differentiation:")

print(
    "Implicit derivative x^2 + y^2 - 25 = 0 ->",
    implicit_derivative(
        "x**2 + y**2 - 25"
    )
)

print(
    "Parametric derivative x=t^2, y=t^3 ->",
    parametric_derivative(
        "t**2",
        "t**3"
    )
)

print(
    "Parametric second derivative x=t^2, y=t^3 ->",
    parametric_second_derivative(
        "t**2",
        "t**3"
    )
)


# ============================================================
# 7. DERIVATIVE APPLICATIONS
# ============================================================

print("\nDerivative Applications:")

print(
    "Tangent line to x^2 at x=1 ->",
    tangent_line(
        "x**2",
        1
    )
)

print(
    "Normal line to x^2 at x=1 ->",
    normal_line(
        "x**2",
        1
    )
)

print(
    "Critical points of x^3 - 3x ->",
    critical_points(
        "x**3 - 3*x"
    )
)

print(
    "Inflection candidates of x^3 ->",
    inflection_candidates(
        "x**3"
    )
)

print(
    "Second derivative test x^2 at 0 ->",
    second_derivative_test(
        "x**2",
        0
    )
)

print(
    "Second derivative test -x^2 at 0 ->",
    second_derivative_test(
        "-x**2",
        0
    )
)


# ============================================================
# 8. OPTIMIZATION
# ============================================================

print("\nOptimization:")

print(
    "Candidates for x^2 on [-2,3] ->",
    optimization_candidates(
        "x**2",
        "x",
        (-2, 3)
    )
)

print(
    "Absolute extrema of x^2 on [-2,3] ->",
    absolute_extrema(
        "x**2",
        -2,
        3
    )
)


# ============================================================
# 9. RELATED RATES
# ============================================================

print("\nRelated Rates:")

print(
    "Solve 2*x*x_rate - 10 = 0 with x=5 ->",
    related_rate(
        "2*x*x_rate - 10",
        "x_rate",
        {
            "x": 5
        }
    )
)


# ============================================================
# 10. LINEARIZATION / DIFFERENTIALS
# ============================================================

print("\nLinearization and Differentials:")

print(
    "Linearization of x^2 at x=1 ->",
    linearization(
        "x**2",
        1
    )
)

print(
    "Differential coefficient of x^3 ->",
    differential(
        "x**3"
    )
)

print(
    "dy approximation for x^2 at x=2, dx=.1 ->",
    differential_approximation(
        "x**2",
        2,
        Rational(1, 10)
    )
)

print(
    "Relative error exact=10 approx=9 ->",
    relative_error(
        10,
        9
    )
)

print(
    "Percentage error exact=10 approx=9 ->",
    percentage_error(
        10,
        9
    )
)


# ============================================================
# 11. ANTIDERIVATIVES
# ============================================================

print("\nAntiderivatives:")

print(
    "Integral of x^2 ->",
    antiderivative(
        "x**2"
    )
)

print(
    "Integral of cos(x) ->",
    indefinite_integral(
        "cos(x)"
    )
)

print(
    "Check x^3/3 as antiderivative of x^2 ->",
    check_antiderivative(
        "x**2",
        "x**3/3"
    )
)


# ============================================================
# 12. DEFINITE INTEGRALS
# ============================================================

print("\nDefinite Integrals:")

print(
    "Integral x from 0 to 2 ->",
    definite_integral(
        "x",
        0,
        2
    )
)

print(
    "Average value x^2 on [0,2] ->",
    average_function_value(
        "x**2",
        0,
        2
    )
)

print(
    "Signed area x from -1 to 1 ->",
    signed_area(
        "x",
        -1,
        1
    )
)


# ============================================================
# 13. INTEGRATION TECHNIQUES
# ============================================================

print("\nIntegration Techniques:")

print(
    "Substitution-style integral 2x*cos(x^2) ->",
    substitution_integral(
        "2*x*cos(x**2)"
    )
)

print(
    "Integration by parts x * exp(x) ->",
    integration_by_parts(
        "x",
        "exp(x)"
    )
)

print(
    "Rational integral 1/(x+1) ->",
    rational_integral(
        "1/(x+1)"
    )
)

print(
    "Trig integral sin(x) ->",
    trig_integral(
        "sin(x)"
    )
)


# ============================================================
# 14. IMPROPER INTEGRALS
# ============================================================

print("\nImproper Integrals:")

print(
    "Integral exp(-x) from 0 to infinity ->",
    improper_integral(
        "exp(-x)",
        0,
        oo
    )
)

print(
    "Does integral exp(-x) converge? ->",
    improper_integral_converges(
        "exp(-x)",
        0,
        oo
    )
)

print(
    "Does integral 1/x from 1 to infinity converge? ->",
    improper_integral_converges(
        "1/x",
        1,
        oo
    )
)


# ============================================================
# 15. NUMERICAL INTEGRATION
# ============================================================

print("\nNumerical Integration:")

print(
    "Left Riemann sum x on [0,1], n=4 ->",
    left_riemann_sum(
        "x",
        0,
        1,
        4
    )
)

print(
    "Right Riemann sum x on [0,1], n=4 ->",
    right_riemann_sum(
        "x",
        0,
        1,
        4
    )
)

print(
    "Midpoint rule x^2 on [0,1], n=4 ->",
    midpoint_rule(
        "x**2",
        0,
        1,
        4
    )
)

print(
    "Trapezoidal rule x^2 on [0,1], n=4 ->",
    trapezoidal_rule(
        "x**2",
        0,
        1,
        4
    )
)

print(
    "Simpson's rule x^2 on [0,1], n=4 ->",
    simpsons_rule(
        "x**2",
        0,
        1,
        4
    )
)


# ============================================================
# 16. AREA APPLICATIONS
# ============================================================

print("\nArea Applications:")

print(
    "Area under y=x from -1 to 1 ->",
    area_under_curve(
        "x",
        -1,
        1
    )
)

print(
    "Area between y=x and y=x^2 on [0,1] ->",
    area_between_curves(
        "x",
        "x**2",
        0,
        1
    )
)

print(
    "Intersections of x and x^2 ->",
    curve_intersections(
        "x",
        "x**2"
    )
)


# ============================================================
# 17. VOLUME APPLICATIONS
# ============================================================

print("\nVolume Applications:")

print(
    "Disk volume radius=x, [0,1] ->",
    disk_volume(
        "x",
        0,
        1
    )
)

print(
    "Washer volume outer=2, inner=1, [0,1] ->",
    washer_volume(
        2,
        1,
        0,
        1
    )
)

print(
    "Shell volume radius=x, height=1, [0,1] ->",
    shell_volume(
        "x",
        1,
        0,
        1
    )
)


# ============================================================
# 18. ARC LENGTH / SURFACE AREA
# ============================================================

print("\nArc Length and Surface Area:")

print(
    "Arc length y=0 from 0 to 5 ->",
    arc_length(
        0,
        0,
        5
    )
)

print(
    "Parametric arc length x=t, y=0, 0 to 5 ->",
    parametric_arc_length(
        "t",
        0,
        0,
        5
    )
)

print(
    "Surface area revolving y=1 about x-axis, 0 to 2 ->",
    surface_area_x_axis(
        1,
        0,
        2
    )
)


# ============================================================
# 19. SEQUENCES
# ============================================================

print("\nSequences:")

print(
    "5th term of 1/n ->",
    sequence_term(
        "1/n",
        5
    )
)

print(
    "Limit of 1/n ->",
    sequence_limit(
        "1/n"
    )
)

print(
    "Does 1/n converge? ->",
    sequence_converges(
        "1/n"
    )
)

print(
    "Does n converge? ->",
    sequence_converges(
        "n"
    )
)


# ============================================================
# 20. INFINITE SERIES
# ============================================================

print("\nInfinite Series:")

print(
    "Partial sum 1/n, n=1..4 ->",
    partial_sum(
        "1/n",
        1,
        4
    )
)

print(
    "Infinite sum 1/2^n from n=1 ->",
    infinite_series_sum(
        "1/2**n",
        1
    )
)

print(
    "Geometric series a=1, r=1/2 ->",
    geometric_series_sum(
        1,
        Rational(1, 2)
    )
)

print(
    "Nth-term condition for 1/n ->",
    nth_term_test(
        "1/n"
    )
)

print(
    "Nth-term condition for 1 ->",
    nth_term_test(
        1
    )
)


# ============================================================
# 21. POWER SERIES
# ============================================================

print("\nPower Series:")

print(
    "Power series of exp(x), order 5 ->",
    power_series_expansion(
        "exp(x)",
        "x",
        0,
        5
    )
)

print(
    "Differentiate power series x + x^2 + x^3 ->",
    differentiate_power_series(
        "x + x**2 + x**3"
    )
)

print(
    "Integrate power series 1 + x + x^2 ->",
    integrate_power_series(
        "1 + x + x**2"
    )
)


# ============================================================
# 22. TAYLOR / MACLAURIN SERIES
# ============================================================

print("\nTaylor / Maclaurin Series:")

print(
    "Taylor series of exp(x) about x=1 ->",
    taylor_series(
        "exp(x)",
        1,
        4
    )
)

print(
    "Maclaurin series of sin(x) ->",
    maclaurin_series(
        "sin(x)",
        6
    )
)

print(
    "Taylor polynomial degree 4 of exp(x) at 0 ->",
    taylor_polynomial(
        "exp(x)",
        0,
        4
    )
)


# ============================================================
# 23. PARAMETRIC CALCULUS
# ============================================================

print("\nParametric Calculus:")

print(
    "Slope x=t^2, y=t^3 at t=1 ->",
    parametric_tangent_slope(
        "t**2",
        "t**3",
        1
    )
)

print(
    "Parametric area x=t, y=t^2, 0 to 1 ->",
    parametric_area(
        "t",
        "t**2",
        0,
        1
    )
)


# ============================================================
# 24. POLAR CALCULUS
# ============================================================

print("\nPolar Calculus:")

print(
    "Polar area r=1, theta 0 to 2pi ->",
    polar_area(
        1,
        0,
        2 * pi
    )
)

print(
    "Polar arc length r=1, theta 0 to 2pi ->",
    polar_arc_length(
        1,
        0,
        2 * pi
    )
)

print(
    "Polar slope r=1 ->",
    polar_slope(
        1
    )
)


# ============================================================
# 25. MULTIVARIABLE FUNCTIONS
# ============================================================

print("\nMultivariable Functions:")

print(
    "Evaluate x^2+y^2 at x=3,y=4 ->",
    evaluate_multivariable(
        "x**2 + y**2",
        {
            "x": 3,
            "y": 4
        }
    )
)

print(
    "Level curve x^2+y^2=25 ->",
    level_curve(
        "x**2 + y**2",
        25
    )
)


# ============================================================
# 26. PARTIAL DERIVATIVES
# ============================================================

print("\nPartial Derivatives:")

print(
    "Partial d/dx of x^2*y ->",
    partial_derivative(
        "x**2*y",
        "x"
    )
)

print(
    "Second partial d²/dx² of x^3*y ->",
    partial_derivative(
        "x**3*y",
        "x",
        2
    )
)

print(
    "Mixed partial d/dy d/dx of x^2*y^3 ->",
    mixed_partial_derivative(
        "x**2*y**3",
        ["x", "y"]
    )
)


# ============================================================
# 27. GRADIENT / DIRECTIONAL DERIVATIVES
# ============================================================

print("\nGradient and Directional Derivatives:")

print(
    "Gradient of x^2+y^2 ->",
    gradient_vector(
        "x**2 + y**2"
    )
)

print(
    "Directional derivative of x+y along (1,1) ->",
    directional_derivative(
        "x + y",
        [1, 1]
    )
)

print(
    "Tangent plane to z=x^2+y^2 at (1,1) ->",
    tangent_plane(
        "x**2 + y**2",
        (1, 1)
    )
)


# ============================================================
# 28. MULTIVARIABLE OPTIMIZATION
# ============================================================

print("\nMultivariable Optimization:")

print(
    "Critical points of x^2+y^2 ->",
    multivariable_critical_points(
        "x**2 + y**2"
    )
)

print(
    "Hessian of x^2+y^2 ->",
    hessian_matrix(
        "x**2 + y**2"
    )
)

print(
    "Lagrange multipliers maximize/minimize x+y with x^2+y^2-1=0 ->",
    lagrange_multipliers(
        "x + y",
        "x**2 + y**2 - 1"
    )
)


# ============================================================
# 29. MULTIPLE INTEGRALS
# ============================================================

print("\nMultiple Integrals:")

print(
    "Double integral 1 over x=[0,1], y=[0,2] ->",
    double_integral(
        1,
        (0, 1),
        (0, 2)
    )
)

print(
    "Triple integral 1 over unit cube ->",
    triple_integral(
        1,
        (0, 1),
        (0, 1),
        (0, 1)
    )
)


# ============================================================
# 30. COORDINATE-SYSTEM INTEGRATION
# ============================================================

print("\nCoordinate-System Integration:")

print(
    "Polar integral 1 over unit disk ->",
    polar_double_integral(
        1,
        (0, 1),
        (0, 2 * pi)
    )
)

print(
    "Cylindrical Jacobian r ->",
    cylindrical_jacobian(
        symbols("r")
    )
)

print(
    "Spherical Jacobian r=2, phi=pi/2 ->",
    spherical_jacobian(
        2,
        pi / 2
    )
)


# ============================================================
# 31. VECTOR CALCULUS
# ============================================================

print("\nVector Calculus:")

print(
    "Derivative of vector <t^2,t^3> ->",
    vector_function_derivative(
        ["t**2", "t**3"]
    )
)

print(
    "Integral of vector <t,t^2> ->",
    vector_function_integral(
        ["t", "t**2"]
    )
)

print(
    "Velocity for r(t)=<t^2,t^3> ->",
    velocity_vector(
        ["t**2", "t**3"]
    )
)

print(
    "Acceleration for r(t)=<t^2,t^3> ->",
    acceleration_vector(
        ["t**2", "t**3"]
    )
)

print(
    "Divergence of <x,y,z> ->",
    vector_divergence(
        ["x", "y", "z"]
    )
)

print(
    "Curl of <-y,x,0> ->",
    vector_curl(
        ["-y", "x", "0"]
    )
)


# ============================================================
# 32. LINE INTEGRALS
# ============================================================

print("\nLine Integrals:")

print(
    "Scalar line integral field=1 along r(t)=<t,0>, 0..2 ->",
    scalar_line_integral(
        1,
        ["t", "0"],
        0,
        2
    )
)

print(
    "Vector line integral F=<x,y> along r(t)=<t,t>, 0..1 ->",
    vector_line_integral(
        ["x", "y"],
        ["t", "t"],
        0,
        1
    )
)


# ============================================================
# 33. VECTOR CALCULUS THEOREM UTILITIES
# ============================================================

print("\nVector Calculus Theorem Utilities:")

print(
    "Is field <2x,2y,2z> conservative? ->",
    is_conservative_field(
        ["2*x", "2*y", "2*z"]
    )
)

print(
    "Fundamental line integral f=x^2+y^2 from (0,0) to (3,4) ->",
    fundamental_line_integral(
        "x**2 + y**2",
        (0, 0),
        (3, 4),
        ("x", "y")
    )
)


# ============================================================
# 34. CALCULUS UTILITIES
# ============================================================

print("\nCalculus Utilities:")

print(
    "Detect variables in x^2+y*z ->",
    detect_variables(
        "x**2 + y*z"
    )
)

print(
    "Exact value sqrt(8) ->",
    exact_calculus_value(
        "sqrt(8)"
    )
)

print(
    "Decimal value pi ->",
    decimal_calculus_value(
        pi
    )
)

print(
    "Simplify (x^2-1)/(x-1) ->",
    simplify_calculus_result(
        "(x**2 - 1)/(x - 1)"
    )
)

print(
    "Check derivative of x^3 is 3x^2 ->",
    check_derivative(
        "x**3",
        "3*x**2"
    )
)

print(
    "Evaluate Piecewise((x,x<0),(x^2,True)) at x=-2 ->",
    evaluate_piecewise_calculus(
        "Piecewise((x, x < 0), (x**2, True))",
        -2
    )
)


# ============================================================
# VALIDATION / ERROR TESTS
# ============================================================

print("\nValidation Error Tests:")

try:
    simpsons_rule(
        "x**2",
        0,
        1,
        3
    )

except ValueError as error:
    print(
        "Correctly caught odd Simpson interval count:",
        error
    )


try:
    geometric_series_sum(
        1,
        2
    )

except ValueError as error:
    print(
        "Correctly caught divergent geometric series:",
        error
    )


try:
    directional_derivative(
        "x + y",
        [0, 0]
    )

except ValueError as error:
    print(
        "Correctly caught zero direction vector:",
        error
    )


try:
    vector_curl(
        ["x", "y"]
    )

except ValueError as error:
    print(
        "Correctly caught invalid curl dimension:",
        error
    )


print("\n==============================")
print("Calculus Test Complete")
print("==============================")
from math_engine.algebra import (
    simplify_expression,
    expand_expression,
    factor_expression,
    substitute,
    solve_equation,
    find_roots,
    solve_system,
    solve_real,
    solve_inequality,
    polynomial_degree,
    polynomial_coefficients,
    quadratic_formula,
    complete_square,
    rational_simplify,
    combine_rational,
    partial_fraction,
    solve_exponential,
    solve_logarithmic,
    logarithm,
    find_domain,
    find_x_intercepts,
    find_y_intercept,
    inverse_function,
    polynomial_division,
    polynomial_remainder,
    polynomial_gcd,
    solve_absolute_value,
    evaluate_piecewise,
    solve_piecewise,
    get_numerator,
    get_denominator,
    leading_coefficient,
    polynomial_terms,
    detect_variables,
    solve_system_advanced,
    classify_system_solution,
    excluded_values,
    valid_domain,
    find_range
)


print("\n==============================")
print("S.A.T.U.R.N. Algebra Test")
print("==============================\n")


# Simplification
print("Simplification:")
print(
    "(x^2 - 1)/(x - 1) =",
    simplify_expression("(x**2 - 1)/(x - 1)")
)


# Expansion
print("\nExpansion:")
print(
    "(x + 2)(x + 3) =",
    expand_expression("(x + 2)*(x + 3)")
)


# Factoring
print("\nFactoring:")
print(
    "x^2 - 9 =",
    factor_expression("x**2 - 9")
)


# Substitution
print("\nSubstitution:")
print(
    "x^2 + 2x at x = 3 ->",
    substitute("x**2 + 2*x", "x", 3)
)


# Solve Linear Equation
print("\nSolve Linear Equation:")
print(
    "3x + 7 = 22 ->",
    solve_equation("3*x + 7", 22, "x")
)


# Solve Quadratic Equation
print("\nSolve Quadratic Equation:")
print(
    "x^2 - 5x + 6 = 0 ->",
    solve_equation("x**2 - 5*x + 6", 0, "x")
)


# Find Roots
print("\nFind Roots:")
print(
    "Roots of x^2 - 9 ->",
    find_roots("x**2 - 9", "x")
)


# Solve System of Equations
print("\nSolve System:")
system_solution = solve_system(
    [
        "x + y - 5",
        "x - y - 1"
    ],
    ["x", "y"]
)

print("x + y = 5")
print("x - y = 1")
print("Solution:", system_solution)


# Solve Over Real Numbers
print("\nSolve Over Real Numbers:")
print(
    "x^2 - 4 = 0 ->",
    solve_real("x**2 - 4", "x")
)


# No Real Solution Test
print("\nNo Real Solution Test:")
print(
    "x^2 + 1 = 0 over the reals ->",
    solve_real("x**2 + 1", "x")
)


# Inequalities
print("\nSolve Inequalities:")

print(
    "x > 3 ->",
    solve_inequality("x > 3", "x")
)

print(
    "2*x + 1 <= 7 ->",
    solve_inequality("2*x + 1 <= 7", "x")
)

print(
    "x^2 < 4 ->",
    solve_inequality("x**2 < 4", "x")
)


# Polynomial Degree
print("\nPolynomial Degree:")
print(
    "Degree of 3*x^4 + 2*x^2 - 1 ->",
    polynomial_degree("3*x**4 + 2*x**2 - 1", "x")
)


# Polynomial Coefficients
print("\nPolynomial Coefficients:")
print(
    "Coefficients of 3*x^2 + 2*x - 5 ->",
    polynomial_coefficients("3*x**2 + 2*x - 5", "x")
)


# Quadratic Formula
print("\nQuadratic Formula:")
print(
    "x^2 - 5x + 6 = 0 ->",
    quadratic_formula(1, -5, 6)
)

print(
    "x^2 + 1 = 0 ->",
    quadratic_formula(1, 0, 1)
)


# Complete the Square
print("\nComplete the Square:")
print(
    "x^2 + 6x + 5 ->",
    complete_square("x**2 + 6*x + 5", "x")
)

print(
    "2*x^2 + 8*x + 3 ->",
    complete_square("2*x**2 + 8*x + 3", "x")
)


# Rational Expression Simplification
print("\nRational Simplification:")
print(
    "(x^2 - 1)/(x - 1) ->",
    rational_simplify("(x**2 - 1)/(x - 1)")
)


# Combine Rational Expressions
print("\nCombine Rational Expressions:")
print(
    "1/x + 1/(x + 1) ->",
    combine_rational("1/x + 1/(x + 1)")
)


# Partial Fraction Decomposition
print("\nPartial Fraction Decomposition:")
print(
    "1/(x*(x + 1)) ->",
    partial_fraction("1/(x*(x + 1))", "x")
)

print(
    "(3*x + 5)/(x**2 + 3*x + 2) ->",
    partial_fraction(
        "(3*x + 5)/(x**2 + 3*x + 2)",
        "x"
    )
)


# Exponential Equations
print("\nExponential Equations:")

print(
    "2^x = 8 ->",
    solve_exponential("2**x", 8, "x")
)

print(
    "3^(x + 1) = 27 ->",
    solve_exponential("3**(x + 1)", 27, "x")
)


# Logarithmic Equations
print("\nLogarithmic Equations:")

print(
    "ln(x) = 0 ->",
    solve_logarithmic("log(x)", 0, "x")
)

print(
    "ln(x) = 2 ->",
    solve_logarithmic("log(x)", 2, "x")
)


# Logarithms
print("\nLogarithms:")

print(
    "ln(E) =",
    logarithm("E")
)

print(
    "log base 2 of 8 =",
    logarithm(8, 2)
)

print(
    "log base 10 of 1000 =",
    logarithm(1000, 10)
)


# ============================================================
# FUNCTION ANALYSIS
# ============================================================

print("\nFunction Analysis:")

print(
    "Domain of 1/(x - 2) ->",
    find_domain("1/(x - 2)", "x")
)

print(
    "x-intercepts of x^2 - 4 ->",
    find_x_intercepts("x**2 - 4", "x")
)

print(
    "y-intercept of x^2 + 3x + 5 ->",
    find_y_intercept("x**2 + 3*x + 5", "x")
)

print(
    "Inverse of 2x + 3 ->",
    inverse_function("2*x + 3", "x")
)


# ============================================================
# POLYNOMIAL TOOLS
# ============================================================

print("\nPolynomial Tools:")

print(
    "(x^2 - 1) / (x - 1) ->",
    polynomial_division(
        "x**2 - 1",
        "x - 1",
        "x"
    )
)

print(
    "Remainder of (x^2 + 1) / (x - 1) ->",
    polynomial_remainder(
        "x**2 + 1",
        "x - 1",
        "x"
    )
)

print(
    "Polynomial GCD ->",
    polynomial_gcd(
        "x**2 - 1",
        "x**2 - 2*x + 1",
        "x"
    )
)


# ============================================================
# ABSOLUTE VALUE EQUATIONS
# ============================================================

print("\nAbsolute Value Equations:")

print(
    "|x - 3| = 5 ->",
    solve_absolute_value(
        "Abs(x - 3)",
        5,
        "x"
    )
)


# ============================================================
# PIECEWISE FUNCTIONS
# ============================================================

print("\nPiecewise Functions:")

piecewise_expression = (
    "Piecewise((x**2, x < 0), "
    "(x + 1, True))"
)

print(
    "Piecewise at x = -2 ->",
    evaluate_piecewise(
        piecewise_expression,
        "x",
        -2
    )
)

print(
    "Piecewise at x = 3 ->",
    evaluate_piecewise(
        piecewise_expression,
        "x",
        3
    )
)

piecewise_equation = (
    "Piecewise((x + 1, x < 0), "
    "(x - 2, True))"
)

print(
    "Solve piecewise = 0 ->",
    solve_piecewise(
        piecewise_equation,
        0,
        "x"
    )
)


# ============================================================
# EXPRESSION INSPECTION
# ============================================================

print("\nExpression Inspection:")

print(
    "Numerator of (x + 1)/(x - 2) ->",
    get_numerator(
        "(x + 1)/(x - 2)"
    )
)

print(
    "Denominator of (x + 1)/(x - 2) ->",
    get_denominator(
        "(x + 1)/(x - 2)"
    )
)

print(
    "Leading coefficient of 5x^3 - 2x + 1 ->",
    leading_coefficient(
        "5*x**3 - 2*x + 1",
        "x"
    )
)

print(
    "Polynomial terms of 3x^2 + 2x - 5 ->",
    polynomial_terms(
        "3*x**2 + 2*x - 5",
        "x"
    )
)

print(
    "Variables in x^2 + y*z ->",
    detect_variables(
        "x**2 + y*z"
    )
)


# ============================================================
# ADVANCED SYSTEM SOLVING
# ============================================================

print("\nAdvanced System Solving:")

print(
    "Nonlinear system ->",
    solve_system_advanced(
        [
            "x**2 + y**2 - 5",
            "x - y - 1"
        ],
        ["x", "y"]
    )
)

print(
    "Unique system classification ->",
    classify_system_solution(
        [
            "x + y - 5",
            "x - y - 1"
        ],
        ["x", "y"]
    )
)

print(
    "No-solution system classification ->",
    classify_system_solution(
        [
            "x + y - 1",
            "x + y - 2"
        ],
        ["x", "y"]
    )
)


# ============================================================
# DOMAIN RESTRICTIONS
# ============================================================

print("\nDomain Restrictions:")

print(
    "Excluded values of (x + 1)/(x^2 - 4) ->",
    excluded_values(
        "(x + 1)/(x**2 - 4)",
        "x"
    )
)

print(
    "Valid domain of sqrt(x - 2) ->",
    valid_domain(
        "sqrt(x - 2)",
        "x"
    )
)

print(
    "Valid domain of log(x) ->",
    valid_domain(
        "log(x)",
        "x"
    )
)


# ============================================================
# FUNCTION RANGE
# ============================================================

print("\nFunction Range:")

print(
    "Range of x^2 ->",
    find_range(
        "x**2",
        "x"
    )
)

print(
    "Range of x^2 + 3 ->",
    find_range(
        "x**2 + 3",
        "x"
    )
)


print("\n==============================")
print("Algebra Test Complete")
print("==============================")
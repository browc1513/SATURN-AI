"""
N.O.V.A. Algebra Subsystem

Provides symbolic algebra operations for the N.O.V.A. math engine.

This subsystem uses SymPy so expressions and solutions remain exact
whenever possible.
"""

from sympy import (
    sympify,
    symbols,
    simplify,
    expand,
    factor,
    solve,
    solveset,
    Eq,
    S,
    solve_univariate_inequality,
    Poly,
    cancel,
    together,
    apart,
    log,
    Abs,
    Piecewise,
    fraction,
    gcd,
    LC,
    FiniteSet,
)

from sympy.calculus.util import continuous_domain, function_range


# ============================================================
# INPUT PARSING
# ============================================================

def parse_expression(expression):
    """
    Convert input into a SymPy expression.

    Examples:
        "x**2 + 2*x + 1"
        "(x + 1)*(x - 1)"
    """

    return sympify(expression)


def parse_variable(variable):
    """
    Convert a variable name into a SymPy symbol.

    Example:
        "x" -> Symbol('x')
    """

    return symbols(str(variable))


# ============================================================
# SIMPLIFY EXPRESSIONS
# ============================================================

def simplify_expression(expression):
    """
    Simplify an algebraic expression.

    Example:
        simplify_expression("(x**2 - 1)/(x - 1)")
        -> x + 1
    """

    expression = parse_expression(expression)

    return simplify(expression)


# ============================================================
# EXPAND EXPRESSIONS
# ============================================================

def expand_expression(expression):
    """
    Expand an algebraic expression.

    Example:
        expand_expression("(x + 2)*(x + 3)")
        -> x**2 + 5*x + 6
    """

    expression = parse_expression(expression)

    return expand(expression)


# ============================================================
# FACTOR EXPRESSIONS
# ============================================================

def factor_expression(expression):
    """
    Factor an algebraic expression.

    Example:
        factor_expression("x**2 - 9")
        -> (x - 3)*(x + 3)
    """

    expression = parse_expression(expression)

    return factor(expression)


# ============================================================
# SUBSTITUTION
# ============================================================

def substitute(expression, variable, value):
    """
    Substitute a value into an expression.

    Example:
        substitute("x**2 + 2*x", "x", 3)
        -> 15
    """

    expression = parse_expression(expression)
    variable = parse_variable(variable)
    value = parse_expression(value)

    return expression.subs(variable, value)


# ============================================================
# SOLVE EQUATIONS
# ============================================================

def solve_equation(left_side, right_side=0, variable="x"):
    """
    Solve an equation for a specified variable.

    Example:
        solve_equation("3*x + 7", 22, "x")
        -> [5]
    """

    left_side = parse_expression(left_side)
    right_side = parse_expression(right_side)
    variable = parse_variable(variable)

    equation = Eq(left_side, right_side)

    return solve(equation, variable)


# ============================================================
# FIND ROOTS
# ============================================================

def find_roots(expression, variable="x"):
    """
    Find the roots of an expression.

    This solves:

        expression = 0

    Example:
        find_roots("x**2 - 9")
        -> [-3, 3]
    """

    expression = parse_expression(expression)
    variable = parse_variable(variable)

    return solve(expression, variable)


# ============================================================
# SOLVE SYSTEM OF EQUATIONS
# ============================================================

def solve_system(equations, variables):
    """
    Solve a system of algebraic equations.

    equations:
        List of expressions or equations assumed equal to zero.

    variables:
        List of variable names.

    Example:

        solve_system(
            [
                "x + y - 5",
                "x - y - 1"
            ],
            ["x", "y"]
        )

        -> {x: 3, y: 2}
    """

    parsed_equations = [
        parse_expression(equation)
        for equation in equations
    ]

    parsed_variables = [
        parse_variable(variable)
        for variable in variables
    ]

    return solve(
        parsed_equations,
        parsed_variables,
        dict=True
    )


# ============================================================
# SOLVE OVER REAL NUMBERS
# ============================================================

def solve_real(expression, variable="x"):
    """
    Solve an equation over the real numbers.

    Assumes:

        expression = 0

    Example:
        solve_real("x**2 - 4")
        -> {-2, 2}
    """

    expression = parse_expression(expression)
    variable = parse_variable(variable)

    return solveset(
        expression,
        variable,
        domain=S.Reals
    )


# ============================================================
# SOLVE INEQUALITIES
# ============================================================

def solve_inequality(inequality, variable="x"):
    """
    Solve a single-variable inequality over the real numbers.

    Examples:
        solve_inequality("x > 3")
        -> 3 < x

        solve_inequality("x**2 < 4")
        -> (-2 < x) & (x < 2)
    """

    inequality = sympify(inequality)
    variable = parse_variable(variable)

    return solve_univariate_inequality(
        inequality,
        variable
    )


# ============================================================
# POLYNOMIAL DEGREE
# ============================================================

def polynomial_degree(expression, variable="x"):
    """
    Return the degree of a polynomial.

    Example:
        polynomial_degree("3*x**4 + 2*x**2 - 1")
        -> 4
    """

    expression = parse_expression(expression)
    variable = parse_variable(variable)

    polynomial = Poly(expression, variable)

    return polynomial.degree()


# ============================================================
# POLYNOMIAL COEFFICIENTS
# ============================================================

def polynomial_coefficients(expression, variable="x"):
    """
    Return the coefficients of a polynomial from highest
    power to lowest power.

    Example:
        polynomial_coefficients("3*x**2 + 2*x - 5")
        -> [3, 2, -5]
    """

    expression = parse_expression(expression)
    variable = parse_variable(variable)

    polynomial = Poly(expression, variable)

    return polynomial.all_coeffs()


# ============================================================
# QUADRATIC FORMULA
# ============================================================

def quadratic_formula(a, b, c):
    """
    Solve a quadratic equation using the quadratic formula.

    Equation:
        a*x**2 + b*x + c = 0

    Returns both roots exactly when possible.

    Example:
        quadratic_formula(1, -5, 6)
        -> [3, 2]
    """

    a = parse_expression(a)
    b = parse_expression(b)
    c = parse_expression(c)

    if a == 0:
        raise ValueError(
            "The coefficient 'a' cannot be zero for a quadratic equation."
        )

    discriminant = b**2 - 4*a*c

    root_1 = simplify(
        (-b + discriminant**(S.Half)) / (2*a)
    )

    root_2 = simplify(
        (-b - discriminant**(S.Half)) / (2*a)
    )

    return [root_1, root_2]


# ============================================================
# COMPLETE THE SQUARE
# ============================================================

def complete_square(expression, variable="x"):
    """
    Rewrite a quadratic expression in completed-square form.

    Example:
        complete_square("x**2 + 6*x + 5")
        -> (x + 3)**2 - 4
    """

    expression = expand(parse_expression(expression))
    variable = parse_variable(variable)

    polynomial = Poly(expression, variable)

    if polynomial.degree() != 2:
        raise ValueError(
            "Completing the square requires a quadratic expression."
        )

    a = polynomial.coeff_monomial(variable**2)
    b = polynomial.coeff_monomial(variable)
    c = polynomial.coeff_monomial(1)

    h = simplify(b / (2*a))
    k = simplify(c - (b**2 / (4*a)))

    return simplify(
        a * (variable + h)**2 + k
    )


# ============================================================
# RATIONAL EXPRESSIONS
# ============================================================

def rational_simplify(expression):
    """
    Simplify a rational algebraic expression by cancelling
    common factors.

    Example:
        rational_simplify("(x**2 - 1)/(x - 1)")
        -> x + 1
    """

    expression = parse_expression(expression)

    return cancel(expression)


def combine_rational(expression):
    """
    Combine a rational expression into a single fraction.

    Example:
        combine_rational("1/x + 1/(x + 1)")
        -> (2*x + 1)/(x*(x + 1))
    """

    expression = parse_expression(expression)

    return together(expression)


def partial_fraction(expression, variable="x"):
    """
    Decompose a rational expression into partial fractions.

    Example:
        partial_fraction(
            "1/(x*(x + 1))",
            "x"
        )
        -> 1/x - 1/(x + 1)
    """

    expression = parse_expression(expression)
    variable = parse_variable(variable)

    return apart(expression, variable)


# ============================================================
# EXPONENTIAL EQUATIONS
# ============================================================

def solve_exponential(left_side, right_side, variable="x"):
    """
    Solve an exponential equation.

    Example:
        solve_exponential("2**x", 8, "x")
        -> [3]
    """

    left_side = parse_expression(left_side)
    right_side = parse_expression(right_side)
    variable = parse_variable(variable)

    equation = Eq(left_side, right_side)

    return solve(equation, variable)


# ============================================================
# LOGARITHMIC EQUATIONS
# ============================================================

def solve_logarithmic(left_side, right_side, variable="x"):
    """
    Solve a logarithmic equation.

    Example:
        solve_logarithmic("log(x)", 0, "x")
        -> [1]
    """

    left_side = parse_expression(left_side)
    right_side = parse_expression(right_side)
    variable = parse_variable(variable)

    equation = Eq(left_side, right_side)

    return solve(equation, variable)


# ============================================================
# CHANGE OF BASE
# ============================================================

def logarithm(value, base=None):
    """
    Evaluate or represent a logarithm.

    If no base is provided, the natural logarithm is used.

    Examples:
        logarithm("E") -> 1
        logarithm(8, 2) -> 3
    """

    value = parse_expression(value)

    if base is None:
        return log(value)

    base = parse_expression(base)

    if base <= 0 or base == 1:
        raise ValueError(
            "Logarithm base must be positive and cannot equal 1."
        )

    return simplify(
        log(value) / log(base)
    )


# ============================================================
# FUNCTION ANALYSIS
# ============================================================

def find_domain(expression, variable="x"):
    """
    Find the real-valued domain of an expression.

    Example:
        find_domain("1/(x - 2)")
        -> Union(Interval.open(-oo, 2), Interval.open(2, oo))
    """

    expression = parse_expression(expression)
    variable = parse_variable(variable)

    return continuous_domain(
        expression,
        variable,
        S.Reals
    )


def find_x_intercepts(expression, variable="x"):
    """
    Find the x-intercepts of an expression.

    These are the values of x where the expression equals zero.

    Example:
        find_x_intercepts("x**2 - 4")
        -> [-2, 2]
    """

    expression = parse_expression(expression)
    variable = parse_variable(variable)

    return solve(
        Eq(expression, 0),
        variable
    )


def find_y_intercept(expression, variable="x"):
    """
    Find the y-intercept of an expression.

    The y-intercept occurs when x = 0.

    Example:
        find_y_intercept("x**2 + 3*x + 5")
        -> 5
    """

    expression = parse_expression(expression)
    variable = parse_variable(variable)

    return simplify(
        expression.subs(variable, 0)
    )


def inverse_function(expression, variable="x", output_variable="y"):
    """
    Solve for the inverse of a function.

    Example:
        inverse_function("2*x + 3")
        -> (x - 3)/2
    """

    expression = parse_expression(expression)
    variable = parse_variable(variable)
    output_variable = parse_variable(output_variable)

    equation = Eq(
        output_variable,
        expression
    )

    solutions = solve(
        equation,
        variable
    )

    if not solutions:
        return []

    inverse_solutions = []

    for solution in solutions:
        inverse_solutions.append(
            simplify(
                solution.subs(
                    output_variable,
                    variable
                )
            )
        )

    if len(inverse_solutions) == 1:
        return inverse_solutions[0]

    return inverse_solutions


# ============================================================
# POLYNOMIAL TOOLS
# ============================================================

def polynomial_division(dividend, divisor, variable="x"):
    """
    Divide one polynomial by another.

    Returns:
        quotient, remainder

    Example:
        polynomial_division(
            "x**2 - 1",
            "x - 1"
        )
        -> (x + 1, 0)
    """

    dividend = parse_expression(dividend)
    divisor = parse_expression(divisor)
    variable = parse_variable(variable)

    dividend_poly = Poly(
        dividend,
        variable
    )

    divisor_poly = Poly(
        divisor,
        variable
    )

    quotient, remainder = divmod(
        dividend_poly,
        divisor_poly
    )

    return (
        quotient.as_expr(),
        remainder.as_expr()
    )


def polynomial_remainder(dividend, divisor, variable="x"):
    """
    Return only the remainder from polynomial division.

    Example:
        polynomial_remainder(
            "x**2 + 1",
            "x - 1"
        )
        -> 2
    """

    quotient, remainder = polynomial_division(
        dividend,
        divisor,
        variable
    )

    return remainder


def polynomial_gcd(expression_1, expression_2, variable="x"):
    """
    Find the greatest common divisor of two polynomials.

    Example:
        polynomial_gcd(
            "x**2 - 1",
            "x**2 - 2*x + 1"
        )
        -> x - 1
    """

    expression_1 = parse_expression(
        expression_1
    )

    expression_2 = parse_expression(
        expression_2
    )

    variable = parse_variable(variable)

    poly_1 = Poly(
        expression_1,
        variable
    )

    poly_2 = Poly(
        expression_2,
        variable
    )

    result = gcd(
        poly_1,
        poly_2
    )

    return result.as_expr()


# ============================================================
# ABSOLUTE VALUE EQUATIONS
# ============================================================

def solve_absolute_value(left_side, right_side=0, variable="x"):
    """
    Solve an equation containing absolute values.

    Example:
        solve_absolute_value(
            "Abs(x - 3)",
            5
        )
        -> [-2, 8]
    """

    variable = symbols(
        str(variable),
        real=True
    )

    left_side = sympify(
        left_side,
        locals={str(variable): variable}
    )

    right_side = sympify(
        right_side,
        locals={str(variable): variable}
    )

    equation = Eq(
        left_side,
        right_side
    )

    return solve(
        equation,
        variable
    )


# ============================================================
# PIECEWISE FUNCTIONS
# ============================================================

def evaluate_piecewise(expression, variable, value):
    """
    Evaluate a piecewise function at a given input.

    The expression should be provided as a valid
    SymPy Piecewise expression.

    Example:
        evaluate_piecewise(
            "Piecewise((x**2, x < 0), (x + 1, True))",
            "x",
            -2
        )
        -> 4
    """

    expression = parse_expression(
        expression
    )

    variable = parse_variable(variable)

    value = parse_expression(value)

    return simplify(
        expression.subs(
            variable,
            value
        )
    )


def solve_piecewise(expression, right_side=0, variable="x"):
    """
    Solve a piecewise expression.

    Example:
        solve_piecewise(
            "Piecewise((x + 1, x < 0), (x - 2, True))",
            0
        )
    """

    expression = parse_expression(
        expression
    )

    right_side = parse_expression(
        right_side
    )

    variable = parse_variable(variable)

    equation = Eq(
        expression,
        right_side
    )

    return solve(
        equation,
        variable
    )


# ============================================================
# EXPRESSION INSPECTION
# ============================================================

def get_numerator(expression):
    """
    Return the numerator of an expression.

    Example:
        get_numerator("(x + 1)/(x - 2)")
        -> x + 1
    """

    expression = together(
        parse_expression(expression)
    )

    numerator, denominator = fraction(
        expression
    )

    return numerator


def get_denominator(expression):
    """
    Return the denominator of an expression.

    Example:
        get_denominator("(x + 1)/(x - 2)")
        -> x - 2
    """

    expression = together(
        parse_expression(expression)
    )

    numerator, denominator = fraction(
        expression
    )

    return denominator


def leading_coefficient(expression, variable="x"):
    """
    Return the leading coefficient of a polynomial.

    Example:
        leading_coefficient("5*x**3 - 2*x + 1")
        -> 5
    """

    expression = parse_expression(expression)
    variable = parse_variable(variable)

    polynomial = Poly(
        expression,
        variable
    )

    return polynomial.LC()


def polynomial_terms(expression, variable="x"):
    """
    Return polynomial terms and their coefficients.

    Example:
        polynomial_terms("3*x**2 + 2*x - 5")
    """

    expression = parse_expression(expression)
    variable = parse_variable(variable)

    polynomial = Poly(
        expression,
        variable
    )

    return polynomial.terms()


def detect_variables(expression):
    """
    Return all symbolic variables found in an expression.

    Example:
        detect_variables("x**2 + y*z")
        -> {x, y, z}
    """

    expression = parse_expression(expression)

    return expression.free_symbols


# ============================================================
# ADVANCED SYSTEM SOLVING
# ============================================================

def solve_system_advanced(equations, variables):
    """
    Solve linear or nonlinear systems of equations.

    Returns solutions as dictionaries whenever possible.

    Example:
        solve_system_advanced(
            [
                "x**2 + y**2 - 5",
                "x - y - 1"
            ],
            ["x", "y"]
        )
    """

    parsed_equations = [
        parse_expression(equation)
        for equation in equations
    ]

    parsed_variables = [
        parse_variable(variable)
        for variable in variables
    ]

    return solve(
        parsed_equations,
        parsed_variables,
        dict=True
    )


def classify_system_solution(equations, variables):
    """
    Attempt to classify a system as:

        "no solution"
        "unique solution"
        "multiple or infinite solutions"

    This is a simple symbolic classifier.
    """

    solutions = solve_system_advanced(
        equations,
        variables
    )

    if solutions == []:
        return "no solution"

    if len(solutions) == 1:
        solution = solutions[0]

        if len(solution) == len(variables):
            return "unique solution"

    return "multiple or infinite solutions"


# ============================================================
# DOMAIN RESTRICTIONS
# ============================================================

def excluded_values(expression, variable="x"):
    """
    Find values excluded because they make the denominator zero.

    This is especially useful for rational expressions.

    Example:
        excluded_values(
            "(x + 1)/(x**2 - 4)"
        )
        -> [-2, 2]
    """

    expression = together(
        parse_expression(expression)
    )

    variable = parse_variable(variable)

    numerator, denominator = fraction(
        expression
    )

    return solve(
        Eq(denominator, 0),
        variable
    )


def valid_domain(expression, variable="x"):
    """
    Return the real continuous domain of an expression.

    Useful for rational, logarithmic, radical,
    and other restricted expressions.
    """

    expression = parse_expression(expression)

    variable = parse_variable(variable)

    return continuous_domain(
        expression,
        variable,
        S.Reals
    )


# ============================================================
# FUNCTION RANGE
# ============================================================

def find_range(expression, variable="x"):
    """
    Attempt to find the real range of a function.

    Example:
        find_range("x**2")
        -> Interval(0, oo)

    Note:
        Symbolic range analysis may not succeed for
        every possible function.
    """

    expression = parse_expression(expression)

    variable = parse_variable(variable)

    return function_range(
        expression,
        variable,
        S.Reals
    )
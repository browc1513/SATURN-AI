from sympy import (
    sympify,
    symbols,
    Symbol,
    Eq,
    S,
    oo,
    pi,
    E,
    Abs,
    sqrt,
    sin,
    cos,
    tan,
    exp,
    log,
    diff,
    integrate,
    limit,
    solveset,
    solve,
    simplify,
    factor,
    cancel,
    together,
    Interval,
    Union,
    FiniteSet,
    Matrix,
    Sum,
    summation,
    series,
    factorial,
    lambdify,
    N,
    Derivative,
    Integral,
    Piecewise,
    hessian,
)


def parse_expression(expression, variables=None):
    """
    Convert input into a SymPy expression.
    """
    locals_dict = {}

    if variables:
        for variable in variables:
            locals_dict[str(variable)] = symbols(
                str(variable),
                real=True
            )

    return sympify(
        expression,
        locals=locals_dict
    )


def parse_variable(variable="x"):
    """
    Create a real SymPy variable.
    """
    return symbols(
        str(variable),
        real=True
    )


# ============================================================
# LIMITS
# ============================================================

def evaluate_limit(
    expression,
    variable="x",
    point=0,
    direction="+-"
):
    variable = parse_variable(variable)

    expression = sympify(
        expression,
        locals={str(variable): variable}
    )

    return limit(
        expression,
        variable,
        sympify(point),
        dir=direction
    )


def left_hand_limit(
    expression,
    variable="x",
    point=0
):
    return evaluate_limit(
        expression,
        variable,
        point,
        "-"
    )


def right_hand_limit(
    expression,
    variable="x",
    point=0
):
    return evaluate_limit(
        expression,
        variable,
        point,
        "+"
    )


def limit_at_infinity(
    expression,
    variable="x",
    direction="positive"
):
    point = (
        oo
        if direction == "positive"
        else -oo
    )

    return evaluate_limit(
        expression,
        variable,
        point
    )


def numerical_limit(
    expression,
    variable="x",
    point=0,
    digits=10
):
    return N(
        evaluate_limit(
            expression,
            variable,
            point
        ),
        digits
    )


def limit_exists(
    expression,
    variable="x",
    point=0
):
    left = left_hand_limit(
        expression,
        variable,
        point
    )

    right = right_hand_limit(
        expression,
        variable,
        point
    )

    return simplify(left - right) == 0


# ============================================================
# CONTINUITY
# ============================================================

def is_continuous_at(
    expression,
    point,
    variable="x"
):
    variable = parse_variable(variable)

    expression = sympify(
        expression,
        locals={str(variable): variable}
    )

    function_value = expression.subs(
        variable,
        sympify(point)
    )

    try:
        function_limit = limit(
            expression,
            variable,
            sympify(point)
        )
    except Exception:
        return False

    return simplify(
        function_value -
        function_limit
    ) == 0


def discontinuity_type(
    expression,
    point,
    variable="x"
):
    variable = parse_variable(variable)

    expression = sympify(
        expression,
        locals={str(variable): variable}
    )

    left = limit(
        expression,
        variable,
        point,
        dir="-"
    )

    right = limit(
        expression,
        variable,
        point,
        dir="+"
    )

    if left in (oo, -oo) or right in (oo, -oo):
        return "infinite"

    if simplify(left - right) != 0:
        return "jump"

    function_value = expression.subs(
        variable,
        point
    )

    if function_value.has(oo) or function_value is S.NaN:
        return "removable"

    if simplify(function_value - left) != 0:
        return "removable"

    return "continuous"


# ============================================================
# BASIC DERIVATIVES
# ============================================================

def derivative(
    expression,
    variable="x",
    order=1
):
    variable = parse_variable(variable)

    expression = sympify(
        expression,
        locals={str(variable): variable}
    )

    return simplify(
        diff(
            expression,
            variable,
            int(order)
        )
    )


def first_derivative(
    expression,
    variable="x"
):
    return derivative(
        expression,
        variable,
        1
    )


def second_derivative(
    expression,
    variable="x"
):
    return derivative(
        expression,
        variable,
        2
    )


def nth_derivative(
    expression,
    order,
    variable="x"
):
    return derivative(
        expression,
        variable,
        order
    )


# ============================================================
# DERIVATIVE RULES
# ============================================================

def product_rule(
    first,
    second,
    variable="x"
):
    variable = parse_variable(variable)

    first = sympify(
        first,
        locals={str(variable): variable}
    )

    second = sympify(
        second,
        locals={str(variable): variable}
    )

    return simplify(
        diff(first, variable) * second +
        first * diff(second, variable)
    )


def quotient_rule(
    numerator,
    denominator,
    variable="x"
):
    variable = parse_variable(variable)

    numerator = sympify(
        numerator,
        locals={str(variable): variable}
    )

    denominator = sympify(
        denominator,
        locals={str(variable): variable}
    )

    return simplify(
        (
            diff(numerator, variable) *
            denominator -
            numerator *
            diff(denominator, variable)
        ) /
        denominator**2
    )


def chain_rule(
    outer_expression,
    inner_expression,
    outer_variable="u",
    variable="x"
):
    x = parse_variable(variable)
    u = parse_variable(outer_variable)

    outer_expression = sympify(
        outer_expression,
        locals={str(u): u}
    )

    inner_expression = sympify(
        inner_expression,
        locals={str(x): x}
    )

    return simplify(
        diff(
            outer_expression,
            u
        ).subs(
            u,
            inner_expression
        ) *
        diff(
            inner_expression,
            x
        )
    )


# ============================================================
# SPECIAL FUNCTION DERIVATIVES
# ============================================================

def trig_derivative(
    expression,
    variable="x"
):
    return derivative(
        expression,
        variable
    )


def exponential_derivative(
    expression,
    variable="x"
):
    return derivative(
        expression,
        variable
    )


def logarithmic_derivative(
    expression,
    variable="x"
):
    return derivative(
        expression,
        variable
    )


def hyperbolic_derivative(
    expression,
    variable="x"
):
    return derivative(
        expression,
        variable
    )


# ============================================================
# IMPLICIT / PARAMETRIC DIFFERENTIATION
# ============================================================

def implicit_derivative(
    equation,
    dependent="y",
    independent="x"
):
    x = parse_variable(independent)
    y = symbols(str(dependent))

    equation = sympify(
        equation,
        locals={
            str(independent): x,
            str(dependent): y
        }
    )

    y_prime = symbols("y_prime")

    differentiated = diff(
        equation,
        x
    ) + diff(
        equation,
        y
    ) * y_prime

    result = solve(
        Eq(
            differentiated,
            0
        ),
        y_prime
    )

    if not result:
        return None

    return simplify(
        result[0]
    )


def parametric_derivative(
    x_expression,
    y_expression,
    parameter="t"
):
    t = parse_variable(parameter)

    x_expression = sympify(
        x_expression,
        locals={str(t): t}
    )

    y_expression = sympify(
        y_expression,
        locals={str(t): t}
    )

    dx_dt = diff(
        x_expression,
        t
    )

    dy_dt = diff(
        y_expression,
        t
    )

    return simplify(
        dy_dt / dx_dt
    )


def parametric_second_derivative(
    x_expression,
    y_expression,
    parameter="t"
):
    t = parse_variable(parameter)

    first = parametric_derivative(
        x_expression,
        y_expression,
        parameter
    )

    dx_dt = diff(
        sympify(
            x_expression,
            locals={str(t): t}
        ),
        t
    )

    return simplify(
        diff(
            first,
            t
        ) /
        dx_dt
    )


# ============================================================
# DERIVATIVE APPLICATIONS
# ============================================================

def tangent_line(
    expression,
    point,
    variable="x"
):
    x = parse_variable(variable)

    expression = sympify(
        expression,
        locals={str(x): x}
    )

    x0 = sympify(point)

    y0 = simplify(
        expression.subs(
            x,
            x0
        )
    )

    slope = simplify(
        diff(
            expression,
            x
        ).subs(
            x,
            x0
        )
    )

    return simplify(
        y0 +
        slope *
        (x - x0)
    )


def normal_line(
    expression,
    point,
    variable="x"
):
    x = parse_variable(variable)

    expression = sympify(
        expression,
        locals={str(x): x}
    )

    x0 = sympify(point)

    y0 = expression.subs(
        x,
        x0
    )

    tangent_slope = diff(
        expression,
        x
    ).subs(
        x,
        x0
    )

    if tangent_slope == 0:
        return Eq(
            x,
            x0
        )

    normal_slope = simplify(
        -1 /
        tangent_slope
    )

    return simplify(
        y0 +
        normal_slope *
        (x - x0)
    )


def critical_points(
    expression,
    variable="x"
):
    x = parse_variable(variable)

    derivative_expression = derivative(
        expression,
        variable
    )

    return solveset(
        Eq(
            derivative_expression,
            0
        ),
        x,
        domain=S.Reals
    )


def inflection_candidates(
    expression,
    variable="x"
):
    x = parse_variable(variable)

    second = second_derivative(
        expression,
        variable
    )

    return solveset(
        Eq(
            second,
            0
        ),
        x,
        domain=S.Reals
    )


def second_derivative_test(
    expression,
    point,
    variable="x"
):
    x = parse_variable(variable)

    second = second_derivative(
        expression,
        variable
    )

    value = simplify(
        second.subs(
            x,
            point
        )
    )

    if value > 0:
        return "local minimum"

    if value < 0:
        return "local maximum"

    return "inconclusive"


# ============================================================
# OPTIMIZATION
# ============================================================

def optimization_candidates(
    expression,
    variable="x",
    interval=None
):
    x = parse_variable(variable)

    expression = sympify(
        expression,
        locals={str(x): x}
    )

    candidates = list(
        solveset(
            Eq(
                diff(
                    expression,
                    x
                ),
                0
            ),
            x,
            domain=S.Reals
        )
    )

    if interval is not None:
        start = sympify(
            interval[0]
        )

        end = sympify(
            interval[1]
        )

        candidates.extend(
            [start, end]
        )

    return candidates


def absolute_extrema(
    expression,
    start,
    end,
    variable="x"
):
    x = parse_variable(variable)

    expression = sympify(
        expression,
        locals={str(x): x}
    )

    candidates = optimization_candidates(
        expression,
        variable,
        (start, end)
    )

    values = {
        point: simplify(
            expression.subs(
                x,
                point
            )
        )
        for point in candidates
    }

    minimum_point = min(
        values,
        key=lambda p: float(
            N(values[p])
        )
    )

    maximum_point = max(
        values,
        key=lambda p: float(
            N(values[p])
        )
    )

    return {
        "minimum": (
            minimum_point,
            values[minimum_point]
        ),
        "maximum": (
            maximum_point,
            values[maximum_point]
        )
    }


# ============================================================
# RELATED RATES
# ============================================================

def related_rate(
    equation,
    solve_for_rate,
    substitutions
):
    """
    Solve a differentiated relation.

    Example inputs may contain symbols
    representing dx/dt, dy/dt, etc.
    """
    equation = sympify(
        equation
    )

    solve_for_rate = symbols(
        str(solve_for_rate)
    )

    differentiated = equation.subs(
        {
            symbols(str(k)): sympify(v)
            for k, v
            in substitutions.items()
        }
    )

    result = solve(
        differentiated,
        solve_for_rate
    )

    return result


# ============================================================
# LINEARIZATION / DIFFERENTIALS
# ============================================================

def linearization(
    expression,
    point,
    variable="x"
):
    return tangent_line(
        expression,
        point,
        variable
    )


def differential(
    expression,
    variable="x"
):
    x = parse_variable(variable)

    return derivative(
        expression,
        variable
    )


def differential_approximation(
    expression,
    point,
    delta_x,
    variable="x"
):
    x = parse_variable(variable)

    derivative_value = derivative(
        expression,
        variable
    ).subs(
        x,
        point
    )

    return simplify(
        derivative_value *
        sympify(delta_x)
    )


def relative_error(
    exact_value,
    approximate_value
):
    exact_value = sympify(
        exact_value
    )

    approximate_value = sympify(
        approximate_value
    )

    return simplify(
        Abs(
            exact_value -
            approximate_value
        ) /
        Abs(exact_value)
    )


def percentage_error(
    exact_value,
    approximate_value
):
    return simplify(
        100 *
        relative_error(
            exact_value,
            approximate_value
        )
    )


# ============================================================
# ANTIDERIVATIVES
# ============================================================

def antiderivative(
    expression,
    variable="x"
):
    x = parse_variable(variable)

    expression = sympify(
        expression,
        locals={str(x): x}
    )

    return integrate(
        expression,
        x
    )


def indefinite_integral(
    expression,
    variable="x"
):
    return antiderivative(
        expression,
        variable
    )


def check_antiderivative(
    integrand,
    candidate,
    variable="x"
):
    x = parse_variable(variable)

    integrand = sympify(
        integrand,
        locals={str(x): x}
    )

    candidate = sympify(
        candidate,
        locals={str(x): x}
    )

    return simplify(
        diff(
            candidate,
            x
        ) -
        integrand
    ) == 0


# ============================================================
# DEFINITE INTEGRALS
# ============================================================

def definite_integral(
    expression,
    lower,
    upper,
    variable="x"
):
    x = parse_variable(variable)

    expression = sympify(
        expression,
        locals={str(x): x}
    )

    return simplify(
        integrate(
            expression,
            (
                x,
                sympify(lower),
                sympify(upper)
            )
        )
    )


def average_function_value(
    expression,
    lower,
    upper,
    variable="x"
):
    lower = sympify(lower)
    upper = sympify(upper)

    return simplify(
        definite_integral(
            expression,
            lower,
            upper,
            variable
        ) /
        (upper - lower)
    )


def signed_area(
    expression,
    lower,
    upper,
    variable="x"
):
    return definite_integral(
        expression,
        lower,
        upper,
        variable
    )


# ============================================================
# INTEGRATION TECHNIQUES
# ============================================================

def substitution_integral(
    expression,
    variable="x"
):
    return antiderivative(
        expression,
        variable
    )


def integration_by_parts(
    u,
    dv,
    variable="x"
):
    x = parse_variable(variable)

    u = sympify(
        u,
        locals={str(x): x}
    )

    dv = sympify(
        dv,
        locals={str(x): x}
    )

    v = integrate(
        dv,
        x
    )

    return simplify(
        u * v -
        integrate(
            v *
            diff(
                u,
                x
            ),
            x
        )
    )


def rational_integral(
    expression,
    variable="x"
):
    return antiderivative(
        expression,
        variable
    )


def trig_integral(
    expression,
    variable="x"
):
    return antiderivative(
        expression,
        variable
    )


# ============================================================
# IMPROPER INTEGRALS
# ============================================================

def improper_integral(
    expression,
    lower,
    upper,
    variable="x"
):
    return definite_integral(
        expression,
        lower,
        upper,
        variable
    )


def improper_integral_converges(
    expression,
    lower,
    upper,
    variable="x"
):
    result = improper_integral(
        expression,
        lower,
        upper,
        variable
    )

    return (
        result != oo
        and result != -oo
        and not result.has(oo)
    )


# ============================================================
# NUMERICAL INTEGRATION
# ============================================================

def left_riemann_sum(
    expression,
    lower,
    upper,
    rectangles,
    variable="x"
):
    x = parse_variable(variable)

    expression = sympify(
        expression,
        locals={str(x): x}
    )

    lower = sympify(lower)
    upper = sympify(upper)

    n = int(rectangles)

    dx = (
        upper -
        lower
    ) / n

    total = 0

    for i in range(n):
        point = (
            lower +
            i * dx
        )

        total += expression.subs(
            x,
            point
        )

    return simplify(
        total * dx
    )


def right_riemann_sum(
    expression,
    lower,
    upper,
    rectangles,
    variable="x"
):
    x = parse_variable(variable)

    expression = sympify(
        expression,
        locals={str(x): x}
    )

    lower = sympify(lower)
    upper = sympify(upper)

    n = int(rectangles)

    dx = (
        upper -
        lower
    ) / n

    total = 0

    for i in range(1, n + 1):
        point = (
            lower +
            i * dx
        )

        total += expression.subs(
            x,
            point
        )

    return simplify(
        total * dx
    )


def midpoint_rule(
    expression,
    lower,
    upper,
    rectangles,
    variable="x"
):
    x = parse_variable(variable)

    expression = sympify(
        expression,
        locals={str(x): x}
    )

    lower = sympify(lower)
    upper = sympify(upper)

    n = int(rectangles)

    dx = (
        upper -
        lower
    ) / n

    total = 0

    for i in range(n):
        midpoint = (
            lower +
            (i + sympify("1/2")) *
            dx
        )

        total += expression.subs(
            x,
            midpoint
        )

    return simplify(
        total * dx
    )


def trapezoidal_rule(
    expression,
    lower,
    upper,
    intervals,
    variable="x"
):
    x = parse_variable(variable)

    expression = sympify(
        expression,
        locals={str(x): x}
    )

    lower = sympify(lower)
    upper = sympify(upper)

    n = int(intervals)

    dx = (
        upper -
        lower
    ) / n

    total = (
        expression.subs(
            x,
            lower
        ) +
        expression.subs(
            x,
            upper
        )
    ) / 2

    for i in range(1, n):
        total += expression.subs(
            x,
            lower +
            i * dx
        )

    return simplify(
        total * dx
    )


def simpsons_rule(
    expression,
    lower,
    upper,
    intervals,
    variable="x"
):
    if intervals % 2 != 0:
        raise ValueError(
            "Simpson's rule requires an even number of intervals."
        )

    x = parse_variable(variable)

    expression = sympify(
        expression,
        locals={str(x): x}
    )

    lower = sympify(lower)
    upper = sympify(upper)

    n = int(intervals)

    dx = (
        upper -
        lower
    ) / n

    total = (
        expression.subs(x, lower) +
        expression.subs(x, upper)
    )

    for i in range(1, n):
        coefficient = (
            4
            if i % 2 == 1
            else 2
        )

        total += coefficient * expression.subs(
            x,
            lower +
            i * dx
        )

    return simplify(
        total *
        dx /
        3
    )


# ============================================================
# AREA APPLICATIONS
# ============================================================

def area_under_curve(
    expression,
    lower,
    upper,
    variable="x"
):
    x = parse_variable(variable)

    expression = sympify(
        expression,
        locals={str(x): x}
    )

    return integrate(
        Abs(expression),
        (
            x,
            lower,
            upper
        )
    )


def area_between_curves(
    upper_function,
    lower_function,
    lower,
    upper,
    variable="x"
):
    x = parse_variable(variable)

    upper_function = sympify(
        upper_function,
        locals={str(x): x}
    )

    lower_function = sympify(
        lower_function,
        locals={str(x): x}
    )

    return simplify(
        integrate(
            upper_function -
            lower_function,
            (
                x,
                lower,
                upper
            )
        )
    )


def curve_intersections(
    first,
    second,
    variable="x"
):
    x = parse_variable(variable)

    first = sympify(
        first,
        locals={str(x): x}
    )

    second = sympify(
        second,
        locals={str(x): x}
    )

    return solveset(
        Eq(
            first,
            second
        ),
        x,
        domain=S.Reals
    )


# ============================================================
# VOLUME APPLICATIONS
# ============================================================

def disk_volume(
    radius_function,
    lower,
    upper,
    variable="x"
):
    x = parse_variable(variable)

    radius_function = sympify(
        radius_function,
        locals={str(x): x}
    )

    return simplify(
        pi *
        integrate(
            radius_function**2,
            (
                x,
                lower,
                upper
            )
        )
    )


def washer_volume(
    outer_radius,
    inner_radius,
    lower,
    upper,
    variable="x"
):
    x = parse_variable(variable)

    outer_radius = sympify(
        outer_radius,
        locals={str(x): x}
    )

    inner_radius = sympify(
        inner_radius,
        locals={str(x): x}
    )

    return simplify(
        pi *
        integrate(
            outer_radius**2 -
            inner_radius**2,
            (
                x,
                lower,
                upper
            )
        )
    )


def shell_volume(
    radius,
    height,
    lower,
    upper,
    variable="x"
):
    x = parse_variable(variable)

    radius = sympify(
        radius,
        locals={str(x): x}
    )

    height = sympify(
        height,
        locals={str(x): x}
    )

    return simplify(
        2 *
        pi *
        integrate(
            radius *
            height,
            (
                x,
                lower,
                upper
            )
        )
    )


# ============================================================
# ARC LENGTH / SURFACE AREA
# ============================================================

def arc_length(
    expression,
    lower,
    upper,
    variable="x"
):
    x = parse_variable(variable)

    expression = sympify(
        expression,
        locals={str(x): x}
    )

    derivative_expression = diff(
        expression,
        x
    )

    return simplify(
        integrate(
            sqrt(
                1 +
                derivative_expression**2
            ),
            (
                x,
                lower,
                upper
            )
        )
    )


def parametric_arc_length(
    x_expression,
    y_expression,
    lower,
    upper,
    parameter="t"
):
    t = parse_variable(parameter)

    x_expression = sympify(
        x_expression,
        locals={str(t): t}
    )

    y_expression = sympify(
        y_expression,
        locals={str(t): t}
    )

    return simplify(
        integrate(
            sqrt(
                diff(
                    x_expression,
                    t
                )**2 +
                diff(
                    y_expression,
                    t
                )**2
            ),
            (
                t,
                lower,
                upper
            )
        )
    )


def surface_area_x_axis(
    expression,
    lower,
    upper,
    variable="x"
):
    x = parse_variable(variable)

    expression = sympify(
        expression,
        locals={str(x): x}
    )

    return simplify(
        2 *
        pi *
        integrate(
            Abs(expression) *
            sqrt(
                1 +
                diff(
                    expression,
                    x
                )**2
            ),
            (
                x,
                lower,
                upper
            )
        )
    )


# ============================================================
# SEQUENCES
# ============================================================

def sequence_term(
    expression,
    index_value,
    index="n"
):
    n = symbols(
        str(index),
        integer=True,
        positive=True
    )

    expression = sympify(
        expression,
        locals={str(n): n}
    )

    return simplify(
        expression.subs(
            n,
            index_value
        )
    )


def sequence_limit(
    expression,
    index="n"
):
    n = symbols(
        str(index),
        integer=True,
        positive=True
    )

    expression = sympify(
        expression,
        locals={str(n): n}
    )

    return limit(
        expression,
        n,
        oo
    )


def sequence_converges(
    expression,
    index="n"
):
    result = sequence_limit(
        expression,
        index
    )

    return (
        result != oo
        and result != -oo
        and result is not S.NaN
    )


# ============================================================
# INFINITE SERIES
# ============================================================

def partial_sum(
    expression,
    start,
    end,
    index="n"
):
    n = symbols(
        str(index),
        integer=True
    )

    expression = sympify(
        expression,
        locals={str(n): n}
    )

    return simplify(
        summation(
            expression,
            (
                n,
                start,
                end
            )
        )
    )


def infinite_series_sum(
    expression,
    start=1,
    index="n"
):
    n = symbols(
        str(index),
        integer=True,
        positive=True
    )

    expression = sympify(
        expression,
        locals={str(n): n}
    )

    return summation(
        expression,
        (
            n,
            start,
            oo
        )
    )


def geometric_series_sum(
    first_term,
    ratio
):
    first_term = sympify(
        first_term
    )

    ratio = sympify(
        ratio
    )

    if Abs(ratio) >= 1:
        raise ValueError(
            "Geometric series diverges when |r| >= 1."
        )

    return simplify(
        first_term /
        (1 - ratio)
    )


def nth_term_test(
    expression,
    index="n"
):
    result = sequence_limit(
        expression,
        index
    )

    return result == 0


# ============================================================
# POWER SERIES
# ============================================================

def power_series_expansion(
    expression,
    variable="x",
    center=0,
    order=6
):
    x = parse_variable(variable)

    expression = sympify(
        expression,
        locals={str(x): x}
    )

    return series(
        expression,
        x,
        sympify(center),
        int(order)
    )


def differentiate_power_series(
    expression,
    variable="x"
):
    return derivative(
        expression,
        variable
    )


def integrate_power_series(
    expression,
    variable="x"
):
    return antiderivative(
        expression,
        variable
    )


# ============================================================
# TAYLOR / MACLAURIN SERIES
# ============================================================

def taylor_series(
    expression,
    center,
    order,
    variable="x"
):
    x = parse_variable(variable)

    expression = sympify(
        expression,
        locals={str(x): x}
    )

    return series(
        expression,
        x,
        sympify(center),
        int(order)
    )


def maclaurin_series(
    expression,
    order,
    variable="x"
):
    return taylor_series(
        expression,
        0,
        order,
        variable
    )


def taylor_polynomial(
    expression,
    center,
    degree,
    variable="x"
):
    return taylor_series(
        expression,
        center,
        degree + 1,
        variable
    ).removeO()


# ============================================================
# PARAMETRIC CALCULUS
# ============================================================

def parametric_tangent_slope(
    x_expression,
    y_expression,
    parameter_value,
    parameter="t"
):
    t = parse_variable(parameter)

    slope = parametric_derivative(
        x_expression,
        y_expression,
        parameter
    )

    return simplify(
        slope.subs(
            t,
            parameter_value
        )
    )


def parametric_area(
    x_expression,
    y_expression,
    lower,
    upper,
    parameter="t"
):
    t = parse_variable(parameter)

    x_expression = sympify(
        x_expression,
        locals={str(t): t}
    )

    y_expression = sympify(
        y_expression,
        locals={str(t): t}
    )

    return simplify(
        integrate(
            y_expression *
            diff(
                x_expression,
                t
            ),
            (
                t,
                lower,
                upper
            )
        )
    )


# ============================================================
# POLAR CALCULUS
# ============================================================

def polar_area(
    radius_expression,
    lower_angle,
    upper_angle,
    variable="theta"
):
    theta = parse_variable(
        variable
    )

    radius_expression = sympify(
        radius_expression,
        locals={str(theta): theta}
    )

    return simplify(
        integrate(
            radius_expression**2 /
            2,
            (
                theta,
                lower_angle,
                upper_angle
            )
        )
    )


def polar_arc_length(
    radius_expression,
    lower_angle,
    upper_angle,
    variable="theta"
):
    theta = parse_variable(
        variable
    )

    radius_expression = sympify(
        radius_expression,
        locals={str(theta): theta}
    )

    dr = diff(
        radius_expression,
        theta
    )

    return simplify(
        integrate(
            sqrt(
                radius_expression**2 +
                dr**2
            ),
            (
                theta,
                lower_angle,
                upper_angle
            )
        )
    )


def polar_slope(
    radius_expression,
    variable="theta"
):
    theta = parse_variable(
        variable
    )

    r = sympify(
        radius_expression,
        locals={str(theta): theta}
    )

    dr = diff(
        r,
        theta
    )

    numerator = (
        dr * sin(theta) +
        r * cos(theta)
    )

    denominator = (
        dr * cos(theta) -
        r * sin(theta)
    )

    return simplify(
        numerator /
        denominator
    )


# ============================================================
# MULTIVARIABLE FUNCTIONS
# ============================================================

def evaluate_multivariable(
    expression,
    substitutions
):
    expression = sympify(
        expression
    )

    substitution_map = {}

    for variable, value in substitutions.items():
        matching = [
            symbol
            for symbol in expression.free_symbols
            if symbol.name == str(variable)
        ]

        for symbol in matching:
            substitution_map[symbol] = sympify(
                value
            )

    return simplify(
        expression.subs(
            substitution_map
        )
    )


def level_curve(
    expression,
    level,
    variables=("x", "y")
):
    variable_symbols = symbols(
        " ".join(variables),
        real=True
    )

    locals_dict = {
        name: symbol
        for name, symbol
        in zip(
            variables,
            variable_symbols
        )
    }

    expression = sympify(
        expression,
        locals=locals_dict
    )

    return Eq(
        expression,
        sympify(level)
    )


# ============================================================
# PARTIAL DERIVATIVES
# ============================================================

def partial_derivative(
    expression,
    variable,
    order=1
):
    variable_symbol = parse_variable(
        variable
    )

    expression = sympify(
        expression,
        locals={
            str(variable_symbol):
            variable_symbol
        }
    )

    return simplify(
        diff(
            expression,
            variable_symbol,
            int(order)
        )
    )


def mixed_partial_derivative(
    expression,
    variables
):
    expression = sympify(
        expression
    )

    result = expression

    for variable in variables:
        matching = [
            symbol
            for symbol in result.free_symbols
            if symbol.name == str(variable)
        ]

        if matching:
            result = diff(
                result,
                matching[0]
            )

    return simplify(
        result
    )


# ============================================================
# GRADIENT / DIRECTIONAL DERIVATIVES
# ============================================================

def gradient_vector(
    expression,
    variables=("x", "y")
):
    variable_symbols = symbols(
        " ".join(variables),
        real=True
    )

    locals_dict = {
        name: symbol
        for name, symbol
        in zip(
            variables,
            variable_symbols
        )
    }

    expression = sympify(
        expression,
        locals=locals_dict
    )

    return Matrix(
        [
            diff(
                expression,
                variable
            )
            for variable
            in variable_symbols
        ]
    )


def directional_derivative(
    expression,
    direction,
    variables=("x", "y")
):
    gradient = gradient_vector(
        expression,
        variables
    )

    direction = Matrix(
        [
            sympify(value)
            for value in direction
        ]
    )

    magnitude = sqrt(
        sum(
            value**2
            for value in direction
        )
    )

    if magnitude == 0:
        raise ValueError(
            "Direction vector cannot be zero."
        )

    unit_vector = (
        direction /
        magnitude
    )

    return simplify(
        gradient.dot(
            unit_vector
        )
    )


def tangent_plane(
    expression,
    point,
    variables=("x", "y")
):
    x, y = symbols(
        "x y",
        real=True
    )

    expression = sympify(
        expression,
        locals={
            variables[0]: x,
            variables[1]: y
        }
    )

    x0, y0 = map(
        sympify,
        point
    )

    z0 = expression.subs(
        {
            x: x0,
            y: y0
        }
    )

    fx = diff(
        expression,
        x
    ).subs(
        {
            x: x0,
            y: y0
        }
    )

    fy = diff(
        expression,
        y
    ).subs(
        {
            x: x0,
            y: y0
        }
    )

    return simplify(
        z0 +
        fx *
        (x - x0) +
        fy *
        (y - y0)
    )


# ============================================================
# MULTIVARIABLE OPTIMIZATION
# ============================================================

def multivariable_critical_points(
    expression,
    variables=("x", "y")
):
    variable_symbols = symbols(
        " ".join(variables),
        real=True
    )

    locals_dict = {
        name: symbol
        for name, symbol
        in zip(
            variables,
            variable_symbols
        )
    }

    expression = sympify(
        expression,
        locals=locals_dict
    )

    equations = [
        Eq(
            diff(
                expression,
                variable
            ),
            0
        )
        for variable
        in variable_symbols
    ]

    return solve(
        equations,
        variable_symbols,
        dict=True
    )


def hessian_matrix(
    expression,
    variables=("x", "y")
):
    variable_symbols = symbols(
        " ".join(variables),
        real=True
    )

    locals_dict = {
        name: symbol
        for name, symbol
        in zip(
            variables,
            variable_symbols
        )
    }

    expression = sympify(
        expression,
        locals=locals_dict
    )

    return hessian(
        expression,
        variable_symbols
    )


def lagrange_multipliers(
    objective,
    constraint,
    variables=("x", "y")
):
    variable_symbols = symbols(
        " ".join(variables),
        real=True
    )

    lam = symbols(
        "lambda",
        real=True
    )

    locals_dict = {
        name: symbol
        for name, symbol
        in zip(
            variables,
            variable_symbols
        )
    }

    objective = sympify(
        objective,
        locals=locals_dict
    )

    constraint = sympify(
        constraint,
        locals=locals_dict
    )

    equations = []

    for variable in variable_symbols:
        equations.append(
            Eq(
                diff(
                    objective,
                    variable
                ),
                lam *
                diff(
                    constraint,
                    variable
                )
            )
        )

    equations.append(
        Eq(
            constraint,
            0
        )
    )

    return solve(
        equations,
        (*variable_symbols, lam),
        dict=True
    )


# ============================================================
# MULTIPLE INTEGRALS
# ============================================================

def double_integral(
    expression,
    x_bounds,
    y_bounds
):
    x, y = symbols(
        "x y",
        real=True
    )

    expression = sympify(
        expression,
        locals={
            "x": x,
            "y": y
        }
    )

    return simplify(
        integrate(
            expression,
            (
                x,
                x_bounds[0],
                x_bounds[1]
            ),
            (
                y,
                y_bounds[0],
                y_bounds[1]
            )
        )
    )


def triple_integral(
    expression,
    x_bounds,
    y_bounds,
    z_bounds
):
    x, y, z = symbols(
        "x y z",
        real=True
    )

    expression = sympify(
        expression,
        locals={
            "x": x,
            "y": y,
            "z": z
        }
    )

    return simplify(
        integrate(
            expression,
            (
                x,
                x_bounds[0],
                x_bounds[1]
            ),
            (
                y,
                y_bounds[0],
                y_bounds[1]
            ),
            (
                z,
                z_bounds[0],
                z_bounds[1]
            )
        )
    )


# ============================================================
# COORDINATE-SYSTEM INTEGRATION
# ============================================================

def polar_double_integral(
    expression,
    r_bounds,
    theta_bounds
):
    r, theta = symbols(
        "r theta",
        real=True
    )

    expression = sympify(
        expression,
        locals={
            "r": r,
            "theta": theta
        }
    )

    return simplify(
        integrate(
            expression * r,
            (
                r,
                r_bounds[0],
                r_bounds[1]
            ),
            (
                theta,
                theta_bounds[0],
                theta_bounds[1]
            )
        )
    )


def cylindrical_jacobian(radius):
    return sympify(
        radius
    )


def spherical_jacobian(
    radius,
    phi
):
    radius = sympify(
        radius
    )

    phi = sympify(
        phi
    )

    return simplify(
        radius**2 *
        sin(phi)
    )


# ============================================================
# VECTOR CALCULUS
# ============================================================

def vector_function_derivative(
    components,
    parameter="t"
):
    t = parse_variable(
        parameter
    )

    return Matrix(
        [
            diff(
                sympify(
                    component,
                    locals={str(t): t}
                ),
                t
            )
            for component
            in components
        ]
    )


def vector_function_integral(
    components,
    parameter="t"
):
    t = parse_variable(
        parameter
    )

    return Matrix(
        [
            integrate(
                sympify(
                    component,
                    locals={str(t): t}
                ),
                t
            )
            for component
            in components
        ]
    )


def velocity_vector(
    position_components,
    parameter="t"
):
    return vector_function_derivative(
        position_components,
        parameter
    )


def acceleration_vector(
    position_components,
    parameter="t"
):
    velocity = velocity_vector(
        position_components,
        parameter
    )

    return vector_function_derivative(
        list(velocity),
        parameter
    )


def vector_divergence(
    components,
    variables=("x", "y", "z")
):
    variable_symbols = symbols(
        " ".join(variables),
        real=True
    )

    locals_dict = {
        name: symbol
        for name, symbol
        in zip(
            variables,
            variable_symbols
        )
    }

    components = [
        sympify(
            component,
            locals=locals_dict
        )
        for component
        in components
    ]

    return simplify(
        sum(
            diff(
                components[i],
                variable_symbols[i]
            )
            for i
            in range(
                len(variable_symbols)
            )
        )
    )


def vector_curl(
    components,
    variables=("x", "y", "z")
):
    if len(components) != 3:
        raise ValueError(
            "Curl requires a 3D vector field."
        )

    x, y, z = symbols(
        "x y z",
        real=True
    )

    locals_dict = {
        variables[0]: x,
        variables[1]: y,
        variables[2]: z
    }

    P, Q, R = [
        sympify(
            component,
            locals=locals_dict
        )
        for component
        in components
    ]

    return Matrix(
        [
            diff(R, y) -
            diff(Q, z),

            diff(P, z) -
            diff(R, x),

            diff(Q, x) -
            diff(P, y)
        ]
    )


# ============================================================
# LINE / SURFACE INTEGRALS
# ============================================================

def scalar_line_integral(
    scalar_field,
    path_components,
    lower,
    upper,
    parameter="t"
):
    t = parse_variable(
        parameter
    )

    path = Matrix(
        [
            sympify(
                component,
                locals={str(t): t}
            )
            for component
            in path_components
        ]
    )

    speed = sqrt(
        sum(
            diff(
                component,
                t
            )**2
            for component
            in path
        )
    )

    field = sympify(
        scalar_field
    )

    variables = sorted(
        list(
            field.free_symbols
        ),
        key=lambda symbol:
        symbol.name
    )

    substituted = field

    for symbol, component in zip(
        variables,
        path
    ):
        substituted = substituted.subs(
            symbol,
            component
        )

    return simplify(
        integrate(
            substituted *
            speed,
            (
                t,
                lower,
                upper
            )
        )
    )


def vector_line_integral(
    field_components,
    path_components,
    lower,
    upper,
    parameter="t"
):
    t = parse_variable(
        parameter
    )

    path = Matrix(
        [
            sympify(
                component,
                locals={str(t): t}
            )
            for component
            in path_components
        ]
    )

    path_derivative = path.diff(
        t
    )

    x, y, z = symbols(
        "x y z",
        real=True
    )

    standard_variables = [
        x,
        y,
        z
    ]

    field = Matrix(
        [
            sympify(
                component,
                locals={
                    "x": x,
                    "y": y,
                    "z": z
                }
            )
            for component
            in field_components
        ]
    )

    substitutions = {
        standard_variables[i]:
        path[i]

        for i in range(
            len(path)
        )
    }

    field_on_path = field.subs(
        substitutions
    )

    integrand = simplify(
        field_on_path.dot(
            path_derivative
        )
    )

    return simplify(
        integrate(
            integrand,
            (
                t,
                lower,
                upper
            )
        )
    )


# ============================================================
# VECTOR CALCULUS THEOREM UTILITIES
# ============================================================

def is_conservative_field(
    components,
    variables=("x", "y", "z")
):
    result = vector_curl(
        components,
        variables
    )

    return all(
        simplify(component) == 0
        for component in result
    )


def fundamental_line_integral(
    potential_function,
    start_point,
    end_point,
    variables=("x", "y", "z")
):
    variable_symbols = symbols(
        " ".join(variables),
        real=True
    )

    locals_dict = {
        name: symbol
        for name, symbol
        in zip(
            variables,
            variable_symbols
        )
    }

    potential = sympify(
        potential_function,
        locals=locals_dict
    )

    start_subs = {
        variable:
        sympify(value)

        for variable, value
        in zip(
            variable_symbols,
            start_point
        )
    }

    end_subs = {
        variable:
        sympify(value)

        for variable, value
        in zip(
            variable_symbols,
            end_point
        )
    }

    return simplify(
        potential.subs(
            end_subs
        ) -
        potential.subs(
            start_subs
        )
    )


# ============================================================
# CALCULUS UTILITIES
# ============================================================

def detect_variables(
    expression
):
    expression = sympify(
        expression
    )

    return sorted(
        [
            str(symbol)
            for symbol
            in expression.free_symbols
        ]
    )


def exact_calculus_value(
    expression
):
    return simplify(
        sympify(expression)
    )


def decimal_calculus_value(
    expression,
    digits=10
):
    return N(
        sympify(expression),
        digits
    )


def simplify_calculus_result(
    expression
):
    return simplify(
        sympify(expression)
    )


def check_derivative(
    original,
    candidate_derivative,
    variable="x"
):
    x = parse_variable(variable)

    original = sympify(
        original,
        locals={str(x): x}
    )

    candidate_derivative = sympify(
        candidate_derivative,
        locals={str(x): x}
    )

    return simplify(
        diff(
            original,
            x
        ) -
        candidate_derivative
    ) == 0


def evaluate_piecewise_calculus(
    expression,
    value,
    variable="x"
):
    x = parse_variable(variable)

    expression = sympify(
        expression,
        locals={str(x): x}
    )

    return simplify(
        expression.subs(
            x,
            value
        )
    )
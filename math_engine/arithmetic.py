"""
S.A.T.U.R.N. Arithmetic Subsystem

Provides core arithmetic operations for the S.A.T.U.R.N. math engine.

This subsystem uses SymPy so that calculations can preserve exact
mathematical values such as fractions and radicals whenever possible.
"""

from sympy import (
    sympify,
    sqrt,
    Abs,
    factorial as sympy_factorial,
    gcd,
    lcm,
    factorint,
    floor,
    ceiling,
    N
)


# ============================================================
# INPUT CONVERSION
# ============================================================

def parse_number(value):
    """
    Convert an input value into a SymPy mathematical expression.

    Examples:
        "1/3"  -> 1/3
        "sqrt(2)" -> sqrt(2)
        5 -> 5
        2.5 -> 2.5
    """

    return sympify(value)


# ============================================================
# BASIC ARITHMETIC
# ============================================================

def add(a, b):
    """
    Return a + b.
    """

    a = parse_number(a)
    b = parse_number(b)

    return a + b


def subtract(a, b):
    """
    Return a - b.
    """

    a = parse_number(a)
    b = parse_number(b)

    return a - b


def multiply(a, b):
    """
    Return a * b.
    """

    a = parse_number(a)
    b = parse_number(b)

    return a * b


def divide(a, b):
    """
    Return a / b.

    Raises:
        ZeroDivisionError if b = 0.
    """

    a = parse_number(a)
    b = parse_number(b)

    if b == 0:
        raise ZeroDivisionError(
            "Cannot divide by zero."
        )

    return a / b


def arithmetic_mean(values):
    """
    Return the arithmetic mean of a nonempty collection.

    Example:
        arithmetic_mean([2, 4, 6]) -> 4
    """

    if isinstance(
        values,
        (
            str,
            bytes,
        ),
    ):
        raise TypeError(
            "Mean values must be supplied as a collection."
        )

    parsed_values = [
        parse_number(value)
        for value in values
    ]

    if not parsed_values:
        raise ValueError(
            "At least one value is required to calculate a mean."
        )

    return sum(parsed_values) / len(parsed_values)


# ============================================================
# POWERS AND ROOTS
# ============================================================

def power(base, exponent):
    """
    Raise a number to a power.

    Example:
        power(2, 3) -> 8
    """

    base = parse_number(base)
    exponent = parse_number(exponent)

    return base ** exponent


def square_root(value):
    """
    Return the exact square root of a value when possible.

    Examples:
        square_root(9) -> 3
        square_root(2) -> sqrt(2)
    """

    value = parse_number(value)

    return sqrt(value)


def nth_root(value, n):
    """
    Return the nth root of a value.

    Examples:
        nth_root(8, 3) -> 2
        nth_root(16, 4) -> 2
    """

    value = parse_number(value)
    n = parse_number(n)

    if n == 0:
        raise ValueError(
            "The zeroth root is undefined."
        )

    return value ** (1 / n)


# ============================================================
# ABSOLUTE VALUE
# ============================================================

def absolute_value(value):
    """
    Return the absolute value of a number.

    Examples:
        absolute_value(-5) -> 5
        absolute_value(5) -> 5
    """

    value = parse_number(value)

    return Abs(value)

# ============================================================
# FACTORIAL
# ============================================================

def factorial(value):
    """
    Return the factorial of a non-negative integer.

    Example:
        factorial(5) -> 120
    """

    value = parse_number(value)

    if value.is_integer is not True or value < 0:
        raise ValueError(
            "Factorial is only defined here for non-negative integers."
        )

    return sympy_factorial(value)


# ============================================================
# GREATEST COMMON DIVISOR
# ============================================================

def greatest_common_divisor(a, b):
    """
    Return the greatest common divisor of two integers.

    Example:
        greatest_common_divisor(12, 18) -> 6
    """

    a = parse_number(a)
    b = parse_number(b)

    if a.is_integer is not True or b.is_integer is not True:
        raise ValueError(
            "GCD requires integer inputs."
        )

    return gcd(a, b)


# ============================================================
# LEAST COMMON MULTIPLE
# ============================================================

def least_common_multiple(a, b):
    """
    Return the least common multiple of two integers.

    Example:
        least_common_multiple(4, 6) -> 12
    """

    a = parse_number(a)
    b = parse_number(b)

    if a.is_integer is not True or b.is_integer is not True:
        raise ValueError(
            "LCM requires integer inputs."
        )

    return lcm(a, b)


# ============================================================
# PERCENTAGE
# ============================================================

def percentage(part, whole):
    """
    Return what percentage 'part' is of 'whole'.

    Example:
        percentage(25, 100) -> 25
    """

    part = parse_number(part)
    whole = parse_number(whole)

    if whole == 0:
        raise ZeroDivisionError(
            "Cannot calculate a percentage with a whole of zero."
        )

    return (part / whole) * 100


# ============================================================
# PERCENT CHANGE
# ============================================================

def percent_change(original, new):
    """
    Return the percent change from original to new.

    Positive result = increase
    Negative result = decrease

    Example:
        percent_change(100, 120) -> 20
    """

    original = parse_number(original)
    new = parse_number(new)

    if original == 0:
        raise ZeroDivisionError(
            "Percent change is undefined when the original value is zero."
        )

    return ((new - original) / original) * 100


# ============================================================
# RATIO
# ============================================================

def ratio(a, b):
    """
    Return the simplified ratio a:b as a tuple.

    Example:
        ratio(10, 15) -> (2, 3)
    """

    a = parse_number(a)
    b = parse_number(b)

    if a.is_integer is not True or b.is_integer is not True:
        raise ValueError(
            "Ratio simplification currently requires integer inputs."
        )

    if b == 0:
        raise ZeroDivisionError(
            "A ratio cannot have zero as its second term."
        )

    divisor = gcd(a, b)

    return (
        a / divisor,
        b / divisor
    )


# ============================================================
# PROPORTIONS
# ============================================================

def solve_proportion(a, b, c):
    """
    Solve the proportion:

        a / b = c / x

    for x.

    Rearranging gives:

        x = (b * c) / a

    Example:
        solve_proportion(2, 3, 4) -> 6
    """

    a = parse_number(a)
    b = parse_number(b)
    c = parse_number(c)

    if a == 0:
        raise ZeroDivisionError(
            "Cannot solve this proportion when the first term is zero."
        )

    return (b * c) / a


# ============================================================
# PRIME FACTORIZATION
# ============================================================

def prime_factorization(value):
    """
    Return the prime factorization of an integer.

    Example:
        prime_factorization(60)
        -> {2: 2, 3: 1, 5: 1}
    """

    value = parse_number(value)

    if value.is_integer is not True:
        raise ValueError(
            "Prime factorization requires an integer."
        )

    if value == 0:
        raise ValueError(
            "Prime factorization of zero is undefined."
        )

    return factorint(abs(value))


# ============================================================
# ROUNDING AND NUMERICAL REPRESENTATION
# ============================================================

def floor_value(value):
    """
    Return the greatest integer less than or equal to value.

    Example:
        floor_value(3.8) -> 3
    """

    value = parse_number(value)

    return floor(value)


def ceiling_value(value):
    """
    Return the smallest integer greater than or equal to value.

    Example:
        ceiling_value(3.2) -> 4
    """

    value = parse_number(value)

    return ceiling(value)


def round_value(value, digits=0):
    """
    Round a numerical value to a specified number of decimal places.

    Examples:
        round_value(3.14159, 2) -> 3.14
        round_value(12.6) -> 13
    """

    value = parse_number(value)
    digits = int(digits)

    return round(float(value), digits)


def decimal_value(value, digits=15):
    """
    Return a numerical decimal approximation.

    Examples:
        decimal_value("1/3") -> 0.333333333333333
        decimal_value("sqrt(2)", 10) -> 1.414213562
    """

    value = parse_number(value)
    digits = int(digits)

    return N(value, digits)


def scientific_notation(value, significant_digits=6):
    """
    Return a value as a scientific-notation string.

    Example:
        scientific_notation(1234567, 4)
        -> '1.235e+06'
    """

    value = parse_number(value)
    significant_digits = int(significant_digits)

    if significant_digits < 1:
        raise ValueError(
            "Significant digits must be at least 1."
        )

    numeric_value = float(value)

    return f"{numeric_value:.{significant_digits - 1}e}"


# ============================================================
# ARITHMETIC REGISTRATION
# ============================================================

from math_engine.arithmetic import (
    add,
    subtract,
    multiply,
    divide,
    power,
    square_root,
    nth_root,
    absolute_value,
    factorial,
    greatest_common_divisor,
    least_common_multiple,
    percentage,
    percent_change,
    ratio,
    solve_proportion,
    prime_factorization,
    floor_value,
    ceiling_value,
    round_value,
    decimal_value,
    scientific_notation
)


def register_arithmetic_operations(registry):
    """
    Register Arithmetic v1 operations.
    """

    registry.register(
        name="add",
        function=add,
        subsystem="arithmetic",
        description="Add two or more numbers.",
        parameters={
            "values": {
                "type": "number_list",
                "required": True,
                "description": "Numbers to add"
            }
        },
        returns={
            "type": "expression",
            "description": "Sum of the input values"
        },
        keywords=[
            "add",
            "addition",
            "sum",
            "plus",
            "total"
        ],
        category="basic_arithmetic"
    )

    registry.register(
        name="subtract",
        function=subtract,
        subsystem="arithmetic",
        description="Subtract one number from another.",
        parameters={
            "a": {
                "type": "number",
                "required": True,
                "description": "Starting value"
            },
            "b": {
                "type": "number",
                "required": True,
                "description": "Value to subtract"
            }
        },
        returns={
            "type": "expression",
            "description": "Difference between the values"
        },
        keywords=[
            "subtract",
            "subtraction",
            "minus",
            "difference"
        ],
        category="basic_arithmetic"
    )

    registry.register(
        name="multiply",
        function=multiply,
        subsystem="arithmetic",
        description="Multiply two or more numbers.",
        parameters={
            "values": {
                "type": "number_list",
                "required": True,
                "description": "Numbers to multiply"
            }
        },
        returns={
            "type": "expression",
            "description": "Product of the input values"
        },
        keywords=[
            "multiply",
            "multiplication",
            "times",
            "product"
        ],
        category="basic_arithmetic"
    )

    registry.register(
        name="divide",
        function=divide,
        subsystem="arithmetic",
        description="Divide one number by another.",
        parameters={
            "numerator": {
                "type": "number",
                "required": True,
                "description": "Value being divided"
            },
            "denominator": {
                "type": "number",
                "required": True,
                "description": "Value dividing the numerator"
            }
        },
        returns={
            "type": "expression",
            "description": "Quotient"
        },
        keywords=[
            "divide",
            "division",
            "quotient",
            "over"
        ],
        category="basic_arithmetic"
    )

    registry.register(
        name="power",
        function=power,
        subsystem="arithmetic",
        description="Raise a number to a power.",
        parameters={
            "base": {
                "type": "number",
                "required": True,
                "description": "Base value"
            },
            "exponent": {
                "type": "number",
                "required": True,
                "description": "Exponent"
            }
        },
        returns={
            "type": "expression",
            "description": "Base raised to the exponent"
        },
        keywords=[
            "power",
            "exponent",
            "raised",
            "squared",
            "cubed"
        ],
        category="powers_roots"
    )

    registry.register(
        name="square_root",
        function=square_root,
        subsystem="arithmetic",
        description="Calculate the square root of a number.",
        parameters={
            "value": {
                "type": "number",
                "required": True,
                "description": "Value whose square root is needed"
            }
        },
        returns={
            "type": "expression",
            "description": "Square root"
        },
        keywords=[
            "square root",
            "sqrt",
            "root"
        ],
        category="powers_roots"
    )

    registry.register(
        name="nth_root",
        function=nth_root,
        subsystem="arithmetic",
        description="Calculate the nth root of a number.",
        parameters={
            "value": {
                "type": "number",
                "required": True,
                "description": "Value"
            },
            "n": {
                "type": "integer",
                "required": True,
                "description": "Root degree"
            }
        },
        returns={
            "type": "expression",
            "description": "Nth root"
        },
        keywords=[
            "nth root",
            "root",
            "cube root"
        ],
        category="powers_roots"
    )

    registry.register(
        name="absolute_value",
        function=absolute_value,
        subsystem="arithmetic",
        description="Calculate the absolute value of a number.",
        parameters={
            "value": {
                "type": "number",
                "required": True,
                "description": "Input value"
            }
        },
        returns={
            "type": "expression",
            "description": "Absolute value"
        },
        keywords=[
            "absolute value",
            "magnitude"
        ],
        category="basic_arithmetic"
    )

    registry.register(
        name="factorial",
        function=factorial,
        subsystem="arithmetic",
        description="Calculate the factorial of a nonnegative integer.",
        parameters={
            "value": {
                "type": "integer",
                "required": True,
                "description": "Nonnegative integer"
            }
        },
        returns={
            "type": "integer",
            "description": "Factorial"
        },
        keywords=[
            "factorial"
        ],
        category="integer_operations"
    )

    registry.register(
        name="greatest_common_divisor",
        function=greatest_common_divisor,
        subsystem="arithmetic",
        description="Find the greatest common divisor of integers.",
        parameters={
            "values": {
                "type": "integer_list",
                "required": True,
                "description": "Integers"
            }
        },
        returns={
            "type": "integer",
            "description": "Greatest common divisor"
        },
        keywords=[
            "gcd",
            "greatest common divisor",
            "greatest common factor"
        ],
        category="integer_operations"
    )

    registry.register(
        name="least_common_multiple",
        function=least_common_multiple,
        subsystem="arithmetic",
        description="Find the least common multiple of integers.",
        parameters={
            "values": {
                "type": "integer_list",
                "required": True,
                "description": "Integers"
            }
        },
        returns={
            "type": "integer",
            "description": "Least common multiple"
        },
        keywords=[
            "lcm",
            "least common multiple"
        ],
        category="integer_operations"
    )

    registry.register(
        name="percentage",
        function=percentage,
        subsystem="arithmetic",
        description="Calculate a percentage of a value.",
        parameters={
            "percent": {
                "type": "number",
                "required": True,
                "description": "Percentage"
            },
            "value": {
                "type": "number",
                "required": True,
                "description": "Value the percentage is taken from"
            }
        },
        returns={
            "type": "expression",
            "description": "Percentage of the value"
        },
        keywords=[
            "percentage",
            "percent",
            "of"
        ],
        category="percentages"
    )

    registry.register(
        name="percent_change",
        function=percent_change,
        subsystem="arithmetic",
        description="Calculate percent change between two values.",
        parameters={
            "old_value": {
                "type": "number",
                "required": True,
                "description": "Original value"
            },
            "new_value": {
                "type": "number",
                "required": True,
                "description": "New value"
            }
        },
        returns={
            "type": "expression",
            "description": "Percent change"
        },
        keywords=[
            "percent change",
            "percentage change",
            "increase",
            "decrease"
        ],
        category="percentages"
    )

    registry.register(
        name="ratio",
        function=ratio,
        subsystem="arithmetic",
        description="Simplify a ratio between two values.",
        parameters={
            "a": {
                "type": "number",
                "required": True,
                "description": "First ratio value"
            },
            "b": {
                "type": "number",
                "required": True,
                "description": "Second ratio value"
            }
        },
        returns={
            "type": "expression",
            "description": "Simplified ratio"
        },
        keywords=[
            "ratio",
            "proportion"
        ],
        category="ratios_proportions"
    )

    registry.register(
        name="solve_proportion",
        function=solve_proportion,
        subsystem="arithmetic",
        description="Solve a proportional relationship for an unknown value.",
        parameters={
            "a": {
                "type": "number",
                "required": True,
                "description": "First numerator"
            },
            "b": {
                "type": "number",
                "required": True,
                "description": "First denominator"
            },
            "c": {
                "type": "number",
                "required": True,
                "description": "Second numerator"
            },
            "d": {
                "type": "number",
                "required": True,
                "description": "Second denominator or unknown"
            }
        },
        returns={
            "type": "expression",
            "description": "Solution to the proportion"
        },
        keywords=[
            "proportion",
            "cross multiply",
            "ratio equation"
        ],
        category="ratios_proportions"
    )

    registry.register(
        name="prime_factorization",
        function=prime_factorization,
        subsystem="arithmetic",
        description="Find the prime factorization of an integer.",
        parameters={
            "value": {
                "type": "integer",
                "required": True,
                "description": "Integer to factor"
            }
        },
        returns={
            "type": "factorization",
            "description": "Prime factors and exponents"
        },
        keywords=[
            "prime factorization",
            "prime factors",
            "factor"
        ],
        category="integer_operations"
    )

    registry.register(
        name="floor_value",
        function=floor_value,
        subsystem="arithmetic",
        description="Calculate the floor of a number.",
        parameters={
            "value": {
                "type": "number",
                "required": True,
                "description": "Input number"
            }
        },
        returns={
            "type": "integer",
            "description": "Floor value"
        },
        keywords=[
            "floor",
            "round down"
        ],
        category="rounding"
    )

    registry.register(
        name="ceiling_value",
        function=ceiling_value,
        subsystem="arithmetic",
        description="Calculate the ceiling of a number.",
        parameters={
            "value": {
                "type": "number",
                "required": True,
                "description": "Input number"
            }
        },
        returns={
            "type": "integer",
            "description": "Ceiling value"
        },
        keywords=[
            "ceiling",
            "ceil",
            "round up"
        ],
        category="rounding"
    )

    registry.register(
        name="round_value",
        function=round_value,
        subsystem="arithmetic",
        description="Round a value to a specified number of decimal places.",
        parameters={
            "value": {
                "type": "number",
                "required": True,
                "description": "Input number"
            },
            "digits": {
                "type": "integer",
                "required": False,
                "description": "Number of decimal places"
            }
        },
        returns={
            "type": "number",
            "description": "Rounded value"
        },
        keywords=[
            "round",
            "rounded",
            "decimal places"
        ],
        category="rounding"
    )

    registry.register(
        name="decimal_value",
        function=decimal_value,
        subsystem="arithmetic",
        description="Convert an exact mathematical value to decimal form.",
        parameters={
            "value": {
                "type": "expression",
                "required": True,
                "description": "Exact value or expression"
            }
        },
        returns={
            "type": "number",
            "description": "Decimal approximation"
        },
        keywords=[
            "decimal",
            "approximate",
            "numerical value"
        ],
        category="numeric_conversion"
    )

    registry.register(
        name="scientific_notation",
        function=scientific_notation,
        subsystem="arithmetic",
        description="Express a number in scientific notation.",
        parameters={
            "value": {
                "type": "number",
                "required": True,
                "description": "Input number"
            }
        },
        returns={
            "type": "scientific_notation",
            "description": "Scientific notation representation"
        },
        keywords=[
            "scientific notation",
            "exponent",
            "power of ten"
        ],
        category="numeric_conversion"
    )
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


print("\n==============================")
print("N.O.V.A. Arithmetic Test")
print("==============================\n")


# Addition
print("Addition:")
print("2 + 3 =", add(2, 3))
print("1/3 + 1/6 =", add("1/3", "1/6"))


# Subtraction
print("\nSubtraction:")
print("10 - 4 =", subtract(10, 4))
print("1/2 - 1/4 =", subtract("1/2", "1/4"))


# Multiplication
print("\nMultiplication:")
print("6 * 7 =", multiply(6, 7))
print("2/3 * 3/4 =", multiply("2/3", "3/4"))


# Division
print("\nDivision:")
print("10 / 2 =", divide(10, 2))
print("1 / 3 =", divide(1, 3))


# Powers
print("\nPowers:")
print("2^3 =", power(2, 3))
print("5^2 =", power(5, 2))


# Square roots
print("\nSquare Roots:")
print("sqrt(9) =", square_root(9))
print("sqrt(2) =", square_root(2))


# Nth roots
print("\nNth Roots:")
print("cube root of 8 =", nth_root(8, 3))
print("fourth root of 16 =", nth_root(16, 4))


# Absolute value
print("\nAbsolute Value:")
print("|-5| =", absolute_value(-5))
print("|5| =", absolute_value(5))


# Division by zero test
print("\nDivision by Zero Test:")

try:
    divide(10, 0)

except ZeroDivisionError as error:
    print("Correctly caught error:", error)


# Factorial
print("\nFactorial:")
print("5! =", factorial(5))
print("0! =", factorial(0))


# Greatest Common Divisor
print("\nGreatest Common Divisor:")
print("GCD of 12 and 18 =", greatest_common_divisor(12, 18))


# Least Common Multiple
print("\nLeast Common Multiple:")
print("LCM of 4 and 6 =", least_common_multiple(4, 6))


# Percentage
print("\nPercentage:")
print("25 is what percent of 100? =", percentage(25, 100), "%")
print("15 is what percent of 60? =", percentage(15, 60), "%")


# Percent Change
print("\nPercent Change:")
print("100 to 120 =", percent_change(100, 120), "%")
print("100 to 80 =", percent_change(100, 80), "%")


# Ratios
print("\nRatios:")
print("10:15 =", ratio(10, 15))
print("20:8 =", ratio(20, 8))


# Proportions
print("\nProportions:")
print("2/3 = 4/x, x =", solve_proportion(2, 3, 4))


# Prime Factorization
print("\nPrime Factorization:")
print("60 =", prime_factorization(60))
print("84 =", prime_factorization(84))


# Floor
print("\nFloor:")
print("floor(3.8) =", floor_value(3.8))
print("floor(-2.3) =", floor_value(-2.3))


# Ceiling
print("\nCeiling:")
print("ceiling(3.2) =", ceiling_value(3.2))
print("ceiling(-2.8) =", ceiling_value(-2.8))


# Rounding
print("\nRounding:")
print("3.14159 rounded to 2 decimals =", round_value(3.14159, 2))
print("12.6 rounded to nearest integer =", round_value(12.6))


# Decimal Approximation
print("\nDecimal Approximation:")
print("1/3 =", decimal_value("1/3"))
print("sqrt(2) to 10 digits =", decimal_value("sqrt(2)", 10))


# Scientific Notation
print("\nScientific Notation:")
print("1234567 =", scientific_notation(1234567, 4))
print("0.000012345 =", scientific_notation(0.000012345, 4))


print("\n==============================")
print("Arithmetic Test Complete")
print("==============================")
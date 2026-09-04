from math_engine.executor import (
    execute_math_operation
)


print("\n==============================")
print("N.O.V.A. Math Executor Test")
print("==============================")


# ------------------------------------------------------------
# ARITHMETIC
# ------------------------------------------------------------

result = execute_math_operation(
    "add",
    {
        "a": 5,
        "b": 7
    }
)

print("\nArithmetic:")
print(result)


# ------------------------------------------------------------
# ALGEBRA
# ------------------------------------------------------------

result = execute_math_operation(
    "simplify_expression",
    {
        "expression": (
            "(x**2 - 1)/(x - 1)"
        )
    }
)

print("\nAlgebra:")
print(result)


# ------------------------------------------------------------
# GEOMETRY
# ------------------------------------------------------------

result = execute_math_operation(
    "circle_area",
    {
        "radius": 3
    }
)

print("\nGeometry:")
print(result)


# ------------------------------------------------------------
# TRIGONOMETRY
# ------------------------------------------------------------

result = execute_math_operation(
    "trig_expression_value",
    {
        "expression": "sin(pi/2)"
    }
)

print("\nTrigonometry:")
print(result)


# ------------------------------------------------------------
# CALCULUS
# ------------------------------------------------------------

result = execute_math_operation(
    "derivative",
    {
        "expression": "x**3",
        "variable": "x"
    }
)

print("\nCalculus:")
print(result)


# ------------------------------------------------------------
# INVALID OPERATION
# ------------------------------------------------------------

result = execute_math_operation(
    "this_operation_does_not_exist"
)

print("\nInvalid operation:")
print(result)


# ------------------------------------------------------------
# INVALID ARGUMENTS
# ------------------------------------------------------------

result = execute_math_operation(
    "circle_area",
    {
        "banana": 5
    }
)

print("\nInvalid arguments:")
print(result)


result = execute_math_operation(
    "circle_area",
    {}
)

print("\nMissing arguments:")
print(result)


print("\n==============================")
print("Executor Test Complete")
print("==============================")
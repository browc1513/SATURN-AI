from math_engine.router import (
    find_math_operations,
    select_math_operation,
    route_and_execute_math
)


print("\n==============================")
print("S.A.T.U.R.N. Math Router Test")
print("==============================")


# ------------------------------------------------------------
# GEOMETRY SEARCH
# ------------------------------------------------------------

results = find_math_operations(
    "area of a circle",
    subsystem="geometry"
)

print("\nGeometry search:")

for result in results:
    print(
        result["score"],
        result["name"]
    )


# ------------------------------------------------------------
# CALCULUS SEARCH
# ------------------------------------------------------------

results = find_math_operations(
    "find the derivative",
    subsystem="calculus"
)

print("\nCalculus search:")

for result in results:
    print(
        result["score"],
        result["name"]
    )


# ------------------------------------------------------------
# ALGEBRA SEARCH
# ------------------------------------------------------------

results = find_math_operations(
    "solve an equation",
    subsystem="algebra"
)

print("\nAlgebra search:")

for result in results:
    print(
        result["score"],
        result["name"]
    )


# ------------------------------------------------------------
# TRIGONOMETRY SEARCH
# ------------------------------------------------------------

results = find_math_operations(
    "right triangle sine",
    subsystem="trigonometry"
)

print("\nTrigonometry search:")

for result in results:
    print(
        result["score"],
        result["name"]
    )


# ------------------------------------------------------------
# GLOBAL SEARCH
# ------------------------------------------------------------

results = find_math_operations(
    "sphere volume"
)

print("\nGlobal search:")

for result in results:
    print(
        result["score"],
        result["subsystem"],
        result["name"]
    )


# ------------------------------------------------------------
# CLEAR SELECTION
# ------------------------------------------------------------

selection = select_math_operation(
    "sphere volume"
)

print("\nClear selection:")
print(selection)


# ------------------------------------------------------------
# AMBIGUOUS SELECTION
# ------------------------------------------------------------

selection = select_math_operation(
    "area of a circle",
    subsystem="geometry"
)

print("\nAmbiguous selection:")
print(selection)


# ------------------------------------------------------------
# WEAK SELECTION
# ------------------------------------------------------------

selection = select_math_operation(
    "something random and unrelated"
)

print("\nWeak selection:")
print(selection)


# ------------------------------------------------------------
# ROUTE AND EXECUTE: SUCCESS
# ------------------------------------------------------------

result = route_and_execute_math(
    "find the derivative",
    arguments={
        "expression": "x**3",
        "variable": "x"
    },
    subsystem="calculus"
)

print("\nRoute and execute - success:")
print(result)


# ------------------------------------------------------------
# ROUTE AND EXECUTE: AMBIGUOUS
# ------------------------------------------------------------

result = route_and_execute_math(
    "area of a circle",
    arguments={
        "radius": 3
    },
    subsystem="geometry"
)

print("\nRoute and execute - ambiguous:")
print(result)


# ------------------------------------------------------------
# ROUTE AND EXECUTE: MISSING ARGUMENT
# ------------------------------------------------------------

result = route_and_execute_math(
    "sphere volume",
    arguments={},
    subsystem="geometry"
)

print("\nRoute and execute - missing argument:")
print(result)


# ------------------------------------------------------------
# ARGUMENT-AWARE ROUTING
# ------------------------------------------------------------

result = route_and_execute_math(
    "area of a circle",
    arguments={
        "radius": 7
    },
    subsystem="geometry"
)

print("\nArgument-aware routing:")
print(result)


print("\n==============================")
print("Router Test Complete")
print("==============================")
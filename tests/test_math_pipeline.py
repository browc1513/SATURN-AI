from math_engine.math_pipeline import (
    interpret_and_execute_math
)


print("\n==============================")
print("N.O.V.A. Natural Language Math Pipeline Test")
print("==============================")


# ============================================================
# TEST 1 — CALCULUS
# ============================================================

result = interpret_and_execute_math(
    "Find the derivative of x**3 with respect to x."
)

print("\nCalculus:")
print(result)


# ============================================================
# TEST 2 — ALTERNATE CALCULUS LANGUAGE
# ============================================================

result = interpret_and_execute_math(
    "Differentiate x squared with respect to x."
)

print("\nAlternate calculus:")
print(result)


# ============================================================
# TEST 3 — GEOMETRY
# ============================================================

result = interpret_and_execute_math(
    "What is the area of a circle with radius 7?"
)

print("\nCircle area:")
print(result)


# ============================================================
# TEST 4 — SPHERE VOLUME
# ============================================================

result = interpret_and_execute_math(
    "Find the volume of a sphere with radius 4."
)

print("\nSphere volume:")
print(result)


# ============================================================
# TEST 5 — MISSING INFORMATION
# ============================================================

result = interpret_and_execute_math(
    "Find the area of a circle."
)

print("\nMissing radius:")
print(result)


# ============================================================
# TEST 6 — UNKNOWN REQUEST
# ============================================================

result = interpret_and_execute_math(
    "Do something mathematical with this."
)

print("\nUnknown request:")
print(result)


# ============================================================
# TEST 7 — EMPTY REQUEST
# ============================================================

result = interpret_and_execute_math(
    ""
)

print("\nEmpty request:")
print(result)


print("\n==============================")
print("Natural Language Pipeline Test Complete")
print("==============================")
from math_engine.interpreter import (
    normalize_math_language,
    detect_subsystem,
    interpret_math_request
)


print("\n==============================")
print("N.O.V.A. Language Interpreter Test")
print("==============================")


# ------------------------------------------------------------
# NORMALIZATION
# ------------------------------------------------------------

result = normalize_math_language(
    "Differentiate x squared"
)

print("\nNormalization:")
print(result)


# ------------------------------------------------------------
# SUBSYSTEM DETECTION
# ------------------------------------------------------------

result = detect_subsystem(
    "find the derivative of x**3"
)

print("\nCalculus subsystem:")
print(result)


result = detect_subsystem(
    "find the area of a circle"
)

print("\nGeometry subsystem:")
print(result)


# ------------------------------------------------------------
# CALCULUS INTERPRETATION
# ------------------------------------------------------------

result = interpret_math_request(
    "Find the derivative of x**3 with respect to x."
)

print("\nCalculus interpretation:")
print(result)


# ------------------------------------------------------------
# GEOMETRY INTERPRETATION
# ------------------------------------------------------------

result = interpret_math_request(
    "What is the area of a circle with radius 7?"
)

print("\nGeometry interpretation:")
print(result)


# ------------------------------------------------------------
# ALTERNATE LANGUAGE
# ------------------------------------------------------------

result = interpret_math_request(
    "Differentiate x squared with respect to x."
)

print("\nAlternate calculus language:")
print(result)


# ------------------------------------------------------------
# UNKNOWN REQUEST
# ------------------------------------------------------------

result = interpret_math_request(
    "Do something mathematical with this."
)

print("\nUnknown interpretation:")
print(result)


# ------------------------------------------------------------
# EMPTY REQUEST
# ------------------------------------------------------------

result = interpret_math_request(
    ""
)

print("\nEmpty interpretation:")
print(result)


print("\n==============================")
print("Interpreter Test Complete")
print("==============================")
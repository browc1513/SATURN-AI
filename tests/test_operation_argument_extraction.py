from math_engine.argument_extractor import (
    get_operation_parameters,
    extract_arguments_for_operation,
)


print()
print("=" * 52)
print("S.A.T.U.R.N. Operation Argument Extraction Test")
print("=" * 52)


# ============================================================
# SIGNATURE INSPECTION
# ============================================================

print("\nRectangle signature:")

result = get_operation_parameters(
    "rectangle_area"
)

print(result)


print("\nCylinder signature:")

result = get_operation_parameters(
    "cylinder_volume"
)

print(result)


# ============================================================
# RECTANGLE
# ============================================================

print("\nRectangle extraction:")

text = (
    "What is the area of a rectangle "
    "with a width of 7 and a length of 5?"
)

result = extract_arguments_for_operation(
    text,
    "rectangle_area",
)

print(result)


# ============================================================
# CYLINDER
# ============================================================

print("\nCylinder extraction:")

text = (
    "Find the volume of a cylinder "
    "with radius 4 and height 10."
)

result = extract_arguments_for_operation(
    text,
    "cylinder_volume",
)

print(result)


# ============================================================
# SPHERE
# ============================================================

print("\nSphere extraction:")

text = (
    "Find the volume of a sphere "
    "with radius 4."
)

result = extract_arguments_for_operation(
    text,
    "sphere_volume",
)

print(result)


# ============================================================
# MISSING ARGUMENT
# ============================================================

print("\nMissing rectangle length:")

text = (
    "Find the area of a rectangle "
    "with width 7."
)

result = extract_arguments_for_operation(
    text,
    "rectangle_area",
)

print(result)


# ============================================================
# UNKNOWN OPERATION
# ============================================================

print("\nUnknown operation:")

result = extract_arguments_for_operation(
    "Do something.",
    "definitely_not_a_real_operation",
)

print(result)


print()
print("=" * 52)
print("Operation Argument Extraction Test Complete")
print("=" * 52)
print()
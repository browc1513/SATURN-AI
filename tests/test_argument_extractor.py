from math_engine.argument_extractor import (
    extract_named_number,
    extract_arguments,
)


print()
print("=" * 44)
print("N.O.V.A. Argument Extractor Test")
print("=" * 44)


# ============================================================
# SINGLE VALUES
# ============================================================

print("\nSingle parameter tests:")

tests = [
    (
        "The radius is 7.",
        "radius",
    ),
    (
        "radius of 5",
        "radius",
    ),
    (
        "width = 12",
        "width",
    ),
    (
        "The height is 3.5",
        "height",
    ),
    (
        "first side is 8",
        "side_a",
    ),
    (
        "second side of 10",
        "side_b",
    ),
]


for text, parameter in tests:

    value = extract_named_number(
        text,
        parameter,
    )

    print(
        f"{parameter}: "
        f"{value}"
    )


# ============================================================
# RECTANGLE
# ============================================================

print("\nRectangle test:")

text = (
    "What is the area of a rectangle "
    "with a width of 7 and a length of 5?"
)

result = extract_arguments(
    text,
    [
        "length",
        "width",
    ],
)

print(
    result
)


# ============================================================
# CYLINDER
# ============================================================

print("\nCylinder test:")

text = (
    "Find the volume of a cylinder "
    "with radius 4 and height 10."
)

result = extract_arguments(
    text,
    [
        "radius",
        "height",
    ],
)

print(
    result
)


# ============================================================
# MISSING INFORMATION
# ============================================================

print("\nMissing parameter test:")

text = (
    "Find the area of a rectangle "
    "with width 7."
)

result = extract_arguments(
    text,
    [
        "length",
        "width",
    ],
)

print(
    result
)


print()
print("=" * 44)
print("Argument Extractor Test Complete")
print("=" * 44)
print()
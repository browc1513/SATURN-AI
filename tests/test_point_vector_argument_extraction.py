from math_engine.argument_extractor import (
    extract_argument,
    extract_arguments_for_operation,
)


def show_test(label, value):
    print()
    print("-" * 60)
    print(label)
    print(value)


print("=" * 60)
print("S.A.T.U.R.N. Point / Vector Argument Extraction Test")
print("=" * 60)


# ============================================================
# BASIC POINTS
# ============================================================

show_test(
    "Basic 2D point:",
    extract_argument(
        "point (3, 4)",
        "point",
    ),
)


show_test(
    "Point using at:",
    extract_argument(
        "Find the tangent line at (2, 5).",
        "point",
    ),
)


show_test(
    "Basic 3D point:",
    extract_argument(
        "point (1, -2, 5)",
        "point",
    ),
)


# ============================================================
# NAMED START / END POINTS
# ============================================================

show_test(
    "Start point:",
    extract_argument(
        (
            "start point (1, 2, 3) "
            "end point (4, 5, 6)"
        ),
        "start_point",
    ),
)


show_test(
    "End point:",
    extract_argument(
        (
            "start point (1, 2, 3) "
            "end point (4, 5, 6)"
        ),
        "end_point",
    ),
)


# ============================================================
# VECTORS
# ============================================================

show_test(
    "Basic vector:",
    extract_argument(
        "vector (3, 4)",
        "vector",
    ),
)


show_test(
    "Direction vector:",
    extract_argument(
        "direction vector (1, -2)",
        "direction",
    ),
)


show_test(
    "3D direction vector:",
    extract_argument(
        "direction (1, 2, 3)",
        "direction",
    ),
)


# ============================================================
# SYMBOLIC COMPONENTS
# ============================================================

show_test(
    "Symbolic point:",
    extract_argument(
        "point (x, y + 1)",
        "point",
    ),
)


# ============================================================
# FULL OPERATION EXTRACTION
# ============================================================

show_test(
    "Directional derivative extraction:",
    extract_arguments_for_operation(
        (
            "Find the directional derivative "
            "of x**2 + y**2 "
            "direction (1, 1)"
        ),
        "directional_derivative",
    ),
)


print()
print("=" * 60)
print("Point / Vector Argument Extraction Test Complete")
print("=" * 60)
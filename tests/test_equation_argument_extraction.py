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
print("N.O.V.A. Equation Argument Extraction Test")
print("=" * 60)


# ============================================================
# BASIC EQUATION
# ============================================================

show_test(
    "Basic equation:",
    extract_argument(
        "Solve 2*x + 3 = 11 for x.",
        "equation",
    ),
)


# ============================================================
# VARIABLE
# ============================================================

show_test(
    "Variable from equation request:",
    extract_argument(
        "Solve 2*x + 3 = 11 for x.",
        "variable",
    ),
)


# ============================================================
# NATURAL-LANGUAGE EQUALS
# ============================================================

show_test(
    "Natural-language equals:",
    extract_argument(
        "Solve x + 5 equals 12 for x.",
        "equation",
    ),
)


# ============================================================
# EXPLICIT EQUATION WORD
# ============================================================

show_test(
    "Explicit equation:",
    extract_argument(
        "equation x**2 - 4 = 0",
        "equation",
    ),
)


# ============================================================
# INEQUALITY
# ============================================================

show_test(
    "Inequality:",
    extract_argument(
        "Solve the inequality 2*x + 1 <= 7 for x.",
        "inequality",
    ),
)


# ============================================================
# NATURAL-LANGUAGE INEQUALITY
# ============================================================

show_test(
    "Natural-language inequality:",
    extract_argument(
        (
            "Solve the inequality "
            "2*x + 1 is less than or equal to 7 "
            "for x."
        ),
        "inequality",
    ),
)


# ============================================================
# FULL REGISTERED OPERATION EXTRACTION
# ============================================================

show_test(
    "Full solve_equation extraction:",
    extract_arguments_for_operation(
        "Solve 2*x + 3 = 11 for x.",
        "solve_equation",
    ),
)


show_test(
    "Left side extraction:",
    extract_argument(
        "Solve 2*x + 3 = 11 for x.",
        "left_side",
    ),
)


show_test(
    "Right side extraction:",
    extract_argument(
        "Solve 2*x + 3 = 11 for x.",
        "right_side",
    ),
)


print()
print("=" * 60)
print("Equation Argument Extraction Test Complete")
print("=" * 60)
from math_engine.argument_extractor import (
    extract_argument,
    extract_arguments_for_operation,
)

from math_engine.executor import (
    execute_math_operation,
)


def show_test(label, value):
    print()
    print("-" * 60)
    print(label)
    print(value)


print("=" * 60)
print("S.A.T.U.R.N. System Argument Extraction Test")
print("=" * 60)


SYSTEM_TEXT = """Solve the system:
x + y = 5
x - y = 1
for x and y"""


# ============================================================
# EQUATION LIST
# ============================================================

show_test(
    "Equation list:",
    extract_argument(
        SYSTEM_TEXT,
        "equations",
    ),
)


# ============================================================
# VARIABLE LIST
# ============================================================

show_test(
    "Variable list:",
    extract_argument(
        SYSTEM_TEXT,
        "variables",
    ),
)


# ============================================================
# SEMICOLON SYSTEM
# ============================================================

show_test(
    "Semicolon equation list:",
    extract_argument(
        (
            "Solve the system: "
            "2*x + y = 7; "
            "x - y = 2 "
            "for x and y"
        ),
        "equations",
    ),
)


# ============================================================
# THREE VARIABLES
# ============================================================

show_test(
    "Three-variable list:",
    extract_argument(
        (
            "Solve the system: "
            "x + y + z = 6; "
            "x - y = 2; "
            "z = 3 "
            "for x, y, and z"
        ),
        "variables",
    ),
)

show_test(
    "Two variables with and:",
    extract_argument(
        (
            "Solve the system: "
            "x + y = 5; "
            "x - y = 1 "
            "for x and y"
        ),
        "variables",
    ),
)


show_test(
    "Three variables without Oxford and:",
    extract_argument(
        (
            "Solve the system: "
            "x + y + z = 6 "
            "for x, y, z"
        ),
        "variables",
    ),
)


# ============================================================
# FULL SOLVE_SYSTEM EXTRACTION
# ============================================================

solve_system_extraction = (
    extract_arguments_for_operation(
        SYSTEM_TEXT,
        "solve_system",
    )
)

show_test(
    "Full solve_system extraction:",
    solve_system_extraction,
)

if solve_system_extraction["success"]:

    solve_system_execution = (
        execute_math_operation(
            "solve_system",
            solve_system_extraction[
                "arguments"
            ],
        )
    )

    show_test(
        "Full solve_system execution:",
        solve_system_execution,
    )


# ============================================================
# ADVANCED SOLVER
# ============================================================

show_test(
    "Full solve_system_advanced extraction:",
    extract_arguments_for_operation(
        SYSTEM_TEXT,
        "solve_system_advanced",
    ),
)


# ============================================================
# CLASSIFIER
# ============================================================

show_test(
    "Full classify_system_solution extraction:",
    extract_arguments_for_operation(
        SYSTEM_TEXT,
        "classify_system_solution",
    ),
)


print()
print("=" * 60)
print("System Argument Extraction Test Complete")
print("=" * 60)
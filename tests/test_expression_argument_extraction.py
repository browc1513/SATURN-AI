from math_engine.argument_extractor import (
    extract_argument,
    extract_arguments_for_operation,
)


def run_test(label, value):
    print()
    print("-" * 60)
    print(label)
    print(value)


print("=" * 60)
print("S.A.T.U.R.N. Expression / Variable Extraction Test")
print("=" * 60)


run_test(
    "Named expression:",
    extract_argument(
        "expression x**2 + 3*x + 2",
        "expression",
    ),
)


run_test(
    "Named variable:",
    extract_argument(
        "variable x",
        "variable",
    ),
)


run_test(
    "Variable from natural calculus language:",
    extract_argument(
        "Differentiate x**3 with respect to x.",
        "variable",
    ),
)


run_test(
    "Expression from derivative:",
    extract_argument(
        "Find the derivative of x**3 with respect to x.",
        "expression",
    ),
)


run_test(
    "Expression from differentiate:",
    extract_argument(
        "Differentiate x**2 + 3*x with respect to x.",
        "expression",
    ),
)


run_test(
    "Expression from simplify:",
    extract_argument(
        "Simplify x**2 + 2*x + 1.",
        "expression",
    ),
)


run_test(
    "Full derivative extraction:",
    extract_arguments_for_operation(
        "Find the derivative of x**3 with respect to x.",
        "derivative",
    ),
)


print()
print("=" * 60)
print("Expression / Variable Extraction Test Complete")
print("=" * 60)
"""
S.A.T.U.R.N. Universal Math Pipeline Regression Test

Purpose
-------
Verify that math_pipeline.py works after removing the temporary
interpreter-argument merge.

Run from the project root with:

    python -m tests.test_math_pipeline_universal
"""

from math_engine.math_pipeline import interpret_and_execute_math


CASES = [
    "add 3 and 5",
    "find the area of a circle with radius 4",
    "differentiate x**3 with respect to x",
    "find the left riemann sum of x**2 from 0 to 1 using 4 rectangles",
    "find the absolute extrema of x**2 - 4*x from 0 to 5",
]


def show_result(text, result):
    print("\n" + "-" * 72)
    print("Input     :", text)
    print("Success   :", result.get("success"))
    print("Stage     :", result.get("stage"))
    print("Operation :", result.get("operation"))
    print("Arguments :", result.get("arguments"))
    print("Exact     :", result.get("exact_result"))
    print("Error     :", result.get("error"))


def main():
    print("=" * 72)
    print("S.A.T.U.R.N. Universal Math Pipeline Regression Test")
    print("=" * 72)

    passed = 0
    failed = 0

    for text in CASES:

        result = interpret_and_execute_math(
            text
        )

        show_result(
            text,
            result,
        )

        if result.get("success"):
            passed += 1
        else:
            failed += 1

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print("Cases passed :", passed)
    print("Cases failed :", failed)

    if failed == 0:
        print("RESULT: UNIVERSAL PIPELINE PASSED")
    else:
        print("RESULT: PIPELINE GAPS FOUND")

    print("=" * 72)


if __name__ == "__main__":
    main()

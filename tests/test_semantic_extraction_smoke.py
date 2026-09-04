"""
N.O.V.A. Semantic Extraction Smoke Test

Purpose
-------
Structural coverage is now complete, but this test checks whether several
important parameter families can actually be extracted from natural language.

Run from the project root with:

    python -m tests.test_semantic_extraction_smoke
"""

from math_engine.argument_extractor import (
    extract_arguments_for_operation,
)


CASES = [
    (
        "Arithmetic operands",
        "add",
        "add 3 and 5",
    ),
    (
        "Subtraction operands",
        "subtract",
        "subtract 4 from 10",
    ),
    (
        "Power base/exponent",
        "power",
        "raise 2 to the power 8",
    ),
    (
        "Quadratic coefficients",
        "quadratic_formula",
        "use the quadratic formula with a 1 b -3 c 2",
    ),
    (
        "Product-rule expressions",
        "product_rule",
        "use the product rule with first x**2 and second sin(x)",
    ),
    (
        "Quotient-rule expressions",
        "quotient_rule",
        "use the quotient rule with numerator x**2 and denominator x + 1",
    ),
    (
        "Integration by parts",
        "integration_by_parts",
        "integrate by parts with u x and dv exp(x)",
    ),
    (
        "Area between curves",
        "area_between_curves",
        "find the area between curves upper function x**2 and lower function x from 0 to 1",
    ),
    (
        "Triangle angles",
        "missing_triangle_angle",
        "find the missing triangle angle with angle 1 50 degrees and angle 2 60 degrees",
    ),
    (
        "Law of cosines included angle",
        "law_of_cosines_side",
        "find the missing side with side a 3 side b 4 and included angle 90 degrees",
    ),
    (
        "Angle unit enum",
        "polar_to_cartesian",
        "convert radius 2 angle pi/2 to cartesian using angle unit radians",
    ),
    (
        "Riemann rectangles",
        "left_riemann_sum",
        "find the left riemann sum of x**2 from 0 to 1 using 4 rectangles",
    ),
    (
        "Absolute extrema bounds",
        "absolute_extrema",
        "find the absolute extrema of x**2 - 4*x from 0 to 5",
    ),
    (
        "Series integer bounds",
        "partial_sum",
        "find the partial sum of 1/n from 1 to 5",
    ),
    (
        "Trig interval angle bounds",
        "solve_trig_interval",
        "solve sin(x) = 0 from 0 to 2*pi",
    ),
]


def show_case(title, operation, text):
    print("\n" + "-" * 72)
    print(title)
    print("-" * 72)
    print("Operation :", operation)
    print("Input     :", text)

    result = extract_arguments_for_operation(
        text,
        operation,
    )

    print("Success   :", result.get("success"))
    print("Arguments :", result.get("arguments"))
    print(
        "Missing   :",
        result.get("missing_required"),
    )
    print(
        "Unparsed  :",
        result.get("unparsed_required"),
    )
    print("Error     :", result.get("error"))


def main():
    print("=" * 72)
    print("N.O.V.A. Semantic Extraction Smoke Test")
    print("=" * 72)

    passed = 0
    failed = 0

    for title, operation, text in CASES:
        result = extract_arguments_for_operation(
            text,
            operation,
        )

        if (
            result.get("success")
            and not result.get("missing_required")
            and not result.get("unparsed_required")
        ):
            passed += 1
        else:
            failed += 1

        show_case(
            title,
            operation,
            text,
        )

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print("Cases passed :", passed)
    print("Cases failed :", failed)

    if failed == 0:
        print("RESULT: SEMANTIC SMOKE TEST PASSED")
    else:
        print("RESULT: SEMANTIC EXTRACTION GAPS FOUND")

    print("=" * 72)


if __name__ == "__main__":
    main()

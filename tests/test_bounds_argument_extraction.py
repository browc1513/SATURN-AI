from math_engine.argument_extractor import (
    extract_argument,
    extract_expression,
    extract_arguments_for_operation,
)


def show_test(title, value):
    print("\n" + "-" * 60)
    print(title + ":")
    print(value)


def main():
    print("=" * 60)
    print("S.A.T.U.R.N. Bounds / Interval Argument Extraction Test")
    print("=" * 60)

    show_test(
        "Lower from 0 to 5",
        extract_argument(
            "integrate x**2 from 0 to 5",
            "lower",
        ),
    )

    show_test(
        "Upper from 0 to 5",
        extract_argument(
            "integrate x**2 from 0 to 5",
            "upper",
        ),
    )

    show_test(
        "Between interval",
        extract_argument(
            "use the interval between -2 and 4",
            "interval",
        ),
    )

    show_test(
        "Parenthesized interval",
        extract_argument(
            "interval (0, 10)",
            "interval",
        ),
    )

    show_test(
        "Symbolic bounds",
        (
            extract_argument(
                "integrate sin(x) from -pi to pi",
                "lower",
            ),
            extract_argument(
                "integrate sin(x) from -pi to pi",
                "upper",
            ),
        ),
    )

    show_test(
        "X bounds",
        extract_argument(
            "x from 0 to 2",
            "x_bounds",
        ),
    )

    show_test(
        "Y bounds",
        extract_argument(
            "y between -1 and 1",
            "y_bounds",
        ),
    )

    show_test(
        "Integral expression excludes bounds",
        extract_expression(
            "integrate x**2 from 0 to 5",
            "expression",
        ),
    )

    print("\n" + "=" * 60)
    print("Bounds / Interval Argument Extraction Test Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()

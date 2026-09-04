from math_engine.argument_extractor import (
    extract_argument,
)


def show_test(title, value):
    print("\n" + "-" * 60)
    print(title + ":")
    print(value)


def main():
    print("=" * 60)
    print("N.O.V.A. String / Enum / Boolean Extraction Test")
    print("=" * 60)

    show_test(
        "Unit degrees",
        extract_argument(
            "unit degrees",
            "unit",
        ),
    )

    show_test(
        "Unit radians",
        extract_argument(
            "unit is radians",
            "unit",
        ),
    )

    show_test(
        "Output unit degrees",
        extract_argument(
            "output unit degrees",
            "output_unit",
        ),
    )

    show_test(
        "Function name",
        extract_argument(
            "function name sin",
            "function_name",
        ),
    )

    show_test(
        "Solve for rate",
        extract_argument(
            "solve for rate x",
            "solve_for_rate",
        ),
    )

    show_test(
        "Decimal true",
        extract_argument(
            "decimal true",
            "decimal",
        ),
    )

    show_test(
        "Decimal false",
        extract_argument(
            "decimal false",
            "decimal",
        ),
    )

    show_test(
        "Decimal yes",
        extract_argument(
            "decimal yes",
            "decimal",
        ),
    )

    show_test(
        "Decimal no",
        extract_argument(
            "decimal no",
            "decimal",
        ),
    )

    show_test(
        "Natural as decimal",
        extract_argument(
            "give the answer as a decimal",
            "decimal",
        ),
    )

    show_test(
        "Natural without decimal",
        extract_argument(
            "give the exact answer without a decimal",
            "decimal",
        ),
    )

    show_test(
        "Unit abbreviation normalization",
        extract_argument(
            "unit deg",
            "unit",
        ),
    )

    print("\n" + "=" * 60)
    print("String / Enum / Boolean Extraction Test Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()

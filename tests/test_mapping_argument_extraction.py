from math_engine.argument_extractor import (
    extract_argument,
)


def show_test(title, value):
    print("\n" + "-" * 60)
    print(title + ":")
    print(value)


def main():
    print("=" * 60)
    print("S.A.T.U.R.N. Mapping / Substitution Extraction Test")
    print("=" * 60)

    show_test(
        "Single numeric substitution",
        extract_argument(
            "substitute x = 2",
            "substitutions",
        ),
    )

    show_test(
        "Two numeric substitutions",
        extract_argument(
            "substitute x = 2 and y = 3",
            "substitutions",
        ),
    )

    show_test(
        "Comma-separated substitutions",
        extract_argument(
            "substitutions x = 2, y = 3",
            "substitutions",
        ),
    )

    show_test(
        "Symbolic substitution",
        extract_argument(
            "substitute x = 2*pi",
            "substitutions",
        ),
    )

    show_test(
        "Mixed substitutions",
        extract_argument(
            "substitute x = 2 and y = a + 1",
            "substitutions",
        ),
    )

    show_test(
        "Replace-with language",
        extract_argument(
            "replace x with 2 and y with 3",
            "substitutions",
        ),
    )

    show_test(
        "Substitutions before target expression",
        extract_argument(
            "substitute x = 2 and y = 3 into x**2 + y",
            "substitutions",
        ),
    )

    print("\n" + "=" * 60)
    print("Mapping / Substitution Extraction Test Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()

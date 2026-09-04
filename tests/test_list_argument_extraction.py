from math_engine.argument_extractor import (
    extract_argument,
    extract_arguments_for_operation,
)


def show_test(title, value):
    print("\n" + "-" * 60)
    print(title + ":")
    print(value)


def main():
    print("=" * 60)
    print("N.O.V.A. Generic List / Component Extraction Test")
    print("=" * 60)

    show_test(
        "Numeric components",
        extract_argument(
            "components [3, 4]",
            "components",
        ),
    )

    show_test(
        "Symbolic components",
        extract_argument(
            "components [x**2, y**2, z**2]",
            "components",
        ),
    )

    show_test(
        "Field components",
        extract_argument(
            "field components [x*y, y*z, z*x]",
            "field_components",
        ),
    )

    show_test(
        "Position components",
        extract_argument(
            "position components [t, t**2, t**3]",
            "position_components",
        ),
    )

    show_test(
        "Side lengths",
        extract_argument(
            "side lengths [3, 4, 5]",
            "side_lengths",
        ),
    )

    show_test(
        "Parenthesized components",
        extract_argument(
            "components (3, 4, 5)",
            "components",
        ),
    )

    show_test(
        "Point list",
        extract_argument(
            "points [(0, 0), (4, 0), (4, 3)]",
            "points",
        ),
    )

    show_test(
        "Unbracketed point list",
        extract_argument(
            "points (0, 0), (4, 0), (4, 3)",
            "points",
        ),
    )

    print("\n" + "=" * 60)
    print("Generic List / Component Extraction Test Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()

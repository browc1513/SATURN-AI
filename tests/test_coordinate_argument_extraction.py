from math_engine.argument_extractor import (
    extract_arguments_for_operation,
    get_operation_parameters,
)
from math_engine.language_schema import (
    get_parameter_type,
)


def show_test(title, value):
    print("\n" + "-" * 60)
    print(title + ":")
    print(value)


def main():
    print("=" * 60)
    print("S.A.T.U.R.N. Coordinate Adapter / Override Test")
    print("=" * 60)

    # --------------------------------------------------------
    # COORDINATE ADAPTERS
    # --------------------------------------------------------

    show_test(
        "Distance between two points",
        extract_arguments_for_operation(
            "Find the distance between points (1, 2) and (4, 6)",
            "distance_between_points",
        ),
    )

    show_test(
        "Midpoint from two points",
        extract_arguments_for_operation(
            "Find the midpoint of (0, 0) and (8, 4)",
            "midpoint",
        ),
    )

    show_test(
        "Slope from two points",
        extract_arguments_for_operation(
            "Find the slope between (2, 3) and (6, 11)",
            "slope",
        ),
    )

    show_test(
        "Line from two points",
        extract_arguments_for_operation(
            "Find the line through points (1, 2) and (3, 6)",
            "line_from_two_points",
        ),
    )

    show_test(
        "Translate point with scalar deltas",
        extract_arguments_for_operation(
            "translate point (3, 5) delta x 2 delta y -1",
            "translate_point",
        ),
    )

    # --------------------------------------------------------
    # OPERATION-SPECIFIC TYPE OVERRIDES
    # --------------------------------------------------------

    show_test(
        "Directional derivative direction type",
        get_parameter_type(
            "direction",
            operation_name="directional_derivative",
        ),
    )

    show_test(
        "Limit direction type",
        get_parameter_type(
            "direction",
            operation_name="evaluate_limit",
        ),
    )

    show_test(
        "Taylor-series center type",
        get_parameter_type(
            "center",
            operation_name="taylor_series",
        ),
    )

    show_test(
        "Numerical-limit point type",
        get_parameter_type(
            "point",
            operation_name="numerical_limit",
        ),
    )

    show_test(
        "Point-to-line point_x type",
        get_parameter_type(
            "point_x",
            operation_name="point_to_line_distance",
        ),
    )

    show_test(
        "Point-to-line point_y type",
        get_parameter_type(
            "point_y",
            operation_name="point_to_line_distance",
        ),
    )

    show_test(
        "Taylor-series parameter metadata",
        get_operation_parameters(
            "taylor_series",
        ),
    )

    show_test(
        "Evaluate-limit parameter metadata",
        get_operation_parameters(
            "evaluate_limit",
        ),
    )

    print("\n" + "=" * 60)
    print("Coordinate Adapter / Override Test Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()

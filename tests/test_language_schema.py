from math_engine.language_schema import (
    get_parameter_type,
    get_parameter_aliases,
)


print("\n==============================")
print("S.A.T.U.R.N. Language Schema Test")
print("==============================")


parameters = [
    "radius",
    "width",
    "height",
    "side_a",
    "angle",
    "expression",
    "variable",
    "equations",
    "point",
    "components",
    "x_bounds",
    "substitutions",
    "unit",
    "decimal",
    "something_unknown",
]


for parameter in parameters:

    print(
        f"\n{parameter}"
    )

    print(
        "Type ->",
        get_parameter_type(
            parameter
        )
    )

    print(
        "Aliases ->",
        get_parameter_aliases(
            parameter
        )
    )


print("\n==============================")
print("Language Schema Test Complete")
print("==============================")
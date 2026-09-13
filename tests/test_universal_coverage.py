"""
Universal Extraction Coverage Test for S.A.T.U.R.N.

This is intentionally stricter than the audit script.

It checks that:
    1. Every registered operation can have its signature inspected.
    2. Every parameter has a known extraction type.
    3. Operation-specific overrides actually resolve to the expected type.

Run from the project root with:

    python -m tests.test_universal_coverage
"""

from math_engine.argument_extractor import (
    get_operation_parameters,
)
from math_engine.language_schema import (
    OPERATION_PARAMETER_TYPE_OVERRIDES,
)
from math_engine.registry import math_registry


def main():

    print("=" * 68)
    print("S.A.T.U.R.N. Universal Extraction Coverage Test")
    print("=" * 68)

    operation_names = sorted(
        math_registry.names()
    )

    inspection_failures = []
    unknown_parameters = []
    override_failures = []

    total_parameters = 0

    for operation_name in operation_names:

        info = get_operation_parameters(
            operation_name
        )

        if not info.get("success"):

            inspection_failures.append(
                (
                    operation_name,
                    info.get("error"),
                )
            )

            continue

        for parameter in info.get(
            "parameters",
            [],
        ):

            total_parameters += 1

            if parameter.get(
                "type"
            ) == "unknown":

                unknown_parameters.append(
                    (
                        operation_name,
                        parameter.get("name"),
                        parameter.get(
                            "required"
                        ),
                        parameter.get(
                            "default"
                        ),
                    )
                )

    for operation_name, overrides in (
        OPERATION_PARAMETER_TYPE_OVERRIDES
        .items()
    ):

        info = get_operation_parameters(
            operation_name
        )

        if not info.get("success"):
            continue

        actual_types = {
            parameter["name"]:
            parameter["type"]
            for parameter in info[
                "parameters"
            ]
        }

        for parameter_name, expected_type in (
            overrides.items()
        ):

            actual_type = actual_types.get(
                parameter_name
            )

            if actual_type != expected_type:

                override_failures.append(
                    (
                        operation_name,
                        parameter_name,
                        expected_type,
                        actual_type,
                    )
                )

    print(
        f"Registered operations : "
        f"{len(operation_names)}"
    )

    print(
        f"Total parameters      : "
        f"{total_parameters}"
    )

    print(
        f"Inspection failures   : "
        f"{len(inspection_failures)}"
    )

    print(
        f"Unknown parameters    : "
        f"{len(unknown_parameters)}"
    )

    print(
        f"Override failures     : "
        f"{len(override_failures)}"
    )

    print("\n" + "-" * 68)
    print("INSPECTION FAILURES")
    print("-" * 68)

    if inspection_failures:

        for operation_name, error in (
            inspection_failures
        ):

            print(
                f"{operation_name}: "
                f"{error}"
            )

    else:
        print("None")

    print("\n" + "-" * 68)
    print("UNKNOWN PARAMETERS")
    print("-" * 68)

    if unknown_parameters:

        for (
            operation_name,
            parameter_name,
            required,
            default,
        ) in unknown_parameters:

            print(
                f"{operation_name}."
                f"{parameter_name}"
                f"  required={required}"
                f"  default={default!r}"
            )

    else:
        print("None")

    print("\n" + "-" * 68)
    print("OVERRIDE FAILURES")
    print("-" * 68)

    if override_failures:

        for (
            operation_name,
            parameter_name,
            expected_type,
            actual_type,
        ) in override_failures:

            print(
                f"{operation_name}."
                f"{parameter_name}: "
                f"expected {expected_type}, "
                f"got {actual_type}"
            )

    else:
        print("None")

    print("\n" + "=" * 68)

    if (
        inspection_failures
        or unknown_parameters
        or override_failures
    ):

        print(
            "RESULT: COVERAGE GAPS FOUND"
        )

    else:

        print(
            "RESULT: STRUCTURAL COVERAGE PASSED"
        )

    print("=" * 68)


if __name__ == "__main__":
    main()

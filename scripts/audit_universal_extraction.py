"""
Universal Extraction Coverage Audit for N.O.V.A.

Purpose
-------
Inspect every registered math operation and every parameter in its
deterministic function signature.

This audit answers:
    - How many operations are registered?
    - How many parameters exist across those operations?
    - Which parameters are classified as "unknown"?
    - Which parameter names are used with multiple semantic types?
    - Which operations fail signature inspection?
    - Which operation-specific overrides are currently active?

Run from the project root with:

    python -m scripts.audit_universal_extraction
"""

from collections import defaultdict
import csv
import json
from pathlib import Path

from math_engine.argument_extractor import get_operation_parameters
from math_engine.language_schema import (
    OPERATION_PARAMETER_TYPE_OVERRIDES,
)
from math_engine.registry import math_registry


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

JSON_OUTPUT = DATA_DIR / "universal_extraction_audit.json"
CSV_OUTPUT = DATA_DIR / "universal_extraction_audit.csv"


def get_operation_names():
    """
    Return all currently registered operation names in sorted order.
    """
    return sorted(math_registry.names())


def audit_operations():
    """
    Inspect every registered operation and return a structured audit.
    """

    operation_names = get_operation_names()

    total_parameters = 0
    known_parameters = 0
    unknown_parameters = []

    inspection_failures = []

    type_usage = defaultdict(set)
    parameter_usage = defaultdict(list)

    operation_rows = []

    for operation_name in operation_names:

        parameter_info = get_operation_parameters(
            operation_name
        )

        if not parameter_info.get("success"):

            inspection_failures.append(
                {
                    "operation": operation_name,
                    "error": parameter_info.get("error"),
                }
            )

            continue

        for parameter in parameter_info.get(
            "parameters",
            [],
        ):

            total_parameters += 1

            parameter_name = parameter.get(
                "name"
            )

            parameter_type = parameter.get(
                "type"
            )

            required = parameter.get(
                "required"
            )

            default = parameter.get(
                "default"
            )

            type_usage[
                parameter_name
            ].add(parameter_type)

            parameter_usage[
                parameter_name
            ].append(
                {
                    "operation": operation_name,
                    "type": parameter_type,
                    "required": required,
                    "default": default,
                }
            )

            row = {
                "operation": operation_name,
                "parameter": parameter_name,
                "type": parameter_type,
                "required": required,
                "default": repr(default),
                "override_active": False,
            }

            override_type = (
                OPERATION_PARAMETER_TYPE_OVERRIDES
                .get(
                    operation_name,
                    {},
                )
                .get(
                    parameter_name
                )
            )

            if override_type is not None:
                row["override_active"] = True
                row["override_type"] = (
                    override_type
                )
            else:
                row["override_type"] = ""

            operation_rows.append(row)

            if parameter_type == "unknown":

                unknown_parameters.append(
                    {
                        "operation": operation_name,
                        "parameter": parameter_name,
                        "required": required,
                        "default": repr(default),
                    }
                )

            else:
                known_parameters += 1

    ambiguous_parameter_names = {}

    for parameter_name, types in sorted(
        type_usage.items()
    ):

        if len(types) > 1:

            ambiguous_parameter_names[
                parameter_name
            ] = {
                "types": sorted(types),
                "uses": parameter_usage[
                    parameter_name
                ],
            }

    active_overrides = []

    for operation_name, overrides in sorted(
        OPERATION_PARAMETER_TYPE_OVERRIDES.items()
    ):

        for parameter_name, parameter_type in sorted(
            overrides.items()
        ):

            active_overrides.append(
                {
                    "operation": operation_name,
                    "parameter": parameter_name,
                    "type": parameter_type,
                }
            )

    audit = {
        "summary": {
            "total_operations": len(
                operation_names
            ),
            "total_parameters": total_parameters,
            "known_parameters": known_parameters,
            "unknown_parameters": len(
                unknown_parameters
            ),
            "inspection_failures": len(
                inspection_failures
            ),
            "ambiguous_parameter_names": len(
                ambiguous_parameter_names
            ),
            "active_overrides": len(
                active_overrides
            ),
        },
        "unknown_parameters": unknown_parameters,
        "inspection_failures": inspection_failures,
        "ambiguous_parameter_names": (
            ambiguous_parameter_names
        ),
        "active_overrides": active_overrides,
        "parameter_rows": operation_rows,
    }

    return audit


def save_audit(audit):
    """
    Save JSON and CSV audit reports under data/.
    """

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        JSON_OUTPUT,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            audit,
            file,
            indent=2,
            ensure_ascii=False,
        )

    fieldnames = [
        "operation",
        "parameter",
        "type",
        "required",
        "default",
        "override_active",
        "override_type",
    ]

    with open(
        CSV_OUTPUT,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        writer.writerows(
            audit["parameter_rows"]
        )


def print_audit(audit):
    """
    Print a compact human-readable audit report.
    """

    summary = audit["summary"]

    print("=" * 68)
    print("N.O.V.A. Universal Extraction Coverage Audit")
    print("=" * 68)

    print(
        f"Total registered operations : "
        f"{summary['total_operations']}"
    )

    print(
        f"Total parameters            : "
        f"{summary['total_parameters']}"
    )

    print(
        f"Known parameter types       : "
        f"{summary['known_parameters']}"
    )

    print(
        f"Unknown parameter types     : "
        f"{summary['unknown_parameters']}"
    )

    print(
        f"Signature inspection errors : "
        f"{summary['inspection_failures']}"
    )

    print(
        f"Ambiguous parameter names   : "
        f"{summary['ambiguous_parameter_names']}"
    )

    print(
        f"Active type overrides       : "
        f"{summary['active_overrides']}"
    )

    print("\n" + "-" * 68)
    print("UNKNOWN PARAMETERS")
    print("-" * 68)

    if audit["unknown_parameters"]:

        for item in audit[
            "unknown_parameters"
        ]:

            print(
                f"{item['operation']}."
                f"{item['parameter']}"
                f"  required={item['required']}"
                f"  default={item['default']}"
            )

    else:
        print("None")

    print("\n" + "-" * 68)
    print("SIGNATURE INSPECTION FAILURES")
    print("-" * 68)

    if audit["inspection_failures"]:

        for item in audit[
            "inspection_failures"
        ]:

            print(
                f"{item['operation']}: "
                f"{item['error']}"
            )

    else:
        print("None")

    print("\n" + "-" * 68)
    print("AMBIGUOUS PARAMETER NAMES")
    print("-" * 68)

    if audit[
        "ambiguous_parameter_names"
    ]:

        for parameter_name, info in (
            audit[
                "ambiguous_parameter_names"
            ].items()
        ):

            print(
                f"{parameter_name}: "
                f"{', '.join(info['types'])}"
            )

    else:
        print("None")

    print("\n" + "-" * 68)
    print("ACTIVE OPERATION-SPECIFIC OVERRIDES")
    print("-" * 68)

    if audit["active_overrides"]:

        for item in audit[
            "active_overrides"
        ]:

            print(
                f"{item['operation']}."
                f"{item['parameter']}"
                f" -> {item['type']}"
            )

    else:
        print("None")

    print("\n" + "=" * 68)

    print(
        "JSON report: "
        f"{JSON_OUTPUT.relative_to(PROJECT_ROOT)}"
    )

    print(
        "CSV report : "
        f"{CSV_OUTPUT.relative_to(PROJECT_ROOT)}"
    )

    print("=" * 68)


def main():
    audit = audit_operations()
    save_audit(audit)
    print_audit(audit)


if __name__ == "__main__":
    main()

import csv
import inspect
import json
from collections import Counter, defaultdict
from pathlib import Path

from math_engine.registry import math_registry


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"

JSON_OUTPUT = DATA_DIR / "math_registry_audit.json"
CSV_OUTPUT = DATA_DIR / "math_registry_audit.csv"


# ============================================================
# POSSIBLE INTERNAL / HELPER OPERATIONS
# ============================================================

HELPER_PREFIXES = (
    "parse_",
    "require_",
    "detect_",
)

HELPER_NAMES = {
    "exact_calculus_value",
    "decimal_calculus_value",
    "simplify_calculus_result",
}


def possible_internal_operation(name):
    """
    Flag operations that may be internal helpers rather than
    user-facing mathematical commands.

    This is only an audit hint.

    It does NOT remove or modify anything in the registry.
    """

    if name in HELPER_NAMES:
        return True, "Known utility/helper operation."

    for prefix in HELPER_PREFIXES:

        if name.startswith(prefix):

            return (
                True,
                f"Operation name begins with helper prefix "
                f"'{prefix}'."
            )

    return False, None


# ============================================================
# PARAMETER ANALYSIS
# ============================================================

def classify_parameter(parameter_name):
    """
    Assign a preliminary language-input type based on the
    parameter name.

    These classifications will help us design Interpreter v2.

    They are intentionally broad and can be refined later.
    """

    name = parameter_name.lower()

    # --------------------------------------------------------
    # SYMBOLIC EXPRESSIONS
    # --------------------------------------------------------

    if name in {
        "expression",
        "expr",
        "function",
        "equation",
        "left_side",
        "right_side",
        "numerator",
        "denominator",
        "integrand",
    }:
        return "expression"

    # --------------------------------------------------------
    # VARIABLES
    # --------------------------------------------------------

    if name in {
        "variable",
        "variables",
        "x",
        "y",
        "z",
        "parameter",
    }:
        return "variable"

    # --------------------------------------------------------
    # POINTS / COORDINATES
    # --------------------------------------------------------

    if (
        "point" in name
        or name in {
            "center",
            "vertex",
            "origin",
        }
    ):
        return "point"

    # --------------------------------------------------------
    # VECTORS
    # --------------------------------------------------------

    if (
        "vector" in name
        or "direction" in name
        or name in {
            "field",
            "normal",
        }
    ):
        return "vector"

    # --------------------------------------------------------
    # MATRICES
    # --------------------------------------------------------

    if (
        "matrix" in name
        or name in {
            "matrices",
        }
    ):
        return "matrix"

    # --------------------------------------------------------
    # ANGLES
    # --------------------------------------------------------

    if (
        "angle" in name
        or name in {
            "theta",
            "phi",
            "bearing",
        }
    ):
        return "angle"

    # --------------------------------------------------------
    # INTEGRAL / INTERVAL BOUNDS
    # --------------------------------------------------------

    if name in {
        "lower",
        "upper",
        "lower_bound",
        "upper_bound",
        "start",
        "end",
        "a",
        "b",
    }:
        return "bound_or_value"

    # --------------------------------------------------------
    # COUNTS / ORDERS
    # --------------------------------------------------------

    if name in {
        "order",
        "degree",
        "n",
        "terms",
        "iterations",
        "precision",
        "places",
    }:
        return "integer_or_value"

    # --------------------------------------------------------
    # COMMON GEOMETRIC VALUES
    # --------------------------------------------------------

    if name in {
        "radius",
        "diameter",
        "length",
        "width",
        "height",
        "base",
        "side",
        "side_length",
        "apothem",
        "area",
        "volume",
        "circumference",
        "perimeter",
        "distance",
        "slant_height",
    }:
        return "numeric_value"

    # --------------------------------------------------------
    # GENERIC VALUES
    # --------------------------------------------------------

    if name in {
        "value",
        "values",
        "number",
        "amount",
        "percentage",
        "percent",
        "ratio",
        "scale_factor",
        "factor",
    }:
        return "numeric_value"

    return "unknown"


def analyze_signature(function):
    """
    Inspect a deterministic function's actual Python signature.
    """

    signature = inspect.signature(function)

    parameters = []

    for parameter_name, parameter in signature.parameters.items():

        required = (
            parameter.default
            is inspect.Parameter.empty
            and parameter.kind not in (
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            )
        )

        if parameter.default is inspect.Parameter.empty:
            default = None
        else:
            default = str(parameter.default)

        parameters.append(
            {
                "name": parameter_name,
                "required": required,
                "default": default,
                "kind": str(parameter.kind),
                "language_type": classify_parameter(
                    parameter_name
                ),
            }
        )

    return str(signature), parameters


# ============================================================
# AUDIT
# ============================================================

def audit_registry():
    """
    Inspect every registered NOVA math operation.
    """

    audit = []

    for operation in math_registry.all_operations():

        registry_name = operation["name"]
        function = operation["function"]

        signature, parameters = analyze_signature(
            function
        )

        possible_internal, internal_reason = (
            possible_internal_operation(
                registry_name
            )
        )

        required_parameters = [
            parameter["name"]
            for parameter in parameters
            if parameter["required"]
        ]

        optional_parameters = [
            parameter["name"]
            for parameter in parameters
            if not parameter["required"]
        ]

        parameter_types = [
            parameter["language_type"]
            for parameter in parameters
        ]

        item = {
            "registry_name": registry_name,
            "function_name": function.__name__,
            "module": function.__module__,
            "subsystem": operation["subsystem"],
            "category": operation["category"],
            "description": operation["description"],
            "keywords": operation["keywords"],
            "signature": signature,
            "parameter_count": len(parameters),
            "required_parameters": required_parameters,
            "optional_parameters": optional_parameters,
            "parameter_types": parameter_types,
            "parameters": parameters,
            "possible_internal": possible_internal,
            "internal_reason": internal_reason,
        }

        audit.append(item)

    return audit


# ============================================================
# OUTPUT FILES
# ============================================================

def write_json(audit):
    """
    Save the complete audit as JSON.
    """

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        JSON_OUTPUT,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            audit,
            file,
            indent=4,
            ensure_ascii=False
        )


def write_csv(audit):
    """
    Save a spreadsheet-friendly summary as CSV.
    """

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    fieldnames = [
        "registry_name",
        "function_name",
        "module",
        "subsystem",
        "category",
        "signature",
        "parameter_count",
        "required_parameters",
        "optional_parameters",
        "parameter_types",
        "possible_internal",
        "internal_reason",
        "description",
        "keywords",
    ]

    with open(
        CSV_OUTPUT,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for item in audit:

            row = dict(item)

            row.pop(
                "parameters",
                None
            )

            row["required_parameters"] = ", ".join(
                item["required_parameters"]
            )

            row["optional_parameters"] = ", ".join(
                item["optional_parameters"]
            )

            row["parameter_types"] = ", ".join(
                item["parameter_types"]
            )

            row["keywords"] = ", ".join(
                item["keywords"]
            )

            writer.writerow(row)


# ============================================================
# TERMINAL SUMMARY
# ============================================================

def print_summary(audit):
    """
    Print the most useful audit information to the terminal.
    """

    subsystem_counts = Counter(
        item["subsystem"]
        for item in audit
    )

    category_counts = Counter(
        item["category"]
        for item in audit
    )

    parameter_type_counts = Counter()

    parameter_name_counts = Counter()

    unknown_parameters = defaultdict(
        list
    )

    possible_internal = []

    for item in audit:

        if item["possible_internal"]:
            possible_internal.append(
                item
            )

        for parameter in item["parameters"]:

            parameter_type_counts[
                parameter["language_type"]
            ] += 1

            parameter_name_counts[
                parameter["name"]
            ] += 1

            if (
                parameter["language_type"]
                == "unknown"
            ):
                unknown_parameters[
                    parameter["name"]
                ].append(
                    item["registry_name"]
                )

    print()
    print("=" * 60)
    print("N.O.V.A. MATH REGISTRY AUDIT")
    print("=" * 60)

    print(
        f"\nTotal registered operations: "
        f"{len(audit)}"
    )

    print("\nOperations by subsystem:")

    for subsystem, count in sorted(
        subsystem_counts.items()
    ):
        print(
            f"  {subsystem}: {count}"
        )

    print("\nParameter language types:")

    for parameter_type, count in (
        parameter_type_counts.most_common()
    ):
        print(
            f"  {parameter_type}: {count}"
        )

    print("\nMost common parameter names:")

    for parameter_name, count in (
        parameter_name_counts.most_common(25)
    ):
        print(
            f"  {parameter_name}: {count}"
        )

    print(
        "\nPossible internal/helper operations:"
    )

    for item in possible_internal:

        print(
            f"  {item['registry_name']}"
            f"{item['signature']}"
        )

    print(
        f"\nPossible internal count: "
        f"{len(possible_internal)}"
    )

    print("\nUnknown parameter types:")

    if not unknown_parameters:

        print("  None")

    else:

        for parameter_name, operations in sorted(
            unknown_parameters.items()
        ):

            print(
                f"\n  {parameter_name}"
            )

            for operation_name in operations[:10]:

                print(
                    f"    - {operation_name}"
                )

            if len(operations) > 10:

                print(
                    f"    ... and "
                    f"{len(operations) - 10} more"
                )

    print("\nLargest categories:")

    for category, count in (
        category_counts.most_common(20)
    ):

        print(
            f"  {category}: {count}"
        )

    print("\nOutput files:")

    print(
        f"  JSON: {JSON_OUTPUT}"
    )

    print(
        f"  CSV:  {CSV_OUTPUT}"
    )

    print()
    print("=" * 60)
    print("Registry Audit Complete")
    print("=" * 60)
    print()


# ============================================================
# MAIN
# ============================================================

def main():

    audit = audit_registry()

    write_json(
        audit
    )

    write_csv(
        audit
    )

    print_summary(
        audit
    )


if __name__ == "__main__":
    main()
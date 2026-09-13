from veterinary_subsystem.database_loader import load_veterinary_database


def search_by_fields(excel_path, filters):
    """
    Search the Guide sheet using multiple exact-match filters.

    Example:
        {
            "host_species": "cattle",
            "target_system": "gastrointestinal"
        }
    """

    workbook = load_veterinary_database(excel_path)
    guide = workbook["Guide"]

    mask = True

    for field_name, search_value in filters.items():

        if field_name not in guide.columns:
            raise ValueError(f"Unknown field: {field_name}")

        column = guide[field_name].fillna("").astype(str)

        field_mask = column.apply(
            lambda cell: search_value.lower()
            in [item.strip().lower() for item in cell.split("|")]
        )

        mask = mask & field_mask

    results = guide.loc[
        mask,
        [
            "entity_id",
            "Diagnosis",
            *filters.keys()
        ]
    ]

    return results


def search_text_field(excel_path, field_name, search_text):
    """
    Search a free-text field using case-insensitive partial matching.
    """

    workbook = load_veterinary_database(excel_path)
    guide = workbook["Guide"]

    if field_name not in guide.columns:
        raise ValueError(f"Unknown field: {field_name}")

    column = guide[field_name].fillna("").astype(str)

    mask = column.str.contains(
        search_text,
        case=False,
        regex=False
    )

    results = guide.loc[
        mask,
        [
            "entity_id",
            "Diagnosis",
            field_name
        ]
    ]

    return results


def combined_search(excel_path, structured_filters=None, text_filters=None):
    """
    Search the Guide sheet using both structured exact-match filters
    and free-text partial-match filters.

    Example:
        structured_filters = {
            "host_species": "cattle"
        }

        text_filters = {
            "clinical_signs": "dehydration"
        }
    """

    workbook = load_veterinary_database(excel_path)
    guide = workbook["Guide"]

    # Start with every row included.
    mask = True

    # Apply structured exact-match filters.
    if structured_filters:
        for field_name, search_value in structured_filters.items():

            if field_name not in guide.columns:
                raise ValueError(f"Unknown field: {field_name}")

            column = guide[field_name].fillna("").astype(str)

            field_mask = column.apply(
                lambda cell: search_value.lower()
                in [item.strip().lower() for item in cell.split("|")]
            )

            mask = mask & field_mask

    # Apply free-text filters.
    if text_filters:
        for field_name, search_text in text_filters.items():

            if field_name not in guide.columns:
                raise ValueError(f"Unknown field: {field_name}")

            column = guide[field_name].fillna("").astype(str)

            field_mask = column.str.contains(
                search_text,
                case=False,
                regex=False
            )

            mask = mask & field_mask

    results = guide.loc[mask]

    return results


if __name__ == "__main__":

    structured_filters = {
        "host_species": "cattle"
    }

    text_filters = {
        "clinical_signs": "dehydration"
    }

    results = combined_search(
        r"data\Pathophysiology Guide.xlsx",
        structured_filters=structured_filters,
        text_filters=text_filters
    )

    print(
        results[
            [
                "entity_id",
                "Diagnosis",
                "host_species",
                "clinical_signs"
            ]
        ].to_string(index=False)
    )
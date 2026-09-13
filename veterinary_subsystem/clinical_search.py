from veterinary_subsystem.database_loader import load_veterinary_database


FIELD_WEIGHTS = {
    "Diagnosis": 5,
    "alternate_names": 4,
    "associated_complexes": 2,
    "pathogenesis": 3,
    "mechanism_of_action": 3,
    "pathophysiology": 4,
    "molecular_target": 3,
    "lesions": 3,
    "clinical_signs": 4,
    "complications": 2,
    "diagnostic_approach": 2,
    "high_yield_notes": 1,
}


def matches_structured_filters(row, guide, structured_filters):
    """
    Return True if the row satisfies all structured filters.
    """

    if not structured_filters:
        return True

    for field_name, search_value in structured_filters.items():

        if field_name not in guide.columns:
            raise ValueError(
                f"Unknown structured field: {field_name}"
            )

        value = row[field_name]

        if value is None:
            return False

        text = str(value)

        if text.lower() == "nan":
            return False

        values = [
            item.strip().lower()
            for item in text.split("|")
        ]

        if search_value.lower().strip() not in values:
            return False

    return True


def search_veterinary_database(
    excel_path,
    search_query,
    structured_filters=None
):
    """
    Search the veterinary Guide sheet.

    Parameters
    ----------
    excel_path : str
        Path to the Excel workbook.

    search_query : str
        Free-text clinical query, such as:
        "watery diarrhea dehydration"

    structured_filters : dict or None
        Optional hard filters, such as:
        {
            "host_species": "cattle"
        }

    Returns
    -------
    list of dict
        Ranked veterinary entities with explainable scoring.
    """

    workbook = load_veterinary_database(excel_path)
    guide = workbook["Guide"]

    search_terms = [
        term.lower().strip()
        for term in search_query.split()
        if term.strip()
    ]

    results = []

    for _, row in guide.iterrows():

        if not matches_structured_filters(
            row,
            guide,
            structured_filters
        ):
            continue

        matched_fields = set()
        matched_terms = set()
        weighted_score = 0
        match_details = []

        for field_name, field_weight in FIELD_WEIGHTS.items():

            if field_name not in guide.columns:
                continue

            value = row[field_name]

            if value is None:
                continue

            text = str(value)

            if text.lower() == "nan":
                continue

            text_lower = text.lower()

            for search_term in search_terms:

                if search_term in text_lower:

                    matched_fields.add(field_name)
                    matched_terms.add(search_term)

                    weighted_score += field_weight

                    match_details.append(
                        {
                            "term": search_term,
                            "field": field_name,
                            "weight": field_weight,
                        }
                    )

        if weighted_score > 0:

            coverage = (
                len(matched_terms) / len(search_terms)
                if search_terms
                else 0.0
            )

            results.append(
                {
                    "entity_id": row["entity_id"],
                    "Diagnosis": row["Diagnosis"],
                    "weighted_score": weighted_score,
                    "coverage": coverage,
                    "matched_terms": sorted(matched_terms),
                    "matched_fields": sorted(matched_fields),
                    "match_details": match_details,
                }
            )

    results.sort(
        key=lambda item: (
            item["coverage"],
            item["weighted_score"]
        ),
        reverse=True
    )

    return results


def format_veterinary_results(results):
    """
    Convert veterinary search results into cleaner GUI-friendly text.
    """

    if not results:
        return "No veterinary matches found."

    lines = []

    for index, result in enumerate(results, start=1):

        coverage = result["coverage"]

        if coverage >= 0.80:
            relevance = "High"
        elif coverage >= 0.50:
            relevance = "Moderate"
        else:
            relevance = "Low"

        lines.append(
            f"{index}. {result['Diagnosis']}"
        )

        lines.append(
            f"   Entity ID: {result['entity_id']}"
        )

        lines.append(
            f"   Relevance: {relevance}"
        )

        lines.append(
            "   Matched clinical features: "
            + ", ".join(result["matched_terms"])
        )

        lines.append(
            "   Evidence found in: "
            + ", ".join(result["matched_fields"])
        )

        lines.append(
            f"   Internal score: "
            f"{result['weighted_score']} | "
            f"Coverage: {result['coverage']:.2f}"
        )

        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":

    results = search_veterinary_database(
        r"data\Pathophysiology Guide.xlsx",
        "watery diarrhea dehydration",
        structured_filters={
            "host_species": "cattle"
        }
    )

    print(
        format_veterinary_results(results)
    )
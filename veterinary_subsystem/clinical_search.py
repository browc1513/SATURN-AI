import re

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


VETERINARY_STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "have",
    "having",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "the",
    "to",
    "what",
    "which",
    "who",
    "with",
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


def _clean_search_terms(search_query, structured_filters=None):
    """
    Convert free-text input into meaningful clinical search terms.

    Common stop words are removed. Values already used as structured
    filters, such as "cattle", are also removed from free-text scoring
    so they do not artificially increase coverage.
    """

    structured_values = set()

    if structured_filters:
        structured_values = {
            str(value).strip().lower()
            for value in structured_filters.values()
            if str(value).strip()
        }

    raw_terms = re.findall(
        r"[A-Za-z0-9_-]+",
        str(search_query).lower()
    )

    return [
        term
        for term in raw_terms
        if (
            term
            and term not in VETERINARY_STOP_WORDS
            and term not in structured_values
        )
    ]


def _term_matches_text(search_term, text):
    """
    Match a term as a complete token instead of a loose substring.
    """

    pattern = (
        r"(?<![A-Za-z0-9_])"
        + re.escape(search_term)
        + r"(?![A-Za-z0-9_])"
    )

    return re.search(
        pattern,
        text,
        flags=re.IGNORECASE
    ) is not None


def search_veterinary_database(
    excel_path,
    search_query,
    structured_filters=None
):
    """
    Search the veterinary Guide sheet.
    """

    workbook = load_veterinary_database(excel_path)
    guide = workbook["Guide"]

    search_terms = _clean_search_terms(
        search_query,
        structured_filters=structured_filters
    )

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

            for search_term in search_terms:

                if _term_matches_text(
                    search_term,
                    text
                ):
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

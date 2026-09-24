import pytest

from core.saturn_personality import SATURN
from math_engine.argument_extractor import (
    extract_arguments_for_operation,
)
from math_engine.math_pipeline import (
    interpret_and_execute_math,
)
from math_engine.router import (
    select_math_operation,
)


@pytest.mark.parametrize(
    ("query", "operation"),
    [
        (
            "Find the difference between 9 and 4.",
            "subtract",
        ),
        (
            "Factor x^2 - 9.",
            "factor_expression",
        ),
        (
            "Factor the polynomial x^2 - 9.",
            "factor_expression",
        ),
        (
            "Calculate the mean of 2, 4, and 6.",
            "arithmetic_mean",
        ),
        (
            "What is the average of 2, 4, and 6?",
            "arithmetic_mean",
        ),
    ],
)
def test_structured_math_intent_selects_operation(
    query,
    operation,
):
    result = select_math_operation(
        query
    )

    assert result["success"] is True
    assert result["operation"] == operation


def test_difference_arguments_are_extracted():
    result = extract_arguments_for_operation(
        "Find the difference between 9 and 4.",
        "subtract",
    )

    assert result["success"] is True
    assert result["arguments"] == {
        "a": 9,
        "b": 4,
    }


@pytest.mark.parametrize(
    "query",
    [
        "Calculate the mean of 2, 4, and 6.",
        "What is the average of 2, 4, and 6?",
    ],
)
def test_mean_values_are_extracted(
    query,
):
    result = extract_arguments_for_operation(
        query,
        "arithmetic_mean",
    )

    assert result["success"] is True
    assert result["arguments"] == {
        "values": [
            2,
            4,
            6,
        ],
    }


@pytest.mark.parametrize(
    ("query", "operation", "exact_result"),
    [
        (
            "Find the difference between 9 and 4.",
            "subtract",
            "5",
        ),
        (
            "Factor x^2 - 9.",
            "factor_expression",
            "(x - 3)*(x + 3)",
        ),
        (
            "Calculate the mean of 2, 4, and 6.",
            "arithmetic_mean",
            "4",
        ),
        (
            "What is the average of 2, 4, and 6?",
            "arithmetic_mean",
            "4",
        ),
    ],
)
def test_math_pipeline_executes_structured_requests(
    query,
    operation,
    exact_result,
):
    result = interpret_and_execute_math(
        query
    )

    assert result["success"] is True
    assert result["operation"] == operation
    assert str(
        result["exact_result"]
    ) == exact_result


@pytest.mark.parametrize(
    "query",
    [
        "Find the difference between 9 and 4.",
        "Factor x^2 - 9.",
        "Calculate the mean of 2, 4, and 6.",
    ],
)
def test_saturn_completes_structured_math_requests(
    query,
):
    saturn = SATURN(
        start_alarm_monitor=False
    )

    result = saturn.handle_query(
        query
    )

    assert result["success"] is True
    assert result["domain"] == "math"

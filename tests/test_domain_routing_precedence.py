from unittest.mock import patch

import pytest

from core.saturn_personality import SATURN


@pytest.fixture
def saturn():
    return SATURN(
        start_alarm_monitor=False
    )


@pytest.mark.parametrize(
    "query",
    [
        "What does never mind mean?",
        "What does power mean in politics?",
        "What is the meaning of product design?",
        "What is the difference between a frog and a toad?",
        "Explain the difference between speed and velocity",
        "Tell me about matrix theory",
        "Explain what an average salary represents",
        "What is the average salary for a physicist?",
    ],
)
def test_explanatory_questions_use_conversation(
    saturn,
    query,
):
    assert saturn._detect_domain(query) == "unknown"

    conversational_result = {
        "success": True,
        "domain": "conversation",
        "response": "Conversational explanation.",
        "data": None,
    }

    with patch.object(
        saturn,
        "_handle_unknown_query",
        return_value=conversational_result,
    ) as mocked_conversation:
        result = saturn.handle_query(
            query,
            session_id="routing-test",
        )

    assert result["domain"] == "conversation"
    mocked_conversation.assert_called_once_with(
        query,
        session_id="routing-test",
    )


@pytest.mark.parametrize(
    "query",
    [
        "Calculate the mean of 2, 4, and 6",
        "Compute the average of 10 and 20",
        "Find the standard deviation of 1, 2, and 3",
        "What is the mean of 2, 4, and 6?",
        "What's the average of 10 and 20?",
        "Mean of 5, 10, and 15",
        "What is 6 times 7?",
        "17 + 28",
        "x^2",
    ],
)
def test_explicit_math_remains_math(
    saturn,
    query,
):
    assert saturn._detect_domain(query) == "math"


@pytest.mark.parametrize(
    ("query", "expected_domain"),
    [
        (
            "What is the average temperature outside?",
            "weather",
        ),
        (
            "What is the average weight of a dog?",
            "veterinary",
        ),
        (
            "Add product design book to my reading list",
            "lists",
        ),
        (
            "What time is it?",
            "time",
        ),
        (
            "Show my alarms",
            "alarms",
        ),
    ],
)
def test_existing_higher_priority_domains_remain_stable(
    saturn,
    query,
    expected_domain,
):
    assert saturn._detect_domain(
        query
    ) == expected_domain

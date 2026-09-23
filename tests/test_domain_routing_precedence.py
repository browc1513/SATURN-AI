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


@pytest.mark.parametrize(
    "query",
    [
        "What product should I buy?",
        "How much power does my computer use?",
        "What is the baggage limit?",
        "What is the maximum highway speed?",
        "What is the minimum age to rent a car?",
        "What area of town should I visit?",
        "What volume should the music be?",
        "What is the radius of Earth?",
        "That answer was a factor in my decision",
        "Which direction is that vector pointing?",
    ],
)
def test_ambiguous_math_words_use_conversation(
    saturn,
    query,
):
    assert saturn._detect_domain(query) == "unknown"


@pytest.mark.parametrize(
    "query",
    [
        "What is the sum of 3 and 5?",
        "What is the difference between 10 and 4?",
        "What is the product of 6 and 7?",
        "6 times 7",
        "Factor x^2 - 9",
        "2 to the power of 8",
        "Find the limit of x^2 as x approaches 2",
        "Limit of x^2 as x approaches 2",
        "Find the maximum of x^2 - 4*x",
        "Calculate the minimum of x^2 + 2*x",
        "What is the area of a circle with radius 7?",
        "Find the volume of a sphere with radius 4",
        "Tangent of 45 degrees",
        "Find the tangent line to x^2 at x = 2",
        "Find the vector magnitude of (3, 4)",
        "Find the magnitude of the vector (3, 4)",
    ],
)
def test_structured_ambiguous_math_words_remain_math(
    saturn,
    query,
):
    assert saturn._detect_domain(query) == "math"

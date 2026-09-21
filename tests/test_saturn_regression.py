import pytest

from core.saturn_instance import get_saturn


@pytest.fixture(scope="module")
def saturn():
    return get_saturn(start_alarm_monitor=False)


@pytest.mark.parametrize(
    ("query", "expected_domain", "expected_success"),
    [
        ("What is 2 plus 2?", "math", True),
        ("What is 20 divided by 4?", "math", True),
        ("6 * 7", "math", True),
        ("What time is it?", "time", True),
        ("Show my lists", "lists", True),
        ("Show my alarms", "alarms", True),
        ("Paint the moon purple", "unknown", False),
    ],
)
def test_released_query_routing(
    saturn,
    query,
    expected_domain,
    expected_success,
):
    result = saturn.handle_query(query)

    assert result.get("domain") == expected_domain
    assert result.get("success") is expected_success
    assert isinstance(result.get("response"), str)
    assert result["response"].strip()


def test_spoken_division_result(saturn):
    result = saturn.handle_query(
        "What is 20 divided by 4?"
    )

    assert result["domain"] == "math"
    assert result["success"] is True
    assert "Result: 5" in result["response"]


def test_symbolic_multiplication_result(saturn):
    result = saturn.handle_query("6 * 7")

    assert result["domain"] == "math"
    assert result["success"] is True
    assert "Result: 42" in result["response"]

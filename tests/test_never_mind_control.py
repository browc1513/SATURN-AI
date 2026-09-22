from unittest.mock import patch

import pytest

from core.saturn_personality import SATURN


@pytest.mark.parametrize(
    "query",
    [
        "Never mind",
        "Nevermind",
        "Forget it",
        "Disregard that",
        "Cancel that",
        "Never mind.",
        "Never mind!",
        "Never mind Saturn",
        "NEVER MIND",
        "  never   mind  ",
    ],
)
def test_cancel_interaction_commands_return_control(
    query,
):
    saturn = SATURN(
        start_alarm_monitor=False
    )

    with patch.object(
        saturn,
        "_handle_unknown_query",
    ) as mocked_unknown:
        result = saturn.handle_query(
            query,
            session_id="test-session",
        )

    assert result == {
        "success": True,
        "domain": "control",
        "response": "Okay.",
        "data": {
            "action": "cancel_interaction",
        },
    }
    mocked_unknown.assert_not_called()


def test_cancel_interaction_is_not_stored_in_memory():
    saturn = SATURN(
        start_alarm_monitor=False
    )

    result = saturn.handle_query(
        "Never mind",
        session_id="phone-a",
    )

    assert result["success"] is True
    assert (
        saturn.conversation_memory.get_history(
            "phone-a"
        )
        == []
    )


@pytest.mark.parametrize(
    ("query", "expected_domain"),
    [
        (
            "Cancel my 7 AM alarm",
            "alarms",
        ),
        (
            "Stop the alarm",
            "alarms",
        ),
    ],
)
def test_alarm_commands_are_not_interaction_cancellations(
    query,
    expected_domain,
):
    saturn = SATURN(
        start_alarm_monitor=False
    )

    assert saturn._detect_domain(
        query
    ) == expected_domain


@pytest.mark.parametrize(
    "query",
    [
        "Please remember that I said never mind yesterday",
        "What does never mind mean?",
        "Do not forget it happened",
    ],
)
def test_longer_queries_are_not_cancelled(
    query,
):
    saturn = SATURN(
        start_alarm_monitor=False
    )

    result = saturn.handle_query(
        query
    )

    assert result["domain"] != "control"
    assert result.get(
        "data",
        {},
    ) != {
        "action": "cancel_interaction",
    }

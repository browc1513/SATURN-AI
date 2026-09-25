from unittest.mock import Mock
from unittest.mock import patch

from core.saturn_personality import SATURN


WEATHER_QUERY = "What is the weather today?"
WEATHER_RESPONSE = "It is 72 degrees and sunny."

WEATHER_RESULT = {
    "success": True,
    "domain": "weather",
    "response": WEATHER_RESPONSE,
}


def create_saturn():
    return SATURN(
        start_alarm_monitor=False
    )


def run_weather_query(
    saturn,
    *,
    session_id="phone-session",
    result=None,
):
    if result is None:
        result = WEATHER_RESULT

    with patch.object(
        saturn,
        "_detect_domain",
        return_value="weather",
    ):
        with patch.object(
            saturn,
            "_handle_weather_query",
            return_value=result,
        ):
            return saturn.handle_query(
                WEATHER_QUERY,
                session_id=session_id,
            )


def test_successful_subsystem_result_is_remembered():
    saturn = create_saturn()

    result = run_weather_query(
        saturn
    )

    assert result == WEATHER_RESULT
    assert saturn.conversation_memory.get_history(
        "phone-session"
    ) == [
        {
            "role": "user",
            "content": WEATHER_QUERY,
        },
        {
            "role": "assistant",
            "content": WEATHER_RESPONSE,
        },
    ]


def test_failed_subsystem_result_is_not_remembered():
    saturn = create_saturn()

    failure = {
        "success": False,
        "domain": "weather",
        "response": "Weather service unavailable.",
    }

    result = run_weather_query(
        saturn,
        result=failure,
    )

    assert result == failure
    assert saturn.conversation_memory.get_history(
        "phone-session"
    ) == []


def test_subsystem_result_reaches_model_follow_up():
    saturn = create_saturn()

    run_weather_query(
        saturn
    )

    local_model = Mock()
    local_model.model = "test-model"
    local_model.chat.return_value = (
        "Yes, sunglasses would be useful."
    )
    saturn.local_model = local_model

    with patch.object(
        saturn,
        "_detect_domain",
        return_value="unknown",
    ):
        result = saturn.handle_query(
            "Should I bring sunglasses?",
            session_id="phone-session",
        )

    assert result["success"] is True
    assert result["domain"] == "conversation"

    call = local_model.chat.call_args
    history = call.kwargs["conversation_history"]

    assert history == [
        {
            "role": "user",
            "content": WEATHER_QUERY,
        },
        {
            "role": "assistant",
            "content": WEATHER_RESPONSE,
        },
    ]


def test_conversation_result_is_not_stored_twice():
    saturn = create_saturn()

    local_model = Mock()
    local_model.model = "test-model"
    local_model.chat.return_value = "Hello there."
    saturn.local_model = local_model

    with patch.object(
        saturn,
        "_detect_domain",
        return_value="unknown",
    ):
        saturn.handle_query(
            "Hello",
            session_id="phone-session",
        )

    assert saturn.conversation_memory.get_history(
        "phone-session"
    ) == [
        {
            "role": "user",
            "content": "Hello",
        },
        {
            "role": "assistant",
            "content": "Hello there.",
        },
    ]


def test_subsystem_history_remains_session_isolated():
    saturn = create_saturn()

    run_weather_query(
        saturn,
        session_id="phone-a",
    )

    assert saturn.conversation_memory.get_history(
        "phone-a"
    )
    assert saturn.conversation_memory.get_history(
        "phone-b"
    ) == []


def test_result_without_a_response_is_not_remembered():
    saturn = create_saturn()

    result = {
        "success": True,
        "domain": "weather",
        "response": "",
    }

    run_weather_query(
        saturn,
        result=result,
    )

    assert saturn.conversation_memory.get_history(
        "phone-session"
    ) == []

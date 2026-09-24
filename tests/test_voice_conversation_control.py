import pytest

from voice.conversation_control import (
    is_silent_follow_up_timeout,
    load_voice_timing,
    should_listen_for_follow_up,
)


def test_default_voice_timing():
    timing = load_voice_timing({})

    assert timing == {
        "command_timeout": 8.0,
        "command_phrase_limit": 25.0,
        "follow_up_timeout": 10.0,
        "follow_up_phrase_limit": 10.0,
    }


def test_voice_timing_accepts_environment_overrides():
    timing = load_voice_timing(
        {
            "SATURN_VOICE_COMMAND_TIMEOUT": "12",
            "SATURN_VOICE_COMMAND_PHRASE_LIMIT": "30",
            "SATURN_VOICE_FOLLOW_UP_TIMEOUT": "7",
            "SATURN_VOICE_FOLLOW_UP_PHRASE_LIMIT": "5",
        }
    )

    assert timing == {
        "command_timeout": 12.0,
        "command_phrase_limit": 30.0,
        "follow_up_timeout": 7.0,
        "follow_up_phrase_limit": 5.0,
    }


@pytest.mark.parametrize(
    "value",
    [
        "0",
        "-1",
        "not-a-number",
        "",
    ],
)
def test_invalid_voice_timing_is_rejected(
    value,
):
    with pytest.raises(
        ValueError,
        match="positive number",
    ):
        load_voice_timing(
            {
                "SATURN_VOICE_COMMAND_TIMEOUT": value,
            }
        )


def test_reboot_request_requires_follow_up():
    result = {
        "success": True,
        "domain": "control",
        "response": "Confirm reboot.",
        "data": {
            "action": "reboot_requested",
        },
    }

    assert should_listen_for_follow_up(
        result
    ) is True


@pytest.mark.parametrize(
    "result",
    [
        None,
        {},
        {"data": None},
        {"data": {}},
        {
            "data": {
                "action": "cancel_interaction",
            }
        },
        {
            "data": {
                "action": "reboot_cancelled",
            }
        },
        {
            "data": {
                "action": "reboot_confirmed",
            }
        },
    ],
)
def test_completed_actions_do_not_require_follow_up(
    result,
):
    assert should_listen_for_follow_up(
        result
    ) is False


def test_successful_conversation_opens_follow_up_window():
    result = {
        "success": True,
        "domain": "conversation",
        "response": "Conversational response.",
        "data": {
            "provider": "ollama",
        },
    }

    assert should_listen_for_follow_up(
        result
    ) is True


def test_failed_conversation_does_not_open_follow_up():
    result = {
        "success": False,
        "domain": "conversation",
        "response": "Model unavailable.",
        "data": None,
    }

    assert should_listen_for_follow_up(
        result
    ) is False


def test_explicit_follow_up_flag_is_supported():
    result = {
        "success": True,
        "domain": "control",
        "response": "Please answer.",
        "data": {
            "follow_up_required": True,
        },
    }

    assert should_listen_for_follow_up(
        result
    ) is True


def test_idle_follow_up_timeout_closes_silently():
    result = {
        "success": False,
        "text": "",
        "response": "I didn't hear anything.",
        "error": "Microphone listening timed out.",
    }

    assert is_silent_follow_up_timeout(
        result
    ) is True


def test_non_timeout_stt_error_is_not_silent():
    result = {
        "success": False,
        "text": "",
        "response": "Microphone unavailable.",
        "error": "No microphone.",
    }

    assert is_silent_follow_up_timeout(
        result
    ) is False

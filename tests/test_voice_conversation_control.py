import pytest

from voice.conversation_control import (
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

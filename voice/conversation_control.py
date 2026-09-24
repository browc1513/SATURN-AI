"""
Configuration and state helpers for SATURN voice conversations.

This module contains no microphone or audio dependencies, allowing the
conversation flow to be tested silently on any development computer.
"""

import os


DEFAULT_COMMAND_TIMEOUT = 8.0
DEFAULT_COMMAND_PHRASE_LIMIT = 25.0
DEFAULT_FOLLOW_UP_TIMEOUT = 10.0
DEFAULT_FOLLOW_UP_PHRASE_LIMIT = 10.0

FOLLOW_UP_ACTIONS = {
    "reboot_requested",
}

CONVERSATIONAL_FOLLOW_UP_DOMAINS = {
    "conversation",
}


def _positive_seconds(
    environment,
    variable,
    default,
):
    raw_value = environment.get(
        variable,
        str(default),
    )

    try:
        value = float(raw_value)
    except (
        TypeError,
        ValueError,
    ) as error:
        raise ValueError(
            f"{variable} must be a positive number."
        ) from error

    if value <= 0:
        raise ValueError(
            f"{variable} must be a positive number."
        )

    return value


def load_voice_timing(environment=None):
    """
    Load configurable microphone timing without opening the microphone.
    """

    if environment is None:
        environment = os.environ

    return {
        "command_timeout": _positive_seconds(
            environment,
            "SATURN_VOICE_COMMAND_TIMEOUT",
            DEFAULT_COMMAND_TIMEOUT,
        ),
        "command_phrase_limit": _positive_seconds(
            environment,
            "SATURN_VOICE_COMMAND_PHRASE_LIMIT",
            DEFAULT_COMMAND_PHRASE_LIMIT,
        ),
        "follow_up_timeout": _positive_seconds(
            environment,
            "SATURN_VOICE_FOLLOW_UP_TIMEOUT",
            DEFAULT_FOLLOW_UP_TIMEOUT,
        ),
        "follow_up_phrase_limit": _positive_seconds(
            environment,
            "SATURN_VOICE_FOLLOW_UP_PHRASE_LIMIT",
            DEFAULT_FOLLOW_UP_PHRASE_LIMIT,
        ),
    }


def should_listen_for_follow_up(result):
    """
    Return True while SATURN should keep the conversation open.

    Explicit workflows such as reboot confirmation can request a
    follow-up through their action or follow_up_required flag.
    Successful conversational-model responses also open a short
    hands-free follow-up window.
    """

    if not isinstance(result, dict):
        return False

    if not result.get("success"):
        return False

    data = result.get("data")

    if isinstance(data, dict):
        if data.get("follow_up_required") is True:
            return True

        if data.get("action") in FOLLOW_UP_ACTIONS:
            return True

    return (
        result.get("domain")
        in CONVERSATIONAL_FOLLOW_UP_DOMAINS
    )


def is_silent_follow_up_timeout(speech_result):
    """
    Return True when an idle follow-up window ended normally.

    Silence after a completed conversational response means the user
    is finished. It is not an error and should not trigger another
    spoken prompt.
    """

    if not isinstance(speech_result, dict):
        return False

    return (
        speech_result.get("success") is False
        and speech_result.get("error")
        == "Microphone listening timed out."
    )

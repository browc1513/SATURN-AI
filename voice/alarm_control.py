"""
Restricted wake-word-free voice controls for ringing alarms.
"""

import re


ALARM_CONTROL_TIMEOUT_SECONDS = 2.0
ALARM_CONTROL_PHRASE_LIMIT_SECONDS = 8.0


def normalize_alarm_control(text):
    normalized = str(
        text or ""
    ).strip().lower()

    normalized = re.sub(
        r"[^\w\s-]",
        " ",
        normalized,
    )

    return " ".join(
        normalized.split()
    )


def is_wake_free_alarm_command(text):
    """
    Accept only stop and snooze commands while an alarm rings.

    Other speech is deliberately ignored rather than routed into
    SATURN's normal conversation system.
    """

    normalized = normalize_alarm_control(
        text
    )

    stop_commands = {
        "stop",
        "stop alarm",
        "stop the alarm",
        "dismiss",
        "dismiss alarm",
        "dismiss the alarm",
        "silence alarm",
        "silence the alarm",
        "turn off alarm",
        "turn off the alarm",
    }

    if normalized in stop_commands:
        return True

    return bool(
        re.fullmatch(
            r"snooze"
            r"(?:\s+(?:the\s+)?alarm)?"
            r"(?:\s+for\s+.+)?",
            normalized,
        )
    )

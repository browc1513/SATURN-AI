"""
Playback-mode policy for SATURN alarms.

New alarms default to ringing until they are explicitly stopped or
snoozed. Timed alarms stop automatically after a validated duration.
"""

import re


TIMED_MODE = "timed"
UNTIL_DISMISSED_MODE = "until_dismissed"

DEFAULT_ALARM_PLAYBACK_MODE = (
    UNTIL_DISMISSED_MODE
)

DEFAULT_TIMED_ALARM_SECONDS = 30
MINIMUM_TIMED_ALARM_SECONDS = 5
MAXIMUM_TIMED_ALARM_SECONDS = 1800


def validate_timed_alarm_seconds(value):
    """
    Return a validated integer duration or None.
    """

    try:
        seconds = int(value)
    except (
        TypeError,
        ValueError,
    ):
        return None

    if not (
        MINIMUM_TIMED_ALARM_SECONDS
        <= seconds
        <= MAXIMUM_TIMED_ALARM_SECONDS
    ):
        return None

    return seconds


def parse_alarm_playback_policy(text):
    """
    Parse an alarm's requested playback behavior.

    Examples:
        Set an alarm for 8 AM.
        Set an alarm for 8 AM until dismissed.
        Set an alarm for 8 AM for 45 seconds.
        Set a timed alarm for 8 AM.
    """

    normalized = re.sub(
        r"\s+",
        " ",
        str(text or "").strip().lower(),
    )

    persistent_patterns = [
        r"\buntil\s+(?:i\s+)?(?:stop|dismiss|snooze)"
        r"(?:\s+it)?\b",
        r"\buntil\s+(?:stopped|dismissed|snoozed)\b",
        r"\bkeep\s+ringing\b",
        r"\bring\s+until\b",
    ]

    if any(
        re.search(
            pattern,
            normalized,
        )
        for pattern in persistent_patterns
    ):
        return {
            "success": True,
            "mode": UNTIL_DISMISSED_MODE,
            "duration_seconds": None,
            "explicit": True,
            "error": None,
        }

    duration_match = re.search(
        r"\bfor\s+(\d+)\s*"
        r"(seconds?|secs?|minutes?|mins?)\b",
        normalized,
    )

    if duration_match:
        amount = int(
            duration_match.group(1)
        )
        unit = duration_match.group(2)

        if unit.startswith(
            (
                "minute",
                "min",
            )
        ):
            amount *= 60

        seconds = validate_timed_alarm_seconds(
            amount
        )

        if seconds is None:
            return {
                "success": False,
                "mode": TIMED_MODE,
                "duration_seconds": amount,
                "explicit": True,
                "error": (
                    "Timed alarm duration must be between "
                    "5 seconds and 30 minutes."
                ),
            }

        return {
            "success": True,
            "mode": TIMED_MODE,
            "duration_seconds": seconds,
            "explicit": True,
            "error": None,
        }

    if re.search(
        r"\b(?:timed|self[- ]stopping)"
        r"(?:\s+alarm)?\b",
        normalized,
    ):
        return {
            "success": True,
            "mode": TIMED_MODE,
            "duration_seconds": (
                DEFAULT_TIMED_ALARM_SECONDS
            ),
            "explicit": True,
            "error": None,
        }

    return {
        "success": True,
        "mode": DEFAULT_ALARM_PLAYBACK_MODE,
        "duration_seconds": None,
        "explicit": False,
        "error": None,
    }


def normalize_saved_playback_policy(
    mode,
    duration_seconds,
):
    """
    Validate playback settings loaded from an alarm record.

    Invalid or unknown records fall back safely to the new default.
    """

    if mode == UNTIL_DISMISSED_MODE:
        return {
            "mode": UNTIL_DISMISSED_MODE,
            "duration_seconds": None,
        }

    if mode == TIMED_MODE:
        seconds = validate_timed_alarm_seconds(
            duration_seconds
        )

        if seconds is not None:
            return {
                "mode": TIMED_MODE,
                "duration_seconds": seconds,
            }

    return {
        "mode": DEFAULT_ALARM_PLAYBACK_MODE,
        "duration_seconds": None,
    }


def timed_alarm_has_expired(
    mode,
    started_at,
    current_time,
    duration_seconds,
):
    """
    Return True only when a timed alarm reached its duration.
    """

    if mode != TIMED_MODE:
        return False

    seconds = validate_timed_alarm_seconds(
        duration_seconds
    )

    if seconds is None:
        return True

    return (
        current_time - started_at
    ) >= seconds


def remove_alarm_playback_policy_language(text):
    """
    Remove playback-mode phrases before parsing the trigger time.

    This keeps the duration in:
        Set an alarm for 8 AM for 2 minutes
    from being interpreted as an alarm two minutes from now.
    """

    cleaned = str(
        text or ""
    )

    patterns = [
        r"\bfor\s+\d+\s*"
        r"(?:seconds?|secs?|minutes?|mins?)\b",
        r"\buntil\s+(?:i\s+)?"
        r"(?:stop|dismiss|snooze)(?:\s+it)?\b",
        r"\buntil\s+"
        r"(?:stopped|dismissed|snoozed)\b",
        r"\band\s+keep\s+ringing\b",
        r"\bkeep\s+ringing\b",
        r"\b(?:timed|self[- ]stopping)"
        r"(?=\s+alarm\b)",
    ]

    for pattern in patterns:
        cleaned = re.sub(
            pattern,
            " ",
            cleaned,
            flags=re.IGNORECASE,
        )

    return re.sub(
        r"\s+",
        " ",
        cleaned,
    ).strip()

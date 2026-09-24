import pytest

from assistant_tools.alarm_playback_policy import (
    DEFAULT_TIMED_ALARM_SECONDS,
    TIMED_MODE,
    UNTIL_DISMISSED_MODE,
    normalize_saved_playback_policy,
    parse_alarm_playback_policy,
    remove_alarm_playback_policy_language,
    timed_alarm_has_expired,
    validate_timed_alarm_seconds,
)


@pytest.mark.parametrize(
    "query",
    [
        "Set an alarm for 8 AM",
        "Set an alarm in 20 minutes",
        "Wake me up at 7:30 AM",
    ],
)
def test_alarm_defaults_to_until_dismissed(
    query,
):
    result = parse_alarm_playback_policy(
        query
    )

    assert result == {
        "success": True,
        "mode": UNTIL_DISMISSED_MODE,
        "duration_seconds": None,
        "explicit": False,
        "error": None,
    }


@pytest.mark.parametrize(
    "query",
    [
        "Set an alarm for 8 AM until dismissed",
        "Set an alarm for 8 AM until stopped",
        "Set an alarm for 8 AM until I stop it",
        "Set an alarm for 8 AM until snoozed",
        "Set an alarm for 8 AM and keep ringing",
    ],
)
def test_explicit_until_dismissed_language(
    query,
):
    result = parse_alarm_playback_policy(
        query
    )

    assert result["success"] is True
    assert result["mode"] == (
        UNTIL_DISMISSED_MODE
    )
    assert result["duration_seconds"] is None
    assert result["explicit"] is True


@pytest.mark.parametrize(
    ("query", "seconds"),
    [
        (
            "Set an alarm for 8 AM for 30 seconds",
            30,
        ),
        (
            "Set an alarm for 8 AM for 45 secs",
            45,
        ),
        (
            "Set an alarm for 8 AM for 2 minutes",
            120,
        ),
        (
            "Set an alarm for 8 AM for 10 mins",
            600,
        ),
    ],
)
def test_timed_duration_language(
    query,
    seconds,
):
    result = parse_alarm_playback_policy(
        query
    )

    assert result["success"] is True
    assert result["mode"] == TIMED_MODE
    assert result["duration_seconds"] == seconds
    assert result["explicit"] is True


@pytest.mark.parametrize(
    "query",
    [
        "Set a timed alarm for 8 AM",
        "Set a self-stopping alarm for 8 AM",
        "Set a self stopping alarm for 8 AM",
    ],
)
def test_timed_alarm_uses_default_duration(
    query,
):
    result = parse_alarm_playback_policy(
        query
    )

    assert result["success"] is True
    assert result["mode"] == TIMED_MODE
    assert (
        result["duration_seconds"]
        == DEFAULT_TIMED_ALARM_SECONDS
    )


@pytest.mark.parametrize(
    ("query", "seconds"),
    [
        (
            "Set an alarm for 8 AM for 4 seconds",
            4,
        ),
        (
            "Set an alarm for 8 AM for 31 minutes",
            1860,
        ),
    ],
)
def test_out_of_range_duration_is_rejected(
    query,
    seconds,
):
    result = parse_alarm_playback_policy(
        query
    )

    assert result["success"] is False
    assert result["mode"] == TIMED_MODE
    assert result["duration_seconds"] == seconds
    assert "5 seconds" in result["error"]
    assert "30 minutes" in result["error"]


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (5, 5),
        ("30", 30),
        (1800, 1800),
        (4, None),
        (1801, None),
        ("invalid", None),
        (None, None),
    ],
)
def test_validate_timed_duration(
    value,
    expected,
):
    assert validate_timed_alarm_seconds(
        value
    ) == expected


def test_normalize_saved_timed_policy():
    assert normalize_saved_playback_policy(
        TIMED_MODE,
        45,
    ) == {
        "mode": TIMED_MODE,
        "duration_seconds": 45,
    }


def test_normalize_saved_persistent_policy():
    assert normalize_saved_playback_policy(
        UNTIL_DISMISSED_MODE,
        45,
    ) == {
        "mode": UNTIL_DISMISSED_MODE,
        "duration_seconds": None,
    }


@pytest.mark.parametrize(
    ("mode", "duration"),
    [
        ("unknown", None),
        (TIMED_MODE, 2),
        (TIMED_MODE, None),
    ],
)
def test_invalid_saved_policy_falls_back_safely(
    mode,
    duration,
):
    assert normalize_saved_playback_policy(
        mode,
        duration,
    ) == {
        "mode": UNTIL_DISMISSED_MODE,
        "duration_seconds": None,
    }


@pytest.mark.parametrize(
    ("current_time", "expired"),
    [
        (100.0, False),
        (129.9, False),
        (130.0, True),
        (145.0, True),
    ],
)
def test_timed_alarm_expiration(
    current_time,
    expired,
):
    assert timed_alarm_has_expired(
        TIMED_MODE,
        started_at=100.0,
        current_time=current_time,
        duration_seconds=30,
    ) is expired


def test_until_dismissed_never_expires_from_time():
    assert timed_alarm_has_expired(
        UNTIL_DISMISSED_MODE,
        started_at=100.0,
        current_time=100000.0,
        duration_seconds=None,
    ) is False


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        (
            "Set an alarm for 8 AM for 30 seconds",
            "Set an alarm for 8 AM",
        ),
        (
            "Set an alarm for 8 AM until dismissed",
            "Set an alarm for 8 AM",
        ),
        (
            "Set an alarm for 8 AM until I stop it",
            "Set an alarm for 8 AM",
        ),
        (
            "Set a timed alarm for 8 AM",
            "Set a alarm for 8 AM",
        ),
        (
            "Set an alarm in 20 minutes",
            "Set an alarm in 20 minutes",
        ),
    ],
)
def test_remove_playback_language_before_time_parsing(
    query,
    expected,
):
    assert remove_alarm_playback_policy_language(
        query
    ) == expected

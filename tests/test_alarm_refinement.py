from pathlib import Path

import pytest

from assistant_tools import alarm_tones
from assistant_tools.alarm_playback_policy import (
    DEFAULT_TIMED_ALARM_SECONDS,
    TIMED_MODE,
    UNTIL_DISMISSED_MODE,
    parse_alarm_playback_policy,
)
from assistant_tools.alarm_tool import (
    _detect_action,
    _parse_snooze_minutes,
    _parse_spoken_number,
)
from core.saturn_personality import SATURN


@pytest.mark.parametrize(
    "query",
    [
        "Remind me at 3 PM to call the vet",
        "Set a reminder for 4 PM",
        "Create a short alarm for 5 PM",
    ],
)
def test_reminders_use_fixed_ten_second_playback(
    query,
):
    result = parse_alarm_playback_policy(
        query
    )

    assert DEFAULT_TIMED_ALARM_SECONDS == 10
    assert result["success"] is True
    assert result["mode"] == TIMED_MODE
    assert result["duration_seconds"] == 10


@pytest.mark.parametrize(
    "query",
    [
        "Set an alarm for 7 AM",
        "Wake me at 6:30 AM",
        "Wake me up in 20 minutes",
    ],
)
def test_normal_alarms_remain_continuous(
    query,
):
    result = parse_alarm_playback_policy(
        query
    )

    assert result["success"] is True
    assert result["mode"] == UNTIL_DISMISSED_MODE
    assert result["duration_seconds"] is None


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        ("Snooze", 10),
        ("Snooze alarm", 10),
        ("Snooze for 5 minutes", 5),
        ("Snooze for five minutes", 5),
        ("Snooze alarm for twenty minutes", 20),
        ("Snooze for forty-five minutes", 45),
        ("Snooze for 1 hour", 60),
        ("Snooze for one hour", 60),
        ("Snooze for two hours", 120),
        ("Snooze for 120 minutes", 120),
    ],
)
def test_variable_snooze_duration(
    query,
    expected,
):
    assert _parse_snooze_minutes(
        query
    ) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("one", 1),
        ("ten", 10),
        ("twenty five", 25),
        ("forty-five", 45),
        ("one hundred", 100),
        ("one hundred ten", 110),
        ("one hundred twenty", 120),
        ("121", 121),
        ("nonsense", None),
    ],
)
def test_spoken_number_parser(
    text,
    expected,
):
    assert _parse_spoken_number(
        text
    ) == expected


@pytest.mark.parametrize(
    "query",
    [
        "Remind me at 3 PM",
        "Remind me in 20 minutes",
    ],
)
def test_reminder_language_is_a_set_action(
    query,
):
    assert _detect_action(query) == "set"


@pytest.mark.parametrize(
    "query",
    [
        "Remind me at 3 PM to call the vet",
        "Set a reminder for 4 PM",
        "Snooze for twenty minutes",
    ],
)
def test_reminder_and_spoken_snooze_route_to_alarms(
    query,
):
    saturn = SATURN(
        start_alarm_monitor=False
    )

    assert saturn._detect_domain(query) == "alarms"


def test_saturn_alarm_one_is_the_installed_default(
    tmp_path,
    monkeypatch,
):
    tone_directory = (
        tmp_path
        / "alarm_tones"
    )
    tone_directory.mkdir()

    tone_path = (
        tone_directory
        / "Saturn Alarm 1.wav"
    )
    tone_path.write_bytes(
        b"RIFF-test"
    )

    monkeypatch.setenv(
        "SATURN_ALARM_TONES_DIR",
        str(tone_directory),
    )

    result = (
        alarm_tones.resolve_default_alarm_tone()
    )

    assert result is not None
    assert result["name"] == "Saturn Alarm 1"
    assert result["filename"] == (
        "Saturn Alarm 1.wav"
    )


def test_additional_tones_remain_discoverable(
    tmp_path,
    monkeypatch,
):
    tone_directory = (
        tmp_path
        / "alarm_tones"
    )
    tone_directory.mkdir()

    for filename in [
        "Saturn Alarm 1.wav",
        "Zen Gong.wav",
        "Morning_Bell.wav",
    ]:
        (
            tone_directory
            / filename
        ).write_bytes(
            b"RIFF-test"
        )

    monkeypatch.setenv(
        "SATURN_ALARM_TONES_DIR",
        str(tone_directory),
    )

    assert [
        tone["name"]
        for tone in alarm_tones.list_alarm_tones()
    ] == [
        "Morning Bell",
        "Saturn Alarm 1",
        "Zen Gong",
    ]

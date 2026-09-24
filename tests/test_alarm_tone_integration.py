from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from assistant_tools import alarm_tool


@pytest.fixture
def isolated_alarm_tone_runtime(
    tmp_path,
    monkeypatch,
):
    alarm_file = (
        tmp_path
        / "saturn_alarms.json"
    )

    tone_directory = (
        tmp_path
        / "alarm_tones"
    )

    tone_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    monkeypatch.setattr(
        alarm_tool,
        "ALARMS_FILE",
        str(alarm_file),
    )

    monkeypatch.setenv(
        "SATURN_ALARM_TONES_DIR",
        str(tone_directory),
    )

    fixed_now = datetime(
        2026,
        9,
        24,
        8,
        0,
        tzinfo=ZoneInfo(
            alarm_tool.DEFAULT_TIMEZONE
        ),
    )

    monkeypatch.setattr(
        alarm_tool,
        "_now",
        lambda: fixed_now,
    )

    return {
        "alarm_file": alarm_file,
        "tone_directory": tone_directory,
    }


def write_tone(
    tone_directory,
    filename,
):
    path = (
        tone_directory
        / filename
    )

    path.write_bytes(
        b"RIFF"
        + (b"\x00" * 32)
        + b"WAVE"
    )

    return path


def test_alarm_can_select_custom_tone_by_voice(
    isolated_alarm_tone_runtime,
):
    write_tone(
        isolated_alarm_tone_runtime[
            "tone_directory"
        ],
        "Zen_Gong.wav",
    )

    result = alarm_tool.handle_alarm_query(
        "Set an alarm in 20 minutes "
        "with the Zen Gong tone"
    )

    assert result["success"] is True
    assert result["action"] == "set"
    assert (
        result["alarm"]["tone"]
        == "Zen_Gong.wav"
    )
    assert (
        "using the Zen Gong tone"
        in result["response"]
    )


def test_alarm_without_tone_uses_default(
    isolated_alarm_tone_runtime,
):
    result = alarm_tool.handle_alarm_query(
        "Set an alarm in 20 minutes"
    )

    assert result["success"] is True
    assert result["alarm"]["tone"] is None


def test_unknown_requested_tone_is_rejected(
    isolated_alarm_tone_runtime,
):
    result = alarm_tool.handle_alarm_query(
        "Set an alarm in 20 minutes "
        "with the Ocean tone"
    )

    assert result["success"] is False
    assert result["error"] == (
        "Alarm tone not found."
    )
    assert (
        "Ocean"
        in result["response"]
    )


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        (
            "Set an alarm in 5 minutes "
            "with the Zen Gong tone",
            "Zen Gong",
        ),
        (
            "Set an alarm for 8 AM "
            "using Morning Bell alarm tone",
            "Morning Bell",
        ),
        (
            "Set an alarm in 10 minutes",
            None,
        ),
    ],
)
def test_requested_tone_parser(
    query,
    expected,
):
    result = alarm_tool._parse_requested_tone(
        query
    )

    assert result["name"] == expected


def test_linux_custom_tone_uses_aplay(
    isolated_alarm_tone_runtime,
):
    path = write_tone(
        isolated_alarm_tone_runtime[
            "tone_directory"
        ],
        "Morning Bell.wav",
    )

    resolved = (
        alarm_tool._resolve_playback_tone_path(
            "Morning Bell.wav"
        )
    )

    assert resolved == str(
        path.resolve()
    )

    assert alarm_tool._linux_alarm_command(
        resolved
    ) == [
        "aplay",
        "--quiet",
        str(path.resolve()),
    ]


def test_linux_default_alarm_uses_speaker_test():
    assert alarm_tool._linux_alarm_command() == [
        "speaker-test",
        "-t",
        "sine",
        "-f",
        "880",
        "-l",
        "1",
    ]


def test_snoozed_alarm_inherits_tone(
    isolated_alarm_tone_runtime,
    monkeypatch,
):
    write_tone(
        isolated_alarm_tone_runtime[
            "tone_directory"
        ],
        "Zen_Gong.wav",
    )

    created = alarm_tool.handle_alarm_query(
        "Set an alarm in 20 minutes "
        "with the Zen Gong tone"
    )

    source_alarm = created["alarm"]

    monkeypatch.setattr(
        alarm_tool,
        "get_ringing_alarm_ids",
        lambda: [
            source_alarm["id"],
        ],
    )

    monkeypatch.setattr(
        alarm_tool,
        "stop_alarm_playback",
        lambda: True,
    )

    result = alarm_tool.handle_alarm_query(
        "Snooze for 5 minutes"
    )

    assert result["success"] is True
    assert (
        result["alarm"]["tone"]
        == "Zen_Gong.wav"
    )


def test_missing_saved_tone_falls_back_to_default(
    isolated_alarm_tone_runtime,
):
    assert (
        alarm_tool._resolve_playback_tone_path(
            "Removed Tone.wav"
        )
        is None
    )


def test_new_alarm_defaults_to_until_dismissed(
    isolated_alarm_tone_runtime,
):
    result = alarm_tool.handle_alarm_query(
        "Set an alarm for 8:30 AM"
    )

    assert result["success"] is True
    assert (
        result["alarm"]["playback_mode"]
        == "until_dismissed"
    )
    assert (
        result["alarm"][
            "playback_duration_seconds"
        ]
        is None
    )
    assert (
        "until stopped or snoozed"
        in result["response"]
    )


def test_timed_alarm_stores_duration(
    isolated_alarm_tone_runtime,
):
    result = alarm_tool.handle_alarm_query(
        "Set an alarm for 8:30 AM for 45 seconds"
    )

    assert result["success"] is True
    assert (
        result["alarm"]["playback_mode"]
        == "timed"
    )
    assert (
        result["alarm"][
            "playback_duration_seconds"
        ]
        == 45
    )
    assert (
        "ring for 45 seconds"
        in result["response"]
    )


def test_timed_duration_does_not_replace_trigger_time(
    isolated_alarm_tone_runtime,
):
    result = alarm_tool.handle_alarm_query(
        "Set an alarm for 9:15 AM for 2 minutes"
    )

    assert result["success"] is True

    trigger = datetime.fromisoformat(
        result["alarm"]["trigger_at"]
    )

    assert trigger.hour == 9
    assert trigger.minute == 15
    assert (
        result["alarm"][
            "playback_duration_seconds"
        ]
        == 120
    )


def test_custom_tone_and_timed_mode_work_together(
    isolated_alarm_tone_runtime,
):
    write_tone(
        isolated_alarm_tone_runtime[
            "tone_directory"
        ],
        "Zen_Gong.wav",
    )

    result = alarm_tool.handle_alarm_query(
        "Set an alarm for 9:15 AM "
        "with the Zen Gong tone "
        "for 30 seconds"
    )

    assert result["success"] is True
    assert result["alarm"]["tone"] == (
        "Zen_Gong.wav"
    )
    assert (
        result["alarm"]["playback_mode"]
        == "timed"
    )
    assert (
        result["alarm"][
            "playback_duration_seconds"
        ]
        == 30
    )


def test_invalid_timed_duration_is_rejected(
    isolated_alarm_tone_runtime,
):
    result = alarm_tool.handle_alarm_query(
        "Set an alarm for 9 AM for 2 seconds"
    )

    assert result["success"] is False
    assert result["error"] == (
        "Invalid alarm playback duration."
    )


def test_snooze_inherits_playback_policy(
    isolated_alarm_tone_runtime,
    monkeypatch,
):
    created = alarm_tool.handle_alarm_query(
        "Set an alarm for 9 AM for 45 seconds"
    )

    source_alarm = created["alarm"]

    monkeypatch.setattr(
        alarm_tool,
        "get_ringing_alarm_ids",
        lambda: [
            source_alarm["id"],
        ],
    )

    monkeypatch.setattr(
        alarm_tool,
        "stop_alarm_playback",
        lambda: True,
    )

    result = alarm_tool.handle_alarm_query(
        "Snooze for 5 minutes"
    )

    assert result["success"] is True
    assert (
        result["alarm"]["playback_mode"]
        == "timed"
    )
    assert (
        result["alarm"][
            "playback_duration_seconds"
        ]
        == 45
    )

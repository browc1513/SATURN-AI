import json
from datetime import timedelta

import pytest

from assistant_tools import (
    alarm_playback,
    alarm_tool,
)
from core.saturn_personality import SATURN


@pytest.fixture
def isolated_alarm_files(
    tmp_path,
    monkeypatch,
):
    alarms_path = (
        tmp_path
        / "saturn_alarms.json"
    )
    playback_path = (
        tmp_path
        / "saturn_alarm_playback.json"
    )

    monkeypatch.setattr(
        alarm_tool,
        "ALARMS_FILE",
        str(alarms_path),
    )
    monkeypatch.setattr(
        alarm_playback,
        "ALARM_PLAYBACK_STATE_FILE",
        str(playback_path),
    )

    return alarms_path, playback_path


def create_ringing_alarm():
    alarm_id = "ringing-alarm-id"

    alarm = {
        "id": alarm_id,
        "created_at": alarm_tool._now().isoformat(),
        "trigger_at": (
            alarm_tool._now()
            - timedelta(minutes=1)
        ).isoformat(),
        "timezone": alarm_tool.DEFAULT_TIMEZONE,
        "status": "fired",
        "label": "Alarm",
    }

    alarm_tool._save_alarms(
        [alarm]
    )

    generation = (
        alarm_playback.begin_alarm_playback(
            alarm_id=alarm_id,
        )
    )

    return alarm, generation


@pytest.mark.parametrize(
    ("query", "minutes"),
    [
        ("Snooze", 10),
        ("Snooze the alarm", 10),
        ("Snooze for 5 minutes", 5),
        ("Snooze the alarm for 20 minutes", 20),
        ("Snooze for 1 hour", 60),
    ],
)
def test_snooze_reschedules_ringing_alarm(
    isolated_alarm_files,
    query,
    minutes,
):
    source_alarm, generation = (
        create_ringing_alarm()
    )

    before = alarm_tool._now()

    result = alarm_tool.handle_alarm_query(
        query
    )

    alarms = alarm_tool._load_alarms()
    active = [
        alarm
        for alarm in alarms
        if alarm.get("status") == "active"
    ]

    assert result["success"] is True, result
    assert result["action"] == "snooze"
    assert result["minutes"] == minutes
    assert result["stopped"] is True

    assert len(active) == 1
    assert (
        active[0]["snoozed_from_alarm_id"]
        == source_alarm["id"]
    )

    trigger_at = alarm_tool._parse_iso(
        active[0]["trigger_at"]
    )

    expected = before + timedelta(
        minutes=minutes
    )

    assert abs(
        (
            trigger_at - expected
        ).total_seconds()
    ) < 5

    assert (
        alarm_playback.should_stop_alarm_playback(
            generation
        )
        is True
    )

    alarm_playback.finish_alarm_playback(
        alarm_id=source_alarm["id"],
    )


def test_repeated_snooze_does_not_duplicate_alarm(
    isolated_alarm_files,
):
    source_alarm, _ = create_ringing_alarm()

    first = alarm_tool.handle_alarm_query(
        "Snooze"
    )
    second = alarm_tool.handle_alarm_query(
        "Snooze"
    )

    alarms = alarm_tool._load_alarms()
    active = [
        alarm
        for alarm in alarms
        if alarm.get("status") == "active"
    ]

    assert first["success"] is True
    assert second["success"] is False
    assert len(active) == 1

    alarm_playback.finish_alarm_playback(
        alarm_id=source_alarm["id"],
    )


def test_snooze_when_nothing_is_ringing_is_safe(
    isolated_alarm_files,
):
    result = alarm_tool.handle_alarm_query(
        "Snooze the alarm"
    )

    assert result["success"] is False
    assert result["action"] == "snooze"
    assert result["response"] == (
        "No alarm is currently ringing."
    )


def test_bare_snooze_routes_only_while_alarm_rings(
    isolated_alarm_files,
):
    saturn = SATURN(
        start_alarm_monitor=False
    )

    assert saturn._detect_domain(
        "snooze"
    ) != "alarms"

    source_alarm, _ = create_ringing_alarm()

    try:
        assert saturn._detect_domain(
            "snooze"
        ) == "alarms"

        result = saturn.handle_query(
            "snooze",
            session_id="voice",
        )

        assert result["success"] is True
        assert result["domain"] == "alarms"
        assert result["data"]["action"] == "snooze"
    finally:
        alarm_playback.finish_alarm_playback(
            alarm_id=source_alarm["id"],
        )


def test_playback_state_records_alarm_id(
    isolated_alarm_files,
):
    _, playback_path = isolated_alarm_files

    generation = (
        alarm_playback.begin_alarm_playback(
            alarm_id="alarm-123",
        )
    )

    state = json.loads(
        playback_path.read_text(
            encoding="utf-8"
        )
    )

    assert generation == 0
    assert state["active_count"] == 1
    assert state["active_alarm_ids"] == [
        "alarm-123"
    ]

    alarm_playback.finish_alarm_playback(
        alarm_id="alarm-123",
    )

    state = json.loads(
        playback_path.read_text(
            encoding="utf-8"
        )
    )

    assert state["active_count"] == 0
    assert state["active_alarm_ids"] == []


def test_environment_can_disable_alarm_monitor(
    monkeypatch,
):
    monkeypatch.setenv(
        "SATURN_DISABLE_ALARM_MONITOR",
        "true",
    )

    saturn = SATURN(
        start_alarm_monitor=True
    )

    assert saturn._alarm_monitor_running is False
    assert saturn._alarm_monitor_thread is None

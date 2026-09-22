import json

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


@pytest.mark.parametrize(
    "query",
    [
        "Stop alarm",
        "Stop the alarm",
        "Stop my alarm",
        "Stop the ringing alarm",
        "Dismiss alarm",
        "Silence the alarm",
    ],
)
def test_explicit_alarm_stop_commands_route_to_alarms(
    isolated_alarm_files,
    query,
):
    saturn = SATURN(
        start_alarm_monitor=False
    )

    assert saturn._detect_domain(query) == "alarms"


def test_bare_stop_routes_to_ringing_alarm(
    isolated_alarm_files,
):
    saturn = SATURN(
        start_alarm_monitor=False
    )

    generation = (
        alarm_playback.begin_alarm_playback()
    )

    try:
        assert saturn._detect_domain(
            "stop"
        ) == "alarms"
    finally:
        alarm_playback.finish_alarm_playback()

    assert generation == 0


def test_bare_stop_does_not_claim_unrelated_context(
    isolated_alarm_files,
):
    saturn = SATURN(
        start_alarm_monitor=False
    )

    assert saturn._detect_domain(
        "stop"
    ) == "unknown"


def test_stop_request_interrupts_current_generation(
    isolated_alarm_files,
):
    generation = (
        alarm_playback.begin_alarm_playback()
    )

    assert (
        alarm_playback.is_alarm_ringing()
        is True
    )
    assert (
        alarm_playback.should_stop_alarm_playback(
            generation
        )
        is False
    )

    assert (
        alarm_playback.stop_alarm_playback()
        is True
    )
    assert (
        alarm_playback.should_stop_alarm_playback(
            generation
        )
        is True
    )

    alarm_playback.finish_alarm_playback()

    assert (
        alarm_playback.is_alarm_ringing()
        is False
    )


def test_stop_when_nothing_is_ringing_is_safe(
    isolated_alarm_files,
):
    result = alarm_tool.handle_alarm_query(
        "stop the alarm"
    )

    assert result["success"] is True
    assert result["action"] == "stop"
    assert result["stopped"] is False
    assert result["response"] == (
        "No alarm is currently ringing."
    )


def test_stopping_sound_does_not_cancel_scheduled_alarm(
    isolated_alarm_files,
):
    set_result = alarm_tool.handle_alarm_query(
        "set an alarm for 7 AM"
    )

    generation = (
        alarm_playback.begin_alarm_playback()
    )

    stop_result = alarm_tool.handle_alarm_query(
        "stop the alarm"
    )

    alarms = alarm_tool._load_alarms()

    alarm_playback.finish_alarm_playback()

    assert set_result["success"] is True
    assert stop_result["success"] is True
    assert stop_result["stopped"] is True
    assert (
        alarm_playback.should_stop_alarm_playback(
            generation
        )
        is True
    )
    assert len(alarms) == 1
    assert alarms[0]["status"] == "active"


def test_saturn_can_stop_alarm_through_normal_query(
    isolated_alarm_files,
):
    saturn = SATURN(
        start_alarm_monitor=False
    )

    alarm_playback.begin_alarm_playback()

    try:
        result = saturn.handle_query(
            "stop"
        )
    finally:
        alarm_playback.finish_alarm_playback()

    assert result["success"] is True
    assert result["domain"] == "alarms"
    assert result["response"] == "Alarm stopped."


def test_playback_state_is_valid_json(
    isolated_alarm_files,
):
    _, playback_path = isolated_alarm_files

    alarm_playback.begin_alarm_playback()
    alarm_playback.stop_alarm_playback()
    alarm_playback.finish_alarm_playback()

    state = json.loads(
        playback_path.read_text(
            encoding="utf-8"
        )
    )

    assert state["active_count"] == 0
    assert state["generation"] == 1

import threading
import time

import pytest

from assistant_tools import alarm_playback
from assistant_tools import alarm_tool


@pytest.fixture
def isolated_playback_state(
    tmp_path,
    monkeypatch,
):
    state_file = (
        tmp_path
        / "saturn_alarm_playback.json"
    )

    monkeypatch.setattr(
        alarm_playback,
        "ALARM_PLAYBACK_STATE_FILE",
        str(state_file),
    )

    monkeypatch.setattr(
        alarm_tool,
        "begin_alarm_playback",
        alarm_playback.begin_alarm_playback,
    )
    monkeypatch.setattr(
        alarm_tool,
        "finish_alarm_playback",
        alarm_playback.finish_alarm_playback,
    )
    monkeypatch.setattr(
        alarm_tool,
        "refresh_alarm_playback",
        alarm_playback.refresh_alarm_playback,
    )
    monkeypatch.setattr(
        alarm_tool,
        "should_stop_alarm_playback",
        alarm_playback.should_stop_alarm_playback,
    )

    return state_file


def test_playback_heartbeat_preserves_active_alarm(
    isolated_playback_state,
):
    generation = (
        alarm_playback.begin_alarm_playback(
            alarm_id="alarm-1"
        )
    )

    assert alarm_playback.refresh_alarm_playback(
        generation,
        alarm_id="alarm-1",
    ) is True

    assert (
        alarm_playback.get_ringing_alarm_ids()
        == ["alarm-1"]
    )

    alarm_playback.finish_alarm_playback(
        alarm_id="alarm-1"
    )


def test_heartbeat_rejects_stopped_generation(
    isolated_playback_state,
):
    generation = (
        alarm_playback.begin_alarm_playback(
            alarm_id="alarm-1"
        )
    )

    assert (
        alarm_playback.stop_alarm_playback()
        is True
    )

    assert alarm_playback.refresh_alarm_playback(
        generation,
        alarm_id="alarm-1",
    ) is False

    alarm_playback.finish_alarm_playback(
        alarm_id="alarm-1"
    )


def test_until_dismissed_fallback_runs_until_stop(
    isolated_playback_state,
    monkeypatch,
):
    monkeypatch.setattr(
        alarm_tool.sys,
        "platform",
        "unsupported-test-platform",
    )

    worker = threading.Thread(
        target=alarm_tool.play_alarm_sound,
        kwargs={
            "alarm_id": "persistent-alarm",
            "playback_mode": "until_dismissed",
        },
        daemon=True,
    )

    worker.start()

    deadline = (
        time.monotonic() + 2
    )

    while (
        "persistent-alarm"
        not in alarm_playback.get_ringing_alarm_ids()
        and time.monotonic() < deadline
    ):
        time.sleep(
            0.01
        )

    assert worker.is_alive()

    assert (
        alarm_playback.stop_alarm_playback()
        is True
    )

    worker.join(
        timeout=2
    )

    assert not worker.is_alive()


def test_timed_fallback_stops_automatically(
    isolated_playback_state,
    monkeypatch,
):
    monkeypatch.setattr(
        alarm_tool.sys,
        "platform",
        "unsupported-test-platform",
    )

    # The production minimum is five seconds. Replace only the policy
    # expiration helper so this test completes quickly and silently.
    started = time.monotonic()

    monkeypatch.setattr(
        alarm_tool,
        "timed_alarm_has_expired",
        lambda mode, started_at, current_time,
        duration_seconds: (
            time.monotonic() - started
        ) >= 0.15,
    )

    worker = threading.Thread(
        target=alarm_tool.play_alarm_sound,
        kwargs={
            "alarm_id": "timed-alarm",
            "playback_mode": "timed",
            "playback_duration_seconds": 5,
        },
        daemon=True,
    )

    worker.start()
    worker.join(
        timeout=2
    )

    assert not worker.is_alive()


def test_legacy_fallback_still_uses_repetitions(
    isolated_playback_state,
    monkeypatch,
):
    monkeypatch.setattr(
        alarm_tool.sys,
        "platform",
        "unsupported-test-platform",
    )

    sleep_calls = []

    monkeypatch.setattr(
        alarm_tool.time,
        "sleep",
        lambda duration: sleep_calls.append(
            duration
        ),
    )

    current = [0.0]

    def fake_monotonic():
        current[0] += 0.1
        return current[0]

    monkeypatch.setattr(
        alarm_tool.time,
        "monotonic",
        fake_monotonic,
    )

    result = alarm_tool.play_alarm_sound(
        repetitions=2,
        alarm_id="legacy-alarm",
    )

    assert result is True
    assert sleep_calls

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


class FakeLinuxSoundProcess:
    def __init__(
        self,
        *,
        running=True,
        time_out_once=False,
    ):
        self.pid = 12345
        self.running = running
        self.time_out_once = time_out_once
        self.wait_calls = 0
        self.terminate_calls = 0
        self.kill_calls = 0

    def poll(self):
        if self.running:
            return None

        return 0

    def wait(self, timeout):
        self.wait_calls += 1

        if (
            self.time_out_once
            and self.wait_calls == 1
        ):
            raise alarm_tool.subprocess.TimeoutExpired(
                cmd="speaker-test",
                timeout=timeout,
            )

        self.running = False
        return 0

    def terminate(self):
        self.terminate_calls += 1
        self.running = False

    def kill(self):
        self.kill_calls += 1
        self.running = False


def test_linux_alarm_starts_in_new_process_group(
    isolated_alarm_files,
    monkeypatch,
):
    process = FakeLinuxSoundProcess(
        running=False
    )
    popen_calls = []

    def fake_popen(
        command,
        **kwargs,
    ):
        popen_calls.append(
            (
                command,
                kwargs,
            )
        )

        return process

    monkeypatch.setattr(
        alarm_tool.sys,
        "platform",
        "linux",
    )
    monkeypatch.setattr(
        alarm_tool.subprocess,
        "Popen",
        fake_popen,
    )

    result = alarm_tool.play_alarm_sound(
        repetitions=1
    )

    assert result is True
    assert len(popen_calls) == 1

    command, kwargs = popen_calls[0]

    assert command[0] == "speaker-test"
    assert kwargs["start_new_session"] is True


def test_linux_alarm_stop_terminates_process_group(
    monkeypatch,
):
    process = FakeLinuxSoundProcess()
    sent_signals = []

    monkeypatch.setattr(
        alarm_tool.os,
        "getpgid",
        lambda process_id: 54321,
        raising=False,
    )
    monkeypatch.setattr(
        alarm_tool.os,
        "killpg",
        lambda process_group, process_signal: (
            sent_signals.append(
                (
                    process_group,
                    process_signal,
                )
            )
        ),
        raising=False,
    )

    alarm_tool._stop_linux_sound_process(
        process
    )

    assert sent_signals == [
        (
            54321,
            alarm_tool.signal.SIGTERM,
        )
    ]
    assert process.terminate_calls == 0
    assert process.kill_calls == 0


def test_linux_alarm_force_kills_process_group(
    monkeypatch,
):
    process = FakeLinuxSoundProcess(
        time_out_once=True
    )
    sent_signals = []

    # Windows does not define SIGKILL. Supply its Linux value so
    # this Linux-specific behavior can still be tested on Windows.
    monkeypatch.setattr(
        alarm_tool.signal,
        "SIGKILL",
        9,
        raising=False,
    )
    monkeypatch.setattr(
        alarm_tool.os,
        "getpgid",
        lambda process_id: 54321,
        raising=False,
    )
    monkeypatch.setattr(
        alarm_tool.os,
        "killpg",
        lambda process_group, process_signal: (
            sent_signals.append(
                (
                    process_group,
                    process_signal,
                )
            )
        ),
        raising=False,
    )

    alarm_tool._stop_linux_sound_process(
        process
    )

    assert sent_signals == [
        (
            54321,
            alarm_tool.signal.SIGTERM,
        ),
        (
            54321,
            alarm_tool.signal.SIGKILL,
        ),
    ]
    assert process.terminate_calls == 0
    assert process.kill_calls == 0

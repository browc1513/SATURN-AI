from pathlib import Path

import pytest

from assistant_tools import alarm_playback
from voice.alarm_control import (
    is_wake_free_alarm_command,
)


@pytest.mark.parametrize(
    "command",
    [
        "Stop",
        "Stop alarm",
        "Stop the alarm",
        "Dismiss",
        "Silence the alarm",
        "Turn off the alarm",
        "Snooze",
        "Snooze alarm",
        "Snooze the alarm",
        "Snooze for five minutes",
        "Snooze the alarm for twenty minutes",
        "Snooze for 1 hour",
    ],
)
def test_wake_free_alarm_commands_are_restricted(
    command,
):
    assert is_wake_free_alarm_command(
        command
    ) is True


@pytest.mark.parametrize(
    "command",
    [
        "",
        "What time is it?",
        "Play music",
        "Tell me a joke",
        "Reboot Saturn",
        "Add milk to my grocery list",
        "The alarm is loud",
        "Please keep ringing",
    ],
)
def test_unrelated_speech_is_not_an_alarm_control(
    command,
):
    assert is_wake_free_alarm_command(
        command
    ) is False


def test_only_continuous_alarm_enables_wake_free_mode(
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

    timed_generation = (
        alarm_playback.begin_alarm_playback(
            alarm_id="timed-alarm",
            requires_dismissal=False,
        )
    )

    assert timed_generation == 0
    assert (
        alarm_playback
        .is_dismissal_required_alarm_ringing()
        is False
    )

    alarm_playback.finish_alarm_playback(
        alarm_id="timed-alarm",
        requires_dismissal=False,
    )

    continuous_generation = (
        alarm_playback.begin_alarm_playback(
            alarm_id="continuous-alarm",
            requires_dismissal=True,
        )
    )

    assert continuous_generation == 0
    assert (
        alarm_playback
        .is_dismissal_required_alarm_ringing()
        is True
    )

    alarm_playback.finish_alarm_playback(
        alarm_id="continuous-alarm",
        requires_dismissal=True,
    )

    assert (
        alarm_playback
        .is_dismissal_required_alarm_ringing()
        is False
    )


def test_voice_runtime_interrupts_wake_word_for_alarm():
    source = Path(
        "voice/voice_assistant.py"
    ).read_text(
        encoding="utf-8"
    )

    assert (
        "is_dismissal_required_alarm_ringing"
        in source
    )
    assert (
        "is_wake_free_alarm_command"
        in source
    )
    assert (
        "interrupt_check=("
        in source
    )
    assert (
        "Ignored non-alarm speech"
        in source
    )


def test_wake_word_supports_interrupt_callback():
    source = Path(
        "voice/wake_word.py"
    ).read_text(
        encoding="utf-8"
    )

    assert "interrupt_check=None" in source
    assert "and interrupt_check()" in source
    assert "return None" in source

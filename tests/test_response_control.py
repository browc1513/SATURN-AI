import threading

import pytest

from voice.response_control import (
    is_response_stop_command,
    speak_with_interrupt,
)


@pytest.mark.parametrize(
    "phrase",
    [
        "Stop",
        "STOP!",
        "Stop talking",
        "Stop speaking",
        "Cancel",
        "Quiet",
        "Be quiet",
        "Never mind",
        "Nevermind",
    ],
)
def test_active_reply_stop_phrases(phrase):
    assert is_response_stop_command(phrase)


@pytest.mark.parametrize(
    "phrase",
    [
        "",
        "What time is it?",
        "I might stop at the store",
        "Cancel my seven o'clock alarm",
        "Please be quiet tomorrow",
        "Never mind the weather; show my lists",
        "Snooze",
        "Add milk to my grocery list",
    ],
)
def test_unrelated_speech_cannot_stop_a_reply(phrase):
    assert not is_response_stop_command(phrase)


def test_stop_cancels_only_active_speech():
    calls = []

    def listen(**kwargs):
        calls.append("listened")
        return {"success": True, "text": "Stop!"}

    def speak(text, cancel_event):
        assert text == "A long reply"
        assert cancel_event.wait(timeout=2)
        calls.append("cancelled")

    assert speak_with_interrupt(
        "A long reply", listen=listen, speak=speak
    ) is True
    assert calls == ["listened", "cancelled"]


def test_unrelated_speech_does_not_cancel_reply():
    heard = threading.Event()

    def listen(**kwargs):
        heard.set()
        return {
            "success": True,
            "text": "Cancel my seven o'clock alarm",
        }

    def speak(text, cancel_event):
        assert heard.wait(timeout=2)
        assert not cancel_event.is_set()

    assert speak_with_interrupt(
        "A reply", listen=listen, speak=speak
    ) is False

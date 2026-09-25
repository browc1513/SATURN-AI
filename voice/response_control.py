"""Restricted wake-free commands while a spoken reply is active."""

import threading

from voice.alarm_control import normalize_alarm_control


_STOP_PHRASES = {
    "stop",
    "stop talking",
    "stop speaking",
    "cancel",
    "quiet",
    "be quiet",
    "never mind",
    "nevermind",
}


def is_response_stop_command(text):
    """Match a complete stop phrase, not a word inside a sentence."""

    return normalize_alarm_control(text) in _STOP_PHRASES


def speak_with_interrupt(text, listen=None, speak=None):
    """Speak one response while accepting only exact stop commands."""

    if listen is None:
        from voice.speech_to_text import listen_once
        listen = listen_once

    if speak is None:
        from voice.text_to_speech import speak_and_wait
        speak = speak_and_wait

    finished = threading.Event()
    cancelled = threading.Event()

    def monitor():
        while not finished.is_set():
            try:
                heard = listen(
                    timeout=0.8,
                    phrase_time_limit=2,
                    ambient_duration=0.1,
                    recognition_timeout=2,
                )
            except Exception:
                return

            if finished.is_set():
                return

            if (
                heard.get("success")
                and is_response_stop_command(heard.get("text", ""))
            ):
                cancelled.set()
                return

            if not heard.get("success"):
                finished.wait(0.1)

    listener = threading.Thread(
        target=monitor,
        daemon=True,
        name="SATURNResponseStop",
    )
    listener.start()
    try:
        speak(text, cancel_event=cancelled)
    finally:
        finished.set()
        listener.join(timeout=5)

    return cancelled.is_set()

"""
S.A.T.U.R.N. Text-to-Speech

Offline text-to-speech using pyttsx3.

Public interfaces:

    speak_async(text)
        Queue speech and return immediately.

    speak_and_wait(text)
        Queue speech and wait until that specific speech job finishes.

This lets the GUI remain non-blocking while the hands-free voice
assistant can synchronize microphone handoffs with TTS completion.
"""

import queue
import threading


try:
    import pyttsx3
except ImportError:
    pyttsx3 = None


_voice_enabled = True
_speech_queue = queue.Queue()
_worker_started = False
_worker_lock = threading.Lock()

# Temporary voice preferences.
# Later these can move into saturn_config.json.
_preferred_voice_name = "Zira"
_preferred_voice_index = None


def set_voice_enabled(enabled):
    """
    Enable or disable spoken responses.
    """

    global _voice_enabled

    _voice_enabled = bool(enabled)


def is_voice_enabled():
    """
    Return the current TTS enabled state.
    """

    return _voice_enabled


def _clean_for_speech(text):
    """
    Make chat-formatted output sound more natural when spoken.
    """

    text = str(text)

    replacements = {
        "S.A.T.U.R.N.": "Saturn",
        "°F": " degrees Fahrenheit",
        "°C": " degrees Celsius",
        "\n": ". ",
    }

    for old, new in replacements.items():
        text = text.replace(
            old,
            new,
        )

    text = " ".join(
        text.split()
    )

    return text.strip()


def _speech_worker():
    """
    Dedicated speech worker.

    Every queue item contains both the text to speak and an optional
    threading.Event used to signal that the speech job has finished.
    """

    if pyttsx3 is None:
        return

    try:
        engine = pyttsx3.init()

        voices = engine.getProperty(
            "voices"
        ) or []

        selected_voice = None

        if (
            _preferred_voice_index is not None
            and 0 <= _preferred_voice_index < len(voices)
        ):
            selected_voice = voices[
                _preferred_voice_index
            ]

        elif _preferred_voice_name:
            target = _preferred_voice_name.lower()

            for voice in voices:
                name = str(
                    getattr(
                        voice,
                        "name",
                        "",
                    )
                ).lower()

                if target in name:
                    selected_voice = voice
                    break

        if selected_voice is not None:
            engine.setProperty(
                "voice",
                selected_voice.id,
            )

        engine.setProperty(
            "rate",
            180,
        )

        engine.setProperty(
            "volume",
            1.0,
        )

        while True:
            job = _speech_queue.get()

            if job is None:
                _speech_queue.task_done()
                break

            text = job["text"]
            finished_event = job.get(
                "finished_event"
            )

            try:
                if not _voice_enabled:
                    continue

                spoken_text = _clean_for_speech(
                    text
                )

                if spoken_text:
                    engine.say(
                        spoken_text
                    )

                    engine.runAndWait()

            except Exception as error:
                print(
                    "S.A.T.U.R.N. TTS warning: "
                    f"{error}"
                )

            finally:
                if finished_event is not None:
                    finished_event.set()

                _speech_queue.task_done()

    except Exception as error:
        print(
            "S.A.T.U.R.N. TTS startup warning: "
            f"{error}"
        )


def _ensure_worker():
    """
    Start the speech worker once.
    """

    global _worker_started

    with _worker_lock:
        if _worker_started:
            return

        _worker_started = True

        threading.Thread(
            target=_speech_worker,
            daemon=True,
            name="SATURNTTS",
        ).start()


def get_available_voices():
    """
    Return installed system voices in a simple structured format.
    """

    if pyttsx3 is None:
        return []

    try:
        engine = pyttsx3.init()

        voices = engine.getProperty(
            "voices"
        ) or []

        results = []

        for index, voice in enumerate(voices):
            results.append(
                {
                    "index": index,
                    "id": getattr(
                        voice,
                        "id",
                        "",
                    ),
                    "name": getattr(
                        voice,
                        "name",
                        f"Voice {index}",
                    ),
                    "languages": getattr(
                        voice,
                        "languages",
                        [],
                    ),
                    "gender": getattr(
                        voice,
                        "gender",
                        None,
                    ),
                    "age": getattr(
                        voice,
                        "age",
                        None,
                    ),
                }
            )

        return results

    except Exception:
        return []


def set_preferred_voice(
    name_contains=None,
    voice_index=None,
):
    """
    Set the preferred voice for future speech worker startup.

    Restart SATURN after changing it so the speech engine is recreated
    with the new voice.
    """

    global _preferred_voice_name
    global _preferred_voice_index

    _preferred_voice_name = (
        str(name_contains).strip()
        if name_contains is not None
        else None
    )

    _preferred_voice_index = (
        int(voice_index)
        if voice_index is not None
        else None
    )


def get_voice_preference():
    return {
        "name_contains": _preferred_voice_name,
        "voice_index": _preferred_voice_index,
    }


def speak_async(text):
    """
    Queue text to be spoken without blocking the caller.
    """

    if not _voice_enabled:
        return

    if pyttsx3 is None:
        print(
            "S.A.T.U.R.N. TTS is unavailable. "
            "Install it with: "
            "python -m pip install pyttsx3"
        )
        return

    _ensure_worker()

    _speech_queue.put(
        {
            "text": str(text),
            "finished_event": None,
        }
    )


def speak_and_wait(text):
    """
    Speak text and block until that specific TTS job has finished.

    This is intended for microphone/TTS synchronization in the
    hands-free voice assistant.
    """

    if not _voice_enabled:
        return

    if pyttsx3 is None:
        print(
            "S.A.T.U.R.N. TTS is unavailable. "
            "Install it with: "
            "python -m pip install pyttsx3"
        )
        return

    _ensure_worker()

    finished_event = threading.Event()

    _speech_queue.put(
        {
            "text": str(text),
            "finished_event": finished_event,
        }
    )

    finished_event.wait()

"""
S.A.T.U.R.N. Text-to-Speech

Offline desktop text-to-speech using pyttsx3.

Windows backend:
    Microsoft SAPI5

The public interface is intentionally small so the backend can later
be replaced on Raspberry Pi without changing SATURN's GUI or tools.
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

# Temporary desktop voice preferences.
# Later these can move into saturn_config.json.
_preferred_voice_name = "Zira"
_preferred_voice_index = None


def set_voice_enabled(enabled):
    """
    Enable or disable spoken responses.
    """

    global _voice_enabled

    _voice_enabled = bool(
        enabled
    )


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

    # Collapse repeated spaces and punctuation created by formatting.
    text = " ".join(
        text.split()
    )

    return text.strip()


def _speech_worker():
    """
    Dedicated speech worker.

    Keeping pyttsx3 inside one background thread avoids blocking
    Tkinter and avoids multiple TTS engines speaking at once.
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

        # Conservative defaults for readable assistant speech.
        engine.setProperty(
            "rate",
            180,
        )

        engine.setProperty(
            "volume",
            1.0,
        )

        while True:
            text = _speech_queue.get()

            if text is None:
                break

            if not _voice_enabled:
                _speech_queue.task_done()
                continue

            try:
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

    On Windows these are the Microsoft SAPI voices currently installed
    for the active Python environment/user.
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

    This updates the module-level preference. Restart SATURN after
    changing it so the speech engine is recreated with the new voice.
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
    Queue text to be spoken without blocking the GUI.
    """

    if not _voice_enabled:
        return

    if pyttsx3 is None:
        print(
            "S.A.T.U.R.N. TTS is unavailable. "
            "Install it with: python -m pip install pyttsx3"
        )
        return

    _ensure_worker()

    _speech_queue.put(
        str(text)
    )

"""
S.A.T.U.R.N. Text-to-Speech

Primary Raspberry Pi backend:
    Piper neural TTS

Default SATURN voice:
    en_GB-alba-medium

Public interfaces:

    speak_async(text)
        Queue speech and return immediately.

    speak_and_wait(text)
        Queue speech and wait until playback has actually finished.

The queue-based architecture keeps SATURN's GUI non-blocking while
allowing the hands-free assistant to synchronize microphone handoffs
with actual speech completion.
"""

import queue
import subprocess
import tempfile
import threading
import wave
from pathlib import Path

from voice.speech_format import to_speech_text


try:
    from piper import PiperVoice
except ImportError:
    PiperVoice = None


VOICE_MODEL_PATH = (
    Path(__file__).resolve().parent
    / "models"
    / "piper"
    / "en_GB-alba-medium.onnx"
)

_voice_enabled = True

_speech_queue = queue.Queue()

_worker_started = False
_worker_lock = threading.Lock()


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
    """Make SATURN's formatted output sound natural when spoken."""

    return to_speech_text(text)


def _load_voice():
    """
    Load SATURN's Piper neural voice.
    """

    if PiperVoice is None:
        raise RuntimeError(
            "Piper TTS is not installed."
        )

    if not VOICE_MODEL_PATH.exists():
        raise FileNotFoundError(
            "SATURN Piper voice model was not found: "
            f"{VOICE_MODEL_PATH}"
        )

    print(
        "Loading S.A.T.U.R.N. neural voice..."
    )

    voice = PiperVoice.load(
        str(VOICE_MODEL_PATH)
    )

    print(
        "S.A.T.U.R.N. neural voice ready."
    )

    return voice


def _synthesize_and_play(
    voice,
    text,
):
    """
    Synthesize text with Piper and play it through the current
    default ALSA/PipeWire output device.

    Playback is synchronous so completion means the audio has
    actually finished playing.
    """

    spoken_text = _clean_for_speech(
        text
    )

    if not spoken_text:
        return

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False,
        ) as temp_file:
            temp_path = Path(
                temp_file.name
            )

        with wave.open(
            str(temp_path),
            "wb",
        ) as wav_file:
            voice.synthesize_wav(
                spoken_text,
                wav_file,
            )

        subprocess.run(
            [
                "aplay",
                "-q",
                str(temp_path),
            ],
            check=True,
        )

    finally:
        if (
            temp_path is not None
            and temp_path.exists()
        ):
            try:
                temp_path.unlink()
            except OSError:
                pass


def _speech_worker():
    """
    Dedicated SATURN speech worker.

    Piper is loaded once and kept in memory rather than reloading
    the neural voice for every response.
    """

    try:
        voice = _load_voice()

    except Exception as error:
        print(
            "S.A.T.U.R.N. TTS startup warning: "
            f"{error}"
        )
        return

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
            if _voice_enabled:
                _synthesize_and_play(
                    voice,
                    text,
                )

        except Exception as error:
            print(
                "S.A.T.U.R.N. TTS warning: "
                f"{error}"
            )

        finally:
            if finished_event is not None:
                finished_event.set()

            _speech_queue.task_done()


def _ensure_worker():
    """
    Start SATURN's TTS worker once.
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
    Return SATURN's configured Piper voice.

    This preserves the existing public function used elsewhere
    while SATURN transitions away from system TTS voices.
    """

    if not VOICE_MODEL_PATH.exists():
        return []

    return [
        {
            "index": 0,
            "id": str(
                VOICE_MODEL_PATH
            ),
            "name": "SATURN Alba",
            "languages": [
                "en_GB"
            ],
            "gender": "female",
            "age": None,
        }
    ]


def set_preferred_voice(
    name_contains=None,
    voice_index=None,
):
    """
    Compatibility function retained for SATURN's existing interface.

    SATURN v1 currently uses the dedicated Alba Piper model.
    """

    return


def get_voice_preference():
    """
    Return SATURN's active neural voice configuration.
    """

    return {
        "backend": "piper",
        "name": "SATURN Alba",
        "model": str(
            VOICE_MODEL_PATH
        ),
    }


def speak_async(text):
    """
    Queue text to be spoken without blocking the caller.
    """

    if not _voice_enabled:
        return

    if PiperVoice is None:
        print(
            "S.A.T.U.R.N. TTS is unavailable. "
            "Install Piper with: "
            "python -m pip install piper-tts"
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
    Speak text and wait until synthesis and audio playback have
    actually completed.

    The hands-free voice assistant uses this before handing the
    microphone back to speech recognition.
    """

    if not _voice_enabled:
        return

    if PiperVoice is None:
        print(
            "S.A.T.U.R.N. TTS is unavailable. "
            "Install Piper with: "
            "python -m pip install piper-tts"
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

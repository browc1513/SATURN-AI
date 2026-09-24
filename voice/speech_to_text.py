"""
S.A.T.U.R.N. Speech-to-Text

Push-to-talk speech recognition for the desktop GUI.

Current v1 backend:
    SpeechRecognition + Google Web Speech API

The microphone is activated only when the user presses the Talk button.
No continuous listening or wake-word detection is performed.
"""

try:
    import speech_recognition as sr
except ImportError:
    sr = None


DEFAULT_LANGUAGE = "en-US"


def listen_once(
    timeout=5,
    phrase_time_limit=15,
    language=DEFAULT_LANGUAGE,
    pause_threshold=1.25,
    phrase_threshold=0.25,
    non_speaking_duration=0.5,
    ambient_duration=0.4,
):
    """
    Listen for one spoken request and return a structured result.

    Returns:
        {
            "success": bool,
            "text": str,
            "response": str,
            "error": str | None
        }
    """

    if sr is None:
        return {
            "success": False,
            "text": "",
            "response": (
                "Speech recognition is not installed yet. "
                "Install it with: "
                "python -m pip install \"SpeechRecognition[audio]\""
            ),
            "error": "speech_recognition is not installed.",
        }

    recognizer = sr.Recognizer()

    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = float(
        pause_threshold
    )
    recognizer.phrase_threshold = float(
        phrase_threshold
    )
    recognizer.non_speaking_duration = float(
        non_speaking_duration
    )

    if (
        recognizer.non_speaking_duration
        > recognizer.pause_threshold
    ):
        return {
            "success": False,
            "text": "",
            "response": (
                "Speech timing configuration is invalid."
            ),
            "error": (
                "Non-speaking duration cannot exceed "
                "the pause threshold."
            ),
        }

    try:
        with sr.Microphone() as source:
            # Briefly sample current room noise before listening.
            recognizer.adjust_for_ambient_noise(
                source,
                duration=float(
                    ambient_duration
                ),
            )

            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit,
            )

    except sr.WaitTimeoutError:
        return {
            "success": False,
            "text": "",
            "response": (
                "I didn't hear anything. Press Talk and begin "
                "speaking within a few seconds."
            ),
            "error": "Microphone listening timed out.",
        }

    except OSError as error:
        return {
            "success": False,
            "text": "",
            "response": (
                "I couldn't access a microphone. Check that Windows "
                "can see your microphone and that microphone access "
                "is enabled for desktop apps."
            ),
            "error": str(error),
        }

    except Exception as error:
        return {
            "success": False,
            "text": "",
            "response": (
                "Something went wrong while opening the microphone."
            ),
            "error": str(error),
        }

    try:
        text = recognizer.recognize_google(
            audio,
            language=language,
        )

        return {
            "success": True,
            "text": text,
            "response": text,
            "error": None,
        }

    except sr.UnknownValueError:
        return {
            "success": False,
            "text": "",
            "response": (
                "I heard you, but I couldn't understand what was said."
            ),
            "error": "Speech was not understood.",
        }

    except sr.RequestError as error:
        return {
            "success": False,
            "text": "",
            "response": (
                "Speech recognition could not reach its online "
                "recognition service. Check your internet connection."
            ),
            "error": str(error),
        }

    except Exception as error:
        return {
            "success": False,
            "text": "",
            "response": (
                "Something went wrong while converting speech to text."
            ),
            "error": str(error),
        }

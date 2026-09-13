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

    try:
        with sr.Microphone() as source:
            # Briefly sample the room so normal background noise
            # does not get interpreted as speech.
            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5,
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

from types import SimpleNamespace

from voice import speech_to_text


class FakeWaitTimeoutError(Exception):
    pass


class FakeUnknownValueError(Exception):
    pass


class FakeRequestError(Exception):
    pass


class FakeMicrophone:
    def __enter__(self):
        return "microphone-source"

    def __exit__(
        self,
        exception_type,
        exception,
        traceback,
    ):
        return False


class FakeRecognizer:
    instance = None

    def __init__(self):
        FakeRecognizer.instance = self
        self.dynamic_energy_threshold = False
        self.pause_threshold = None
        self.phrase_threshold = None
        self.non_speaking_duration = None
        self.ambient_duration = None
        self.listen_arguments = None

    def adjust_for_ambient_noise(
        self,
        source,
        duration,
    ):
        assert source == "microphone-source"
        self.ambient_duration = duration

    def listen(
        self,
        source,
        timeout,
        phrase_time_limit,
    ):
        self.listen_arguments = {
            "source": source,
            "timeout": timeout,
            "phrase_time_limit": phrase_time_limit,
        }

        return "captured-audio"

    def recognize_google(
        self,
        audio,
        language,
    ):
        assert audio == "captured-audio"
        assert language == "en-US"

        return "A complete spoken command"


def fake_speech_recognition():
    return SimpleNamespace(
        Recognizer=FakeRecognizer,
        Microphone=FakeMicrophone,
        WaitTimeoutError=FakeWaitTimeoutError,
        UnknownValueError=FakeUnknownValueError,
        RequestError=FakeRequestError,
    )


def test_listen_once_applies_adaptive_pause_settings(
    monkeypatch,
):
    monkeypatch.setattr(
        speech_to_text,
        "sr",
        fake_speech_recognition(),
    )

    result = speech_to_text.listen_once(
        timeout=10,
        phrase_time_limit=30,
        pause_threshold=1.25,
        phrase_threshold=0.25,
        non_speaking_duration=0.5,
        ambient_duration=0.4,
    )

    recognizer = FakeRecognizer.instance

    assert result["success"] is True
    assert result["text"] == "A complete spoken command"
    assert recognizer.dynamic_energy_threshold is True
    assert recognizer.pause_threshold == 1.25
    assert recognizer.phrase_threshold == 0.25
    assert recognizer.non_speaking_duration == 0.5
    assert recognizer.ambient_duration == 0.4
    assert recognizer.listen_arguments == {
        "source": "microphone-source",
        "timeout": 10,
        "phrase_time_limit": 30,
    }


def test_invalid_pause_relationship_is_rejected(
    monkeypatch,
):
    monkeypatch.setattr(
        speech_to_text,
        "sr",
        fake_speech_recognition(),
    )

    result = speech_to_text.listen_once(
        pause_threshold=0.4,
        non_speaking_duration=0.5,
    )

    assert result["success"] is False
    assert (
        result["error"]
        == (
            "Non-speaking duration cannot exceed "
            "the pause threshold."
        )
    )

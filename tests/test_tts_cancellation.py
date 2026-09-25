import threading
from unittest.mock import patch

from voice.text_to_speech import _synthesize_and_play


class FakeVoice:
    def synthesize_wav(self, text, wav_file):
        assert text == "A spoken reply"
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(16000)
        wav_file.writeframes(b"\x00\x00" * 10)


def test_stop_terminates_current_playback():
    cancelled = threading.Event()

    class FakePlayer:
        returncode = None
        args = ["aplay"]

        def __init__(self):
            self.terminated = False

        def poll(self):
            cancelled.set()
            return None if not self.terminated else 0

        def terminate(self):
            self.terminated = True

        def wait(self, timeout=None):
            self.returncode = 0
            return 0

    player = FakePlayer()
    with patch(
        "voice.text_to_speech.subprocess.Popen",
        return_value=player,
    ) as popen:
        _synthesize_and_play(
            FakeVoice(), "A spoken reply", cancel_event=cancelled
        )

    popen.assert_called_once()
    assert player.terminated


def test_reply_completes_without_stop():
    class FakePlayer:
        returncode = 0
        args = ["aplay"]

        def poll(self):
            return 0

        def terminate(self):
            raise AssertionError("Completed reply must not terminate")

    player = FakePlayer()
    with patch(
        "voice.text_to_speech.subprocess.Popen",
        return_value=player,
    ):
        _synthesize_and_play(
            FakeVoice(),
            "A spoken reply",
            cancel_event=threading.Event(),
        )

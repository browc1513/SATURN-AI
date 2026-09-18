import time
from pathlib import Path

import numpy as np
import pyaudio
from openwakeword.model import Model


RATE = 16000
CHANNELS = 1
CHUNK = 1280
THRESHOLD = 0.5

MODEL_PATH = (
    Path(__file__).resolve().parent
    / "models"
    / "hey_saturn.onnx"
)


def create_wake_model():
    """
    Load and return the custom Hey Saturn wake-word model.
    """

    return Model(
        wakeword_models=[str(MODEL_PATH)],
        inference_framework="onnx",
    )


def wait_for_wake_word(model):
    """
    Listen until Hey Saturn is detected.

    The microphone stream is closed before returning so another
    subsystem, such as speech-to-text, can safely use the microphone.

    Returns:
        {
            "wakeword": str,
            "score": float
        }
    """

    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=pyaudio.paInt16,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    print("Waiting for 'Hey Saturn'...")

    try:
        while True:
            audio_bytes = stream.read(
                CHUNK,
                exception_on_overflow=False,
            )

            audio_frame = np.frombuffer(
                audio_bytes,
                dtype=np.int16,
            )

            prediction = model.predict(
                audio_frame
            )

            for wakeword, score in prediction.items():
                if score >= THRESHOLD:
                    print(
                        f"Wake word detected! "
                        f"{wakeword} score={score:.3f}"
                    )

                    model.reset()

                    return {
                        "wakeword": wakeword,
                        "score": float(score),
                    }

    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()


def main():
    """
    Standalone wake-word test.
    """

    print("Loading openWakeWord...")
    print(f"Model: {MODEL_PATH}")

    model = create_wake_model()

    print("Listening for 'Hey Saturn'...")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            wait_for_wake_word(
                model
            )

            # Preserve the behavior of the original known-good
            # standalone listener.
            time.sleep(1)

    except KeyboardInterrupt:
        print(
            "\nStopping wake-word listener..."
        )


if __name__ == "__main__":
    main()

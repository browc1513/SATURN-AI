import time

from core.saturn_instance import get_saturn
from voice.speech_to_text import listen_once
from voice.text_to_speech import speak_async
from voice.wake_word import (
    MODEL_PATH,
    create_wake_model,
    wait_for_wake_word,
)


ACKNOWLEDGEMENT = "Yes?"

# Temporary synchronization because speak_async() queues speech
# in another thread and returns immediately.
ACKNOWLEDGEMENT_WAIT_SECONDS = 2.0


def wait_for_response_speech(response):
    """
    Temporary v1 approximation of TTS duration.

    Later this should be replaced with explicit TTS completion
    signaling instead of a timer.
    """

    return max(
        3,
        min(
            10,
            len(str(response)) / 15,
        ),
    )


def main():
    print(
        "Starting S.A.T.U.R.N. voice assistant..."
    )

    # ----------------------------------------------------------
    # Initialize SATURN
    # ----------------------------------------------------------
    saturn = get_saturn()

    # ----------------------------------------------------------
    # Load the same custom wake model used by the proven
    # standalone wake-word listener.
    # ----------------------------------------------------------
    print(
        f"Loading wake-word model: {MODEL_PATH}"
    )

    wake_model = create_wake_model()

    print(
        "S.A.T.U.R.N. voice assistant is ready."
    )
    print(
        "Press Ctrl+C to stop.\n"
    )

    try:
        while True:

            # --------------------------------------------------
            # 1. Wait for Hey Saturn
            #
            # This calls the exact reusable listener from
            # voice/wake_word.py.
            # --------------------------------------------------
            wait_for_wake_word(
                wake_model
            )

            # --------------------------------------------------
            # 2. Acknowledge wake event
            # --------------------------------------------------
            print(
                "S.A.T.U.R.N.: Yes?"
            )

            speak_async(
                ACKNOWLEDGEMENT
            )

            time.sleep(
                ACKNOWLEDGEMENT_WAIT_SECONDS
            )

            # --------------------------------------------------
            # 3. Listen for one command
            # --------------------------------------------------
            print(
                "Listening for command..."
            )

            speech_result = listen_once(
                timeout=5,
                phrase_time_limit=15,
            )

            # --------------------------------------------------
            # 4. Handle STT failure
            # --------------------------------------------------
            if not speech_result["success"]:
                response = speech_result[
                    "response"
                ]

                print(
                    f"S.A.T.U.R.N.: {response}"
                )

                if speech_result.get("error"):
                    print(
                        "STT error: "
                        f"{speech_result['error']}"
                    )

                speak_async(
                    response
                )

                time.sleep(3)

                print()

                continue

            # --------------------------------------------------
            # 5. Extract recognized command
            # --------------------------------------------------
            command = speech_result[
                "text"
            ]

            print(
                f"You: {command}"
            )

            # --------------------------------------------------
            # 6. Send raw command through SATURN
            # --------------------------------------------------
            result = saturn.handle_query(
                command
            )

            response = result.get(
                "response",
                "I couldn't generate a response.",
            )

            print(
                f"S.A.T.U.R.N.: {response}"
            )

            # --------------------------------------------------
            # 7. Speak SATURN response
            # --------------------------------------------------
            speak_async(
                response
            )

            time.sleep(
                wait_for_response_speech(
                    response
                )
            )

            print()

    except KeyboardInterrupt:
        print(
            "\nStopping S.A.T.U.R.N. "
            "voice assistant..."
        )


if __name__ == "__main__":
    main()

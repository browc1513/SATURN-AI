from assistant_tools.alarm_playback import (
    is_dismissal_required_alarm_ringing,
)
from core.saturn_instance import get_saturn
from voice.alarm_control import (
    ALARM_CONTROL_PHRASE_LIMIT_SECONDS,
    ALARM_CONTROL_TIMEOUT_SECONDS,
    is_wake_free_alarm_command,
)
from voice.conversation_control import (
    is_silent_follow_up_timeout,
    load_voice_timing,
    should_listen_for_follow_up,
)
from voice.speech_to_text import listen_once
from voice.text_to_speech import speak_and_wait
from voice.wake_word import (
    MODEL_PATH,
    create_wake_model,
    wait_for_wake_word,
)


ACKNOWLEDGEMENT = "Yes?"
VOICE_SESSION_ID = "voice"


def main():
    print(
        "Starting S.A.T.U.R.N. voice assistant..."
    )

    # ----------------------------------------------------------
    # Initialize SATURN
    # ----------------------------------------------------------
    saturn = get_saturn()
    voice_timing = load_voice_timing()

    # ----------------------------------------------------------
    # Load custom Hey Saturn wake-word model
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
            # 1. Wait for "Hey Saturn"
            # --------------------------------------------------
            wake_event = wait_for_wake_word(
                wake_model,
                interrupt_check=(
                    is_dismissal_required_alarm_ringing
                ),
            )

            if wake_event is None:
                print(
                    "Continuous alarm active; "
                    "listening for stop or snooze..."
                )

                speech_result = listen_once(
                    timeout=(
                        ALARM_CONTROL_TIMEOUT_SECONDS
                    ),
                    phrase_time_limit=(
                        ALARM_CONTROL_PHRASE_LIMIT_SECONDS
                    ),
                )

                if not speech_result["success"]:
                    continue

                command = speech_result["text"]

                if not is_wake_free_alarm_command(
                    command
                ):
                    print(
                        "Ignored non-alarm speech "
                        "while alarm was ringing."
                    )
                    continue

                print(
                    f"You: {command}"
                )

                result = saturn.handle_query(
                    command,
                    session_id=VOICE_SESSION_ID,
                )

                response = result.get(
                    "response",
                    "I couldn't control the alarm.",
                )

                print(
                    f"S.A.T.U.R.N.: {response}"
                )

                speak_and_wait(
                    response
                )

                print()
                continue

            # --------------------------------------------------
            # 2. Acknowledge wake event
            #
            # Wait for the actual TTS engine to finish instead
            # of guessing how long "Yes?" takes.
            # --------------------------------------------------
            print(
                "S.A.T.U.R.N.: Yes?"
            )

            speak_and_wait(
                ACKNOWLEDGEMENT
            )

            # --------------------------------------------------
            # 3. Immediately hand the microphone to STT
            # --------------------------------------------------
            print(
                "Listening for command..."
            )

            speech_result = listen_once(
                timeout=voice_timing[
                    "command_timeout"
                ],
                phrase_time_limit=voice_timing[
                    "command_phrase_limit"
                ],
                pause_threshold=voice_timing[
                    "pause_threshold"
                ],
                phrase_threshold=voice_timing[
                    "phrase_threshold"
                ],
                non_speaking_duration=voice_timing[
                    "non_speaking_duration"
                ],
                ambient_duration=voice_timing[
                    "ambient_duration"
                ],
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

                speak_and_wait(
                    response
                )

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
            # 6. Route through SATURN
            # --------------------------------------------------
            result = saturn.handle_query(
                command,
                session_id=VOICE_SESSION_ID,
            )

            response = result.get(
                "response",
                "I couldn't generate a response.",
            )

            print(
                f"S.A.T.U.R.N.: {response}"
            )

            # --------------------------------------------------
            # 7. Speak response and wait for actual completion
            # --------------------------------------------------
            speak_and_wait(
                response
            )

            print()

            # --------------------------------------------------
            # 8. Continue listening when SATURN explicitly asks
            #    for a short follow-up response.
            # --------------------------------------------------
            while should_listen_for_follow_up(
                result
            ):
                print(
                    "Listening for follow-up..."
                )

                speech_result = listen_once(
                    timeout=voice_timing[
                        "follow_up_timeout"
                    ],
                    phrase_time_limit=voice_timing[
                        "follow_up_phrase_limit"
                    ],
                    pause_threshold=voice_timing[
                        "pause_threshold"
                    ],
                    phrase_threshold=voice_timing[
                        "phrase_threshold"
                    ],
                    non_speaking_duration=voice_timing[
                        "non_speaking_duration"
                    ],
                    ambient_duration=voice_timing[
                        "ambient_duration"
                    ],
                )

                if not speech_result["success"]:
                    if is_silent_follow_up_timeout(
                        speech_result
                    ):
                        print(
                            "Follow-up window closed."
                        )
                        print()
                        break

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

                    speak_and_wait(
                        response
                    )

                    print()
                    break

                command = speech_result[
                    "text"
                ]

                print(
                    f"You: {command}"
                )

                result = saturn.handle_query(
                    command,
                    session_id=VOICE_SESSION_ID,
                )

                response = result.get(
                    "response",
                    "I couldn't generate a response.",
                )

                print(
                    f"S.A.T.U.R.N.: {response}"
                )

                speak_and_wait(
                    response
                )

                print()

            # Return to wake-word listening when the exchange ends.

    except KeyboardInterrupt:
        print(
            "\nStopping S.A.T.U.R.N. "
            "voice assistant..."
        )


if __name__ == "__main__":
    main()

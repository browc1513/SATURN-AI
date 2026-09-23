from pathlib import Path


VOICE_ASSISTANT_PATH = Path(
    "voice/voice_assistant.py"
)


def read_voice_source():
    return VOICE_ASSISTANT_PATH.read_text(
        encoding="utf-8"
    )


def test_voice_assistant_loads_configurable_timing():
    source = read_voice_source()

    assert "voice_timing = load_voice_timing()" in source
    assert '"command_timeout"' in source
    assert '"command_phrase_limit"' in source
    assert '"follow_up_timeout"' in source
    assert '"follow_up_phrase_limit"' in source


def test_voice_assistant_has_follow_up_loop():
    source = read_voice_source()

    assert (
        "while should_listen_for_follow_up("
        in source
    )
    assert "Listening for follow-up..." in source
    assert (
        "session_id=VOICE_SESSION_ID"
        in source
    )

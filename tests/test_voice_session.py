import ast
from pathlib import Path


VOICE_ASSISTANT_PATH = Path(
    "voice/voice_assistant.py"
)


def load_voice_source():
    return VOICE_ASSISTANT_PATH.read_text(
        encoding="utf-8"
    )


def test_voice_session_id_is_defined():
    tree = ast.parse(
        load_voice_source()
    )

    assignments = {
        target.id: node.value.value
        for node in tree.body
        if isinstance(node, ast.Assign)
        for target in node.targets
        if isinstance(target, ast.Name)
        and isinstance(node.value, ast.Constant)
    }

    assert assignments["VOICE_SESSION_ID"] == "voice"


def test_voice_query_uses_voice_session():
    source = load_voice_source()

    assert '''result = saturn.handle_query(
                command,
                session_id=VOICE_SESSION_ID,
            )''' in source

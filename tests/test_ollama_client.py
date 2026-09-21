import json
from unittest.mock import patch
from urllib.error import URLError

import pytest

from ai_models.ollama_client import (
    OllamaClient,
    OllamaError,
)


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(
        self,
        exception_type,
        exception,
        traceback,
    ):
        return False

    def read(self):
        return json.dumps(
            self.payload
        ).encode("utf-8")


def test_ollama_chat_returns_assistant_content():
    client = OllamaClient(
        model="test-model",
        timeout=12,
    )

    fake_response = FakeResponse(
        {
            "message": {
                "role": "assistant",
                "content": "Hello from SATURN.",
            }
        }
    )

    with patch(
        "ai_models.ollama_client.urlopen",
        return_value=fake_response,
    ) as mocked_urlopen:
        result = client.chat(
            "Hello",
            system_prompt="You are SATURN.",
        )

    assert result == "Hello from SATURN."

    request = mocked_urlopen.call_args.args[0]
    timeout = mocked_urlopen.call_args.kwargs["timeout"]
    payload = json.loads(
        request.data.decode("utf-8")
    )

    assert request.full_url == (
        "http://127.0.0.1:11434/api/chat"
    )
    assert timeout == 12
    assert payload == {
        "model": "test-model",
        "messages": [
            {
                "role": "system",
                "content": "You are SATURN.",
            },
            {
                "role": "user",
                "content": "Hello",
            },
        ],
        "stream": False,
    }


def test_ollama_chat_wraps_connection_errors():
    client = OllamaClient(
        model="test-model"
    )

    with patch(
        "ai_models.ollama_client.urlopen",
        side_effect=URLError("offline"),
    ):
        with pytest.raises(
            OllamaError,
            match="Ollama request failed",
        ):
            client.chat("Hello")


def test_ollama_chat_rejects_empty_response():
    client = OllamaClient(
        model="test-model"
    )

    fake_response = FakeResponse(
        {
            "message": {
                "role": "assistant",
                "content": "   ",
            }
        }
    )

    with patch(
        "ai_models.ollama_client.urlopen",
        return_value=fake_response,
    ):
        with pytest.raises(
            OllamaError,
            match="empty response",
        ):
            client.chat("Hello")


@pytest.mark.parametrize(
    "message",
    ["", "   ", None],
)
def test_ollama_chat_rejects_empty_user_message(
    message,
):
    client = OllamaClient(
        model="test-model"
    )

    with pytest.raises(
        ValueError,
        match="user message",
    ):
        client.chat(message)

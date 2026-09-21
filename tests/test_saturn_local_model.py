import json
from pathlib import Path
from unittest.mock import patch

from ai_models.ollama_client import (
    OllamaClient,
    OllamaError,
)
from core.saturn_personality import SATURN


def create_config(
    tmp_path,
    enabled,
):
    config = json.loads(
        Path("saturn_config.json").read_text(
            encoding="utf-8"
        )
    )

    config["local_model"] = {
        "enabled": enabled,
        "provider": "ollama",
        "model": "test-model",
        "base_url": "http://127.0.0.1:11434",
        "timeout_seconds": 5,
        "system_prompt": "You are test SATURN.",
    }

    config_path = tmp_path / "saturn-test-config.json"
    config_path.write_text(
        json.dumps(config),
        encoding="utf-8",
    )

    return config_path


def test_local_model_is_disabled_by_default():
    saturn = SATURN(
        start_alarm_monitor=False
    )

    result = saturn.handle_query(
        "Paint the moon purple"
    )

    assert saturn.local_model is None
    assert result["success"] is False
    assert result["domain"] == "unknown"


def test_unknown_query_uses_enabled_local_model(
    tmp_path,
):
    config_path = create_config(
        tmp_path,
        enabled=True,
    )

    with patch.object(
        OllamaClient,
        "chat",
        return_value="Purple moon protocol engaged.",
    ) as mocked_chat:
        saturn = SATURN(
            config_path=str(config_path),
            start_alarm_monitor=False,
        )

        result = saturn.handle_query(
            "Paint the moon purple"
        )

    assert result == {
        "success": True,
        "domain": "conversation",
        "response": "Purple moon protocol engaged.",
        "data": {
            "provider": "ollama",
            "model": "test-model",
        },
    }

    mocked_chat.assert_called_once_with(
        "Paint the moon purple",
        system_prompt="You are test SATURN.",
        conversation_history=[],
    )


def test_known_domain_bypasses_local_model(
    tmp_path,
):
    config_path = create_config(
        tmp_path,
        enabled=True,
    )

    with patch.object(
        OllamaClient,
        "chat",
    ) as mocked_chat:
        saturn = SATURN(
            config_path=str(config_path),
            start_alarm_monitor=False,
        )

        result = saturn.handle_query(
            "What is 2 plus 2?"
        )

    assert result["success"] is True
    assert result["domain"] == "math"
    mocked_chat.assert_not_called()


def test_model_failure_preserves_unknown_fallback(
    tmp_path,
):
    config_path = create_config(
        tmp_path,
        enabled=True,
    )

    with patch.object(
        OllamaClient,
        "chat",
        side_effect=OllamaError("offline"),
    ):
        saturn = SATURN(
            config_path=str(config_path),
            start_alarm_monitor=False,
        )

        result = saturn.handle_query(
            "Paint the moon purple"
        )

    assert result["success"] is False
    assert result["domain"] == "unknown"
    assert "not sure which subsystem" in (
        result["response"]
    )


def test_environment_can_enable_local_model(
    monkeypatch,
):
    monkeypatch.setenv(
        "SATURN_LOCAL_MODEL_ENABLED",
        "true",
    )
    monkeypatch.setenv(
        "SATURN_LOCAL_MODEL_NAME",
        "qwen3:8b",
    )

    with patch.object(
        OllamaClient,
        "chat",
        return_value="Environment model response.",
    ) as mocked_chat:
        saturn = SATURN(
            start_alarm_monitor=False
        )

        result = saturn.handle_query(
            "Paint the moon purple"
        )

    assert saturn.local_model_enabled is True
    assert saturn.local_model.model == "qwen3:8b"
    assert result["success"] is True
    assert result["domain"] == "conversation"
    mocked_chat.assert_called_once()


def test_environment_can_force_model_disabled(
    tmp_path,
    monkeypatch,
):
    config_path = create_config(
        tmp_path,
        enabled=True,
    )

    monkeypatch.setenv(
        "SATURN_LOCAL_MODEL_ENABLED",
        "false",
    )

    with patch.object(
        OllamaClient,
        "chat",
    ) as mocked_chat:
        saturn = SATURN(
            config_path=str(config_path),
            start_alarm_monitor=False,
        )

        result = saturn.handle_query(
            "Paint the moon purple"
        )

    assert saturn.local_model_enabled is False
    assert saturn.local_model is None
    assert result["success"] is False
    assert result["domain"] == "unknown"
    mocked_chat.assert_not_called()


def test_session_remembers_successful_exchanges(
    tmp_path,
):
    config_path = create_config(
        tmp_path,
        enabled=True,
    )

    with patch.object(
        OllamaClient,
        "chat",
        side_effect=[
            "Nice to meet you, Colin.",
            "Your name is Colin.",
        ],
    ) as mocked_chat:
        saturn = SATURN(
            config_path=str(config_path),
            start_alarm_monitor=False,
        )

        first_result = saturn.handle_query(
            "My name is Colin.",
            session_id="phone-a",
        )
        second_result = saturn.handle_query(
            "What is my name?",
            session_id="phone-a",
        )

    assert first_result["success"] is True
    assert second_result["response"] == (
        "Your name is Colin."
    )

    first_call = mocked_chat.call_args_list[0]
    second_call = mocked_chat.call_args_list[1]

    assert (
        first_call.kwargs["conversation_history"]
        == []
    )
    assert (
        second_call.kwargs["conversation_history"]
        == [
            {
                "role": "user",
                "content": "My name is Colin.",
            },
            {
                "role": "assistant",
                "content": "Nice to meet you, Colin.",
            },
        ]
    )


def test_conversation_sessions_remain_isolated(
    tmp_path,
):
    config_path = create_config(
        tmp_path,
        enabled=True,
    )

    with patch.object(
        OllamaClient,
        "chat",
        side_effect=[
            "Response for phone A.",
            "Response for phone B.",
        ],
    ) as mocked_chat:
        saturn = SATURN(
            config_path=str(config_path),
            start_alarm_monitor=False,
        )

        saturn.handle_query(
            "Message from phone A",
            session_id="phone-a",
        )
        saturn.handle_query(
            "Message from phone B",
            session_id="phone-b",
        )

    second_call = mocked_chat.call_args_list[1]

    assert (
        second_call.kwargs["conversation_history"]
        == []
    )
    assert saturn.conversation_memory.get_history(
        "phone-a"
    )[0]["content"] == "Message from phone A"
    assert saturn.conversation_memory.get_history(
        "phone-b"
    )[0]["content"] == "Message from phone B"


def test_failed_model_request_is_not_remembered(
    tmp_path,
):
    config_path = create_config(
        tmp_path,
        enabled=True,
    )

    with patch.object(
        OllamaClient,
        "chat",
        side_effect=[
            OllamaError("offline"),
            "Recovered response.",
        ],
    ) as mocked_chat:
        saturn = SATURN(
            config_path=str(config_path),
            start_alarm_monitor=False,
        )

        failed_result = saturn.handle_query(
            "Failed message",
            session_id="phone-a",
        )
        recovered_result = saturn.handle_query(
            "New message",
            session_id="phone-a",
        )

    assert failed_result["success"] is False
    assert recovered_result["success"] is True

    second_call = mocked_chat.call_args_list[1]

    assert (
        second_call.kwargs["conversation_history"]
        == []
    )
    assert saturn.conversation_memory.get_history(
        "phone-a"
    ) == [
        {
            "role": "user",
            "content": "New message",
        },
        {
            "role": "assistant",
            "content": "Recovered response.",
        },
    ]

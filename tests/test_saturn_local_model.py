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

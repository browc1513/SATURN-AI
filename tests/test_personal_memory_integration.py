from unittest.mock import Mock
from unittest.mock import patch

from ai_models.personal_memory import (
    PersonalMemoryStore,
)
from core.saturn_personality import SATURN


def create_saturn(
    tmp_path,
):
    saturn = SATURN(
        start_alarm_monitor=False
    )
    saturn.personal_memory = PersonalMemoryStore(
        database_path=(
            tmp_path
            / "integration-memory.db"
        )
    )
    saturn.personal_memory_enabled = True

    return saturn


def test_explicit_remember_command_stores_memory(
    tmp_path,
):
    saturn = create_saturn(
        tmp_path
    )

    result = saturn.handle_query(
        "Remember that my dog is named Snoopy.",
        session_id="phone-a",
    )

    assert result["success"] is True
    assert result["domain"] == "memory"
    assert result["data"]["action"] == "remember"
    assert result["data"]["status"] == "created"

    memories = saturn.personal_memory.list_memories()

    assert [
        memory["content"]
        for memory in memories
    ] == [
        "my dog is named Snoopy."
    ]


def test_duplicate_remember_command_is_idempotent(
    tmp_path,
):
    saturn = create_saturn(
        tmp_path
    )

    first = saturn.handle_query(
        "Remember that my dog is named Snoopy.",
        session_id="phone-a",
    )
    duplicate = saturn.handle_query(
        "Remember that MY DOG IS NAMED SNOOPY",
        session_id="phone-b",
    )

    assert first["data"]["status"] == "created"
    assert duplicate["success"] is True
    assert duplicate["data"]["status"] == "existing"
    assert duplicate["response"] == (
        "I already remember that."
    )
    assert saturn.personal_memory.count() == 1


def test_memory_list_command_returns_saved_facts(
    tmp_path,
):
    saturn = create_saturn(
        tmp_path
    )

    saturn.handle_query(
        "Remember that my dog is named Snoopy."
    )
    saturn.handle_query(
        "Remember that my favorite color is blue."
    )

    result = saturn.handle_query(
        "What do you remember about me?"
    )

    assert result["success"] is True
    assert result["domain"] == "memory"
    assert result["data"]["action"] == "list"
    assert result["data"]["count"] == 2
    assert "my dog is named Snoopy." in result["response"]
    assert (
        "my favorite color is blue."
        in result["response"]
    )


def test_empty_memory_list_has_clear_response(
    tmp_path,
):
    saturn = create_saturn(
        tmp_path
    )

    result = saturn.handle_query(
        "Show my memories"
    )

    assert result["success"] is True
    assert result["data"]["count"] == 0
    assert "don't have any persistent memories" in (
        result["response"]
    )


def test_forget_command_removes_matching_memory(
    tmp_path,
):
    saturn = create_saturn(
        tmp_path
    )

    saturn.handle_query(
        "Remember that my dog is named Snoopy."
    )

    result = saturn.handle_query(
        "Forget that my dog is named Snoopy"
    )

    assert result["success"] is True
    assert result["domain"] == "memory"
    assert result["data"]["status"] == "forgotten"
    assert saturn.personal_memory.count() == 0


def test_forget_missing_memory_reports_not_found(
    tmp_path,
):
    saturn = create_saturn(
        tmp_path
    )

    result = saturn.handle_query(
        "Forget that my favorite color is blue."
    )

    assert result["success"] is False
    assert result["data"]["status"] == "not_found"


def test_sensitive_memory_command_is_rejected(
    tmp_path,
):
    saturn = create_saturn(
        tmp_path
    )

    result = saturn.handle_query(
        "Remember that my password is hunter2"
    )

    assert result["success"] is False
    assert result["domain"] == "memory"
    assert result["data"]["status"] == (
        "rejected_sensitive"
    )
    assert saturn.personal_memory.count() == 0


def test_ordinary_conversation_is_not_persisted(
    tmp_path,
):
    saturn = create_saturn(
        tmp_path
    )

    local_model = Mock()
    local_model.model = "test-model"
    local_model.chat.return_value = "Hello."
    saturn.local_model = local_model

    with patch.object(
        saturn,
        "_detect_domain",
        return_value="unknown",
    ):
        result = saturn.handle_query(
            "My favorite color is blue.",
            session_id="phone-a",
        )

    assert result["success"] is True
    assert result["domain"] == "conversation"
    assert saturn.personal_memory.count() == 0


def test_persistent_memory_is_added_to_model_prompt(
    tmp_path,
):
    saturn = create_saturn(
        tmp_path
    )

    saturn.handle_query(
        "Remember that my dog is named Snoopy."
    )

    local_model = Mock()
    local_model.model = "test-model"
    local_model.chat.return_value = (
        "Your dog is named Snoopy."
    )
    saturn.local_model = local_model

    with patch.object(
        saturn,
        "_detect_domain",
        return_value="unknown",
    ):
        result = saturn.handle_query(
            "What is my dog's name?",
            session_id="phone-a",
        )

    assert result["success"] is True

    system_prompt = (
        local_model.chat.call_args.kwargs[
            "system_prompt"
        ]
    )

    assert "user explicitly asked SATURN" in system_prompt
    assert "- my dog is named Snoopy." in system_prompt


def test_empty_memory_does_not_change_model_prompt(
    tmp_path,
):
    saturn = create_saturn(
        tmp_path
    )

    local_model = Mock()
    local_model.model = "test-model"
    local_model.chat.return_value = "Hello."
    saturn.local_model = local_model

    with patch.object(
        saturn,
        "_detect_domain",
        return_value="unknown",
    ):
        saturn.handle_query(
            "Hello",
            session_id="phone-a",
        )

    assert (
        local_model.chat.call_args.kwargs[
            "system_prompt"
        ]
        == saturn.local_model_system_prompt
    )


def test_memory_commands_work_without_local_model(
    tmp_path,
):
    saturn = create_saturn(
        tmp_path
    )
    saturn.local_model = None

    result = saturn.handle_query(
        "Remember that I study physics."
    )

    assert result["success"] is True
    assert result["domain"] == "memory"
    assert saturn.personal_memory.count() == 1


def test_disabled_memory_returns_clear_response(
    tmp_path,
):
    saturn = create_saturn(
        tmp_path
    )
    saturn.personal_memory = None
    saturn.personal_memory_enabled = False

    result = saturn.handle_query(
        "Remember that I study physics."
    )

    assert result["success"] is False
    assert result["domain"] == "memory"
    assert result["data"]["status"] == "disabled"


def test_exact_never_mind_command_remains_control(
    tmp_path,
):
    saturn = create_saturn(
        tmp_path
    )

    result = saturn.handle_query(
        "Forget it"
    )

    assert result["success"] is True
    assert result["domain"] == "control"
    assert saturn.personal_memory.count() == 0

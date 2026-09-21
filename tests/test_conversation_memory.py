import pytest

from ai_models.conversation_memory import (
    ConversationMemory,
)


def test_memory_stores_an_exchange():
    memory = ConversationMemory(
        max_turns=3
    )

    memory.add_exchange(
        "phone-a",
        "My name is Colin.",
        "Nice to meet you, Colin.",
    )

    assert memory.get_history(
        "phone-a"
    ) == [
        {
            "role": "user",
            "content": "My name is Colin.",
        },
        {
            "role": "assistant",
            "content": "Nice to meet you, Colin.",
        },
    ]


def test_sessions_are_isolated():
    memory = ConversationMemory()

    memory.add_exchange(
        "phone-a",
        "Message from A",
        "Response to A",
    )
    memory.add_exchange(
        "phone-b",
        "Message from B",
        "Response to B",
    )

    history_a = memory.get_history(
        "phone-a"
    )
    history_b = memory.get_history(
        "phone-b"
    )

    assert history_a[0]["content"] == (
        "Message from A"
    )
    assert history_b[0]["content"] == (
        "Message from B"
    )


def test_memory_discards_oldest_turns():
    memory = ConversationMemory(
        max_turns=2
    )

    memory.add_exchange(
        "session",
        "User 1",
        "Assistant 1",
    )
    memory.add_exchange(
        "session",
        "User 2",
        "Assistant 2",
    )
    memory.add_exchange(
        "session",
        "User 3",
        "Assistant 3",
    )

    assert memory.get_history(
        "session"
    ) == [
        {
            "role": "user",
            "content": "User 2",
        },
        {
            "role": "assistant",
            "content": "Assistant 2",
        },
        {
            "role": "user",
            "content": "User 3",
        },
        {
            "role": "assistant",
            "content": "Assistant 3",
        },
    ]


def test_memory_can_clear_one_session():
    memory = ConversationMemory()

    memory.add_exchange(
        "phone-a",
        "Message A",
        "Response A",
    )
    memory.add_exchange(
        "phone-b",
        "Message B",
        "Response B",
    )

    memory.clear("phone-a")

    assert memory.get_history(
        "phone-a"
    ) == []
    assert memory.get_history(
        "phone-b"
    )


def test_history_returns_a_copy():
    memory = ConversationMemory()

    memory.add_exchange(
        "session",
        "Original",
        "Original response",
    )

    returned_history = memory.get_history(
        "session"
    )
    returned_history[0]["content"] = "Changed"

    assert memory.get_history(
        "session"
    )[0]["content"] == "Original"


@pytest.mark.parametrize(
    "max_turns",
    [0, -1, 1.5, None],
)
def test_invalid_max_turns_are_rejected(
    max_turns,
):
    with pytest.raises(
        ValueError,
        match="positive integer",
    ):
        ConversationMemory(
            max_turns=max_turns
        )

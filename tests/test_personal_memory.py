from concurrent.futures import ThreadPoolExecutor

import pytest

from ai_models.personal_memory import (
    PersonalMemoryStore,
    SensitiveMemoryError,
)


def create_store(
    tmp_path,
    **kwargs,
):
    return PersonalMemoryStore(
        database_path=(
            tmp_path
            / "saturn-memory.db"
        ),
        **kwargs,
    )


def test_memory_persists_between_store_instances(
    tmp_path,
):
    first_store = create_store(
        tmp_path
    )

    created = first_store.remember(
        "My favorite color is blue."
    )

    second_store = create_store(
        tmp_path
    )
    memories = second_store.list_memories()

    assert created["status"] == "created"
    assert len(memories) == 1
    assert memories[0]["memory_id"] == (
        created["memory_id"]
    )
    assert memories[0]["content"] == (
        "My favorite color is blue."
    )
    assert memories[0]["category"] == "personal"
    assert memories[0]["source"] == "explicit"


def test_duplicate_memory_is_not_created(
    tmp_path,
):
    store = create_store(
        tmp_path
    )

    first = store.remember(
        "My favorite color is blue."
    )
    duplicate = store.remember(
        "  MY FAVORITE COLOR IS BLUE.  "
    )

    assert first["status"] == "created"
    assert duplicate["status"] == "existing"
    assert duplicate["memory_id"] == first["memory_id"]
    assert store.count() == 1


def test_memory_whitespace_is_normalized(
    tmp_path,
):
    store = create_store(
        tmp_path
    )

    memory = store.remember(
        "My   dog\n is   named Snoopy."
    )

    assert memory["content"] == (
        "My dog is named Snoopy."
    )


def test_memories_can_be_searched(
    tmp_path,
):
    store = create_store(
        tmp_path
    )

    store.remember(
        "My dog is named Snoopy."
    )
    store.remember(
        "My favorite color is blue."
    )

    results = store.search(
        "Snoopy"
    )

    assert [
        memory["content"]
        for memory in results
    ] == [
        "My dog is named Snoopy."
    ]


def test_like_wildcards_are_treated_literally(
    tmp_path,
):
    store = create_store(
        tmp_path
    )

    store.remember(
        "My test value is 100%."
    )
    store.remember(
        "A different test value."
    )

    results = store.search(
        "100%"
    )

    assert [
        memory["content"]
        for memory in results
    ] == [
        "My test value is 100%."
    ]


def test_memory_can_be_forgotten_by_content(
    tmp_path,
):
    store = create_store(
        tmp_path
    )

    store.remember(
        "My favorite color is blue."
    )

    assert store.forget_exact(
        "MY FAVORITE COLOR IS BLUE."
    )
    assert store.count() == 0
    assert not store.forget_exact(
        "My favorite color is blue."
    )


def test_memory_can_be_forgotten_by_id(
    tmp_path,
):
    store = create_store(
        tmp_path
    )

    memory = store.remember(
        "My favorite color is blue."
    )

    assert store.forget_by_id(
        memory["memory_id"]
    )
    assert store.count() == 0
    assert not store.forget_by_id(
        memory["memory_id"]
    )


def test_clear_returns_deleted_count(
    tmp_path,
):
    store = create_store(
        tmp_path
    )

    store.remember(
        "My favorite color is blue."
    )
    store.remember(
        "My dog is named Snoopy."
    )

    assert store.clear() == 2
    assert store.count() == 0


def test_prompt_context_contains_memories(
    tmp_path,
):
    store = create_store(
        tmp_path
    )

    store.remember(
        "My dog is named Snoopy."
    )
    store.remember(
        "My favorite color is blue."
    )

    context = store.format_for_prompt()

    assert context.startswith(
        "User-approved persistent facts:"
    )
    assert "- My dog is named Snoopy." in context
    assert "- My favorite color is blue." in context


def test_empty_store_has_no_prompt_context(
    tmp_path,
):
    store = create_store(
        tmp_path
    )

    assert store.format_for_prompt() == ""


def test_prompt_context_respects_limit(
    tmp_path,
):
    store = create_store(
        tmp_path,
        prompt_memory_limit=2,
    )

    store.remember(
        "Memory one."
    )
    store.remember(
        "Memory two."
    )
    store.remember(
        "Memory three."
    )

    context = store.format_for_prompt()

    assert context.count("\n- ") == 2


@pytest.mark.parametrize(
    "content",
    [
        "My password is hunter2",
        "My passcode is 1234",
        "My PIN is 9876",
        "My API key is abc123",
        "My access token is secret-token",
        "My secret is hidden",
        "My SSN is 123-45-6789",
    ],
)
def test_sensitive_information_is_rejected(
    tmp_path,
    content,
):
    store = create_store(
        tmp_path
    )

    with pytest.raises(
        SensitiveMemoryError
    ):
        store.remember(
            content
        )

    assert store.count() == 0


@pytest.mark.parametrize(
    "content",
    [
        None,
        "",
        "   ",
    ],
)
def test_empty_memory_is_rejected(
    tmp_path,
    content,
):
    store = create_store(
        tmp_path
    )

    with pytest.raises(
        ValueError
    ):
        store.remember(
            content
        )


def test_memory_length_is_limited(
    tmp_path,
):
    store = create_store(
        tmp_path,
        max_memory_length=10,
    )

    with pytest.raises(
        ValueError
    ):
        store.remember(
            "This memory is too long."
        )


def test_two_store_instances_share_database(
    tmp_path,
):
    first_store = create_store(
        tmp_path
    )
    second_store = create_store(
        tmp_path
    )

    first_store.remember(
        "My dog is named Snoopy."
    )
    second_store.remember(
        "My favorite color is blue."
    )

    assert first_store.count() == 2
    assert second_store.count() == 2


def test_parallel_writes_do_not_lose_memories(
    tmp_path,
):
    database_path = (
        tmp_path
        / "parallel-memory.db"
    )

    def add_memory(number):
        store = PersonalMemoryStore(
            database_path=database_path
        )
        store.remember(
            f"Parallel memory {number}."
        )

    with ThreadPoolExecutor(
        max_workers=4,
    ) as executor:
        list(
            executor.map(
                add_memory,
                range(8),
            )
        )

    store = PersonalMemoryStore(
        database_path=database_path
    )

    assert store.count() == 8


@pytest.mark.parametrize(
    "kwargs",
    [
        {
            "max_memory_length": 0,
        },
        {
            "prompt_memory_limit": 0,
        },
    ],
)
def test_invalid_configuration_is_rejected(
    tmp_path,
    kwargs,
):
    with pytest.raises(
        ValueError
    ):
        create_store(
            tmp_path,
            **kwargs,
        )

def test_database_file_is_released_after_operations(
    tmp_path,
):
    database_path = (
        tmp_path
        / "released-memory.db"
    )

    store = PersonalMemoryStore(
        database_path=database_path
    )

    store.remember(
        "My dog is named Snoopy."
    )
    store.list_memories()
    store.search(
        "Snoopy"
    )
    store.forget_exact(
        "My dog is named Snoopy."
    )
    store.count()

    database_path.unlink()

    assert not database_path.exists()

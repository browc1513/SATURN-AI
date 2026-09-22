import pytest

from assistant_tools import list_tool
from core.saturn_personality import SATURN


@pytest.fixture
def isolated_lists(
    tmp_path,
    monkeypatch,
):
    lists_path = (
        tmp_path
        / "saturn_lists.json"
    )

    monkeypatch.setattr(
        list_tool,
        "LISTS_FILE",
        str(lists_path),
    )

    return lists_path


@pytest.mark.parametrize(
    "query",
    [
        "Add chicken to my grocery list",
        "Add cattle to my grocery list",
        "Add dog food to my shopping list",
        "What's on my grocery list?",
        "What is on my grocery list?",
        "Show my grocery list",
    ],
)
def test_explicit_list_commands_override_other_domains(
    query,
):
    saturn = SATURN(
        start_alarm_monitor=False
    )

    assert saturn._detect_domain(query) == "lists"


@pytest.mark.parametrize(
    "query",
    [
        "Does this chicken appear ill?",
        "What diseases affect cattle?",
        "What clinical signs should I check in a dog?",
    ],
)
def test_genuine_veterinary_queries_remain_veterinary(
    query,
):
    saturn = SATURN(
        start_alarm_monitor=False
    )

    assert saturn._detect_domain(query) == "veterinary"


@pytest.mark.parametrize(
    "query",
    [
        "What's on my grocery list?",
        "What is on my grocery list?",
        "Show my grocery list",
    ],
)
def test_named_list_questions_extract_the_list_name(
    isolated_lists,
    query,
):
    list_tool.handle_list_query(
        "create a grocery list"
    )
    list_tool.handle_list_query(
        "add chicken and cattle to my grocery list"
    )

    result = list_tool.handle_list_query(
        query
    )

    assert result["success"] is True
    assert result["action"] == "show"
    assert result["list_name"] == "grocery"
    assert result["items"] == [
        "chicken",
        "cattle",
    ]


def test_saturn_adds_veterinary_words_as_list_items(
    isolated_lists,
):
    saturn = SATURN(
        start_alarm_monitor=False
    )

    chicken_result = saturn.handle_query(
        "Add chicken to my grocery list"
    )
    cattle_result = saturn.handle_query(
        "Add cattle to my grocery list"
    )
    show_result = saturn.handle_query(
        "What's on my grocery list?"
    )

    assert chicken_result["success"] is True
    assert chicken_result["domain"] == "lists"

    assert cattle_result["success"] is True
    assert cattle_result["domain"] == "lists"

    assert show_result["success"] is True
    assert show_result["domain"] == "lists"
    assert "chicken" in show_result["response"].lower()
    assert "cattle" in show_result["response"].lower()

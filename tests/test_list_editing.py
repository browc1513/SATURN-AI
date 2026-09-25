import pytest

from assistant_tools import list_tool
from api import saturn_api


@pytest.fixture
def isolated_lists(tmp_path, monkeypatch):
    monkeypatch.setattr(
        list_tool,
        "LISTS_FILE",
        str(tmp_path / "saturn_lists.json"),
    )
    return list_tool


def test_edit_preserves_position_and_follow_up(isolated_lists):
    isolated_lists.handle_list_query("create a grocery list")
    isolated_lists.handle_list_query(
        "add milk, eggs, and bread to my grocery list"
    )

    result = isolated_lists.update_list_item(
        "grocery", "eggs", "oat milk"
    )
    shown = isolated_lists.handle_list_query(
        "show my grocery list"
    )

    assert result["success"] is True
    assert result["items"] == ["milk", "oat milk", "bread"]
    assert shown["items"] == ["milk", "oat milk", "bread"]
    assert "oat milk" in shown["response"]


def test_edit_rejects_duplicate_without_changing_storage(isolated_lists):
    isolated_lists.handle_list_query(
        "add milk and eggs to my grocery list"
    )

    result = isolated_lists.update_list_item(
        "grocery", "eggs", "MILK"
    )

    assert result["success"] is False
    assert result["error"] == "Duplicate item."
    assert isolated_lists.get_all_lists()["lists"][0]["items"] == [
        "milk", "eggs"
    ]


def test_edit_rejects_missing_item_and_empty_replacement(isolated_lists):
    isolated_lists.handle_list_query(
        "add milk to my grocery list"
    )

    missing = isolated_lists.update_list_item(
        "grocery", "bread", "eggs"
    )
    empty = isolated_lists.update_list_item(
        "grocery", "milk", "   "
    )

    assert missing["success"] is False
    assert empty["success"] is False
    assert isolated_lists.get_all_lists()["lists"][0]["items"] == [
        "milk"
    ]


def test_api_edit_passes_literal_item_text(isolated_lists):
    isolated_lists.handle_list_query(
        "add milk to my grocery list"
    )

    response = saturn_api.edit_list_item(
        "grocery",
        "milk",
        saturn_api.ListItemUpdateRequest(
            item="add bread to my chores list"
        ),
    )

    assert response["success"] is True
    assert response["result"]["items"] == [
        "add bread to my chores list"
    ]
    assert [
        entry["name"]
        for entry in isolated_lists.get_all_lists()["lists"]
    ] == ["grocery"]

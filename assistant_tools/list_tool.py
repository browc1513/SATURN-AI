"""
S.A.T.U.R.N. List Tool

Persistent local list management stored in:
    data/saturn_lists.json

Supported actions:
    create
    show
    add
    remove
    clear
    delete
"""

import json
import os
import re


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(
    PROJECT_ROOT,
    "data",
)

LISTS_FILE = os.path.join(
    DATA_DIR,
    "saturn_lists.json",
)


def _ensure_storage():
    os.makedirs(
        DATA_DIR,
        exist_ok=True,
    )

    if not os.path.exists(
        LISTS_FILE
    ):
        with open(
            LISTS_FILE,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                {},
                file,
                indent=2,
            )


def _load_lists():
    _ensure_storage()

    try:
        with open(
            LISTS_FILE,
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(
                file
            )

    except (
        json.JSONDecodeError,
        OSError,
    ):
        data = {}

    if not isinstance(
        data,
        dict,
    ):
        data = {}

    return data


def _save_lists(data):
    _ensure_storage()

    with open(
        LISTS_FILE,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
        )


def _normalize_list_name(name):
    name = str(name).strip().lower()

    name = re.sub(
        r"\b(?:my|the|a|an)\b",
        " ",
        name,
        flags=re.IGNORECASE,
    )

    name = re.sub(
        r"\blist\b",
        " ",
        name,
        flags=re.IGNORECASE,
    )

    name = re.sub(
        r"\s+",
        " ",
        name,
    ).strip()

    return name or "default"


def _display_name(name):
    return " ".join(
        word.capitalize()
        for word in str(name).split()
    )


def _split_items(text):
    """
    Split common natural-language item lists.

    Examples:
        "milk"
        "milk and eggs"
        "milk, eggs, and bread"
    """

    text = str(text).strip()

    text = re.sub(
        r"\s*,\s*and\s+",
        ", ",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\s+and\s+",
        ", ",
        text,
        flags=re.IGNORECASE,
    )

    parts = [
        item.strip(" ,.!?")
        for item in text.split(",")
    ]

    return [
        item
        for item in parts
        if item
    ]


def _extract_list_name(text, action=None):
    """
    Extract the target list name with action-aware patterns.

    The action-aware handling is important for commands such as:

        remove eggs from my grocery list

    where "eggs" is an item, not part of the list name.
    """

    normalized = str(text).strip()

    patterns = []

    if action == "add":
        patterns = [
            r"\badd\s+.+?\s+to\s+"
            r"(?:my\s+|the\s+|a\s+)?(.+?)\s+list\b",
        ]

    elif action == "remove":
        patterns = [
            r"\b(?:remove|delete)\s+.+?\s+from\s+"
            r"(?:my\s+|the\s+|a\s+)?(.+?)\s+list\b",
        ]

    elif action == "create":
        patterns = [
            r"\b(?:create|make)\s+"
            r"(?:a\s+|my\s+|the\s+)?(.+?)\s+list\b",
        ]

    elif action in {"show", "clear", "delete"}:
        action_word = {
            "show": r"(?:show|view|open)",
            "clear": r"clear",
            "delete": r"delete",
        }[action]

        patterns = [
            rf"\b{action_word}\s+(?:me\s+)?"
            rf"(?:my\s+|the\s+|a\s+)?(.+?)\s+list\b",
        ]

    # General fallback for simple phrases.
    patterns.extend(
        [
            r"\b(?:my\s+|the\s+)?(.+?)\s+list\b",
        ]
    )

    for pattern in patterns:
        match = re.search(
            pattern,
            normalized,
            flags=re.IGNORECASE,
        )

        if not match:
            continue

        candidate = match.group(1).strip()

        candidate = re.sub(
            r"^(?:me\s+|a\s+|my\s+|the\s+)",
            "",
            candidate,
            flags=re.IGNORECASE,
        )

        name = _normalize_list_name(
            candidate
        )

        if name:
            return name

    return None


def _detect_action(text):
    normalized = str(text).lower()

    if re.search(
        r"\b(?:create|make)\b",
        normalized,
    ):
        return "create"

    if re.search(
        r"\badd\b",
        normalized,
    ):
        return "add"

    if re.search(
        r"\b(?:remove|delete)\b.+\bfrom\b",
        normalized,
    ):
        return "remove"

    if re.search(
        r"\bclear\b",
        normalized,
    ):
        return "clear"

    if re.search(
        r"\bdelete\b",
        normalized,
    ):
        return "delete"

    if re.search(
        r"\b(?:show|view|open|what(?:'s| is) on)\b",
        normalized,
    ):
        return "show"

    return "show"


def _extract_items(text, action):
    text = str(text).strip()

    if action == "add":
        match = re.search(
            r"\badd\s+(.+?)\s+to\s+",
            text,
            flags=re.IGNORECASE,
        )

        if match:
            return _split_items(
                match.group(1)
            )

    if action == "remove":
        match = re.search(
            r"\b(?:remove|delete)\s+(.+?)\s+from\s+",
            text,
            flags=re.IGNORECASE,
        )

        if match:
            return _split_items(
                match.group(1)
            )

    return []


def handle_list_query(text):
    """
    Handle a natural-language persistent list request.
    """

    action = _detect_action(
        text
    )

    list_name = _extract_list_name(
        text,
        action=action,
    )

    if list_name is None:
        return {
            "success": False,
            "action": action,
            "response": (
                "I couldn't determine which list you meant."
            ),
            "error": "List name not detected.",
        }

    lists = _load_lists()

    display_name = _display_name(
        list_name
    )

    # --------------------------------------------------------
    # CREATE
    # --------------------------------------------------------

    if action == "create":

        if list_name in lists:
            return {
                "success": True,
                "action": action,
                "list_name": list_name,
                "items": lists[list_name],
                "response": (
                    f"Your {display_name} list already exists."
                ),
                "error": None,
            }

        lists[list_name] = []
        _save_lists(
            lists
        )

        return {
            "success": True,
            "action": action,
            "list_name": list_name,
            "items": [],
            "response": (
                f"I created your {display_name} list."
            ),
            "error": None,
        }

    # --------------------------------------------------------
    # ADD
    # --------------------------------------------------------

    if action == "add":

        items = _extract_items(
            text,
            action,
        )

        if not items:
            return {
                "success": False,
                "action": action,
                "list_name": list_name,
                "response": (
                    "I couldn't determine what you wanted to add."
                ),
                "error": "No list items detected.",
            }

        if list_name not in lists:
            lists[list_name] = []

        added = []

        existing_lower = {
            str(item).lower()
            for item in lists[list_name]
        }

        for item in items:
            if item.lower() not in existing_lower:
                lists[list_name].append(
                    item
                )
                existing_lower.add(
                    item.lower()
                )
                added.append(
                    item
                )

        _save_lists(
            lists
        )

        if not added:
            response = (
                f"Those items are already on your "
                f"{display_name} list."
            )
        else:
            response = (
                f"I added {', '.join(added)} to your "
                f"{display_name} list."
            )

        return {
            "success": True,
            "action": action,
            "list_name": list_name,
            "items": lists[list_name],
            "added": added,
            "response": response,
            "error": None,
        }

    # --------------------------------------------------------
    # REMOVE ITEM(S)
    # --------------------------------------------------------

    if action == "remove":

        if list_name not in lists:
            return {
                "success": False,
                "action": action,
                "list_name": list_name,
                "response": (
                    f"I couldn't find a {display_name} list."
                ),
                "error": "List does not exist.",
            }

        items = _extract_items(
            text,
            action,
        )

        if not items:
            return {
                "success": False,
                "action": action,
                "list_name": list_name,
                "response": (
                    "I couldn't determine what you wanted to remove."
                ),
                "error": "No list items detected.",
            }

        removed = []

        for requested_item in items:

            for existing_item in list(
                lists[list_name]
            ):

                if (
                    str(existing_item).lower()
                    == requested_item.lower()
                ):
                    lists[list_name].remove(
                        existing_item
                    )
                    removed.append(
                        existing_item
                    )
                    break

        _save_lists(
            lists
        )

        if removed:
            response = (
                f"I removed {', '.join(removed)} from your "
                f"{display_name} list."
            )
        else:
            response = (
                f"I couldn't find those items on your "
                f"{display_name} list."
            )

        return {
            "success": True,
            "action": action,
            "list_name": list_name,
            "items": lists[list_name],
            "removed": removed,
            "response": response,
            "error": None,
        }

    # --------------------------------------------------------
    # CLEAR ITEMS
    # --------------------------------------------------------

    if action == "clear":

        if list_name not in lists:
            return {
                "success": False,
                "action": action,
                "list_name": list_name,
                "response": (
                    f"I couldn't find a {display_name} list."
                ),
                "error": "List does not exist.",
            }

        lists[list_name] = []
        _save_lists(
            lists
        )

        return {
            "success": True,
            "action": action,
            "list_name": list_name,
            "items": [],
            "response": (
                f"I cleared your {display_name} list."
            ),
            "error": None,
        }

    # --------------------------------------------------------
    # DELETE LIST
    # --------------------------------------------------------

    if action == "delete":

        if list_name not in lists:
            return {
                "success": False,
                "action": action,
                "list_name": list_name,
                "response": (
                    f"I couldn't find a {display_name} list."
                ),
                "error": "List does not exist.",
            }

        del lists[list_name]

        _save_lists(
            lists
        )

        return {
            "success": True,
            "action": action,
            "list_name": list_name,
            "response": (
                f"I deleted your {display_name} list."
            ),
            "error": None,
        }

    # --------------------------------------------------------
    # SHOW
    # --------------------------------------------------------

    if list_name not in lists:
        return {
            "success": False,
            "action": "show",
            "list_name": list_name,
            "response": (
                f"I couldn't find a {display_name} list."
            ),
            "error": "List does not exist.",
        }

    items = lists[list_name]

    if not items:
        response = (
            f"Your {display_name} list is empty."
        )

    else:
        lines = [
            f"{display_name} list:"
        ]

        for index, item in enumerate(
            items,
            start=1,
        ):
            lines.append(
                f"{index}. {item}"
            )

        response = "\n".join(
            lines
        )

    return {
        "success": True,
        "action": "show",
        "list_name": list_name,
        "items": items,
        "response": response,
        "error": None,
    }

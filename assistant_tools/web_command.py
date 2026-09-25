"""Handle explicit webpage reading and web search requests."""

import re

from assistant_tools.web_access import WebAccessError, read_public_page
from assistant_tools.web_search import WebSearchError, search_web


def handle_web_read(text):
    text = str(text)

    search = re.fullmatch(
        r"\s*(?:search(?: the web)? for|look up)\s+(.+?)\s*",
        text,
        flags=re.IGNORECASE,
    )
    if search:
        try:
            results = search_web(search.group(1))
        except WebSearchError as error:
            return {
                "success": False,
                "domain": "web",
                "response": str(error),
                "data": None,
            }

        if not results:
            response = "I found no web results."
        else:
            response = "Web results: " + " ".join(
                f"{index}. {item['title']}. {item['description']}"
                for index, item in enumerate(results, 1)
            )
        return {
            "success": True,
            "domain": "web",
            "response": response,
            "data": {"query": search.group(1), "results": results},
        }

    read = re.fullmatch(
        r"\s*(?:read|open)\s+(https://\S+)\s*",
        text,
        flags=re.IGNORECASE,
    )
    if not read:
        return None

    try:
        page = read_public_page(read.group(1))
    except WebAccessError as error:
        return {
            "success": False,
            "domain": "web",
            "response": f"I couldn't read that page: {error}",
            "data": None,
        }

    excerpt = page["text"][:700].strip()
    return {
        "success": True,
        "domain": "web",
        "response": excerpt or "That page has no readable text.",
        "data": page,
    }

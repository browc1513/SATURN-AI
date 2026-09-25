"""Optional Brave web search for SATURN."""

import http.client
import json
import os
from urllib.parse import urlencode


class WebSearchError(RuntimeError):
    pass


def search_web(query, api_key=None):
    query = str(query).strip()
    if not query or len(query) > 400:
        raise WebSearchError("Search text must be 1–400 characters.")

    key = api_key if api_key is not None else os.getenv("SATURN_BRAVE_API_KEY")
    if not key:
        raise WebSearchError("Web search needs a Brave Search API key.")

    connection = http.client.HTTPSConnection(
        "api.search.brave.com", timeout=8
    )
    try:
        connection.request(
            "GET",
            "/res/v1/web/search?" + urlencode({"q": query, "count": 3}),
            headers={
                "X-Subscription-Token": key,
                "Accept": "application/json",
            },
        )
        response = connection.getresponse()
        if response.status != 200:
            raise WebSearchError(
                f"Search service returned HTTP {response.status}."
            )
        payload = response.read(200001)
        if len(payload) > 200000:
            raise WebSearchError("Search response is too large.")
        data = json.loads(payload)
    except (OSError, ValueError, http.client.HTTPException) as error:
        raise WebSearchError("Could not retrieve search results.") from error
    finally:
        connection.close()

    results = []
    for item in data.get("web", {}).get("results", [])[:3]:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title", "")).strip()
        url = str(item.get("url", "")).strip()
        description = str(item.get("description", "")).strip()
        if title and url.startswith("https://"):
            results.append({
                "title": title[:200],
                "url": url[:2000],
                "description": description[:500],
            })
    return results

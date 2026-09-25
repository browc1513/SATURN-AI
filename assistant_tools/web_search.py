"""Search the Pi's local SearXNG instance."""

import http.client
import json
from urllib.parse import urlencode


class WebSearchError(RuntimeError):
    pass


def search_web(query):
    query = str(query).strip()
    if not query or len(query) > 400:
        raise WebSearchError("Search text must be 1–400 characters.")

    connection = http.client.HTTPConnection("127.0.0.1", 8888, timeout=20)
    try:
        path = "/search?" + urlencode({"q": query, "format": "json"})
        connection.request("GET", path, headers={"Accept": "application/json"})
        response = connection.getresponse()
        if response.status != 200:
            raise WebSearchError(
                f"Local search returned HTTP {response.status}."
            )
        payload = response.read(500001)
        if len(payload) > 500000:
            raise WebSearchError("Search response is too large.")
        data = json.loads(payload)
        if not isinstance(data, dict):
            raise ValueError("Invalid search response")
    except (OSError, ValueError, http.client.HTTPException) as error:
        raise WebSearchError("Local search is unavailable.") from error
    finally:
        connection.close()

    results = []
    for item in data.get("results", []):
        if not isinstance(item, dict):
            continue
        title = str(item.get("title", "")).strip()
        url = str(item.get("url", "")).strip()
        description = str(item.get("content", "")).strip()
        if title and url.startswith("https://"):
            results.append({
                "title": title[:200],
                "url": url[:2000],
                "description": description[:500],
                "published": str(item.get("publishedDate") or "")[:80],
            })
        if len(results) == 5:
            break
    return results

import json
from unittest.mock import patch

import pytest

from assistant_tools.web_search import WebSearchError, search_web


class FakeResponse:
    status = 200

    def read(self, limit):
        assert limit == 500001
        return json.dumps({"results": [{
            "title": "FRC Research",
            "url": "https://example.org/frc",
            "content": "An FRC research overview.",
            "publishedDate": "2026-09-20",
        }]}).encode()


class FakeConnection:
    def __init__(self, host, port, timeout):
        assert (host, port, timeout) == ("127.0.0.1", 8888, 20)
        self.request_args = None

    def request(self, method, path, headers):
        self.request_args = (method, path, headers)

    def getresponse(self):
        return FakeResponse()

    def close(self):
        pass


def test_search_uses_local_endpoint_and_returns_sources():
    connection = FakeConnection("127.0.0.1", 8888, 20)
    with patch(
        "assistant_tools.web_search.http.client.HTTPConnection",
        return_value=connection,
    ):
        results = search_web("fusion research")

    method, path, headers = connection.request_args
    assert method == "GET"
    assert path == "/search?q=fusion+research&format=json"
    assert headers["Accept"] == "application/json"
    assert results[0]["url"] == "https://example.org/frc"
    assert results[0]["published"] == "2026-09-20"


def test_invalid_query_makes_no_request():
    with patch("assistant_tools.web_search.http.client.HTTPConnection") as client:
        with pytest.raises(WebSearchError):
            search_web("")
    client.assert_not_called()

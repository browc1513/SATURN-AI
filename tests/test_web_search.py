import json
from unittest.mock import patch

import pytest

from assistant_tools.web_search import WebSearchError, search_web


class FakeResponse:
    def __init__(self, status=200, payload=None):
        self.status = status
        self.payload = payload if payload is not None else {
            "web": {"results": [{
                "title": "Fusion Research",
                "url": "https://example.org/fusion",
                "description": "Research overview",
            }]}
        }

    def read(self, limit):
        assert limit == 200001
        return json.dumps(self.payload).encode()


class FakeConnection:
    def __init__(self, host, timeout):
        assert host == "api.search.brave.com"
        assert timeout == 8
        self.request_args = None
        self.response = FakeResponse()

    def request(self, method, path, headers):
        self.request_args = (method, path, headers)

    def getresponse(self):
        return self.response

    def close(self):
        pass


def test_search_uses_fixed_host_and_returns_sources():
    connection = FakeConnection("api.search.brave.com", 8)
    with patch(
        "assistant_tools.web_search.http.client.HTTPSConnection",
        return_value=connection,
    ):
        results = search_web("fusion research", api_key="test-key")

    method, path, headers = connection.request_args
    assert method == "GET"
    assert path.startswith("/res/v1/web/search?q=fusion+research&count=3")
    assert headers["X-Subscription-Token"] == "test-key"
    assert results[0]["url"] == "https://example.org/fusion"


def test_missing_key_makes_no_request(monkeypatch):
    monkeypatch.delenv("SATURN_BRAVE_API_KEY", raising=False)
    with patch("assistant_tools.web_search.http.client.HTTPSConnection") as client:
        with pytest.raises(WebSearchError, match="API key"):
            search_web("fusion")
    client.assert_not_called()


def test_http_error_does_not_return_results():
    connection = FakeConnection("api.search.brave.com", 8)
    connection.response = FakeResponse(status=429)
    with patch(
        "assistant_tools.web_search.http.client.HTTPSConnection",
        return_value=connection,
    ):
        with pytest.raises(WebSearchError, match="429"):
            search_web("fusion", api_key="test-key")

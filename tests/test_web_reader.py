from unittest.mock import patch

import pytest

from assistant_tools.web_access import WebAccessError, read_public_page


class Response:
    def __init__(self, status=200, headers=None, body=b""):
        self.status = status
        self.headers = headers or {}
        self.body = body

    def getheader(self, name, default=None):
        return self.headers.get(name, default)

    def read(self, size):
        return self.body[:size]


def reader(responses, validator):
    calls = []
    responses = iter(responses)

    class Connection:
        def __init__(self, host, ip, timeout):
            calls.append((host, ip, timeout))
            self.response = next(responses)

        def request(self, method, path, headers):
            assert method == "GET"
            assert headers["Accept-Encoding"] == "identity"

        def getresponse(self):
            return self.response

        def close(self):
            pass

    return calls, patch("assistant_tools.web_access._PinnedHTTPS", Connection), patch(
        "assistant_tools.web_access.validate_public_url", side_effect=validator
    )


def test_visible_html_is_extracted_with_validated_ip():
    calls, connection, validation = reader(
        [Response(headers={"Content-Type": "text/html"}, body=b"<h1>News</h1><script>secret</script><p>Article</p>")],
        [("example.org", "93.184.215.14")],
    )
    with connection, validation:
        result = read_public_page("https://example.org/story")
    assert result["text"] == "News\nArticle"
    assert calls == [("example.org", "93.184.215.14", 5)]


def test_redirect_is_validated_before_second_connection():
    calls, connection, validation = reader(
        [Response(status=302, headers={"Location": "https://127.0.0.1/private"})],
        [("example.org", "93.184.215.14"), WebAccessError("blocked")],
    )
    with connection, validation, pytest.raises(WebAccessError):
        read_public_page("https://example.org/")
    assert len(calls) == 1


def test_oversized_page_is_rejected():
    calls, connection, validation = reader(
        [Response(headers={"Content-Type": "text/html"}, body=b"a" * 11)],
        [("example.org", "93.184.215.14")],
    )
    with connection, validation, pytest.raises(WebAccessError, match="size"):
        read_public_page("https://example.org/", max_bytes=10)

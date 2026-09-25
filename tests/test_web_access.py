from unittest.mock import patch

import pytest

from assistant_tools.web_access import (
    WebAccessError,
    validate_public_url,
)


def dns_result(address):
    return [(2, 1, 6, "", (address, 443))]


def test_public_https_host_is_accepted():
    with patch(
        "assistant_tools.web_access.socket.getaddrinfo",
        return_value=dns_result("93.184.215.14"),
    ):
        assert validate_public_url(
            "https://example.org/article",
            allowed_domains=("example.org",),
        ) == ("example.org", "93.184.215.14")


@pytest.mark.parametrize(
    "url",
    [
        "http://example.org/",
        "file:///etc/passwd",
        "https://user:secret@example.org/",
        "https://example.org:8443/",
        "https://example.org/#fragment",
    ],
)
def test_unsafe_url_shapes_are_rejected(url):
    with pytest.raises(WebAccessError):
        validate_public_url(url)


@pytest.mark.parametrize(
    "address",
    ["127.0.0.1", "10.0.0.1", "169.254.169.254", "::1"],
)
def test_local_and_metadata_addresses_are_rejected(address):
    with patch(
        "assistant_tools.web_access.socket.getaddrinfo",
        return_value=dns_result(address),
    ):
        with pytest.raises(WebAccessError):
            validate_public_url("https://example.org/")


def test_disallowed_domain_is_rejected_before_dns():
    with patch(
        "assistant_tools.web_access.socket.getaddrinfo"
    ) as dns:
        with pytest.raises(WebAccessError):
            validate_public_url(
                "https://example.org.evil.test/",
                allowed_domains=("example.org",),
            )
    dns.assert_not_called()

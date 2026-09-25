"""Bounded HTTPS retrieval for public pages."""

import http.client
import ipaddress
import socket
import ssl
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit


class WebAccessError(ValueError):
    """The requested page cannot be safely retrieved."""


class _Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript", "svg", "template"}:
            self.hidden += 1
        elif tag in {"p", "div", "br", "li", "h1", "h2", "h3", "h4", "title"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript", "svg", "template"}:
            self.hidden = max(0, self.hidden - 1)
        elif tag in {"p", "div", "li", "h1", "h2", "h3", "h4", "title"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def validate_public_url(url, allowed_domains=None):
    if not isinstance(url, str) or not url or any(
        ord(c) < 33 or ord(c) == 127 for c in url
    ):
        raise WebAccessError("Invalid URL.")
    try:
        parsed = urlsplit(url)
        host = parsed.hostname
        port = parsed.port
    except ValueError as exc:
        raise WebAccessError("Invalid URL.") from exc
    if (parsed.scheme != "https" or not host or parsed.username is not None
            or parsed.password is not None or parsed.fragment or port not in (None, 443)):
        raise WebAccessError("Only public HTTPS URLs on port 443 are allowed.")
    host = host.rstrip(".").lower()
    if not host or "_" in host:
        raise WebAccessError("Invalid host.")
    if allowed_domains is not None:
        allowed = [str(d).strip().lower().lstrip(".").rstrip(".") for d in allowed_domains]
        if not any(d and (host == d or host.endswith("." + d)) for d in allowed):
            raise WebAccessError("This domain is not allowed.")
    try:
        addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        ips = [ipaddress.ip_address(item[4][0]) for item in addresses]
    except (socket.gaierror, ValueError) as exc:
        raise WebAccessError("The host could not be resolved.") from exc
    if not ips or any(not ip.is_global for ip in ips):
        raise WebAccessError("Private or reserved destinations are blocked.")
    return host, str(ips[0])


class _PinnedHTTPS(http.client.HTTPSConnection):
    def __init__(self, host, ip, timeout):
        super().__init__(host, port=443, timeout=timeout, context=ssl.create_default_context())
        self._validated_ip = ip

    def connect(self):
        sock = socket.create_connection((self._validated_ip, 443), self.timeout)
        try:
            self.sock = self._context.wrap_socket(sock, server_hostname=self.host)
        except BaseException:
            sock.close()
            raise


def read_public_page(url, allowed_domains=None, max_bytes=262144, max_redirects=3, timeout=5):
    """Return a bounded dict containing the final URL and visible HTML text."""
    if max_bytes < 1 or max_bytes > 1048576 or not 0 <= max_redirects <= 5 or not 0 < timeout <= 15:
        raise ValueError("Invalid retrieval limits.")
    current = url
    for hop in range(max_redirects + 1):
        host, ip = validate_public_url(current, allowed_domains)
        parsed = urlsplit(current)
        path = parsed.path or "/"
        if parsed.query:
            path += "?" + parsed.query
        conn = _PinnedHTTPS(host, ip, timeout)
        try:
            conn.request("GET", path, headers={"User-Agent": "SATURN/1.0", "Accept": "text/html", "Accept-Encoding": "identity"})
            response = conn.getresponse()
            if response.status in (301, 302, 303, 307, 308):
                destination = response.getheader("Location")
                if not destination or hop == max_redirects:
                    raise WebAccessError("Redirect limit reached or location missing.")
                current = urljoin(current, destination)
                continue
            if response.status != 200:
                raise WebAccessError(f"Page returned HTTP {response.status}.")
            if response.getheader("Content-Type", "").split(";", 1)[0].strip().lower() not in {"text/html", "application/xhtml+xml"}:
                raise WebAccessError("Only HTML pages are supported.")
            if response.getheader("Content-Encoding", "identity").lower() != "identity":
                raise WebAccessError("Compressed pages are not supported.")
            data = response.read(max_bytes + 1)
            if len(data) > max_bytes:
                raise WebAccessError("Page exceeds the size limit.")
        except (OSError, ssl.SSLError, http.client.HTTPException) as exc:
            raise WebAccessError("Page retrieval failed.") from exc
        finally:
            conn.close()
        parser = _Text()
        parser.feed(data.decode("utf-8", errors="replace"))
        content = "\n".join(" ".join(line.split()) for line in "".join(parser.parts).splitlines() if line.strip())
        return {"url": current, "text": content[:20000], "truncated": len(content) > 20000}
    raise WebAccessError("Redirect limit reached.")

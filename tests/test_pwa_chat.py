from pathlib import Path


PWA_DIRECTORY = Path("pwa")


def read_pwa_file(name):
    return (
        PWA_DIRECTORY
        .joinpath(name)
        .read_text(encoding="utf-8")
    )


def test_chat_controls_exist():
    html = read_pwa_file("index.html")

    expected_ids = [
        'id="chat-button"',
        'id="chat-view"',
        'id="chat-back-button"',
        'id="chat-messages"',
        'id="chat-form"',
        'id="chat-input"',
        'id="chat-send-button"',
    ]

    for expected_id in expected_ids:
        assert expected_id in html


def test_chat_uses_persistent_browser_session():
    javascript = read_pwa_file("app.js")

    assert "localStorage.getItem" in javascript
    assert "localStorage.setItem" in javascript
    assert "saturn-conversation-session-id" in javascript
    assert "randomUUID" in javascript


def test_chat_sends_session_to_query_api():
    javascript = read_pwa_file("app.js")

    assert '"/api/query"' in javascript
    assert "session_id:" in javascript
    assert "getConversationSessionId()" in javascript


def test_chat_renders_response_as_text():
    javascript = read_pwa_file("app.js")

    assert "contentElement.textContent = message;" in javascript
    assert "innerHTML = message" not in javascript


def test_service_worker_uses_v4_cache():
    service_worker = read_pwa_file(
        "service-worker.js"
    )

    assert 'CACHE_NAME = "saturn-pwa-v4"' in (
        service_worker
    )


def test_pwa_assets_use_matching_v4_cache_urls():
    index = Path(
        "pwa/index.html"
    ).read_text(encoding="utf-8")

    worker = Path(
        "pwa/service-worker.js"
    ).read_text(encoding="utf-8")

    assert 'href="/app/style.css?v=4"' in index
    assert 'src="/app/app.js?v=4"' in index
    assert 'saturn-pwa-v4' in worker
    assert '"/app/style.css?v=4"' in worker
    assert '"/app/app.js?v=4"' in worker
    assert (
        'fetch(event.request, { cache: "no-store" })'
        in worker
    )

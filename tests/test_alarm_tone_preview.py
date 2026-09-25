from pathlib import Path

import pytest
from fastapi import HTTPException

import api.saturn_api as saturn_api


PWA_DIRECTORY = Path("pwa")


def read_pwa_file(filename):
    return (
        PWA_DIRECTORY
        / filename
    ).read_text(
        encoding="utf-8"
    )


def test_preview_endpoint_returns_discovered_wav(
    monkeypatch,
):
    tone = {
        "name": "Morning Tone",
        "filename": "Morning Tone.wav",
        "path": "/tmp/Morning Tone.wav",
    }

    monkeypatch.setattr(
        saturn_api,
        "resolve_alarm_tone",
        lambda name: (
            tone
            if name == "Morning Tone"
            else None
        ),
    )

    response = saturn_api.preview_alarm_tone(
        "Morning Tone"
    )

    assert str(response.path) == tone["path"]
    assert response.media_type == "audio/wav"
    assert response.headers["cache-control"] == "no-store"


def test_preview_endpoint_rejects_unknown_tone(
    monkeypatch,
):
    monkeypatch.setattr(
        saturn_api,
        "resolve_alarm_tone",
        lambda name: None,
    )

    with pytest.raises(
        HTTPException,
        match="Alarm tone not found",
    ) as error:
        saturn_api.preview_alarm_tone(
            "Missing Tone"
        )

    assert error.value.status_code == 404


def test_pwa_only_exposes_selector_and_preview():
    index = read_pwa_file(
        "index.html"
    )

    assert 'id="alarm-tone-select"' in index
    assert 'id="preview-alarm-tone-button"' in index
    assert "Preview Tone" in index

    assert 'id="alarm-tone-file"' not in index
    assert 'id="upload-alarm-tone-button"' not in index
    assert 'id="rename-alarm-tone-button"' not in index
    assert 'id="delete-alarm-tone-button"' not in index


def test_pwa_preview_plays_on_browser_device():
    script = read_pwa_file(
        "app.js"
    )

    assert (
        "async function "
        "previewSelectedAlarmTone()"
        in script
    )
    assert (
        "alarmToneSelect.dataset.defaultTone"
        in script
    )
    assert "new Audio(" in script
    assert (
        '"/api/alarm-tones/"'
        in script
    )
    assert "encodeURIComponent(toneName)" in script
    assert "await audio.play()" in script


def test_pwa_uses_v10_assets():
    index = read_pwa_file(
        "index.html"
    )
    worker = read_pwa_file(
        "service-worker.js"
    )

    assert 'href="/app/style.css?v=10"' in index
    assert 'src="/app/app.js?v=10"' in index
    assert 'CACHE_NAME = "saturn-pwa-v10"' in worker
    assert '"/app/style.css?v=10"' in worker
    assert '"/app/app.js?v=10"' in worker

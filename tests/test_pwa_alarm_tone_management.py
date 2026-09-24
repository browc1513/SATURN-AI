from pathlib import Path


PWA_DIRECTORY = Path("pwa")


def read_pwa_file(filename):
    return (
        PWA_DIRECTORY
        / filename
    ).read_text(
        encoding="utf-8"
    )


def test_pwa_exposes_alarm_tone_management_controls():
    index = read_pwa_file(
        "index.html"
    )

    expected_ids = [
        "alarm-tone-file",
        "upload-alarm-tone-button",
        "preview-alarm-tone-button",
        "rename-alarm-tone-button",
        "delete-alarm-tone-button",
        "alarm-tone-status",
    ]

    for element_id in expected_ids:
        assert f'id="{element_id}"' in index

    assert 'accept=".wav,audio/wav"' in index
    assert "Preview plays on" in index
    assert "this device" in index


def test_pwa_uploads_raw_wav_audio():
    script = read_pwa_file(
        "app.js"
    )

    assert "async function uploadAlarmTone()" in script
    assert 'method: "POST"' in script
    assert '"Content-Type": "audio/wav"' in script
    assert "await file.arrayBuffer()" in script
    assert (
        '"/api/alarm-tones?name="'
        in script
    )
    assert "encodeURIComponent(toneName)" in script


def test_pwa_previews_selected_tone_on_device():
    script = read_pwa_file(
        "app.js"
    )

    assert (
        "async function "
        "previewSelectedAlarmTone()"
        in script
    )
    assert "new Audio(" in script
    assert "await audio.play()" in script
    assert (
        "Preview started on this device."
        in script
    )


def test_pwa_renames_and_deletes_custom_tones():
    script = read_pwa_file(
        "app.js"
    )

    assert (
        "async function "
        "renameSelectedAlarmTone()"
        in script
    )
    assert (
        "async function "
        "deleteSelectedAlarmTone()"
        in script
    )
    assert 'method: "PATCH"' in script
    assert 'method: "DELETE"' in script
    assert "window.prompt(" in script
    assert "window.confirm(" in script


def test_pwa_protects_default_tone_controls():
    script = read_pwa_file(
        "app.js"
    )

    assert (
        "alarmToneSelect.dataset.defaultTone"
        in script
    )
    assert (
        "selectedTone === defaultTone"
        in script
    )
    assert (
        "renameAlarmToneButton.disabled "
        "= defaultSelected"
        in script
    )
    assert (
        "deleteAlarmToneButton.disabled "
        "= defaultSelected"
        in script
    )
    assert (
        "The default alarm tone cannot be renamed."
        in script
    )
    assert (
        "The default alarm tone cannot be deleted."
        in script
    )


def test_pwa_tone_manager_has_dedicated_styles():
    styles = read_pwa_file(
        "style.css"
    )

    assert ".alarm-tone-manager" in styles
    assert ".alarm-tone-actions" in styles
    assert ".alarm-tone-status" in styles


def test_pwa_tone_management_uses_v7_assets():
    index = read_pwa_file(
        "index.html"
    )
    worker = read_pwa_file(
        "service-worker.js"
    )

    assert 'href="/app/style.css?v=7"' in index
    assert 'src="/app/app.js?v=7"' in index
    assert 'CACHE_NAME = "saturn-pwa-v7"' in worker
    assert '"/app/style.css?v=7"' in worker
    assert '"/app/app.js?v=7"' in worker

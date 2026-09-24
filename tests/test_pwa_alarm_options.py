from pathlib import Path


PWA_DIRECTORY = Path("pwa")


def read_pwa_file(filename):
    return (
        PWA_DIRECTORY
        / filename
    ).read_text(
        encoding="utf-8"
    )


def test_alarm_form_exposes_tone_and_mode_options():
    index = read_pwa_file(
        "index.html"
    )

    assert 'id="alarm-tone-select"' in index
    assert 'id="alarm-playback-mode"' in index
    assert 'value="until_dismissed"' in index
    assert 'value="timed"' in index
    assert 'id="alarm-duration-container"' in index
    assert 'id="alarm-duration-seconds"' in index
    assert 'min="5"' in index
    assert 'max="1800"' in index
    assert 'value="30"' in index


def test_pwa_loads_safe_alarm_tone_inventory():
    script = read_pwa_file(
        "app.js"
    )

    assert 'async function loadAlarmTones()' in script
    assert '"/api/alarm-tones"' in script
    assert 'cache: "no-store"' in script
    assert "tone.name" in script
    assert "tone.filename" in script
    assert "tone.path" not in script


def test_pwa_submits_alarm_playback_policy():
    script = read_pwa_file(
        "app.js"
    )

    assert "playback_mode: playbackMode" in script
    assert (
        "playback_duration_seconds:"
        in script
    )
    assert 'playbackMode === "timed"' in script
    assert "durationSeconds < 5" in script
    assert "durationSeconds > 1800" in script


def test_duration_control_tracks_selected_mode():
    script = read_pwa_file(
        "app.js"
    )

    assert (
        "function updateAlarmDurationVisibility()"
        in script
    )
    assert (
        'alarmPlaybackMode.addEventListener('
        in script
    )
    assert (
        'alarmDurationContainer.classList.toggle('
        in script
    )
    assert (
        "alarmDurationSeconds.disabled = !timed"
        in script
    )


def test_alarm_view_loads_alarms_and_tones():
    script = read_pwa_file(
        "app.js"
    )

    assert "await Promise.all([" in script
    assert "loadAlarms()," in script
    assert "loadAlarmTones()," in script


def test_pwa_uses_atomic_v5_assets():
    index = read_pwa_file(
        "index.html"
    )
    worker = read_pwa_file(
        "service-worker.js"
    )

    assert 'href="/app/style.css?v=5"' in index
    assert 'src="/app/app.js?v=5"' in index
    assert 'CACHE_NAME = "saturn-pwa-v5"' in worker
    assert '"/app/style.css?v=5"' in worker
    assert '"/app/app.js?v=5"' in worker

    assert "saturn-pwa-v4" not in worker
    assert "style.css?v=4" not in index
    assert "app.js?v=4" not in index

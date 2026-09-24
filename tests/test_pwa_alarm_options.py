from pathlib import Path


PWA_DIRECTORY = Path("pwa")


def read_pwa_file(filename):
    return (
        PWA_DIRECTORY
        / filename
    ).read_text(
        encoding="utf-8"
    )


def test_alarm_form_exposes_two_simple_types():
    index = read_pwa_file(
        "index.html"
    )

    assert 'id="alarm-tone-select"' in index
    assert 'id="alarm-type-select"' in index
    assert 'value="wake_up"' in index
    assert 'value="reminder"' in index
    assert "Wake-up alarm" in index
    assert "Reminder" in index
    assert "10 seconds" in index

    assert 'id="alarm-playback-mode"' not in index
    assert 'id="alarm-duration-container"' not in index
    assert 'id="alarm-duration-seconds"' not in index


def test_pwa_loads_default_and_additional_tones():
    script = read_pwa_file(
        "app.js"
    )

    assert 'async function loadAlarmTones()' in script
    assert '"/api/alarm-tones"' in script
    assert 'cache: "no-store"' in script
    assert "result.default_tone" in script
    assert '"Saturn Alarm 1"' in script
    assert "`${defaultTone} (Default)`" in script
    assert "tone.name === defaultTone" in script
    assert "tone.filename" in script
    assert "tone.path" not in script


def test_pwa_submits_simple_alarm_type():
    script = read_pwa_file(
        "app.js"
    )

    assert "alarm_type: alarmType" in script
    assert "alarmTypeSelect.value" in script
    assert "playback_mode:" not in script
    assert "playback_duration_seconds:" not in script
    assert "updateAlarmDurationVisibility" not in script
    assert "alarmDurationSeconds" not in script


def test_alarm_view_loads_alarms_and_tones():
    script = read_pwa_file(
        "app.js"
    )

    assert "await Promise.all([" in script
    assert "loadAlarms()," in script
    assert "loadAlarmTones()," in script


def test_pwa_uses_atomic_v6_assets():
    index = read_pwa_file(
        "index.html"
    )
    worker = read_pwa_file(
        "service-worker.js"
    )

    assert 'href="/app/style.css?v=6"' in index
    assert 'src="/app/app.js?v=6"' in index
    assert 'CACHE_NAME = "saturn-pwa-v6"' in worker
    assert '"/app/style.css?v=6"' in worker
    assert '"/app/app.js?v=6"' in worker

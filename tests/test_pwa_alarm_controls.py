from pathlib import Path
from unittest.mock import patch

from api.saturn_api import (
    snooze_ringing_alarm,
    stop_ringing_alarm,
)


def alarm_result(action, response):
    return {
        "success": True,
        "domain": "alarms",
        "response": response,
        "data": {
            "action": action,
        },
    }


def test_stop_alarm_endpoint_uses_saturn_query():
    expected = alarm_result(
        "stop",
        "Alarm stopped.",
    )

    with patch(
        "api.saturn_api.run_saturn_query",
        return_value=expected,
    ) as mocked_query:
        response = stop_ringing_alarm()

    mocked_query.assert_called_once_with(
        "stop the alarm"
    )
    assert response == {
        "success": True,
        "result": expected,
    }


def test_snooze_endpoint_uses_ten_minutes():
    expected = alarm_result(
        "snooze",
        "Alarm snoozed for 10 minutes.",
    )

    with patch(
        "api.saturn_api.run_saturn_query",
        return_value=expected,
    ) as mocked_query:
        response = snooze_ringing_alarm()

    mocked_query.assert_called_once_with(
        "snooze the alarm for 10 minutes"
    )
    assert response == {
        "success": True,
        "result": expected,
    }


def test_pwa_contains_alarm_control_buttons():
    index = Path(
        "pwa/index.html"
    ).read_text(encoding="utf-8")

    assert 'id="snooze-alarm-button"' in index
    assert "Snooze 10 Minutes" in index
    assert 'id="stop-alarm-button"' in index
    assert "Stop Alarm" in index


def test_pwa_connects_alarm_controls_to_api():
    app = Path(
        "pwa/app.js"
    ).read_text(encoding="utf-8")

    assert '"/api/alarms/' not in app
    assert "`/api/alarms/${action}`" in app
    assert '"snooze"' in app
    assert '"stop"' in app


def test_pwa_alarm_controls_use_v4_assets():
    index = Path(
        "pwa/index.html"
    ).read_text(encoding="utf-8")

    worker = Path(
        "pwa/service-worker.js"
    ).read_text(encoding="utf-8")

    assert 'app.js?v=4' in index
    assert 'style.css?v=4' in index
    assert 'saturn-pwa-v4' in worker
    assert 'app.js?v=4' in worker
    assert 'style.css?v=4' in worker

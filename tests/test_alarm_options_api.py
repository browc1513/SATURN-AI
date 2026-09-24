from unittest.mock import patch

import pytest
from pydantic import ValidationError

from api import saturn_api


def test_alarm_tone_endpoint_hides_internal_paths():
    discovered = [
        {
            "name": "Saturn Alarm 1",
            "filename": "Saturn Alarm 1.wav",
            "path": "/private/Saturn Alarm 1.wav",
        },
        {
            "name": "Zen Gong",
            "filename": "Zen_Gong.wav",
            "path": "/private/Zen_Gong.wav",
        },
    ]

    with patch.object(
        saturn_api,
        "DEFAULT_ALARM_TONE_NAME",
        "Saturn Alarm 1",
    ), patch.object(
        saturn_api,
        "list_alarm_tones",
        return_value=discovered,
    ):
        result = saturn_api.get_alarm_tones()

    assert result == {
        "success": True,
        "default_tone": "Saturn Alarm 1",
        "tones": [
            {
                "name": "Saturn Alarm 1",
                "filename": "Saturn Alarm 1.wav",
            },
            {
                "name": "Zen Gong",
                "filename": "Zen_Gong.wav",
            },
        ],
    }

    assert all(
        "path" not in tone
        for tone in result["tones"]
    )


def test_create_wake_up_alarm_query():
    request = saturn_api.AlarmCreateRequest(
        time="8:30 AM",
        tone="Zen Gong",
        alarm_type="wake_up",
    )

    expected_result = {
        "success": True,
        "domain": "alarms",
    }

    with patch.object(
        saturn_api,
        "run_saturn_query",
        return_value=expected_result,
    ) as mocked_query:
        response = saturn_api.create_alarm(
            request
        )

    mocked_query.assert_called_once_with(
        "set an alarm for 8:30 AM "
        "with the Zen Gong tone "
        "until dismissed"
    )

    assert response["success"] is True


def test_create_reminder_query_is_fixed_at_ten_seconds():
    request = saturn_api.AlarmCreateRequest(
        time="9:15 AM",
        tone="Morning Bell",
        alarm_type="reminder",
    )

    with patch.object(
        saturn_api,
        "run_saturn_query",
        return_value={
            "success": True,
        },
    ) as mocked_query:
        response = saturn_api.create_alarm(
            request
        )

    mocked_query.assert_called_once_with(
        "remind me at 9:15 AM "
        "with the Morning Bell tone "
        "for 10 seconds"
    )

    assert response["success"] is True


def test_wake_up_is_default_alarm_type():
    request = saturn_api.AlarmCreateRequest(
        time="7 AM",
    )

    with patch.object(
        saturn_api,
        "run_saturn_query",
        return_value={
            "success": True,
        },
    ) as mocked_query:
        saturn_api.create_alarm(
            request
        )

    mocked_query.assert_called_once_with(
        "set an alarm for 7 AM until dismissed"
    )


@pytest.mark.parametrize(
    "alarm_type",
    [
        "timed",
        "until_dismissed",
        "forever",
        "",
    ],
)
def test_api_rejects_unknown_user_alarm_type(
    alarm_type,
):
    with pytest.raises(
        ValidationError
    ):
        saturn_api.AlarmCreateRequest(
            time="7 AM",
            alarm_type=alarm_type,
        )


def test_alarm_time_cannot_be_empty():
    with pytest.raises(
        ValidationError
    ):
        saturn_api.AlarmCreateRequest(
            time="",
        )

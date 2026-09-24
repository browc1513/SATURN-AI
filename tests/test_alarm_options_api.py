from unittest.mock import patch

import pytest
from pydantic import ValidationError

from api import saturn_api


def test_alarm_tone_endpoint_hides_internal_paths():
    discovered = [
        {
            "name": "Zen Gong",
            "filename": "Zen_Gong.wav",
            "path": "/private/runtime/Zen_Gong.wav",
        },
    ]

    with patch.object(
        saturn_api,
        "list_alarm_tones",
        return_value=discovered,
    ):
        result = saturn_api.get_alarm_tones()

    assert result == {
        "success": True,
        "tones": [
            {
                "name": "Zen Gong",
                "filename": "Zen_Gong.wav",
            },
        ],
    }

    assert "path" not in result["tones"][0]


def test_create_persistent_alarm_query():
    request = saturn_api.AlarmCreateRequest(
        time="8:30 AM",
        tone="Zen Gong",
        playback_mode="until_dismissed",
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
    assert response["result"] == expected_result


def test_create_timed_alarm_query():
    request = saturn_api.AlarmCreateRequest(
        time="9:15 AM",
        tone="Morning Bell",
        playback_mode="timed",
        playback_duration_seconds=45,
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
        "set an alarm for 9:15 AM "
        "with the Morning Bell tone "
        "for 45 seconds"
    )

    assert response["success"] is True


def test_timed_alarm_defaults_to_thirty_seconds():
    request = saturn_api.AlarmCreateRequest(
        time="7 AM",
        playback_mode="timed",
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
        "set an alarm for 7 AM for 30 seconds"
    )


def test_persistent_alarm_does_not_include_duration():
    request = saturn_api.AlarmCreateRequest(
        time="7 AM",
        playback_mode="until_dismissed",
        playback_duration_seconds=45,
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
    "duration",
    [
        4,
        1801,
    ],
)
def test_api_rejects_invalid_timed_duration(
    duration,
):
    with pytest.raises(
        ValidationError
    ):
        saturn_api.AlarmCreateRequest(
            time="7 AM",
            playback_mode="timed",
            playback_duration_seconds=duration,
        )


def test_api_rejects_unknown_playback_mode():
    with pytest.raises(
        ValidationError
    ):
        saturn_api.AlarmCreateRequest(
            time="7 AM",
            playback_mode="forever",
        )


def test_alarm_time_cannot_be_empty():
    with pytest.raises(
        ValidationError
    ):
        saturn_api.AlarmCreateRequest(
            time="",
        )

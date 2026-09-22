from unittest.mock import Mock, patch

import pytest

from assistant_tools.reboot_control import (
    REBOOT_COMMAND,
    RebootController,
)
from core.saturn_personality import SATURN


class ManualClock:
    def __init__(self):
        self.value = 100.0

    def __call__(self):
        return self.value

    def advance(self, seconds):
        self.value += seconds


@pytest.fixture
def enabled_controller():
    return RebootController(
        enabled=True,
        executor=Mock(),
        reboot_delay_seconds=0,
    )


def test_reboot_is_disabled_by_default():
    controller = RebootController()

    assert controller.enabled is False
    assert controller.request_confirmation() == {
        "status": "disabled",
        "expires_in_seconds": None,
    }


def test_reboot_command_is_fixed():
    assert REBOOT_COMMAND == (
        "/usr/bin/sudo",
        "-n",
        "/usr/bin/systemctl",
        "reboot",
    )


def test_reboot_requires_confirmation(
    enabled_controller,
):
    request = (
        enabled_controller.request_confirmation(
            "phone-a"
        )
    )

    assert request == {
        "status": "pending",
        "expires_in_seconds": 30,
    }
    assert enabled_controller.has_pending_confirmation(
        "phone-a"
    )


def test_confirmation_is_session_scoped(
    enabled_controller,
):
    enabled_controller.request_confirmation(
        "phone-a"
    )

    assert enabled_controller.confirm(
        "phone-b"
    ) == {
        "status": "missing",
    }
    assert enabled_controller.confirm(
        "phone-a"
    ) == {
        "status": "confirmed",
    }


def test_confirmation_expires():
    clock = ManualClock()
    controller = RebootController(
        enabled=True,
        executor=Mock(),
        confirmation_seconds=30,
        clock=clock,
    )

    controller.request_confirmation(
        "voice"
    )
    clock.advance(31)

    assert controller.confirm(
        "voice"
    ) == {
        "status": "expired",
    }


def test_confirmation_can_be_cancelled(
    enabled_controller,
):
    enabled_controller.request_confirmation(
        "phone-a"
    )

    assert enabled_controller.cancel(
        "phone-a"
    ) is True
    assert enabled_controller.confirm(
        "phone-a"
    ) == {
        "status": "missing",
    }


@pytest.mark.parametrize(
    "query",
    [
        "Reboot Saturn",
        "Restart Saturn",
        "Reboot the Pi",
        "Restart the Pi",
        "Reboot Raspberry Pi",
        "Restart Raspberry Pi",
        "Reboot yourself",
    ],
)
def test_saturn_requests_reboot_confirmation(
    enabled_controller,
    query,
):
    saturn = SATURN(
        start_alarm_monitor=False
    )
    saturn.reboot_controller = (
        enabled_controller
    )

    result = saturn.handle_query(
        query,
        session_id="phone-a",
    )

    assert result["success"] is True
    assert result["domain"] == "control"
    assert result["data"]["action"] == (
        "reboot_requested"
    )
    assert enabled_controller.has_pending_confirmation(
        "phone-a"
    )


def test_saturn_confirms_reboot_for_same_session(
    enabled_controller,
):
    saturn = SATURN(
        start_alarm_monitor=False
    )
    saturn.reboot_controller = (
        enabled_controller
    )

    saturn.handle_query(
        "Reboot Saturn",
        session_id="phone-a",
    )

    with patch.object(
        enabled_controller,
        "schedule_reboot",
    ) as mocked_schedule:
        result = saturn.handle_query(
            "Confirm reboot",
            session_id="phone-a",
        )

    assert result["success"] is True
    assert result["data"]["action"] == (
        "reboot_confirmed"
    )
    mocked_schedule.assert_called_once_with()


def test_other_session_cannot_confirm_reboot(
    enabled_controller,
):
    saturn = SATURN(
        start_alarm_monitor=False
    )
    saturn.reboot_controller = (
        enabled_controller
    )

    saturn.handle_query(
        "Reboot Saturn",
        session_id="phone-a",
    )

    with patch.object(
        enabled_controller,
        "schedule_reboot",
    ) as mocked_schedule:
        result = saturn.handle_query(
            "Confirm reboot",
            session_id="phone-b",
        )

    assert result["success"] is False
    assert result["data"]["action"] == (
        "reboot_not_pending"
    )
    mocked_schedule.assert_not_called()


def test_never_mind_cancels_pending_reboot(
    enabled_controller,
):
    saturn = SATURN(
        start_alarm_monitor=False
    )
    saturn.reboot_controller = (
        enabled_controller
    )

    saturn.handle_query(
        "Reboot Saturn",
        session_id="voice",
    )

    result = saturn.handle_query(
        "Never mind",
        session_id="voice",
    )

    assert result["success"] is True
    assert result["response"] == (
        "Okay, reboot cancelled."
    )
    assert result["data"]["action"] == (
        "reboot_cancelled"
    )
    assert not enabled_controller.has_pending_confirmation(
        "voice"
    )


def test_explicit_cancel_reboot(
    enabled_controller,
):
    saturn = SATURN(
        start_alarm_monitor=False
    )
    saturn.reboot_controller = (
        enabled_controller
    )

    saturn.handle_query(
        "Reboot Saturn",
        session_id="phone-a",
    )

    result = saturn.handle_query(
        "Cancel reboot",
        session_id="phone-a",
    )

    assert result["success"] is True
    assert result["data"]["action"] == (
        "reboot_cancelled"
    )


def test_confirm_without_request_does_not_reboot(
    enabled_controller,
):
    saturn = SATURN(
        start_alarm_monitor=False
    )
    saturn.reboot_controller = (
        enabled_controller
    )

    with patch.object(
        enabled_controller,
        "schedule_reboot",
    ) as mocked_schedule:
        result = saturn.handle_query(
            "Confirm reboot",
            session_id="phone-a",
        )

    assert result["success"] is False
    assert result["data"]["action"] == (
        "reboot_not_pending"
    )
    mocked_schedule.assert_not_called()


def test_disabled_saturn_does_not_request_reboot():
    saturn = SATURN(
        start_alarm_monitor=False
    )

    result = saturn.handle_query(
        "Reboot Saturn",
        session_id="phone-a",
    )

    assert result["success"] is False
    assert result["data"]["action"] == (
        "reboot_disabled"
    )


def test_reboot_phrases_never_reach_local_model(
    enabled_controller,
):
    saturn = SATURN(
        start_alarm_monitor=False
    )
    saturn.reboot_controller = (
        enabled_controller
    )

    with patch.object(
        saturn,
        "_handle_unknown_query",
    ) as mocked_unknown:
        saturn.handle_query(
            "Reboot Saturn",
            session_id="phone-a",
        )
        saturn.handle_query(
            "Confirm reboot",
            session_id="phone-a",
        )

    mocked_unknown.assert_not_called()

"""
Restricted reboot control for SATURN.

This module never accepts a user-provided command. On an explicitly
enabled Linux deployment, it can only execute the fixed Raspberry Pi
reboot command after SATURN's confirmation workflow approves it.
"""

import os
import subprocess
import sys
import threading
import time


REBOOT_COMMAND = (
    "/usr/bin/sudo",
    "-n",
    "/usr/bin/systemctl",
    "reboot",
)

TRUE_VALUES = {
    "1",
    "true",
    "yes",
    "on",
}

FALSE_VALUES = {
    "0",
    "false",
    "no",
    "off",
    "",
}


def _environment_enabled():
    raw_value = os.environ.get(
        "SATURN_REBOOT_ENABLED",
        "false",
    )

    normalized = raw_value.strip().lower()

    if normalized in TRUE_VALUES:
        return True

    if normalized in FALSE_VALUES:
        return False

    raise ValueError(
        "SATURN_REBOOT_ENABLED must be true or false."
    )


def _execute_system_reboot():
    subprocess.run(
        list(REBOOT_COMMAND),
        check=True,
        timeout=15,
        capture_output=True,
        text=True,
    )


class RebootController:
    """
    Maintain session-scoped reboot confirmations.

    Confirmation state intentionally remains in memory. Restarting
    SATURN automatically destroys any pending reboot request.
    """

    def __init__(
        self,
        enabled=None,
        confirmation_seconds=30,
        reboot_delay_seconds=5,
        executor=None,
        clock=None,
    ):
        if enabled is None:
            enabled = _environment_enabled()

        if confirmation_seconds <= 0:
            raise ValueError(
                "confirmation_seconds must be positive."
            )

        if reboot_delay_seconds < 0:
            raise ValueError(
                "reboot_delay_seconds cannot be negative."
            )

        self.executor = (
            executor
            if executor is not None
            else _execute_system_reboot
        )
        self.clock = (
            clock
            if clock is not None
            else time.monotonic
        )

        # Real reboot execution is Linux-only. Tests may supply a
        # harmless executor on another platform.
        platform_supported = (
            sys.platform.startswith("linux")
            or executor is not None
        )

        self.enabled = bool(
            enabled
            and platform_supported
        )
        self.confirmation_seconds = float(
            confirmation_seconds
        )
        self.reboot_delay_seconds = float(
            reboot_delay_seconds
        )
        self._pending = {}
        self._lock = threading.RLock()

    @staticmethod
    def _session_key(session_id):
        if session_id is None:
            return "default"

        normalized = str(
            session_id
        ).strip()

        return normalized or "default"

    def request_confirmation(
        self,
        session_id=None,
    ):
        if not self.enabled:
            return {
                "status": "disabled",
                "expires_in_seconds": None,
            }

        session_key = self._session_key(
            session_id
        )

        with self._lock:
            self._pending[session_key] = (
                self.clock()
                + self.confirmation_seconds
            )

        return {
            "status": "pending",
            "expires_in_seconds": int(
                self.confirmation_seconds
            ),
        }

    def confirm(
        self,
        session_id=None,
    ):
        session_key = self._session_key(
            session_id
        )

        with self._lock:
            deadline = self._pending.pop(
                session_key,
                None,
            )

        if deadline is None:
            return {
                "status": "missing",
            }

        if self.clock() > deadline:
            return {
                "status": "expired",
            }

        return {
            "status": "confirmed",
        }

    def cancel(
        self,
        session_id=None,
    ):
        session_key = self._session_key(
            session_id
        )

        with self._lock:
            deadline = self._pending.pop(
                session_key,
                None,
            )

        if deadline is None:
            return False

        return self.clock() <= deadline

    def has_pending_confirmation(
        self,
        session_id=None,
    ):
        session_key = self._session_key(
            session_id
        )

        with self._lock:
            deadline = self._pending.get(
                session_key
            )

            if deadline is None:
                return False

            if self.clock() > deadline:
                self._pending.pop(
                    session_key,
                    None,
                )
                return False

            return True

    def schedule_reboot(self):
        if not self.enabled:
            raise RuntimeError(
                "Reboot control is not enabled."
            )

        timer = threading.Timer(
            self.reboot_delay_seconds,
            self._run_reboot,
        )
        timer.daemon = True
        timer.name = "SATURNReboot"
        timer.start()

        return timer

    def _run_reboot(self):
        try:
            self.executor()
        except Exception as error:
            print(
                "S.A.T.U.R.N. reboot warning: "
                f"{error}"
            )

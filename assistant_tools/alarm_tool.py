"""
S.A.T.U.R.N. Alarm Tool

Persistent local alarms stored in:
    data/saturn_alarms.json

Supported commands include:
    Set an alarm for 7:30 AM.
    Set an alarm for 20 minutes from now.
    Set an alarm for 2 hours from now.
    Show my alarms.
    Cancel my 7:30 AM alarm.

This module also exposes check_due_alarms(), which the GUI or
future Raspberry Pi runtime can poll periodically.
"""

import json
import os
import re
import signal
import sys
import time
import uuid
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import subprocess

from functools import wraps
from assistant_tools.alarm_playback import (
    begin_alarm_playback,
    finish_alarm_playback,
    get_ringing_alarm_ids,
    should_stop_alarm_playback,
    stop_alarm_playback,
)
from assistant_tools.storage_tool import atomic_save_json, storage_transaction

try:
    import winsound
except ImportError:
    winsound = None


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(
    PROJECT_ROOT,
    "data",
)

ALARMS_FILE = os.path.join(
    DATA_DIR,
    "saturn_alarms.json",
)

DEFAULT_TIMEZONE = "America/Detroit"
DEFAULT_SNOOZE_MINUTES = 10


def _ensure_storage():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(ALARMS_FILE):
        atomic_save_json(ALARMS_FILE, [])


def _load_alarms():
    _ensure_storage()

    try:
        with open(ALARMS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        data = []

    if not isinstance(data, list):
        data = []

    return data


def _save_alarms(alarms):
    atomic_save_json(ALARMS_FILE, alarms)


def _now():
    return datetime.now(
        ZoneInfo(
            DEFAULT_TIMEZONE
        )
    )


def _format_alarm_time(dt):
    return dt.strftime(
        "%I:%M %p"
    ).lstrip("0")


def _format_alarm_date(dt):
    return dt.strftime(
        "%A, %B %d"
    ).replace(
        " 0",
        " ",
    )


def _parse_relative_alarm(text, now):
    """
    Parse:
        in 20 minutes
        20 minutes from now
        in 2 hours
        2 hours from now
    """

    match = re.search(
        r"\b(?:in\s+)?(\d+)\s+"
        r"(minute|minutes|hour|hours)"
        r"(?:\s+from\s+now)?\b",
        text,
        flags=re.IGNORECASE,
    )

    if not match:
        return None

    amount = int(
        match.group(1)
    )

    unit = match.group(2).lower()

    if unit.startswith("hour"):
        return now + timedelta(
            hours=amount
        )

    return now + timedelta(
        minutes=amount
    )


def _parse_clock_alarm(text, now):
    """
    Parse common clock times such as:
        7 AM
        7:30 AM
        19:30
    """

    # 12-hour time with AM/PM
    match = re.search(
        r"\b(\d{1,2})"
        r"(?::(\d{2}))?"
        r"\s*(a\.?m\.?|p\.?m\.?)\b",
        text,
        flags=re.IGNORECASE,
    )

    if match:
        hour = int(
            match.group(1)
        )

        minute = int(
            match.group(2) or 0
        )

        meridiem = (
            match.group(3)
            .lower()
            .replace(".", "")
        )

        if (
            hour < 1
            or hour > 12
            or minute > 59
        ):
            return None

        if meridiem == "am":
            hour = 0 if hour == 12 else hour
        else:
            hour = 12 if hour == 12 else hour + 12

        alarm_time = now.replace(
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0,
        )

        # If that time has already passed today,
        # schedule it for tomorrow.
        if alarm_time <= now:
            alarm_time += timedelta(
                days=1
            )

        return alarm_time

    # 24-hour time
    match = re.search(
        r"\b([01]?\d|2[0-3]):([0-5]\d)\b",
        text,
    )

    if match:
        hour = int(
            match.group(1)
        )

        minute = int(
            match.group(2)
        )

        alarm_time = now.replace(
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0,
        )

        if alarm_time <= now:
            alarm_time += timedelta(
                days=1
            )

        return alarm_time

    return None


def _parse_alarm_datetime(text):
    now = _now()

    relative = _parse_relative_alarm(
        text,
        now,
    )

    if relative is not None:
        return relative

    return _parse_clock_alarm(
        text,
        now,
    )


def _detect_action(text):
    normalized = str(text).lower()

    if re.search(
        r"\bsnooze\b",
        normalized,
    ):
        return "snooze"

    if re.search(
        r"\b(?:stop|dismiss|silence)"
        r"(?:\s+(?:the\s+|my\s+)?)?"
        r"(?:ringing\s+)?alarms?\b",
        normalized,
    ) or normalized.strip() in {
        "stop",
        "dismiss",
        "silence",
    }:
        return "stop"

    if re.search(
        r"\b(?:cancel|delete|remove)\b",
        normalized,
    ):
        return "cancel"

    if re.search(
        r"\b(?:show|list|view)\b",
        normalized,
    ):
        return "show"

    if re.search(
        r"\b(?:set|create|make|wake me)\b",
        normalized,
    ):
        return "set"

    if "alarm" in normalized:
        return "show"

    return "unknown"


def _parse_snooze_minutes(text):
    normalized = str(text).lower()

    match = re.search(
        r"\bsnooze(?:\s+(?:the\s+)?alarm)?"
        r"(?:\s+for)?\s+(\d+)\s*"
        r"(minutes?|mins?|hours?|hrs?)\b",
        normalized,
    )

    if not match:
        return DEFAULT_SNOOZE_MINUTES

    amount = int(
        match.group(1)
    )
    unit = match.group(2)

    if unit.startswith(
        (
            "hour",
            "hr",
        )
    ):
        amount *= 60

    return amount


def _active_alarms(alarms):
    return [
        alarm
        for alarm in alarms
        if alarm.get(
            "status"
        ) == "active"
    ]


def _parse_iso(value):
    try:
        return datetime.fromisoformat(
            value
        )
    except (
        TypeError,
        ValueError,
    ):
        return None


def _find_alarm_to_cancel(text, alarms):
    """
    Try to match a requested clock time against active alarms.
    If there is only one active alarm and no time was supplied,
    allow cancelling that alarm.
    """

    active = _active_alarms(
        alarms
    )

    if not active:
        return None

    requested = _parse_alarm_datetime(
        text
    )

    if requested is not None:
        requested_clock = (
            requested.hour,
            requested.minute,
        )

        for alarm in active:
            alarm_dt = _parse_iso(
                alarm.get(
                    "trigger_at"
                )
            )

            if (
                alarm_dt is not None
                and (
                    alarm_dt.hour,
                    alarm_dt.minute,
                ) == requested_clock
            ):
                return alarm

    if len(active) == 1:
        return active[0]

    return None


def _locked_alarm_operation(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        with storage_transaction(ALARMS_FILE):
            return function(*args, **kwargs)

    return wrapper


@_locked_alarm_operation
def handle_alarm_query(text):
    """
    Handle a natural-language alarm request.
    """

    action = _detect_action(
        text
    )

    alarms = _load_alarms()

    # --------------------------------------------------------
    # SNOOZE CURRENTLY RINGING ALARM
    # --------------------------------------------------------

    if action == "snooze":
        ringing_alarm_ids = get_ringing_alarm_ids()

        if not ringing_alarm_ids:
            return {
                "success": False,
                "action": action,
                "response": "No alarm is currently ringing.",
                "error": "No ringing alarm.",
            }

        if len(ringing_alarm_ids) != 1:
            return {
                "success": False,
                "action": action,
                "response": (
                    "More than one alarm is currently ringing. "
                    "Please stop them and set a new alarm."
                ),
                "error": "Multiple ringing alarms.",
            }

        source_alarm_id = ringing_alarm_ids[0]

        source_alarm = next(
            (
                alarm
                for alarm in alarms
                if str(alarm.get("id")) == source_alarm_id
            ),
            None,
        )

        if source_alarm is None:
            return {
                "success": False,
                "action": action,
                "response": (
                    "I couldn't identify the ringing alarm."
                ),
                "error": "Ringing alarm record not found.",
            }

        if source_alarm.get("snoozed_to_alarm_id"):
            stop_alarm_playback()

            return {
                "success": False,
                "action": action,
                "response": "That alarm has already been snoozed.",
                "error": "Alarm already snoozed.",
            }

        minutes = _parse_snooze_minutes(
            text
        )

        if minutes < 1 or minutes > 1440:
            return {
                "success": False,
                "action": action,
                "response": (
                    "Please choose a snooze time between "
                    "1 minute and 24 hours."
                ),
                "error": "Invalid snooze duration.",
            }

        stopped = stop_alarm_playback()

        if not stopped:
            return {
                "success": False,
                "action": action,
                "response": "No alarm is currently ringing.",
                "error": "Playback ended before snooze.",
            }

        trigger_at = _now() + timedelta(
            minutes=minutes
        )

        snoozed_alarm = {
            "id": str(
                uuid.uuid4()
            ),
            "created_at": _now().isoformat(),
            "trigger_at": trigger_at.isoformat(),
            "timezone": DEFAULT_TIMEZONE,
            "status": "active",
            "label": source_alarm.get(
                "label",
                "Alarm",
            ),
            "snoozed_from_alarm_id": source_alarm_id,
            "snooze_minutes": minutes,
        }

        source_alarm["snoozed_at"] = (
            _now().isoformat()
        )
        source_alarm["snoozed_to_alarm_id"] = (
            snoozed_alarm["id"]
        )

        alarms.append(
            snoozed_alarm
        )

        _save_alarms(
            alarms
        )

        return {
            "success": True,
            "action": action,
            "stopped": True,
            "minutes": minutes,
            "alarm": snoozed_alarm,
            "response": (
                f"Alarm snoozed for {minutes} "
                f"{'minute' if minutes == 1 else 'minutes'}."
            ),
            "error": None,
        }

    # --------------------------------------------------------
    # STOP CURRENTLY RINGING ALARM
    # --------------------------------------------------------

    if action == "stop":
        stopped = stop_alarm_playback()

        return {
            "success": True,
            "action": action,
            "stopped": stopped,
            "response": (
                "Alarm stopped."
                if stopped
                else "No alarm is currently ringing."
            ),
            "error": None,
        }

    # --------------------------------------------------------
    # SET
    # --------------------------------------------------------

    if action == "set":
        trigger_at = _parse_alarm_datetime(
            text
        )

        if trigger_at is None:
            return {
                "success": False,
                "action": action,
                "response": (
                    "I couldn't determine when you wanted "
                    "the alarm to go off."
                ),
                "error": "Alarm time not detected.",
            }

        alarm = {
            "id": str(
                uuid.uuid4()
            ),
            "created_at": _now().isoformat(),
            "trigger_at": trigger_at.isoformat(),
            "timezone": DEFAULT_TIMEZONE,
            "status": "active",
            "label": "Alarm",
        }

        alarms.append(
            alarm
        )

        _save_alarms(
            alarms
        )

        response = (
            f"Alarm set for {_format_alarm_time(trigger_at)} "
            f"on {_format_alarm_date(trigger_at)}."
        )

        return {
            "success": True,
            "action": action,
            "alarm": alarm,
            "response": response,
            "error": None,
        }

    # --------------------------------------------------------
    # SHOW
    # --------------------------------------------------------

    if action == "show":
        active = sorted(
            _active_alarms(
                alarms
            ),
            key=lambda alarm: alarm.get(
                "trigger_at",
                "",
            ),
        )

        if not active:
            return {
                "success": True,
                "action": action,
                "alarms": [],
                "response": (
                    "You don't have any active alarms."
                ),
                "error": None,
            }

        lines = [
            "Active alarms:"
        ]

        for index, alarm in enumerate(
            active,
            start=1,
        ):
            alarm_dt = _parse_iso(
                alarm.get(
                    "trigger_at"
                )
            )

            if alarm_dt is None:
                continue

            lines.append(
                f"{index}. "
                f"{_format_alarm_time(alarm_dt)} "
                f"on {_format_alarm_date(alarm_dt)}"
            )

        return {
            "success": True,
            "action": action,
            "alarms": active,
            "response": "\n".join(
                lines
            ),
            "error": None,
        }

    # --------------------------------------------------------
    # CANCEL
    # --------------------------------------------------------

    if action == "cancel":
        normalized = str(text).lower()

        if re.search(
            r"\b(?:cancel|delete|remove)\s+all\s+(?:my\s+)?alarms?\b",
            normalized,
        ):
            active = _active_alarms(
                alarms
            )

            if not active:
                return {
                    "success": True,
                    "action": "cancel_all",
                    "alarms": [],
                    "response": (
                        "You don't have any active alarms to cancel."
                    ),
                    "error": None,
                }

            cancelled_at = (
                _now().isoformat()
            )

            for alarm in active:
                alarm["status"] = "cancelled"
                alarm["cancelled_at"] = (
                    cancelled_at
                )

            _save_alarms(
                alarms
            )

            return {
                "success": True,
                "action": "cancel_all",
                "alarms": active,
                "response": (
                    f"I cancelled {len(active)} active "
                    f"{'alarm' if len(active) == 1 else 'alarms'}."
                ),
                "error": None,
            }

        alarm = _find_alarm_to_cancel(
            text,
            alarms,
        )

        if alarm is None:
            return {
                "success": False,
                "action": action,
                "response": (
                    "I couldn't determine which active alarm "
                    "you wanted to cancel."
                ),
                "error": "Alarm not uniquely identified.",
            }

        alarm["status"] = "cancelled"
        alarm["cancelled_at"] = (
            _now().isoformat()
        )

        _save_alarms(
            alarms
        )

        alarm_dt = _parse_iso(
            alarm.get(
                "trigger_at"
            )
        )

        if alarm_dt is None:
            response = "I cancelled the alarm."
        else:
            response = (
                f"I cancelled your "
                f"{_format_alarm_time(alarm_dt)} alarm."
            )

        return {
            "success": True,
            "action": action,
            "alarm": alarm,
            "response": response,
            "error": None,
        }

    return {
        "success": False,
        "action": action,
        "response": (
            "I couldn't determine what you wanted me to do "
            "with your alarms."
        ),
        "error": "Alarm action not detected.",
    }


def _wait_for_alarm_interval(
    playback_generation,
    duration,
    interval=0.05,
):
    """
    Wait briefly while checking for a cross-process stop request.
    """

    deadline = time.monotonic() + duration

    while time.monotonic() < deadline:
        if should_stop_alarm_playback(
            playback_generation
        ):
            return False

        time.sleep(
            min(
                interval,
                max(
                    0,
                    deadline - time.monotonic(),
                ),
            )
        )

    return not should_stop_alarm_playback(
        playback_generation
    )


def _signal_linux_sound_process(
    process,
    process_signal,
):
    """
    Signal the entire alarm process group.

    speaker-test may create a child audio process. Stopping only
    speaker-test can leave that child playing after SATURN says the
    alarm was dismissed.
    """

    try:
        process_group = os.getpgid(
            process.pid
        )

        os.killpg(
            process_group,
            process_signal,
        )
    except (
        AttributeError,
        OSError,
    ):
        if process_signal == signal.SIGTERM:
            process.terminate()
        else:
            process.kill()


def _stop_linux_sound_process(process):
    if process.poll() is not None:
        return

    _signal_linux_sound_process(
        process,
        signal.SIGTERM,
    )

    try:
        process.wait(
            timeout=1
        )
    except subprocess.TimeoutExpired:
        _signal_linux_sound_process(
            process,
            signal.SIGKILL,
        )
        process.wait(
            timeout=1
        )


def play_alarm_sound(
    repetitions=5,
    alarm_id=None,
):
    """
    Play SATURN's interruptible alarm sound.

    Playback state is shared across processes so the API or voice
    service can dismiss an alarm owned by the voice runtime.
    """

    repetitions = max(
        1,
        int(repetitions),
    )

    playback_generation = (
        begin_alarm_playback(
            alarm_id=alarm_id,
        )
    )

    try:
        if (
            sys.platform.startswith("win")
            and winsound is not None
        ):
            for _ in range(repetitions):
                if should_stop_alarm_playback(
                    playback_generation
                ):
                    break

                try:
                    winsound.PlaySound(
                        "SystemAlarm",
                        winsound.SND_ALIAS
                        | winsound.SND_ASYNC,
                    )
                except RuntimeError:
                    winsound.MessageBeep(
                        winsound.MB_ICONEXCLAMATION
                    )

                if not _wait_for_alarm_interval(
                    playback_generation,
                    1,
                ):
                    break

            try:
                winsound.PlaySound(
                    None,
                    winsound.SND_PURGE,
                )
            except RuntimeError:
                pass

            return True

        if sys.platform.startswith("linux"):
            for _ in range(repetitions):
                if should_stop_alarm_playback(
                    playback_generation
                ):
                    break

                try:
                    process = subprocess.Popen(
                        [
                            "speaker-test",
                            "-t",
                            "sine",
                            "-f",
                            "880",
                            "-l",
                            "1",
                        ],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        start_new_session=True,
                    )

                    deadline = (
                        time.monotonic() + 3
                    )

                    while (
                        process.poll() is None
                        and time.monotonic() < deadline
                    ):
                        if should_stop_alarm_playback(
                            playback_generation
                        ):
                            _stop_linux_sound_process(
                                process
                            )
                            break

                        time.sleep(
                            0.05
                        )

                    if process.poll() is None:
                        _stop_linux_sound_process(
                            process
                        )

                except OSError:
                    print(
                        "\a",
                        end="",
                        flush=True,
                    )

                if not _wait_for_alarm_interval(
                    playback_generation,
                    0.15,
                ):
                    break

            return True

        for _ in range(repetitions):
            if should_stop_alarm_playback(
                playback_generation
            ):
                break

            print(
                "\a",
                end="",
                flush=True,
            )

            if not _wait_for_alarm_interval(
                playback_generation,
                0.5,
            ):
                break

        return True

    finally:
        finish_alarm_playback()


@_locked_alarm_operation
def check_due_alarms(mark_fired=True):
    """
    Return alarms that are due now or overdue.

    The GUI or Raspberry Pi runtime can call this once per second.
    When mark_fired=True, returned alarms are immediately marked
    as fired so they trigger only once.
    """

    alarms = _load_alarms()
    now = _now()

    due = []

    for alarm in alarms:
        if alarm.get(
            "status"
        ) != "active":
            continue

        trigger_at = _parse_iso(
            alarm.get(
                "trigger_at"
            )
        )

        if trigger_at is None:
            continue

        if trigger_at <= now:
            due.append(
                alarm
            )

            if mark_fired:
                alarm["status"] = "fired"
                alarm["fired_at"] = (
                    now.isoformat()
                )

    if (
        mark_fired
        and due
    ):
        _save_alarms(
            alarms
        )

    return due

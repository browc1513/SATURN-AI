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
    refresh_alarm_playback,
    should_stop_alarm_playback,
    stop_alarm_playback,
)
from assistant_tools.alarm_playback_policy import (
    TIMED_MODE,
    UNTIL_DISMISSED_MODE,
    normalize_saved_playback_policy,
    parse_alarm_playback_policy,
    remove_alarm_playback_policy_language,
    timed_alarm_has_expired,
)
from assistant_tools.alarm_tones import (
    resolve_alarm_tone,
    resolve_default_alarm_tone,
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
        r"\b(?:set|create|make|wake me|remind me)\b",
        normalized,
    ):
        return "set"

    if "alarm" in normalized:
        return "show"

    return "unknown"


def _parse_spoken_number(text):
    """
    Parse the small spoken-number range needed for snoozing.
    """

    normalized = re.sub(
        r"[-]+",
        " ",
        str(text or "").strip().lower(),
    )

    if normalized.isdigit():
        return int(normalized)

    units = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19,
    }

    tens = {
        "twenty": 20,
        "thirty": 30,
        "forty": 40,
        "fifty": 50,
        "sixty": 60,
        "seventy": 70,
        "eighty": 80,
        "ninety": 90,
    }

    tokens = [
        token
        for token in normalized.split()
        if token != "and"
    ]

    if not tokens:
        return None

    if len(tokens) == 1:
        return (
            units.get(tokens[0])
            if tokens[0] in units
            else tens.get(tokens[0])
        )

    if (
        len(tokens) == 2
        and tokens[0] in tens
        and tokens[1] in units
        and units[tokens[1]] < 10
    ):
        return (
            tens[tokens[0]]
            + units[tokens[1]]
        )

    if tokens in (
        ["one", "hundred"],
        ["a", "hundred"],
    ):
        return 100

    if (
        len(tokens) == 3
        and tokens[0] in {"one", "a"}
        and tokens[1] == "hundred"
    ):
        remainder = (
            units.get(tokens[2])
            if tokens[2] in units
            else tens.get(tokens[2])
        )

        if remainder is not None:
            return 100 + remainder

    if (
        len(tokens) == 4
        and tokens[0] in {"one", "a"}
        and tokens[1] == "hundred"
        and tokens[2] in tens
        and tokens[3] in units
        and units[tokens[3]] < 10
    ):
        return (
            100
            + tens[tokens[2]]
            + units[tokens[3]]
        )

    return None


def _parse_snooze_minutes(text):
    normalized = re.sub(
        r"\s+",
        " ",
        str(text or "").strip().lower(),
    )

    match = re.search(
        r"\bsnooze(?:\s+(?:the\s+)?alarm)?"
        r"(?:\s+for)?\s+"
        r"(.+?)\s*"
        r"(minutes?|mins?|hours?|hrs?)\b",
        normalized,
    )

    if not match:
        return DEFAULT_SNOOZE_MINUTES

    amount = _parse_spoken_number(
        match.group(1)
    )

    if amount is None:
        return None

    unit = match.group(2)

    if unit.startswith(
        (
            "hour",
            "hr",
        )
    ):
        amount *= 60

    return amount


def _parse_requested_tone(text):
    """
    Extract a friendly custom-tone name from an alarm request.

    Examples:
        with the Zen Gong tone
        using Morning Bell tone
        with the Ocean alarm tone
    """

    match = re.search(
        r"\b(?:with|using)\s+"
        r"(?:the\s+)?"
        r"(.+?)\s+"
        r"(?:alarm\s+)?tone\b",
        str(text),
        flags=re.IGNORECASE,
    )

    if not match:
        return {
            "requested": False,
            "name": None,
            "tone": None,
        }

    requested_name = re.sub(
        r"\s+",
        " ",
        match.group(1),
    ).strip(
        " .,!?:;"
    )

    return {
        "requested": True,
        "name": requested_name,
        "tone": resolve_alarm_tone(
            requested_name
        ),
    }


def _resolve_playback_tone_path(tone_name):
    tone = resolve_alarm_tone(
        tone_name
    )

    if tone is None:
        return None

    return tone["path"]


def _linux_alarm_command(tone_path=None):
    if tone_path:
        return [
            "aplay",
            "--quiet",
            tone_path,
        ]

    return [
        "speaker-test",
        "-t",
        "sine",
        "-f",
        "880",
        "-l",
        "1",
    ]


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

        if (
            minutes is None
            or minutes < 1
            or minutes > 120
        ):
            return {
                "success": False,
                "action": action,
                "response": (
                    "Please choose a snooze time between "
                    "1 and 120 minutes."
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
            "tone": source_alarm.get(
                "tone"
            ),
            "playback_mode": source_alarm.get(
                "playback_mode",
                "until_dismissed",
            ),
            "playback_duration_seconds": source_alarm.get(
                "playback_duration_seconds"
            ),
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
        playback_policy = (
            parse_alarm_playback_policy(
                text
            )
        )

        if not playback_policy["success"]:
            return {
                "success": False,
                "action": action,
                "response": playback_policy[
                    "error"
                ],
                "error": (
                    "Invalid alarm playback duration."
                ),
            }

        tone_request = _parse_requested_tone(
            text
        )

        if (
            tone_request["requested"]
            and tone_request["tone"] is None
        ):
            requested_name = (
                tone_request["name"]
                or "that"
            )

            return {
                "success": False,
                "action": action,
                "response": (
                    f"I couldn't find the {requested_name} "
                    "alarm tone."
                ),
                "error": "Alarm tone not found.",
            }

        selected_tone = (
            tone_request["tone"]
            if tone_request["requested"]
            else resolve_default_alarm_tone()
        )

        trigger_text = (
            remove_alarm_playback_policy_language(
                text
            )
        )

        trigger_at = _parse_alarm_datetime(
            trigger_text
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
            "tone": (
                selected_tone["filename"]
                if selected_tone
                else None
            ),
            "playback_mode": playback_policy[
                "mode"
            ],
            "playback_duration_seconds": (
                playback_policy[
                    "duration_seconds"
                ]
            ),
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

        if tone_request["tone"]:
            response = (
                response[:-1]
                + " using the "
                + tone_request["tone"]["name"]
                + " tone."
            )

        if (
            playback_policy["mode"]
            == TIMED_MODE
        ):
            seconds = playback_policy[
                "duration_seconds"
            ]

            response += (
                f" It will ring for {seconds} "
                f"{'second' if seconds == 1 else 'seconds'}."
            )
        else:
            response += (
                " It will ring until stopped or snoozed."
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
    tone=None,
    playback_mode=None,
    playback_duration_seconds=None,
):
    """
    Play SATURN's interruptible alarm sound.

    New alarms use either timed playback or continue until explicitly
    stopped or snoozed. Calls without a playback mode retain the
    historical finite-repetition behavior for compatibility.
    """

    repetitions = max(
        1,
        int(repetitions),
    )

    legacy_playback = (
        playback_mode is None
    )

    if legacy_playback:
        resolved_mode = "legacy"
        resolved_duration = None
    else:
        policy = normalize_saved_playback_policy(
            playback_mode,
            playback_duration_seconds,
        )
        resolved_mode = policy["mode"]
        resolved_duration = policy[
            "duration_seconds"
        ]

    tone_path = (
        _resolve_playback_tone_path(
            tone
        )
        if tone
        else None
    )

    playback_generation = (
        begin_alarm_playback(
            alarm_id=alarm_id,
            requires_dismissal=(
                resolved_mode
                == UNTIL_DISMISSED_MODE
            ),
        )
    )

    started_at = time.monotonic()
    completed_repetitions = 0

    def playback_should_continue():
        if not refresh_alarm_playback(
            playback_generation,
            alarm_id=alarm_id,
        ):
            return False

        if should_stop_alarm_playback(
            playback_generation
        ):
            return False

        if legacy_playback:
            return (
                completed_repetitions
                < repetitions
            )

        if resolved_mode == TIMED_MODE:
            return not timed_alarm_has_expired(
                resolved_mode,
                started_at=started_at,
                current_time=time.monotonic(),
                duration_seconds=resolved_duration,
            )

        return (
            resolved_mode
            == UNTIL_DISMISSED_MODE
        )

    try:
        if (
            sys.platform.startswith("win")
            and winsound is not None
        ):
            while playback_should_continue():
                try:
                    winsound.PlaySound(
                        (
                            tone_path
                            if tone_path
                            else "SystemAlarm"
                        ),
                        (
                            winsound.SND_FILENAME
                            if tone_path
                            else winsound.SND_ALIAS
                        )
                        | winsound.SND_ASYNC,
                    )
                except RuntimeError:
                    winsound.MessageBeep(
                        winsound.MB_ICONEXCLAMATION
                    )

                completed_repetitions += 1

                wait_deadline = (
                    time.monotonic() + 1
                )

                while (
                    time.monotonic()
                    < wait_deadline
                ):
                    if not playback_should_continue():
                        break

                    time.sleep(
                        0.05
                    )

            try:
                winsound.PlaySound(
                    None,
                    winsound.SND_PURGE,
                )
            except RuntimeError:
                pass

            return True

        if sys.platform.startswith("linux"):
            while playback_should_continue():
                process = None

                try:
                    process = subprocess.Popen(
                        _linux_alarm_command(
                            tone_path
                        ),
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        start_new_session=True,
                    )

                    # speaker-test needs a defensive limit. A custom
                    # WAV is allowed to finish naturally, while stop,
                    # snooze, and timed expiration remain responsive.
                    process_deadline = (
                        None
                        if tone_path
                        else time.monotonic() + 3
                    )

                    while process.poll() is None:
                        if not playback_should_continue():
                            _stop_linux_sound_process(
                                process
                            )
                            break

                        if (
                            process_deadline is not None
                            and time.monotonic()
                            >= process_deadline
                        ):
                            _stop_linux_sound_process(
                                process
                            )
                            break

                        time.sleep(
                            0.05
                        )

                except OSError:
                    print(
                        "\a",
                        end="",
                        flush=True,
                    )
                finally:
                    if (
                        process is not None
                        and process.poll() is None
                    ):
                        _stop_linux_sound_process(
                            process
                        )

                completed_repetitions += 1

                pause_deadline = (
                    time.monotonic() + 0.15
                )

                while (
                    time.monotonic()
                    < pause_deadline
                ):
                    if not playback_should_continue():
                        break

                    time.sleep(
                        0.05
                    )

            return True

        while playback_should_continue():
            print(
                "\a",
                end="",
                flush=True,
            )

            completed_repetitions += 1

            wait_deadline = (
                time.monotonic() + 0.5
            )

            while (
                time.monotonic()
                < wait_deadline
            ):
                if not playback_should_continue():
                    break

                time.sleep(
                    0.05
                )

        return True

    finally:
        finish_alarm_playback(
            alarm_id=alarm_id,
            requires_dismissal=(
                resolved_mode
                == UNTIL_DISMISSED_MODE
            ),
        )


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

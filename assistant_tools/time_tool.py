"""
S.A.T.U.R.N. Time Tool

Deterministic time/date handling using Python's standard library.
No network connection is required.
"""

import re
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


DEFAULT_TIMEZONE = "America/Detroit"


TIMEZONE_ALIASES = {
    # Local / US
    "local": DEFAULT_TIMEZONE,
    "detroit": "America/Detroit",
    "michigan": "America/Detroit",
    "eastern": "America/New_York",
    "et": "America/New_York",
    "central": "America/Chicago",
    "ct": "America/Chicago",
    "mountain": "America/Denver",
    "mt": "America/Denver",
    "pacific": "America/Los_Angeles",
    "pt": "America/Los_Angeles",

    # Common international requests
    "utc": "UTC",
    "gmt": "UTC",
    "tokyo": "Asia/Tokyo",
    "japan": "Asia/Tokyo",
    "london": "Europe/London",
}


def _detect_timezone(text, default_timezone=DEFAULT_TIMEZONE):
    """
    Detect a small set of common timezone/location aliases.

    Version 1 intentionally stays deterministic and conservative.
    """

    normalized = str(text).lower()

    for alias, timezone_name in TIMEZONE_ALIASES.items():
        if re.search(
            r"\b" + re.escape(alias) + r"\b",
            normalized,
        ):
            return timezone_name, alias

    return default_timezone, "local"


def _detect_request_type(text):
    """
    Return:
        "time"
        "date"
        "datetime"
    """

    normalized = str(text).lower()

    asks_date = any(
        re.search(pattern, normalized)
        for pattern in (
            r"\bdate\b",
            r"\bwhat\s+day\s+is\s+it\b",
            r"\btoday\b",
        )
    )

    asks_time = any(
        re.search(pattern, normalized)
        for pattern in (
            r"\btime\b",
            r"\bclock\b",
        )
    )

    if asks_date and asks_time:
        return "datetime"

    if asks_date:
        return "date"

    return "time"


def handle_time_query(
    text,
    default_timezone=DEFAULT_TIMEZONE,
):
    """
    Handle a natural-language time/date request.

    Returns a structured dictionary suitable for SATURN.handle_query().
    """

    timezone_name, detected_alias = _detect_timezone(
        text,
        default_timezone=default_timezone,
    )

    try:
        timezone = ZoneInfo(
            timezone_name
        )

    except ZoneInfoNotFoundError:
        return {
            "success": False,
            "response": (
                "I couldn't load the requested timezone."
            ),
            "timezone": timezone_name,
            "error": (
                f"Timezone not found: {timezone_name}"
            ),
        }

    now = datetime.now(
        timezone
    )

    request_type = _detect_request_type(
        text
    )

    time_12h = now.strftime(
        "%I:%M %p"
    ).lstrip("0")

    time_24h = now.strftime(
        "%H:%M"
    )

    date_display = now.strftime(
        "%A, %B %d, %Y"
    ).replace(
        " 0",
        " ",
    )

    if request_type == "date":
        response = (
            f"Today is {date_display}."
        )

    elif request_type == "datetime":
        response = (
            f"It is {time_12h} on {date_display}."
        )

    else:
        if detected_alias == "local":
            response = (
                f"It is {time_12h}."
            )
        else:
            response = (
                f"It is {time_12h} in {detected_alias.title()}."
            )

    return {
        "success": True,
        "request_type": request_type,
        "timezone": timezone_name,
        "detected_alias": detected_alias,
        "datetime_iso": now.isoformat(),
        "date": now.date().isoformat(),
        "time_12h": time_12h,
        "time_24h": time_24h,
        "response": response,
        "error": None,
    }

"""
Cross-process playback state for SATURN alarms.

The voice service owns sound playback, while commands can arrive
through either the voice service or the API service. This shared
state allows either process to dismiss currently ringing alarms.
"""

import json
import os
from datetime import datetime, timezone

from assistant_tools.storage_tool import (
    atomic_save_json,
    storage_transaction,
)


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(
    PROJECT_ROOT,
    "data",
)

ALARM_PLAYBACK_STATE_FILE = os.path.join(
    DATA_DIR,
    "saturn_alarm_playback.json",
)

STALE_PLAYBACK_SECONDS = 60


def _utc_now():
    return datetime.now(
        timezone.utc
    )


def _default_state():
    return {
        "generation": 0,
        "active_count": 0,
        "updated_at": _utc_now().isoformat(),
    }


def _load_state():
    try:
        with open(
            ALARM_PLAYBACK_STATE_FILE,
            "r",
            encoding="utf-8",
        ) as file:
            state = json.load(file)
    except (
        FileNotFoundError,
        json.JSONDecodeError,
        OSError,
    ):
        state = _default_state()

    if not isinstance(state, dict):
        state = _default_state()

    try:
        generation = max(
            0,
            int(state.get("generation", 0)),
        )
    except (
        TypeError,
        ValueError,
    ):
        generation = 0

    try:
        active_count = max(
            0,
            int(state.get("active_count", 0)),
        )
    except (
        TypeError,
        ValueError,
    ):
        active_count = 0

    updated_at = state.get("updated_at")

    try:
        updated = datetime.fromisoformat(
            str(updated_at)
        )

        if updated.tzinfo is None:
            updated = updated.replace(
                tzinfo=timezone.utc
            )

        age = (
            _utc_now() - updated
        ).total_seconds()
    except (
        TypeError,
        ValueError,
    ):
        age = STALE_PLAYBACK_SECONDS + 1

    if (
        active_count
        and age > STALE_PLAYBACK_SECONDS
    ):
        active_count = 0

    return {
        "generation": generation,
        "active_count": active_count,
        "updated_at": str(updated_at or ""),
    }


def _save_state(state):
    state["updated_at"] = (
        _utc_now().isoformat()
    )

    atomic_save_json(
        ALARM_PLAYBACK_STATE_FILE,
        state,
    )


def begin_alarm_playback():
    os.makedirs(
        DATA_DIR,
        exist_ok=True,
    )

    with storage_transaction(
        ALARM_PLAYBACK_STATE_FILE
    ):
        state = _load_state()
        state["active_count"] += 1
        _save_state(state)

        return state["generation"]


def finish_alarm_playback():
    with storage_transaction(
        ALARM_PLAYBACK_STATE_FILE
    ):
        state = _load_state()
        state["active_count"] = max(
            0,
            state["active_count"] - 1,
        )
        _save_state(state)


def stop_alarm_playback():
    """
    Request that every currently active alarm sound stop.

    Incrementing the generation stops existing playback while
    allowing alarms started afterward to use the new generation.
    """

    with storage_transaction(
        ALARM_PLAYBACK_STATE_FILE
    ):
        state = _load_state()

        if state["active_count"] <= 0:
            return False

        state["generation"] += 1
        _save_state(state)

        return True


def should_stop_alarm_playback(
    playback_generation,
):
    with storage_transaction(
        ALARM_PLAYBACK_STATE_FILE
    ):
        state = _load_state()

        return (
            state["generation"]
            != playback_generation
        )


def is_alarm_ringing():
    with storage_transaction(
        ALARM_PLAYBACK_STATE_FILE
    ):
        state = _load_state()

        return state["active_count"] > 0

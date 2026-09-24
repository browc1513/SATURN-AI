"""
Discovery and validation for SATURN custom alarm tones.

Only WAV files located directly inside SATURN's configured alarm-tone
directory are exposed. Callers select tones by their friendly stem,
never by supplying an arbitrary filesystem path.
"""

import os
import re
from pathlib import Path


PROJECT_ROOT = Path(
    __file__
).resolve().parent.parent

DEFAULT_ALARM_TONES_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "alarm_tones"
)

ALARM_TONES_DIRECTORY_ENV = (
    "SATURN_ALARM_TONES_DIR"
)

SUPPORTED_ALARM_TONE_SUFFIXES = {
    ".wav",
}


def get_alarm_tones_directory():
    """
    Return the configured custom-tone directory.

    SATURN_ALARM_TONES_DIR may relocate runtime audio outside the
    repository. Otherwise, data/alarm_tones is used.
    """

    configured = os.environ.get(
        ALARM_TONES_DIRECTORY_ENV,
        "",
    ).strip()

    if configured:
        return Path(
            configured
        ).expanduser().resolve()

    return (
        DEFAULT_ALARM_TONES_DIRECTORY.resolve()
    )


def ensure_alarm_tones_directory():
    directory = get_alarm_tones_directory()

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory


def normalize_alarm_tone_name(value):
    """
    Normalize a filename or spoken tone name for safe comparison.
    """

    name = Path(
        str(value or "").strip()
    ).stem

    name = re.sub(
        r"[_-]+",
        " ",
        name,
    )

    name = re.sub(
        r"\s+",
        " ",
        name,
    ).strip()

    return name.casefold()


def _friendly_alarm_tone_name(path):
    name = re.sub(
        r"[_-]+",
        " ",
        path.stem,
    )

    name = re.sub(
        r"\s+",
        " ",
        name,
    ).strip()

    return name


def _is_safe_tone_file(path, directory):
    try:
        resolved = path.resolve(
            strict=True
        )
        resolved.relative_to(
            directory.resolve()
        )
    except (
        FileNotFoundError,
        OSError,
        ValueError,
    ):
        return False

    return (
        resolved.is_file()
        and not path.is_symlink()
        and resolved.parent == directory.resolve()
        and resolved.suffix.casefold()
        in SUPPORTED_ALARM_TONE_SUFFIXES
    )


def list_alarm_tones():
    """
    Return safely discoverable custom WAV tones.

    Results contain a friendly name and filename. Internal paths are
    included for trusted playback code but should not be accepted from
    user input.
    """

    directory = ensure_alarm_tones_directory()
    tones = []

    try:
        candidates = list(
            directory.iterdir()
        )
    except OSError:
        return []

    for path in candidates:
        if not _is_safe_tone_file(
            path,
            directory,
        ):
            continue

        tones.append(
            {
                "name": _friendly_alarm_tone_name(
                    path
                ),
                "filename": path.name,
                "path": str(
                    path.resolve()
                ),
            }
        )

    return sorted(
        tones,
        key=lambda tone: (
            tone["name"].casefold(),
            tone["filename"].casefold(),
        ),
    )


def resolve_alarm_tone(value):
    """
    Resolve a friendly name or filename to a discovered WAV tone.

    Arbitrary filesystem paths are never resolved directly.
    """

    requested = normalize_alarm_tone_name(
        value
    )

    if not requested:
        return None

    for tone in list_alarm_tones():
        names = {
            normalize_alarm_tone_name(
                tone["name"]
            ),
            normalize_alarm_tone_name(
                tone["filename"]
            ),
        }

        if requested in names:
            return tone

    return None

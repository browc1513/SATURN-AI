"""
Discovery and validation for SATURN custom alarm tones.

Only WAV files located directly inside SATURN's configured alarm-tone
directory are exposed. Callers select tones by their friendly stem,
never by supplying an arbitrary filesystem path.
"""

import io
import os
import re
import uuid
import wave
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

DEFAULT_ALARM_TONE_NAME = os.environ.get(
    "SATURN_DEFAULT_ALARM_TONE",
    "Saturn Alarm 1",
).strip()

MAX_ALARM_TONE_BYTES = 10 * 1024 * 1024
MAX_ALARM_TONE_SECONDS = 30.0
VALID_ALARM_TONE_SAMPLE_RATES = {
    44100,
    48000,
}
VALID_ALARM_TONE_NAME_PATTERN = re.compile(
    r"[A-Za-z0-9][A-Za-z0-9 _-]{0,79}"
)


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

def resolve_default_alarm_tone():
    """
    Return SATURN's installed default tone, when available.

    A missing default never exposes or constructs an arbitrary path.
    Playback safely falls back to the platform alarm sound.
    """

    if not DEFAULT_ALARM_TONE_NAME:
        return None

    return resolve_alarm_tone(
        DEFAULT_ALARM_TONE_NAME
    )

def validate_alarm_tone_name(value):
    """
    Return a safe friendly tone name.

    Files are always stored directly inside the configured tone
    directory and always receive a .wav extension.
    """

    name = str(
        value or ""
    ).strip()

    if name.casefold().endswith(
        ".wav"
    ):
        name = name[:-4].strip()

    if not VALID_ALARM_TONE_NAME_PATTERN.fullmatch(
        name
    ):
        raise ValueError(
            "Tone names must contain 1-80 letters, numbers, "
            "spaces, underscores, or hyphens."
        )

    return name


def validate_alarm_tone_wav(
    wav_data,
):
    """
    Validate uploaded WAV bytes without playing the audio.
    """

    if not isinstance(
        wav_data,
        (
            bytes,
            bytearray,
        ),
    ):
        raise ValueError(
            "Alarm tone data must be WAV bytes."
        )

    wav_data = bytes(
        wav_data
    )

    if not wav_data:
        raise ValueError(
            "The WAV file is empty."
        )

    if len(wav_data) > MAX_ALARM_TONE_BYTES:
        raise ValueError(
            "The WAV file exceeds the 10 MB limit."
        )

    try:
        with wave.open(
            io.BytesIO(wav_data),
            "rb",
        ) as audio:
            channels = audio.getnchannels()
            sample_width = audio.getsampwidth()
            sample_rate = audio.getframerate()
            frame_count = audio.getnframes()
            compression = audio.getcomptype()

    except (
        EOFError,
        wave.Error,
    ) as error:
        raise ValueError(
            f"Invalid WAV file: {error}"
        ) from error

    duration = (
        frame_count / sample_rate
        if sample_rate
        else 0
    )

    problems = []

    if compression != "NONE":
        problems.append(
            "audio must use uncompressed PCM"
        )

    if sample_width != 2:
        problems.append(
            "samples must be signed 16-bit"
        )

    if channels not in {
        1,
        2,
    }:
        problems.append(
            "audio must be mono or stereo"
        )

    if (
        sample_rate
        not in VALID_ALARM_TONE_SAMPLE_RATES
    ):
        problems.append(
            "sample rate must be 44100 or 48000 Hz"
        )

    if duration <= 0:
        problems.append(
            "audio contains no playable frames"
        )

    if duration > MAX_ALARM_TONE_SECONDS:
        problems.append(
            "audio must be 30 seconds or shorter"
        )

    if problems:
        raise ValueError(
            "Incompatible WAV: "
            + "; ".join(problems)
            + "."
        )

    return {
        "channels": channels,
        "sample_bits": sample_width * 8,
        "sample_rate": sample_rate,
        "duration_seconds": duration,
        "compression": compression,
        "size_bytes": len(wav_data),
    }


def install_alarm_tone(
    name,
    wav_data,
):
    """
    Validate and atomically install a custom alarm tone.
    """

    safe_name = validate_alarm_tone_name(
        name
    )
    metadata = validate_alarm_tone_wav(
        wav_data
    )

    if resolve_alarm_tone(
        safe_name
    ) is not None:
        raise FileExistsError(
            f"An alarm tone named {safe_name} already exists."
        )

    directory = ensure_alarm_tones_directory()
    destination = (
        directory
        / f"{safe_name}.wav"
    )
    temporary = (
        directory
        / (
            f".{safe_name}."
            f"{uuid.uuid4().hex}.tmp"
        )
    )

    try:
        with open(
            temporary,
            "xb",
        ) as file:
            file.write(
                bytes(wav_data)
            )
            file.flush()
            os.fsync(
                file.fileno()
            )

        os.chmod(
            temporary,
            0o644,
        )

        os.replace(
            temporary,
            destination,
        )

    finally:
        try:
            temporary.unlink(
                missing_ok=True
            )
        except OSError:
            pass

    tone = resolve_alarm_tone(
        safe_name
    )

    if tone is None:
        raise OSError(
            "The alarm tone could not be installed."
        )

    return {
        **tone,
        **metadata,
    }


def _require_editable_alarm_tone(
    value,
):
    tone = resolve_alarm_tone(
        value
    )

    if tone is None:
        raise FileNotFoundError(
            "Alarm tone was not found."
        )

    if (
        normalize_alarm_tone_name(
            tone["name"]
        )
        == normalize_alarm_tone_name(
            DEFAULT_ALARM_TONE_NAME
        )
    ):
        raise PermissionError(
            "The default Saturn Alarm 1 tone "
            "cannot be renamed or deleted."
        )

    return tone


def rename_alarm_tone(
    current_name,
    new_name,
):
    """
    Rename a non-default custom tone within the tone directory.
    """

    tone = _require_editable_alarm_tone(
        current_name
    )
    safe_name = validate_alarm_tone_name(
        new_name
    )

    existing = resolve_alarm_tone(
        safe_name
    )

    if (
        existing is not None
        and existing["filename"]
        != tone["filename"]
    ):
        raise FileExistsError(
            f"An alarm tone named {safe_name} already exists."
        )

    source = Path(
        tone["path"]
    )
    destination = (
        ensure_alarm_tones_directory()
        / f"{safe_name}.wav"
    )

    if source == destination:
        return tone

    os.replace(
        source,
        destination,
    )

    renamed = resolve_alarm_tone(
        safe_name
    )

    if renamed is None:
        raise OSError(
            "The alarm tone could not be renamed."
        )

    return renamed


def delete_alarm_tone(
    value,
):
    """
    Delete a non-default custom tone.
    """

    tone = _require_editable_alarm_tone(
        value
    )

    Path(
        tone["path"]
    ).unlink()

    return {
        "name": tone["name"],
        "filename": tone["filename"],
    }

import io
import wave

import pytest

from assistant_tools import alarm_tones


def make_wav(
    *,
    channels=1,
    sample_width=2,
    sample_rate=44100,
    duration_seconds=0.1,
):
    frame_count = int(
        sample_rate * duration_seconds
    )

    buffer = io.BytesIO()

    with wave.open(
        buffer,
        "wb",
    ) as audio:
        audio.setnchannels(
            channels
        )
        audio.setsampwidth(
            sample_width
        )
        audio.setframerate(
            sample_rate
        )
        audio.writeframes(
            b"\x00"
            * frame_count
            * channels
            * sample_width
        )

    return buffer.getvalue()


@pytest.fixture
def isolated_tones(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        alarm_tones,
        "DEFAULT_ALARM_TONES_DIRECTORY",
        tmp_path / "alarm_tones",
    )
    monkeypatch.delenv(
        alarm_tones.ALARM_TONES_DIRECTORY_ENV,
        raising=False,
    )

    return (
        tmp_path
        / "alarm_tones"
    )


def test_install_valid_alarm_tone(
    isolated_tones,
):
    result = alarm_tones.install_alarm_tone(
        "Morning Bell",
        make_wav(),
    )

    assert result["name"] == "Morning Bell"
    assert result["filename"] == "Morning Bell.wav"
    assert result["channels"] == 1
    assert result["sample_bits"] == 16
    assert result["sample_rate"] == 44100
    assert result["duration_seconds"] == pytest.approx(
        0.1
    )

    installed = (
        isolated_tones
        / "Morning Bell.wav"
    )

    assert installed.is_file()


@pytest.mark.parametrize(
    "name",
    [
        "",
        "../escape",
        r"C:\tone",
        "nested/tone",
        ".hidden",
        "bad?.wav",
        "a" * 81,
    ],
ids=['case-1', 'case-2', 'case-3', 'case-4', 'case-5', 'case-6', 'case-7'],
)
def test_unsafe_tone_names_are_rejected(
    isolated_tones,
    name,
):
    with pytest.raises(
        ValueError
    ):
        alarm_tones.install_alarm_tone(
            name,
            make_wav(),
        )


@pytest.mark.parametrize(
    (
        "wav_data",
        "message",
    ),
    [
        (
            b"not a wav",
            "Invalid WAV",
        ),
        (
            make_wav(
                sample_width=3
            ),
            "signed 16-bit",
        ),
        (
            make_wav(
                sample_rate=22050
            ),
            "44100 or 48000",
        ),
        (
            make_wav(
                channels=3
            ),
            "mono or stereo",
        ),
        (
            make_wav(
                duration_seconds=31
            ),
            "30 seconds or shorter",
        ),
    ],
ids=['case-1', 'case-2', 'case-3', 'case-4', 'case-5'],
)
def test_incompatible_wav_is_rejected(
    isolated_tones,
    wav_data,
    message,
):
    with pytest.raises(
        ValueError,
        match=message,
    ):
        alarm_tones.install_alarm_tone(
            "Invalid Tone",
            wav_data,
        )


def test_duplicate_tone_is_rejected(
    isolated_tones,
):
    alarm_tones.install_alarm_tone(
        "Zen Gong",
        make_wav(),
    )

    with pytest.raises(
        FileExistsError
    ):
        alarm_tones.install_alarm_tone(
            "zen-gong",
            make_wav(),
        )


def test_custom_tone_can_be_renamed_and_deleted(
    isolated_tones,
):
    alarm_tones.install_alarm_tone(
        "Zen Gong",
        make_wav(),
    )

    renamed = alarm_tones.rename_alarm_tone(
        "Zen Gong",
        "Morning Gong",
    )

    assert renamed["name"] == "Morning Gong"
    assert (
        alarm_tones.resolve_alarm_tone(
            "Zen Gong"
        )
        is None
    )

    deleted = alarm_tones.delete_alarm_tone(
        "Morning Gong"
    )

    assert deleted["filename"] == "Morning Gong.wav"
    assert (
        alarm_tones.resolve_alarm_tone(
            "Morning Gong"
        )
        is None
    )


def test_default_tone_is_protected(
    isolated_tones,
):
    alarm_tones.install_alarm_tone(
        "Saturn Alarm 1",
        make_wav(),
    )

    with pytest.raises(
        PermissionError
    ):
        alarm_tones.rename_alarm_tone(
            "Saturn Alarm 1",
            "Replacement",
        )

    with pytest.raises(
        PermissionError
    ):
        alarm_tones.delete_alarm_tone(
            "Saturn Alarm 1"
        )


def test_tone_name_accepts_wav_extension(
    isolated_tones,
):
    result = alarm_tones.install_alarm_tone(
        "Soft Chime.wav",
        make_wav(),
    )

    assert result["filename"] == "Soft Chime.wav"

from pathlib import Path

import pytest

from assistant_tools import alarm_tones


@pytest.fixture
def isolated_tone_directory(
    tmp_path,
    monkeypatch,
):
    tone_directory = (
        tmp_path
        / "alarm_tones"
    )

    monkeypatch.setenv(
        "SATURN_ALARM_TONES_DIR",
        str(tone_directory),
    )

    return tone_directory


def write_tone(
    tone_directory,
    filename,
):
    tone_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = (
        tone_directory
        / filename
    )

    path.write_bytes(
        b"RIFF"
        + (b"\x00" * 32)
        + b"WAVE"
    )

    return path


def test_tone_directory_is_created(
    isolated_tone_directory,
):
    result = (
        alarm_tones.ensure_alarm_tones_directory()
    )

    assert result == (
        isolated_tone_directory.resolve()
    )
    assert result.is_dir()


def test_only_wav_files_are_discovered(
    isolated_tone_directory,
):
    write_tone(
        isolated_tone_directory,
        "Morning Bell.wav",
    )
    write_tone(
        isolated_tone_directory,
        "ignored.mp3",
    )
    write_tone(
        isolated_tone_directory,
        "ignored.txt",
    )

    tones = alarm_tones.list_alarm_tones()

    assert [
        tone["filename"]
        for tone in tones
    ] == [
        "Morning Bell.wav",
    ]


def test_tone_names_are_friendly_and_sorted(
    isolated_tone_directory,
):
    write_tone(
        isolated_tone_directory,
        "Zen_Gong.wav",
    )
    write_tone(
        isolated_tone_directory,
        "bright-bell.WAV",
    )

    tones = alarm_tones.list_alarm_tones()

    assert [
        tone["name"]
        for tone in tones
    ] == [
        "bright bell",
        "Zen Gong",
    ]


@pytest.mark.parametrize(
    "requested",
    [
        "Zen Gong",
        "zen gong",
        "ZEN_GONG",
        "zen-gong",
        "Zen_Gong.wav",
    ],
)
def test_resolve_tone_by_spoken_name_or_filename(
    isolated_tone_directory,
    requested,
):
    path = write_tone(
        isolated_tone_directory,
        "Zen_Gong.wav",
    )

    result = alarm_tones.resolve_alarm_tone(
        requested
    )

    assert result is not None
    assert result["name"] == "Zen Gong"
    assert result["filename"] == "Zen_Gong.wav"
    assert result["path"] == str(
        path.resolve()
    )


def test_unknown_tone_returns_none(
    isolated_tone_directory,
):
    write_tone(
        isolated_tone_directory,
        "Morning Bell.wav",
    )

    assert (
        alarm_tones.resolve_alarm_tone(
            "Ocean"
        )
        is None
    )


def test_nested_files_are_not_discovered(
    isolated_tone_directory,
):
    write_tone(
        isolated_tone_directory,
        "Morning Bell.wav",
    )

    nested = (
        isolated_tone_directory
        / "nested"
    )

    write_tone(
        nested,
        "Hidden.wav",
    )

    tones = alarm_tones.list_alarm_tones()

    assert [
        tone["filename"]
        for tone in tones
    ] == [
        "Morning Bell.wav",
    ]


def test_path_input_cannot_escape_tone_directory(
    isolated_tone_directory,
    tmp_path,
):
    outside = write_tone(
        tmp_path,
        "Outside.wav",
    )

    assert outside.exists()

    assert (
        alarm_tones.resolve_alarm_tone(
            str(outside)
        )
        is None
    )


def test_symlink_is_not_exposed(
    isolated_tone_directory,
    tmp_path,
):
    outside = write_tone(
        tmp_path,
        "Outside.wav",
    )

    isolated_tone_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    link = (
        isolated_tone_directory
        / "Linked.wav"
    )

    try:
        link.symlink_to(
            outside
        )
    except (
        OSError,
        NotImplementedError,
    ):
        pytest.skip(
            "Symlinks are unavailable on this Windows setup."
        )

    assert alarm_tones.list_alarm_tones() == []

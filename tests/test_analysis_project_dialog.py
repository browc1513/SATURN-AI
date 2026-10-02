"""Exercise desktop form parsing through the real project writer."""

import pytest

from gui.project_dialog import create_project
from data_analysis.projects import load_project


@pytest.fixture
def fields():
    return {
        "name": " Test project ", "reference": "501",
        "display_start": "-50", "display_stop": "50",
        "baseline_start": "-30", "baseline_stop": "-20",
        "event_start": "20", "event_stop": "30",
    }


@pytest.fixture
def shot(tmp_path):
    path = tmp_path / "shot.CSV"
    path.write_text(
        '"Model","SL1000"\n'
        '"BlockNumber","1"\n'
        '"TraceName","ND",\n'
        'BlockSize,1000,\n'
        'Date,2025/10/23,\n'
        'Time,16:34:38,\n'
        'VUnit,V,\n'
        'HResolution,1e-7,\n'
        'HUnit,s,\n'
        + ',2\n' * 1000,
        encoding="utf-8",
    )
    return path


def test_form_saves_reopenable_project_and_preserves_source(tmp_path, shot, fields):
    original = shot.read_bytes()
    destination = tmp_path / "project.json"
    created = create_project(destination, [shot], fields)
    assert load_project(destination) == created
    assert created["name"] == "Test project"
    assert created["reference_sample_one_based"] == 501
    assert created["measurement_windows_us"] == {
        "Baseline": [-30, -20], "Candidate event": [20, 30],
    }
    assert shot.read_bytes() == original


@pytest.mark.parametrize("key,value", [
    ("name", " "), ("reference", "0"), ("reference", "1.5"),
    ("reference", "1001"), ("display_start", "nan"),
    ("event_stop", "inf"), ("baseline_start", "abc"),
    ("baseline_stop", "-40"), ("event_stop", "60"),
])
def test_invalid_form_does_not_write_project(tmp_path, shot, fields, key, value):
    fields[key] = value
    destination = tmp_path / "project.json"
    with pytest.raises(ValueError):
        create_project(destination, [shot], fields)
    assert not destination.exists()


def test_existing_project_is_preserved(tmp_path, shot, fields):
    destination = tmp_path / "project.json"
    destination.write_text("existing", encoding="utf-8")
    with pytest.raises(FileExistsError):
        create_project(destination, [shot], fields)
    assert destination.read_text(encoding="utf-8") == "existing"


def test_duplicate_sources_do_not_write_project(tmp_path, shot, fields):
    destination = tmp_path / "project.json"
    with pytest.raises(ValueError, match="Duplicate"):
        create_project(destination, [shot, shot], fields)
    assert not destination.exists()


def test_no_sources_do_not_write_project(tmp_path, fields):
    destination = tmp_path / "project.json"
    with pytest.raises(ValueError, match="Select"):
        create_project(destination, [], fields)
    assert not destination.exists()

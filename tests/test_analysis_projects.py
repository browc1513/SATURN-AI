import pytest

from data_analysis.projects import load_project, save_project


def shot_file(tmp_path):
    path = tmp_path / "R24913.CSV"
    path.write_text(
        '"Model","SL1000"\n'
        '"BlockNumber","1"\n'
        '"TraceName","ND",\n'
        'BlockSize,3,\n'
        'Date,2025/10/23,\n'
        'Time,16:34:38,\n'
        'VUnit,V,\n'
        'HResolution,1e-7,\n'
        'HUnit,s,\n'
        ',-1\n,0\n,2\n',
        encoding="utf-8",
    )
    return path


def test_project_reopens_and_preserves_source(tmp_path):
    shot = shot_file(tmp_path)
    original = shot.read_bytes()
    project = tmp_path / "project.json"
    saved = save_project(project, "Reference shots", [shot], 2)
    assert load_project(project) == saved
    assert shot.read_bytes() == original


def test_changed_source_is_rejected(tmp_path):
    shot = shot_file(tmp_path)
    project = tmp_path / "project.json"
    save_project(project, "Reference shots", [shot], 2)
    original = shot.read_bytes()
    changed = original.replace(b",2", b",3")
    assert changed != original
    shot.write_bytes(changed)
    with pytest.raises(ValueError, match="Source file changed"):
        load_project(project)


def test_existing_project_is_not_overwritten(tmp_path):
    shot = shot_file(tmp_path)
    project = tmp_path / "project.json"
    save_project(project, "Original", [shot], 2)
    original = project.read_bytes()
    with pytest.raises(FileExistsError):
        save_project(project, "Replacement", [shot], 2)
    assert project.read_bytes() == original


def test_duplicate_source_is_rejected(tmp_path):
    shot = shot_file(tmp_path)
    with pytest.raises(ValueError, match="Duplicate"):
        save_project(tmp_path / "project.json", "Duplicate", [shot, shot], 2)


def test_project_preserves_custom_window(tmp_path):
    shot = shot_file(tmp_path)
    project = tmp_path / "custom.json"
    save_project(
        project, "Custom window", [shot], 2,
        start_us=-50.0, stop_us=100.0,
    )
    window = load_project(project)["window_seconds"]
    assert window == pytest.approx([-50e-6, 100e-6])


@pytest.mark.parametrize(
    "start,stop",
    [(10.0, 10.0), (20.0, 10.0), (float("nan"), 100.0)],
)
def test_invalid_project_window_is_rejected(tmp_path, start, stop):
    shot = shot_file(tmp_path)
    project = tmp_path / "invalid.json"
    with pytest.raises(ValueError, match="Window"):
        save_project(
            project, "Invalid", [shot], 2,
            start_us=start, stop_us=stop,
        )
    assert not project.exists()

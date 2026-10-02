import json

import numpy as np
import pytest

from data_analysis.projects import save_project
from data_analysis.spectrum_report import build_report as original_report
from data_analysis.window_sensitivity import build_report, save_report, window_variants


@pytest.fixture
def project_files(tmp_path):
    shot = tmp_path / "shot.CSV"
    values = 3 + 2 * np.sin(2 * np.pi * np.arange(1000) / 10)
    shot.write_text(
        '"Model","SL1000"\n'
        '"BlockNumber","1"\n'
        '"TraceName","ND",\n'
        'BlockSize,1000,\n'
        'Date,2025/10/23,\n'
        'Time,16:34:38,\n'
        'VUnit,V,\n'
        'HResolution,1e-7,\n'
        'HUnit,s,\n'
        + "".join(f",{value:.17g}\n" for value in values),
        encoding="utf-8",
    )
    project = tmp_path / "project.json"
    save_project(
        project, "Sensitivity test", [shot], 501,
        start_us=-50, stop_us=50,
        measurement_windows={
            "Baseline": [-30, -20], "Candidate event": [20, 30],
        },
    )
    return project, shot


def test_variations_have_explicit_boundaries():
    assert window_variants([20, 30]) == {
        "Original": [20, 30], "Earlier": [18, 28],
        "Later": [22, 32], "Wider": [17.5, 32.5],
    }


def test_known_stationary_signal_and_original_match(project_files):
    project, shot = project_files
    originals = [project.read_bytes(), shot.read_bytes()]
    previous = original_report(project)
    report = build_report(project)
    record = report["shots"][0]
    for name, cases in record["windows"].items():
        assert cases["Original"]["spectrum"] == previous["shots"][0]["spectra"][name]
        for label, result in cases.items():
            assert result["measurement"]["sample_count"] == (
                150 if label == "Wider" else 100
            )
            assert result["spectrum"]["integrated_power_v2"] == pytest.approx(2)
            assert result["variance_ratio_to_original"] == pytest.approx(1)
    assert [project.read_bytes(), shot.read_bytes()] == originals


def test_save_round_trip_and_overwrite_protection(tmp_path, project_files):
    project, _ = project_files
    output = tmp_path / "sensitivity.json"
    report = save_report(project, output)
    assert json.loads(output.read_text(encoding="utf-8")) == report
    original = output.read_bytes()
    with pytest.raises(FileExistsError):
        save_report(project, output)
    assert output.read_bytes() == original


def test_changed_source_creates_no_report(tmp_path, project_files):
    project, shot = project_files
    lines = shot.read_text(encoding="utf-8").splitlines()
    lines[-1] = ",123.456"
    shot.write_text("\n".join(lines) + "\n", encoding="utf-8")
    output = tmp_path / "sensitivity.json"
    with pytest.raises(ValueError, match="Source file changed"):
        save_report(project, output)
    assert not output.exists()


def test_variant_outside_display_creates_no_report(tmp_path, project_files):
    _, shot = project_files
    project = tmp_path / "edge.json"
    save_project(
        project, "Edge", [shot], 501, start_us=-50, stop_us=50,
        measurement_windows={"Baseline": [-49, -39]},
    )
    output = tmp_path / "sensitivity.json"
    with pytest.raises(ValueError, match="outside the saved display"):
        save_report(project, output)
    assert not output.exists()


def test_zero_variance_ratio_is_explicit(tmp_path, project_files):
    _, shot = project_files
    constant = tmp_path / "constant.CSV"
    header = shot.read_text(encoding="utf-8").splitlines()[:9]
    constant.write_text(
        "\n".join(header) + "\n" + ",2\n" * 1000, encoding="utf-8"
    )
    project = tmp_path / "constant.json"
    save_project(
        project, "Constant", [constant], 501, start_us=-50, stop_us=50,
        measurement_windows={"Baseline": [-30, -20]},
    )
    for result in build_report(project)["shots"][0]["windows"]["Baseline"].values():
        assert result["spectrum"]["integrated_power_v2"] == 0
        assert result["variance_ratio_to_original"] is None

import json

import numpy as np
import pytest

from data_analysis.projects import save_project
from data_analysis.spectrum_report import build_report, main, save_report
from data_analysis.spectrum_viewer import build_figure


@pytest.fixture
def project_files(tmp_path):
    shot = tmp_path / "shot.CSV"
    values = 3.0 + 2.0 * np.sin(2 * np.pi * np.arange(1000) / 10)
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
    saved = save_project(
        project, "Spectrum test", [shot], 501,
        start_us=-50, stop_us=50,
        measurement_windows={
            "Baseline": [-30, -20],
            "Candidate event": [20, 30],
        },
    )
    return project, shot, saved


def test_report_preserves_sources_and_known_spectrum(project_files):
    project, shot, saved = project_files
    original_project = project.read_bytes()
    original_shot = shot.read_bytes()
    report = build_report(project)

    assert report["project_name"] == "Spectrum test"
    assert report["project"] == str(project.resolve())
    record = report["shots"][0]
    assert record["sha256"] == saved["shots"][0]["sha256"]
    assert record["source_path"] == str(shot.resolve())
    assert record["reference_sample_one_based"] == 501
    assert record["correction_seconds"] == 0.0
    assert record["reference_provisional"] is True
    for spectrum in record["spectra"].values():
        assert spectrum["metadata"]["sample_count"] == 100
        assert spectrum["integrated_power_v2"] == pytest.approx(2.0)
        peak = int(np.argmax(spectrum["power_spectral_density_v2_per_hz"]))
        assert spectrum["frequency_hz"][peak] == pytest.approx(1e6)
    assert project.read_bytes() == original_project
    assert shot.read_bytes() == original_shot


def test_saved_report_round_trips_into_viewer(tmp_path, project_files):
    project, _, _ = project_files
    output = tmp_path / "spectra.json"
    report = save_report(project, output)
    reopened = json.loads(output.read_text(encoding="utf-8"))
    assert reopened == report
    figure = build_figure(reopened)
    assert sum(trace.type == "scatter" for trace in figure.data) == 2
    assert figure.layout.meta["report"] == report


def test_changed_source_creates_no_report(tmp_path, project_files):
    project, shot, _ = project_files
    lines = shot.read_text(encoding="utf-8").splitlines()
    assert lines[-1].startswith(",")
    lines[-1] = ",123.456"
    shot.write_text("\n".join(lines) + "\n", encoding="utf-8")
    output = tmp_path / "spectra.json"
    with pytest.raises(ValueError, match="Source file changed"):
        save_report(project, output)
    assert not output.exists()


def test_missing_windows_creates_no_report(tmp_path, project_files):
    _, shot, _ = project_files
    project = tmp_path / "no-windows.json"
    save_project(project, "No windows", [shot], 501)
    output = tmp_path / "spectra.json"
    with pytest.raises(ValueError, match="measurement windows"):
        save_report(project, output)
    assert not output.exists()


def test_existing_report_is_preserved(tmp_path, project_files):
    project, _, _ = project_files
    output = tmp_path / "spectra.json"
    output.write_text("existing report", encoding="utf-8")
    original = output.read_bytes()
    with pytest.raises(FileExistsError, match="already exists"):
        save_report(project, output)
    assert output.read_bytes() == original


def test_command_generates_report(tmp_path, project_files, monkeypatch, capsys):
    project, _, _ = project_files
    output = tmp_path / "command.json"
    monkeypatch.setattr("sys.argv", [
        "spectrum_report", "--project", str(project), "--output", str(output),
    ])
    main()
    assert len(json.loads(output.read_text(encoding="utf-8"))["shots"]) == 1
    assert "Shots: 1; spectra: 2" in capsys.readouterr().out

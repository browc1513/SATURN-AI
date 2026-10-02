import pytest

from gui.analysis_panel import generate_outputs


def test_generation_creates_unique_runs_and_passes_saved_report(tmp_path, monkeypatch):
    from data_analysis import spectrum_report, spectrum_viewer

    calls = []

    def save_report(project, output):
        calls.append(("report", project, output))
        output.write_text("saved report", encoding="utf-8")
        return {"shots": [{"spectra": {"Baseline": {}, "Candidate event": {}}}]}

    def save_viewer(report, output):
        assert report.read_text(encoding="utf-8") == "saved report"
        calls.append(("viewer", report, output))
        output.write_text("saved viewer", encoding="utf-8")

    monkeypatch.setattr(spectrum_report, "save_report", save_report)
    monkeypatch.setattr(spectrum_viewer, "save_viewer", save_viewer)

    first = generate_outputs("project.json", tmp_path)
    second = generate_outputs("project.json", tmp_path)

    assert first["shots"] == 1
    assert first["spectra"] == 2
    assert first["viewer"].exists()
    assert first["report"].exists()
    assert first["report"].parent != second["report"].parent
    assert calls[0][1] == "project.json"
    assert calls[1][1] == first["report"]


def test_report_failure_does_not_generate_viewer(tmp_path, monkeypatch):
    from data_analysis import spectrum_report, spectrum_viewer

    def fail(*args):
        raise ValueError("Source file changed")

    def unexpected(*args):
        pytest.fail("Viewer must not run after report failure.")

    monkeypatch.setattr(spectrum_report, "save_report", fail)
    monkeypatch.setattr(spectrum_viewer, "save_viewer", unexpected)

    with pytest.raises(RuntimeError, match="Source file changed"):
        generate_outputs("project.json", tmp_path)
    assert not list(tmp_path.rglob("spectra.html"))


def test_viewer_failure_keeps_completed_report(tmp_path, monkeypatch):
    from data_analysis import spectrum_report, spectrum_viewer

    def report(project, output):
        output.write_text("completed report", encoding="utf-8")
        return {"shots": []}

    def fail(*args):
        raise ValueError("Viewer failed")

    monkeypatch.setattr(spectrum_report, "save_report", report)
    monkeypatch.setattr(spectrum_viewer, "save_viewer", fail)

    with pytest.raises(RuntimeError, match="completed output files"):
        generate_outputs("project.json", tmp_path)
    reports = list(tmp_path.rglob("spectra.json"))
    assert len(reports) == 1
    assert reports[0].read_text(encoding="utf-8") == "completed report"

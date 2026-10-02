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


def test_raw_preview_preserves_project_sources_and_saved_settings(tmp_path):
    from html.parser import HTMLParser
    from data_analysis.projects import save_project
    from gui.analysis_panel import generate_raw_preview

    shot = tmp_path / "shot.CSV"
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
        + ',2\n' * 1000,
        encoding="utf-8",
    )
    project = tmp_path / "project.json"
    save_project(
        project, "Raw preview test", [shot],
        reference_sample=501, start_us=-50, stop_us=50,
        measurement_windows={
            "Baseline": [-30, -20], "Candidate event": [20, 30],
        },
    )
    originals = [shot.read_bytes(), project.read_bytes()]
    first = generate_raw_preview(project, tmp_path / "output")
    second = generate_raw_preview(project, tmp_path / "output")
    assert first["shots"] == 1
    assert first["viewer"] != second["viewer"]
    assert [shot.read_bytes(), project.read_bytes()] == originals
    html = first["viewer"].read_text(encoding="utf-8")
    assert "Raw preview test" in html
    assert '"reference_sample_one_based":501' in html
    import json
    import re

    match = re.search(r'"requested_window_us"\s*:\s*(\[[^\]]*\])', html)
    assert match is not None
    assert json.loads(match.group(1)) == pytest.approx([-50.0, 50.0])
    assert '"Baseline"' in html
    assert '"Candidate event"' in html

    class Scripts(HTMLParser):
        def __init__(self):
            super().__init__()
            self.sources = []

        def handle_starttag(self, tag, attrs):
            if tag.lower() == "script":
                self.sources.extend(
                    value for name, value in attrs if name.lower() == "src"
                )

    scripts = Scripts()
    scripts.feed(html)
    assert scripts.sources == []


def test_raw_preview_rejects_source_changed_during_loading(tmp_path, monkeypatch):
    import plotly.graph_objects as go
    from data_analysis import projects, viewer
    from gui.analysis_panel import generate_raw_preview

    project = {
        "shots": [{"path": "shot.CSV", "filename": "shot.CSV", "sha256": "saved"}],
        "reference_sample_one_based": 501,
        "window_seconds": [-50e-6, 50e-6],
        "measurement_windows_us": {"Baseline": [-30, -20]},
    }
    monkeypatch.setattr(projects, "load_project", lambda path: project)

    def changed(paths, **settings):
        assert paths == ["shot.CSV"]
        assert settings["reference_sample"] == 501
        assert settings["start_us"] == pytest.approx(-50)
        assert settings["stop_us"] == pytest.approx(50)
        assert settings["measurement_windows"] == {"Baseline": [-30, -20]}
        figure = go.Figure()
        figure.update_layout(meta={"shots": [{"sha256": "changed"}]})
        return figure

    monkeypatch.setattr(viewer, "build_figure", changed)
    output = tmp_path / "output"
    with pytest.raises(ValueError, match="Source file changed"):
        generate_raw_preview("project.json", output)
    assert not output.exists()


def test_raw_preview_stops_when_project_verification_fails(tmp_path, monkeypatch):
    from data_analysis import projects, viewer
    from gui.analysis_panel import generate_raw_preview

    def fail(path):
        raise ValueError("Source file changed")

    def unexpected(*args, **kwargs):
        pytest.fail("Waveforms must not load after project verification fails.")

    monkeypatch.setattr(projects, "load_project", fail)
    monkeypatch.setattr(viewer, "build_figure", unexpected)
    with pytest.raises(ValueError, match="Source file changed"):
        generate_raw_preview("project.json", tmp_path / "output")
    assert not (tmp_path / "output").exists()


def test_sensitivity_generation_uses_saved_report_and_unique_runs(tmp_path, monkeypatch):
    from data_analysis import window_sensitivity, sensitivity_viewer

    calls = []

    def save_report(project, output):
        calls.append(("report", project, output))
        output.write_text("saved sensitivity report", encoding="utf-8")
        return {"shots": [{"windows": {
            name: {variant: {} for variant in ("Original", "Earlier", "Later", "Wider")}
            for name in ("Baseline", "Candidate event")
        }}]}

    def save_viewer(report, output):
        assert report.read_text(encoding="utf-8") == "saved sensitivity report"
        calls.append(("viewer", report, output))
        output.write_text("viewer", encoding="utf-8")

    monkeypatch.setattr(window_sensitivity, "save_report", save_report)
    monkeypatch.setattr(sensitivity_viewer, "save_viewer", save_viewer)
    first = generate_outputs("project.json", tmp_path, operation="sensitivity")
    second = generate_outputs("project.json", tmp_path, operation="sensitivity")

    assert first["shots"] == 1
    assert first["comparisons"] == 2
    assert first["window_results"] == 8
    assert first["report"].name == "sensitivity.json"
    assert first["viewer"].name == "sensitivity.html"
    assert first["viewer"].exists()
    assert first["report"].parent != second["report"].parent
    assert calls[0][1] == "project.json"
    assert calls[1][1] == first["report"]


def test_sensitivity_report_failure_stops_viewer(tmp_path, monkeypatch):
    from data_analysis import window_sensitivity, sensitivity_viewer

    def fail(*args):
        raise ValueError("Source file changed")

    def unexpected(*args):
        pytest.fail("Viewer must not run after report failure.")

    monkeypatch.setattr(window_sensitivity, "save_report", fail)
    monkeypatch.setattr(sensitivity_viewer, "save_viewer", unexpected)
    with pytest.raises(RuntimeError, match="Source file changed"):
        generate_outputs("project.json", tmp_path, operation="sensitivity")
    assert not list(tmp_path.rglob("sensitivity.html"))


def test_sensitivity_viewer_failure_keeps_report(tmp_path, monkeypatch):
    from data_analysis import window_sensitivity, sensitivity_viewer

    def report(project, output):
        output.write_text("completed sensitivity report", encoding="utf-8")
        return {"shots": []}

    def fail(*args):
        raise ValueError("Viewer failed")

    monkeypatch.setattr(window_sensitivity, "save_report", report)
    monkeypatch.setattr(sensitivity_viewer, "save_viewer", fail)
    with pytest.raises(RuntimeError, match="completed output files"):
        generate_outputs("project.json", tmp_path, operation="sensitivity")
    reports = list(tmp_path.rglob("sensitivity.json"))
    assert len(reports) == 1
    assert reports[0].read_text(encoding="utf-8") == "completed sensitivity report"


def test_worker_routes_sensitivity_and_queues_result(tmp_path):
    from queue import Queue
    from unittest.mock import patch
    from gui.analysis_panel import AnalysisPanel

    panel = AnalysisPanel.__new__(AnalysisPanel)
    panel.results = Queue()
    expected = {"viewer": tmp_path / "sensitivity.html", "comparisons": 2}
    with patch("gui.analysis_panel.generate_outputs", return_value=expected) as generate:
        panel.worker("project.json", tmp_path, "sensitivity")
    generate.assert_called_once_with("project.json", tmp_path, operation="sensitivity")
    assert panel.results.get_nowait() == ("success", expected)

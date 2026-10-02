from copy import deepcopy
from html.parser import HTMLParser
import json

import pytest

from data_analysis.sensitivity_viewer import build_figure, save_viewer, VARIANTS


@pytest.fixture
def report():
    cases = {
        label: {
            "requested_window_us": [20, 30],
            "measurement": {"sample_count": 4},
            "variance_ratio_to_original": 1.0,
            "spectrum": {
                "frequency_hz": [0, 1e6, 2e6],
                "power_spectral_density_v2_per_hz": [0, 2e-6, 0],
                "integrated_power_v2": 2.0,
                "metadata": {"window": "rectangular"},
            },
        }
        for label in VARIANTS
    }
    return {
        "schema_version": 1, "report_type": "window_sensitivity",
        "shots": [
            {"filename": f"shot-{index}.CSV", "windows": {
                "Baseline": deepcopy(cases), "Candidate event": deepcopy(cases),
            }}
            for index in range(3)
        ],
    }


def test_selection_keeps_four_spectra_and_matching_table(report):
    original = deepcopy(report)
    figure = build_figure(report)
    assert len(figure.data) == 30
    buttons = figure.layout.updatemenus[0].buttons
    assert len(buttons) == 6
    assert sum(trace.visible is True for trace in figure.data) == 5
    for group_index, button in enumerate(buttons):
        mask = list(button.args[0]["visible"])
        assert mask == [index // 5 == group_index for index in range(30)]
    assert tuple(figure.data[0].x) == (1, 2)
    assert tuple(figure.data[0].y) == (2e-6, None)
    assert figure.data[4].cells.values[4][0] == "2"
    assert figure.layout.meta["report"] == original
    assert figure.layout.meta["display"]["recalculated"] is False
    assert report == original


@pytest.mark.parametrize("case", [
    "type", "missing_variant", "bounds", "samples", "ratio", "density",
])
def test_invalid_report_rejected(report, case):
    result = report["shots"][0]["windows"]["Baseline"]["Original"]
    if case == "type":
        report["report_type"] = "other"
    elif case == "missing_variant":
        del report["shots"][0]["windows"]["Baseline"]["Wider"]
    elif case == "bounds":
        result["requested_window_us"] = [30, 20]
    elif case == "samples":
        result["measurement"]["sample_count"] = True
    elif case == "ratio":
        result["variance_ratio_to_original"] = float("nan")
    else:
        result["spectrum"]["power_spectral_density_v2_per_hz"][1] = -1
    with pytest.raises(ValueError):
        build_figure(report)


def test_undefined_ratio_is_explicit(report):
    report["shots"][0]["windows"]["Baseline"]["Original"]["variance_ratio_to_original"] = None
    figure = build_figure(report)
    assert figure.data[4].cells.values[5][0] == "Undefined"


def test_offline_save_preserves_report_and_output(tmp_path, report):
    source = tmp_path / "report.json"
    source.write_text(json.dumps(report), encoding="utf-8")
    original = source.read_bytes()
    output = tmp_path / "viewer.html"
    save_viewer(source, output)
    assert source.read_bytes() == original

    class Scripts(HTMLParser):
        def __init__(self):
            super().__init__()
            self.sources = []

        def handle_starttag(self, tag, attrs):
            if tag.lower() == "script":
                self.sources.extend(value for key, value in attrs if key == "src")

    scripts = Scripts()
    scripts.feed(output.read_text(encoding="utf-8"))
    assert scripts.sources == []
    saved = output.read_bytes()
    with pytest.raises(FileExistsError):
        save_viewer(source, output)
    assert output.read_bytes() == saved


def test_invalid_report_creates_no_output(tmp_path):
    source = tmp_path / "invalid.json"
    source.write_text("{}", encoding="utf-8")
    output = tmp_path / "viewer.html"
    with pytest.raises(ValueError):
        save_viewer(source, output)
    assert not output.exists()

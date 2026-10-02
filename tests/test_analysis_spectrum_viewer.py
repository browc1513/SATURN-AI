from copy import deepcopy
import json

import numpy as np
import pytest

from data_analysis.spectrum_viewer import build_figure, save_viewer


@pytest.fixture
def report():
    spectrum = {
        "frequency_hz": [0.0, 1e6, 2e6],
        "power_spectral_density_v2_per_hz": [0.0, 2e-6, 0.0],
        "integrated_power_v2": 2.0,
        "metadata": {
            "sample_count": 4,
            "sample_interval_seconds": 2.5e-7,
            "frequency_bin_spacing_hz": 1e6,
            "window": "rectangular",
            "detrending": "subtract selected-window mean",
            "zero_padding": False,
        },
    }
    return {
        "schema_version": 1,
        "project": "saved-project.json",
        "interpretation": "Recorded voltage; neutron origin unconfirmed.",
        "shots": [
            {
                "filename": f"shot-{index}.CSV",
                "sha256": str(index) * 64,
                "reference_sample_one_based": 2,
                "correction_seconds": 0.0,
                "reference_provisional": True,
                "spectra": {
                    "Baseline": deepcopy(spectrum),
                    "Candidate event": deepcopy(spectrum),
                },
            }
            for index in range(3)
        ],
    }


def test_six_traces_preserve_values_styles_and_provenance(report):
    original = deepcopy(report)
    figure = build_figure(report)

    assert sum(trace.type == "scatter" for trace in figure.data) == 6
    np.testing.assert_array_equal(figure.data[0].x, [1.0, 2.0])
    assert tuple(figure.data[0].y) == (2e-6, None)
    assert figure.data[0].line.dash == "dash"
    assert figure.data[1].line.dash == "solid"
    assert figure.data[0].line.color == figure.data[1].line.color
    assert figure.data[0].line.color != figure.data[2].line.color
    assert figure.layout.yaxis.type == "log"
    assert figure.layout.meta["report"] == original
    assert figure.layout.meta["display"]["recalculated"] is False
    assert report == original

    report["shots"][0]["sha256"] = "changed"
    assert figure.layout.meta["report"] == original


@pytest.mark.parametrize("case", [
    "schema", "empty", "mismatch", "negative", "nonfinite",
    "unordered", "nonzero_dc", "nested", "missing_array", "metadata",
])
def test_invalid_reports_are_rejected(report, case):
    spectrum = report["shots"][0]["spectra"]["Baseline"]
    if case == "schema":
        report["schema_version"] = 2
    elif case == "empty":
        report["shots"] = []
    elif case == "mismatch":
        spectrum["frequency_hz"] = [0.0, 1e6]
    elif case == "negative":
        spectrum["power_spectral_density_v2_per_hz"][1] = -1.0
    elif case == "nonfinite":
        spectrum["power_spectral_density_v2_per_hz"][1] = float("nan")
    elif case == "unordered":
        spectrum["frequency_hz"] = [0.0, 2e6, 1e6]
    elif case == "nonzero_dc":
        spectrum["frequency_hz"] = [1.0, 1e6, 2e6]
    elif case == "nested":
        spectrum["frequency_hz"] = [[0.0, 1e6, 2e6]]
    elif case == "missing_array":
        del spectrum["frequency_hz"]
    elif case == "metadata":
        spectrum["metadata"] = None

    with pytest.raises(ValueError, match="Spectrum"):
        build_figure(report)


def test_save_preserves_source_and_refuses_overwrite(tmp_path, report):
    source = tmp_path / "report.json"
    source.write_text(json.dumps(report), encoding="utf-8")
    original = source.read_bytes()
    output = tmp_path / "viewer.html"

    figure = save_viewer(source, output)

    assert sum(trace.type == "scatter" for trace in figure.data) == 6
    assert source.read_bytes() == original
    assert figure.layout.meta["report_path"] == str(source.resolve())
    html = output.read_text(encoding="utf-8")
    assert "Plotly.newPlot" in html
    from html.parser import HTMLParser

    class ScriptSources(HTMLParser):
        def __init__(self):
            super().__init__()
            self.sources = []

        def handle_starttag(self, tag, attrs):
            if tag.lower() == "script":
                for name, value in attrs:
                    if name.lower() == "src":
                        self.sources.append(value)

    scripts = ScriptSources()
    scripts.feed(html)
    assert scripts.sources == []
    saved = output.read_bytes()

    with pytest.raises(FileExistsError, match="already exists"):
        save_viewer(source, output)
    assert output.read_bytes() == saved


def test_invalid_report_does_not_create_output(tmp_path):
    source = tmp_path / "invalid.json"
    source.write_text('{"schema_version": 1, "shots": []}', encoding="utf-8")
    output = tmp_path / "viewer.html"

    with pytest.raises(ValueError):
        save_viewer(source, output)
    assert not output.exists()


def test_selector_shows_matching_spectra_and_table(report):
    figure = build_figure(report)
    buttons = figure.layout.updatemenus[0].buttons
    assert [button.label for button in buttons] == [
        "All shots", "shot-0.CSV", "shot-1.CSV", "shot-2.CSV",
    ]
    tables = [trace for trace in figure.data if trace.type == "table"]
    assert len(tables) == 4
    assert tables[0].visible is True
    assert all(table.visible is False for table in tables[1:])

    all_mask = list(buttons[0].args[0]["visible"])
    assert all_mask == [True] * 7 + [False] * 3
    for shot_index, button in enumerate(buttons[1:]):
        mask = list(button.args[0]["visible"])
        assert len(mask) == len(figure.data)
        assert mask[:6] == [
            index // 2 == shot_index for index in range(6)
        ]
        assert mask[6:] == [False] + [
            index == shot_index for index in range(3)
        ]


def test_power_table_uses_saved_values_without_changing_spectra(report):
    report["shots"][0]["spectra"]["Baseline"]["integrated_power_v2"] = 0.25
    report["shots"][0]["spectra"]["Candidate event"]["integrated_power_v2"] = 2.0
    original = deepcopy(report)
    figure = build_figure(report)
    table = next(trace for trace in figure.data if trace.type == "table")
    assert table.cells.values[1][0] == "0.25"
    assert table.cells.values[2][0] == "2"
    assert table.cells.values[3][0] == "8"
    assert report == original
    assert figure.layout.meta["report"] == original


def test_zero_baseline_and_missing_named_window_are_explicit(report):
    report["shots"][0]["spectra"]["Baseline"]["integrated_power_v2"] = 0.0
    del report["shots"][1]["spectra"]["Candidate event"]
    figure = build_figure(report)
    table = next(trace for trace in figure.data if trace.type == "table")
    assert table.cells.values[1][0] == "0"
    assert table.cells.values[3][0] == "Undefined"
    assert table.cells.values[2][1] == "N/A"
    assert table.cells.values[3][1] == "Undefined"


@pytest.mark.parametrize("power", [-1, float("nan"), float("inf"), True, "2", None])
def test_invalid_saved_power_is_rejected(report, power):
    report["shots"][0]["spectra"]["Baseline"]["integrated_power_v2"] = power
    with pytest.raises(ValueError, match="Spectrum integrated power"):
        build_figure(report)

"""Display saved voltage spectra without recalculating or modifying them."""

import argparse
from copy import deepcopy
from html import escape
import json
import math
from pathlib import Path

import numpy as np
import plotly.graph_objects as go


def _comparison_row(shot):
    spectra = shot["spectra"]
    baseline = spectra.get("Baseline", {}).get("integrated_power_v2")
    event = spectra.get("Candidate event", {}).get("integrated_power_v2")
    ratio = None
    if baseline is not None and event is not None and baseline > 0:
        ratio = event / baseline
        if not math.isfinite(ratio):
            ratio = None
    return [
        escape(shot["filename"]),
        "N/A" if baseline is None else f"{baseline:.6g}",
        "N/A" if event is None else f"{event:.6g}",
        "Undefined" if ratio is None else f"{ratio:.6g}",
    ]


def _power_table(rows, visible):
    return go.Table(
        visible=visible,
        domain={"x": [0, 1], "y": [0, 0.23]},
        header={"values": [
            "Shot", "Baseline variance (V?)",
            "Event variance (V?)", "Event / baseline",
        ]},
        cells={"values": list(map(list, zip(*rows)))},
    )


def build_figure(report):
    """Build an interactive spectrum comparison with saved provenance."""
    if (
        not isinstance(report, dict)
        or report.get("schema_version") != 1
        or not isinstance(report.get("shots"), list)
        or not report["shots"]
    ):
        raise ValueError("Spectrum report must contain schema version 1 and shots.")

    figure = go.Figure()
    colors = ["#2563eb", "#dc2626", "#059669"]
    styles = ["dash", "solid", "dot", "dashdot", "longdash"]
    window_styles = {}
    maximum_frequency = 0.0

    for index, shot in enumerate(report["shots"]):
        if (
            not isinstance(shot, dict)
            or not isinstance(shot.get("filename"), str)
            or not shot["filename"].strip()
            or not isinstance(shot.get("spectra"), dict)
            or not shot["spectra"]
        ):
            raise ValueError("Spectrum report contains an invalid shot.")

        for name, spectrum in shot["spectra"].items():
            if (
                not isinstance(name, str)
                or not name.strip()
                or not isinstance(spectrum, dict)
                or not isinstance(spectrum.get("metadata"), dict)
            ):
                raise ValueError("Spectrum report contains an invalid window.")

            try:
                frequency = np.asarray(spectrum["frequency_hz"], dtype=float)
                density = np.asarray(
                    spectrum["power_spectral_density_v2_per_hz"], dtype=float
                )
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError("Spectrum arrays must be numeric.") from exc

            if (
                frequency.ndim != 1
                or density.ndim != 1
                or frequency.size < 2
                or frequency.shape != density.shape
                or not np.all(np.isfinite(frequency))
                or not np.all(np.isfinite(density))
                or frequency[0] != 0
                or np.any(np.diff(frequency) <= 0)
                or np.any(density < 0)
            ):
                raise ValueError("Spectrum arrays are invalid.")

            power = spectrum.get("integrated_power_v2")
            if (
                type(power) not in (int, float)
                or not math.isfinite(power)
                or power < 0
            ):
                raise ValueError("Spectrum integrated power must be finite and nonnegative.")

            # Keep zero-power bins as gaps; logarithmic axes cannot show zero.
            selected = frequency > 0
            values = [
                float(value) if value > 0 else None
                for value in density[selected]
            ]
            if name not in window_styles:
                if name == "Baseline":
                    window_styles[name] = "dash"
                elif name == "Candidate event":
                    window_styles[name] = "solid"
                else:
                    window_styles[name] = styles[len(window_styles) % len(styles)]

            figure.add_trace(go.Scatter(
                x=(frequency[selected] / 1e6).tolist(),
                y=values,
                mode="lines+markers",
                name=f'{escape(shot["filename"])} — {escape(name)}',
                line={
                    "color": colors[index % len(colors)],
                    "dash": window_styles[name],
                },
                marker={"size": 4},
                connectgaps=False,
                hovertemplate=(
                    "%{x:.3f} MHz<br>%{y:.6g} V²/Hz"
                    "<extra>%{fullData.name}</extra>"
                ),
                meta={
                    "shot_index": index,
                    "window": name,
                    "processing": deepcopy(spectrum["metadata"]),
                },
            ))
            maximum_frequency = max(maximum_frequency, float(frequency[-1]))

    spectrum_count = len(figure.data)
    rows = [_comparison_row(shot) for shot in report["shots"]]
    figure.add_trace(_power_table(rows, visible=True))
    for row in rows:
        figure.add_trace(_power_table([row], visible=False))

    total_count = len(figure.data)
    all_visible = [
        index <= spectrum_count for index in range(total_count)
    ]
    buttons = [{
        "label": "All shots",
        "method": "update",
        "args": [{"visible": all_visible}],
    }]
    for shot_index, shot in enumerate(report["shots"]):
        visible = [
            trace.meta["shot_index"] == shot_index
            for trace in figure.data[:spectrum_count]
        ]
        visible += [False] + [
            index == shot_index for index in range(len(rows))
        ]
        buttons.append({
            "label": escape(shot["filename"]),
            "method": "update",
            "args": [{"visible": visible}],
        })

    figure.update_layout(
        updatemenus=[{
            "buttons": buttons,
            "active": 0,
            "x": 1.03,
            "y": 1.0,
            "xanchor": "left",
            "yanchor": "top",
            "direction": "down",
        }],
        title=(
            "Baseline and candidate-event voltage spectra"
            "<br><sup>Saved spectra · DC omitted · zero-power bins shown as gaps"
            "<br>Exploratory recorded voltage; neutron origin unconfirmed</sup>"
        ),
        template="plotly_white",
        xaxis_title="Frequency (MHz)",
        yaxis_title="Power spectral density (V²/Hz)",
        yaxis_type="log",
        hovermode="closest",
        height=1000,
        yaxis={"domain": [0.43, 1]},
        legend={"orientation": "h", "y": 0.33, "x": 0},
        margin={"t": 180, "b": 60, "r": 230},
        annotations=[{
            "text": (
                "Table uses saved full-spectrum voltage variance, including DC. "
                "Ratio is not neutron yield or signal-to-noise ratio."
            ),
            "xref": "paper", "yref": "paper",
            "x": 0, "y": 0.27, "xanchor": "left",
            "showarrow": False, "font": {"size": 11},
        }],
        meta={
            "report": deepcopy(report),
            "display": {
                "dc_omitted": True,
                "zero_power_bins": "gaps",
                "frequency_unit": "MHz",
                "density_unit": "V^2/Hz",
                "recalculated": False,
            },
        },
    )
    figure.update_xaxes(range=[0, maximum_frequency / 1e6])
    return figure


def save_viewer(report_path, output_path):
    """Write a standalone HTML viewer; refuse to replace an existing file."""
    source = Path(report_path)
    output = Path(output_path)
    if output.exists():
        raise FileExistsError("Output already exists; choose another filename.")

    report = json.loads(source.read_text(encoding="utf-8"))
    figure = build_figure(report)
    figure.layout.meta["report_path"] = str(source.resolve())
    html = figure.to_html(
        full_html=True,
        include_plotlyjs=True,
        config={"scrollZoom": True, "displaylogo": False},
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as stream:
        stream.write(html)
    return figure


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    figure = save_viewer(args.report, args.output)
    print(f"Saved: {Path(args.output).resolve()}")
    count = sum(trace.type == "scatter" for trace in figure.data)
    print(f"Spectra displayed: {count}")


if __name__ == "__main__":
    main()

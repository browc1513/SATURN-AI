"""Display saved voltage spectra without recalculating or modifying them."""

import argparse
from copy import deepcopy
from html import escape
import json
from pathlib import Path

import numpy as np
import plotly.graph_objects as go


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

    figure.update_layout(
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
        height=800,
        legend={"orientation": "h", "y": -0.2, "x": 0},
        margin={"t": 110, "b": 180},
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
    print(f"Spectra displayed: {len(figure.data)}")


if __name__ == "__main__":
    main()

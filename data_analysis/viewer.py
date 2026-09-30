"""Interactive raw-waveform comparison with recorded time references."""

import argparse
from pathlib import Path

import plotly.graph_objects as go

from data_analysis.waveforms import (
    TimeReference, load_waveform, select_time_window,
)


def build_figure(paths, reference_sample=801250):
    figure = go.Figure()
    records = []

    for path in paths:
        waveform = load_waveform(
            path, TimeReference(reference_sample)
        )
        time, voltage = select_time_window(
            waveform, 0.0, 100e-6
        )
        figure.add_trace(go.Scatter(
            x=(time * 1e6).tolist(),
            y=voltage.tolist(),
            mode="lines",
            name=Path(path).stem,
            hovertemplate=(
                "%{x:.1f} microseconds<br>"
                "%{y:.6f} V<extra>%{fullData.name}</extra>"
            ),
        ))
        records.append({
            "filename": waveform.summary.filename,
            "sha256": waveform.summary.sha256,
            "recorded_date": waveform.summary.recorded_date,
            "reference_sample_one_based": reference_sample,
            "correction_seconds": 0.0,
            "reference_provisional": True,
            "processing": "raw; no smoothing or baseline subtraction",
        })

    figure.update_layout(
        title=(
            "Reference-shot comparison"
            "<br><sup>Raw data; provisional time alignment</sup>"
        ),
        xaxis_title="Time relative to initial plasmoid generation (us)",
        yaxis_title="Detector signal (V)",
        template="plotly_white",
        hovermode="closest",
        meta={"shots": records},
    )
    figure.update_xaxes(range=[0, 100])
    return figure


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--reference-sample", type=int, default=801250)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    output = Path(args.output)
    if output.exists():
        raise SystemExit("Output already exists; choose another filename.")
    output.parent.mkdir(parents=True, exist_ok=True)

    figure = build_figure(args.paths, args.reference_sample)
    figure.write_html(
        output,
        include_plotlyjs=True,
        config={"scrollZoom": True, "displaylogo": False},
    )
    print("Saved:", output.resolve())


if __name__ == "__main__":
    main()

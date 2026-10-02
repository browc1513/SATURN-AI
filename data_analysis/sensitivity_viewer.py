"""Display saved window sensitivity spectra and measurements offline."""

import argparse
from copy import deepcopy
from html import escape
import json
import math
from pathlib import Path

import plotly.graph_objects as go

from data_analysis.spectrum_viewer import build_figure as spectrum_figure

VARIANTS = ("Original", "Earlier", "Later", "Wider")
COLORS = ("#2563eb", "#dc2626", "#059669", "#9333ea")


def finite_number(value):
    return type(value) in (int, float) and math.isfinite(value)


def build_figure(report):
    if (
        not isinstance(report, dict)
        or report.get("schema_version") != 1
        or report.get("report_type") != "window_sensitivity"
        or not isinstance(report.get("shots"), list)
        or not report["shots"]
    ):
        raise ValueError("Invalid sensitivity report.")

    figure = go.Figure()
    groups = []
    for shot in report["shots"]:
        if (
            not isinstance(shot, dict)
            or not isinstance(shot.get("filename"), str)
            or not shot["filename"].strip()
            or not isinstance(shot.get("windows"), dict)
            or not shot["windows"]
        ):
            raise ValueError("Invalid sensitivity shot.")
        for name, cases in shot["windows"].items():
            if (
                not isinstance(name, str) or not name.strip()
                or not isinstance(cases, dict)
                or set(cases) != set(VARIANTS)
            ):
                raise ValueError("Sensitivity windows require four named variants.")
            rows = []
            spectra = {}
            for label in VARIANTS:
                result = cases[label]
                if not isinstance(result, dict):
                    raise ValueError("Invalid sensitivity result.")
                bounds = result.get("requested_window_us")
                measurement = result.get("measurement")
                ratio = result.get("variance_ratio_to_original")
                if (
                    not isinstance(bounds, list) or len(bounds) != 2
                    or not all(finite_number(value) for value in bounds)
                    or bounds[0] >= bounds[1]
                    or not isinstance(measurement, dict)
                    or type(measurement.get("sample_count")) is not int
                    or measurement["sample_count"] < 2
                    or (
                        ratio is not None
                        and (not finite_number(ratio) or ratio < 0)
                    )
                ):
                    raise ValueError("Invalid sensitivity measurements.")
                spectra[label] = result.get("spectrum")
                rows.append([
                    label, f"{bounds[0]:g}", f"{bounds[1]:g}",
                    measurement["sample_count"],
                    None,
                    "Undefined" if ratio is None else f"{ratio:.6g}",
                ])

            # Reuse saved-array validation and DC/zero-bin display handling.
            validated = spectrum_figure({
                "schema_version": 1,
                "shots": [{"filename": shot["filename"], "spectra": spectra}],
            })
            group_index = len(groups)
            trace_indices = []
            maximum = 0.0
            for index, trace in enumerate(
                trace for trace in validated.data if trace.type == "scatter"
            ):
                label = VARIANTS[index]
                trace.name = label
                trace.line.color = COLORS[index]
                trace.line.dash = ("solid", "dash", "dot", "dashdot")[index]
                trace.visible = group_index == 0
                trace.meta = {
                    "group_index": group_index, "variant": label,
                    "processing": deepcopy(spectra[label]["metadata"]),
                }
                trace_indices.append(len(figure.data))
                figure.add_trace(trace)
                maximum = max(maximum, max(trace.x))
                rows[index][4] = f'{spectra[label]["integrated_power_v2"]:.6g}'

            trace_indices.append(len(figure.data))
            figure.add_trace(go.Table(
                visible=group_index == 0,
                domain={"x": [0, 1], "y": [0, 0.25]},
                header={"values": [
                    "Variant", "Start (us)", "Stop (us)", "Samples",
                    "Variance (V^2)", "Relative to original",
                ]},
                cells={"values": list(map(list, zip(*rows)))},
            ))
            groups.append({
                "label": f'{escape(shot["filename"])} / {escape(name)}',
                "indices": trace_indices, "maximum_mhz": maximum,
            })

    def title(group):
        return (
            "Window sensitivity: " + group["label"]
            + "<br><sup>Saved voltage spectra; neutron origin unconfirmed</sup>"
        )

    buttons = []
    for group in groups:
        buttons.append({
            "label": group["label"], "method": "update",
            "args": [
                {"visible": [
                    index in group["indices"] for index in range(len(figure.data))
                ]},
                {
                    "title.text": title(group),
                    "xaxis.range": [0, group["maximum_mhz"]],
                },
            ],
        })
    figure.update_layout(
        title={"text": title(groups[0])},
        template="plotly_white", height=950,
        xaxis={"title": "Frequency (MHz)", "range": [0, groups[0]["maximum_mhz"]]},
        yaxis={
            "title": "Power spectral density (V^2/Hz)",
            "type": "log", "domain": [0.45, 1],
        },
        legend={"orientation": "h", "x": 0, "y": 0.37},
        margin={"t": 120, "b": 60, "r": 350},
        updatemenus=[{
            "buttons": buttons, "active": 0, "x": 1.03, "y": 1,
            "xanchor": "left", "yanchor": "top", "direction": "down",
        }],
        annotations=[{
            "text": (
                "DC omitted; zero PSD shown as gaps. Wider windows change bin spacing."
                "<br>Variance ratios are not neutron yield or SNR; windows overlap."
            ),
            "xref": "paper", "yref": "paper", "x": 0, "y": 0.30,
            "xanchor": "left", "showarrow": False, "font": {"size": 11},
        }],
        meta={
            "report": deepcopy(report),
            "display": {"recalculated": False, "dc_omitted": True},
        },
    )
    return figure


def save_viewer(report_path, output_path):
    source, output = Path(report_path), Path(output_path)
    if output.exists():
        raise FileExistsError("Output already exists; choose another filename.")
    report = json.loads(source.read_text(encoding="utf-8-sig"))
    figure = build_figure(report)
    figure.layout.meta["report_path"] = str(source.resolve())
    html = figure.to_html(
        full_html=True, include_plotlyjs=True,
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
    print("Saved:", Path(args.output).resolve())
    print("Shot/window comparisons:", len(figure.layout.updatemenus[0].buttons))
    print("Visible spectra: 4")


if __name__ == "__main__":
    main()

"""Save local project references and verify source files when reopening."""

import argparse
import json
import math
from pathlib import Path

from data_analysis.sl1000 import inspect_sl1000



def _validate_measurement_windows(windows, start_us, stop_us):
    if not isinstance(windows, dict):
        raise ValueError("Measurement windows must be a dictionary.")
    validated = {}
    for name, bounds in windows.items():
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Measurement window names must be nonempty.")
        if not isinstance(bounds, (list, tuple)) or len(bounds) != 2:
            raise ValueError("Measurement windows require two boundaries.")
        if not all(
            type(value) in (int, float) and math.isfinite(value)
            for value in bounds
        ):
            raise ValueError("Measurement boundaries must be finite numbers.")
        if not start_us <= bounds[0] < bounds[1] <= stop_us:
            raise ValueError("Measurement windows must lie within the display.")
        validated[name] = list(bounds)
    return validated


def save_project(destination, name, paths, reference_sample=801250,
                 start_us=0.0, stop_us=100.0,
                 measurement_windows=None):
    from data_analysis.waveforms import TimeReference

    if not isinstance(name, str) or not name.strip():
        raise ValueError("A project name is required.")

    if not (
        math.isfinite(start_us) and math.isfinite(stop_us)
        and start_us < stop_us
    ):
        raise ValueError("Window must be finite and increasing.")

    windows = _validate_measurement_windows(
        {} if measurement_windows is None else measurement_windows,
        start_us, stop_us,
    )

    shots = []
    seen = set()
    for path in paths:
        source = Path(path).resolve(strict=True)
        summary = inspect_sl1000(source)
        TimeReference(reference_sample).zero_index(summary.actual_samples)
        if summary.sha256 in seen:
            raise ValueError("Duplicate source data selected.")
        seen.add(summary.sha256)
        shots.append({
            "path": str(source),
            "sha256": summary.sha256,
            "filename": summary.filename,
            "recorded_date": summary.recorded_date,
        })

    if not shots:
        raise ValueError("Select at least one source file.")

    record = {
        "schema_version": 1,
        "name": name.strip(),
        "reference_sample_one_based": reference_sample,
        "reference_provisional": True,
        "correction_seconds": 0.0,
        "window_seconds": [start_us * 1e-6, stop_us * 1e-6],
        "processing": "raw",
        "shots": shots,
    }

    if windows:
        record["measurement_windows_us"] = windows

    text = json.dumps(record, indent=2, allow_nan=False)
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("x", encoding="utf-8") as stream:
        stream.write(text + "\n")
    return record


def load_project(source):
    from data_analysis.waveforms import TimeReference

    with Path(source).open(encoding="utf-8-sig") as stream:
        record = json.load(stream)

    if not isinstance(record, dict) or record.get("schema_version") != 1:
        raise ValueError("Unsupported project format.")
    if (
        record.get("reference_provisional") is not True
        or record.get("correction_seconds") != 0.0
        or record.get("processing") != "raw"
    ):
        raise ValueError("Unsupported analysis settings.")
    if not isinstance(record.get("name"), str) or not record["name"].strip():
        raise ValueError("Invalid project name.")

    window = record.get("window_seconds")
    if not isinstance(window, list) or len(window) != 2:
        raise ValueError("Invalid project window.")
    if not all(
        type(value) in (int, float) and math.isfinite(value)
        for value in window
    ) or window[0] >= window[1]:
        raise ValueError("Window must be finite and increasing.")

    _validate_measurement_windows(
        record.get("measurement_windows_us", {}),
        window[0] * 1e6, window[1] * 1e6,
    )

    shots = record.get("shots")
    if not isinstance(shots, list) or not shots:
        raise ValueError("Project has no source files.")

    seen = set()
    for shot in shots:
        if not isinstance(shot, dict) or not isinstance(shot.get("path"), str):
            raise ValueError("Invalid source record.")
        path = Path(shot["path"])
        if not path.is_absolute():
            raise ValueError("Source paths must be absolute.")
        summary = inspect_sl1000(path)
        if summary.sha256 != shot.get("sha256"):
            raise ValueError(f"Source file changed: {path.name}")
        if summary.sha256 in seen:
            raise ValueError("Duplicate source data in project.")
        seen.add(summary.sha256)
        TimeReference(
            record.get("reference_sample_one_based")
        ).zero_index(summary.actual_samples)

    return record


def main():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)

    create = commands.add_parser("create")
    create.add_argument("--name", required=True)
    create.add_argument("--project", required=True)
    create.add_argument("--start-us", type=float, default=0.0)
    create.add_argument("--stop-us", type=float, default=100.0)
    create.add_argument("paths", nargs="+")

    reopen = commands.add_parser("open")
    reopen.add_argument("--project", required=True)
    reopen.add_argument("--output", required=True)

    args = parser.parse_args()
    if args.command == "create":
        save_project(
            args.project, args.name, args.paths,
            start_us=args.start_us, stop_us=args.stop_us,
        )
        print("Project saved:", Path(args.project).resolve())
        return

    from data_analysis.viewer import build_figure

    record = load_project(args.project)
    output = Path(args.output)
    if output.exists():
        raise ValueError("Output already exists; choose another filename.")
    figure = build_figure(
        [shot["path"] for shot in record["shots"]],
        reference_sample=record["reference_sample_one_based"],
        start_us=record["window_seconds"][0] * 1e6,
        stop_us=record["window_seconds"][1] * 1e6,
        measurement_windows=record.get("measurement_windows_us", {}),
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.write_html(
        output,
        include_plotlyjs=True,
        config={"scrollZoom": True, "displaylogo": False},
    )
    print("Viewer saved:", output.resolve())


if __name__ == "__main__":
    main()

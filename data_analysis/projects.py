"""Save local project references and verify source files when reopening."""

import argparse
import json
from pathlib import Path

from data_analysis.sl1000 import inspect_sl1000


def save_project(destination, name, paths, reference_sample=801250):
    from data_analysis.waveforms import TimeReference

    if not isinstance(name, str) or not name.strip():
        raise ValueError("A project name is required.")

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
        "window_seconds": [0.0, 100e-6],
        "processing": "raw",
        "shots": shots,
    }

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
        or record.get("window_seconds") != [0.0, 100e-6]
        or record.get("processing") != "raw"
    ):
        raise ValueError("Unsupported analysis settings.")
    if not isinstance(record.get("name"), str) or not record["name"].strip():
        raise ValueError("Invalid project name.")

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
    create.add_argument("paths", nargs="+")

    reopen = commands.add_parser("open")
    reopen.add_argument("--project", required=True)
    reopen.add_argument("--output", required=True)

    args = parser.parse_args()
    if args.command == "create":
        save_project(args.project, args.name, args.paths)
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

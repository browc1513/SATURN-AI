"""Generate voltage spectra from verified saved analysis projects."""

import argparse
import json
import math
from pathlib import Path

import numpy as np

from data_analysis.measurements import measure_window
from data_analysis.projects import load_project
from data_analysis.spectra import calculate_spectrum
from data_analysis.waveforms import TimeReference, load_waveform


def build_report(project_path):
    project = load_project(project_path)
    windows = project.get("measurement_windows_us", {})
    if not windows:
        raise ValueError("Project requires measurement windows for spectra.")

    reference = TimeReference(
        project["reference_sample_one_based"],
        correction_seconds=project["correction_seconds"],
        provisional=project["reference_provisional"],
    )
    records = []
    for shot in project["shots"]:
        waveform = load_waveform(shot["path"], reference)
        if waveform.summary.sha256 != shot["sha256"]:
            raise ValueError("Source file changed after project verification.")

        spectra = {}
        for name, bounds in windows.items():
            start, stop = [value * 1e-6 for value in bounds]
            result = calculate_spectrum(waveform, start, stop)
            measured = measure_window(waveform, start, stop)
            metadata = result["metadata"]
            density = result["power_spectral_density_v2_per_hz"]
            power = float(
                np.sum(density) * metadata["frequency_bin_spacing_hz"]
            )
            if not math.isfinite(power) or not math.isclose(
                power, measured["ac_rms_voltage"] ** 2,
                rel_tol=1e-12, abs_tol=1e-15,
            ):
                raise ValueError("Spectral power does not match measured AC RMS.")

            spectra[name] = {
                "metadata": metadata,
                "frequency_hz": result["frequency_hz"].tolist(),
                "power_spectral_density_v2_per_hz": density.tolist(),
                "integrated_power_v2": power,
            }

        records.append({
            "filename": waveform.summary.filename,
            "sha256": waveform.summary.sha256,
            "source_path": shot["path"],
            "reference_sample_one_based": reference.sample_number,
            "correction_seconds": reference.correction_seconds,
            "reference_provisional": reference.provisional,
            "spectra": spectra,
        })

    return {
        "schema_version": 1,
        "project": str(Path(project_path).resolve()),
        "project_name": project["name"],
        "interpretation": (
            "Exploratory recorded-voltage spectra. Largest bins do not "
            "identify neutron origin. Instrument response is not corrected."
        ),
        "shots": records,
    }


def save_report(project_path, output_path):
    output = Path(output_path)
    if output.exists():
        raise FileExistsError("Output already exists; choose another filename.")
    report = build_report(project_path)
    text = json.dumps(report, indent=2, allow_nan=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as stream:
        stream.write(text + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    report = save_report(args.project, args.output)
    count = sum(len(shot["spectra"]) for shot in report["shots"])
    print("Report saved:", Path(args.output).resolve())
    print(f'Shots: {len(report["shots"])}; spectra: {count}')


if __name__ == "__main__":
    main()

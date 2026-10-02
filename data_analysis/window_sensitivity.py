"""Compare saved voltage windows with explicit timing and width variations."""

import argparse
from copy import deepcopy
import json
import math
from pathlib import Path

import numpy as np

from data_analysis.measurements import measure_window
from data_analysis.projects import load_project
from data_analysis.spectra import calculate_spectrum
from data_analysis.waveforms import TimeReference, load_waveform


def window_variants(bounds):
    start, stop = bounds
    width = stop - start
    shift = width * 0.2
    expansion = width * 0.25
    return {
        "Original": [start, stop],
        "Earlier": [start - shift, stop - shift],
        "Later": [start + shift, stop + shift],
        "Wider": [start - expansion, stop + expansion],
    }


def build_report(project_path):
    project = load_project(project_path)
    windows = project.get("measurement_windows_us", {})
    if not windows:
        raise ValueError("Project requires measurement windows.")

    display_start, display_stop = [
        value * 1e6 for value in project["window_seconds"]
    ]
    variants = {name: window_variants(bounds) for name, bounds in windows.items()}
    for name, cases in variants.items():
        for label, (start, stop) in cases.items():
            if (
                start < display_start
                and not math.isclose(start, display_start, rel_tol=0, abs_tol=1e-9)
            ) or (
                stop > display_stop
                and not math.isclose(stop, display_stop, rel_tol=0, abs_tol=1e-9)
            ):
                raise ValueError(
                    f"{name} / {label} extends outside the saved display."
                )

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

        results = {}
        for name, cases in variants.items():
            results[name] = {}
            for label, bounds in cases.items():
                start, stop = [value * 1e-6 for value in bounds]
                try:
                    measurement = measure_window(waveform, start, stop)
                    spectrum = calculate_spectrum(waveform, start, stop)
                except ValueError as error:
                    raise ValueError(
                        f'{shot["filename"]} / {name} / {label}: {error}'
                    ) from error
                density = spectrum["power_spectral_density_v2_per_hz"]
                power = float(
                    np.sum(density)
                    * spectrum["metadata"]["frequency_bin_spacing_hz"]
                )
                if not math.isfinite(power) or not math.isclose(
                    power, measurement["ac_rms_voltage"] ** 2,
                    rel_tol=1e-12, abs_tol=1e-15,
                ):
                    raise ValueError("Spectral power does not match measured AC RMS.")
                results[name][label] = {
                    "requested_window_us": bounds,
                    "measurement": measurement,
                    "spectrum": {
                        "metadata": spectrum["metadata"],
                        "frequency_hz": spectrum["frequency_hz"].tolist(),
                        "power_spectral_density_v2_per_hz": density.tolist(),
                        "integrated_power_v2": power,
                    },
                }

            original = results[name]["Original"]["spectrum"]["integrated_power_v2"]
            for result in results[name].values():
                power = result["spectrum"]["integrated_power_v2"]
                ratio = power / original if original > 0 else None
                result["variance_ratio_to_original"] = (
                    ratio if ratio is not None and math.isfinite(ratio) else None
                )

        records.append({
            "filename": waveform.summary.filename,
            "sha256": waveform.summary.sha256,
            "source_path": shot["path"],
            "windows": results,
        })

    return {
        "schema_version": 1,
        "report_type": "window_sensitivity",
        "project_path": str(Path(project_path).resolve()),
        "project": deepcopy(project),
        "variation_settings": {
            "shift_fraction_of_original_width": 0.2,
            "wider_width_multiplier": 1.5,
            "boundary_convention": "[start, stop)",
        },
        "interpretation": (
            "Exploratory voltage-window sensitivity. Ratios compare voltage "
            "variance with the original window; they are not neutron yield "
            "or signal-to-noise ratio. Overlapping windows are not independent "
            "measurements. Wider windows have different frequency-bin spacing."
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
    count = 0
    for shot in report["shots"]:
        for name, cases in shot["windows"].items():
            for label, result in cases.items():
                count += 1
                measurement = result["measurement"]
                power = result["spectrum"]["integrated_power_v2"]
                ratio = result["variance_ratio_to_original"]
                ratio_text = "Undefined" if ratio is None else f"{ratio:.6g}"
                bounds = result["requested_window_us"]
                print(
                    f'{shot["filename"]} | {name} | {label} | '
                    f'{bounds[0]:g} to {bounds[1]:g} us | '
                    f'N={measurement["sample_count"]} | '
                    f'variance={power:.6g} V^2 | relative={ratio_text}'
                )
    print("Report saved:", Path(args.output).resolve())
    print(f'Shots: {len(report["shots"])}; window results: {count}')


if __name__ == "__main__":
    main()

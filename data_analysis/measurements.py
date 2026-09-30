"""Descriptive voltage measurements without modifying recorded samples."""

import numpy as np

from data_analysis.waveforms import select_time_window


def measure_window(waveform, start_seconds, stop_seconds):
    """Measure a fully recorded [start, stop) window."""
    interval = waveform.summary.sample_interval_seconds
    recording_start = float(waveform.time_seconds[0])
    recording_stop = float(waveform.time_seconds[-1]) + interval
    tolerance = interval * 1e-8

    if (
        start_seconds < recording_start - tolerance
        or stop_seconds > recording_stop + tolerance
    ):
        raise ValueError("Requested window extends outside the recording.")

    time, voltage = select_time_window(
        waveform, start_seconds, stop_seconds
    )
    if voltage.size < 2:
        raise ValueError("Measurements require at least two samples.")
    if not np.all(np.isfinite(voltage)):
        raise ValueError("Voltage samples must be finite.")

    mean = float(np.mean(voltage))
    return {
        "requested_window_seconds": [start_seconds, stop_seconds],
        "sample_count": int(voltage.size),
        "sample_interval_seconds": float(interval),
        "first_sample_time_seconds": float(time[0]),
        "last_sample_time_seconds": float(time[-1]),
        "mean_voltage": mean,
        "rms_voltage": float(np.sqrt(np.mean(voltage ** 2))),
        "ac_rms_voltage": float(np.sqrt(np.mean((voltage - mean) ** 2))),
        "min_voltage": float(np.min(voltage)),
        "max_voltage": float(np.max(voltage)),
        "peak_to_peak_voltage": float(np.ptp(voltage)),
        "processing": "raw; no smoothing or baseline subtraction",
    }

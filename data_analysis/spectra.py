"""Explicitly normalized spectra of recorded voltage samples."""

import numpy as np

from data_analysis.measurements import measure_window
from data_analysis.waveforms import select_time_window


def calculate_spectrum(waveform, start_seconds, stop_seconds):
    """Return a mean-subtracted, one-sided rectangular-window periodogram."""
    measurement = measure_window(waveform, start_seconds, stop_seconds)
    _, voltage = select_time_window(waveform, start_seconds, stop_seconds)

    count = voltage.size
    interval = float(waveform.summary.sample_interval_seconds)
    if not np.isfinite(interval) or interval <= 0:
        raise ValueError("Sample interval must be finite and positive.")

    centered = voltage - np.mean(voltage)
    transform = np.fft.rfft(centered)
    frequency = np.fft.rfftfreq(count, d=interval)

    # PSD units: V^2/Hz. Double only bins with negative-frequency partners.
    density = (interval / count) * np.abs(transform) ** 2
    if count % 2 == 0:
        density[1:-1] *= 2
    else:
        density[1:] *= 2

    if not np.all(np.isfinite(density)):
        raise ValueError("Spectrum contains nonfinite values.")

    frequency.setflags(write=False)
    density.setflags(write=False)

    return {
        "frequency_hz": frequency,
        "power_spectral_density_v2_per_hz": density,
        "metadata": {
            "requested_window_seconds": [start_seconds, stop_seconds],
            "sample_count": int(count),
            "sample_interval_seconds": interval,
            "sample_rate_hz": 1.0 / interval,
            "nyquist_frequency_hz": 0.5 / interval,
            "frequency_bin_spacing_hz": 1.0 / (count * interval),
            "removed_mean_voltage": measurement["mean_voltage"],
            "window": "rectangular",
            "detrending": "subtract selected-window mean",
            "normalization": "one-sided power spectral density in V^2/Hz",
            "zero_padding": False,
            "interpretation": "Recorded-voltage spectrum; neutron origin unconfirmed.",
        },
    }

"""Load validated waveforms with an explicit event-time reference."""

from dataclasses import dataclass

import numpy as np

from data_analysis.sl1000 import inspect_sl1000


@dataclass(frozen=True)
class TimeReference:
    sample_number: int
    correction_seconds: float = 0.0
    provisional: bool = True

    def zero_index(self, sample_count):
        if isinstance(self.sample_number, bool) or not isinstance(
            self.sample_number, int
        ):
            raise ValueError("Sample number must be an integer.")
        if not 1 <= self.sample_number <= sample_count:
            raise ValueError("Reference sample lies outside the recording.")
        if not np.isfinite(self.correction_seconds):
            raise ValueError("Timing correction must be finite.")
        return self.sample_number - 1


@dataclass(frozen=True)
class Waveform:
    summary: object
    voltage: np.ndarray
    time_seconds: np.ndarray
    reference: TimeReference


def load_waveform(path, reference):
    summary = inspect_sl1000(path)
    zero = reference.zero_index(summary.actual_samples)

    voltage = np.loadtxt(
        path, delimiter=",", skiprows=9, usecols=1, encoding="utf-8-sig"
    )
    if voltage.size != summary.actual_samples:
        raise ValueError("File sample count changed during loading.")

    time = (
        (np.arange(voltage.size, dtype=np.float64) - zero)
        * summary.sample_interval_seconds
        + reference.correction_seconds
    )
    voltage.setflags(write=False)
    time.setflags(write=False)
    return Waveform(summary, voltage, time, reference)

def select_time_window(waveform, start_seconds, stop_seconds):
    """Return samples in [start, stop), using sample-based boundaries."""
    if not (
        np.isfinite(start_seconds)
        and np.isfinite(stop_seconds)
        and start_seconds < stop_seconds
    ):
        raise ValueError("Window boundaries must be finite and increasing.")

    interval = waveform.summary.sample_interval_seconds
    zero = waveform.reference.zero_index(waveform.voltage.size)
    correction = waveform.reference.correction_seconds

    def boundary(value):
        position = (value - correction) / interval
        nearest = round(position)
        if abs(position - nearest) <= 1e-8:
            position = nearest
        return zero + int(np.ceil(position))

    first = max(0, boundary(start_seconds))
    last = min(waveform.voltage.size, boundary(stop_seconds))
    if first >= last:
        raise ValueError("Window contains no recorded samples.")

    return (
        waveform.time_seconds[first:last],
        waveform.voltage[first:last],
    )

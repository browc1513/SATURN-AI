from types import SimpleNamespace

import numpy as np
import pytest

from data_analysis.measurements import measure_window
from data_analysis.waveforms import TimeReference, Waveform


def waveform(values):
    voltage = np.array(values, dtype=float)
    voltage.setflags(write=False)
    return Waveform(
        SimpleNamespace(sample_interval_seconds=1.0),
        voltage,
        np.arange(voltage.size, dtype=float),
        TimeReference(1),
    )


def test_measurements_match_known_values_and_preserve_samples():
    data = waveform([1, 2, 3, 4])
    original = data.voltage.copy()
    result = measure_window(data, 0.0, 4.0)

    assert result["sample_count"] == 4
    assert result["mean_voltage"] == pytest.approx(2.5)
    assert result["rms_voltage"] == pytest.approx(np.sqrt(7.5))
    assert result["ac_rms_voltage"] == pytest.approx(np.sqrt(1.25))
    assert result["peak_to_peak_voltage"] == pytest.approx(3.0)
    np.testing.assert_array_equal(data.voltage, original)


def test_constant_offset_has_zero_ac_rms():
    result = measure_window(waveform([5, 5, 5]), 0.0, 3.0)
    assert result["rms_voltage"] == 5.0
    assert result["ac_rms_voltage"] == 0.0


@pytest.mark.parametrize("start,stop", [(-1, 3), (0, 5)])
def test_partial_recording_window_is_rejected(start, stop):
    with pytest.raises(ValueError, match="outside"):
        measure_window(waveform([1, 2, 3, 4]), start, stop)


def test_stop_boundary_is_excluded():
    result = measure_window(waveform([1, 2, 100]), 0.0, 2.0)
    assert result["sample_count"] == 2
    assert result["max_voltage"] == 2.0


def test_single_sample_window_is_rejected():
    with pytest.raises(ValueError, match="two samples"):
        measure_window(waveform([1, 2, 3]), 0.0, 1.0)


def test_nonfinite_voltage_is_rejected():
    with pytest.raises(ValueError, match="finite"):
        measure_window(waveform([1, float("nan"), 3]), 0.0, 3.0)

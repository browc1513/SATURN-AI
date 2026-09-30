from types import SimpleNamespace

import numpy as np
import pytest

from data_analysis.spectra import calculate_spectrum
from data_analysis.waveforms import TimeReference, Waveform


def make_waveform(values, interval=1e-7):
    voltage = np.asarray(values, dtype=float)
    voltage.setflags(write=False)
    return Waveform(
        SimpleNamespace(sample_interval_seconds=interval),
        voltage,
        np.arange(voltage.size, dtype=float) * interval,
        TimeReference(1),
    )


def test_known_sine_frequency_and_integrated_power():
    count = 100
    interval = 1e-7
    amplitude = 2.0
    values = 3.0 + amplitude * np.sin(
        2 * np.pi * 1e6 * np.arange(count) * interval
    )
    waveform = make_waveform(values, interval)
    original = waveform.voltage.copy()
    result = calculate_spectrum(waveform, 0, count * interval)
    frequency = result["frequency_hz"]
    density = result["power_spectral_density_v2_per_hz"]
    spacing = result["metadata"]["frequency_bin_spacing_hz"]

    assert frequency[np.argmax(density)] == pytest.approx(1e6)
    assert np.sum(density) * spacing == pytest.approx(amplitude ** 2 / 2)
    assert result["metadata"]["removed_mean_voltage"] == pytest.approx(3.0)
    np.testing.assert_array_equal(waveform.voltage, original)
    assert not frequency.flags.writeable
    assert not density.flags.writeable


@pytest.mark.parametrize("count", [99, 100])
def test_integrated_spectrum_matches_mean_square_variation(count):
    values = np.random.default_rng(42).normal(size=count)
    result = calculate_spectrum(make_waveform(values), 0, count * 1e-7)
    power = (
        np.sum(result["power_spectral_density_v2_per_hz"])
        * result["metadata"]["frequency_bin_spacing_hz"]
    )
    assert power == pytest.approx(np.mean((values - values.mean()) ** 2))


def test_nyquist_bin_is_not_doubled():
    values = np.array([1.0, -1.0] * 50)
    result = calculate_spectrum(make_waveform(values), 0, 100 * 1e-7)
    density = result["power_spectral_density_v2_per_hz"]
    spacing = result["metadata"]["frequency_bin_spacing_hz"]
    assert result["frequency_hz"][-1] == pytest.approx(5e6)
    assert density[-1] * spacing == pytest.approx(1.0)


def test_constant_signal_has_zero_spectrum_after_mean_removal():
    result = calculate_spectrum(make_waveform(np.full(100, 5.0)), 0, 1e-5)
    np.testing.assert_array_equal(
        result["power_spectral_density_v2_per_hz"], np.zeros(51)
    )


def test_partial_window_is_rejected():
    with pytest.raises(ValueError, match="outside"):
        calculate_spectrum(make_waveform(np.ones(100)), -1e-6, 1e-5)

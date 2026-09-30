import numpy as np
import pytest

from data_analysis.waveforms import TimeReference, load_waveform


def test_one_based_reference_and_correction(tmp_path):
    path = tmp_path / "shot.CSV"
    path.write_text(
        '"Model","SL1000"\n'
        '"BlockNumber","1"\n'
        '"TraceName","ND",\n'
        'BlockSize,3,\n'
        'Date,2025/10/23,\n'
        'Time,16:34:38,\n'
        'VUnit,V,\n'
        'HResolution,1e-7,\n'
        'HUnit,s,\n'
        ',-1\n,0\n,2\n',
        encoding="utf-8",
    )
    waveform = load_waveform(
        path, TimeReference(2, correction_seconds=2e-7)
    )
    np.testing.assert_allclose(
        waveform.time_seconds, [1e-7, 2e-7, 3e-7],
        rtol=0, atol=1e-15,
    )
    np.testing.assert_array_equal(waveform.voltage, [-1, 0, 2])
    assert not waveform.voltage.flags.writeable
    assert not waveform.time_seconds.flags.writeable


@pytest.mark.parametrize("sample", [0, 4, 1.5, True])
def test_invalid_reference_is_rejected(sample):
    with pytest.raises(ValueError):
        TimeReference(sample).zero_index(3)


def test_nonfinite_correction_is_rejected():
    with pytest.raises(ValueError):
        TimeReference(1, correction_seconds=float("nan")).zero_index(3)


def test_window_includes_exact_start_and_excludes_stop():
    from types import SimpleNamespace
    from data_analysis.waveforms import Waveform, select_time_window

    interval = 1e-7
    values = np.arange(1000, dtype=float)
    waveform = Waveform(
        SimpleNamespace(sample_interval_seconds=interval),
        values,
        np.arange(1000) * interval,
        TimeReference(1),
    )
    time, voltage = select_time_window(waveform, 20e-6, 30e-6)
    assert voltage.size == 100
    assert voltage[0] == 200
    assert voltage[-1] == 299

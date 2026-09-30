import hashlib

import pytest

from data_analysis.sl1000 import SL1000FormatError, inspect_sl1000


HEADER = (
    '"Model","SL1000"\n"BlockNumber","1"\n"TraceName","ND",\n'
    'BlockSize,3,\nDate,2025/10/09,\nTime,11:15:29.423007,\n'
    'VUnit,V,\nHResolution,1.000000e-007,\nHUnit,s,\n'
)


def test_inspection_preserves_original_and_counts_samples(tmp_path):
    content = (HEADER + ',-1.0\n,0.0\n,2.0\n').encode()
    path = tmp_path / "R24886.CSV"
    path.write_bytes(content)
    result = inspect_sl1000(path)
    assert path.read_bytes() == content
    assert result.sha256 == hashlib.sha256(content).hexdigest()
    assert result.actual_samples == 3
    assert result.duration_seconds == pytest.approx(2e-7)
    assert (result.min_voltage, result.max_voltage) == (-1.0, 2.0)


@pytest.mark.parametrize("body", [",nan\n,0\n,1\n", ",0\n,1\n", ",0\n,1\n,2\n,3\n"])
def test_rejects_invalid_samples_and_counts(tmp_path, body):
    path = tmp_path / "bad.CSV"
    path.write_text(HEADER + body)
    with pytest.raises(SL1000FormatError):
        inspect_sl1000(path)

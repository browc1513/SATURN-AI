import numpy as np

from data_analysis.viewer import build_figure


def test_viewer_preserves_raw_samples_and_records_provenance(tmp_path):
    path = tmp_path / "R24913.CSV"
    path.write_text(
        '"Model","SL1000"\n'
        '"BlockNumber","1"\n'
        '"TraceName","ND",\n'
        'BlockSize,4,\n'
        'Date,2025/10/23,\n'
        'Time,16:34:38,\n'
        'VUnit,V,\n'
        'HResolution,1e-7,\n'
        'HUnit,s,\n'
        ',-1\n,0\n,2\n,3\n',
        encoding="utf-8",
    )
    original = path.read_bytes()
    figure = build_figure([path], reference_sample=2)

    assert len(figure.data) == 1
    np.testing.assert_allclose(
        figure.data[0].x, [0.0, 0.1, 0.2],
        rtol=0, atol=1e-12,
    )
    np.testing.assert_array_equal(figure.data[0].y, [0, 2, 3])

    record = figure.layout.meta["shots"][0]
    assert record["filename"] == "R24913.CSV"
    assert record["reference_sample_one_based"] == 2
    assert record["reference_provisional"] is True
    assert record["processing"] == "raw; no smoothing or baseline subtraction"
    assert len(record["sha256"]) == 64
    assert path.read_bytes() == original


def test_viewer_uses_requested_sample_window(tmp_path):
    path = tmp_path / "shot.CSV"
    path.write_text(
        '"Model","SL1000"\n'
        '"BlockNumber","1"\n'
        '"TraceName","ND",\n'
        'BlockSize,4,\n'
        'Date,2025/10/23,\n'
        'Time,16:34:38,\n'
        'VUnit,V,\n'
        'HResolution,1e-7,\n'
        'HUnit,s,\n'
        ',-1\n,0\n,2\n,3\n',
        encoding="utf-8",
    )
    figure = build_figure(
        [path], reference_sample=2, start_us=0.1, stop_us=0.3
    )
    np.testing.assert_array_equal(figure.data[0].y, [2, 3])
    record = figure.layout.meta["shots"][0]
    assert record["requested_window_us"] == [0.1, 0.3]
    assert record["displayed_samples"] == 2

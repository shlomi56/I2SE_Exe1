"""Generalized regression tests for Ex0.py.

Run the complete battery from the repository root with::

    pytest -q test_ex0_generalized.py

The parameterized tests below collect as 124 independent pytest cases.  They
exercise public behaviour rather than implementation details, so the file can
also be kept as a regression suite when the projection implementation changes.
"""

import numpy as np
import pytest

import Ex0
from Ex0 import (
    normalize_volume_to_uint8,
    parse_csv_planes,
    project_plane_kernel,
    run_pipeline,
)


@pytest.mark.parametrize(
    "volume, expected",
    [
        (np.array([[[0, 1, 2]]], dtype=np.uint8), np.array([[[0, 1, 2]]], dtype=np.uint8)),
        (np.array([[[0, 255]]], dtype=np.uint8), np.array([[[0, 255]]], dtype=np.uint8)),
        (np.array([[[0, 1]]], dtype=np.uint16), np.array([[[0, 255]]], dtype=np.uint8)),
        (np.array([[[100, 200]]], dtype=np.uint16), np.array([[[0, 255]]], dtype=np.uint8)),
        (np.array([[[-5, 5]]], dtype=np.int16), np.array([[[0, 255]]], dtype=np.uint8)),
        (np.array([[[2.0, 4.0]]], dtype=np.float32), np.array([[[0, 255]]], dtype=np.uint8)),
        (np.array([[[-1.5, 1.5]]], dtype=np.float64), np.array([[[0, 255]]], dtype=np.uint8)),
        (np.full((2, 3, 4), 7, dtype=np.int16), np.zeros((2, 3, 4), dtype=np.uint8)),
        (np.full((1, 1, 1), 0.0, dtype=np.float32), np.zeros((1, 1, 1), dtype=np.uint8)),
        (np.array([[[0, 127, 255]]], dtype=np.uint8), np.array([[[0, 127, 255]]], dtype=np.uint8)),
        (np.array([[[0, 32768, 65535]]], dtype=np.uint16), np.array([[[0, 127, 255]]], dtype=np.uint8)),
        (np.array([[[10, 20, 30]]], dtype=np.int32), np.array([[[0, 127, 255]]], dtype=np.uint8)),
        (np.array([[[-10.0, 0.0, 10.0]]], dtype=np.float32), np.array([[[0, 127, 255]]], dtype=np.uint8)),
        (np.array([[[1, 2, 3, 4]]], dtype=np.uint8), np.array([[[1, 2, 3, 4]]], dtype=np.uint8)),
        (np.array([[[0, 10]]], dtype=np.int8), np.array([[[0, 255]]], dtype=np.uint8)),
    ],
)
def test_normalize_volume_general_cases(volume, expected):
    result = normalize_volume_to_uint8(volume)
    assert result.dtype == np.uint8
    assert result.flags.c_contiguous
    np.testing.assert_array_equal(result, expected)


CSV_CASES = [
    ("", 0),
    ("\n\n", 0),
    ("1,2,3,4,5,6,7,8,9\n", 1),
    ("1,2,3,4,5,6,7,8,9,10,11,12\n", 1),
    (" 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 \n", 1),
    ("1,2,3\n", 0),
    ("a,b,c\n", 0),
    ("1,2,3,4,5,6,7,8,not-a-number\n", 0),
    ("1,2,3,4,5,6,7,8,9\n1,2,3,4,5,6,7,8,9\n", 2),
    ("1,2,3,4,5,6,7,8,9\n\n1,2,3,4\n", 1),
    ("1,2,3,4,5,6,7,8,9,,,,\n", 1),
    ("\ufeff1,2,3,4,5,6,7,8,9\n", 1),
    ("1.5,-2,3e1,4,5,6,7,8,9\n", 1),
    ("1,2,3,4,5,6,7,8,9,10,11,12\n1,2\n", 1),
    (" , , \n1,2,3,4,5,6,7,8,9\n", 1),
]


@pytest.mark.parametrize("contents, expected_count", CSV_CASES)
def test_parse_csv_accepts_only_supported_rows(tmp_path, contents, expected_count):
    path = tmp_path / "planes.csv"
    path.write_text(contents, encoding="utf-8")
    planes = parse_csv_planes(path)
    assert len(planes) == expected_count
    for a1, a2, b, c in planes:
        assert all(point.dtype == np.float64 and point.shape == (3,) for point in (a1, a2, b, c))


def test_parse_csv_maps_triangle_first_point_to_both_a_points(tmp_path):
    path = tmp_path / "triangle.csv"
    path.write_text("1,2,3,4,5,6,7,8,9\n", encoding="utf-8")
    a1, a2, b, c = parse_csv_planes(path)[0]
    np.testing.assert_array_equal(a1, [1.0, 2.0, 3.0])
    np.testing.assert_array_equal(a2, a1)
    assert a1 is not a2
    np.testing.assert_array_equal(b, [4.0, 5.0, 6.0])
    np.testing.assert_array_equal(c, [7.0, 8.0, 9.0])


PROJECTION_CASES = [
    (height_axis, width_axis, height, width)
    for height_axis in range(3)
    for width_axis in range(3)
    if width_axis != height_axis
    for height in (1, 2, 3)
    for width in (1, 2, 3, 4)
]


@pytest.mark.parametrize("height_axis, width_axis, height, width", PROJECTION_CASES)
def test_projection_shape_type_and_values_for_many_orientations(
    height_axis, width_axis, height, width
):
    volume = np.full((32, 32, 32), 73, dtype=np.uint8)
    a = np.array([10.0, 10.0, 10.0])
    b = a.copy()
    b[height_axis] += height
    c = b.copy()
    c[width_axis] += width

    projection = project_plane_kernel(volume, a, a.copy(), b, c)

    assert projection.shape == (height, width)
    assert projection.dtype == np.float32
    assert np.isfinite(projection).all()
    assert set(np.unique(projection)).issubset({0.0, 73.0})
    assert projection.max() == 73.0


@pytest.mark.parametrize("axis", range(3))
@pytest.mark.parametrize("distance", (1, 2, 5, 9))
def test_projection_returns_black_for_completely_out_of_bounds_planes(axis, distance):
    volume = np.full((8, 8, 8), 255, dtype=np.uint8)
    a = np.array([100.0, 100.0, 100.0])
    b = a.copy()
    b[axis] += distance
    c = b.copy()
    c[(axis + 1) % 3] += distance
    projection = project_plane_kernel(volume, a, a.copy(), b, c)
    assert projection.shape == (distance, distance)
    assert np.all(projection == 0.0)


@pytest.mark.parametrize(
    "a, b, c",
    [
        ([1, 1, 1], [1, 1, 1], [2, 2, 2]),
        ([1, 1, 1], [2, 1, 1], [2, 1, 1]),
        ([1, 1, 1], [1, 2, 1], [1, 2, 1]),
        ([1, 1, 1], [1, 1, 2], [1, 1, 2]),
        ([1, 1, 1], [1.1, 1, 1], [1.1, 1, 1]),
        ([1, 1, 1], [1, 1.1, 1], [1, 1.1, 1]),
    ],
)
def test_projection_returns_fallback_for_zero_output_dimension(a, b, c):
    volume = np.ones((8, 8, 8), dtype=np.uint8)
    projection = project_plane_kernel(
        volume, np.asarray(a, dtype=float), np.asarray(a, dtype=float),
        np.asarray(b, dtype=float), np.asarray(c, dtype=float),
    )
    assert projection.shape == (10, 10)
    assert projection.dtype == np.float32
    assert np.all(projection == 0.0)


@pytest.mark.parametrize("missing_name", ("missing.nrrd", "missing.csv"))
def test_pipeline_rejects_missing_inputs(tmp_path, missing_name, capsys):
    existing = tmp_path / "existing"
    existing.write_text("placeholder", encoding="utf-8")
    nrrd_path = tmp_path / "missing.nrrd" if missing_name == "missing.nrrd" else existing
    csv_path = tmp_path / "missing.csv" if missing_name == "missing.csv" else existing
    with pytest.raises(SystemExit) as error:
        run_pipeline(str(nrrd_path), str(csv_path), str(tmp_path / "out.mp4"))
    assert error.value.code == 1
    assert "not found" in capsys.readouterr().err


def test_main_requires_exactly_three_arguments(monkeypatch, capsys):
    monkeypatch.setattr(Ex0.sys, "argv", ["Ex0.py", "only-one-argument"])
    with pytest.raises(SystemExit) as error:
        Ex0.main()
    assert error.value.code == 1
    assert "Usage:" in capsys.readouterr().err

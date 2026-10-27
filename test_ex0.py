import os
import numpy as np
from Ex0 import (
    project_plane_kernel,
    validate_plane_geometry,
    normalize_volume_to_uint8,
    run_pipeline,
)
from generate_sample_data import create_synthetic_nrrd, create_sample_csv


def test_isosceles_triangle_projection():
    volume = np.full((100, 100, 100), 200, dtype=np.uint8)
    a = np.array([50.0, 10.0, 50.0])
    b = np.array([10.0, 90.0, 50.0])
    c = np.array([90.0, 90.0, 50.0])

    assert validate_plane_geometry(a, a, b, c)
    proj = project_plane_kernel(volume, a, a, b, c)
    assert proj.shape[0] > 0 and proj.shape[1] > 0
    mid_y = proj.shape[0] // 2
    mid_x = proj.shape[1] // 2
    assert proj[mid_y, mid_x] == 200.0


def test_out_of_bounds_handling():
    volume = np.full((50, 50, 50), 255, dtype=np.uint8)
    a1 = np.array([200.0, 200.0, 200.0])
    a2 = np.array([200.0, 250.0, 200.0])
    b = np.array([250.0, 200.0, 200.0])
    c = np.array([250.0, 250.0, 200.0])

    proj = project_plane_kernel(volume, a1, a2, b, c)
    assert np.all(proj == 0.0)


def test_bit_depth_normalization():
    vol16 = np.array([[[0, 32768, 65535]]], dtype=np.uint16)
    norm = normalize_volume_to_uint8(vol16)
    assert norm.dtype == np.uint8
    assert norm[0, 0, 0] == 0
    assert norm[0, 0, 2] == 255


def test_end_to_end_demo_and_fps(tmp_path):
    nrrd_file = str(tmp_path / "test.nrrd")
    csv_file = str(tmp_path / "test.csv")
    mp4_file = str(tmp_path / "out.mp4")

    create_synthetic_nrrd(nrrd_file, size=128)
    create_sample_csv(csv_file, size=128, num_frames=60)

    fps = run_pipeline(nrrd_file, csv_file, mp4_file)
    assert os.path.isfile(mp4_file)
    assert os.path.getsize(mp4_file) > 0
    assert fps >= 30.0

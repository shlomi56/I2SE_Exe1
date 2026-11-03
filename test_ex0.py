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

import os
import sys
import subprocess
import numpy as np
import nrrd
import pytest
from Ex0 import parse_csv_planes


def test_cli_missing_arguments():
    """1. CLI Argument Validation: Ensure Ex0.py exits with an error when given too few arguments."""
    result = subprocess.run(
        [sys.executable, "Ex0.py", "only_one_arg.nrrd"],
        capture_output=True,
        text=True
    )
    assert result.returncode != 0, "Program should fail with non-zero exit code when arguments are missing."


def test_missing_input_files(tmp_path):
    """2. Missing File Handling: Ensure Ex0.py handles non-existent NRRD or CSV files gracefully."""
    fake_nrrd = str(tmp_path / "does_not_exist.nrrd")
    fake_csv = str(tmp_path / "does_not_exist.csv")
    out_mp4 = str(tmp_path / "out.mp4")

    result = subprocess.run(
        [sys.executable, "Ex0.py", fake_nrrd, fake_csv, out_mp4],
        capture_output=True,
        text=True
    )
    # Should either return a non-zero exit code or print an error without generating an output video
    assert result.returncode != 0 or not os.path.exists(out_mp4)


def test_course_csv_and_comment_parsing(tmp_path):
    """3. Course CSV Format & Comments: Verify 10/13-column rows and '#' comments are parsed properly."""
    csv_file = tmp_path / "course_format.csv"
    csv_file.write_text(
        "Number of Points (3 or 4),x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4\n"
        "# Comment line that must be ignored\n"
        "3,10,10,10,20,10,10,15,20,10,,,\n"
        "4,0,0,0,0,10,0,10,0,0,10,10,0\n",
        encoding="utf-8"
    )
    planes = parse_csv_planes(str(csv_file))
    assert len(planes) == 2
    # Check 3-point triangle (a1 and a2 should be identical)
    a1, a2, b, c = planes[0]
    assert np.allclose(a1, a2)
    # Check 4-point trapezoid (a1 and a2 should be distinct)
    a1_trap, a2_trap, _, _ = planes[1]
    assert not np.allclose(a1_trap, a2_trap)


def test_empty_or_comments_only_csv(tmp_path):
    """4. Empty CSV Edge Case: Ensure a CSV with only headers and comments returns an empty list."""
    empty_csv = tmp_path / "empty.csv"
    empty_csv.write_text(
        "Number of Points (3 or 4),x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4\n"
        "# Only comments here\n"
        "   \n",
        encoding="utf-8"
    )
    planes = parse_csv_planes(str(empty_csv))
    assert planes == []


def test_end_to_end_mp4_generation(tmp_path):
    """5. End-to-End Video Generation: Run the full CLI pipeline on a synthetic volume and verify the MP4 file."""
    nrrd_path = str(tmp_path / "tiny_scan.nrrd")
    csv_path = str(tmp_path / "tiny_planes.csv")
    mp4_path = str(tmp_path / "tiny_output.mp4")

    # Create a small 32x32x32 3D volume
    volume = np.random.randint(0, 255, size=(32, 32, 32), dtype=np.uint8)
    nrrd.write(nrrd_path, volume)

    # Create a 5-frame CSV file
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("Number of Points (3 or 4),x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4\n")
        for z in range(5, 10):
            f.write(f"4,0,0,{z},0,31,{z},31,0,{z},31,31,{z}\n")

    result = subprocess.run(
        [sys.executable, "Ex0.py", nrrd_path, csv_path, mp4_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Ex0.py failed with stderr: {result.stderr}"
    assert os.path.exists(mp4_path), "MP4 file was not created."
    assert os.path.getsize(mp4_path) > 0, "MP4 file is empty (0 bytes)."
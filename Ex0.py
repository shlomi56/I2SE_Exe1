import sys
import os
import csv
import time
import math
import numpy as np
import nrrd
import cv2
from numba import njit, prange


@njit(parallel=True, fastmath=True)
def project_plane_kernel(volume, a1_init, a2_init, b, c):
    # 1. Calculate distances Dab = dist(a1, b) and Dbc = dist(b, c)
    vec_ab_x = b[0] - a1_init[0]
    vec_ab_y = b[1] - a1_init[1]
    vec_ab_z = b[2] - a1_init[2]
    Dab = math.sqrt(vec_ab_x**2 + vec_ab_y**2 + vec_ab_z**2)

    vec_ac_x = c[0] - a2_init[0]
    vec_ac_y = c[1] - a2_init[1]
    vec_ac_z = c[2] - a2_init[2]
    Dac = math.sqrt(vec_ac_x**2 + vec_ac_y**2 + vec_ac_z**2)

    vec_bc_x = c[0] - b[0]
    vec_bc_y = c[1] - b[1]
    vec_bc_z = c[2] - b[2]
    Dbc = math.sqrt(vec_bc_x**2 + vec_bc_y**2 + vec_bc_z**2)

    height = int(round(Dab))
    width = int(round(Dbc))

    if height <= 0 or width <= 0:
        return np.zeros((10, 10), dtype=np.float32)

    # 2. Normalized vectors v(a,b) and v(a,c)
    v_ab_x, v_ab_y, v_ab_z = vec_ab_x / Dab, vec_ab_y / Dab, vec_ab_z / Dab
    v_ac_x, v_ac_y, v_ac_z = vec_ac_x / Dac, vec_ac_y / Dac, vec_ac_z / Dac

    # 3. Output 2D Matrix E
    E = np.zeros((height, width), dtype=np.float32)
    sx, sy, sz = volume.shape

    # 5. Parallelized loop: y runs from 0 up to Dab
    for y in prange(height):
        step = y + 1.0
        a1_x = a1_init[0] + step * v_ab_x
        a1_y = a1_init[1] + step * v_ab_y
        a1_z = a1_init[2] + step * v_ab_z

        a2_x = a2_init[0] + step * v_ac_x
        a2_y = a2_init[1] + step * v_ac_y
        a2_z = a2_init[2] + step * v_ac_z

        dx = a2_x - a1_x
        dy = a2_y - a1_y
        dz = a2_z - a1_z
        d12 = math.sqrt(dx * dx + dy * dy + dz * dz)

        if d12 > 1e-6:
            dp_x = dx / d12
            dp_y = dy / d12
            dp_z = dz / d12
        else:
            dp_x, dp_y, dp_z = 0.0, 0.0, 0.0

        limit_x1 = int(d12)
        offset_x = (Dbc * 0.5) - (d12 * 0.5)

        for x1 in range(limit_x1 + 1):
            px = int(round(a1_x + x1 * dp_x))
            py = int(round(a1_y + x1 * dp_y))
            pz = int(round(a1_z + x1 * dp_z))

            # REQ-05: Out-of-Bounds check
            if 0 <= px < sx and 0 <= py < sy and 0 <= pz < sz:
                v = float(volume[px, py, pz])
            else:
                v = 0.0

            x_idx = int(round(offset_x + x1))
            if 0 <= x_idx < width:
                E[y, x_idx] = v

    return E


def validate_plane_geometry(a1, a2, b, c, eps=0.001):
    dab = np.linalg.norm(b - a1)
    dac = np.linalg.norm(c - a2)
    da1a2 = np.linalg.norm(a2 - a1)
    dbc = np.linalg.norm(c - b)
    return (abs(dab - dac) < eps) and (da1a2 <= dbc + eps)


def parse_csv_planes(csv_path):
    planes = []
    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for row_idx, row in enumerate(reader):
            if not row:
                continue
            # Clean empty cells (such as trailing ,,, on 3-point rows)
            cleaned = [token.strip() for token in row if token.strip() != ""]
            if not cleaned or cleaned[0].startswith("#"):
                continue
            try:
                coords = [float(val) for val in cleaned]
            except ValueError:
                # Skip header row
                continue

            # Course CSV format: leading column is 3 (10 values) or 4 (13 values)
            if len(coords) == 10 and int(coords[0]) == 3:
                coords = coords[1:]
            elif len(coords) == 13 and int(coords[0]) == 4:
                coords = coords[1:]

            if len(coords) == 9:
                a = np.array(coords[0:3], dtype=np.float64)
                b = np.array(coords[3:6], dtype=np.float64)
                c = np.array(coords[6:9], dtype=np.float64)
                planes.append((a, a.copy(), b, c))
            elif len(coords) == 12:
                a1 = np.array(coords[0:3], dtype=np.float64)
                a2 = np.array(coords[3:6], dtype=np.float64)
                b = np.array(coords[6:9], dtype=np.float64)
                c = np.array(coords[9:12], dtype=np.float64)
                planes.append((a1, a2, b, c))
            else:
                print(f"Warning: Row {row_idx + 1} has {len(coords)} values. Skipping.")
    return planes

def normalize_volume_to_uint8(volume):
    if volume.dtype == np.uint8:
        return np.ascontiguousarray(volume)
    v_min = float(np.min(volume))
    v_max = float(np.max(volume))
    if v_max > v_min:
        scaled = ((volume.astype(np.float32) - v_min) / (v_max - v_min) * 255.0).astype(np.uint8)
    else:
        scaled = np.zeros_like(volume, dtype=np.uint8)
    return np.ascontiguousarray(scaled)


def run_pipeline(nrrd_path, csv_path, mp4_path):
    if not os.path.isfile(nrrd_path):
        print(f"Error: NRRD file not found at '{nrrd_path}'", file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(csv_path):
        print(f"Error: CSV file not found at '{csv_path}'", file=sys.stderr)
        sys.exit(1)

    print(f"Loading 3D volume from '{nrrd_path}'...")
    raw_volume, _ = nrrd.read(nrrd_path)
    volume = normalize_volume_to_uint8(raw_volume)
    print(f"Volume loaded: shape={volume.shape}, original_dtype={raw_volume.dtype}")

    planes = parse_csv_planes(csv_path)
    if not planes:
        print("Error: No valid plane coordinates found in the CSV file.", file=sys.stderr)
        sys.exit(1)
    print(f"Loaded {len(planes)} cutting planes from '{csv_path}'.")

    first_a1, first_a2, first_b, first_c = planes[0]
    first_frame = project_plane_kernel(volume, first_a1, first_a2, first_b, first_c)
    frame_h, frame_w = first_frame.shape

    frames = []
    start_time = time.perf_counter()

    for a1, a2, b, c in planes:
        proj = project_plane_kernel(volume, a1, a2, b, c)
        frames.append(proj.astype(np.uint8))

    elapsed = time.perf_counter() - start_time
    fps = len(planes) / elapsed if elapsed > 0 else float("inf")
    print(f"Projection completed: {len(planes)} frames in {elapsed:.4f}s ({fps:.2f} FPS)")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(mp4_path, fourcc, 30.0, (frame_w, frame_h), isColor=True)

    if not writer.isOpened():
        print(f"Error: Could not open video writer for '{mp4_path}'", file=sys.stderr)
        sys.exit(1)

    for frame in frames:
        if frame.shape[0] != frame_h or frame.shape[1] != frame_w:
            frame = cv2.resize(frame, (frame_w, frame_h), interpolation=cv2.INTER_NEAREST)
        bgr_frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        writer.write(bgr_frame)

    writer.release()
    print(f"Successfully saved output video to '{mp4_path}'.")
    return fps


def main():
    if len(sys.argv) != 4:
        print("Usage: python Ex0.py <file.nrrd> <file.csv> <file.mp4>", file=sys.stderr)
        sys.exit(1)
    run_pipeline(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()

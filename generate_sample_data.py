import os
import csv
import numpy as np
import nrrd


def create_synthetic_nrrd(filepath, size=256):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    x, y, z = np.ogrid[:size, :size, :size]
    center = size // 2
    dist_from_center = np.sqrt((x - center)**2 + (y - center)**2 + (z - center)**2)

    volume = np.zeros((size, size, size), dtype=np.uint8)
    volume[(dist_from_center <= size * 0.4) & (dist_from_center >= size * 0.3)] = 180
    c_min, c_max = int(size * 0.38), int(size * 0.62)
    volume[c_min:c_max, c_min:c_max, c_min:c_max] = 255

    nrrd.write(filepath, volume)
    print(f"Generated sample NRRD volume at '{filepath}' (shape: {volume.shape})")


def create_sample_csv(filepath, size=256, num_frames=90):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, mode="w", newline="") as f:
        writer = csv.writer(f)
        for i in range(num_frames):
            z = float(i * (size / num_frames))
            a1 = [0.0, 0.0, z]
            a2 = [0.0, float(size - 1), z]
            b = [float(size - 1), 0.0, z]
            c = [float(size - 1), float(size - 1), z]
            writer.writerow(a1 + a2 + b + c)
    print(f"Generated sample CSV planes at '{filepath}' ({num_frames} frames)")


if __name__ == "__main__":
    create_synthetic_nrrd("data/sample_scan.nrrd", size=256)
    create_sample_csv("data/sample_planes.csv", size=256, num_frames=90)

# I2SE_Exe1 — 3D Volume Plane Projection

## Overview

This project implements a command-line tool that reads a 3D volume stored in NRRD format, reads a sequence of plane definitions from a CSV file, projects the volume onto each plane, and writes the resulting 2D frames to an MP4 video.

The implementation is written in Python and uses NumPy, Numba, pynrrd, and OpenCV.

## Problem Statement

Given a 3D volume \(M\) and a sequence of planes defined by coordinates, calculate a 2D projection for each plane and combine the projections into a video.

The exact mapping between arbitrary plane geometry and output pixels is a design concern. The current implementation uses distance calculations and directional sampling; its behavior for every possible planar quadrilateral has not yet been fully verified. See [Known Issues and Limitations](#known-issues-and-limitations).

## Input and Output

### Input volume

The application accepts a `.nrrd` file containing a 3D raster volume. The assignment describes volume dimensions up to \(500 \times 500 \times 500\), with voxel values represented using unsigned integer types.

The current implementation converts non-`uint8` input volumes to 8-bit values by scaling the volume's minimum and maximum values to the range 0–255. A constant-valued volume is converted to zeros.

### Plane coordinates

The application accepts a CSV file containing one plane definition per row:

- **Three-point definition:** 9 numeric coordinate values, interpreted as three 3D points.
- **Four-point definition:** 12 numeric coordinate values, interpreted as four 3D points.

The assignment is understood to guarantee that supplied points describe valid, non-degenerate shapes and that all four points in a four-point definition lie on the same plane. A four-point shape may be a square, trapezoid, or another valid planar quadrilateral.

The CSV is processed in top-down row order: the first data row defines the first projection frame, followed by subsequent rows in order. Rows with unsupported numbers of coordinate values are skipped with a warning.

### Output

The application writes an `.mp4` video. Each accepted CSV plane produces a frame, in CSV order. Samples that fall outside the 3D volume are assigned a value of `0`.

## Requirements and Performance Targets

- Correctly read the input NRRD volume and CSV plane definitions.
- Generate a 2D projection for each accepted plane.
- Use zero for samples outside the volume.
- Encode the projections into an MP4 video.
- Achieve at least **30 FPS** for a \(500 \times 500 \times 500\) volume; **100 FPS or more** is the stated target.

Performance numbers should be interpreted according to the measurement method. The current reported measurement focuses on projection throughput; it does not represent the complete end-to-end time for projection plus video encoding, and initial JIT compilation is not included in the measured projection interval.

## Usage

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the program with exactly three positional arguments:

```bash
python Ex0.py file.nrrd file.csv file.mp4
```

Arguments are:

1. `file.nrrd` — input 3D volume.
2. `file.csv` — plane coordinates, one plane per row.
3. `file.mp4` — destination video path.

## Generating Sample Data and Running Tests

The repository includes a sample-data generator and tests.

```bash
python generate_sample_data.py
pytest
```

Check the scripts' help text or source for the exact sample-data output paths, if applicable.

## Repository Contents

- `Ex0.py` — projection implementation and command-line entry point.
- `SRS.md` — Software Requirements Specification.
- `generate_sample_data.py` — generates synthetic volume and plane data.
- `test_ex0.py` — automated tests.
- `requirements.txt` — Python dependencies.
- `build_project.py` — generates project files from embedded templates. Review its behavior before running it, because it may overwrite existing files.

## Available Volumes

The repository documentation lists the following datasets. Confirm that the corresponding data files are present locally before running the program.

### 1. Biscuit Cake
- **File:** `biscuit_cake.nrrd`
- **Dimensions:** 256 × 256 × 130
- **Voxel size:** 1 × 1 × 1.3 mm
- **Type:** `uint16`

### 2. Swiss Roll
- **File:** `swiss_roll.nrrd`
- **Dimensions:** 256 × 256 × 130
- **Voxel size:** 1.1 × 1.1 × 1.43 mm
- **Type:** Verify the source dataset's actual type; earlier documentation listed `unit32`, which appears to be a typo.

### 3. Onion
- **File:** `onion.nrrd`
- **Dimensions:** 256 × 256 × 130
- **Voxel size:** 0.55 × 0.55 × 0.715 mm
- **Type:** `uint8`

### 4. Croissant
- **File:** `croissant.nrrd`
- **Dimensions:** 500 × 500 × 500
- **Voxel size:** 0.37 × 0.37 × 0.37 mm
- **Type:** `uint8`

### 5. MR Head
- **File:** `MRHead_1.nrrd`
- **Dimensions:** 256 × 256 × 130
- **Voxel size:** 1 × 1 × 1.3 mm
- **Type:** Verify the source dataset's actual type; earlier documentation listed `unit16`, which appears to be a typo.

## Experimental Results

Previously recorded projection-throughput results on an Apple Silicon Mac are shown below. These are measurements reported by the project, not independent benchmark results. Because the timing excludes video encoding and initial JIT compilation, these values should not be presented as end-to-end video-generation FPS.

| Scan | Dimensions | Frames | Reported projection throughput |
|---|---:|---:|---:|
| Croissant | 500 × 500 × 500 | 150 | 1967.35 FPS |
| MR Head | 256 × 256 × 130 | 130 | 5691.36 FPS |
| Onion | 256 × 256 × 130 | 130 | 5541.21 FPS |
| Swiss Roll | 256 × 256 × 130 | 130 | 5511.77 FPS |
| Biscuit Cake | 256 × 256 × 130 | 130 | 5606.46 FPS |

The results above indicate projection throughput only. A separate end-to-end benchmark would need to time volume loading, plane parsing, projection, and video writing together.

## Known Issues and Limitations

1. **Shape-dependent sampling:** The current algorithm constructs rows by advancing points along direction vectors and sampling the line between them. Row lengths can vary for trapezoids and irregular quadrilaterals, while the output matrix has a fixed width. Depending on the input geometry, this may leave unused pixels, shift samples, clip part of the intended shape, or distort the projection.
2. **Boundary convention:** The current row sampling starts with a step of `y + 1.0`. The intended treatment of the plane boundary should be confirmed, since this may omit the initial boundary depending on the coordinate convention.
3. **Voxel spacing and physical coordinates:** The assignment's coordinate convention has not yet been confirmed. The implementation should not be assumed to account for NRRD voxel spacing, origin, or orientation unless this is explicitly implemented.
4. **Performance scope:** The reported FPS is projection throughput, not full pipeline throughput. Initial JIT compilation and video encoding are excluded from that timing.
5. **Input validation:** The assignment is assumed to supply valid, non-degenerate plane definitions. The implementation's geometric validation is limited, and arbitrary quadrilateral projection correctness remains unverified.

These issues are documented for transparency; this README does not claim that they have been fixed.

# Software Requirements Specification (SRS)
## 3D Volume Plane Projection — I2SE_Exe1

## 1. Introduction

### 1.1 Purpose

This document specifies the functional and non-functional requirements for the 3D Volume Plane Projection application. It describes the expected inputs, processing, outputs, constraints, and known limitations.

### 1.2 Scope

The application is a Python command-line tool that reads a 3D volume from an NRRD file, reads a sequence of plane definitions from a CSV file, generates a 2D projection for each plane, and encodes the frames into an MP4 video.

A graphical user interface is outside the scope of this project.

### 1.3 Definitions and Abbreviations

- **NRRD:** Nearly Raw Raster Data, a format used to store multidimensional raster data.
- **Voxel:** A value at a discrete location in a 3D volume.
- **Plane projection:** The process of sampling the 3D volume at positions associated with a specified plane to create a 2D matrix.
- **CSV:** Comma-Separated Values.
- **FPS:** Frames per second.
- **CLI:** Command-line interface.
- **JIT:** Just-in-time compilation.

### 1.4 References

- Project assignment: Software Engineering Ex1 / 3D volume plane projection.
- Project implementation: `Ex0.py`.
- Project documentation: `README.md`.

### 1.5 Document Overview

Section 2 describes the product, users, environment, constraints, and assumptions. Section 3 defines the external interfaces and functional and non-functional requirements. Section 4 contains use cases, a data dictionary, and a requirements traceability matrix.

## 2. Overall Description

### 2.1 Product Perspective

The application is a standalone command-line processing pipeline. It does not require a graphical interface or a network service. It uses Python libraries to read volume data, calculate projections, and encode video frames.

### 2.2 Product Functions

The system shall:
1. Accept an NRRD input path, a CSV coordinate path, and an MP4 output path.
2. Load the 3D volume into memory.
3. Parse plane definitions from the CSV file in row order.
4. Generate a 2D projection for each accepted plane.
5. Use a pixel value of zero for projected sample positions outside the volume.
6. Write the projections to an MP4 video in the same order as the accepted CSV rows.

### 2.3 User Classes

- **Command-line user:** Runs the application and supplies the input and output paths.
- **Developer/tester:** Installs dependencies, runs automated tests, and evaluates projection correctness and performance.

### 2.4 Operating Environment

The application requires a Python environment with the packages listed in `requirements.txt`. The implementation uses NumPy, Numba, pynrrd, and OpenCV. It is intended to run locally from a terminal or command prompt.

### 2.5 Constraints

- The application shall be invoked through a CLI.
- The command shall accept exactly three positional arguments: input NRRD, input CSV, and output MP4.
- The implementation language is Python.
- The volume may contain unsigned 8-bit, 16-bit, or 32-bit values; the current implementation normalizes non-`uint8` values to `uint8` before projection.
- Performance is important for large volumes, including a \(500 \times 500 \times 500\) volume.

### 2.6 Assumptions and Dependencies

- The input NRRD file exists and can be read by the installed NRRD library.
- The CSV contains one plane definition per row and is processed in top-down row order: the first data row defines the first projection frame, followed by subsequent rows in order.
- A plane definition contains either three 3D points (9 numeric values) or four 3D points (12 numeric values).
- Input points are guaranteed by the assignment to define valid, non-degenerate shapes.
- For four-point definitions, all four points are guaranteed to lie on the same plane. The shape may be a square, trapezoid, or another valid planar quadrilateral.
- The intended interpretation of coordinates—voxel indices versus physical coordinates—has not yet been confirmed. Voxel spacing, origin, and orientation should not be assumed to be applied by the implementation.
- The current projection algorithm's correctness for every possible planar quadrilateral has not been verified.

### 2.7 Known Implementation Limitations

These are known or unresolved implementation concerns, not additional input guarantees:

- The algorithm samples rows between points advanced along direction vectors. Row lengths may vary for trapezoids and irregular quadrilaterals, while the output matrix has a fixed width. This can potentially cause unused pixels, shifted samples, clipping, or geometric distortion.
- Sampling uses a row step of `y + 1.0`, so the boundary convention needs verification.
- Geometric validation is limited; correctness for arbitrary planar quadrilaterals remains to be verified.
- Reported FPS measures projection throughput and excludes video encoding and initial JIT compilation. It therefore does not by itself establish end-to-end pipeline performance.

## 3. Specific Requirements

### 3.1 External Interfaces

#### REQ-01 — CLI Execution

The system shall accept exactly three positional arguments in this order:

```bash
python Ex0.py file.nrrd file.csv file.mp4
```

The arguments identify the input volume, plane-coordinate file, and output video.

#### REQ-02 — Input Volume Interface

The system shall read a 3D volume from the NRRD file specified by the first argument.

#### REQ-03 — Plane Coordinate Interface

The system shall read the CSV file specified by the second argument. Each accepted row shall define one plane using either three 3D points (9 numeric values) or four 3D points (12 numeric values). The system shall process accepted rows in their original top-down CSV order, so the first data row defines the first projection frame.

#### REQ-04 — Output Video Interface

The system shall write the generated 2D projection frames to an MP4 file at the output path specified by the third argument.

### 3.2 Functional Requirements

#### REQ-05 — Volume Value Normalization

The system shall convert non-`uint8` volume data to 8-bit values before projection. For non-constant volumes, values shall be scaled from the input volume's minimum and maximum to the range 0–255. A constant-valued volume shall be converted to zeros.

#### REQ-06 — Plane Projection

For each accepted plane definition, the system shall calculate a 2D projection matrix by sampling the 3D volume at positions derived from the input coordinates.

The projection shall use the coordinate-derived directions and distances implemented by the system. Exact pixel mapping for arbitrary planar quadrilaterals is a known limitation and has not yet been verified for all valid shapes.

#### REQ-07 — Out-of-Bounds Sampling

If a calculated sample position lies outside the bounds of the 3D volume, the system shall assign the corresponding projection pixel a value of `0`.

#### REQ-08 — Frame Ordering

The system shall preserve the top-down order of accepted CSV plane definitions in the output video: the first accepted data row shall produce the first frame, followed by subsequent accepted rows in order.

#### REQ-09 — Invalid CSV Rows

If a CSV row contains an unsupported number of coordinate values or cannot be parsed as expected, the system shall skip the row and issue a warning, as supported by the current implementation.

#### REQ-10 — Missing Input Paths

If a required input path does not exist, the system shall report an error and stop processing rather than continuing as if the input were available.

### 3.3 Non-Functional Requirements

#### NFR-01 — Minimum Projection Performance

For a \(500 \times 500 \times 500\) input volume, the projection algorithm shall achieve a minimum processing rate of 30 frames per second under the agreed test conditions.

The benchmark conditions shall state whether initial JIT compilation is excluded. Projection-only FPS shall not be reported as end-to-end video-generation FPS.

#### NFR-02 — Target Projection Performance

The target is to exceed 100 projected frames per second under the agreed test conditions.

#### NFR-03 — Stability

The system shall handle input-path errors and unsupported CSV rows without silently treating them as valid plane definitions.

#### NFR-04 — Output Consistency

Each accepted plane shall produce one projection frame, and out-of-bounds samples shall use the defined value of zero.

#### NFR-05 — Maintainability

The implementation should keep input parsing, projection, normalization, and video writing sufficiently separated to allow these stages to be tested and measured independently.

## 4. Appendices

### 4.1 Use Cases

#### UC-01 — Generate Projection Video

- **Actor:** Command-line user.
- **Preconditions:**
  - The user has installed the required Python dependencies.
  - The input NRRD and CSV files exist and are readable.
  - The coordinate rows follow one of the supported formats.
- **Main flow:**
  1. The user runs `python Ex0.py file.nrrd file.csv file.mp4`.
  2. The system checks the required input paths.
  3. The system loads the NRRD volume.
  4. The system normalizes the volume to 8-bit values if needed.
  5. The system parses the CSV plane definitions.
  6. The system calculates one projection for each accepted plane.
  7. The system writes the projections in sequence to the MP4 file.
  8. The system releases the video writer and finishes processing.
- **Alternative flows:**
  - **A1 — Missing input:** The system reports the missing path and stops.
  - **A2 — Unsupported CSV row:** The system warns about the row and skips it.
  - **A3 — Out-of-bounds sample:** The system assigns zero to that projection pixel and continues.
  - **A4 — Output-writing failure:** The system should report the failure if detected by the video-writing stage.
- **Postcondition:** The output MP4 contains the generated projection frames if processing completes successfully.

### 4.2 Data Dictionary

| Data item | Description | Representation |
|---|---|---|
| Input volume | 3D raster data loaded from NRRD | 3D NumPy array |
| Plane row | One plane definition in the CSV | 9 or 12 numeric coordinate values |
| 3D point | Coordinate used to define a plane | Three numeric values `(x, y, z)` |
| Projection matrix | 2D samples from the input volume | 2D NumPy array of 8-bit values |
| Out-of-bounds sample | Sample coordinate outside the volume dimensions | Pixel value `0` |
| Output video | Ordered projection frames | MP4 file |
| Projection FPS | Number of projections calculated per second during the measured projection interval | Frames/second; excludes encoding and initial JIT compilation in the current measurement |

### 4.3 Requirements Traceability Matrix

| Requirement | Main implementation location | Verification approach |
|---|---|---|
| REQ-01 — CLI execution | `Ex0.py` entry point | Run with three arguments; verify argument handling |
| REQ-02 — Load volume | `run_pipeline()` and NRRD loading | Test with a valid NRRD file and a missing path |
| REQ-03 — Parse plane coordinates | `parse_csv_planes()` | Test 9-value and 12-value rows, malformed rows, and row order |
| REQ-04 — Write output video | `run_pipeline()` and OpenCV writer | Verify output file is created and can be opened |
| REQ-05 — Normalize values | `normalize_volume_to_uint8()` | Test `uint8`, non-`uint8`, and constant-valued volumes |
| REQ-06 — Project plane | `project_plane_kernel()` | Compare known simple planes against expected projections; add tests for trapezoids and irregular quadrilaterals |
| REQ-07 — Out-of-bounds handling | `project_plane_kernel()` | Test coordinates outside each volume boundary |
| REQ-08 — Frame ordering | `run_pipeline()` | Use distinguishable planes and verify frame sequence |
| REQ-09 — Invalid CSV rows | `parse_csv_planes()` | Verify unsupported or malformed rows are warned about and skipped |
| REQ-10 — Missing input paths | `run_pipeline()` | Test missing NRRD and CSV paths |
| NFR-01 — Minimum performance | Projection timing in `run_pipeline()` | Benchmark a \(500^3\) volume under documented conditions |
| NFR-02 — Target performance | Projection timing in `run_pipeline()` | Benchmark projection throughput and report timing conditions |
| NFR-03 — Stability | Input parsing and pipeline checks | Run invalid-input tests |
| NFR-04 — Output consistency | Projection and video-writing stages | Verify one frame per accepted plane and zero out-of-bounds values |
| NFR-05 — Maintainability | Overall module structure | Review separation of processing stages and test coverage |

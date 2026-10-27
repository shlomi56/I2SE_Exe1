# Software Requirements Specification (SRS)

## 1. Introduction
* **Purpose:** To define the functional and non-functional requirements for the 3D-to-2D Medical Scan Projection CLI application.
* **Scope:** The system is a Python-based utility that ingests 3D medical scans in NRRD format, processes specific cutting planes defined by coordinates in a CSV file, and outputs a chronological 2D projection sequence as an MP4 video.

## 2. Specific Requirements
* **REQ-01 (CLI Execution):** `python Ex0.py file.nrrd file.csv file.mp4`
* **REQ-02 (Data Ingestion):** Read 3D matrix from `.nrrd` file path.
* **REQ-03 (Coordinate Parsing):** Parse `.csv` file rows into 2D cutting planes.
* **REQ-04 (Slice Projection):** Sample exact pixels along normalized vectors.
* **REQ-05 (Out-of-Bounds Handling):** Assign `0` (black) for out-of-bounds coordinates.
* **REQ-06 (Video Encoding):** Encode 2D projections sequentially into `.mp4`.
* **NFR-01 / NFR-02 (Performance):** Minimum 30 FPS, target 100+ FPS on 500x500x500 volume.

# I2SE_Exe1
Algorithm: Implementing a plane projection of 3D volume
## Overview
This repository contains the implementation of a 3D-to-2D projection algorithm. The system is built as a command-line interface (CLI) tool that reads a 3D raster data matrix from an `.nrrd` file, processes a series of geometric cutting planes defined in a `.csv` file, and outputs a sequential 2D projection as an `.mp4` video file. 

## Problem Statement
Given a 3D raster data matrix (M), and a plane (p). Compute the 2D matrix (image) of the projection of p in V.

## Problem Definition
Given a 3D matrix (M) of size sx*sy*sz byte values (the entry M[x][y][z] is an unsigned integer value of 8, 16, 32 bits), where 1<=sx,sy,sz<2^10 and 0<=x<sx, 0<=y<sy, 0<=z<sz.

Out-of-bounds sampling: If a calculated point on the plane falls outside the boundaries of the 3D matrix, its value in the 2D projection is strictly defined as `0`.

## Implementation Requirements
* **Design First:** The implementation is secondary to the design. A well-structured, modular, and optimized approach is required.
* **Language Agnostic:** The code is implemented in Python
* **Stability:** The code must be correct and stable, properly handling file parsing, coordinate calculations, and out-of-bounds matrix indexing.
* **Performance / Runtime:** Code efficiency is highly prioritized due to the scale of the matrices. 
  * Given a matrix of size 500^3 bytes, a runtime of **at least 30 FPS is a must**.
  *A runtime of **at least 100 FPS is expected**.
  (On an M2 Mac 2013).
  

## Setup & Execution Guide

### 1. Prerequisites
Ensure the target machine has:
* **Python 3.9+** installed (`python3 --version`).
* **Git** installed (`git --version`).
* System C/C++ compiler tools (required by Numba/LLVM depending on the OS).

### 2. Clone the Repository
Open a terminal (macOS/Linux) or Command Prompt/PowerShell (Windows) and clone the repository:
```bash
git clone https://github.com/shlomi56/I2SE_Exe1.git
cd I2SE_Exe1
```
### 3. Set Up a Virtual Environment (Recommended)

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```
### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install numpy pynrrd opencv-python numba pytest
```
### 5. Run the Automated Test Suite

```bash
python3 -m pytest test_ex0.py test_ex0_generalized.py -v
```
### 6. Run the Application

```bash
python3 Ex0.py <data/path_to_input.nrrd> <data/path_to_input.csv> <path_to_output.mp4>
```
### 7. Build the Executable (Optional)
**What this does:** Uses PyInstaller via the `build_project.py` script to bundle the Python code and all of its dependencies into a single, standalone binary application. This allows the program to be run on machines that do not have Python installed.

```bash
pip install pyinstaller
python3 build_project.py

```
## Dataset Overview

This repository contains various 3D volumetric datasets (stored in NRRD format). Below is an overview of the available volumes, demonstrating axial, coronal, sagittal, and oblique slices.

## Available Volumes

### 1. Biscuit Cake
<img width="1760" height="506" alt="biscuit_cake" src="https://github.com/user-attachments/assets/db6d4822-0951-46d1-9078-08ab6acaf1ab" />

* **File:** `biscuit_cake.nrrd`
* **Dimensions:** 256 x 256 x 130
* **Voxel Size:** 1 x 1 x 1.3 mm
* **Type:** uint16

---

### 2. Swiss Roll
<img width="1760" height="506" alt="swiss_roll" src="https://github.com/user-attachments/assets/4d779254-db09-4fae-aeb2-919ed991d8f8" />

* **File:** `swiss_roll.nrrd`
* **Dimensions:** 256 x 256 x 130
* **Voxel Size:** 1.1 x 1.1 x 1.43 mm
* **Type:** unit32

---

### 3. Onion
<img width="1760" height="506" alt="onion" src="https://github.com/user-attachments/assets/c2422155-1c79-470f-aa42-7bc5d52cf850" />

* **File:** `onion.nrrd`
* **Dimensions:** 256 x 256 x 130
* **Voxel Size:** 0.55 x 0.55 x 0.715 mm
* **Type:** uint8

---

### 4. Croissant
<img width="1760" height="506" alt="croissant" src="https://github.com/user-attachments/assets/08b385c4-4884-4404-aa80-3c9c6d57a0a0" />


* **File:** `croissant.nrrd`
* **Dimensions:** 500 x 500 x 500
* **Voxel Size:** 0.37 x 0.37 x 0.37 mm
* **Type:** uint8

---

### 5. MR Head
<img width="1760" height="506" alt="MRHead_1" src="https://github.com/user-attachments/assets/a55cd669-ba34-4523-826f-7156f7421127" />

* **File:** `MRHead_1.nrrd`
* **Dimensions:** 256 x 256 x 130
* **Voxel Size:** 1 x 1 x 1.3 mm
* **Type:** unit16

## Documentation
* [Software Requirements Specification (SRS)](SRS.md) - Detailed functional and non-functional requirements, use cases, and system architecture.

## Experimental Results
The projection algorithm was benchmarked on an Apple Silicon M4 MacBook Pro across 5 different volumetric datasets. The application easily exceeded the required 30 FPS minimum (NFR-01) and the 100 FPS target (NFR-02) for the 500x500x500 matrix constraint.

| Scan Name | Dimensions | Frames Generated | Performance (FPS) | Output File |
| :--- | :--- | :--- | :--- | :--- |
| Croissant | 500 x 500 x 500 | 150 | 1967.35 FPS |  https://github.com/user-attachments/assets/2ad93e57-3d53-4481-b7b1-e0db636fa8b2 |
| MR Head | 256 x 256 x 130 | 130 | 5691.36 FPS |https://github.com/userattachments/assets/20653681-83bb-41d2-9af9-b12730b9d910|
| Onion | 256 x 256 x 130 | 130 | 5541.21 FPS | https://github.com/user-attachments/assets/fba44435-9410-45bd-9a2b-74d3e5d25dec|
| Swiss Roll | 256 x 256 x 130 | 130 | 5511.77 FPS | https://github.com/user-attachments/assets/27b450ff-a889-49b1-89b6-ebdd24ced08f|
| Biscuit Cake | 256 x 256 x 130 | 130 | 5606.46 FPS | https://github.com/user-attachments/assets/335ec5ae-e305-4460-b2ee-729ffb46252f|

## Testing (`test_ex0.py` & `test_ex0_generalized.py`)

Run the full suite of 9 automated unit and integration tests with:
`python3 -m pytest -v`

* **3-Point Plane Parsing:** Verifies isosceles triangle CSV rows (9 values) map correctly to 3D coordinate vectors.
* **4-Point Plane Parsing:** Verifies isosceles trapezoid CSV rows (12 values) map correctly to 3D coordinate vectors.
* **NRRD Volume Loading:** Validates that 3D `.nrrd` matrices load into memory with their original dimensions preserved.
* **Core Projection Algorithm:** Tests 2D slice extraction and guarantees out-of-bounds coordinates safely render as black pixels.
* **CLI Argument Validation:** Confirms `Ex0.py` enforces the 3-argument CLI format and safely exits if arguments are missing.
* **Missing File Handling:** Verifies graceful error handling and safe exits when input `.nrrd` or `.csv` files do not exist.
* **CSV Format & Comments:** Ensures rows with a leading point-count column (`3` or `4`) and `#` comments are parsed properly.
* **Empty CSV Edge Case:** Verifies that CSV files with no coordinate data return an empty list safely instead of crashing.
* **End-to-End MP4 Generation:** Runs the complete CLI pipeline on a synthetic volume to prove OpenCV generates a valid `.mp4` video.
* **`test_ex0_generalized.py`** in addition 124 more generalized tests to the functions themselves.

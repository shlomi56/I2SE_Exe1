# I2SE_Exe1
Algorithm: Implementing a plane projection of 3D volume
## Overview
This repository contains the implementation of a 3D-to-2D projection algorithm. The system is built as a command-line interface (CLI) tool that reads a 3D raster data matrix from an `.nrrd` file, processes a series of geometric cutting planes defined in a `.csv` file, and outputs a sequential 2D projection as an `.mp4` video file. 

## Problem Statement
Given a 3D raster data matrix (M), and a plane (p). Compute the 2D matrix (image) of the projection of p in V *(note: this problem is NOT well-defined for implementation - a detailed design is needed)*.

## Problem Definition
Given a 3D matrix (M) of size sx*sy*sz byte values (the entry M[x][y][z] is an unsigned integer value of 8, 16, 32 bits), where 1<=sx,sy,sz<2^10 and 0<=x<sx, 0<=y<sy, 0<=z<sz.

Out-of-bounds sampling: If a calculated point on the plane falls outside the boundaries of the 3D matrix, its value in the 2D projection is strictly defined as `0`.

## Implementation Requirements
* **Design First:** The implementation is secondary to the design. A well-structured, modular, and optimized approach is required.
* **Language Agnostic:** The code is implemented in Python
* **Stability:** The code must be correct and stable, properly handling file parsing, coordinate calculations, and out-of-bounds matrix indexing.
* **Performance / Runtime:** Code efficiency is highly prioritized due to the scale of the matrices. 
  * Given a matrix of size 500^3 bytes, a runtime of **at least 30 FPS is a must**.
  * A runtime of **at least 100 FPS is expected**. 
  *(To achieve these performance targets in Python, numerical compilation tools such as Numba/JIT are highly recommended).*

## Usage & Execution
The application is executed strictly via the command line with exactly three arguments:

```bash 
python Ex0.py file.nrrd file.csv file.mp4.
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
![Biscuit Cake Slices](path/to/biscuit_cake.png)

---

### 2. Swiss Roll
<img width="1760" height="506" alt="swiss_roll" src="https://github.com/user-attachments/assets/4d779254-db09-4fae-aeb2-919ed991d8f8" />

* **File:** `swiss_roll.nrrd`
* **Dimensions:** 256 x 256 x 130
* **Voxel Size:** 1.1 x 1.1 x 1.43 mm
* **Type:** uint32
![Swiss Roll Slices](path/to/swiss_roll.png)

---

### 3. Onion
<img width="1760" height="506" alt="onion" src="https://github.com/user-attachments/assets/c2422155-1c79-470f-aa42-7bc5d52cf850" />

* **File:** `onion.nrrd`
* **Dimensions:** 256 x 256 x 130
* **Voxel Size:** 0.55 x 0.55 x 0.715 mm
* **Type:** uint8
![Onion Slices](path/to/onion.png)

---

### 4. Croissant
<img width="1760" height="506" alt="croissant" src="https://github.com/user-attachments/assets/08b385c4-4884-4404-aa80-3c9c6d57a0a0" />

* **File:** `croissant.nrrd`
* **Dimensions:** 500 x 500 x 500
* **Voxel Size:** 0.37 x 0.37 x 0.37 mm
* **Type:** uint8
![Croissant Slices](path/to/croissant.jpg)

---

### 5. MR Head
<img width="1760" height="506" alt="MRHead_1" src="https://github.com/user-attachments/assets/a55cd669-ba34-4523-826f-7156f7421127" />

* **File:** `MRHead_1.nrrd`
* **Dimensions:** 256 x 256 x 130
* **Voxel Size:** 1 x 1 x 1.3 mm
* **Type:** int16
![MR Head Slices](path/to/MRHead_1.jpg)

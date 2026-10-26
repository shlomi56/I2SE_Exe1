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
python Ex0.py file.nrrd file.csv file.mp4

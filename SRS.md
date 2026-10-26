[software_requirements_specification.md](https://github.com/user-attachments/files/33969017/software_requirements_specification.md)
# Software Requirements Specification (SRS)

## 1. Introduction
* **Purpose:** To define the functional and non-functional requirements for the 3D-to-2D Medical Scan Projection CLI application.
* **Scope:** The system is a Python-based utility that ingests 3D medical scans in NRRD format, processes specific cutting planes defined by coordinates in a CSV file, and outputs a chronological 2D projection sequence as an MP4 video.
* **Definitions:**
  * **NRRD:** Nearly Raw Raster Data, a format for representing n-dimensional medical image volumes.
  * **FPS:** Frames Per Second, the unit of measurement for processing speed and video playback.
* **References:** Object-Oriented Design (OOD) / Software Engineering Ex1 Assignment prompt.

## 2. Overall Description
* **Product Perspective:** A standalone, command-line data processing pipeline intended to run locally on a user's machine.
* **User Classes:** Software Engineering students, developers, and medical imaging researchers testing 3D projection algorithms.
* **Operating Environment:** A local terminal or command prompt equipped with a standard Python runtime environment and appropriate numerical/computer vision libraries (e.g., Numpy, Numba, OpenCV).
* **Constraints:** The system is constrained strictly to the required CLI format. GUI implementation is out of scope.
* **Assumptions:** It is assumed that the provided CSV file strictly contains valid geometric definitions (either 3 points forming an isosceles triangle or 4 points forming an isosceles trapezoid).

## 3. Specific Requirements

### External Interfaces
* **REQ-01 (CLI Execution):** The system shall accept exactly three positional arguments via the command line interface in the following rigid format: `python Ex0.py file.nrrd file.csv file.mp4`.

### Functional Requirements
* **REQ-02 (Data Ingestion):** The system shall read and load into memory a 3D matrix from the provided `.nrrd` file path.
* **REQ-03 (Coordinate Parsing):** The system shall parse the `.csv` file, treating every row as a separate predefined 2D cutting plane defined by its spatial coordinates.
* **REQ-04 (Slice Projection):** The system shall calculate the normalized vectors and absolute distances between the provided plane coordinates to sample the exact pixels from the 3D NRRD matrix into a 2D projection matrix.
* **REQ-05 (Out-of-Bounds Handling):** The system shall assign a strict pixel value of `0` (black) for any coordinate on the cutting plane that falls outside the boundaries of the original 3D volume.
* **REQ-06 (Video Encoding):** The system shall encode the sequence of generated 2D projections into an `.mp4` video, where row $i$ in the CSV corresponds exactly to frame $i$ in the output video.

### Non-Functional Requirements
* **NFR-01 (Minimum Performance):** The application shall execute the projection algorithm and generate the video at a minimum processing rate of 30 frames per second (FPS) when processing a $500 \times 500 \times 500$ 3D matrix.
* **NFR-02 (Target Performance):** The application should optimally achieve a processing rate exceeding 100 FPS for standard operations.

## 4. Appendices

### Use Cases

#### UC-01: Generate Projection Video
* **Actor:** Command-Line User.
* **Precondition:** A valid `.nrrd` medical scan and a valid `.csv` coordinate file exist at the specified local paths.
* **Main success flow:**
  1. User executes the standard command (`python Ex0.py file.nrrd file.csv file.mp4`).
  2. System validates the file paths and loads the NRRD volume data into memory.
  3. System parses the CSV file sequentially.
  4. System applies the projection algorithm to extract 2D slice matrices for each defined plane.
  5. System writes the extracted 2D matrices sequentially into an MP4 video file.
  6. System gracefully terminates the operation.
* **Alternative flows:**
  * **2a. Missing Input File:** System detects that the `.nrrd` or `.csv` file is missing, outputs an error message to the console, and terminates.
  * **4a. Coordinates Exceed Volume Matrix:** System detects that a calculated point on the requested plane is out of bounds, assigns the pixel a value of `0`, and continues sampling.
* **Postcondition:** An `.mp4` video file accurately representing the sequential CSV cutting planes is saved to the designated output path.

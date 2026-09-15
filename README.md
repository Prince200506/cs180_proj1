# proj1 English Guide

This document explains the implementation logic of the project and how to configure the environment and run the main notebook.

The Chinese version is available in README.md.

## Project Goal

This project implements the classic Prokudin-Gorskii colorization pipeline. The input image is a single grayscale scan with three channels stacked vertically. The goal is to split the scan into blue, green, and red channels, align them to correct for the camera misalignment, and then reconstruct a color image.

## Repository Layout

- code/ : main implementation and notebook
- code/colorize_skel.py : a compact single-scale alignment reference implementation
- code/main.ipynb : the main workflow for loading, splitting, aligning, visualizing, and saving results
- test_images/ : input test images
- test_results/ : output directory for saved results
- CS180_fa2026_proj1_data/ : course-provided dataset
- web/ : static page assets for display

## Implementation Logic

### 1. Load and normalize the input image

main.ipynb reads a stacked grayscale image from test_images/ and normalizes pixel values to the range [0, 1]. This makes later similarity comparisons more stable.

### 2. Split the three channels

The image is divided into three equal vertical sections, which are treated as the blue, green, and red channels. The notebook first computes one third of the image height and then slices the image accordingly.

### 3. Crop black borders

Original glass-plate scans often contain black borders. These borders can hurt alignment quality, so the code crops roughly 10 percent from each side and uses only the central region for matching.

### 4. Compute matching scores

Two similarity metrics are implemented:

- L2 distance: smaller is better.
- NCC, normalized cross-correlation: larger is better.

The scores are computed only on the cropped region so that border artifacts do not dominate the result.

### 5. Single-scale alignment

align_single_scale performs an exhaustive search over a limited translation range. For each candidate dx and dy, the code:

- shifts the target channel with np.roll
- ignores the border affected by wrap-around
- computes the L2 or NCC score against the reference channel
- keeps the best offset found so far

The function returns the aligned channel together with the best dx, dy, and score.

### 6. Pyramid alignment

align_pyramid is used when the displacement is larger or the image resolution is higher. It follows a coarse-to-fine strategy:

- downsample the channels to a lower resolution
- estimate a rough offset at the coarse level
- propagate that offset to the next level as an initial guess
- repeat the process while gradually increasing resolution

This makes the search more robust than a single full-resolution scan.

### 7. Merge into a color image

After alignment, the red, green, and blue channels are stacked back into an RGB image, displayed with matplotlib, and saved to test_results/.

## How to Configure and Run main

### 1. Activate the Python environment

If you already have a conda environment named cv, activate it first:

```bash
conda activate cv
```

### 2. Check dependencies

Make sure the environment includes the following packages:

- numpy
- opencv-python or opencv
- matplotlib
- jupyter

### 3. Open the notebook

Open code/main.ipynb in VS Code and select the Python kernel from the environment above.

### 4. Verify the working directory

The notebook uses relative paths such as test_images and test_results, so it is best to open the notebook from the project root or ensure that the current working directory is the project root.

If you run the notebook from code/ as the working directory and the images are not found, adjust the paths to point to the parent directory.

### 5. Choose an input image

Change the IDX value in the notebook to select a different image. The notebook reads the selected image and saves the final result under test_results/.

### 6. Run the cells in order

Recommended execution order:

1. Load the image

2. Split the stacked channels

3. Inspect the cropped b, g, r channels

4. Run single-scale alignment and compare L2 and NCC

5. Run pyramid alignment

6. Save the final output

## Output

The final colorized image is saved in test_results/. The output filename usually preserves the original input name with a jpg suffix.

## Notes

- code/colorize_skel.py contains a compact single-scale aligner that can be used as a reference.
- code/main.ipynb is the primary entry point and is recommended for running the project because it shows each intermediate result visually.

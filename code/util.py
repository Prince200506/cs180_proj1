import numpy as np
import cv2
import matplotlib.pyplot as plt


class ImageProcessor:
    """Utility class for image channel split, alignment, and colorization."""

    def __init__(self):
        pass

    @staticmethod
    def split_channels(image):
        """
        Splits an image into its individual color channels.

        Parameters:
            image (numpy.ndarray): The input image to be split.

        Returns:
            tuple: A tuple containing the individual color channels.
        """
        if len(image.shape) == 3 and image.shape[2] == 3:
            return image[:, :, 0], image[:, :, 1], image[:, :, 2]
        raise ValueError("Input image must be a 3-channel RGB image.")

    @staticmethod
    def score_l2(img1, img2):
        """
        Computes the L2 score (Euclidean distance) between two images.

        Parameters:
            img1 (numpy.ndarray): The first input image.
            img2 (numpy.ndarray): The second input image.

        Returns:
            float: The L2 score between the two images.
        """
        img1 = img1.astype(np.float32)
        img2 = img2.astype(np.float32)

        if img1.shape != img2.shape:
            raise ValueError("Input images must have the same dimensions.")

        return np.sqrt(np.sum((img1 - img2) ** 2))

    @staticmethod
    def score_ncc(img1, img2):
        """
        Computes the Normalized Cross-Correlation (NCC) score between two images.

        Parameters:
            img1 (numpy.ndarray): The first input image.
            img2 (numpy.ndarray): The second input image.

        Returns:
            float: The NCC score between the two images.
        """
        img1 = img1.astype(np.float32)
        img2 = img2.astype(np.float32)

        if img1.shape != img2.shape:
            raise ValueError("Input images must have the same dimensions.")

        img1_mean = np.mean(img1)
        img2_mean = np.mean(img2)
        denom1 = np.linalg.norm(img1 - img1_mean)
        denom2 = np.linalg.norm(img2 - img2_mean)
        if denom1 < 1e-8 or denom2 < 1e-8:
            return 0.0

        img1_normalized = (img1 - img1_mean) / denom1
        img2_normalized = (img2 - img2_mean) / denom2

        return np.sum(img1_normalized * img2_normalized)

    @staticmethod
    def align_single_scale(target, reference, search_range=15, select="ncc"):
        """
        Aligns the target image to the reference image using a single scale approach.

        Parameters:
            target (numpy.ndarray): The target image to be aligned.
            reference (numpy.ndarray): The reference image for alignment.
            search_range (int): The range of pixels to search for alignment.
            select (str): The metric to use for alignment ("ncc" or "l2").

        Returns:
            tuple: (aligned_target, dx, dy, score)
        """
        border = search_range

        if select not in ["ncc", "l2"]:
            raise ValueError("Invalid selection for alignment metric. Choose 'ncc' or 'l2'.")

        best_dx_ncc, best_dy_ncc = 0, 0
        best_dx_l2, best_dy_l2 = 0, 0

        if select == "ncc":
            best_score_ncc = float('-inf')
            for i_x in range(-search_range, search_range + 1):
                for i_y in range(-search_range, search_range + 1):
                    shifted_target = np.roll(target, shift=(i_y, i_x), axis=(0, 1))
                    score = ImageProcessor.score_ncc(
                        shifted_target[border:-border, border:-border],
                        reference[border:-border, border:-border]
                    )
                    if score > best_score_ncc:
                        best_score_ncc = score
                        best_dx_ncc, best_dy_ncc = i_x, i_y
            aligned_ncc = np.roll(target, shift=(best_dy_ncc, best_dx_ncc), axis=(0, 1))
            return aligned_ncc, best_dx_ncc, best_dy_ncc, best_score_ncc

        best_score_l2 = float('inf')
        for i_x in range(-search_range, search_range + 1):
            for i_y in range(-search_range, search_range + 1):
                shifted_target = np.roll(target, shift=(i_y, i_x), axis=(0, 1))
                score = ImageProcessor.score_l2(
                    shifted_target[border:-border, border:-border],
                    reference[border:-border, border:-border]
                )
                if score < best_score_l2:
                    best_score_l2 = score
                    best_dx_l2, best_dy_l2 = i_x, i_y

        aligned_l2 = np.roll(target, shift=(best_dy_l2, best_dx_l2), axis=(0, 1))
        return aligned_l2, best_dx_l2, best_dy_l2, best_score_l2

    @staticmethod
    def align_pyramid(target, reference):
        """
        Aligns the target image to the reference image using a multi-scale pyramid approach.

        Parameters:
            target (numpy.ndarray): The target image to be aligned.
            reference (numpy.ndarray): The reference image for alignment.
        """
        raise NotImplementedError("align_pyramid is not implemented yet.")

    @staticmethod
    def colorize(image):
        """
        Colorizes a grayscale image.

        Parameters:
            image (numpy.ndarray): The input grayscale image to be colorized.

        Returns:
            numpy.ndarray: The colorized image.
        """
        raise NotImplementedError("colorize is not implemented yet.")


split_channels = ImageProcessor.split_channels
score_l2 = ImageProcessor.score_l2
score_ncc = ImageProcessor.score_ncc
align_single_scale = ImageProcessor.align_single_scale
align_pyramid = ImageProcessor.align_pyramid
colorize = ImageProcessor.colorize

__all__ = [
    "ImageProcessor",
    "split_channels",
    "score_l2",
    "score_ncc",
    "align_single_scale",
    "align_pyramid",
    "colorize",
]

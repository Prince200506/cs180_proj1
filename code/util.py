import cv2
import numpy as np


class SingleScaleAligner:
    def __init__(self, search_range=15, metric="ncc"):
        """
        Single-scale image aligner.

        Parameters
        ----------
        search_range : int
            Search offsets in [-search_range, search_range].
        metric : str
            Matching metric: "ncc" or "l2".
        """
        if metric not in ["ncc", "l2"]:
            raise ValueError("metric must be either 'ncc' or 'l2'.")

        self.search_range = search_range
        self.metric = metric

    @staticmethod
    def score_l2(img1, img2):
        """
        Compute L2 distance between two images.
        Smaller is better.
        """
        img1 = img1.astype(np.float32)
        img2 = img2.astype(np.float32)

        if img1.shape != img2.shape:
            raise ValueError("Input images must have the same shape.")

        return np.sqrt(np.sum((img1 - img2) ** 2))

    @staticmethod
    def score_ncc(img1, img2):
        """
        Compute normalized cross-correlation.
        Larger is better.
        """
        img1 = img1.astype(np.float32)
        img2 = img2.astype(np.float32)

        if img1.shape != img2.shape:
            raise ValueError("Input images must have the same shape.")

        img1_mean = np.mean(img1)
        img2_mean = np.mean(img2)
        denom1 = np.linalg.norm(img1 - img1_mean)
        denom2 = np.linalg.norm(img2 - img2_mean)

        if denom1 < 1e-8 or denom2 < 1e-8:
            return 0.0

        img1_normalized = (img1 - img1_mean) / denom1
        img2_normalized = (img2 - img2_mean) / denom2

        return np.sum(img1_normalized * img2_normalized)

    def _score(self, img1, img2):
        if self.metric == "ncc":
            return self.score_ncc(img1, img2)
        return self.score_l2(img1, img2)

    def align(self, target, reference, offset=(0, 0)):
        """
        Align target image to reference image using the selected metric.

        Parameters
        ----------
        target : np.ndarray
            Image to move, such as G or R.
        reference : np.ndarray
            Fixed reference image, usually B.
        offset : tuple[int, int]
            Existing (x, y) offset. This is mainly used by PyramidAligner.

        Returns
        -------
        aligned : np.ndarray
            Target shifted by the best displacement found at this scale.
        dx : int
            Best horizontal displacement at this scale.
        dy : int
            Best vertical displacement at this scale.
        score : float
            Best matching score.
        """
        if target.shape != reference.shape:
            raise ValueError("Target and reference must have the same shape.")

        border = self.search_range
        offset_x, offset_y = offset[0], offset[1]

        if (
            target.shape[0] <= 2 * border
            or target.shape[1] <= 2 * border
        ):
            raise ValueError("Image is too small for the selected search range.")

        if self.metric == "ncc":
            best_score = float("-inf")
        else:
            best_score = float("inf")

        best_dx = 0
        best_dy = 0

        # Keep the loop order and shift convention from the original notebook.
        for i_x in range(-self.search_range, self.search_range + 1):
            for i_y in range(-self.search_range, self.search_range + 1):
                shifted_target = np.roll(
                    target,
                    shift=(i_y + offset_y, i_x + offset_x),
                    axis=(0, 1),
                )

                score = self._score(
                    shifted_target[border:-border, border:-border],
                    reference[border:-border, border:-border],
                )

                if self.metric == "ncc":
                    is_better = score > best_score
                else:
                    is_better = score < best_score

                if is_better:
                    best_score = score
                    best_dx = i_x
                    best_dy = i_y

        # This intentionally applies only the displacement found at this scale,
        # matching align_single_scale() in the original notebook. PyramidAligner
        # accumulates the existing offset separately.
        aligned = np.roll(
            target,
            shift=(best_dy, best_dx),
            axis=(0, 1),
        )

        return aligned, best_dx, best_dy, best_score


class PyramidAligner:
    def __init__(self, div=16, metric="ncc"):
        """
        Multi-scale pyramid image aligner.

        Parameters
        ----------
        div : int
            Initial scale factor for the pyramid.
        metric : str
            Matching metric used at each pyramid level.
            The original notebook uses "ncc".
        """
        if div < 1:
            raise ValueError("div must be >= 1.")
        if metric not in ["ncc", "l2"]:
            raise ValueError("metric must be either 'ncc' or 'l2'.")

        self.div = div
        self.metric = metric

        # Final values are stored after align() for easy inspection.
        self.offset_x_red = 0
        self.offset_y_red = 0
        self.offset_x_green = 0
        self.offset_y_green = 0
        self.center_r = [0, 0]
        self.center_g = [0, 0]

    @staticmethod
    def resize(image, scale=2):
        """Resize an image using the same logic as the original notebook."""
        return cv2.resize(
            image,
            (image.shape[1] // scale, image.shape[0] // scale),
            interpolation=cv2.INTER_AREA,
        )

    def align(self, b, g, r):
        """
        Align green and red channels to the blue channel with an image pyramid.

        Parameters
        ----------
        b, g, r : np.ndarray
            Cropped blue, green, and red channel images.

        Returns
        -------
        offset_x_red, offset_y_red, offset_x_green, offset_y_green : int
            Final accumulated offsets, in the same order as align_pyramid()
            in the original notebook.
        """
        div = self.div

        offset_x_red = 0
        offset_y_red = 0
        offset_x_green = 0
        offset_y_green = 0

        center_r = [0, 0]
        center_g = [0, 0]

        while div >= 1:
            # Resize the images.
            b_resized = self.resize(b, scale=div)
            g_resized = self.resize(g, scale=div)
            r_resized = self.resize(r, scale=div)

            # Update offsets for the next finer scale.
            offset_x_red *= 2
            offset_y_red *= 2
            offset_x_green *= 2
            offset_y_green *= 2

            aligner = SingleScaleAligner(
                search_range=max(div, 8),
                metric=self.metric,
            )

            # Align Green to Blue.
            _, dx_g, dy_g, score_g = aligner.align(
                g_resized,
                b_resized,
                offset=(offset_x_green, offset_y_green),
            )
            print(
                f"\033[92mGreen\033[0m channel aligned to Blue channel "
                f"with {self.metric.upper()} score: dx={dx_g}, dy={dy_g}, "
                f"scale={div}, score={score_g}"
            )
            center_g[0] += dx_g * div
            center_g[1] += dy_g * div

            # Align Red to Blue.
            _, dx_r, dy_r, score_r = aligner.align(
                r_resized,
                b_resized,
                offset=(offset_x_red, offset_y_red),
            )
            print(
                f"\033[91mRed\033[0m channel aligned to Blue channel "
                f"with {self.metric.upper()} score: dx={dx_r}, dy={dy_r}, "
                f"scale={div}, score={score_r}"
            )
            center_r[0] += dx_r * div
            center_r[1] += dy_r * div

            # Accumulate the displacement found at the current scale.
            offset_x_red += dx_r
            offset_y_red += dy_r
            offset_x_green += dx_g
            offset_y_green += dy_g

            div //= 2

        self.offset_x_red = offset_x_red
        self.offset_y_red = offset_y_red
        self.offset_x_green = offset_x_green
        self.offset_y_green = offset_y_green
        self.center_r = center_r
        self.center_g = center_g

        print(f"center of red: {center_r}, center of green: {center_g}")

        return (
            offset_x_red,
            offset_y_red,
            offset_x_green,
            offset_y_green,
        )


def colorize(aligned_red, aligned_green, b_cropped):
    """Stack R, G, B channels into the final color image."""
    return np.dstack([
        aligned_red,
        aligned_green,
        b_cropped,
    ])


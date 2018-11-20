"""
--Naim Sen--
--Toby Ticehurst--

windowed_laplacian.py

Testing a windowing technique to produce a focus-depth map
"""

import cv2
import numpy as np

def compute_blur(img_segment):
    """
    Function to compute the blur value of an array.
    """
    return cv2.Laplacian(img_segment, cv2.CV_64F).var()

def blockshaped(arr, nrows, ncols):
    """
    Return an array of shape (n, nrows, ncols) where
    n * nrows * ncols = arr.size

    If arr is a 2D array, the returned array should look like n subblocks with
    each subblock preserving the "physical" layout of arr.
    """
    h, w = arr.shape
    return (arr.reshape(h//nrows, nrows, -1, ncols)
               .swapaxes(1,2)
               .reshape(-1, nrows, ncols))
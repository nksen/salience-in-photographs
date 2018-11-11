"""
--Naim Sen--
--Toby Ticehurst--
Oct 18

Functions for preprocessing of images. 
"""

import cv2
import sys
import matplotlib.pyplot as plt

def generate_saliency_map(image, threshold_floor=None, to_display=False):
    """
    Calculates the spectral saliency of the input image

    Args:
        image: loaded using scikit-image/opencv
        threshold_floor: optional minimum value of saliency.
                         Any areas below this threshold will be set to 0 saliency
        to_display: optional flag. When enabled, rescales saliency values so they
                    can be displayed (max of 255)
    Returns:
        Spectral saliency of the input image as a numpy matrix

    Raises:
    """
    # initialise saliency detector object
    saliency_detector = cv2.saliency.StaticSaliencySpectralResidual_create()
    # compute saliency map
    __, saliency_map = saliency_detector.computeSaliency(image)

    # check if rescaling is wanted
    if to_display:
        saliency_map = (saliency_map * 255).astype("uint8")
        if threshold_floor is not None:
            threshold_floor = threshold_floor * 255
        threshold_ceiling = 255
    else:
        threshold_ceiling = 1
    # check if thresholding is wanted
    if threshold_floor is not None:
        saliency_map = cv2.threshold(saliency_map, threshold_floor, threshold_ceiling,
                                 cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    return saliency_map
        

if __name__ == "__main__":

    """
    Just for testing these functions. This should be
    removed before distribution.
    """

    image = cv2.imread('/home/naim/Repos/mphys-testing/salience-in-photographs/images/birds.jpg')

    s_map = generate_saliency_map(image, threshold_floor=0.2, to_display=True)
    cv2.imshow("smap", s_map)
    cv2.waitKey()

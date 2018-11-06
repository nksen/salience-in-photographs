"""
--Naim Sen--
--Toby Ticehurst--
Oct 18

factory.py

Class to generate boxes of a standard type.
Also generates directions lists.
"""

from bounding_box import *
import numpy as np


class BoxFactory(object):
    """
    Factory for building specific boxes
    """
    def __init__(self, image):
        # check image is valid
        if np.any(image.shape) is 0:
            raise ValueError("image dims must be non-zero")
        self._image = image

    # ~~ Properties ~~ #

    # ~~ Methods ~~ #
    def unconstrained(self, box_tl, dims):
        """
        Generates an unconstrained box 
        """
        

"""
--Naim Sen--
--Toby Ticehurst--

text.py 

Contains text class
"""

import cv2
from pathlib import Path
from pathlib import PurePath
import numpy as np

import utilities

class Text(object):
    """
    Text class. Handles all operations with text.

    """
    def __init__(self, in_text, font_path, size_pt, color=(0,0,0)):
        """
        Init function
        """
        # assign variables
        self._raw_text = in_text
        self._font_path = font_path
        self._font_size = size_pt

        # check font path has valid extension
        ext = font_path.suffix
        if not ext == ".pil" \
        and not ext == ".otf" \
        and not ext == ".ttf":
            raise ValueError("font filetype must be .pil .ttf or . otf")
    
    def __str__(self):
        return self._raw_text

    # ~~ properties ~~ #
    
    # ~~ methods ~~ #
    def draw(self, img_path, box_shape):
        """
        Draws text on the image provided given a constraining box shape
        """

if __name__ == "__main__":
    raw = "This is a sentence that is going to be long This is a sentence that is going to be long This is a sentence that is going to be long This is a sentence that is going to be long."
    fontpath = PurePath("/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf")
    trialtext = Text(raw, fontpath, 40)
    print(trialtext)

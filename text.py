"""
--Naim Sen--
--Toby Ticehurst--

Dec 18

text.py 

Contains text class

Copyright © 2018, Naim Sen
Licensed under the terms of the GNU General Public License
<https://www.gnu.org/licenses/gpl-3.0.en.html>
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
    def __init__(self, in_text, font_path,
                size_pt,
                alignment='left',
                colour=(0,0,0),
                bg_colour=(0,0,0,0)):
        """
        Init function
        """
        # assign variables
        self._raw_text = in_text
        self._font_path = font_path
        self._font_size = size_pt
        self._colour = colour
        self._bg_colour = bg_colour
        self._alignment = alignment

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
    def draw(self, img_path, box_tl, box_shape):
        """
        Draws text on the image provided given a constraining box shape
        
        NOTE: Pass bg_colour to ImageText so that text can have a darker
              background if desired. Default should be transparent. If handled
              by the draw method instead of ImageText it should be done before
              drawing of the text. 
        """
        # Construct ImageText object

        img = utilities.ImageText(img_path)
        img.write_text_box(box_tl, self._raw_text, box_shape[1],
                            font_filename=str(self._font_path),
                            font_size=self._font_size,
                            color=self._colour,
                            place=self._alignment
                            )
        return img


if __name__ == "__main__":
    
    raw = "This is a sentence that is going to be long This is a sentence that is going to be long This is a sentence that is going to be long This is a sentence that is going to be long."
    fontpath = PurePath("LiberationSerif-Bold.ttf")
    trialtext = Text(raw, fontpath, 40)
    img = trialtext.draw("../mphys-testing/salience-in-photographs/images/birds.jpg", (0,0), (100,100))
    img.image.show()
"""
--Naim Sen--
--Toby Ticehurst--

text.py 

Contains text class
"""

import cv2
from pathlib import Path
from pathlib import PurePath
from PIL import ImageFont, ImageDraw
import numpy as np

import utilities

class Text(object):
    """
    Text class. Handles all operations with text.

    """
    def __init__(self, in_text, font_path, size_pt):
        """
        Init function
        """
        # assign variables
        self._raw_text = in_text
        self._font_path = font_path
        self._font_size = size_pt

        # load font
        # get font type
        ext = font_path.suffix
        if ext == ".pil":
            self._font_obj = ImageFont.load(font_path)
        elif ext == ".ttf" or ext == ".otf":
            self._font_obj = ImageFont.truetype(str(font_path), size=size_pt)
        else:
            raise ValueError("font filetype must be .pil .ttf or . otf")
    
    # properties
    @property
    def raw_text(self):
        return self._raw_text
    
    @property
    def font_obj(self):
        return self._font_obj


if __name__ == "__main__":
    raw = "This is a sentence that is going to be long This is a sentence that is going to be long This is a sentence that is going to be long This is a sentence that is going to be long."
    fontpath = PurePath("/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf")
    trialtext = Text(raw, fontpath, 40)

    trialtext.break_text(400)
    #print(trialtext._wrapped_text)
    txt = ImageDraw.Image.new('RGBA', (500,500), (255,255,255,0))
    d = ImageDraw.Draw(txt)
    for i, line in enumerate(trialtext.break_text(500)):
        d.text((0, 16*i), line, (255,255,255), font=trialtext.font_obj)
    #d.text((10, 25), raw, font=trialtext.font_obj)
    txt.show()
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

    def break_text(self, max_width):

        # We share the subset to remember the last finest guess over 
        # the text breakpoint and make it faster
        print("aaaaaaaaaaaaa")
        self._wrapped_text = self._raw_text
        subset = len(self._wrapped_text)
        letter_size = None

        text_size = len(self._wrapped_text)
        while text_size > 0:

            # Let's find the appropriate subset size
            while True:
                width, height = self._font_obj.getsize(self._wrapped_text[:subset])
                letter_size = width / subset

                # min/max(..., subset +/- 1) are to avoid looping infinitely over a wrong value
                if width < max_width - letter_size and text_size >= subset: # Too short
                    subset = max(int(max_width * subset / width), subset + 1)
                elif width > max_width: # Too large
                    subset = min(int(max_width * subset / width), subset - 1)
                else: # Subset fits, we exit
                    break

            yield self._wrapped_text[:subset]
            self._wrapped_text = self._wrapped_text[subset:]   
            text_size = len(self._wrapped_text)
    
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
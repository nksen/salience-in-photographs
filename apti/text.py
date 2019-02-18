"""
--Naim Sen--
--Toby Ticehurst--

text.py

Contains text class
"""

from pathlib import PurePath
import numpy as np
import cv2

from bounding_box import Box
import preprocessing
import utilities

class Text(object):
    """
    Text class. Handles all operations with text.

    """
    def __init__(self, in_text, font_path,
                 size_pt,
                 alignment='left',
                 colour=(0, 0, 0),
                 bg_colour=(0, 0, 0, 0)):
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
    def draw(self, text_box, raw_img_path):
        """
        Draws text on the image provided given a constraining box shape
        # TODO: Just pass Box class instead and grab all the things we need from it.
        TODO: Pass bg_colour to ImageText so that text can have a darker
              background if desired. Default should be transparent. If handled
              by the draw method instead of ImageText it should be done before
              drawing of the text.
        """
        # grab useful bits from the box
        box_tl = text_box.box_tl
        box_shape = text_box.shape

        # Construct ImageText object
        img = utilities.ImageText(raw_img_path)
        img.write_text_box(box_tl, self._raw_text, box_shape[1],
                           font_filename=str(self._font_path),
                           font_size=self._font_size,
                           color=self._colour,
                           place=self._alignment
                           )
        return img


def main():
    """
    main for testing
    """
    # load image
    raw_img = cv2.imread(r'D:\Users\Naim\OneDrive\CloudDocs\UNIVERSITY\S7\MPhys\test_images\delpotro.jpg')
    s_map = preprocessing.generate_saliency_map(raw_img)
    text_box = Box(s_map, np.array([0, 0]), np.array([100, 100]))
    print(text_box)

    raw = "This is a sentence that is going to be long This is a sentence that is going to be long This is a sentence and that is going to be long This is a sentence that is going to be long."
    fontpath = PurePath(r'../assets/BBCReithSans_Bd.ttf')
    trialtext = Text(raw, fontpath, 40)
    img = trialtext.draw(text_box, r'D:\Users\Naim\OneDrive\CloudDocs\UNIVERSITY\S7\MPhys\test_images\delpotro.jpg')
    img.image.show()


if __name__ == "__main__":
    main()
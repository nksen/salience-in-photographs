"""
--Naim Sen--
--Toby Ticehurst--

text.py

Contains text class
"""

from pathlib import PurePath
import copy
import time

import numpy as np
import cv2
from PIL import Image ImageDraw

from bounding_box import Box
import preprocessing
import utilities


class Text(object):
    """
    Text class. Handles all operations with text.

    """

    def __init__(self,
                 in_text,
                 font_path,
                 size_pt,
                 alignment='left',
                 colour=(255, 255, 255),
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
    def draw(self, text_box, raw_img):
        """
        Draws text on the image provided given a constraining box shape
        TODO: Pass bg_colour to ImageText so that text can have a darker
              background if desired. Default should be transparent. If handled
              by the draw method instead of ImageText it should be done before
              drawing of the text.
        """
        # grab useful bits from the box
        box_tl = text_box.box_tl
        box_br = text_box.box_br
        box_shape = text_box.shape
        # account for padding
        padding_size = utilities.estimate_stroke_width(raw_img.size)

        # determine box's proximity to edges
        # create modifiable text dimensions

        text_tl = copy.copy(box_tl)
        text_br = copy.copy(box_br)

        if box_tl[0] < padding_size:
            text_tl[0] = padding_size
        if box_tl[1] < padding_size:
            text_tl[1] = padding_size
        if box_br[0] > raw_img.size[0] - padding_size:
            text_br[0] = raw_img.size[0] - padding_size - box_shape[0]
        if box_br[1] > raw_img.size[1] - padding_size:
            text_br[1] = raw_img.size[1] - padding_size - box_shape[1]

        # Construct ImageText context
        text_writer = utilities.ImageText(raw_img)

        # Write text to duplicate image to get text dimensions
        # for scrim.
        # Make duplicate ImageText context
        dupe_raw_img = copy.copy(raw_img)
        dupe_text_writer = utilities.ImageText(dupe_raw_img)

        # write_text_box dims must conform with PIL.ImageText (xy not ij) convention
        text_dims = dupe_text_writer.write_text_box(
            (text_tl[1], text_tl[0]),
            self._raw_text,
            box_shape[1],
            font_filename=str(self._font_path),
            font_size=self._font_size,
            color=self._colour,
            place=self._alignment)
        # add padding
        scrim_dims = (text_dims[0] + padding_size, text_dims[1] + padding_size)
        scrim_tl = text_box.box_tl
        scrim_br = (scrim_tl[0] + scrim_dims[0], scrim_tl[1] + scrim_dims[1])
        scrim_draw_context = PIL.ImageDraw.draw(raw_img)

        # Add scrim
        #scrim_draw_context = PIL.ImageDraw.draw(raw_img)
        #scrim_draw_context.draw.rectangle()

        # write_text_box dims must conform with PIL.ImageText (xy not ij) convention
        text_writer.write_text_box((text_tl[1], text_tl[0]),
                                   self._raw_text,
                                   box_shape[1],
                                   font_filename=str(self._font_path),
                                   font_size=self._font_size,
                                   color=self._colour,
                                   place=self._alignment)


def main():
    """
    main for testing
    """
    # load image
    raw_img = cv2.imread(
        r'D:\Users\Naim\OneDrive\CloudDocs\UNIVERSITY\S7\MPhys\test_images\flintoff football getty.jpg'
    )
    pil_img = Image.open(
        r'D:\Users\Naim\OneDrive\CloudDocs\UNIVERSITY\S7\MPhys\test_images\flintoff football getty.jpg'
    )
    s_map = preprocessing.generate_saliency_map(raw_img)

    text_box = Box(s_map, np.array([500, 0]), np.array([500, 800]))
    #text_box = Box(s_map, np.array([raw_img.shape[0] - 501, 0]), np.array([500, 800]))
    drawn_box = Box(s_map, np.array([500, 0]), np.array([1150, 800]))

    raw = r'thre folders all the folders in alpha space missing .'
    fontpath = PurePath(r'../assets/BBCReithSans_Bd.ttf')
    text_context = Text(raw, fontpath, 90)
    text_context.draw(text_box, pil_img)
    pil_out = drawn_box.overlay_box(pil_img)
    """
    cv_out = text_box.overlay_box(raw_img)
    cv2.namedWindow("cv2", cv2.WINDOW_NORMAL)        # Create a named window
    cv2.moveWindow("cv2", 40, 30)  # Move it to (40,30)
    cv2.imshow("cv2", cv_out)
    """

    pil_out.show()

    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

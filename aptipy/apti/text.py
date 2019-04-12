"""
--Naim Sen--
--Toby Ticehurst--

text.py

Contains text class

Copyright © 2018, Naim Sen
Licensed under the terms of the GNU General Public License
<https://www.gnu.org/licenses/gpl-3.0.en.html>
"""

from pathlib import PurePath
from math import sqrt
import copy
import time

import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

from .bounding_box import Box, minimise_cost
from ..apti import directions_factory, preprocessing, utilities

# TODO: Procedural colour if necessary?
BBC_YELLOW = (255, 210, 47)
BBC_GREY = (50, 50, 50)


# draw transparent box on PIL image
def composite_draw(xy, RGBA, raw_img):
    """
    Draws RGBA rectangle given corner coordinates xy
    """
    img = raw_img.convert("RGBA")

    # Make a blank image for the rectangle, initialized to a completely
    # transparent color.
    tmp = Image.new('RGBA', img.size, (0, 0, 0, 0))

    # Create a draw context.
    draw = ImageDraw.Draw(tmp)
    draw.rectangle(xy, fill=RGBA)

    # Alpha composite the two images together.
    img = Image.alpha_composite(img, tmp)
    return img


class Text(object):
    """
    Text class. Handles all operations with text.

    """

    def __init__(self,
                 in_text,
                 font_path,
                 size_pt=24,
                 alignment='left',
                 colour=BBC_YELLOW,
                 bg_colour=BBC_GREY):
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

    def rescale_font_size(self,
                          original_image_dims,
                          target_image_size=5,
                          target_dpi=114):
        """
        MODIFIES OBJECT
        Scales the font size from target size to the size required for
        the high-res original: font size must be increased in order to
        be drawn at the correct size for the small image size.
        Args:
            original_image_dims: image dims in pixels (i,j) OR (x,y) agnostic
            target_image_size: tuple (dimensions in inches) or int (diagonal in inches).
            target_dpi: desired resolution in DPI (px/inch).
        returns:
        raises:
        """
        original_diagonal = sqrt(
            pow(original_image_dims[0], 2) + pow(original_image_dims[1], 2))
        # Image size can be passed as a single measurement of the diagonal...
        if isinstance(target_image_size, int):
            # original divide target: scaling factor
            scale_factor = original_diagonal / target_image_size
        # ...or passed as a tuple dimensions (shape) pair
        elif isinstance(target_image_size, tuple):
            target_diagonal = sqrt(
                pow(target_image_size[0], 2) + pow(target_image_size[1], 2))
            scale_factor = original_diagonal / target_diagonal

        scaled_size_pt = int((scale_factor / target_dpi) * self._font_size)
        # assign new, scaled font size and keep copy of original
        self._desired_font_size = self._font_size
        self._font_size = scaled_size_pt

    def get_text_size(self, text):
        """
        Passthrough function for PIL.ImageFont.getsize()
        """
        font = ImageFont.truetype(str(self._font_path), self._font_size)
        return font.getsize(text)

    def get_constraints(self, headline=None):
        """
        Gets minimum box height, width, and area from string
        """
        if headline is None:
            headline = self._raw_text
        # get height and width limits
        longest_word = ''
        lword_x = 0
        # loop over headline and measure each word
        for word in headline.split():
            word_x, word_y = self.get_text_size(word)
            if word_x > lword_x:
                # save longest word and it's width
                longest_word = word
                lword_x = word_x
        min_width = lword_x
        # get area
        line_width, line_height = self.get_text_size(headline)

        area = line_width * line_height
        minimum_size = np.array([line_height, min_width])

        return minimum_size, area

    def draw(self, raw_img, box_tl, box_br, box_shape):
        """
        Draws text on the image provided given a constraining box shape
        """
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

        # Write text to duplicate image to get text dimensions
        # for scrim.
        # Make duplicate ImageText context
        dupe_raw_img = copy.copy(raw_img)
        dupe_text_writer = utilities.ImageText(dupe_raw_img)

        # write_text_box dims must conform with PIL.ImageText (xy not ij) convention
        text_xy = dupe_text_writer.write_text_box(
            (text_tl[1], text_tl[0]),
            self._raw_text,
            box_shape[1],
            font_filename=str(self._font_path),
            font_size=self._font_size,
            color=self._colour,
            place=self._alignment)
        # add padding
        scrim_tl = (text_tl[1] - padding_size, text_tl[0])
        scrim_br = (text_tl[1] + text_xy[0] + padding_size,
                    text_tl[0] + text_xy[1] + padding_size)
        # check if scrim exceeds image dimensions
        if scrim_br[0] > raw_img.size[0] or scrim_br[1] > raw_img.size[1]:
            print("WARN: Text drawn out of bounds.")
        # draw scrim
        out_img = composite_draw((scrim_tl, scrim_br),
                                 self._bg_colour + (127, ), raw_img)

        # Construct ImageText context
        text_writer = utilities.ImageText(out_img)

        # write_text_box dims must conform with PIL.ImageText (xy not ij) convention
        text_writer.write_text_box((text_tl[1], text_tl[0]),
                                   self._raw_text,
                                   box_shape[1],
                                   font_filename=str(self._font_path),
                                   font_size=self._font_size,
                                   color=self._colour,
                                   place=self._alignment)
        return out_img


def main():
    """
    main for testing
    """
    # load image
    raw_img = cv2.imread(
        r'D:\Users\Naim\OneDrive\CloudDocs\UNIVERSITY\S7\MPhys\test_images\klopp getty.jpg'
    )
    pil_img = Image.open(
        r'D:\Users\Naim\OneDrive\CloudDocs\UNIVERSITY\S7\MPhys\test_images\klopp getty.jpg'
    )
    s_map = preprocessing.generate_saliency_map(raw_img)

    init_box = Box(s_map, np.array([0, 0]), np.array([700, 300]))
    text_box = Box(s_map, np.array([raw_img.shape[0] - 501, 0]),
                   np.array([500, 800]))
    #drawn_box = Box(s_map, np.array([500, 0]), np.array([1150, 800]))
    directions_list = directions_factory.unconstrained()
    #text_box = minimise_cost(init_box, directions_list)

    raw = r"Andy Murray: Former Wimbledon champion is |pain free| after hip injury."
    fontpath = PurePath(r'../assets/BBCReith/BBCReithSans_Bd.ttf')
    text_context = Text(raw, fontpath, size_pt=24)
    text_context.rescale_font_size(pil_img.size)

    #exit()

    pil_out = text_context.draw(pil_img, text_box.box_tl, text_box.box_br,
                                text_box.shape)
    pil_out = init_box.overlay_box(pil_out)
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

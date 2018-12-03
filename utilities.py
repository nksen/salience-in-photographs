"""
--Naim Sen--
--Toby Ticehurst--
Nov 18

utilities.py

Contains useful utilities
"""


class Bunch(object):
    """
    Struct-style data structure utilises built-in
    class dictionary
    """
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


# Copyright 2011 Álvaro Justen [alvarojusten at gmail dot com]
# https://gist.github.com/josephkern/69591e9bc1d2e07a46d35d2a3ab66542/4f7a1a1631e72e184af9ad4d33a79a612e01e605
# https://gist.github.com/turicas/1455973
# License: GPL <http://www.gnu.org/copyleft/gpl.html>

from PIL import Image, ImageDraw, ImageFont
class ImageText(object):
    """
    Class to improve handling text-wrapping.
    """
    def __init__(self, filename_or_size, mode='RGBA', background=(0, 0, 0, 0),
                 encoding='utf8'):
        # check whether filename_or_size is a filename or a size tuple
        if isinstance(filename_or_size, str):
            self.filename = filename_or_size
            self.image = Image.open(self.filename)
            self.size = self.image.size
        elif isinstance(filename_or_size, (list, tuple)):
            self.size = filename_or_size
            self.image = Image.new(mode, self.size, color=background)
            self.filename = None
         else:
            raise TypeError("ImageText __init__() : invalid filename_or_size type. %s" %\
                            type(filename_or_size)) 
        # open PIL image for drawing
        self.draw = ImageDraw.Draw(self.image)
        self.encoding = encoding

    def save(self, filename=None):
        self.image.save(filename or self.filename)

    def get_font_size(self, text, font, max_width=None, max_height=None):
        """
        Returns max font size that fulfil max_width and or max_height
        constraints.
        """
        # check that at least one constraint has been added
        if max_width is None and max_height is None:
            raise ValueError('You need to pass max_width or max_height')
        # initialise font size
        font_size = 1
        text_size = self.get_text_size(font, font_size, text)
        
        # check for constraints that are too small for the text to fit
        if (max_width is not None and text_size[0] > max_width) or \
           (max_height is not None and text_size[1] > max_height):
            raise ValueError("Text can't be filled in only (%dpx, %dpx)" % \
                    text_size)
        # loop until text width/height limit is reached, incrementing font size
        while True:
            # exit condition
            if (max_width is not None and text_size[0] >= max_width) or \
               (max_height is not None and text_size[1] >= max_height):
                return font_size - 1
            # increment font and text size
            font_size += 1
            text_size = self.get_text_size(font, font_size, text)

    def write_text(self, xy, text, font_filename, font_size=11,
                   color=(0, 0, 0), max_width=None, max_height=None):
        """
        Writes 'text' to location '(x,y)' with font 'font_filename'.
        Respects max_width & max_height constraints.
        font_size can be set to 'fill' to invoke the "get_font_size() method"
        for auto-fitting the text.
        """
        # unpack tuple
        x, y = xy
        # if we want to auto-fit the text
        if font_size == 'fill' and \
           (max_width is not None or max_height is not None):
            font_size = self.get_font_size(text, font_filename, max_width,
                                           max_height)
        
        # otherwise get the text size the usual way
        text_size = self.get_text_size(font_filename, font_size, text)
        font = ImageFont.truetype(font_filename, font_size)
        
        # (x,y)='center' keyword
        if x == 'center':
            x = (self.size[0] - text_size[0]) / 2
        if y == 'center':
            y = (self.size[1] - text_size[1]) / 2
        
        self.draw.text((x, y), text, font=font, fill=color)
        return text_size

    def get_text_size(self, font_filename, font_size, text):
        """
        Passthrough function for PIL.ImageFont.getsize()
        """

        font = ImageFont.truetype(font_filename, font_size)
        return font.getsize(text)

    def write_text_box(self, xy, text, box_width, font_filename,
                       font_size=11, color=(0, 0, 0), place='left',
                       justify_last_line=False):
        # unpack position tuple
        x, y = xy
        lines = []                          # list of wrapped lines
        line = []                           # list of words in current line
        words = text.split()                # list of all words 
        
        for word in words:
            new_line = ' '.join(line + [word])
            # get size of the proposed line
            size = self.get_text_size(font_filename, font_size, new_line)
            text_height = size[1]
            # check that line doesn't exceed box_width
            if size[0] <= box_width:
                line.append(word)
            else:
                # if the proposed line is too long, append it to the list of lines
                # set the start of a new line to the current word.
                lines.append(line)
                line = [word]
        # if the current line is not blank
        if line:
            lines.append(line)
        # add spaces to word endings
        lines = [' '.join(line) for line in lines if line]
        height = y
        # loop over lines and write (account for alignment)
        for index, line in enumerate(lines):
            # get height
            height += text_height
            # left aligned
            if place == 'left':
                self.write_text((x, height), line, font_filename, font_size,
                                color)
            # right aligned
            elif place == 'right':
                total_size = self.get_text_size(font_filename, font_size, line)
                x_left = x + box_width - total_size[0]
                self.write_text((x_left, height), line, font_filename,
                                font_size, color)
            # center aligned
            elif place == 'center':
                total_size = self.get_text_size(font_filename, font_size, line)
                x_left = int(x + ((box_width - total_size[0]) / 2))
                self.write_text((x_left, height), line, font_filename,
                                font_size, color)
            # justified
            elif place == 'justify':
                words = line.split()
                if (index == len(lines) - 1 and not justify_last_line) or \
                   len(words) == 1:
                    self.write_text((x, height), line, font_filename, font_size,
                                    color)
                    continue
                line_without_spaces = ''.join(words)
                total_size = self.get_text_size(font_filename, font_size,
                                                line_without_spaces)
                # even spacing between words 
                space_width = (box_width - total_size[0]) / (len(words) - 1.0)
                start_x = x
                for word in words[:-1]:
                    self.write_text((start_x, height), word, font_filename,
                                    font_size, color)
                    word_size = self.get_text_size(font_filename, font_size,
                                                    word)
                    start_x += word_size[0] + space_width
                last_word_size = self.get_text_size(font_filename, font_size,
                                                    words[-1])
                last_word_x = x + box_width - last_word_size[0]
                self.write_text((last_word_x, height), words[-1], font_filename,
                                font_size, color)
        return (box_width, height - y)

"""
--Naim Sen--
Mar 2019

requester.py

Requester class for serving headlines from a given

Copyright © 2018, Naim Sen
Licensed under the terms of the GNU General Public License
<https://www.gnu.org/licenses/gpl-3.0.en.html>
"""
import json
import random
from pathlib import Path, PurePath
import numpy as np
from ..apti.text import Text


class Requester(object):
    """
    Attaches to json to serve up headlines. Keeps track of which
    headlines have been served by a single Requester.
    """

    def __init__(self, filepath='./aptipy/assets/headlines_list.json'):
        """
        ctor
        """
        self._path = Path(filepath)
        # load json file
        with self._path.open() as file:
            self._file_contents = json.load(file)
            # check that all items in the file have expected keys
            # Here it is set up for a list of dicts
            if all('headline' in item and 'date' in item and 'source' in item
                   for item in self._file_contents):
                pass
            else:
                print("WARNING: File contents may be corrupted")
        # get a lits of headlines
        self._headlines = [
            item['headline'] for item in self._file_contents
            if 'headline' in item
        ]
        # list of served indices
        self._served_indices = []

    def get(self, index=None):
        """
        Get headline (leave index none for a random selection)
        """
        # get headline from index
        if index is not None:
            item = self._headlines[index]
            self._served_indices.append(index)
            return item
        # get random headline
        else:
            random.seed()
            # get random headline index
            rand_index = random.randint(0, len(self._headlines) - 1)
            self._served_indices.append(rand_index)
            return (self._headlines[rand_index], rand_index)


def get_constraints(headline, text_context):
    """
    Gets minimum box height and width from string
    """
    # get height and width limits
    longest_word = ''
    lword_x = 0
    # loop over headline and measure each word
    for word in headline.split():
        word_x, word_y = text_context.get_text_size(word)
        if word_x > lword_x:
            # save longest word and it's width
            longest_word = word
            lword_x = word_x
    min_width = lword_x
    # get area
    line_width, line_height = text_context.get_text_size(headline)
    
    area = line_width * line_height
    minimum_size = np.array([line_height, min_width])

    return minimum_size, area


def main():
    headline_server = Requester()
    hl, idx = headline_server.get()
    print(idx, hl)
    # text context needed for getting constraints
    fontpath = Path(r'../salience-in-photographs/aptipy/assets/BBCReith/BBCReithSans_Bd.ttf').resolve()
    text_ctx = Text('raw', fontpath, size_pt=24)
    # get constraints
    vals = get_constraints(hl, text_ctx)
    print(vals)


if __name__ == '__main__':
    main()
    
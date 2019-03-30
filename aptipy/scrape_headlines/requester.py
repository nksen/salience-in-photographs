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
from pathlib import Path


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


def main():
    headline_server = Requester()
    out, idx = headline_server.get()
    print(idx, out)


if __name__ == '__main__':
    main()

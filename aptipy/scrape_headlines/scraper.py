"""
--Naim Sen--
Mar 2019

scraper.py

Scraper class for grabbing headlines from
an associated URL.

Copyright © 2018, Naim Sen
Licensed under the terms of the GNU General Public License
<https://www.gnu.org/licenses/gpl-3.0.en.html>
"""

import re
import json
import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup as bs


class Scraper(object):
    """
    Scraper object attaches to a webpage and scrapes the headlines
    """

    def __init__(self,
                 base_url="https://www.bbc.co.uk/sport/",
                 save_path="./aptipy/assets/headlines_list.json"):
        """
        Construct scraper
        """
        response = requests.get(base_url)
        self._soup = bs(response.text, 'html.parser')
        self._save_path = Path(save_path)
        self._base_url = base_url
        self.output = []

    def grab_headlines(self):
        """
        Gets headlines from base_url by searching for 'h3' with class attrs 
        .+?heading__title.
        """
        # get relevent html elements
        element_list = self._soup.find_all(
            'h3', attrs={'class': re.compile('.+?heading__title')})
        # loop over each headline and construct a list of dicts
        for item in element_list:
            output_element = {}
            output_element['headline'] = str(item.get_text())
            output_element['date'] = datetime.datetime.now().isoformat()
            output_element['source'] = self._base_url
            self.output.append(output_element)

    def save_scrapings(self):
        """
        Add scraped headlines to file (or write new file if file doesn't exist)
        """
        # check if file exists and read
        try:
            with self._save_path.open(mode='r') as file:
                existing_data = json.load(file)
                print(type(existing_data))
                #exit()
                writeout = existing_data + self.output
        except FileNotFoundError:
            writeout = self.output

        # write to file
        with self._save_path.open(mode='w') as file:
            json.dump(writeout, file)


def main():
    bbc_sport_scraper = Scraper()
    bbc_sport_scraper.grab_headlines()
    bbc_sport_scraper.save_scrapings()


if __name__ == "__main__":
    main()
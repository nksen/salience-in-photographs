"""
--Naim Sen--
Mar 2019

scrape_headlines - main.py

main for testing.

Copyright © 2018, Naim Sen
Licensed under the terms of the GNU General Public License
<https://www.gnu.org/licenses/gpl-3.0.en.html>
"""

import os
print(os.getcwd())

import requests
from pathlib import Path
from bs4 import BeautifulSoup as bs

from scraper import Scraper


def main():
    Scraper()


if __name__ == "__main__":
    #main()
    res = requests.get("https://www.bbc.co.uk/sport/")
    soup = bs(res.text, 'html.parser')

    path = Path("./aptipy/assets/scratch.html")

    with open(path, 'a') as file:
        file.write(soup.prettify())

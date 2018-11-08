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

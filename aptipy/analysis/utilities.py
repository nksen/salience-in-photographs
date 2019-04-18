"""
--Naim Sen--

Apr 19

Utility functions for eye tracking analysis

Copyright © 2019, Naim Sen
Licensed under the terms of the GNU General Public License
<https://www.gnu.org/licenses/gpl-3.0.en.html>
"""
import os
import matplotlib.pyplot as plt


def wavg(df, data_name, weight_name):
    """
    Calculates the weighted average of the column named
    data_name using pandas.
    """
    d = df[data_name]
    w = df[weight_name]
    try:
        return (d * w).sum() / w.sum()
    except ZeroDivisionError:
        return d.mean()


def wvar(df, data_name, weight_name):
    """
    Calculates the weighted sample variance of the column named
    data_name
    """
    d = df[data_name]
    w = df[weight_name]
    wmean = wavg(df, data_name, weight_name)
    try:
        return (w * (d - wmean)**2).sum() / w.sum()
    except ZeroDivisionError:
        return d.var()


def load_images(folder):
    """
    Loads all images in folder into a dict
    """
    images = dict()
    for file in os.listdir(folder):
        images[file] = plt.imread(folder + '\\' + file)
    return images

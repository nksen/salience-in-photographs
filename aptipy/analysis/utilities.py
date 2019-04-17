"""
--Naim Sen--

Apr 19

Utility functions for eye tracking analysis

Copyright © 2019, Naim Sen
Licensed under the terms of the GNU General Public License
<https://www.gnu.org/licenses/gpl-3.0.en.html>
"""


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

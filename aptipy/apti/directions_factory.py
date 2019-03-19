"""
--Naim Sen--
--Toby Ticehurst--

Oct 2018

directions_factory.py

Module to generate directions vectors.

Copyright © 2018, Naim Sen
Licensed under the terms of the GNU General Public License
<https://www.gnu.org/licenses/gpl-3.0.en.html>
"""

import numpy as np


def unconstrained():
    directions = np.array(
        [
            [[1, 0], [0, 0]],
            [[0, 1], [0, 0]],
            [[-1, 0], [0, 0]],
            [[0, -1], [0, 0]],
            [[0, 0], [1, 0]],
            [[0, 0], [0, 1]],
            [[0, 0], [-1, 0]],
            [[0, 0], [0, -1]]
        ])
    return directions


def left_anchored():
    directions = np.array(
        [
            [[1, 0], [0, 0]],
            [[-1, 0], [0, 0]],
            [[0, 0], [1, 0]],
            [[0, 0], [0, 1]],
            [[0, 0], [-1, 0]],
            [[0, 0], [0, -1]]
        ])
    return directions


def right_anchored():
    directions = np.array(
        [
            [[1, 0], [0, 0]],
            [[-1, 0], [0, 0]],
            [[0, 0], [1, 0]],
            [[0, -1], [0, 1]],
            [[0, 0], [-1, 0]],
            [[0, 1], [0, -1]]
        ])
    return directions


def top_anchored():
    directions = np.array(
        [
            [[0, 1], [0, 0]],
            [[0, -1], [0, 0]],
            [[0, 0], [1, 0]],
            [[0, 0], [0, 1]],
            [[0, 0], [-1, 0]],
            [[0, 0], [0, -1]]
        ])
    return directions


def bottom_anchored():
    directions = np.array(
        [
            [[0, 1], [0, 0]],
            [[0, -1], [0, 0]],
            [[-1, 0], [1, 0]],
            [[0, 0], [0, 1]],
            [[1, 0], [-1, 0]],
            [[0, 0], [0, -1]]
        ])
    return directions


def topleft_anchored():
    directions = np.array(
        [
            [[0, 0], [1, 0]],
            [[0, 0], [0, 1]],
            [[0, 0], [-1, 0]],
            [[0, 0], [0, -1]]
        ])
    return directions


def topright_anchored():
    directions = np.array(
        [
            [[0, 0], [1, 0]],
            [[0, -1], [0, 1]],
            [[0, 0], [-1, 0]],
            [[0, 1], [0, -1]]
        ])
    return directions


def bottomleft_anchored():
    directions = np.array(
        [
            [[-1, 0], [1, 0]],
            [[0, 0], [0, 1]],
            [[1, 0], [-1, 0]],
            [[0, 0], [0, -1]]
        ])
    return directions


def bottomright_anchored():
    directions = np.array(
        [
            [[-1, 0], [1, 0]],
            [[0, -1], [0, 1]],
            [[1, 0], [-1, 0]],
            [[0, 1], [0, -1]]
        ])
    return directions
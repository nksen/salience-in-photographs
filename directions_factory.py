"""
--Naim Sen--
--Toby Ticehurst--
Oct 18

directions_factory.py

Module to generate directions vectors.
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


def bottomright_anchored():
    directions = np.array(
        [
            [[-1, 0], [1, 0]],
            [[0, -1], [0, 1]],
            [[1, 0], [-1, 0]],
            [[0, 1], [0, -1]]
        ])
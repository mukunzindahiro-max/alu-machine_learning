#!/usr/bin/env python3
"""function to calculate the definiteness of a matrix
    """
import numpy as np


def definiteness(matrix):
    """function to determine the definiteness of a matrix
    """
    if type(matrix) is not np.ndarray:
        raise TypeError("matrix must be a numpy.ndarray")
    if (matrix.ndim != 2 or
        matrix.shape[0] != matrix.shape[1] or
        matrix.shape[1] == 0 or
            (np.matrix.conjugate(matrix.T) != matrix).any()):
        return None
    wight, _ = np.linalg.eig(matrix)

    if np.all(wight > 0):
        return 'Positive definite'
    if np.all(wight >= 0):
        return 'Positive semi-definite'
    if np.all(wight < 0):
        return 'Negative definite'
    if np.all(wight <= 0):
        return 'Negative semi-definite'
    else:
        return 'Indefinite'

#!/usr/bin/env python3
"""[summary]

    Raises:
        TypeError: [description]
        ValueError: [description]
        ValueError: [description]

    Returns:
        [type]: [description]
    """
import numpy as np


def correlation(C):
    """[summary]

    Args:
        C ([type]): [description]

    Raises:
        TypeError: [description]
        ValueError: [description]
        ValueError: [description]

    Returns:
        [type]: [description]
    """
    if type(C) != np.ndarray:
        raise TypeError('C must be a numpy.ndarray')

    if len(C.shape) != 2:
        raise ValueError('C must be a 2D square matrix')
    if C.shape[0] != C.shape[1]:
        raise ValueError('C must be a 2D square matrix')
    std = np.sqrt(np.diag(1 / np.diag(C)))
    return np.dot(np.dot(std, C), std)

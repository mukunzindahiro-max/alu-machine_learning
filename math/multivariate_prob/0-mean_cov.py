#!/usr/bin/env python3
"""[summary]

Raises:
    TypeError: [description]
    ValueError: [description]

Returns:
    [type]: [description]
"""
import numpy as np


def mean_cov(X):
    """[summary]

    Args:
        X ([type]): [description]

    Raises:
        TypeError: [description]
        ValueError: [description]

    Returns:
        [type]: [description]
    """
    if type(X) is not np.ndarray or X.ndim != 2:
        raise TypeError("X must be a 2D numpy.ndarray")
    if X.shape[0] < 2:
        raise ValueError("X must contain multiple data points")
    mean = np.expand_dims((np.sum(X, axis=0) / X.shape[0]), axis=0)
    cov = np.matmul((X - mean).T, (X - mean)) / (X.shape[0] - 1)
    return mean, cov

#!/usr/bin/env python3
"""[summary]

Raises:
    ValueError: [description]
    ValueError: [description]
    ValueError: [description]
    TypeError: [description]
    TypeError: [description]
    ValueError: [description]
    ValueError: [description]
    ValueError: [description]

Returns:
    [type]: [description]
"""
import numpy as np


def posterior(x, n, P, Pr):
    """[summary]

    Args:
        x ([type]):is the number of patients that develop severe side effects
        n ([type]):is the total number of patients observed
        P ([type]):is a 1D numpy.ndarray containing the various hypothetical
        Pr ([type]):is a 1D numpy.ndarray containing the prior beliefs of P

    Raises:
        ValueError: [description]
        ValueError: [description]
        ValueError: [description]
        TypeError: [description]
        TypeError: [description]
        ValueError: [description]
        ValueError: [description]
        ValueError: [description]

    Returns:
        [type]: [description]
    """
    if not isinstance(n, int) or n < 1:
        raise ValueError('n must be a positive integer')
    if not isinstance(x, int) or x < 0:
        raise ValueError(
            'x must be an integer that is greater than or equal to 0')
    if x > n:
        raise ValueError('x cannot be greater than n')
    if not isinstance(P, np.ndarray) or len(P.shape) != 1:
        raise TypeError('P must be a 1D numpy.ndarray')
    if not isinstance(Pr, np.ndarray) or Pr.shape != P.shape:
        raise TypeError('Pr must be a numpy.ndarray with the same shape as P')
    if np.any(P < 0) or np.any(P > 1):
        raise ValueError('All values in P must be in the range [0, 1]')
    if np.any(Pr < 0) or np.any(P > 1):
        raise ValueError('All values in Pr must be in the range [0, 1]')
    if not np.isclose([np.sum(Pr)], [1.])[0]:
        raise ValueError('Pr must sum to 1')
    return (((np.math.factorial(n) /
              (np.math.factorial(x) * np.math.factorial(n - x)
               )) * (P ** x) * (1 - P)**(n - x)) * Pr) / np.sum(
                   ((np.math.factorial(n) /
                     (np.math.factorial(x) * np.math.factorial(n - x)
                      )) * (P ** x) * (1 - P) ** (n - x)) * Pr)

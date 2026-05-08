#!/usr/bin/env python3
"""[summary]

Raises:
    TypeError: [description]
    ValueError: [description]
    TypeError: [description]
    ValueError: [description]
    ValueError: [description]

Returns:
    [type]: [description]
"""
import numpy as np


class MultiNormal:
    """[summary]
    """

    def __init__(self, data):
        """[summary]

        Args:
            data ([type]): [description]

        Raises:
            TypeError: [description]
            ValueError: [description]

        """
        if type(data) != np.ndarray or len(data.shape) != 2:
            raise TypeError('data must be a 2D numpy.ndarray')
        if data.shape[1] < 2:
            raise ValueError('data must contain multiple data points')
        self.mean = np.mean(data, axis=1).reshape(data.shape[0], 1)
        self.cov = np.matmul((data - self.mean),
                             (data - self.mean).T) / (data.shape[1] - 1)

    def pdf(self, x):
        """[summary]

        Args:
            x ([type]): [description]

        Raises:
            TypeError: [description]
            ValueError: [description]
            ValueError: [description]

        Returns:
            [type]: [description]
        """

        if type(x) != np.ndarray:
            raise TypeError('x must be a numpy.ndarray')
        if len(x.shape) != 2:
            raise ValueError(
                'x must have the shape ({}, 1)'.format(self.cov.shape[0]))
        if x.shape[1] != 1 or x.shape[0] != self.cov.shape[0]:
            raise ValueError(
                'x must have the shape ({}, 1)'.format(self.cov.shape[0]))
        out = np.matmul(np.matmul(-1*(x - self.mean).T,
                                  np.linalg.inv(self.cov)),
                        ((x - self.mean) / 2))
        pdf = ((1 /
                np.sqrt(
                    ((2*np.pi)**self.cov.shape[0]) *
                    np.linalg.det(self.cov))) *
               np.exp(out)).reshape(-1)[0]
        return pdf

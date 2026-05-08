#!/usr/bin/env python3
"""
This module contains a function that returns the shape of a matrix.
"""


def matrix_shape(matrix):
    """return dimension of matrix"""
    new_matrix = []
    while type(matrix) == list:
        new_matrix.append(len(matrix))
        matrix = matrix[0]
    return new_matrix

#!/usr/bin/env python3
"""
This module contains a function that returns the transpose of a matrix.
"""


def matrix_transpose(matrix):
    """transpose a matrix"""

    row = len(matrix)
    col = len(matrix[0])
    new_matrix = []
    for i in range(0, col):
        aux_r = []
        for j in range(0, row):
            aux_r.append(matrix[j][i])
        new_matrix.append(aux_r)
    return new_matrix

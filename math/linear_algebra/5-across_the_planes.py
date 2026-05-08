#!/usr/bin/env python3
"""
This module contains a function that returns the sum of
two dimension matrices .
"""


def add_matrices2D(mat1, mat2):
    """Add two matrices"""

    sum = []
    if len(mat1) != len(mat2):
        return None
    for i in range(0, len(mat1)):
        if len(mat1[i]) == len(mat2[i]):
            new_row = []
            for j in range(0, len(mat1[i])):
                new_row.append(mat1[i][j] + mat2[i][j])
            sum.append(new_row)
        else:
            return None
    return sum

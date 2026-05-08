#!/usr/bin/env python3
"""
This module contains a function multiply two arrays.
"""


def mat_mul(mat1, mat2):
    """multiply two matrices"""
    new_matrix = []
    if len(mat1[0]) != len(mat2):
        return None
    for row in range(0, len(mat1)):
        new_row = []
        for col in range(0, len(mat2[0])):
            new_value = 0
            for value in range(0, len(mat1[0])):
                new_value += mat1[row][value] * mat2[value][col]
            new_row.append(new_value)
        new_matrix.append(new_row)
    return new_matrix

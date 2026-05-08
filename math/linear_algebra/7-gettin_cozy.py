#!/usr/bin/env python3
"""
This module contains a function concatenate two arrays.
"""


def cat_matrices2D(mat1, mat2, axis=0):
    """concetenate two matrices"""
    if len(mat1) != len(mat2) and axis == 1:
        return None
    if len(mat1[0]) != len(mat2[0]) and axis == 0:
        return None

    new_matrix = []
    for row in range(0, len(mat1)):
        new_row = []
        for col in range(0, len(mat1[0])):
            new_row.append(mat1[row][col])
        if axis == 1:
            for col in range(0, len(mat2[0])):
                new_row.append(mat2[row][col])
        new_matrix.append(new_row)
    if axis == 0:
        for row in range(0, len(mat2)):
            new_row = []
            for col in range(0, len(mat2[0])):
                new_row.append(mat2[row][col])
            new_matrix.append(new_row)
    return new_matrix

#!/usr/bin/env python3
"""this module contains a function to calculate the minor of a matrix"""


def determinant(matrix):
    """function to calculate the determinant of a matrix"""

    if type(matrix) is not list or len(matrix) == 0:
        raise TypeError("matrix must be a list of lists")
    if len(matrix) == 1 and len(matrix[0]) == 0:
        return 1
    for row in matrix:
        if type(row) is not list:
            raise TypeError("matrix must be a list of lists")
        if len(row) != len(matrix):
            raise ValueError("matrix must be a spuare matrix")
    if len(matrix) == 1:
        return matrix[0][0]
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    det = 0
    for i, j in enumerate(matrix[0]):
        _mrows = [r for r in matrix[1:]]
        aux_sub = []
        for row in _mrows:
            aux = []
            for c in range(len(matrix)):
                if c != i:
                    aux.append(row[c])
            aux_sub.append(aux)
        det += (-1) ** i * j * determinant(aux_sub)
    return det


def minor(matrix):
    """function to calculate a minor of a function"""
    if type(matrix) is not list or len(matrix) == 0:
        raise TypeError("matrix must be a list of lists")
    if not matrix:
        raise TypeError("matrix must be a list of lists")
    for row in matrix:
        if type(row) is not list:
            raise TypeError("matrix must be a list of lists")
        if len(row) != len(matrix):
            raise ValueError("matrix must be a non-empty square matrix")
    if len(matrix[0]) == 1:
        return [[1]]

    minor_matrix = []
    for r in range(len(matrix)):
        minor_row = []
        for c in range(len(matrix)):
            row = [matrix[i] for i in range(len(matrix)) if i != r]
            sub_m = []

            for r_aux in row:
                aux = []
                for col in range(len(matrix)):
                    if col != c:
                        aux.append(r_aux[col])
                sub_m.append(aux)

            det = determinant(sub_m)
            minor_row.append(det)
        minor_matrix.append(minor_row)
    return minor_matrix

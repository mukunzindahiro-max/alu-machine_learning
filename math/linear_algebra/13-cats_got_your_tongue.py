#!/usr/bin/env python3
"""
This module contains a function that returns transpose of array.
"""
import numpy as np


def np_cat(mat1, mat2, axis=0):
    """concatnates two matrices"""
    return np.concatenate((mat1, mat2), axis)

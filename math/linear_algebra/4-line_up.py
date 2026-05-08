#!/usr/bin/env python3
"""
This module contains a function that returns the sum of two matrices.
"""


def add_arrays(arr1, arr2):
    """Add two array"""

    sum = []
    if len(arr1) != len(arr2):
        return None
    for i in range(0, len(arr1)):
        sum.append(arr1[i] + arr2[i])
    return sum

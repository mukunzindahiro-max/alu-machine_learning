#!/usr/bin/env python3
"""This module contains a function that perfoms
finds the best number of clusters for a GMM using the
Bayesian Information Criterion"""
import numpy as np
expectation_maximization = __import__('8-EM').expectation_maximization


def BIC(X, kmin=1, kmax=None, iterations=1000, tol=1e-5, verbose=False):
    """
    finds the best number of clusters for a GMM using the
    Bayesian Information Criterion

    X: numpy.ndarray (n, d) containing the dataset
        - n no. of data points
        - d no. of dimensions for each data point
    kmin: positive integer, smallest number of clusters to check, inclusive
    kmax: positive integer, largest number of clusters to check, inclusive
        if None, it becomes the largest number of clusters possible
    iterations: positive integer, maximum iterations used by each model
    tol: non-negative float, tolerance of the log likelihood
    verbose: boolean that determines if the EM output should be printed

    returns:
        best_k, best_result, l, b or None, None, None, None on failure
        - best_k: the number of clusters with the lowest BIC
        - best_result: tuple of (pi, m, S) for the best number of clusters
        - l: numpy.ndarray (kmax - kmin + 1) log likelihood of each size
        - b: numpy.ndarray (kmax - kmin + 1) BIC value of each size
    """
    if not isinstance(X, np.ndarray) or len(X.shape) != 2:
        return None, None, None, None
    n, d = X.shape
    if not isinstance(kmin, int) or kmin < 1 or kmin >= n:
        return None, None, None, None
    if kmax is None:
        kmax = n
    if not isinstance(kmax, int) or kmax < 1 or kmax > n:
        return None, None, None, None
    if kmax <= kmin:
        return None, None, None, None
    if not isinstance(iterations, int) or iterations <= 0:
        return None, None, None, None
    if not isinstance(tol, float) or tol <= 0:
        return None, None, None, None
    if not isinstance(verbose, bool):
        return None, None, None, None

    results = []
    likelihoods = []
    bics = []

    for k in range(kmin, kmax + 1):
        pi, m, S, g, likelihood = expectation_maximization(
            X, k, iterations, tol, verbose)
        # k means, k covariance matrices that are symmetric, and the
        # priors, of which the last is fixed by the others
        parameters = (k * d) + (k * d * (d + 1) / 2) + (k - 1)
        results.append((pi, m, S))
        likelihoods.append(likelihood)
        bics.append(parameters * np.log(n) - 2 * likelihood)

    likelihoods = np.array(likelihoods)
    bics = np.array(bics)
    best = int(np.argmin(bics))

    return kmin + best, results[best], likelihoods, bics

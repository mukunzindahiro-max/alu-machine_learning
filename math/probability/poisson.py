#!/usr/bin/env python3
"""
Poisson distribution
"""


class Poisson:
    """Poisson distribution class"""

    def __init__(self, data=None, lambtha=1.):
        """Initialize the Poisson distribution."""
        if data is not None:
            if type(data) is not list:
                raise TypeError("data must be a list")
            elif len(data) < 2:
                raise ValueError("data must contain multiple values")
            else:
                self.lambtha = float(sum(data) / len(data))
        else:
            if lambtha <= 0:
                raise ValueError("lambtha must be a positive value")
            else:
                self.lambtha = float(lambtha)

    def pmf(self, k):
        """Probability Mass Function (PMF) of
        the Poisson distribution.
        """
        k = int(k)
        if k < 0:
            return 0
        euler = 2.7182818285
        aux_factorio = 1
        aux_k = k + 1
        for i in range(1, aux_k):
            aux_factorio = aux_factorio * i
        res = ((euler **
                (-1 * self.lambtha)) *
               (self.lambtha ** k)) * (1 / aux_factorio)
        return res

    def cdf(self, k):
        """Cumulative Distribution Function (CDF) of
        the Poisson distribution.
        """
        k = int(k)
        if k < 0:
            return 0
        euler = 2.7182818285
        aux_factorio = 1
        aux_k = k + 1
        aux_s = 0
        for i in range(0, aux_k):
            aux_factorio = 1
            n_aux = i + 1
            for j in range(1, n_aux):
                aux_factorio = aux_factorio * j
            aux_s = aux_s + (self.lambtha ** i) * (1 / aux_factorio)
        res = (euler ** (-1 * self.lambtha)) * aux_s
        return res

#!/usr/bin/env python3
"""Binomial"""


class Binomial():
    """Binomial"""

    def __init__(self, data=None, n=1, p=0.5):
        """Binomial"""
        if data is None:
            if n <= 0:
                raise ValueError("n must be a positive value")
            elif p <= 0 or p >= 1:
                raise ValueError("p must be greater than 0 and less than 1")
            else:
                self.n = int(n)
                self.p = float(p)
        else:
            if type(data) != list:
                raise TypeError("data must be a list")
            elif len(data) < 2:
                raise ValueError("data must contain multiple values")
            else:
                mean = sum(data) / len(data)  # mean = n*p
                var = sum([(data[x] - mean) ** 2 for x in range(len(data))]
                          ) / len(data)
                self.p = (1 - (var / mean))
                n = mean / self.p
                self.n = int(round(n))
                self.p = mean / self.n

    def pmf(self, k):
        """pmf function"""
        k = int(k)
        if k < 0:
            return 0
        else:
            ww = factorial(self.n) / (factorial(k) * factorial(self.n - k))
            return ww * (self.p ** k) * ((1 - self.p) ** (self.n - k))

    def cdf(self, k):
        """cdf function"""
        k = int(k)
        if k < 0:
            return 0
        else:
            c = 0
            for i in range(k + 1):
                c += self.pmf(i)
            return c


def factorial(k):
    """factorial function"""
    if k == 0:
        return 1
    else:
        return k * factorial(k - 1)

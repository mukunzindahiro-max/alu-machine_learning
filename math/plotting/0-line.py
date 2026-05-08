#!/usr/bin/env python3
"""
This script generates a simple plot of the cube of numbers from 0 to 10.
"""
import numpy as np
import matplotlib.pyplot as plt

y = np.arange(0, 11) ** 3
plt.plot(y, 'r')
plt.show()

#!/usr/bin/env python3
"""
This script generates a bar of distribution of fruits.
"""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(5)
fruit = np.random.randint(0, 20, (4,3))

vect = [0, 0, 0]
l = ('apples', 'bananas', 'oranges', 'peaches')
data = ('Farrah', 'Fred', 'Felicia')
c = ('red', 'yellow', '#ff8000', '#ffe5b4')

for w in range(0, len(fruit)):
  plt.bar(data, fruit[w], 0.5, vect, color=c[w], label=l[w])
  vect = vect + fruit[w]

plt.title('Number of Fruit per Person')
plt.ylabel('Quantity of Fruit')
plt.legend(["apples", "bananas", "oranges", "peaches"])
plt.yticks(range(0, 81, 10))
plt.axis(ymax=80)
plt.show()

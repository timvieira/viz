#!/usr/bin/env python
import matplotlib
from matplotlib.widgets import Cursor
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, axisbg='#FFFFCC')

x, y = 4*(np.random.rand(2, 100)-.5)
ax.plot(x, y, 'o')
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)

# set useblit = True on gtkagg for enhanced performance
cursor = Cursor(ax, useblit=True, color='red', linewidth=1)

plt.title('gtkagg for enhanced performance using matplotlib',fontstyle='normal')
#plt.savefig('matplotlib-227.png')
#plt.savefig('matplotlib-227.svg')
#plt.clf()

plt.show()

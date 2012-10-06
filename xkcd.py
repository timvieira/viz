from pylab import linspace, show, sin, sqrt, figure, rand, exp
from matplotlib.backends.backend_agg import FigureCanvasAgg as fc
import matplotlib.font_manager as fm
import scipy.signal as signal
from scipy.stats import norm


# Function to draw a random function
def rand_func(mag=1):
    coeffs = mag * norm.rvs(loc = 0, scale = 1e-2, size = 257)
    # low pass filter
    b = signal.firwin(20, 0.15, window=('kaiser', 8))
    response = signal.lfilter(b,1,coeffs)+1
    return response

# Make some data
x = linspace(1.0, 9.0, num=257, endpoint=True)
y1 = 1.5 + 10.0 * (sin(x) * sin(x) / sqrt(x)) * exp(-0.5 * (x - 5.0) * (x - 5.0))
y2 = 3.0 + 10.0 * (sin(x) * sin(x) / sqrt(x)) * exp(-0.5 * (x - 7.0) * (x - 7.0))

#y1 *= rand_func()
#y2 *= rand_func()
#x *= rand_func()

# Set up a figure
fig = figure()
canvas = fc(fig)
# Plot the data
ax = fig.add_subplot(1, 1, 1)
ax.plot(x, y1, 'c', lw=2)
ax.plot(x, y2, 'white', lw=7)
ax.plot(x, y2, 'r', lw=2)
ax.set_ylim(0, 8)
ax.set_xlim(0, 10)

# Poor man's x-axis. There's probably a better way of doing this.
yaxis = [1.0] * 257 * rand_func(3)
xaxis = linspace(0.5,9,257)
#xaxis *= rand_func()
ax.plot(xaxis, yaxis, 'k', lw=2)
ax.arrow(9, 1, 0.1, 0, fc='k', lw=2, head_width=0.2, head_length=0.15)
# Poor man's x-tick
xax = [4.75, 4.75] + 0.1*rand(2)
yaxis = [0.9, 1.1]
ax.plot(xax, yaxis, 'k', lw=1.5)
# Poor man's y-axis. There's probably a better way of doing this.
xaxis = [1] * 257 * rand_func(3)
yaxis= linspace(0.5,7,257)
ax.plot(xaxis, yaxis, 'k', lw=2)
ax.arrow(1, 7, 0, 0.1, fc='k', lw=2, head_width=0.2, head_length=0.15)
# Font is available here: http://antiyawn.com/uploads/Humor-Sans.ttf
from os import path
print __file__
prop = fm.FontProperties(fname=path.join(path.dirname(path.abspath(__file__)), 'Humor-Sans.ttf'))
ax.text(4.5, 0.5, 'PEAK', fontproperties=prop, size=14)
ax.text(0.1, 7.5, 'intensity', fontproperties=prop, size=14, rotation=75)
ax.text(9, 0.6, 'time', fontproperties=prop, size=14, rotation=5)

ax.axison = False
# Save
#fig.savefig('xkcd.svg')
#from IPython.core.display import SVG
#SVG(filename='.svg')

show()

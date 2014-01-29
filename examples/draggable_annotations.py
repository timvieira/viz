"""
Draggable annotations are a bit quirky when one pans the axes

"""

import numpy as np
from pylab import draw, show, figure
from matplotlib.offsetbox import OffsetImage, AnnotationBbox, DraggableAnnotation, DraggableBase


def onpress(event):
    print event.key
    if event.key == 'right':
        ax.xaxis.pan(1)
    elif event.key == 'left':
        ax.xaxis.pan(-1)
    elif event.key == 'up':
        ax.yaxis.pan(+1)
    elif event.key == 'down':
        ax.yaxis.pan(-1)
    draw()

fig = figure()
fig.canvas.mpl_connect('key_press_event', onpress)

ax = fig.gca()

ann = AnnotationBbox(OffsetImage(np.arange(256).reshape(16,16)/256.0,
                                 zoom=2,
                                 norm = None,
                                 origin=None),
                     (0.5, 0.5),
                     xybox=(30, 30),
                     xycoords='data',
                     boxcoords="offset points",
                     frameon=True, pad=0.4,  # BboxPatch
                     bboxprops=dict(boxstyle="round", fc="y"),
                     fontsize=None,
                     arrowprops=dict(arrowstyle="->"))

ax.add_artist(ann)

ann.draggable()

show()

#draggable = DraggableAnnotation(a, use_blit=True)

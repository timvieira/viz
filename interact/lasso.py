"""
Show how to use a lasso to select a set of points and get the indices
of the selected points.  A callback is used to change the color of the
selected points

This is currently a proof-of-concept implementation (though it is
usable as is).  There will be some refinement of the API and the
inside polygon detection routine.
"""
from matplotlib.widgets import Lasso
from matplotlib.nxutils import points_inside_poly
from matplotlib.collections import RegularPolyCollection

from numpy import nonzero

from debug import ip

from matplotlib.colors import colorConverter
to_rgba = colorConverter.to_rgba


class LassoManager(object):

    def __init__(self, ax, df, xcol='x', ycol='y'):
        self.df = df
        self.ax = ax
        self.canvas = ax.figure.canvas
        self.lasso_lock = False  # indicates whether another widget event has priority

        self.xys = df[[xcol, ycol]].values
        self.collection = RegularPolyCollection(numsides=ax.figure.dpi,
                                                rotation=6,
                                                sizes=(100,),
                                                facecolors = [to_rgba('green', alpha=0.0)]*len(self.xys),
                                                linewidths = 0,
                                                offsets = self.xys,
                                                transOffset = ax.transData)
        ax.add_collection(self.collection)

        self.canvas.mpl_connect('button_press_event', self.onpress)
        self.canvas.mpl_connect('button_release_event', self.onrelease)
        self.selected = []
        self.lasso = None

    def callback(self, verts):
        [selected] = nonzero(points_inside_poly(self.xys, verts))
        # change face colors inplace
        facecolors = self.collection.get_facecolors()
        facecolors[:] = to_rgba('green', alpha=0.0)
        facecolors[selected] = to_rgba('yellow', alpha=0.6)
        self.canvas.draw_idle()
        self.canvas.widgetlock.release(self.lasso)
        self.selected = selected

    def onpress(self, event):
        if self.canvas.widgetlock.locked():
            return
        if event.inaxes is None:
            return
        self.lasso = Lasso(event.inaxes, (event.xdata, event.ydata), self.callback)
        self.canvas.widgetlock(self.lasso)  # acquire lock on this lasso widget
        self.lasso_lock = True              # used when we release

    def onrelease(self, event):
        'on release we reset the press data'
        # test whether the widgetlock was initiated by the lasso
        if self.lasso_lock:
            self.canvas.widgetlock.release(self.lasso)
            self.lasso_lock = False
        print self.selected

def example():
    import matplotlib.pyplot as pl

    import pandas
    from numpy.random import uniform

    n = 25
    m = pandas.DataFrame({'x': uniform(-1, 1, size=n),
                          'y': uniform(-1, 1, size=n),
                          'size': uniform(3, 10, size=n) ** 2,
                          'color': uniform(0, 1, size=n)})


    print m

    ax = pl.subplot(111)
    lman = LassoManager(ax, m)

    pl.scatter(m['x'], m['y'])

    pl.show()

if __name__ == '__main__':
    example()

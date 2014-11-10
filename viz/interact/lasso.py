"""
Use a lasso to select a set of points and get the indices of the selected
points.  A callback is used to change the color of the selected points

TODO:

 * LassoBrowser and PointBrowser should be composable. Currently, they don't
   communicate.

    - Common code for dealing with pandas (e.g. the parallel idxs and point
      array); plot/axes updating; callback

    - PointBrowser only supports selecting one point. Why not generalize to
      shift-click many points this makes it much more like lasso.

"""
import matplotlib.pylab as pl
from matplotlib.widgets import Lasso
from matplotlib.nxutils import points_inside_poly
from matplotlib.collections import RegularPolyCollection
from matplotlib.colors import colorConverter
from numpy import nonzero, array

import matplotlib.pyplot as pl

to_rgba = colorConverter.to_rgba

try:
    from debug import ip
except ImportError:
    pass


class LassoBrowser(object):

    def __init__(self, df, ax=None, xcol='x', ycol='y', callback=None):
        self.df = df
        self.ax = ax or pl.gca()
        self.canvas = ax.figure.canvas
        self.lasso_lock = False             # indicates if another widget event has priority
        self.idxs = array(list(self.df.T))  # look up parallel with point indices
        self.xys = df[[xcol, ycol]].values
        self.xcol = xcol
        self.ycol = ycol

        # timv: don't think this PolyCollection is needed..
        self.collection = RegularPolyCollection(numsides=ax.figure.dpi,
                                                rotation=6,
                                                sizes=(100,),
                                                facecolors = [to_rgba('green', alpha=0.0)]*len(self.xys),
                                                linewidths = 0,
                                                offsets = self.xys,
                                                transOffset = ax.transData)
        ax.add_collection(self.collection)

        self.user_callback = callback
        self.canvas.mpl_connect('key_press_event', self.onpress)
        self.canvas.mpl_connect('button_press_event', self.onpress)
        self.canvas.mpl_connect('button_release_event', self.onrelease)
        self.selected = None
        self.lasso = None

    def lasso_callback(self, verts):
        if verts is not None and len(verts):
            [selected] = nonzero(points_inside_poly(self.xys, verts))
        else:
            selected = []

        # change face colors inplace
        facecolors = self.collection.get_facecolors()
        facecolors[:] = to_rgba('green', alpha=0.0)
        facecolors[selected] = to_rgba('yellow', alpha=0.6)

        # convert from point indices to dataframe indices
        idx = self.idxs[selected]
        m = self.df.ix[idx]      # show selected rows of dataframe

        if self.user_callback is None:
            print m
        else:
            self.user_callback(m)

        self.canvas.draw_idle()
        self.canvas.widgetlock.release(self.lasso)
        self.selected = selected

    def onpress(self, event):
        if self.canvas.widgetlock.locked():
            return
        if event.inaxes is None:
            return

        if event.key in ('escape',):
            self.selected = []
            self.lasso_callback([])
            return

        # TODO: implement zoom out as undo.
        # zoom in to selection
        if event.key in ('+', '='):
            selected_rows = self.df.ix[self.selected]
            xs = selected_rows[self.xcol]
            ys = selected_rows[self.ycol]
            self.ax.set_xlim(xs.min(), xs.max())
            self.ax.set_ylim(ys.min(), ys.max())
            self.canvas.draw()
            return

        self.lasso = Lasso(event.inaxes, (event.xdata, event.ydata), self.lasso_callback)
        self.canvas.widgetlock(self.lasso)  # acquire lock on lasso widget
        self.lasso_lock = True              # used when we release

    def onrelease(self, event):
        'on release we reset the press data'
        # test whether the widgetlock was initiated by the lasso
        if self.lasso_lock:
            self.canvas.widgetlock.release(self.lasso)
            self.lasso_lock = False


def example():
#    pl.ioff()
    pl.ion()

    import pandas
    from numpy.random import uniform

    n = 25
    m = pandas.DataFrame({
            'x': uniform(-1, 1, size=n),
            'y': uniform(-1, 1, size=n),
            'size': uniform(3, 10, size=n) ** 2,
            'color': uniform(0, 1, size=n),
    })

    # test using a custom index
    m['silly_index'] = ['%sth' % x for x in range(n)]
    m.set_index('silly_index', drop=True, inplace=True, verify_integrity=True)

    print m

    ax = pl.subplot(111)
    plt = ax.scatter(m['x'], m['y'])

    b = LassoBrowser(m, ax)
    print b.idxs

    #from viz.interact.pointbrowser import PointBrowser
    #pb = PointBrowser(m, plot=plt)

    pl.show()

    ip()

if __name__ == '__main__':
    example()

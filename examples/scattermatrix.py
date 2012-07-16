import pylab as pl
from debug import ip

import pandas
d = pandas.read_csv('/home/timv/projects/viz/demo/bubble/crimeRatesByState2005.csv')
d = d.ix[1:]  # remove aggregate entry for United States -- does pandas have a nicer way to do this?

# Attempting to copy the axes from scatter_matrix plot to its own
# figure. Currrently, sort of works, but is tiny because the axes remains its
# original size.
def callback(event):
    print 'callback:', event
    ax = event.inaxes
    pl.ion()
    newfig = pl.figure()
    ax.set_figure(newfig)
    newfig.set_axes([ax])
    newfig.canvas.show()
    ip()

# scatter matrix
axes = pandas.tools.plotting.scatter_matrix(d)
fig = axes[0,0].figure  # all axes are on the same figure, so take the first one.
fig.canvas.mpl_connect('button_press_event', callback)

pl.show()

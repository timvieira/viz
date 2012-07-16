import pylab as pl
import numpy as np
from viz.interact.pointbrowser import PointBrowser

import pandas
d = pandas.read_csv('crimeRatesByState2005.csv')
d = d.ix[1:]  # remove aggregate entry for United States -- does pandas have a nicer way to do this?

def draw_text(row):
    pl.text(x=row['murder'],
            y=row['burglary'],
            s=row['state'],
            size=11,
            horizontalalignment='center')

sct = pl.scatter(x=d['murder'],
                 y=d['burglary'],
                 c=d['larceny_theft'],
                 s=np.sqrt(d['population']),
                 linewidths=2,
                 edgecolor='w')
d.T.apply(draw_text)  # add labels by apply the draw_text function row-wise

b = PointBrowser(d, xcol='murder', ycol='burglary', plot=sct)

sct.set_alpha(0.5)
pl.axis([0,11,200,1280])   # -- remove this and see D.C. an outlier a very serious outlier
pl.xlabel('Murders per 100,000 population')
pl.ylabel('Burglaries per 100,000 population')

pandas.tools.plotting.scatter_matrix(d)

pl.show()

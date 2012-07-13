from pylab import *
from scipy import *

import pandas
d = pandas.read_csv('crimeRatesByState2005.csv')
d = d.ix[1:]  # remove aggregate entry for United States -- does pandas have a nicer way to do this?

def draw_text(row):
    text(x=row['murder'],
         y=row['burglary'],
         s=row['state'],
         size=11,
         horizontalalignment='center')

import pandas
import sys
sys.path.append('/home/timv/projects/ldp/code/working/bin')
from viz.pointbrowser import PointBrowser

def callback(browser, row):
    print
    print row

sct = scatter(x=d['murder'],
              y=d['burglary'],
              c=d['larceny_theft'],
              s=sqrt(d['population']),
              linewidths=2,
              edgecolor='w')
d.T.apply(draw_text)  # add labels

b = PointBrowser(d, xcol='murder', ycol='burglary', callback=callback, plot=sct)

sct.set_alpha(0.5)
axis([0,11,200,1280])   # -- remove this and see D.C. an outlier a very serious outlier
xlabel('Murders per 100,000 population')
ylabel('Burglaries per 100,000 population')

# scatter matrix
pandas.tools.plotting.scatter_matrix(d)

show()

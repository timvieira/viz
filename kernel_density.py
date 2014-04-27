# -*- coding: utf-8 -*-
"""Scatter plots considered harmful.

Original by endolith@gmail.com (2011-Jun-19)
Modifications by http://timvieira.github.io
"""

import pylab as pl
import numpy as np
from scipy.stats.kde import gaussian_kde


def scatter_kde(x, y, ax=None):
    if ax is None:
        ax = pl.gca()

    # build kernel density estimator (KDE)
    kde = gaussian_kde(np.array(zip(x,y)).T)

    ax.scatter(x, y, alpha=0.5, color='white')

    # top right bottom left
    t = y.max()
    r = x.max()
    b = y.min()
    l = x.min()

    # Regular grid to evaluate kde upon
    n = 128
    x_flat = np.r_[l:r:n*1j]
    y_flat = np.r_[b:t:n*1j]

    g = np.array(np.meshgrid(x_flat, y_flat)).reshape(2,n*n)

    # evaluate the KDE at grid points
    z = kde(g).reshape(n,n)

    ax.imshow(z,
              aspect=x_flat.ptp()/y_flat.ptp(),
              origin='lower',
              extent=(l,r,b,t))

    return ax


def test():
    from scipy.stats import norm
    rvs = np.append(norm.rvs(loc=2,scale=1,size=(200,1)),
                    norm.rvs(loc=1,scale=3,size=(200,1)),
                    axis=1).T

    scatter_kde(rvs[0,:], rvs[1,:])

    pl.show()


if __name__ == '__main__':
    test()

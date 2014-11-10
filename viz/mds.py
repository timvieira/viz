#!/usr/bin/env python
import pylab
from numpy import sqrt, mean, array, zeros, mat
from numpy.linalg import svd
from mpl_toolkits.mplot3d import Axes3D

def mds(X, dimensions=2):
    """
    Multidimensional Scaling - Given a matrix of interpoint distances,
    find a set of low dimensional points that have similar interpoint
    distances.

    Author: Jeremy M. Stober
    with modifications by Tim Vieira
    """
    E = (-0.5 * X*X)
    # Use mat to get column and row means to act as column and row means.
    Er = mat(mean(E, axis=1))
    Es = mat(mean(E, axis=0))
    # From Principles of Multivariate Analysis: A User's Perspective (pg 107).
    F = array(E - Er.T - Es + mean(E))
    # svd to get low rank approximation or F
    [U, S, V] = svd(F)
    Y = U * sqrt(S)
    return (Y[:,0:dimensions], S)

def mds_scatter(distance):
    Y, _ = mds(distance)
    pylab.scatter(Y[:,0], Y[:,1], s=20, c='b', marker='o')
    pylab.grid(True)
    return Y

def mds_plot2D(points, distance):
    Y, _ = mds(distance)
    pylab.scatter(Y[:,0], Y[:,1], s=20, c='b', marker='o')
    for user, x, y in zip(points, Y[:,0], Y[:,1]):
        pylab.text(x, y, user, fontsize=7)
    pylab.grid(True)
    return Y

def mds_plot3D(points, distance):
    Y, _ = mds(distance, 3)
    ax = Axes3D(pylab.figure())
    ax.scatter(Y[:,0], Y[:,1], Y[:,2])            # add points to plot
    map(ax.text, Y[:,0], Y[:,1], Y[:,2], points)  # add labels to points
    #pylab.grid(True)

if __name__ == '__main__':
    from viz.demo import mds_twitter
    mds_twitter.main()

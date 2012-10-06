from viz.mds import mds, mds_plot2D, mds_plot3D
from numpy import array, zeros, reshape, shape

import numpy as np
import pylab as pl

# hack the sys path to import twitter similarity metric
import sys; sys.path.append('/home/timv/projects/shelf/twitter-similarity')
from similarity import User, example_data

from matplotlib.image import imread

import cPickle as pickle
import Image

import pandas

from debug import ip
from terminal import yellow

# place to cache data
from os import path
import mds_twitter
tweet_cache = path.join(path.dirname(path.abspath(mds_twitter.__file__)), 'tweets.pkl~')

from viz.interact import LassoBrowser, PointBrowser


def main(usecached=True):
    if usecached and path.exists(tweet_cache):
        (users, distance) = pickle.load(file(tweet_cache, 'r'))
    else:
        sets = example_data()
        users = list(reduce(set.union, sets))
        N = len(users)
        distance = zeros((N, N))
        for (i, xi) in enumerate(users):
            for (j, xj) in enumerate(users):
                distance[i,j] = xi.similarity(xj)
        pickle.dump((users, distance), file(tweet_cache, 'wb'))

    pl.figure()
    pl.grid(True)

    labels = [u.username for u in users]

    [Y, _] = mds(distance)

    print users

    X = pandas.DataFrame({
        'x': Y[:,0],
        'y': Y[:,1],
        'user': labels,
        'obj': users,
    })

    sct = pl.scatter(Y[:,0], Y[:,1], s=30*np.ones_like(users), c='b', lw=0)
    for user, x, y in zip(labels, Y[:,0], Y[:,1]):
        pl.text(x, y, user, fontsize=7)
    pl.grid(False)

    threshold = 0.05
    for i in xrange(len(users)):
        for j in xrange(i + 1, len(users)):
            x = Y[[i,j], 0]
            y = Y[[i,j], 1]
            if distance[i,j] >= threshold:
                pl.plot(x, y, lw=10.0*distance[i,j], alpha=distance[i,j], c='k')


    if 0:
        # TODO: I want points to resize according proportional to similarity to
        # selected point. I'm having trouble getting matplotlib to do this for
        # me -- such an inconsistent API!
        def callback(br, m):
            _ = users, sct   # FIXME: ip only seems to take local and global; sct is neither..
            newsizes = np.array(map(m.ix[0].similarity, users)) * 30
            #s = sct.get_sizes()
            #s[:] = newsizes
            sct._sizes = newsizes
            ip()
        b = PointBrowser(X, ax=sct.get_axes(), callback=callback)
    else:
        def callback(m):
            if m.empty:
                return
            print '***********************************'
            common_words = reduce(set.intersection, m['obj'].map(lambda x: x.features))
            print common_words
            print '***********************************'
        b = LassoBrowser(X, ax=sct.get_axes(), callback=callback)

    #mds_plot2D(labels, distance)
    #mds_plot3D(labels, distance)
    if 'icons' in sys.argv:
        icons(users, distance)

    b.ax.figure.set_facecolor('white')
    b.ax.set_axis_off()

#    pl.ion()
    pl.show()
#    ip()


def icons(users, distance):
    """Visualization using user profile images as the points."""

    # It would be pretty cool to put user thumbails where points are.
    # but i'm still not sure how to do this yet.
    images = []

    try:
        print 'getting images..'
        for p in users:
            print p
            f = p.image
            img = imread('image.tmp')
            images.append(img)
    except Exception as e:
        print 'got an error...'
        import traceback
        etype, evalue, tb = sys.exc_info()
        print yellow % '\n'.join(traceback.format_exception(etype, evalue, tb))
        ip()

    (W, H, _) = shape(img)  # thumbnails should all be the same size
    count = len(images)

    pl.figure()

    P2, _ = mds(distance, 2)
    X,Y = P2[:,0], P2[:,1]

    ## XXX: not a great transformation b/c we might stretch more in one dimension
    def N(x):
        "force x to fit in interval [0,1]"
        x = (x - x.min())
        x = x / x.max()
        assert all(x >= 0) and all(x <= 1)
        return x
    X = N(X)*475
    Y = N(Y)*425

    figimages = [pl.figimage(img, xo=x, yo=y) for img, x, y in zip(images, X, Y)]


if __name__ == "__main__":
    main()

from viz.mds import mds, mds_plot2D, mds_plot3D
from numpy import array, zeros, reshape, shape

import pylab as pl

# hack the sys path to import twitter similarity metric
import sys; sys.path.append('/home/timv/projects/shelf/twitter-similarity')
from similarity import User, example_data

import cPickle as pickle
import Image
from debug import ip

def twitter_example():

    if 1:
        sets = example_data()
        points = reduce(set.union, sets)
#        users = map(User, points)
        users = points
        N = len(points)
        distance = zeros((N, N))
        for (i, xi) in enumerate(points):
            for (j, xj) in enumerate(points):
                distance[i,j] = xi.similarity(xj)

        pickle.dump((users, distance), file('junk.pkl~','wb'))
    else:
        (users, distance) = pickle.load(file('junk.pkl~', 'r'))

    pl.figure()
    pl.grid(True)
    mds_plot2D(points, distance)
    mds_plot3D(points, distance)
#    twitter_icons(users, distance)


def twitter_icons(users, distance):
    """Visualization using user profile images as the points."""

    # It would be pretty cool to put user thumbails where points are.
    # but i'm still not sure how to do this yet.
    images = []

    try:
        print 'getting images..'
        for p in users:
            print p

            f = p.image
            img = Image.open(f).convert('RGB')
            images.append(img)
    except Exception as e:
        print 'got an error...'

        import traceback, sys
        from terminal import yellow
        etype, evalue, tb = sys.exc_info()
        print yellow % '\n'.join(traceback.format_exception(etype, evalue, tb))

        ip()


    (W, H) = shape(img.getdata())  # thumbnails should all be the same size
    count = len(images)

    def img2array(im):
        return reshape(array(im.getdata()), (im.size[1], im.size[0], 3))

    images = [img2array(img) for img in images]

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

    figimages = [pl.figimage(img, xo=x, yo=y) #, cmap=pl.cm.gist_gray)
                 for img, x, y in zip(images, X, Y)]

    pl.show()


if __name__ == "__main__":
    twitter_example()

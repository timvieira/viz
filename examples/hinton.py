from numpy import array, log, max, ceil, abs, sqrt
from pylab import axis, fill, isinteractive, ioff, clf, ion, show

def _blob(x,y,area,colour):
    """
    Draws a square-shaped blob with the given area (< 1) at
    the given coordinates.
    """
    hs = sqrt(area) / 2
    xcorners = array([x - hs, x + hs, x + hs, x - hs])
    ycorners = array([y - hs, y - hs, y + hs, y + hs])
    fill(xcorners, ycorners, colour, edgecolor=colour)

def hinton(W, maxWeight=None):
    """
    Draws a Hinton diagram for visualizing a weight matrix.
    Temporarily disables matplotlib interactive mode if it is on,
    otherwise this takes forever.
    """
    reenable = False
    if isinteractive():
        ioff()
    clf()
    height, width = W.shape
    if not maxWeight:
        maxWeight = 2**ceil(log(max(abs(W)))/log(2))

    fill(array([0,width,width,0]), array([0,0,height,height]), 'gray')
    axis('off')
    axis('equal')
    for x in xrange(width):
        for y in xrange(height):
            _x = x+1
            _y = y+1
            w = W[y,x]
            if w > 0:
                _blob(_x - 0.5, height - _y + 0.5, min(1, w/maxWeight), 'white')
            elif w < 0:
                _blob(_x - 0.5, height - _y + 0.5, min(1, -w/maxWeight), 'black')
    if reenable:
        ion()
    show()

def example():
    from numpy.random import rand
    N = 20
    X = rand(N,N) - 0.5
    hinton(X)

if __name__ == '__main__':
    example()

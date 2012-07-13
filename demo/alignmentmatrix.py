import numpy as np
import pylab as pl
from debug import ip

def extraction_set(e, f, a):
    pass


def align(E, F, threshold = 0.25):
    "Really simple aligner."

    def score(e,f):
        "Score affinity between two words."
        return len(set(e) & set(f)) * 1.0 / len(set(e) | set(f))

    a = np.zeros((len(E), len(F)))

    for i, e in enumerate(E):
        for j, f in enumerate(F):
            a[i,j] = score(e, f) >= threshold

    return a


from matplotlib.patches import FancyBboxPatch, Rectangle, BoxStyle
from matplotlib.collections import PatchCollection


def draw_alignment(E, F, A):

    fig = pl.figure(figsize=(len(E), len(F)))
    ax = fig.add_subplot(111)
    ax.grid(False)

    #ax = pl.axes([0,0,1,1])

    #N = len(E) + 1
    #for i, e in enumerate(E):
    #    pl.text((i+2) * 1.0 / N, 0.1, e, ha="center", size=14)

    #M = len(F) + 1
    #for j, f in enumerate(F):
    #    pl.text(0.1, (j+2) * 1.0 / M, f, ha="center", size=14)

    ax.matshow(A)
    ax.set_xticks(np.arange(0, len(F)) + 0.5)
    ax.set_xticklabels(F)
    ax.set_yticks(np.arange(0, len(E)) + 0.5)
    ax.set_yticklabels(E)

    #patches = []
    # add a fancy box
    #fancybox = FancyBboxPatch((0,0), 0.05, 0.1, boxstyle=BoxStyle("Round", pad=0.02))
    #patches.append(fancybox)
    #art = Rectangle(pos[:,1] - np.array([0.025, 0.05]), 0.05, 0.1, ec="none")
    #collection = PatchCollection(patches, cmap='jet', alpha=0.4)
    #ax.add_collection(collection)

    pl.draw()



def test():

    e = 'The chicken is dry .'
    f = 'Da chikin iz on the drizzy .'

    e = e.split()
    f = f.split()

    a = align(e, f)
    print a

    draw_alignment(e, f, a)

    extraction_set(e, f, a)

    pl.show()



if __name__ == '__main__':
    test()

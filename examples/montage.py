#!/usr/bin/env pythonw
# encoding: utf-8
"""
M = montage(X, colormap=cm.gist_gray)

Generates a single "contact sheet" montage array and plots the result using the
supplied colormap. X is a multimensional array with sides of length (m,n,count).

See
http://www.mathworks.com/access/helpdesk/help/toolbox/images/montage.html

Inspired by the following Octave function (the code is in Finnish):
http://www.cis.hut.fi/Opinnot/T-61.2010/Harjoitustyo/myOctaveMontage.m

Sample data used in main() is from MIT open courseware (creative commons?):
http://ocw.mit.edu/OcwWeb/Brain-and-Cognitive-Sciences/9-641JSpring-2005/Assignments/

Created by Peter Skomoroch on 2008-02-28.
Copyright (c) 2008 DataWrangling. All rights reserved.
"""

import os
import sys
import time

from numpy import array, flipud, shape, zeros, rot90, ceil, floor, sqrt
from scipy import io, reshape, size
import pylab

def montage(X, colormap=pylab.cm.gist_gray):

    m, n, count = shape(X)

    mm = int(ceil(sqrt(count)))
    nn = mm
    M = zeros((mm * m, nn * n))

    image_id = 0
    for j in range(mm):
        for k in range(nn):
            if image_id >= count:
                break
            sliceM, sliceN = j * m, k * n
            M[sliceN:sliceN + n, sliceM:sliceM + m] = X[:, :, image_id]
            image_id += 1

    pylab.imshow(flipud(rot90(M)), cmap=colormap)
    pylab.axis('off')
    return M


def main():
    # This example loads greyscale face data which has been cropped into
    # square matrices of length L.  The raw matlab data has one column
    # for each face, which has been reshaped into a vector.
    faces_workspace = io.loadmat('/home/timv/projects/scientific/data/faces.mat')
    faces = faces_workspace['faces']

    # This example creates a similar montage of handwritten digits from a
    # sample of the the MNIST database
    digits_workspace = io.loadmat('../data/mnistabridged.mat')
    digits = digits_workspace['test']

    for j, D in enumerate([faces, digits]):

        try:
            array_count = shape(D)[1]
            L = int(sqrt(shape(D)[0]))
            X = zeros((L, L, array_count))

            for i in range(array_count):
                X[:,:,i]= reshape(D[:,i], (L, L))

            pylab.figure(j)
            montage(X)

        except MemoryError, detail:
            print "MemoryError: ", detail

    pylab.show()


if __name__ == '__main__':
    main()

from numpy.random import rand
from numpy import arange

from pylab import bar, figure, xticks, show, grid, plot, text


def labeled_points(X, Y, labels):
    """ labeled scatter plot """
    figure()
    for x,y,l in zip(X, Y,labels):
        plot([x], [y], 'o')
        text(x, y, ' ' + l, fontsize=9, rotation=30, color='green')
    grid()



def bar_graph(d):
    """ bar graph from dict """

    figure()

    items = d.items()

    # add bars
    for (i, (_, v)) in enumerate(items):
        bar(i + 0.25 , v, color='red')

    # x-axis labels
    xticks(arange(0.65, len(items)),
           ['%s' % (k,) for (k,_) in items])


if __name__ == '__main__':
    bar_graph({'A': 70, 'B': 290, 'C': 130})

    N = 10
    labeled_points(X=rand(N), 
                   Y=rand(N),
                   labels=['label-%d' % i for i in xrange(N)])

    show()


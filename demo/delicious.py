#!/usr/bin/env python
import simplejson
from urllib import urlopen
from collections import namedtuple
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import networkx as nx
import pandas
from debug import ip
from terminal import *
from iterextras import flatten

def delicious_data(tag, count=100):
    url = 'http://feeds.delicious.com/v2/json/tag/%s?count=%s' % (tag, count)
    return simplejson.load(urlopen(url))


Bookmark = namedtuple('Bookmark', 'title url user tags')

def delicious(tag, num=50):
    # TODO: pager to get data when more than 1 page
    url = "http://feeds.delicious.com/v2/json/tag/%s?count=%d" % (tag, num)
    for x in simplejson.load(urlopen(url)):
        yield Bookmark(url=x['u'], user=x['a'], tags=[t.lower() for t in x['t']], title=x['d'])

def fallbackdata():
    yield Bookmark(user='timvieira', tags=['python', 'nlp'], url=None, title=None)
    yield Bookmark(user='jayjay', tags=['python'], url=None, title=None)
    yield Bookmark(user='fanny', tags=['python'], url=None, title=None)
    yield Bookmark(user='markus', tags=['python'], url=None, title=None)
    yield Bookmark(user='billy', tags=['python', 'nlp'], url=None, title=None)


def main(tag):

    G = nx.Graph()
    G.tags = set()
    G.users = set()

    data = list(delicious(tag))
    #data = list(fallbackdata())

    for b in data:
        for t in b.tags:
            G.add_edge(b.user, t)
        G.tags.update(b.tags)
        G.users.add(b.user)

    plt.figure(figsize=(20,10))

    pos = nx.spring_layout(G, iterations=100)

    for node in G.tags:
        nx.draw_networkx_nodes(G,
                               pos,
                               nodelist=[node],
                               node_shape='o',
#                               node_size=G.degree(node)*355,
                               node_size=355,
                               node_color='b')

    nx.draw_networkx_edges(G, pos, width=1, edge_color='k')

    ax = pl.gca()

    for node in G.nodes():
        font_color = 'w'
        font_size = 8
        kw = {}
        if node in G.tags:
            #font_size = (G.degree(node) + 4)*1.3
            font_size = 10
        else:
            kw['backgroundcolor'] ='red'

        (x,y) = pos[node]
        t = ax.text(x, y, node,
                    size=font_size,
                    color=font_color,
                    horizontalalignment='center',
                    verticalalignment='center',
                    **kw)

    plt.show()

if __name__ == '__main__':
    main(tag='python')

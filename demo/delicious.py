import simplejson
import urllib
import pandas

import numpy as np
from debug import ip
from terminal import *
from iterextras import flatten

def delicious_data(tag, count=100):
    url = 'http://feeds.delicious.com/v2/json/tag/%s?count=%s' % (tag, count)
    return simplejson.load(urllib.urlopen(url))

def main(tag):
    data = delicious_data(tag)

    # u: url, a: user, t: tags, d: title, dt: date
    df = pandas.DataFrame(data)

    for user, data in df.groupby('a'):
        print yellow % user
        print flatten(data['t'].values)

    for doc, data in df.groupby('u'):
        print yellow % doc
        print flatten(data['t'].values)
        #print data['a'].values
        print map(repr, data['d'].values)


if __name__ == '__main__':
    main(tag='python')

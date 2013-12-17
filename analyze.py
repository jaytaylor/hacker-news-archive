#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from pprint import pprint
from models import ItemLog, Item, Snapshot
try:
    import cPickle as pickle
except ImportError:
    import pickle

if len(sys.argv) <= 1:
    sys.stderr.write('error: missing required parameter: pickled items filename\n')
    sys.exit(1)

inputFilename = sys.argv[1]

if not os.path.exists(inputFilename):
    sys.stderr.write('error: file not found: "{0}"\n'.format(inputFilename))
    sys.exit(1)

with open(inputFilename, 'rb') as fh:
    items = pickle.load(fh)
    print 'items loaded'


N = 20

def printSet(items):
    pprint(map(lambda i: 'hours={0}, maxPoints={1}, maxComments={2}, {3}'.format(len(i.log), i.maxPoints(), i.maxComments(), i.__str__()[0:80]), items))

print '\nTop {0} by hours on Front Page:'.format(N)
byDurationOnFrontPage = sorted(items.values(), key=lambda item: len(item.log), reverse=True)[0:N]
printSet(byDurationOnFrontPage)

print '\nTop {0} by points:'.format(N)
byPoints = sorted(items.values(), key=lambda item: item.maxPoints(), reverse=True)[0:N]
printSet(byPoints)

print '\nTop {0} by comments:'.format(N)
byComments = sorted(items.values(), key=lambda item: item.maxComments(), reverse=True)[0:N]
printSet(byComments)

print '\nTop {0} articles with more comments than points:'.format(N)
moreCommentsThanPoints = sorted(filter(lambda item: item.maxComments() > item.maxPoints(), items.values()), key=lambda item: item.maxComments() / item.maxPoints(), reverse=True)[0:N]
printSet(moreCommentsThanPoints)


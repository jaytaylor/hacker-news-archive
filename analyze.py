#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import ItemLog, Item, Snapshot
try:
    import cPickle as pickle
except ImportError:
    import pickle

with open('items.pickle', 'rb') as fh:
    items = pickle.load(fh)
    print 'items loaded'

byDurationOnFrontPage = sorted(items.values(), key=lambda item: len(item.log), reverse=True)[0:10]

print map(lambda i: '{0}/{1}'.format(len(i.log), i.__str__()), byDurationOnFrontPage)




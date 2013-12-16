#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
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

byDurationOnFrontPage = sorted(items.values(), key=lambda item: len(item.log), reverse=True)[0:10]

print map(lambda i: '{0}/{1}'.format(len(i.log), i.__str__()), byDurationOnFrontPage)




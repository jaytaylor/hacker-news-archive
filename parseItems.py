#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Snapshot parser."""

import subprocess
from bs4 import BeautifulSoup
from lib.models import ItemLog, Item, Snapshot
from lib.text import unixTimestamp, integerRe
try:
    import cPickle as pickle
except ImportError:
    import pickle

out =  subprocess.check_output(['find', 'data', '-wholename', '*.html.orig']).strip()
snapshots = []
for filename in out.split('\n'):
    with open(filename, 'r') as fh:
        #print filename
        snapshot = Snapshot(unixTimestamp(filename), fh.read())
        snapshots.append(snapshot)
#        break
        #print map(lambda s: s.__str__(), snapshots[-1].items())

items = {}
for snapshot in snapshots:
    print snapshot.ts
    for item in snapshot.items():
        if item.id not in items:
            items[item.id] = item
        else:
            # Just append the log.
            items[item.id].log += item.log
        
with open('items.pickle', 'wb') as fh:
    pickle.dump(items, fh)

print len(snapshots)
print len(items)




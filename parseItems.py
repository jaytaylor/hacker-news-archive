#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Snapshot parser."""

import os, subprocess
from bs4 import BeautifulSoup
from lib.models import ItemLog, Item, Snapshot
from lib.text import unixTimestamp, integerRe
try:
    import cPickle as pickle
except ImportError:
    import pickle


print 'starting data loading'

if not os.path.exists('snapshots.pickle'):
    def getCachedSnapshot(filename):
        """Attempt to get pre-computed snapshot."""
        pickleFilename = filename.replace('.html.orig', '.pickle')
        if os.path.isfile(pickleFilename):
            try:
                with open(pickleFilename, 'rb') as pfh:
                    return pickle.load(pfh)
            except Exception, e:
                print 'error: {0}'.format(e)
        return None

    out =  subprocess.check_output(['find', 'data', '-wholename', '*.html.orig']).strip()
    snapshots = []
    for filename in out.split('\n'):
        snapshot = getCachedSnapshot(filename)
        if snapshot is None:
            with open(filename, 'r') as fh:
                snapshot = Snapshot(unixTimestamp(filename), fh.read())
                pickleFilename = filename.replace('.html.orig', '.pickle')
                with open(pickleFilename, 'wb') as pfh:
                    pickle.dump(snapshot, pfh)
        print snapshot.ts
        snapshots.append(snapshot)

    with open('snapshots.pickle', 'wb') as fh:
        pickle.dump(snapshots, fh)
else:
    with open('snapshots.pickle', 'rb') as fh:
        snapshots = pickle.load(fh)

print 'finished reading data'

items = {}
for snapshot in snapshots:
    print snapshot.ts
    for item in snapshot.items():
        if item.id not in items:
            items[item.id] = item
        else:
            # Merge the logs.
            items[item.id].log += item.log

with open('items.pickle', 'wb') as fh:
    pickle.dump(items, fh)

print len(snapshots)
print len(items)




#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""d"""

import re, subprocess
from datetime import datetime
from bs4 import BeautifulSoup
from models import ItemLog, Item, Snapshot
try:
    import cPickle as pickle
except ImportError:
    import pickle

unixTsRe = re.compile(r'''[^0-9]*([0-9]+)[^0-9]*''')
integerRe = re.compile(r'''[^0-9]+''')

def extractTimestamp(s):
    m = unixTsRe.match(s)
    return datetime.fromtimestamp(int(m.group(1)))

out =  subprocess.check_output(['find', 'data', '-wholename', '*.html.orig']).strip()
snapshots = []
for filename in out.split('\n'):
    with open(filename, 'r') as fh:
        #print filename
        snapshot = Snapshot(extractTimestamp(filename), fh.read())
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




#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""String/text utilities."""

import datetime, re


integerRe = re.compile(r'''[^0-9]+''')

_unixTsRe = re.compile(r'''[^0-9]*([0-9]+)[^0-9]*''')

def unixTimestamp(ts):
    """Extract a unix timestamp from a string."""
    match = _unixTsRe.match(str(ts))
    return datetime.datetime.fromtimestamp(int(match.group(1))) if match is not None else None

def utf8(s):
    """Easy str-to-utf8 utility function."""
    try:
        return unicode(s).encode('utf-8')
    except UnicodeDecodeError:
        return s.decode('utf-8').encode('utf-8')


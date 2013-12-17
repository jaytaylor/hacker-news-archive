#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""HackerNews models."""

from bs4 import BeautifulSoup
from .text import utf8, integerRe


class ItemLog(object):
    """Keep track of points and comments for an item by timestamp."""
    def __init__(self, ts, points, comments):
        self.ts = ts
        self.points = points
        self.comments = comments

    def __str__(self):
        return '<ItemLog ts={0} points={1} comments={2}'.format(self.ts, self.points, self.comments)


class Item(object):
    """HN item."""
    def __init__(self, id, title, url):
        self.id = id
        self.title = utf8(title)
        self.url = url
        self.log = []

    def __str__(self):
        return '<Item id={0} title="{1}" url={2}>'.format(self.id, utf8(self.title), utf8(self.url))

    def maxPoints(self):
        return max(map(lambda l: l.points, self.log))

    def maxComments(self):
        return max(map(lambda l: l.comments, self.log))


def _commentFilterFn(tag):
    """Returns true only if the tag is a good candidate for an HN comment/discussion link."""
    if not tag.has_attr('href') or not tag.attrs['href'].startswith('item?id='):
        return False
    text = tag.get_text().strip()
    return text.endswith(' comments') or text.endswith(' comment') or text == 'discuss'

class Snapshot(object):
    """HN Snapshot."""
    def __init__(self, ts, data):
        self.ts = ts
        self.data = data

    def items(self):
        """Parse out the items from an HN webpage snapshot."""
        items = []
        soup = BeautifulSoup(self.data)
        itemNodes = soup.select('td.title > a')
        for node in itemNodes:
            if node.parent is not None and node.parent.parent is not None and node.parent.parent.next_sibling is not None:
                commentNode = node.parent.parent.next_sibling
                #print unicode(node)
                #print node.get_text()
                comments = commentNode.find(_commentFilterFn)
                if comments:
                    itemId = int(comments.attrs.get('href', '').replace('item?id=', ''))
                    numComments = int(integerRe.sub('', comments.get_text())) if comments.get_text() != 'discuss' else 0
                    numPoints = int(integerRe.sub('', commentNode.select('td.subtext span')[0].get_text()))
                    nodeLink = node.parent.find('a')
                    url = nodeLink.attrs.get('href', '')
                    title = nodeLink.get_text()
                    items.append(Item(itemId, title, url))
                    items[-1].log.append(ItemLog(self.ts, numPoints, numComments))
                #else:
                #    print ':(',node.get_text(), node.parent.parent.next_sibling.get_text()
                #    print comments
        return items


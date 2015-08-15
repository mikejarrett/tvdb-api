#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import urllib2

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from common import BaseClass


class SearchSeries(BaseClass):

    SeriesName = ''
    id = ''

    def __init__(self, data):
        self.raw_data = data
        self.update(**data)

    def __str__(self):
        return "<SearchSeries: {} - {}>".format(self.SeriesName, self.id)


class SearchResult(object):

    def __init__(self, query, root_node):
        self.query = query
        self.results = self._parse(root_node)
        self.hits = len(self.results)

    def _parse(self, root):
        result = []
        for elem in root.iterfind('Series'):
            parsed = {child.tag: child.text for child in elem.getchildren()}
            if parsed:
                result.append(SearchSeries(parsed))
        return result

    def __str__(self):
        return "<SearchResult: {}>".format(self.query)

    def __repr__(self):
        return self.__unicode__()

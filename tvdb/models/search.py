# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .common import BaseClass


class SearchSeries(BaseClass):

    SeriesName = ''
    _series = None
    id = ''

    def __init__(self, tvdb_class, data):
        self._tvdb_class = tvdb_class
        self.raw_data = data
        self.update(**data)

    def __str__(self):  # pragma: no cover
        return "<SearchSeries: {} - {}>".format(self.SeriesName, self.id)

    def __repr__(self):  # pragma: no cover
        return self.__str__()

    @property
    def series(self):
        if getattr(self, '_series', None) is None:
            self._series = self._tvdb_class.series(self.id)
        return self._series


class SearchResult(object):

    def __init__(self, tvdb_class, query, root_node):
        self._tvdb_class = tvdb_class
        self.query = query
        self.results = self._parse_series(root_node)
        self.hits = len(self.results)

    def _parse_series(self, root):
        result = []
        for elem in root.iterfind('Series'):
            parsed = {child.tag: child.text for child in elem.getchildren()}
            if parsed:
                result.append(SearchSeries(self._tvdb_class, parsed))
        return result

    def __str__(self):  # pragma: no cover
        return "<SearchResult: {}>".format(self.query)

    def __repr__(self):  # pragma: no cover
        return self.__str__()

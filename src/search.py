#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""
from __future__ import unicode_literals

import urllib2

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

API_KEY = 'D8CA5C3C42F8B120'
BASE_URL = 'http://thetvdb.com/api'


class SearchSeries(object):

    def __init__(self, data):
        self.raw_data = data

        self.alias_name = data.get('AliasNames', '')
        self.first_aired = data.get('FirstAired', '')
        self.imdb_id = data.get('IMDB_ID', '')
        self.network = data.get('Network', '')
        self.overview = data.get('Overview', '')
        self.series_name = data.get('SeriesName', '')
        self.banner = data.get('banner', '')
        self.id = data.get('id', '')
        self.language = data.get('language', '')
        self.seriesid = data.get('seriesid', '')

    def __unicode__(self):
        return "<SearchSeries: {} - {}>".format(self.series_name, self.id)

    def __repr__(self):
        return self.__unicode__()


class SearchResult(object):

    def __init__(self, query, data):
        self.query = query
        root = ET.fromstring(data)
        self.results = self._parse(root)
        self.hits = len(self.results)

    def _parse(self, root):
        result = []
        for elem in root.iterfind('Series'):
            parsed = {child.tag: child.text for child in elem.getchildren()}
            if parsed:
                result.append(SearchSeries(parsed))
        return result

    def __unicode__(self):
        return "<SearchResult: {}>".format(self.query)

    def __repr__(self):
        return self.__unicode__()


def search(query):
    query = urllib2.quote(query)
    url = '{}/GetSeries.php?seriesname={}'.format(BASE_URL, query)
    try:
        result = urllib2.urlopen(url)
        data = result.read()
        result.close()
    except Exception as err:
        data = ''
    return SearchResult(query, data)

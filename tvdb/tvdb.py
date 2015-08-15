#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import BaseClass

from search import SearchResult

from series import Episode
from series import Season
from series import Series


API_KEY = 'D8CA5C3C42F8B120'
BASE_URL = 'http://thetvdb.com/api'
SERIES_URL = 'http://thetvdb.com/api/{api_key}/series/{series_id}/all'


class TVDB(class):

    @staticmethod
    def _get(url):
        try:
            result = urllib2.urlopen(url)
            data = result.read()
            result.close()
        except Exception as err:
            data = ''

        return data

    @classmethod
    def search(cls, query):
        query = urllib2.quote(query)
        url = '{}/GetSeries.php?seriesname={}'.format(BASE_URL, query)
        data = cls._get(url)
        root_node = ET.fromstring(data)
        return SearchResult(query, root_node)

    @classmethod
    def series(series_id):
        url = SERIES_URL.format(**{'api_key': API_KEY, 'series_id': series_id})
        data = get(url)
        root_node = ET.fromstring(data)
        return Seriesl(root_node)

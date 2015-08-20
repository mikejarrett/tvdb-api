# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
	import urllib.request as urllib2
except ImportError:
	import urllib2

try:
    import xml.etree.cElementTree as ET
except ImportError:  # pragma: no cover
    import xml.etree.ElementTree as ET

from models.search import SearchResult
from models.series import Series
from . import settings


class TVDB(object):

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
        url = '{}/GetSeries.php?seriesname={}'.format(settings.BASE_URL, query)
        data = cls._get(url)
        root_node = ET.fromstring(data)
        return SearchResult(cls, query, root_node)

    @classmethod
    def series(cls, series_id):
        url = settings.SERIES_URL.format(
            api_key=settings.API_KEY,
            series_id=series_id
        )
        data = cls._get(url)
        root_node = ET.fromstring(data)
        return Series(root_node)

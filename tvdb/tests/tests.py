# -*- coding: utf-8 -*-

import mock
import unittest

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from tvdb import TVDB as tvdb
from tvdb.models.search import SearchResult, SearchSeries


SEARCH_DATA_PARSED = {
    'FirstAired': '1989-12-17',
    'IMDB_ID': 'tt0096697',
    'Network': 'FOX (US)',
    'Overview': 'Set in Springfield...',
    'SeriesName': 'The Simpsons',
    'banner': 'graphical/71663-g24.jpg',
    'id': '71663',
    'language': 'en',
    'seriesid': '71663',
    'zap2it_id': 'EP00018693'
}

SEARCH_DATA_XML = """
<Data>
    <Series>
        <seriesid>71663</seriesid>
        <language>en</language>
        <SeriesName>The Simpsons</SeriesName>
        <banner>graphical/71663-g24.jpg</banner>
        <Overview>Set in Springfield...</Overview>
        <FirstAired>1989-12-17</FirstAired>
        <Network>FOX (US)</Network>
        <IMDB_ID>tt0096697</IMDB_ID>
        <zap2it_id>EP00018693</zap2it_id>
        <id>71663</id>
    </Series>
</Data>
"""


class TestTVDB(unittest.TestCase):

    def setUp(self):
        self.mock_urlopen = mock.patch('tvdb.tvdb.urllib2.urlopen').start()
        self.mock_et = mock.patch('tvdb.tvdb.ET').start()
        self.mock_search_result = mock.patch('tvdb.tvdb.SearchResult').start()
        self.mock_series = mock.patch('tvdb.tvdb.Series').start()

        self.returned_xml = '<Some>XML Data</Some>'

        self.mock_urlopen_result = mock.Mock()
        self.mock_urlopen_result.read.return_value = self.returned_xml
        self.mock_urlopen.return_value = self.mock_urlopen_result

    def tearDown(self):
        self.mock_urlopen.stop()
        self.mock_et.stop()
        self.mock_search_result.stop()
        self.mock_series.stop()

    def test_get_urlopen(self):
        url = 'http://some.url.com'
        ret_val = tvdb._get(url)

        self.assertEqual(ret_val, self.returned_xml)
        self.mock_urlopen.assert_called_once_with(url)
        self.assertEqual(self.mock_urlopen_result.close.call_count, 1)

    def test_get_urlopen_with_exception(self):
        self.assertEqual(1, 0)

    def test_search(self):
        tvdb.search('The Simpsons')
        self.mock_et.fromstring.assert_called_once_with(self.returned_xml)
        self.mock_search_result.assert_called_once_with(
            tvdb,
            'The%20Simpsons',
            self.mock_et.fromstring.return_value
        )

    def test_series(self):
        tvdb.series('71663')
        self.mock_et.fromstring.assert_called_once_with(self.returned_xml)
        self.mock_series.assert_called_once_with(
            self.mock_et.fromstring.return_value
        )


class TestSearchSeries(unittest.TestCase):

    def setUp(self):
        self.data = {
            'SeriesName': 'The Simpsons',
            'id': '71663',
        }

    def test_series_property(self):
        mock_tvdb = mock.Mock(spec_set=tvdb)
        search_series = SearchSeries(mock_tvdb, self.data)

        # Make sure the `series` property is lazily evaluated
        self.assertEqual(mock_tvdb.series.call_count, 0)
        self.assertIsNone(search_series._series)

        self.assertEqual(search_series.raw_data, self.data)
        self.assertEqual(search_series.SeriesName, 'The Simpsons')
        self.assertEqual(search_series.id, '71663')

        self.assertIsNotNone(search_series.series)
        self.assertEqual(mock_tvdb.series.call_count, 1)
        self.assertIsNotNone(search_series._series)
        mock_tvdb.series.assert_called_once_with('71663')


class TestSearchResult(unittest.TestCase):

    def setUp(self):
        pass

    def test_parse_series(self):
        root_node = ET.fromstring(SEARCH_DATA_XML)
        search_result = SearchResult(tvdb, 'The Simpsons', root_node)

        self.assertEqual(search_result.hits, 1)
        self.assertEqual(search_result.query, 'The Simpsons')

        search_series = search_result.results[0]
        self.assertEqual(search_series.raw_data, SEARCH_DATA_PARSED)

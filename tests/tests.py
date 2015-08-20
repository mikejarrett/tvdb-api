# -*- coding: utf-8 -*-
# pylint: disable=no-name-in-module
from __future__ import unicode_literals

import mock
import unittest

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from tvdb import TVDB as tvdb
from tvdb import models
from tvdb import settings
from .data import (
    EPISODE_DATA_PARSED,
    SEARCH_DATA_PARSED,
    SEARCH_DATA_XML,
    SEASON_DATA_PARSED,
    SEASON_EPISODE_DATA_XML,
    SERIES_DATA_PARSED
)


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

    @mock.patch('tvdb.tvdb.urllib2.urlopen')
    def test_get_urlopen_with_httperror(self, mock_urlopen):
        mock_urlopen.side_effect = urllib2.HTTPError(
            'http://url.com',
            code=404,
            msg="Not Found",
            hdrs='',
            fp=None,
        )
        ret_val = tvdb._get('http://url.com')
        self.assertEqual(ret_val, '')

    @mock.patch('tvdb.tvdb.urllib2.urlopen')
    def test_get_urlopen_with_urlerror(self, mock_urlopen):
        mock_urlopen.side_effect = urllib2.URLError('Error Reason')
        ret_val = tvdb._get('http://url.com')
        self.assertEqual(ret_val, '')

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
        search_series = models.SearchSeries(mock_tvdb, self.data)

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

    def test_parse_series(self):
        root_node = ET.fromstring(SEARCH_DATA_XML)
        search_result = models.SearchResult(tvdb, 'The Simpsons', root_node)

        self.assertEqual(search_result.hits, 1)
        self.assertEqual(search_result.query, 'The Simpsons')

        search_series = search_result.results[0]
        self.assertEqual(search_series.raw_data, SEARCH_DATA_PARSED)


class TestSeriesEpisode(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        root_node = ET.fromstring(SEASON_EPISODE_DATA_XML)
        self.series = models.Series(root_node)

    def test_series_init(self):
        self.assertTrue('season_4' in self.series)
        self.assertTrue('raw_data' in self.series)

        # Throw away data not needed for this test
        self.series.pop('season_4')
        self.series.pop('raw_data')

        self.assertEqual(self.series.__dict__, SERIES_DATA_PARSED)

    def test_series_thumbnail(self):
        expected = settings.THUMBNAILS_URL.format(thumbnail=self.series.banner)
        self.assertEqual(self.series.thumbnail, expected)

    def test_series_without_banner(self):
        self.series.pop('banner')
        self.assertEqual(self.series.thumbnail, '')

    def test_series_seasons(self):
        seasons = [season for season in self.series.seasons]
        self.assertEqual(len(seasons), 1)
        season = self.series.season_4
        self.assertEqual(seasons[0].season_number, season.season_number)

    def test_season_init(self):
        self.assertTrue('season_4' in self.series)
        season = self.series.season_4

        self.assertTrue('episode_19' in season.__dict__)
        season.pop('episode_19')

        self.assertEqual(season.__dict__, SEASON_DATA_PARSED)

    def test_season_episodes(self):
        season = self.series.season_4
        episodes = [episode for episode in season.episodes]
        self.assertEqual(len(episodes), 1)
        self.assertEqual(episodes[0].EpisodeName, 'The Front')

    def test_episode_init(self):
        episode = self.series.season_4.episode_19
        self.assertEqual(episode.__dict__, EPISODE_DATA_PARSED)

    def test_episode_thumbnail(self):
        episode = self.series.season_4.episode_19
        expected = settings.THUMBNAILS_URL.format(thumbnail=episode.filename)
        self.assertEqual(episode.thumbnail, expected)

# -*- coding: utf-8 -*-
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

SEASON_EPISODE_DATA_XML = """
<Data>
    <Series>
        <id>71663</id>
        <Actors>Dan Castellaneta</Actors>
        <Airs_DayOfWeek>Sunday</Airs_DayOfWeek>
        <Airs_Time>8:00 PM</Airs_Time>
        <ContentRating>TV-PG</ContentRating>
        <FirstAired>1989-12-17</FirstAired>
        <Genre>|Animation|Comedy|</Genre>
        <IMDB_ID>tt0096697</IMDB_ID>
        <Language>en</Language>
        <Network>FOX (US)</Network>
        <NetworkID/>
        <Overview>Set in Springfield...</Overview>
        <Rating>9.0</Rating>
        <RatingCount>573</RatingCount>
        <Runtime>30</Runtime>
        <SeriesID>146</SeriesID>
        <SeriesName>The Simpsons</SeriesName>
        <Status>Continuing</Status>
        <added/>
        <addedBy/>
        <banner>graphical/71663-g24.jpg</banner>
        <fanart>fanart/original/71663-31.jpg</fanart>
        <lastupdated>1440075183</lastupdated>
        <poster>posters/71663-10.jpg</poster>
        <tms_wanted_old>1</tms_wanted_old>
        <zap2it_id>EP00018693</zap2it_id>
    </Series>
    <Episode>
        <id>55529</id>
        <Combined_episodenumber>19.0</Combined_episodenumber>
        <Combined_season>4</Combined_season>
        <DVD_chapter/>
        <DVD_discid/>
        <DVD_episodenumber>19.0</DVD_episodenumber>
        <DVD_season>4</DVD_season>
        <Director>Rich Moore</Director>
        <EpImgFlag>1</EpImgFlag>
        <EpisodeName>The Front</EpisodeName>
        <EpisodeNumber>19</EpisodeNumber>
        <FirstAired>1993-04-15</FirstAired>
        <GuestStars>Brooke Shields</GuestStars>
        <IMDB_ID/>
        <Language>en</Language>
        <Overview>Convinced that Itchy &amp; Scratchy...</Overview>
        <ProductionCode>9F16</ProductionCode>
        <Rating>7.4</Rating>
        <RatingCount>36</RatingCount>
        <SeasonNumber>4</SeasonNumber>
        <Writer>Adam I. Lapidus</Writer>
        <absolute_number>78</absolute_number>
        <filename>episodes/71663/55529.jpg</filename>
        <lastupdated>1386023580</lastupdated>
        <seasonid>2738</seasonid>
        <seriesid>71663</seriesid>
        <thumb_added/>
        <thumb_height>300</thumb_height>
        <thumb_width>400</thumb_width>
    </Episode>
</Data>
"""

SEASON_DATA_PARSED = {
    'SeriesName': 'The Simpsons',
    'season_number': '4',
}

SERIES_DATA_PARSED = {
    'SeriesID': '146',
    'Network': 'FOX (US)',
    'IMDB_ID': 'tt0096697',
    'Actors': 'Dan Castellaneta',
    'id': '71663',
    'Status': 'Continuing',
    'Airs_Time': '8:00 PM',
    'fanart': 'fanart/original/71663-31.jpg',
    'lastupdated': '1440075183',
    'FirstAired': '1989-12-17',
    'RatingCount': '573',
    'Genre': '|Animation|Comedy|',
    'added': None,
    'Language': 'en',
    'Airs_DayOfWeek': 'Sunday',
    'tms_wanted_old': '1',
    'poster': 'posters/71663-10.jpg',
    'ContentRating': 'TV-PG',
    'addedBy': None,
    'SeriesName': 'The Simpsons',
    'Runtime': '30',
    'banner': 'graphical/71663-g24.jpg',
    'NetworkID': None,
    'Rating': '9.0',
    'zap2it_id': 'EP00018693',
    'Overview': 'Set in Springfield...',
    '_seasons': ['season_4'],
}

EPISODE_DATA_PARSED = {
    'Combined_episodenumber': '19.0',
    'Combined_season': '4',
    'DVD_chapter': None,
    'DVD_discid': None,
    'DVD_episodenumber': '19.0',
    'DVD_season': '4',
    'Director': 'Rich Moore',
    'EpImgFlag': '1',
    'EpisodeName': 'The Front',
    'EpisodeNumber': '19',
    'FirstAired': '1993-04-15',
    'GuestStars': 'Brooke Shields',
    'IMDB_ID': None,
    'Language': 'en',
    'Overview': 'Convinced that Itchy & Scratchy...',
    'ProductionCode': '9F16',
    'Rating': '7.4',
    'RatingCount': '36',
    'SeasonNumber': '4',
    'SeriesName': 'The Simpsons',
    'Writer': 'Adam I. Lapidus',
    'absolute_number': '78',
    'filename': 'episodes/71663/55529.jpg',
    'id': '55529',
    'lastupdated': '1386023580',
    'seasonid': '2738',
    'seriesid': '71663',
    'thumb_added': None,
    'thumb_height': '300',
    'thumb_width': '400'
}

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

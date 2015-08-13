#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""
from __future__ import unicode_literals

from collections import defaultdict, MutableMapping
import urllib2

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

API_KEY = 'D8CA5C3C42F8B120'
SERIES_URL = 'http://thetvdb.com/api/{api_key}/series/{series_id}/all'


class BaseClass(MutableMapping):

    def __init__(self, *args, **kwargs):
        self.__dict__.update(*args, **kwargs)

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

    def __delitem__(self, key):
        del self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    # def __str__(self):
    #     '''returns simple dict representation of the mapping'''
    #     return str(self.__dict__)

    # def __repr__(self):
    #     '''echoes class, id, & reproducible representation in the REPL'''
    #     return '{}, Episode({})'.format(super(D, self).__repr__(),
    #                               self.__dict__)


class Season(BaseClass):

    def __iter__(self):
        return iter(self.episodes)

    @property
    def episodes(self):
        for key in sorted(self.__dict__.iterkeys()):
            if key.startswith('episode_'):
                episode = getattr(self, key, None)
                if episode:
                    yield episode

    def __str__(self):
        return '<Season: {} ({})>'.format(self.season_number, self.SeriesName)

    def __repr__(self):
        return self.__str__()


class Episode(BaseClass):

    EpisodeNumber = ''
    SeriesName = ''
    SeasonNumber = ''

    def __str__(self):
        return '<Episode: {} ({} - Season {})>'.format(
            self.EpisodeNumber,
            self.SeriesName,
            self.SeasonNumber,
        )

    def __repr__(self):
        return self.__str__()


class Series(BaseClass):

    SeriesName = ''

    def __init__(self, series_id):
        url = SERIES_URL.format(**{'api_key': API_KEY, 'series_id': series_id})
        try:
            result = urllib2.urlopen(url)
            data = result.read()
            result.close()
        except Exception as err:
            data = ''

        root = ET.fromstring(data)

        series_info = self._get_series_info(root)
        self.raw_data = series_info
        self.__dict__.update(**series_info)

        seasons_info = self._get_seasons_info(root)
        self.__dict__.update(**seasons_info)

        self.__dict__['_seasons'] = sorted(seasons_info.keys())

    def __iter__(self):
        return iter(self.seasons)

    @property
    def seasons(self):
        for key in self._seasons:
            season = getattr(self, key, None)
            if season:
                yield season

    def _get_series_info(self, root):
        data = {}
        for elem in root.iterfind('Series'):
            data = {child.tag: child.text for child in elem.getchildren()}
        return data

    def _get_seasons_info(self, root):
        seasons = defaultdict(Season)
        for elem in root.iterfind('Episode'):
            parsed = {child.tag: child.text for child in elem.getchildren()}
            if parsed and 'SeasonNumber' and 'EpisodeNumber' in parsed:
                season_number = parsed['SeasonNumber']
                season_number_str = 'season_{}'.format(season_number)
                episode_number = 'episode_{}'.format(parsed['EpisodeNumber'])

                parsed['SeriesName'] = self.SeriesName

                seasons[season_number_str].__dict__.update({
                    episode_number: Episode(**parsed),
                    'season_number': season_number,
                    'SeriesName': self.SeriesName,
                })
        return seasons

    def __len__(self):
        return len(self.seasons)

    def __str__(self):
        return '<Series: {}>'.format(self.SeriesName)

    def __repr__(self):
        return self.__str__()


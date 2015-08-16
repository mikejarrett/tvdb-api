#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import defaultdict

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from .common import BaseClass


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

    def __init__(self, root):
        self.SeriesName = ''

        series_info = self._get_series_info(root)
        self.raw_data = series_info
        self.update(**series_info)

        seasons_info = self._get_seasons_info(root)
        self.update(**seasons_info)

        self._seasons = sorted(seasons_info.keys())

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

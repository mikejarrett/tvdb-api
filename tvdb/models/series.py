# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
from __future__ import unicode_literals

from collections import defaultdict

from tvdb.models import BaseClass
from tvdb.models.mixins import ThumbnailMixin


class Episode(BaseClass, ThumbnailMixin):

    EpisodeNumber = ''
    SeriesName = ''
    SeasonNumber = ''

    def __str__(self):  # pragma: no cover
        return '<Episode: {} ({} - Season {})>'.format(
            self.EpisodeNumber,
            self.SeriesName,
            self.SeasonNumber,
        )

    def __repr__(self):  # pragma: no cover
        return self.__str__()


class Series(BaseClass, ThumbnailMixin):

    def __init__(self, root, *args, **kwargs):
        super(Series, self).__init__(*args, **kwargs)
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

    @staticmethod
    def _get_series_info(root):
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

                seasons[season_number_str].update({
                    episode_number: Episode(**parsed),
                    'season_number': season_number,
                    'SeriesName': self.SeriesName,
                })
        return seasons

    def __len__(self):
        return len(self.seasons)

    def __str__(self):  # pragma: no cover
        return '<Series: {}>'.format(self.SeriesName)

    def __repr__(self):  # pragma: no cover
        return self.__str__()


class Season(BaseClass):

    _episodes = []

    def _populate_episodes(self):
        for season_number in sorted(self.keys()):
            if season_number.startswith('episode_'):
                self._episodes.append(season_number)
        self._episodes = sorted(self._episodes)

    @property
    def episodes(self):
        if not self._episodes:
            self._populate_episodes()

        for key in self._episodes:
            episode = getattr(self, key, None)
            if episode:
                yield episode

    def __str__(self):  # pragma: no cover
        return '<Season: {} ({})>'.format(self.season_number, self.SeriesName)

    def __repr__(self):  # pragma: no cover
        return self.__str__()

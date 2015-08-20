# -*- coding: utf-8 -*-
from __future__ import unicode_literals


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

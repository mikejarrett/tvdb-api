# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from tvdb import settings


class ThumbnailMixin(object):

    @property
    def thumbnail(self):
        if 'filename' in self:
            thumbnail = settings.THUMBNAILS_URL.format(thumbnail=self.filename)
        elif 'banner' in self:
            thumbnail = settings.THUMBNAILS_URL.format(thumbnail=self.banner)
        else:
            thumbnail = ''

        return thumbnail

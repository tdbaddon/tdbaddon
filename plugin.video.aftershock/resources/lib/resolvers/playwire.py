# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2015 IDev

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import json

from resources.lib.libraries import client
from resources.lib.libraries import logger

def resolve(url):
    try:
        result = client.source(url)
        data = json.loads(result)
        try :
            publisherId = data['publisherId']
            hostingId = data['hostingId']
            videoId = data['content']['videoId']

        except:
            publisherId = data['settings']['publisherId']
            hostingId = data['settings']['hostingId']
            videoId = data['settings']['videoId']

        url = 'https://cdn.video.playwire.com/%s/videos/%s/video-sd.mp4?hosting_id=%s' % (publisherId, videoId, hostingId)
        logger.debug('%s URL [%s]' % (__name__, url))
        return url
    except:
        return
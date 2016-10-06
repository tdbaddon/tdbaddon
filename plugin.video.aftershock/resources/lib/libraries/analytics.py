# -*- coding: utf-8 -*-

'''
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


import xbmc, uuid, base64, json, urllib

from resources.lib.libraries import control
from resources.lib.libraries import client
from resources.lib.libraries import cache
from resources.lib.libraries import logger

def sendAnalytics(screenName):
    try :
        if not (control.setting('analytics.enabled') == 'true' or 'Installed' in screenName):
            raise Exception()
        guid = cache.get(getGuid, 600000000, control.addonInfo('version'), table='changelog')
        url = base64.urlsafe_b64decode("aHR0cDovL3d3dy5nb29nbGUtYW5hbHl0aWNzLmNvbS9jb2xsZWN0")
        version = control.addonInfo('version')
        post = base64.urlsafe_b64decode("eyJ2IjoiMSIsInQiOiJzY3JlZW52aWV3IiwidGlkIjoiVUEtNzQ2Mzg0NjQtMSIsImFuIjoiQWZ0ZXJzaG9jay1Lb2RpIiwiYXYiOiIlcyIsImNpZCI6IiVzIiwiY2QiOiIlcyJ9") % (version, guid, screenName)
        post = urllib.urlencode(json.loads(post))
        client.request(url, post=post)
        logger.debug('Sent Analytics for [%s]' % screenName)
        return '1'
    except:
        logger.debug('Analytics disabled for [%s]' % screenName)
        return '1'
        pass

def getGuid(version):
    guid = uuid.uuid4()
    return str(guid)
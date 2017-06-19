# -*- coding: utf-8 -*-

"""
    Exodus Add-on
    Copyright (C) 2016 Exodus

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
"""

import json
import re
import urllib
import urlparse

from resources.lib.modules import client
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['video4k.to']
        self.base_link = 'http://video4k.to'
        self.request_link = '/request'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            return urllib.urlencode({'mID': re.sub('[^0-9]', '', imdb)})
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            return urllib.urlencode({'mID': re.sub('[^0-9]', '', imdb)})
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return

            return urllib.urlencode({'mID': re.sub('[^0-9]', '', imdb), 'season': season, 'episode': episode})
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if url == None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            data.update({'raw': 'true', 'language': 'de'})
            data = urllib.urlencode(data)
            data = client.request(urlparse.urljoin(self.base_link, self.request_link), post=data)
            data = json.loads(data)
            data = [i[1] for i in data[1].items()]
            data = [(i['name'].lower(), i['links']) for i in data]

            for host, links in data:
                valid, host = source_utils.is_host_valid(host, hostDict)
                if not valid: continue

                for link in links:
                    try:sources.append({'source': host, 'quality': 'SD', 'language': 'de', 'url': link['URL'], 'direct': False, 'debridonly': False})
                    except: pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

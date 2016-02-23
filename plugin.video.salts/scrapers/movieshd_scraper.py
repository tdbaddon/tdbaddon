"""
    SALTS XBMC Addon
    Copyright (C) 2014 tknorris

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
import re
import urllib
import urlparse

from salts_lib import kodi
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://movieshd.eu'

class MoviesHD_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'MoviesHD'

    def resolve_link(self, link):
        if 'videomega' in link:
            html = self._http_get(link, cache_limit=.5)
            match = re.search('ref="([^"]+)', html)
            if match:
                return 'http://videomega.tv/iframe.php?ref=%s' % (match.group(1))
        else:
            return link

    def format_source_label(self, item):
        return '[%s] %s' % (item['quality'], item['host'])

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)

            match = re.search("(?:'|\")([^'\"]+hashkey=[^'\"]+)", html)
            stream_url = ''
            if match:
                stream_url = match.group(1)
                if stream_url.startswith('//'): stream_url = 'http:' + stream_url
                host = 'videomega.tv'
            else:
                match = re.search('iframe[^>]*src="([^"]+)', html)
                if match:
                    stream_url = match.group(1)
                    host = urlparse.urlparse(stream_url).hostname
                    
                if stream_url:
                    hoster = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': QUALITIES.HD720, 'views': None, 'rating': None, 'up': None, 'down': None, 'direct': False}
                    hosters.append(hoster)
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year):
        search_url = urlparse.urljoin(self.base_url, '/?s=')
        search_url += urllib.quote_plus(title)
        html = self._http_get(search_url, cache_limit=.25)
        results = []
        if not re.search('nothing matched your search criteria', html, re.I):
            pattern = 'href="([^"]+)"\s+title="([^"]+)\s+\((\d{4})\)'
            for match in re.finditer(pattern, html):
                url, title, match_year = match.groups('')
                if not year or not match_year or year == match_year:
                    result = {'url': scraper_utils.pathify_url(url), 'title': title, 'year': match_year}
                    results.append(result)
        return results

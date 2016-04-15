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

from salts_lib import dom_parser
from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'https://ganool.ag'

class Ganool_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'Ganool'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        if item['views'] is not None: label += ' (%s Views)' % (item['views'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            q_str = 'HDRIP'
            match = re.search('<p\s+rel="tag">Quality:\s*(.*?)</p>', html, re.I)
            if match:
                q_str = match.group(1)

            stream_url = self.__decode(html)
            if stream_url:
                host = urlparse.urlparse(stream_url).hostname
                quality = scraper_utils.blog_get_quality(video, q_str, host)
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
                hosters.append(hoster)

        return hosters

    def __decode(self, html):
        fragment = dom_parser.parse_dom(html, 'div', {'id': 'watchonlinearea\d*'})
        if fragment:
            match = re.search('var\s+s\s*=\s*"([^"]+)', fragment[0])
            source = ''
            if match:
                for c in match.group(1):
                    if ord(c) == 28:
                        source += '&'
                    elif ord(c) == 23:
                        source += '!'
                    else:
                        source += chr(ord(c) - 1)
                
                match = re.search('<iframe[^>]+src="([^"]+)', source, re.I)
                if match:
                    return match.group(1)
    
    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year, season=''):
        results = []
        search_title = re.sub(r'[^a-zA-Z0-9\s]+', ' ', title).lower().strip()
        search_title = re.sub('\s+', ' ', search_title)
        search_url = urlparse.urljoin(self.base_url, '/?s=%s' % (urllib.quote_plus(search_title)))
        html = self._http_get(search_url, cache_limit=1)
        for item in dom_parser.parse_dom(html, 'div', {'id': 'homepost_\d+'}):
            match = re.search('href="([^"]+)[^>]*title="([^"]+)', item)
            if match:
                match_url, match_title_year = match.groups()
                match = re.search('(.*?)(?:\s+\(?(\d{4})\)?)\s*(.*)', match_title_year)
                if match:
                    match_title, match_year, extra = match.groups()
                    match_title += ' [%s]' % (extra)
                else:
                    match_title = match_title_year
                    match_year = ''
                    extra = ''
                
                if not year or not match_year or year == match_year:
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)

        return results

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
import scraper
import urllib
import urlparse
import re
from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import dom_parser
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES

BASE_URL = 'http://moviesonline7.co'
BUY_VIDS_URL = '/includes/buyVidS.php?vid=%s&num=%s'
QUALITY_MAP = {'BRRIP1': QUALITIES.HIGH, 'BRRIP2': QUALITIES.HD720, 'BRRIP3': QUALITIES.MEDIUM, 'BRRIP4': QUALITIES.HD720,
               'DVDRIP1': QUALITIES.HIGH, 'DVDRIP2': QUALITIES.HIGH, 'DVDRIP3': QUALITIES.HIGH,
               'CAM1': QUALITIES.LOW, 'CAM2': QUALITIES.LOW}

class MO7_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'MoviesOnline7'

    def resolve_link(self, link):
        html_url = self._http_get(link, cache_limit=.5)
        if html_url:
            html = self._http_get(html_url, cache_limit=.5)
            match = re.search("'file'\s*,\s*'([^']+)", html)
            if match:
                host = urlparse.urlparse(html_url).hostname
                stream_url = 'http://' + host + match.group(1)
                return stream_url
            else:
                match = re.search('<source\s+src="([^"]+)', html)
                if match:
                    host = urlparse.urlparse(html_url).hostname
                    stream_url = 'http://' + host + match.group(1)
                    return stream_url

    def format_source_label(self, item):
        return '[%s] %s' % (item['quality'], item['host'])

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            html = html.decode('utf-8', 'ignore')
            fragment = dom_parser.parse_dom(html, 'div', {'class': 'list-wrap'})
            if fragment:
                for stream_url in dom_parser.parse_dom(fragment[0], 'iframe', ret='src'):
                    host = urlparse.urlparse(stream_url).hostname
                    hoster = {'multi-part': False, 'host': host, 'url': stream_url, 'class': self, 'rating': None, 'views': None, 'quality': QUALITIES.HIGH, 'direct': True}
                    hosters.append(hoster)

        return hosters

    def get_url(self, video):
        return super(MO7_Scraper, self)._default_get_url(video)

    def search(self, video_type, title, year):
        results = []
        search_url = urlparse.urljoin(self.base_url, '/search.php?stext=')
        search_url += urllib.quote_plus(title)
        html = self._http_get(search_url, cache_limit=.25)
        for cell in dom_parser.parse_dom(html, 'table', {'class': 'boxed'}):
            url = dom_parser.parse_dom(cell, 'a', ret='href')
            match_title = dom_parser.parse_dom(cell, 'h3', {'class': 'title_grid'})
            if url and match_title:
                result = {'url': self._pathify_url(url[0]), 'title': match_title[0], 'year': ''}
                results.append(result)

        return results

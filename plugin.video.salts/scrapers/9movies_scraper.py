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
import time
import urllib
import urlparse

from salts_lib import dom_parser
from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://9movies.to'
HASH_URL = '/ajax/film/episode?hash_id=%s&f=&p=%s'
Q_MAP = {'TS': QUALITIES.LOW, 'CAM': QUALITIES.LOW, 'HDTS': QUALITIES.LOW, 'HD 720P': QUALITIES.HD720}
XHR = {'X-Requested-With': 'XMLHttpRequest'}

class NineMovies_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return '9Movies'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        sources = {}
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            for server_list in dom_parser.parse_dom(html, 'ul', {'class': 'episodes'}):
                for hash_id in dom_parser.parse_dom(server_list, 'a', ret='data-id'):
                    now = time.localtime()
                    url = urlparse.urljoin(self.base_url, HASH_URL)
                    url = url % (hash_id, now.tm_hour + now.tm_min)
                    html = self._http_get(url, headers=XHR, cache_limit=.5)
                    js_result = scraper_utils.parse_json(html, url)
                    if 'videoUrlHash' in js_result and 'grabber' in js_result:
                        query = {'flash': 1, 'json': 1, 's': now.tm_min, 'link': js_result['videoUrlHash'], '_': int(time.time())}
                        query['link'] = query['link'].replace('\/', '/')
                        grab_url = js_result['grabber'].replace('\/', '/')
                        grab_url += '?' + urllib.urlencode(query)
                        html = self._http_get(grab_url, headers=XHR, cache_limit=.5)
                        js_result = scraper_utils.parse_json(html, grab_url)
                        for result in js_result:
                            if 'label' in result:
                                quality = scraper_utils.height_get_quality(result['label'])
                            else:
                                quality = scraper_utils.gv_get_quality(result['file'])
                            sources[result['file']] = quality
                
            for source in sources:
                hoster = {'multi-part': False, 'host': self._get_direct_hostname(source), 'class': self, 'quality': sources[source], 'views': None, 'rating': None, 'url': source, 'direct': True}
                hosters.append(hoster)
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year):
        search_url = urlparse.urljoin(self.base_url, '/search?keyword=%s' % (urllib.quote_plus(title)))
        html = self._http_get(search_url, cache_limit=1)
        results = []
        match_year = ''
        fragment = dom_parser.parse_dom(html, 'ul', {'class': 'movie-list'})
        if fragment:
            for item in dom_parser.parse_dom(fragment[0], 'li'):
                if dom_parser.parse_dom(item, 'div', {'class': '[^"]*episode[^"]*'}): continue
                match = re.search('href="([^"]+).*?title="([^"]+)', item)
                if match:
                    match_url, match_title = match.groups()
                    if not year or not match_year or year == match_year:
                        result = {'title': match_title, 'year': '', 'url': scraper_utils.pathify_url(match_url)}
                        results.append(result)

        return results

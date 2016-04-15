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
import urlparse

from salts_lib import dom_parser
from salts_lib import kodi
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://www.movie-tube.co'

class MovieTube_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'MovieTube'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        if 'views' in item and item['views']:
            label += ' (%s views)' % item['views']
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            fragment = dom_parser.parse_dom(html, 'div', {'id': 'fstory-video'})
            if fragment:
                q_str = ''
                match = re.search('<span>([^<]+)', fragment[0])
                if match:
                    q_str = match.group(1)

                for match in re.finditer('<iframe[^>]*src="([^"]+)', fragment[0], re.I):
                    stream_url = match.group(1)
                    host = urlparse.urlparse(stream_url).hostname
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': scraper_utils.blog_get_quality(video, q_str, host), 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
                    hosters.append(hoster)
            
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year, season=''):
        results = []
        search_url = urlparse.urljoin(self.base_url, '/index.php?do=search')
        data = {'subaction': 'search', 'story': title, 'do': 'search'}
        headers = {'Referer': search_url}
        html = self._http_get(search_url, data=data, headers=headers, cache_limit=1)
        fragment = dom_parser.parse_dom(html, 'div', {'id': 'dle-content'})
        if fragment:
            for item in dom_parser.parse_dom(fragment[0], 'div', {'class': 'short-film'}):
                match = re.search('<h5><a\s+href="([^"]+)[^>]+title="([^"]+)', item)
                if match:
                    url, match_title = match.groups('')
                    result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(match_title), 'year': ''}
                    results.append(result)
        
        return results

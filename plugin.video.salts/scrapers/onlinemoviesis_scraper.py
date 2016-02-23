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


BASE_URL = 'http://onlinemovies.is'

class OnlineMoviesIs_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'OnlineMoviesIs'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        if item['views'] is not None:
            label += ' (%s Views)' % (item['views'])
        if item['rating'] is not None:
            label += ' (%s/100)' % (item['rating'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            q_str = ''
            match = re.search('>quality(.*?)<br\s*/>', html, re.I)
            if match:
                q_str = match.group(1)
                q_str = q_str.decode('utf-8').encode('ascii', 'ignore')
                q_str = re.sub('(</?strong[^>]*>|:|\s)', '', q_str, re.I | re.U)

            fragment = dom_parser.parse_dom(html, 'div', {'class': 'video-embed'})
            if fragment:
                for match in re.finditer('<iframe[^>]+src="([^"]+)', fragment[0], re.I):
                    stream_url = match.group(1)
                    host = urlparse.urlparse(stream_url).hostname
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': scraper_utils.blog_get_quality(video, q_str, host), 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
                    match = re.search('class="views-infos">(\d+).*?class="rating">(\d+)%', html, re.DOTALL)
                    if match:
                        hoster['views'] = int(match.group(1))
                        hoster['rating'] = match.group(2)
    
                    hosters.append(hoster)
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year):
        results = []
        test_url = title.replace("'", '')
        test_url = re.sub(r'[^a-zA-Z0-9\s]+', ' ', test_url).lower().strip()
        test_url = re.sub('\s+', ' ', test_url)
        test_url = test_url.replace(' ', '-')
        if year:
            test_url += '-%s' % (year)
        
        test_url = urlparse.urljoin(self.base_url, test_url)
        if self._http_get(test_url, cache_limit=1):
            result = {'title': title, 'year': year, 'url': scraper_utils.pathify_url(test_url)}
            results.append(result)

        return results

    def _http_get(self, url, data=None, cache_limit=8):
        headers = {'Referer': url}
        return self._cached_http_get(url, self.base_url, self.timeout, data=data, headers=headers, cache_limit=cache_limit)

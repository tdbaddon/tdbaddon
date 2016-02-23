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
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'https://beinmovie.com'
DETAIL_URL = '/movie-detail.php?%s'
PLAYER_URL = '/movie-player.php?%s'

QUALITY_MAP = {'HD': QUALITIES.HD720, 'FULL HD': QUALITIES.HD1080, 'DVD': QUALITIES.MEDIUM}
XHR = {'X-Requested-With': 'XMLHttpRequest'}

class BeinMovie_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'beinmovie'

    def resolve_link(self, link):
        if self.base_url in link:
            html = self._http_get(link, cache_limit=.5)
            match = re.search('<source\s+src="([^"]+)', html)
            if match and match.group(1) != 'nop':
                return match.group(1)
        else:
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
            html = self._http_get(url, headers=XHR, cache_limit=.5)
            
            fragment = dom_parser.parse_dom(html, 'div', {'class': '[^"]*movie_langs_list[^"]*'})
            if fragment:
                for match in re.finditer('href="([^"]+)', fragment[0]):
                    match = re.search('movie-player/(.*)', match.group(1))
                    if match:
                        player_url = urlparse.urljoin(self.base_url, PLAYER_URL % (match.group(1)))
                        html = self._http_get(player_url, cache_limit=.5)
                        match = re.search('<source\s+src="([^"]+)', html)
                        if match:
                            stream_url = match.group(1)
                            hoster = {'multi-part': False, 'url': stream_url, 'class': self, 'quality': scraper_utils.gv_get_quality(stream_url), 'host': self._get_direct_hostname(stream_url), 'rating': None, 'views': None, 'direct': True}
                            hosters.append(hoster)
                        
                        fragment2 = dom_parser.parse_dom(html, 'ul', {'class': 'servers'})
                        if fragment2:
                            for match in re.finditer('href="([^"]+).*?<span>(.*?)</span>', fragment2[0]):
                                other_url, quality = match.groups()
                                match = re.search('movie-player/(.*)', other_url)
                                if match:
                                    other_url = urlparse.urljoin(self.base_url, PLAYER_URL % (match.group(1)))
                                    if other_url == player_url: continue
                                    other_url += '|User-Agent=%s&X-Requested-With=XMLHttpRequest' % (scraper_utils.get_ua())
                                    hoster = {'multi-part': False, 'url': other_url, 'class': self, 'quality': QUALITY_MAP.get(quality, QUALITIES.HD720), 'host': self._get_direct_hostname(other_url), 'rating': None, 'views': None, 'direct': True}
                                    hosters.append(hoster)

        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year):
        search_url = urlparse.urljoin(self.base_url, '/movies-list.php?b=search&v=%s')
        search_url = search_url % (urllib.quote_plus(title))
        html = self._http_get(search_url, headers=XHR, cache_limit=0)
        results = []
        for movie in dom_parser.parse_dom(html, 'li', {'class': '[^"]*movie[^"]*'}):
            href = dom_parser.parse_dom(movie, 'a', ret='href')
            title = dom_parser.parse_dom(movie, 'h4')
            
            if href and title:
                match = re.search('movie-detail/(.*?)/', href[0])
                if match:
                    result = {'url': DETAIL_URL % (match.group(1)), 'title': title[0], 'year': ''}
                    results.append(result)
        return results

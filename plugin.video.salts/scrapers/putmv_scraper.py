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
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://putmv.com'
GVIDEO_NAMES = ['english sub', 'picasa']

class PutMV_Scraper(scraper.Scraper):
    base_url = BASE_URL
    
    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'PutMV'

    def resolve_link(self, link):
        if self._get_direct_hostname(link) == 'gvideo':
            return link
        else:
            for source in self.__get_links(link):
                return source

    def format_source_label(self, item):
        return '[%s] %s' % (item['quality'], item['host'])

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.5)
            fragment = dom_parser.parse_dom(html, 'ul', {'class': 'css_server_new'})
            if fragment:
                for match in re.finditer('href="([^"]+).*?/>(.*?)(?:-\d+)?</a>', fragment[0]):
                    url, host = match.groups()
                    host = host.lower()
                    if host in GVIDEO_NAMES:
                        sources = self.__get_links(urlparse.urljoin(self.base_url, url))
                        direct = True
                    else:
                        sources = {url: host}
                        direct = False
                    
                    for source in sources:
                        if self._get_direct_hostname(source) == 'gvideo':
                            quality = scraper_utils.gv_get_quality(source)
                        else:
                            quality = scraper_utils.get_quality(video, source, QUALITIES.HIGH)
                    
                        hoster = {'multi-part': False, 'host': sources[source], 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': source, 'direct': direct}
                        hosters.append(hoster)
            
        return hosters

    def __get_links(self, url):
        sources = {}
        html = self._http_get(url, cache_limit=.5)
        match = re.search('sources\s*:\s*\[(.*?)\]', html, re.DOTALL)
        if match:
            for match in re.finditer('''['"]*file['"]*\s*:\s*['"]*([^'"]+)''', match.group(1), re.DOTALL):
                stream_url = match.group(1)
                if self._get_direct_hostname(stream_url) == 'gvideo':
                    sources[stream_url] = self._get_direct_hostname(stream_url)
        
        if not sources:
            fragment = dom_parser.parse_dom(html, 'div', {'class': 'bx-main'})
            if fragment:
                match = re.search('<iframe[^>]*src="([^"]+)', fragment[0])
                if match:
                    stream_url = match.group(1)
                    host = urlparse.urlparse(stream_url).hostname
                    sources[stream_url] = host
                    
        return sources
    
    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year):
        search_url = urlparse.urljoin(self.base_url, '/search/%s.html' % urllib.quote_plus(title))
        html = self._http_get(search_url, cache_limit=.25)
        results = []
        fragment = dom_parser.parse_dom(html, 'div', {'class': 'list-movie'})
        if fragment:
            for item in dom_parser.parse_dom(fragment[0], 'div', {'class': 'movie'}):
                match = re.search('class="movie-name".*?href="([^"]+)[^>]+>([^<]+)', item)
                if match:
                    url, match_title = match.groups()
                    
                    match_year = ''
                    for info_frag in dom_parser.parse_dom(item, 'p', {'class': 'info'}):
                        match = re.search('(\d{4})', info_frag)
                        if match:
                            match_year = match.group(1)
                            break
                            
                    if (not year or not match_year or year == match_year):
                        result = {'url': scraper_utils.pathify_url(url), 'title': match_title, 'year': match_year}
                        results.append(result)
        
        return results

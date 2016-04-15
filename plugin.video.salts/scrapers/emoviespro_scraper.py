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


BASE_URL = 'http://emovies.pro'

class EMoviesPro_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'eMovies.Pro'

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
            fragment = dom_parser.parse_dom(html, 'div', {'class': 'tab_container'})
            if fragment:
                q_str = 'HDRIP'
                match = re.search('>Quality(.*?)<br\s*/?>', html, re.I)
                if match:
                    q_str = match.group(1)
                    q_str = re.sub('(</?strong[^>]*>|:|\s)', '', q_str, re.I | re.U)

                for source in dom_parser.parse_dom(fragment[0], 'iframe', ret='src'):
                    host = urlparse.urlparse(source).hostname
                    quality = scraper_utils.blog_get_quality(video, q_str, host)
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': source, 'direct': False}
                    
                    match = re.search('class="views-infos">(\d+).*?class="rating">(\d+)%', html, re.DOTALL)
                    if match:
                        hoster['views'] = int(match.group(1))
                        hoster['rating'] = match.group(2)
                    
                    hosters.append(hoster)

        return hosters

    def __get_sources(self, html):
        sources = []
        for source in dom_parser.parse_dom(html, 'source', {'type': 'video/mp4'}, ret='src'):
            if source:
                if self._get_direct_hostname(source) == 'gvideo':
                    sources.append(source)
                else:
                    redir_url = self._http_get(source, allow_redirect=False, method='HEAD', cache_limit=.5)
                    if redir_url.startswith('http'):
                        sources.append(redir_url)
                    else:
                        sources.append(source)
                
        return sources
    
    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year, season=''):
        results = []
        search_url = urlparse.urljoin(self.base_url, '/?s=%s' % (urllib.quote_plus(title)))
        html = self._http_get(search_url, cache_limit=1)
        if not re.search('nothing matched your search criteria', html, re.I):
            for item in dom_parser.parse_dom(html, 'li', {'class': '[^"]*box-shadow[^"]*'}):
                match = re.search('href="([^"]+)[^>]*title="([^"]+)', item)
                if match:
                    match_url, match_title_year = match.groups()
                    match = re.search('(.*?)(?:\s+\(?(\d{4})\)?)', match_title_year)
                    if match:
                        match_title, match_year = match.groups()
                    else:
                        match_title = match_title_year
                        match_year = ''
                    
                    if not year or not match_year or year == match_year:
                        result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                        results.append(result)

        return results

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


BASE_URL = 'http://firemovieshd.com'
Q_MAP = {'TS': QUALITIES.LOW, 'CAM': QUALITIES.LOW, 'HDTS': QUALITIES.LOW, 'HD 720P': QUALITIES.HD720}

class FireMovies_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'FireMoviesHD'

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
            fragment = dom_parser.parse_dom(html, 'div', {'class': 'meta-media'})
            if fragment:
                iframe_url = dom_parser.parse_dom(fragment[0], 'iframe', ret='src')
                if iframe_url:
                    iframe_url = urlparse.urljoin(self.base_url, iframe_url[0])
                    html = self._http_get(iframe_url, cache_limit=.5)
                    for source in dom_parser.parse_dom(html, 'source', ret='src'):
                        source_url = urlparse.urljoin(self.base_url, source)
                        redir_url = self._http_get(source_url, allow_redirect=False, cache_limit=.5)
                        if redir_url.startswith('http'):
                            sources[redir_url] = scraper_utils.gv_get_quality(redir_url)
                        else:
                            sources[source_url] = QUALITIES.HIGH
                    
            for source in sources:
                hoster = {'multi-part': False, 'host': self._get_direct_hostname(source), 'class': self, 'quality': sources[source], 'views': None, 'rating': None, 'url': source, 'direct': True}
                hosters.append(hoster)
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year):
        search_url = urlparse.urljoin(self.base_url, '/?s=%s' % (urllib.quote_plus(title)))
        html = self._http_get(search_url, cache_limit=1)
        results = []
        match_year = ''
        for entry in dom_parser.parse_dom(html, 'header', {'class': 'entry-header'}):
            match = re.search('href="([^"]+)[^>]+>([^<]+)', entry)
            if match:
                match_url, match_title_year = match.groups()
                match = re.search('(.*?)\s+\(?(\d{4})\)?', match_title_year)
                if match:
                    match_title, match_year = match.groups()
                else:
                    match_title = match_title_year
                    match_year = ''
                
                if not year or not match_year or year == match_year:
                    result = {'title': match_title, 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)

        return results

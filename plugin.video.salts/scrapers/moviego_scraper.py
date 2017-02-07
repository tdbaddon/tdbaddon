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
import urlparse
import re
import kodi
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES

BASE_URL = 'http://moviego.cc'
XHR = {'X-Requested-With': 'XMLHttpRequest'}
Q_MAP = {'HD1080': QUALITIES.HD1080, 'HD720': QUALITIES.HD720, 'SD480': QUALITIES.HIGH, 'CAMRIP': QUALITIES.LOW}

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'MovieGo'

    def get_sources(self, video):
        source_url = self.get_url(video)
        sources = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=8)
            q_str = dom_parser.parse_dom(html, 'div', {'class': 'poster-qulabel'})
            if q_str:
                q_str = q_str[0].replace(' ', '').upper()
                page_quality = Q_MAP.get(q_str, QUALITIES.HIGH)
            else:
                page_quality = QUALITIES.HIGH
                
            for fragment in dom_parser.parse_dom(html, 'div', {'class': 'tab_box'}):
                direct = True
                match = re.search('file\s*:\s*"([^"]+)', fragment)
                if match:
                    stream_url = match.group(1)
                else:
                    stream_url = self.__get_ajax_sources(fragment, page_url)
                
                if not stream_url:
                    stream_url = dom_parser.parse_dom(fragment, 'iframe', ret='src')
                    if stream_url:
                        stream_url = stream_url[0]
                        direct = False
                    
                if stream_url:
                    quality = page_quality
                    if direct:
                        stream_url += scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua(), 'Referer': page_url})
                        host = self._get_direct_hostname(stream_url)
                        if host == 'gvideo':
                            quality = scraper_utils.gv_get_quality(stream_url)
                    else:
                        host = urlparse.urlparse(stream_url).hostname
                        
                    source = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': direct}
                    sources.append(source)

        return sources

    def __get_ajax_sources(self, html, page_url):
        stream_url = ''
        match = re.search('''\$\.getJSON\('([^']+)'\s*,\s*(\{.*?\})''', html)
        if match:
            ajax_url, params = match.groups()
            params = scraper_utils.parse_params(params)
            ajax_url = urlparse.urljoin(self.base_url, ajax_url)
            headers = {'Referer': page_url}
            headers.update(XHR)
            html = self._http_get(ajax_url, params=params, headers=headers, cache_limit=.5)
            js_data = scraper_utils.parse_json(html, ajax_url)
            stream_url = js_data.get('file', '')
        return stream_url
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        data = {'hash': 'indexert', 'do': 'search', 'subaction': 'search', 'search_start': 0, 'full_search': 0, 'result_from': 1, 'story': title}
        search_url = urlparse.urljoin(self.base_url, 'index.php')
        html = self._http_get(search_url, params={'do': 'search'}, data=data, cache_limit=8)
        if dom_parser.parse_dom(html, 'div', {'class': 'sresult'}):
            for item in dom_parser.parse_dom(html, 'div', {'class': 'short_content'}):
                match = re.search('href="([^"]+)', item)
                match_title_year = dom_parser.parse_dom(item, 'div', {'class': 'short_header'})
                if match and match_title_year:
                    url = match.group(1)
                    match_title, match_year = scraper_utils.extra_year(match_title_year[0])
                    if not year or not match_year or year == match_year:
                        result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(url)}
                        results.append(result)

        return results

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
import kodi
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://viooz.ac'
GK_URL = '/p9/plugins/gkpluginsphp.php'
XHR = {'X-Requested-With': 'XMLHttpRequest'}

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
        return 'viooz.ac'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            page_html = self._http_get(url, cache_limit=.5)

            if re.search('<span[^>]+>\s*Low Quality\s*</span>', page_html):
                quality = QUALITIES.LOW
            else:
                quality = QUALITIES.HIGH
            
            for match in re.finditer('gkpluginsphp.*?link\s*:\s*"([^"]+)', page_html):
                data = {'link': match.group(1)}
                headers = XHR
                headers['Referer'] = url
                gk_url = urlparse.urljoin(self.base_url, GK_URL)
                html = self._http_get(gk_url, data=data, headers=headers, cache_limit=.25)
                js_result = scraper_utils.parse_json(html, gk_url)
                if 'link' in js_result:
                    if isinstance(js_result['link'], list):
                        sources = dict((link['link'], scraper_utils.height_get_quality(link['label'])) for link in js_result['link'])
                        direct = True
                    elif js_result['link'].startswith('http'):
                        sources = {js_result['link']: quality}
                        direct = False
                    
                    for source in sources:
                        if direct:
                            host = self._get_direct_hostname(source)
                        else:
                            host = urlparse.urlparse(source).hostname
                        hoster = {'multi-part': False, 'url': source, 'class': self, 'quality': sources[source], 'host': host, 'rating': None, 'views': None, 'direct': direct}
                        hosters.append(hoster)
            
            for fragment in dom_parser.parse_dom(page_html, 'div', {'class': 'tabContent'}):
                for stream_url in dom_parser.parse_dom(fragment, 'iframe', ret='src') + dom_parser.parse_dom(fragment, 'a', ret='href'):
                    host = urlparse.urlparse(stream_url).hostname
                    hoster = {'multi-part': False, 'url': stream_url, 'class': self, 'quality': quality, 'host': host, 'rating': None, 'views': None, 'direct': False}
                    hosters.append(hoster)

        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        search_url = urlparse.urljoin(self.base_url, '/search')
        params = {'q': title, 's': 't'}
        html = self._http_get(search_url, params=params, cache_limit=1)
        pattern = 'class="title_list">\s*<a\s+href="([^"]+)"\s+title="([^"]+)\((\d{4})\)'
        results = []
        for match in re.finditer(pattern, html):
            url, title, match_year = match.groups('')
            if not year or not match_year or year == match_year:
                result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(title), 'year': match_year}
                results.append(result)
        return results

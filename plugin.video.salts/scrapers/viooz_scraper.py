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

from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://viooz.ac'
GK_URL = '/p8/plugins/gkpluginsphp.php'
XHR = {'X-Requested-With': 'XMLHttpRequest'}

class VioozAc_Scraper(scraper.Scraper):
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

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        return '[%s] %s' % (item['quality'], item['host'])

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)

            if re.search('<span[^>]+>\s*Low Quality\s*</span>', html):
                quality = QUALITIES.LOW
            else:
                quality = QUALITIES.HIGH
            
            for match in re.finditer('gkpluginsphp.*?link\s*:\s*"([^"]+)', html):
                data = {'link': match.group(1)}
                headers = XHR
                headers['Referer'] = url
                gk_url = urlparse.urljoin(self.base_url, GK_URL)
                html = self._http_get(gk_url, data=data, headers=headers, cache_limit=.25)
                js_result = scraper_utils.parse_json(html, gk_url)
                if 'link' in js_result and 'func' not in js_result:
                    if isinstance(js_result['link'], list):
                        sources = dict((link['link'], scraper_utils.height_get_quality(link['label'])) for link in js_result['link'])
                    else:
                        sources = {js_result['link']: quality}
                    
                    for source in sources:
                        host = self._get_direct_hostname(source)
                        hoster = {'multi-part': False, 'url': source, 'class': self, 'quality': sources[source], 'host': host, 'rating': None, 'views': None, 'direct': True}
                        hosters.append(hoster)

        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year):
        search_url = urlparse.urljoin(self.base_url, '/search?q=')
        search_url += urllib.quote_plus(title)
        search_url += '&s=t'
        html = self._http_get(search_url, cache_limit=.25)
        pattern = 'class="title_list">\s*<a\s+href="([^"]+)"\s+title="([^"]+)\((\d{4})\)'
        results = []
        for match in re.finditer(pattern, html):
            url, title, match_year = match.groups('')
            if not year or not match_year or year == match_year:
                result = {'url': scraper_utils.pathify_url(url), 'title': title, 'year': match_year}
                results.append(result)
        return results

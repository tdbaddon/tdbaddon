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
from salts_lib.constants import Q_ORDER
from salts_lib.constants import VIDEO_TYPES
import scraper


XHR = {'X-Requested-With': 'XMLHttpRequest'}
BASE_URL = 'http://zumvo.so'
QUALITY_MAP = {'HD': QUALITIES.HD1080, 'CAM': QUALITIES.MEDIUM, 'BR-RIP': QUALITIES.HD720, 'UNKNOWN': QUALITIES.MEDIUM, 'SD': QUALITIES.HIGH}
GK_URL = '/player/gkplayerphp/plugins/gkpluginsphp.php'

class Zumvo_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'zumvo.com'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        if item['views'] is not None:
            label += ' (%s views)' % (item['views'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            match = re.search('href="([^"]+)"\s*class="player_btn_big"', html)
            if match:
                url = match.group(1)
                html = self._http_get(url, cache_limit=.5)
            
                q_str = ''
                match = re.search('class="status">([^<]+)', html)
                if match:
                    q_str = match.group(1)
                page_quality = QUALITY_MAP.get(q_str, QUALITIES.HIGH)
                    
                views = None
                match = re.search('Views:</dt>\s*<dd>(\d+)', html, re.DOTALL)
                if match:
                    views = match.group(1)
                    
                for src in dom_parser.parse_dom(html, 'iframe', ret='SRC'):
                    html = self._http_get(src, cache_limit=.5)
                    for match in re.finditer('gkpluginsphp.*?link\s*:\s*"([^"]+)', html):
                        data = {'link': match.group(1)}
                        headers = XHR
                        headers['Referer'] = url
                        gk_url = urlparse.urljoin(src, GK_URL)
                        html = self._http_get(gk_url, data=data, headers=headers, cache_limit=.25)
                        js_result = scraper_utils.parse_json(html, gk_url)
                        if 'link' in js_result and 'func' not in js_result:
                            if isinstance(js_result['link'], list):
                                sources = dict((link['link'], scraper_utils.height_get_quality(link['label'])) for link in js_result['link'])
                            else:
                                sources = {js_result['link']: page_quality}
                            
                            for source in sources:
                                host = self._get_direct_hostname(source)
                                if Q_ORDER[page_quality] < Q_ORDER[sources[source]]:
                                    quality = page_quality
                                else:
                                    quality = sources[source]
                                hoster = {'multi-part': False, 'url': source, 'class': self, 'quality': quality, 'host': host, 'rating': None, 'views': views, 'direct': True}
                                hosters.append(hoster)
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year, season=''):
        search_url = urlparse.urljoin(self.base_url, '/search/')
        search_url += urllib.quote_plus(title)
        html = self._http_get(search_url, cache_limit=0)
        results = []
        match = re.search('ul class="list-film"(.*?)</ul>', html, re.DOTALL)
        if match:
            result_fragment = match.group(1)
            pattern = 'class="name">\s*<a\s+href="([^"]+)"\s+title="Watch\s+(.*?)\s+\((\d{4})\)'
            for match in re.finditer(pattern, result_fragment, re.DOTALL):
                url, title, match_year = match.groups('')
                if not year or not match_year or year == match_year:
                    result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(title), 'year': match_year}
                    results.append(result)
        return results

    def _http_get(self, url, data=None, headers=None, cache_limit=8):
        html = self._cached_http_get(url, self.base_url, self.timeout, data=data, headers=headers, cache_limit=cache_limit)
        cookie = scraper_utils.get_sucuri_cookie(html)
        if cookie:
            log_utils.log('Setting Zumvo cookie: %s' % (cookie), log_utils.LOGDEBUG)
            html = self._cached_http_get(url, self.base_url, self.timeout, cookies=cookie, data=data, headers=headers, cache_limit=0)
        return html

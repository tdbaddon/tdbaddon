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
import base64
import re
import urllib
import urlparse

from salts_lib import dom_parser
from salts_lib import kodi
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://miradetodo.com.ar'
GK_KEY1 = base64.urlsafe_b64decode('QjZVTUMxUms3VFJBVU56V3hraHI=')
GK_KEY2 = base64.urlsafe_b64decode('aUJocnZjOGdGZENaQWh3V2huUm0=')

class MiraDetodo_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'MiraDeTodo'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            match = re.search('proxy\.link=([^"&]+)', html)
            if match:
                proxy_link = match.group(1)
                proxy_link = proxy_link.split('*', 1)[-1]
                if len(proxy_link) <= 224:
                    picasa_url = scraper_utils.gk_decrypt(self.get_name(), GK_KEY1, proxy_link)
                else:
                    picasa_url = scraper_utils.gk_decrypt(self.get_name(), GK_KEY2, proxy_link)
                if self._get_direct_hostname(picasa_url) == 'gvideo':
                    sources = self._parse_google(picasa_url)
                    for source in sources:
                        hoster = {'multi-part': False, 'url': source, 'class': self, 'quality': scraper_utils.gv_get_quality(source), 'host': self._get_direct_hostname(source), 'rating': None, 'views': None, 'direct': True}
                        hosters.append(hoster)
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year):
        search_url = urlparse.urljoin(self.base_url, '/search_result.php?search=&query=')
        search_url += urllib.quote_plus('%s' % (title))
        html = self._http_get(search_url, cache_limit=1)
        results = []
        for item in dom_parser.parse_dom(html, 'div', {'class': 'BrVidCon'}):
            match = re.search('href="([^"]+).*?alt="([^"]+)', item)
            if match:
                url, match_title_year = match.groups()
                if re.search('\d+\s*x\s*\d+', match_title_year): continue  # exclude episodes
                match = re.search('(.*?)\s+\((\d{4})\)', match_title_year)
                if match:
                    match_title, match_year = match.groups()
                else:
                    match_title = match_title_year
                    match_year = ''

                if not year or not match_year or year == match_year:
                    result = {'title': match_title, 'year': match_year, 'url': scraper_utils.pathify_url(url)}
                    results.append(result)

        return results

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
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


QUALITY_MAP = {'DVD': QUALITIES.HIGH, 'CAM': QUALITIES.LOW}
BASE_URL = 'http://movie25.hk'

class Movie25_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'movie25'

    def resolve_link(self, link):
        if self.base_url in link:
            url = urlparse.urljoin(self.base_url, link)
            html = self._http_get(url, cache_limit=0)
            match = re.search('''href='([^']*)'\s+value="Click Here to Play"''', html, re.DOTALL | re.I)
            if match:
                return match.group(1)
            else:
                iframe_url = dom_parser.parse_dom(html, 'IFRAME', {'id': 'showvideo'}, 'src')
                if iframe_url:
                    return iframe_url[0]
                else:
                    return link
        else:
                return link

    def format_source_label(self, item):
        return '[%s] %s' % (item['quality'], item['host'])

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)

            quality = None
            match = re.search('Links\s+-\s+Quality\s*([^<]*)</h1>', html, re.DOTALL | re.I)
            if match:
                quality = QUALITY_MAP.get(match.group(1).strip().upper())

            for match in re.finditer('id="link_name">\s*([^<]+).*?href="([^"]+)', html, re.DOTALL):
                host, url = match.groups()
                match = re.search('url=([^&]+)', url)
                if match:
                    url = base64.b64decode(match.group(1))
                    host = urlparse.urlparse(url).hostname
                    
                hoster = {'multi-part': False, 'host': host, 'class': self, 'url': url, 'quality': scraper_utils.get_quality(video, host, quality), 'rating': None, 'views': None, 'direct': False}
                hosters.append(hoster)
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year, season=''):
        search_url = urlparse.urljoin(self.base_url, '/search.php?key=')
        search_url += urllib.quote_plus('%s %s' % (title, year))
        search_url += '&submit='
        html = self._http_get(search_url, cache_limit=.25)
        pattern = 'class="movie_about">.*?href="([^"]+).*?>\s+(.*?)\s*\(?(\d{4})?\)?\s+</a></h1>'
        results = []
        for match in re.finditer(pattern, html, re.DOTALL):
            url, title, year = match.groups('')
            result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(title), 'year': year}
            results.append(result)
        return results

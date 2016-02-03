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
import urllib
import urlparse
import re
import random
from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import dom_parser
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import XHR

VIDEO_URL = '/video_info/html5'

class XMovies8_Scraper(scraper.Scraper):
    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'xmovies8'

    def resolve_link(self, link):
        link = link.split('|', 1)[0]
        html = self._http_get(link, allow_redirect=False, cache_limit=0)
        if html.startswith('http'):
            return html
        else:
            return link

    def format_source_label(self, item):
        return '[%s] %s' % (item['quality'], item['host'])

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.5)
            match = re.search('video_id\s*=\s*"([^"]+)', html)
            if match:
                data = {'v': match.group(1)}
                url = urlparse.urljoin(self.base_url, VIDEO_URL)
                headers = XHR
                headers['Referer'] = page_url
                html = self._http_get(url, data=data, headers=headers, cache_limit=.25)
                for match in re.finditer('<source\s+data-res="([^"]+)"\s+src="([^"]+)', html):
                    stream_url = urlparse.urljoin(self.base_url, match.group(2)) + '|User-Agent=%s' % (self._get_ua())
                    quality = self._height_get_quality(match.group(1))
                    hoster = {'multi-part': False, 'host': self._get_direct_hostname(stream_url), 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
                    hosters.append(hoster)
            
        return hosters

    def get_url(self, video):
        return super(XMovies8_Scraper, self)._default_get_url(video)

    def search(self, video_type, title, year):
        search_url = urlparse.urljoin(self.base_url, '/results?q=%s' % urllib.quote_plus(title))
        html = self._http_get(search_url, cache_limit=.25)
        results = []
        for result in dom_parser.parse_dom(html, 'div', {'class': 'cell'}):
            match = re.search('class="video_title".*?href="([^"]+)"[^>]*>\s*([^<]+)', result, re.DOTALL)
            if match:
                url, match_title_year = match.groups()
                match = re.search('(.*?)\s+\((\d{4})\)', match_title_year)
                if match:
                    match_title, match_year = match.groups()
                else:
                    match_title = match_title_year
                    match = re.search('class="video_quality".*?Year\s*(?:</b>)?\s*:\s*(\d{4})', result, re.DOTALL)
                    if match:
                        match_year = match.group(1)
                    else:
                        match_year = ''

                if not year or not match_year or year == match_year:
                    result = {'url': self._pathify_url(url), 'title': match_title, 'year': match_year}
                    results.append(result)
        return results

    @classmethod
    def get_settings(cls):
        settings = super(XMovies8_Scraper, cls).get_settings()
        settings.append('         <setting id="%s-default_url" type="string" visible="false"/>' % (cls.get_name()))
        return settings

# if no default url has been set, then pick one and set it. If one has been set, use it
default_url = kodi.get_setting('%s-default_url' % (XMovies8_Scraper.get_name()))
if not default_url:
    BASE_URL = random.choice(['https://xmovies8.org', 'http://genvideos.com'])
    XMovies8_Scraper.base_url = BASE_URL
    kodi.set_setting('%s-default_url' % (XMovies8_Scraper.get_name()), BASE_URL)
else:
    XMovies8_Scraper.base_url = default_url

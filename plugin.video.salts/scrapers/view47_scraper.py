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
import time
import urllib
import urlparse

from salts_lib import dom_parser
from salts_lib import kodi
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://view47.com'
EPID_URL = '/ip.temp/swf/plugins/ipplugins.php'
JSON_URL = '/ip.temp/swf/plugins/plugins_player.php'

class View47_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        if 'www' in self.base_url: self.base_url = BASE_URL  # hack base url to work

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'view47'

    def resolve_link(self, link):
        url = urlparse.urljoin(self.base_url, link)
        html = self._http_get(url, cache_limit=.5)
        match = re.search('file\s*:\s*"([^"]+)', html)
        if match:
            return match.group(1)
        else:
            match = re.search('<iframe[^<]*src="([^"]+)', html)
            if match:
                return match.group(1)
            else:
                match = re.search('proxy\.link=([^"]+)', html)
                if match:
                    return match.group(1)
        
    def format_source_label(self, item):
        return '[%s] %s' % (item['quality'], item['host'])

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            div = dom_parser.parse_dom(html, 'ul', {'class': 'css_server[^"]*'})
            if div:
                div = re.sub('<img[^>]+>', '', div[0])
                for match in re.finditer('href="([^"]+)">([^<]+)', div):
                    stream_url, host = match.groups()
                    host = re.sub('-\d+$', '', host)
                    if host == 'picasa':
                        stream_url = stream_url + '|User-Agent=%s' % (scraper_utils.get_ua())
                        direct = True
                        host = 'gvideo'
                        quality = QUALITIES.MEDIUM
                    else:
                        quality = scraper_utils.get_quality(video, host, QUALITIES.MEDIUM)
                        direct = False

                    hosters.append({'multi-part': False, 'url': stream_url, 'class': self, 'quality': quality, 'host': host, 'rating': None, 'views': None, 'direct': direct})

        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year):
        search_url = urlparse.urljoin(self.base_url, '/search.php?q=%s&limit=20&timestamp=%s' % (urllib.quote_plus(title), time.time()))
        html = self._http_get(search_url, cache_limit=.25)
        results = []
        items = dom_parser.parse_dom(html, 'li')
        if len(items) >= 2:
            items = items[1:]
            for item in items:
                url = dom_parser.parse_dom(item, 'a', ret='href')
                match_title_year = dom_parser.parse_dom(item, 'strong')
                if url and match_title_year:
                    url = url[0]
                    match_title_year = match_title_year[0].replace('<strong>', '').replace('</strong>', '')
                    match = re.search('(.*?)(?:\s+\(?(\d{4})\)?)', match_title_year)
                    if match:
                        match_title, match_year = match.groups()
                    else:
                        match_title = match_title_year
                        match_year = ''
                    
                    result = {'title': match_title, 'year': match_year, 'url': scraper_utils.pathify_url(url)}
                    results.append(result)
        return results

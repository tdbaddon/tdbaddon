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
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
from salts_lib.constants import Q_ORDER
from salts_lib.constants import XHR
import scraper

BASE_URL = 'http://watchitvideos.info'
Q_MAP = {'1080P HD': QUALITIES.HD1080, '720P HD': QUALITIES.HD720, 'HD': QUALITIES.HD720, 'DVD': QUALITIES.HIGH}

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
        return 'WatchItVideos'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.5)
            
            best_quality = QUALITIES.HIGH
            fragment = dom_parser.parse_dom(html, 'div', {'class': 'entry'})
            if fragment:
                for match in re.finditer('href="[^"]*/movies-quality/[^"]*[^>]*>([^<]+)', fragment[0], re.I):
                    quality = Q_MAP.get(match.group(1).upper(), QUALITIES.HIGH)
                    if Q_ORDER[quality] > Q_ORDER[best_quality]:
                        best_quality = quality
                        
            sources = []
            for vid_url in dom_parser.parse_dom(html, 'a', ret='data-vid'):
                vid_url = dom_parser.parse_dom(scraper_utils.cleanse_title(vid_url), 'iframe', ret='src')
                if vid_url:
                    sources.append(vid_url[0])
                
            fragment = dom_parser.parse_dom(html, 'table', {'class': 'additional-links'})
            if fragment:
                sources += re.findall('href="([^"]+)', fragment[0])
                    
            for stream_url in sources:
                host = urlparse.urlparse(stream_url).hostname
                quality = scraper_utils.get_quality(video, host, best_quality)
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
                hosters.append(hoster)
        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = urlparse.urljoin(self.base_url, '/wp-admin/admin-ajax.php')
        data = {'action': 'ajaxy_sf', 'sf_value': title, 'search': 'false'}
        headers = {'Referer': self.base_url}
        headers.update(XHR)
        html = self._http_get(search_url, data=data, headers=headers, cache_limit=2)
        js_data = scraper_utils.parse_json(html, search_url)
        try: items = js_data['post'][0]['all']
        except: items = []
        for item in items:
            match_url = item['post_link']
            match_title, match_year = scraper_utils.extra_year(item['post_title'])
            if not year or not match_year or year == match_year:
                result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                results.append(result)
        return results

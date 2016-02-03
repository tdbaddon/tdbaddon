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
import re
import urlparse
import urllib
from salts_lib import kodi
from salts_lib import dom_parser
from salts_lib import log_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH

BASE_URL = 'http://dizipas.com'

class Dizipas_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'Dizipas'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s (Turkish Subtitles)' % (item['quality'], item['host'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            pattern = '\$\.post\("([^"]+)"\s*,\s*\{\s*[\'"]id["\']\s*:\s*["\']([^\'"]+)'
            match = re.search(pattern, html)
            if match:
                post_url, vid_id = match.groups()
                data = {'id': vid_id, 'type': 'new'}
                html = self._http_get(post_url, data=data, cache_limit=.5)
                js_result = self._parse_json(html, post_url)
                for key in js_result:
                    stream_url = js_result[key]
                    host = self._get_direct_hostname(stream_url)
                    if host == 'gvideo':
                        quality = self._gv_get_quality(stream_url)
                    else:
                        quality = self._height_get_quality(key)
                        
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
                    hosters.append(hoster)

        return hosters

    def get_url(self, video):
        return super(Dizipas_Scraper, self)._default_get_url(video)

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'class="episode"\s+href="([^"]+/sezon-%s/bolum-%s)"' % (video.season, video.episode)
        title_pattern = 'class="episode-name"\s+href="(?P<url>[^"]+)">(?P<title>[^<]+)'
        return super(Dizipas_Scraper, self)._default_get_episode_url(show_url, video, episode_pattern, title_pattern)

    def search(self, video_type, title, year):
        search_url = urlparse.urljoin(self.base_url, '/arsiv?keyword=')
        search_url += urllib.quote_plus(title)
        html = self._http_get(search_url, cache_limit=8)
        results = []
        for item in dom_parser.parse_dom(html, 'div', {'class': 'tv-series-single'}):
            try:
                url = re.search('href="([^"]+)', item).group(1)
            except:
                url = ''

            try:
                match_year = re.search('<span>\s*(\d{4})\s*</span>', item).group(1)
            except:
                match_year = ''
            
            try:
                match_title = dom_parser.parse_dom(item, 'a', {'class': 'title'})
                match_title = re.search('([^>]+)$', match_title[0]).group(1)
                match_title = match_title.strip()
            except:
                match_title = ''
            
            if url and match_title and (not year or not match_year or year == match_year):
                result = {'url': self._pathify_url(url), 'title': match_title, 'year': ''}
                results.append(result)

        return results

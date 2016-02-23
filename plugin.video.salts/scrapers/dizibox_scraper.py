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

from salts_lib import dom_parser
from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://www.dizibox.com'

class Dizibox_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'Dizibox'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.25)
            match = re.search('''<option[^>]+value\s*=\s*["']([^"']+)[^>]*>(?:1|Altyaz.{1,3}s.{1,3}z)<''', html)
            if match:
                option_url = urlparse.urljoin(self.base_url, match.group(1))
                html = self._http_get(option_url, cache_limit=.25)
                fragment = dom_parser.parse_dom(html, 'span', {'class': 'object-wrapper'})
                if fragment:
                    iframe_url = dom_parser.parse_dom(fragment[0], 'iframe', ret='src')
                    if iframe_url:
                        html = self._http_get(iframe_url[0], cache_limit=.25)
                        seen_urls = {}
                        for match in re.finditer('"?file"?\s*:\s*"([^"]+)"\s*,\s*"?label"?\s*:\s*"(\d+)p?[^"]*"', html):
                            stream_url, height = match.groups()
                            if stream_url not in seen_urls:
                                seen_urls[stream_url] = True
                                stream_url += '|User-Agent=%s' % (scraper_utils.get_ua())
                                host = self._get_direct_hostname(stream_url)
                                if host == 'gvideo':
                                    quality = scraper_utils.gv_get_quality(stream_url)
                                else:
                                    quality = scraper_utils.height_get_quality(height)
                                hoster = {'multi-part': False, 'host': self._get_direct_hostname(stream_url), 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
                                hosters.append(hoster)
    
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def _get_episode_url(self, show_url, video):
        show_url = urlparse.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, cache_limit=24)
        pattern = '''href=['"]([^'"]+)[^>]+>\s*%s\.\s*Sezon<''' % (video.season)
        match = re.search(pattern, html)
        if match:
            season_url = urlparse.urljoin(self.base_url, match.group(1))
            episode_pattern = '''href=['"]([^'"]+-%s-sezon-%s-[^\;"]*bolum[^'"]*)''' % (video.season, video.episode)
            return self._default_get_episode_url(season_url, video, episode_pattern)

    def search(self, video_type, title, year):
        html = self._http_get(self.base_url, cache_limit=8)
        results = []
        seen_urls = {}
        norm_title = scraper_utils.normalize_title(title)
        for fragment in dom_parser.parse_dom(html, 'ul', {'class': 'category-list'}):
            for match in re.finditer('''href=["']([^'"]+)[^>]+>([^<]+)''', fragment):
                url, match_title = match.groups()
                if url not in seen_urls:
                    seen_urls[url] = True
                    if norm_title in scraper_utils.normalize_title(match_title):
                        result = {'url': scraper_utils.pathify_url(url), 'title': match_title, 'year': ''}
                        results.append(result)

        return results

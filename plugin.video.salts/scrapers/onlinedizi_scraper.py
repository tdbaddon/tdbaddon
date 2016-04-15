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
from salts_lib.constants import QUALITIES
import scraper


BASE_URL = 'http://onlinedizi.co'

class OnlineDizi_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'OnlineDizi'

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
            fragment = dom_parser.parse_dom(html, 'ul', {'class': 'dropdown-menu'})
            if fragment:
                match = re.search('''href=['"]([^'"]+)[^>]*>(?:Altyaz.{1,3}s.{1,3}z)<''', fragment[0])
                if match:
                    option_url = urlparse.urljoin(self.base_url, match.group(1))
                    html = self._http_get(option_url, cache_limit=2)
                    fragment = dom_parser.parse_dom(html, 'div', {'class': 'video-player'})
                    if fragment:
                        iframe_url = dom_parser.parse_dom(fragment[0], 'iframe', ret='src')
                        if iframe_url:
                            html = self._http_get(iframe_url[0], cache_limit=.25)
                            iframe_url = dom_parser.parse_dom(html, 'iframe', {'id': 'ifr'}, ret='src')
                            if iframe_url:
                                html = self._http_get(iframe_url[0], allow_redirect=False, method='HEAD', cache_limit=.25)
                                if html.startswith('http'):
                                    stream_url = html
                                    host = urlparse.urlparse(stream_url).hostname
                                    stream_url += '|User-Agent=%s' % (scraper_utils.get_ua())
                                    quality = QUALITIES.HIGH
                                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
                                    hosters.append(hoster)
    
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def _get_episode_url(self, show_url, video):
        episode_pattern = '''href=['"]([^'"]+-%s-sezon-%s-bolum[^'"]*)''' % (video.season, video.episode)
        return self._default_get_episode_url(show_url, video, episode_pattern)

    def search(self, video_type, title, year, season=''):
        html = self._http_get(self.base_url, cache_limit=48)
        results = []
        seen_urls = {}
        norm_title = scraper_utils.normalize_title(title)
        for fragment in dom_parser.parse_dom(html, 'ul', {'class': '[^"]*all-series-list[^"]*'}):
            for match in re.finditer('''href=["']([^'"]+)[^>]+>([^<]+)''', fragment):
                url, match_title = match.groups()
                if url not in seen_urls:
                    seen_urls[url] = True
                    if norm_title in scraper_utils.normalize_title(match_title):
                        result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(match_title), 'year': ''}
                        results.append(result)

        return results

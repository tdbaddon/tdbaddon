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
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://streamallthis.is'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'streamallthis.is'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=2)
            urls = dom_parser.parse_dom(html, 'iframe', ret='src')
            for iframe_url in urls:
                if '/ads/' in iframe_url:
                    continue
                elif '/watch/' in iframe_url:
                    url = urlparse.urljoin(self.base_url, iframe_url)
                    html = self._http_get(url, cache_limit=2)
                    urls += dom_parser.parse_dom(html, 'iframe', ret='src')
                    match = re.search('''location.href=['"]([^'"]+)''', html)
                    if match:
                        urls.append(match.group(1))
                else:
                    stream_url = iframe_url
                    host = urlparse.urlparse(stream_url).hostname
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'url': stream_url, 'quality': QUALITIES.HIGH, 'views': None, 'rating': None, 'direct': False}
                    hosters.append(hoster)
                    
        return hosters

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+s%02de%02d\.html)"\s+class="la"' % (int(video.season), int(video.episode))
        return self._default_get_episode_url(show_url, video, episode_pattern, '')

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        url = urlparse.urljoin(self.base_url, '/tv-shows-list.html')
        html = self._http_get(url, cache_limit=8)

        results = []
        norm_title = scraper_utils.normalize_title(title)
        pattern = 'href="([^"]+)"\s+class="lc">\s*(.*?)\s*<'
        for match in re.finditer(pattern, html):
            url, match_title = match.groups()
            if norm_title in scraper_utils.normalize_title(match_title):
                result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(match_title), 'year': ''}
                results.append(result)

        return results

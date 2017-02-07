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
import base64
import kodi
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
import scraper

BASE_URL = 'http://opentuner.is'

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
        return 'tvonline'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.25)
            for button in dom_parser.parse_dom(html, 'li', {'class': 'playing_button'}):
                try:
                    link = dom_parser.parse_dom(button, 'a', ret='href')
                    match = re.search('php\?.*?=?([^"]+)', link[0])
                    stream_url = base64.b64decode(match.group(1))
                    match = re.search('(https?://.*)', stream_url)
                    stream_url = match.group(1)
                    host = urlparse.urlparse(stream_url).hostname
                    quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
                    hosters.append(hoster)
                except Exception as e:
                    log_utils.log('Exception during tvonline source: %s - |%s|' % (e, button), log_utils.LOGDEBUG)
                    raise
    
        return hosters

    def _get_episode_url(self, show_url, video):
        episode_pattern = '''href=['"]([^'"]+/season-%s-episode-%s/?)''' % (video.season, video.episode)
        title_pattern = '''href=['"](?P<url>[^'"]+/season-\d+-episode-\d+/?).*?>\s*\d+\s*-\s*(?P<title>.*?)</a>'''
        return self._default_get_episode_url(show_url, video, episode_pattern, title_pattern)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
#         if title:
#             first_letter = title[:1].lower()
#             if first_letter.isdigit(): first_letter = '0-9'
#             search_url = '/alphabet/%s/' % (first_letter)
#             search_url = urlparse.urljoin(self.base_url, search_url)
#             html = self._http_get(search_url, cache_limit=24)
#             fragment = dom_parser.parse_dom(html, 'div', {'class': 'home'})
        results = []
        url = urlparse.urljoin(self.base_url, '/search.php')
        html = self._http_get(url, params={'q': title}, cache_limit=8)
        fragment = dom_parser.parse_dom(html, 'div', {'class': 'found'})
        if fragment:
            norm_title = scraper_utils.normalize_title(title)
            for match in re.finditer('''href=["']([^'"]+)[^>]+>([^<]+)''', fragment[0]):
                url, match_title_year = match.groups()
                match_title, match_year = scraper_utils.extra_year(match_title_year)
                if norm_title in scraper_utils.normalize_title(match_title) and (not year or not match_year or year == match_year):
                    result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)

        return results

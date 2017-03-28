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
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

QUALITY_MAP = {'HD': QUALITIES.HIGH, 'DVD': QUALITIES.HIGH, 'TV': QUALITIES.HIGH, 'LQ DVD': QUALITIES.MEDIUM, 'CAM': QUALITIES.LOW}
BASE_URL = 'http://www.tvsolarmovie.com'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'SolarMovie'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = urlparse.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)

        for _attrs, tr in dom_parser2.parse_dom(html, 'tr', {'id': re.compile('link_\d+')}):
            link_pattern = 'href="[^"]+go.php\?url=([^"]+).*?class="qualityCell[^>]*>\s*([^<]+)'
            link_match = re.search(link_pattern, tr, re.DOTALL)
            if link_match:
                stream_url, quality = link_match.groups()
                host = urlparse.urlparse(stream_url).hostname
                if host:
                    quality = QUALITY_MAP.get(quality.strip().upper(), QUALITIES.MEDIUM)
                    hoster = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': scraper_utils.get_quality(video, host, quality), 'views': None, 'rating': None, 'direct': False}
                    hosters.append(hoster)

        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        if video_type == VIDEO_TYPES.TVSHOW:
            return self.__tv_search(title, year)
        else:
            results = []
            html = self. _http_get(self.base_url, params={'s': title}, cache_limit=8)
            norm_title = scraper_utils.normalize_title(title)
            for attrs, _content in dom_parser2.parse_dom(html, 'a', {'class': 'coverImage'}, req=['title', 'href']):
                match_title_year, match_url = attrs['title'], attrs['href']
                if 'Season' in match_title_year and 'Episode' in match_title_year: continue
                match_title, match_year = scraper_utils.extra_year(match_title_year)
                match_norm_title = scraper_utils.normalize_title(match_title)
                if (norm_title not in match_norm_title) and (match_norm_title not in norm_title): continue
                if not year or not match_year or year == match_year:
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)
        return results

    def __tv_search(self, title, year):  # @UnusedVariable
        results = []
        url = urlparse.urljoin(self.base_url, '/watch-series')
        html = self._http_get(url, cache_limit=48)
        norm_title = scraper_utils.normalize_title(title)
        for _attrs, fragment in dom_parser2.parse_dom(html, 'ul', {'class': 'letter-box-container'}):
            for attrs, match_title in dom_parser2.parse_dom(fragment, 'a', req='href'):
                match_url = attrs['href']
                if norm_title in scraper_utils.normalize_title(match_title):
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': ''}
                    results.append(result)
        return results
    
    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+season-%s-episode-%s(?!\d)[^"]*)' % (video.season, video.episode)
        return self._default_get_episode_url(show_url, video, episode_pattern)

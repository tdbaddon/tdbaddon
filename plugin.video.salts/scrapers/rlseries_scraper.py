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

BASE_URL = 'http://rlseries.com'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.SEASON, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'RLSeries'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=1)
            fragment = dom_parser.parse_dom(html, 'div', {'class': 'v_ifo'})
            if fragment:
                for stream_url in dom_parser.parse_dom(fragment[0], 'a', ret='href'):
                    host = urlparse.urlparse(stream_url).hostname
                    quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
                    hosters.append(hoster)
        return hosters

    def _get_episode_url(self, season_url, video):
        episode_pattern = 'href="([^"]*episode-%s-[^"]*)' % (video.episode)
        title_pattern = '<a[^>]*href="(?P<url>[^"]+)[^>]+title="Episode\s+\d+:\s*(?P<title>[^"]+)'
        airdate_pattern = 'class="lst"[^>]+href="([^"]+)(?:[^>]+>){6}{p_day}/{p_month}/{year}<'
        return self._default_get_episode_url(season_url, video, episode_pattern, title_pattern, airdate_pattern)
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        if title and title[0].isalpha():
            page_url = ['/list/?char=%s' % (title[0])]
            while page_url:
                page_url = urlparse.urljoin(self.base_url, page_url[0])
                html = self._http_get(page_url, cache_limit=48)
                fragment = dom_parser.parse_dom(html, 'ul', {'class': 'list-film-char'})
                if fragment:
                    norm_title = scraper_utils.normalize_title(title)
                    for match in re.finditer('href="([^"]+)[^>]+>(.*?)</a>', fragment[0]):
                        match_url, match_title = match.groups()
                        match_title = re.sub('</?strong>', '', match_title)
                        match = re.search('Season\s+(\d+)', match_title, re.I)
                        if match:
                            if season and int(season) != int(match.group(1)):
                                continue
                            
                            if norm_title in scraper_utils.normalize_title(match_title):
                                result = {'title': scraper_utils.cleanse_title(match_title), 'year': '', 'url': scraper_utils.pathify_url(match_url)}
                                results.append(result)
                
                if results:
                    break
                
                page_url = dom_parser.parse_dom(html, 'a', {'class': 'nextpostslink'}, ret='href')

        return results

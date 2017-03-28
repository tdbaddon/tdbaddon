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
import urlparse
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


QUALITY_MAP = {'HD': QUALITIES.HD720, 'HDTV': QUALITIES.HIGH, 'DVD': QUALITIES.HIGH, '3D': QUALITIES.HIGH, 'CAM': QUALITIES.LOW}
BASE_URL = 'http://www.iwatchonline.cr'

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
        return 'iWatchOnline'

    def resolve_link(self, link):
        url = urlparse.urljoin(self.base_url, link)
        html = self._http_get(url, allow_redirect=False, cache_limit=.5)
        if html.startswith('http'):
            return html
        else:
            iframe_url = dom_parser2.parse_dom(html, 'iframe', {'class': 'frame'}, req='src')
            if iframe_url:
                return iframe_url[0].attrs['src']

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = urlparse.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)

        fragment = dom_parser2.parse_dom(html, 'table', {'id': 'streamlinks'})
        if not fragment: return hosters
        
        max_age = 0
        now = min_age = int(time.time())
        for _attrs, row in dom_parser2.parse_dom(fragment[0].content, 'tr', {'id': re.compile('pt\d+')}):
            if video.video_type == VIDEO_TYPES.MOVIE:
                pattern = 'href="([^"]+).*?/>([^<]+).*?(?:<td>.*?</td>\s*){1}<td>(.*?)</td>\s*<td>(.*?)</td>'
            else:
                pattern = 'href="([^"]+).*?/>([^<]+).*?(<span class="linkdate">.*?)</td>\s*<td>(.*?)</td>'
            match = re.search(pattern, row, re.DOTALL)
            if not match: continue
            
            url, host, age, quality = match.groups()
            age = self.__get_age(now, age)
            quality = quality.upper()
            if age > max_age: max_age = age
            if age < min_age: min_age = age
            host = host.strip()
            hoster = {'multi-part': False, 'class': self, 'url': scraper_utils.pathify_url(url), 'host': host, 'age': age, 'views': None, 'rating': None, 'direct': False}
            hoster['quality'] = scraper_utils.get_quality(video, host, QUALITY_MAP.get(quality, QUALITIES.HIGH))
            hosters.append(hoster)

        unit = (max_age - min_age) / 100
        if unit > 0:
            for hoster in hosters:
                hoster['rating'] = (hoster['age'] - min_age) / unit
        return hosters

    def __get_age(self, now, age_str):
        age_str = re.sub('</?span[^>]*>', '', age_str)
        try:
            age = int(age_str)
        except ValueError:
            match = re.search('(\d+)\s+(.*)', age_str)
            if match:
                num, unit = match.groups()
                num = int(num)
                unit = unit.lower()
                if 'minute' in unit:
                    mult = 60
                elif 'hour' in unit:
                    mult = (60 * 60)
                elif 'day' in unit:
                    mult = (60 * 60 * 24)
                elif 'month' in unit:
                    mult = (60 * 60 * 24 * 30)
                elif 'year' in unit:
                    mult = (60 * 60 * 24 * 365)
                else:
                    mult = 0
            else:
                num = 0
                mult = 0
            age = now - (num * mult)
        return age

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_in = 'm' if video_type == VIDEO_TYPES.MOVIE else 't'
        search_url = urlparse.urljoin(self.base_url, '/search')
        html = self._http_get(search_url, data={'searchquery': title, 'searchin': search_in}, cache_limit=8)
        try:
            fragment = dom_parser2.parse_dom(html, 'div', {'class': 'search-page'})
            fragment = dom_parser2.parse_dom(fragment[0].content, 'table')
            for attrs, match_title_year in dom_parser2.parse_dom(fragment[0].content, 'a', req='href'):
                match_url = attrs['href']
                match_title, match_year = scraper_utils.extra_year(match_title_year)
                if not year or not match_year or year == match_year:
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)
        except:
            pass
        
        return results

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+-s%02de%02d)"' % (int(video.season), int(video.episode))
        title_pattern = 'href="(?P<url>[^"]+)"><i class="icon-play-circle">.*?<td>(?P<title>[^<]+)</td>'
        return self._default_get_episode_url(show_url, video, episode_pattern, title_pattern)

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


BASE_URL = 'http://moviestorm.eu'
QUALITY_MAP = {'HD': QUALITIES.HIGH, 'CAM': QUALITIES.LOW, 'BRRIP': QUALITIES.HIGH, 'UNKNOWN': QUALITIES.MEDIUM, 'DVDRIP': QUALITIES.HIGH}

class MovieStorm_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'moviestorm.eu'

    def resolve_link(self, link):
        if self.base_url in link:
            url = urlparse.urljoin(self.base_url, link)
            html = self._http_get(url, cache_limit=.5)
            match = re.search('class="real_link"\s+href="([^"]+)', html)
            if match:
                return match.group(1)
        else:
            return link

    def format_source_label(self, item):
        label = '[%s] %s (%s views)' % (item['quality'], item['host'], item['views'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            pattern = 'class="source_td">\s*<img[^>]+>\s*(.*?)\s*-\s*\((\d+) views\).*?class="quality_td">\s*(.*?)\s*<.*?href="([^"]+)'
            for match in re.finditer(pattern, html, re.DOTALL):
                host, views, quality_str, stream_url = match.groups()

                hoster = {'multi-part': False, 'host': host, 'class': self, 'url': stream_url, 'quality': scraper_utils.get_quality(video, host, QUALITY_MAP.get(quality_str.upper())), 'views': views, 'rating': None, 'direct': False}
                hosters.append(hoster)
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+season-%d/episode-%d/[^"]+)' % (int(video.season), int(video.episode))
        title_pattern = 'class="name left">\s*<a\s+href="(?P<url>[^"]+)">(?P<title>[^<]+)'
        airdate_pattern = 'class="edate[^>]+>\s*{p_month}-{p_day}-{year}.*?href="([^"]+)'
        return self._default_get_episode_url(show_url, video, episode_pattern, title_pattern, airdate_pattern)

    def search(self, video_type, title, year):
        results = []
        if video_type == VIDEO_TYPES.TVSHOW:
            url = urlparse.urljoin(self.base_url, '/series/all/')
            html = self._http_get(url, cache_limit=8)
    
            links = dom_parser.parse_dom(html, 'a', {'class': 'underilne'}, 'href')
            titles = dom_parser.parse_dom(html, 'a', {'class': 'underilne'})
            items = zip(links, titles)
        else:
            url = urlparse.urljoin(self.base_url, '/search?=%s' % urllib.quote_plus(title))
            data = {'q': title, 'go': 'Search'}
            html = self._http_get(url, data=data, cache_limit=8)
            match = re.search('you can search again in (\d+) seconds', html, re.I)
            if match:
                wait = int(match.group(1))
                if wait > self.timeout: wait = self.timeout
                time.sleep(wait)
                html = self._http_get(url, data=data, cache_limit=0)
                
            pattern = 'class="movie_box.*?href="([^"]+).*?<h1>([^<]+)'
            items = re.findall(pattern, html, re.DOTALL)

        norm_title = scraper_utils.normalize_title(title)
        for item in items:
            url, match_title = item
            if norm_title in scraper_utils.normalize_title(match_title):
                result = {'url': scraper_utils.pathify_url(url), 'title': match_title, 'year': ''}
                results.append(result)

        return results

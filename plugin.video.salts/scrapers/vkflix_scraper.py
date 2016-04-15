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
import urllib
import urlparse

from salts_lib import dom_parser
from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://vkflix.com'
QUALITY_MAP = {'HD': QUALITIES.HIGH, 'DVD': QUALITIES.HIGH, 'TS': QUALITIES.MEDIUM, 'CAM': QUALITIES.LOW}

class MoxieXK_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'VKFlix'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        return '[%s] %s' % (item['quality'], item['host'])

    def get_sources(self, video):
        source_url = self.get_url(video)
        sources = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            if video.video_type == VIDEO_TYPES.EPISODE:
                html = self.__get_episode_fragment(html, video)
            for item in dom_parser.parse_dom(html, 'div', {'class': 'linkTr'}):
                stream_url = dom_parser.parse_dom(item, 'div', {'class': '[^"]*linkHiddenUrl[^"]*'})
                q_str = dom_parser.parse_dom(item, 'div', {'class': '[^"]*linkQualityText[^"]*'})
                if stream_url and q_str:
                    stream_url = stream_url[0]
                    q_str = q_str[0]
                    host = urlparse.urlparse(stream_url).hostname
                    base_quality = QUALITY_MAP.get(q_str, QUALITIES.HIGH)
                    quality = scraper_utils.get_quality(video, host, base_quality)
                    source = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': False}
                    sources.append(source)

        return sources

    def __get_episode_fragment(self, html, video):
        fragment = dom_parser.parse_dom(html, 'div', {'id': 'season%s' % (video.season)})
        if fragment:
            fragment = fragment[0]
            labels = dom_parser.parse_dom(fragment, 'h3')
            pattern = 'Season\s+%s\s+Series?\s+%s$' % (video.season, video.episode)
            for i, label in enumerate(labels):
                match = re.search(pattern, label, re.I)
                if match:
                    fragments = dom_parser.parse_dom(fragment, 'div', {'class': '[^"]*tableLinks[^"]*'})
                    if len(fragments) > i:
                        return fragments[i]
                    else:
                        break
                
        return ''
    
    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year, season=''):
        results = []
        search_url = urlparse.urljoin(self.base_url, '/search?q=')
        search_url += urllib.quote_plus(title)
        html = self._http_get(search_url, cache_limit=1)
        match_year = ''
        for item in dom_parser.parse_dom(html, 'div', {'id': 'movie-\d+'}):
            is_tvshow = dom_parser.parse_dom(item, 'div', {'class': 'movieTV'})
            if (is_tvshow and video_type == VIDEO_TYPES.TVSHOW) or (not is_tvshow and video_type == VIDEO_TYPES.MOVIE):
                fragment = dom_parser.parse_dom(item, 'h4', {'class': '[^"]*showRowName[^"]*'})
                if fragment:
                    match = re.search('href="([^"]+)[^>]+>([^<]+)', fragment[0])
                    if match:
                        match_url, match_title = match.groups()
    
                        if not year or not match_year or year == match_year:
                            result = {'title': scraper_utils.cleanse_title(match_title), 'url': scraper_utils.pathify_url(match_url), 'year': match_year}
                            results.append(result)

        return results

    def _get_episode_url(self, show_url, video):
        url = urlparse.urljoin(self.base_url, show_url)
        html = self._http_get(url, cache_limit=8)
        pattern = '<h3>[^>]*Season\s+%s\s+Series?\s+%s<' % (video.season, video.episode)
        match = re.search(pattern, html, re.I)
        if match:
            return show_url

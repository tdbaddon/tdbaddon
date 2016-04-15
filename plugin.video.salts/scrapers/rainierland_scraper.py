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
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://rainierland.com'
PAGE_LIMIT = 5

class Rainierland_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'Rainierland'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            fragment = dom_parser.parse_dom(html, 'div', {'class': '[^"]*screen[^"]*'})
            if fragment:
                js_src = dom_parser.parse_dom(fragment[0], 'script', ret='src')
                if js_src:
                    js_url = urlparse.urljoin(self.base_url, js_src[0])
                    html = self._http_get(js_url, cache_limit=.5)
                else:
                    html = fragment[0]
                    
                for match in re.finditer('<source[^>]+src="([^"]+)', html):
                    stream_url = match.group(1)
                    host = self._get_direct_hostname(stream_url)
                    if host == 'gvideo':
                        quality = scraper_utils.gv_get_quality(stream_url)
                    else:
                        _, _, height, _ = scraper_utils.parse_movie_link(stream_url)
                        quality = scraper_utils.height_get_quality(height)
                        stream_url += '|User-Agent=%s' % (scraper_utils.get_ua())
                        
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
                    hosters.append(hoster)
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def _get_episode_url(self, show_url, video):
        for page_num in xrange(1, PAGE_LIMIT + 1):
            if page_num > 1:
                page_url = show_url + '/page/' + str(page_num)
            else:
                page_url = show_url
            episode_pattern = 'href="([^"]+season-%s-episode-%s-[^"]*)' % (video.season, video.episode)
            title_pattern = 'class="entry-title".*?href="(?P<url>[^"]+)[^>]+title="[^"]*&#8211;\s*(?P<title>[^"]+)'
            result = self._default_get_episode_url(page_url, video, episode_pattern, title_pattern)
            if result:
                return result
    
    def search(self, video_type, title, year, season=''):
        results = []
        if video_type == VIDEO_TYPES.MOVIE:
            search_url = urlparse.urljoin(self.base_url, '/?s=')
            search_url += urllib.quote_plus('%s' % (title))
            html = self._http_get(search_url, cache_limit=1)
            links = dom_parser.parse_dom(html, 'a', {'class': 'clip-link'}, 'href')
            titles = dom_parser.parse_dom(html, 'a', {'class': 'clip-link'}, 'title')
            matches = zip(links, titles)
        else:
            html = self._http_get(self.base_url, cache_limit=8)
            matches = re.findall('<li\s+class="cat-item[^>]+>\s*<a\s+href="([^"]+)[^>]+>([^<]+)', html)
                
        norm_title = scraper_utils.normalize_title(title)
        for item in matches:
            url, match_title_year = item
            match = re.search('(.*?)\s+\(?(\d{4})\)?', match_title_year)
            if match:
                match_title, match_year = match.groups()
            else:
                match_title = match_title_year
                match_year = ''
            
            if norm_title in scraper_utils.normalize_title(match_title) and (not year or not match_year or year == match_year):
                result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(url)}
                results.append(result)

        return results

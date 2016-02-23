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
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://funtastic-vids.com'

class Funtastic_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'funtastic-vids'

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

            q_str = ''
            match = re.search('class="calishow">([^<]+)', html)
            if match:
                q_str = match.group(1)
            else:
                match = re.search('<a[^>]*href="#embed\d*"[^>]+>([^<]+)', html)
                if match:
                    q_str = match.group(1)
                
            fragment = dom_parser.parse_dom(html, 'div', {'class': 'tab-content'})
            if fragment:
                for source in dom_parser.parse_dom(fragment[0], 'iframe', ret='src'):
                    host = urlparse.urlparse(source).hostname
                    quality = scraper_utils.blog_get_quality(video, q_str, host)
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': source, 'direct': False}
                    hosters.append(hoster)

                fragment = dom_parser.parse_dom(html, 'div', {'id': 'olmt'})
                if fragment:
                    hosters += self.__get_links(video, fragment[0])
                fragment = dom_parser.parse_dom(html, 'div', {'id': 'dlnmt'})
                if fragment:
                    hosters += self.__get_links(video, fragment[0])
            
            hosters = dict((stream['url'], stream) for stream in hosters).values()
        return hosters

    def __get_links(self, video, fragment):
        hosters = []
        for match in re.finditer('href="([^"]+).*?<td>(.*?)</td>\s*</tr>', fragment, re.DOTALL):
            stream_url, q_str = match.groups()
            host = urlparse.urlparse(stream_url).hostname
            quality = scraper_utils.blog_get_quality(video, q_str, host)
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
            hosters.append(hoster)
        return hosters
    
    def get_url(self, video):
        return self._default_get_url(video)

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+/season-%s/episode-%s-[^"]*)' % (video.season, video.episode)
        title_pattern = 'href="(?P<url>[^"]+/season-\d+/episode-\d+-[^"]*)"\s+title="[^-]*-\s*(?P<title>[^"]+)'
        return self._default_get_episode_url(show_url, video, episode_pattern, title_pattern)

    def search(self, video_type, title, year):
        results = []
        temp_results = []
        if video_type == VIDEO_TYPES.MOVIE:
            search_url = urlparse.urljoin(self.base_url, '/?s=')
            search_url += urllib.quote_plus('%s' % (title))
            temp_results = self.__get_movie_results(search_url)
        else:
            search_url = urlparse.urljoin(self.base_url, '/tv-shows/?s=')
            search_url += urllib.quote_plus('%s' % (title))
            temp_results = self.__get_show_results(search_url)
        
        for result in temp_results:
            if not year or not result['year'] or year == result['year']:
                result['url'] = scraper_utils.pathify_url(result['url'])
                results.append(result)

        return results

    def __get_show_results(self, search_url):
        results = []
        html = self._http_get(search_url, cache_limit=.5)
        for item in dom_parser.parse_dom(html, 'li', {'class': 'item'}):
            url = dom_parser.parse_dom(item, 'a', ret='href')
            match_title = dom_parser.parse_dom(item, 'a', ret='title')
            if url and match_title:
                result = {'title': match_title[0], 'year': '', 'url': url[0]}
                results.append(result)
        return results

    def __get_movie_results(self, search_url):
        results = []
        html = self._http_get(search_url, cache_limit=.5)
        for div in dom_parser.parse_dom(html, 'div', {'class': 'col-xs-10'}):
            url = dom_parser.parse_dom(div, 'a', ret='href')
            match_title = dom_parser.parse_dom(div, 'a', ret='title')
            match = re.search('class="main-info-list">\s*Movie\s+of\s+(\d{4})', div)
            if match and url and match_title:
                result = {'title': match_title[0], 'year': match.group(1), 'url': url[0]}
                results.append(result)
        return results

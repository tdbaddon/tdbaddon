"""
    SALTS XBMC Addon
    Copyright (C) 2014 tknorris

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty ofl
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
from salts_lib import log_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://view47.com'
GVIDEO_NAMES = ['picasa']
HOSTS = {'vidag': 'vid.ag', 'videott': 'video.tt'}

class View47_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        if 'www' in self.base_url: self.base_url = BASE_URL  # hack base url to work

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.SEASON, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'view47'

    def resolve_link(self, link):
        if self._get_direct_hostname(link) == 'gvideo':
            return link
        else:
            for source in self.__get_links(link):
                return source
        
    def format_source_label(self, item):
        return '[%s] %s' % (item['quality'], item['host'])

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            fragment = dom_parser.parse_dom(html, 'ul', {'class': 'css_server_new'})
            if fragment:
                for match in re.finditer('href="([^"]+)[^>]*>(.*?)(?:-\d+)?</a>', fragment[0]):
                    url, host = match.groups()
                    host = host.lower()
                    host = re.sub('<img.*?/>', '', host)
                    host = HOSTS.get(host, host)
                    if host in GVIDEO_NAMES:
                        sources = self.__get_links(urlparse.urljoin(self.base_url, url))
                    else:
                        sources = {url: {'quality': scraper_utils.get_quality(video, host, QUALITIES.HIGH), 'direct': False, 'host': host}}
                    
                    for source in sources:
                        direct = sources[source]['direct']
                        quality = sources[source]['quality']
                        host = self._get_direct_hostname(source)
                        if host == 'gvideo':
                            stream_url = source + '|User-Agent=%s' % (scraper_utils.get_ua())
                        else:
                            host = sources[source]['host']
                            stream_url = source
                        hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': direct}
                        hosters.append(hoster)
        return hosters

    def __get_links(self, url):
        html = self._http_get(url, cache_limit=.5)
        sources = self._parse_sources_list(html)
        if not sources:
            fragment = re.search('setup_media(.*?)setup_media', html, re.DOTALL)
            if fragment:
                match = re.search('<iframe[^>]*src="([^"]+)', fragment.group(1))
                if match:
                    stream_url = match.group(1)
                    sources[stream_url] = {'quality': scraper_utils.gv_get_quality(stream_url), 'direct': True}
                    
        return sources
    
    def get_url(self, video):
        return self._default_get_url(video)
    
    def _get_episode_url(self, season_url, video):
        episode_pattern = 'href="([^"]+)[^>]*title="Watch\s+Episode\s+%s"' % (video.episode)
        return self._default_get_episode_url(season_url, video, episode_pattern)
    
    def search(self, video_type, title, year, season=''):
        search_url = urlparse.urljoin(self.base_url, '/search/%s.html' % (urllib.quote_plus(title)))
        html = self._http_get(search_url, cache_limit=.25)
        results = []
        for item in dom_parser.parse_dom(html, 'li', {'class': 'items-\d+-\d+'}):
            match_url = dom_parser.parse_dom(item, 'a', {'class': 'play'}, ret='href')
            match_title = dom_parser.parse_dom(item, 'a', {'class': 'play'}, ret='title')
            year_frag = dom_parser.parse_dom(item, 'span', {'class': 'year'})
            if match_url and match_title:
                match_url = match_url[0]
                match_title = match_title[0]
                is_season = re.search('S(?:eason\s+)?(\d+)$', match_title, re.I)
                if not is_season and video_type == VIDEO_TYPES.MOVIE or is_season and VIDEO_TYPES.SEASON:
                    if video_type == VIDEO_TYPES.MOVIE:
                        if year_frag:
                            match_year = year_frag[0]
                        else:
                            match_year = ''
                    else:
                        if season and int(is_season.group(1)) != int(season):
                            continue
                        match_year = ''
                
                    if (not year or not match_year or year == match_year):
                        result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                        results.append(result)
        return results

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


BASE_URL = 'http://putmv.com'
GK_URL = '/ip.temp/swf/ipplayer/ipplayer.php?u=%s&w=100%%&h=500'
GVIDEO_NAMES = ['english sub', 'picasa', 'putlocker']
XHR = {'X-Requested-With': 'XMLHttpRequest'}
HOSTS = {'vidag': 'vid.ag', 'videott': 'video.tt'}

class PutMV_Scraper(scraper.Scraper):
    base_url = BASE_URL
    
    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.SEASON, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'PutMV'

    def resolve_link(self, link):
        if self.base_url in link:
            sources = self.__get_links(link)
            if sources: return sources.items()[0][0]
        else:
            return link

    def format_source_label(self, item):
        return '[%s] %s' % (item['quality'], item['host'])

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.5)
            fragment = dom_parser.parse_dom(html, 'ul', {'class': 'css_server_new'})
            if fragment:
                for match in re.finditer('href="([^"]+).*?/>(.*?)(?:-\d+)?</a>', fragment[0]):
                    url, host = match.groups()
                    host = host.lower()
                    host = HOSTS.get(host, host)
                    if host in GVIDEO_NAMES:
                        sources = self.__get_links(urlparse.urljoin(self.base_url, url))
                    else:
                        sources = {url: {'quality': scraper_utils.get_quality(video, host, QUALITIES.HIGH), 'direct': False, 'host': host}}
                    
                    for source in sources:
                        direct = sources[source]['direct']
                        quality = sources[source]['quality']
                        host = sources[source]['host']
                        stream_url = source if not direct else source + '|User-Agent=%s' % (scraper_utils.get_ua())
                        hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': direct}
                        hosters.append(hoster)
            
        return hosters

    def __get_links(self, url):
        sources = {}
        html = self._http_get(url, cache_limit=.5)
        match = re.search("files\s*:\s*'([^']+)", html)
        if match:
            gk_url = GK_URL % (match.group(1))
            gk_url = urlparse.urljoin(self.base_url, gk_url)
            headers = XHR
            headers['Referer'] = url
            html = self._http_get(gk_url, headers=headers, cache_limit=.5)
            try: html = html.decode('utf-8-sig')
            except: pass
            js_data = scraper_utils.parse_json(html, gk_url)
            if 'data' in js_data:
                if isinstance(js_data['data'], list):
                    stream_list = [item['files'] for item in js_data['data']]
                else:
                    stream_list = [js_data['data']]
                
                for stream_url in stream_list:
                    host = self._get_direct_hostname(stream_url)
                    if host == 'gvideo':
                        sources = {stream_url: {'quality': scraper_utils.gv_get_quality(stream_url), 'direct': True, 'host': host}}
                    else:
                        host = urlparse.urlparse(stream_url).hostname
                        sources = {stream_url: {'quality': QUALITIES.HIGH, 'direct': False, 'host': host}}
                    
        return sources
    
    def get_url(self, video):
        return self._default_get_url(video)

    def _get_episode_url(self, season_url, video):
        episode_pattern = 'href="([^"]+)[^>]*title="Watch\s+Episode\s+%s"' % (video.episode)
        return self._default_get_episode_url(season_url, video, episode_pattern)
    
    def search(self, video_type, title, year, season=''):
        search_url = urlparse.urljoin(self.base_url, '/search/%s.html' % urllib.quote_plus(title))
        html = self._http_get(search_url, cache_limit=.25)
        results = []
        fragment = dom_parser.parse_dom(html, 'div', {'class': 'list-movie'})
        if fragment:
            for item in dom_parser.parse_dom(fragment[0], 'div', {'class': 'movie'}):
                match = re.search('class="movie-name".*?href="([^"]+)[^>]+>([^<]+)', item)
                if match:
                    url, match_title = match.groups()
                    is_season = re.search('\s+-\s+[Ss](\d+)$', match_title)
                    if not is_season and video_type == VIDEO_TYPES.MOVIE or is_season and VIDEO_TYPES.SEASON:
                        match_year = ''
                        if video_type == VIDEO_TYPES.MOVIE:
                            for info_frag in dom_parser.parse_dom(item, 'p', {'class': 'info'}):
                                match = re.search('(\d{4})', info_frag)
                                if match:
                                    match_year = match.group(1)
                                    break
                            
                            if not match_year:
                                match = re.search('(\d{4})$', url)
                                if match:
                                    match_year = match.group(1)
                        else:
                            if season and int(is_season.group(1)) != int(season):
                                continue
                                
                        if (not year or not match_year or year == match_year):
                            result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                            results.append(result)
        
        return results

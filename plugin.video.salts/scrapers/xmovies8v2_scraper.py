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
import time
import kodi
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
from salts_lib.constants import XHR
import scraper

BASE_URL = 'http://xmovies8.tv'
PLAYER_URL = '/ajax/movie/load_player_v2'
EPISODES_URL = '/ajax/movie/load_episodes_v2'

class Scraper(scraper.Scraper):
    base_url = BASE_URL
    
    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.SEASON, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'xmovies8.v2'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        sources = {}
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.5)
            html = self.__get_players(html, page_url)
            players = list(set(re.findall("load_player\(\s*'([^']+)'\s*,\s*'?(\d+)\s*'?", html)))
            player_url = urlparse.urljoin(self.base_url, PLAYER_URL)
            for link_id, height in players:
                headers = {'Referer': page_url, 'Server': 'cloudflare-nginx', 'Accept': 'text/html, */*; q=0.01',
                           'Accept-Language': 'en-US,en;q=0.5', 'Accept-Formating': 'application/json, text/javascript', 'Accept-Encoding': 'gzip, deflate'}
                headers.update(XHR)
                params = {'id': link_id, 'quality': height, '_': self.__make_token()}
                html = self._http_get(player_url, params=params, headers=headers, cache_limit=1)
                js_data = scraper_utils.parse_json(html, player_url)
                if js_data.get('playlist', ''):
                    link_url = js_data['playlist']
                else:
                    link_url = js_data.get('link', '')
                    
                if link_url:
                    headers = {'Referer': page_url, 'Origin': self.base_url}
                    html = self._http_get(link_url, headers=headers, allow_redirect=False, method='HEAD', cache_limit=0)
                    if html.startswith('http'):
                        streams = [html]
                    else:
                        html = self._http_get(link_url, headers=headers, cache_limit=0)
                        js_data = scraper_utils.parse_json(html, link_url)
                        try: streams = [source['file'] for source in js_data['playlist'][0]['sources']]
                        except: streams = []
                        
                    for stream in streams:
                        if self._get_direct_hostname(stream) == 'gvideo':
                            quality = scraper_utils.gv_get_quality(stream)
                            sources[stream] = {'quality': quality, 'direct': True}
                        else:
                            if height != '0':
                                quality = scraper_utils.height_get_quality(height)
                            else:
                                quality = QUALITIES.HIGH
                            sources[stream] = {'quality': quality, 'direct': False}
                    
            for source in sources:
                direct = sources[source]['direct']
                quality = sources[source]['quality']
                if direct:
                    host = self._get_direct_hostname(source)
                else:
                    host = urlparse.urlparse(source).hostname

                stream_url = source + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': direct}
                hosters.append(hoster)
            
        return hosters

    def __get_players(self, html, page_url):
        url = urlparse.urljoin(self.base_url, EPISODES_URL)
        match = re.search("data\s*:\s*{\s*id:\s*(\d+),\s*episode_id:\s*(\d+),\s*link_id:\s*(\d+)", html)
        if match:
            show_id, ep_id, link_id = match.groups()
            params = {'id': show_id, 'episode_id': ep_id, 'link_id': link_id, '_': self.__make_token()}
            headers = {'Referer': page_url, 'Server': 'cloudflare-nginx', 'Accept': 'text/html, */*; q=0.01',
                       'Accept-Language': 'en-US,en;q=0.5', 'Accept-Formating': 'application/json, text/javascript'}
            headers.update(XHR)
            html = self._http_get(url, params=params, headers=headers, cache_limit=1)
        return html
    
    def __make_token(self):
        token = int(time.time()) / 60 * 60
        token = token * 1000 + (token % 1000)
        return token
        
    def _get_episode_url(self, season_url, video):
        season_url = urlparse.urljoin(self.base_url, season_url)
        html = self._http_get(season_url, cache_limit=.5)
        fragment = dom_parser.parse_dom(html, 'div', {'class': '[^"]*ep_link[^"]*'})
        if fragment:
            episode_pattern = 'href="([^"]+)[^>]+>(?:Episode)?\s*0*%s<' % (video.episode)
            match = re.search(episode_pattern, fragment[0])
            if match:
                return scraper_utils.pathify_url(match.group(1))

    def search(self, video_type, title, year, season=''):
        results = []
        search_url = urlparse.urljoin(self.base_url, '/movies/search')
        html = self._http_get(search_url, params={'s': title}, cache_limit=8)
        for item in dom_parser.parse_dom(html, 'div', {'class': 'item_movie'}):
            match_title_year = dom_parser.parse_dom(item, 'a', ret='title')
            match_url = dom_parser.parse_dom(item, 'a', ret='href')
            if match_title_year and match_url:
                match_title_year = match_title_year[0]
                match_url = match_url[0]
                is_season = re.search('Season\s+\d+', match_title_year, re.I)
                if (video_type == VIDEO_TYPES.MOVIE and not is_season) or (video_type == VIDEO_TYPES.SEASON and is_season):
                    match_year = ''
                    if video_type == VIDEO_TYPES.SEASON:
                        match_title = match_title_year
                        if season and not re.search('Season\s+(%s)\s+' % (season), match_title_year, re.I):
                            continue
                    else:
                        match_title, match_year = scraper_utils.extra_year(match_title_year)
        
                    match_url = urlparse.urljoin(match_url, 'watching.html')
                    if not year or not match_year or year == match_year:
                        result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                        results.append(result)
        return results

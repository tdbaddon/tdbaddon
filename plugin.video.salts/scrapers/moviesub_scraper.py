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
import kodi
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://moviesub.org'
LINK_URL = '/ip.temp/swf/plugins/ipplugins.php'
LINK_URL2 = '/Htplugins/Loader.php'
LINK_URL3 = '/ip.temp/swf/ipplayer/ipplayer.php'
XHR = {'X-Requested-With': 'XMLHttpRequest'}

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
        return 'MovieSub'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        sources = {}
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            sources = self.__get_gk_links(html, url)
            sources.update(self.__get_ht_links(html, url))
            
            for source in sources:
                host = self._get_direct_hostname(source)
                if host == 'gvideo':
                    direct = True
                else:
                    host = urlparse.urlparse(source).hostname
                    direct = False
                
                if host is not None:
                    stream_url = source + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': sources[source], 'views': None, 'rating': None, 'url': stream_url, 'direct': direct}
                    hosters.append(hoster)

        return hosters

    def __get_ht_links(self, html, page_url):
        sources = {}
        match = re.search('Htplugins_Make_Player\("([^"]+)', html)
        if match:
            data = {'data': match.group(1)}
            url = urlparse.urljoin(self.base_url, LINK_URL2)
            headers = {'Referer': page_url}
            html = self._http_get(url, data=data, headers=headers, cache_limit=.25)
            js_data = scraper_utils.parse_json(html, url)
            if 'l' in js_data:
                for link in js_data['l']:
                    if self._get_direct_hostname(link) == 'gvideo':
                        quality = scraper_utils.gv_get_quality(link)
                    else:
                        quality = QUALITIES.HIGH
                    sources[link] = quality
        return sources
        
    def __get_gk_links(self, html, page_url):
        sources = {}
        for link in dom_parser.parse_dom(html, 'div', {'class': '[^"]*server_line[^"]*'}):
            film_id = dom_parser.parse_dom(link, 'a', ret='data-film')
            name_id = dom_parser.parse_dom(link, 'a', ret='data-name')
            server_id = dom_parser.parse_dom(link, 'a', ret='data-server')
            if film_id and name_id and server_id:
                data = {'ipplugins': 1, 'ip_film': film_id[0], 'ip_server': server_id[0], 'ip_name': name_id[0]}
                headers = {'Referer': page_url}
                headers.update(XHR)
                url = urlparse.urljoin(self.base_url, LINK_URL)
                html = self._http_get(url, data=data, headers=headers, cache_limit=.25)
                js_data = scraper_utils.parse_json(html, url)
                if 's' in js_data and isinstance(js_data['s'], basestring):
                    url = urlparse.urljoin(self.base_url, LINK_URL3)
                    params = {'u': js_data['s'], 'w': '100%', 'h': 450, 's': js_data['v']}
                    html = self._http_get(url, params=params, headers=headers, cache_limit=.25)
                    js_data = scraper_utils.parse_json(html, url)
                    if 'data' in js_data and js_data['data']:
                        if isinstance(js_data['data'], basestring):
                            sources[js_data['data']] = QUALITIES.HIGH
                        else:
                            for link in js_data['data']:
                                stream_url = link['files']
                                if self._get_direct_hostname(stream_url) == 'gvideo':
                                    quality = scraper_utils.gv_get_quality(stream_url)
                                elif 'quality' in link:
                                    quality = scraper_utils.height_get_quality(link['quality'])
                                else:
                                    quality = QUALITIES.HIGH
                                sources[stream_url] = quality
                    
        return sources

    def _get_episode_url(self, season_url, video):
        season_url = urlparse.urljoin(self.base_url, season_url)
        episode_pattern = 'href="([^"]+)[^>]*title="Watch\s+Episode\s+\d+[^>]*>%s<' % (video.episode)
        return self._default_get_episode_url(season_url, video, episode_pattern)
    
    def search(self, video_type, title, year, season=''):
        results = []
        search_url = urlparse.urljoin(self.base_url, '/search/%s.html' % (urllib.quote_plus(title)))
        html = self._http_get(search_url, cache_limit=1)
        fragment = dom_parser.parse_dom(html, 'ul', {'class': 'cfv'})
        if fragment:
            for item in dom_parser.parse_dom(fragment[0], 'li'):
                is_season = dom_parser.parse_dom(item, 'div', {'class': 'status'})
                if (not is_season and video_type == VIDEO_TYPES.MOVIE) or (is_season and video_type == VIDEO_TYPES.SEASON):
                    match_url = dom_parser.parse_dom(item, 'a', ret='href')
                    match_title = dom_parser.parse_dom(item, 'a', ret='title')
                    if match_url and match_title:
                        match_title = match_title[0]
                        match_url = match_url[0]
                        match_year = ''
                        if video_type == VIDEO_TYPES.SEASON:
                            if season and not re.search('Season\s+%s$' % (season), match_title, re.I):
                                continue
                        else:
                            match = re.search('-(\d{4})\.html', match_url)
                            if match:
                                match_year = match.group(1)
                        
                        if not year or not match_year or year == match_year:
                            result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                            results.append(result)

        return results

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
import random
from salts_lib import dom_parser
from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://fmovies.to'
HASH_URL = '/ajax/episode/info'
Q_MAP = {'TS': QUALITIES.LOW, 'CAM': QUALITIES.LOW, 'HDTS': QUALITIES.LOW, 'HD 720P': QUALITIES.HD720}
XHR = {'X-Requested-With': 'XMLHttpRequest'}
MAX_SOURCES = 5

class NineMovies_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.SEASON, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return '9Movies'

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
            for server_list in dom_parser.parse_dom(html, 'ul', {'class': 'episodes'}):
                labels = dom_parser.parse_dom(server_list, 'a')
                hash_ids = dom_parser.parse_dom(server_list, 'a', ret='data-id')
                for label, hash_id in zip(labels, hash_ids):
                    if video.video_type == VIDEO_TYPES.EPISODE and not self.__episode_match(label, video.episode):
                        continue
                    
                    hash_url = urlparse.urljoin(self.base_url, HASH_URL)
                    query = {'id': hash_id, 'update': '0'}
                    query.update(self.__get_token(query))
                    hash_url = hash_url + '?' + urllib.urlencode(query)
                    headers = XHR
                    headers['Referer'] = url
                    html = self._http_get(hash_url, headers=headers, cache_limit=.5)
                    js_data = scraper_utils.parse_json(html, hash_url)
                    sources = {}
                    link_type = js_data.get('type')
                    target = js_data.get('target')
                    grabber = js_data.get('grabber')
                    params = js_data.get('params')
                    if link_type == 'iframe' and target:
                        sources[target] = {'direct': False, 'quality': QUALITIES.HD720}
                    elif grabber and params:
                        sources = self.__grab_links(grabber, params, url)
                        
                    for source in sources:
                        direct = sources[source]['direct']
                        quality = sources[source]['quality']
                        if direct:
                            host = self._get_direct_hostname(source)
                        else:
                            host = urlparse.urlparse(source).hostname
                        hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': source, 'direct': direct}
                        hosters.append(hoster)
        return hosters

    def __grab_links(self, grab_url, query, referer):
        try:
            sources = {}
            query['mobile'] = '0'
            query.update(self.__get_token(query))
            grab_url = grab_url + '?' + urllib.urlencode(query)
            headers = XHR
            headers['Referer'] = referer
            html = self._http_get(grab_url, headers=headers, cache_limit=.5)
            js_data = scraper_utils.parse_json(html, grab_url)
            if 'data' in js_data:
                for link in js_data['data']:
                    stream_url = link['file']
                    if self._get_direct_hostname(stream_url) == 'gvideo':
                        quality = scraper_utils.gv_get_quality(stream_url)
                    elif 'label' in link:
                        quality = scraper_utils.height_get_quality(link['label'])
                    else:
                        quality = QUALITIES.HIGH
                    sources[stream_url] = {'direct': True, 'quality': quality}
        except Exception as e:
            log_utils.log('9Movies Link Parse Error: %s' % (e), log_utils.LOGWARNING)
                
        return sources
    
    def __get_token(self, data):
        n = 0
        for key in data:
            if not key.startswith('_'):
                for i, c in enumerate(data[key]):
                    n += ord(c) * (i + 1990)
        return {'_token': hex(n)[2:]}
                
    def get_url(self, video):
        return self._default_get_url(video)

    def _get_episode_url(self, season_url, video):
        url = urlparse.urljoin(self.base_url, season_url)
        html = self._http_get(url, cache_limit=8)
        fragment = dom_parser.parse_dom(html, 'ul', {'class': 'episodes'})
        if fragment:
            for link in dom_parser.parse_dom(fragment[0], 'a'):
                if self.__episode_match(link, video.episode):
                    return season_url
    
    def __episode_match(self, label, episode):
        try: link = int(label)
        except: link = -1
        return link == int(episode)
        
    def search(self, video_type, title, year, season=''):
        search_url = urlparse.urljoin(self.base_url, '/search?keyword=%s' % (urllib.quote_plus(title)))
        html = self._http_get(search_url, cache_limit=1)
        results = []
        match_year = ''
        fragment = dom_parser.parse_dom(html, 'div', {'class': '[^"]*movie-list[^"]*'})
        if fragment:
            for item in dom_parser.parse_dom(fragment[0], 'div', {'class': 'item'}):
                links = dom_parser.parse_dom(item, 'a', {'class': 'name'}, ret='href')
                titles = dom_parser.parse_dom(item, 'a', {'class': 'name'})
                is_season = dom_parser.parse_dom(item, 'div', {'class': 'status'})
                for match_url, match_title in zip(links, titles):
                    if (not is_season and video_type == VIDEO_TYPES.MOVIE) or (is_season and video_type == VIDEO_TYPES.SEASON):
                        if video_type == VIDEO_TYPES.SEASON:
                            if season and not re.search('\s+%s$' % (season), match_title): continue
                            
                        if not year or not match_year or year == match_year:
                            result = {'title': scraper_utils.cleanse_title(match_title), 'year': '', 'url': scraper_utils.pathify_url(match_url)}
                            results.append(result)

        return results

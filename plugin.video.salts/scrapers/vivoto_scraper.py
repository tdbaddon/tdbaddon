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

BASE_URL = 'http://vivo.to'
LINK_URL = '/ip.temp/swf/plugins/ipplugins.php'
PLAYER_URL = '/ip.temp/swf/ipplayer/ipplayer.php'
XHR = {'X-Requested-With': 'XMLHttpRequest'}
QUALITY_MAP = {'HD': QUALITIES.HD720, 'SD': QUALITIES.HIGH}

class Scraper(scraper.Scraper):
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
        return 'vivo.to'

    def resolve_link(self, link):
        if self.base_url in link:
            html = self._http_get(link, cache_limit=.5)
            match = re.search('<iframe[^>]*src="([^"]+)', html)
            if match:
                link = match.group(1)

        return link
        
    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            page_quality = dom_parser.parse_dom(html, 'dd', {'class': 'status'})
            if page_quality:
                page_quality = QUALITY_MAP.get(page_quality[0], QUALITIES.HIGH)
            else:
                page_quality = QUALITIES.HIGH
            
            sources = self.__get_gk_links(html, url, page_quality)
            for source in sources:
                host = self._get_direct_hostname(source)
                if host == 'gvideo':
                    direct = True
                    quality = sources[source]
                else:
                    host = urlparse.urlparse(source).hostname
                    quality = scraper_utils.get_quality(video, host, sources[source])
                    direct = False

                if host is not None:
                    stream_url = source + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': direct}
                    hosters.append(hoster)

        return hosters

    def __get_gk_links(self, html, page_url, page_quality):
        sources = {}
        fragment = dom_parser.parse_dom(html, 'div', {'id': 'load_server'})
        if fragment:
            for link in dom_parser.parse_dom(fragment[0], 'li'):
                film_id = dom_parser.parse_dom(link, 'a', ret='data-film')
                name_id = dom_parser.parse_dom(link, 'a', ret='data-name')
                server_id = dom_parser.parse_dom(link, 'a', ret='data-server')
                if film_id and name_id and server_id:
                    data = {'ipplugins': 1, 'ip_film': film_id[0], 'ip_server': server_id[0], 'ip_name': name_id[0]}
                    headers = XHR
                    headers['Referer'] = page_url
                    url = urlparse.urljoin(self.base_url, LINK_URL)
                    html = self._http_get(url, data=data, headers=headers, cache_limit=.25)
                    js_data = scraper_utils.parse_json(html, url)
                    if 's' in js_data:
                        if isinstance(js_data['s'], basestring):
                            stream_urls = self.__get_real_url(js_data['s'])
                            if stream_urls is not None:
                                if isinstance(stream_urls, basestring):
                                    sources[stream_urls] = page_quality
                                else:
                                    for item in stream_urls:
                                        stream_url = item['files']
                                        if self._get_direct_hostname(stream_url) == 'gvideo':
                                            quality = scraper_utils.gv_get_quality(stream_url)
                                        elif 'quality' in item:
                                            quality = scraper_utils.height_get_quality(item['quality'])
                                        else:
                                            quality = page_quality
                                        sources[stream_url] = quality
                        else:
                            for link in js_data['s']:
                                stream_url = self.__get_real_url(link['file'])
                                if stream_url is not None:
                                    if self._get_direct_hostname(stream_url) == 'gvideo':
                                        quality = scraper_utils.gv_get_quality(stream_url)
                                    elif 'label' in link:
                                        quality = scraper_utils.height_get_quality(link['label'])
                                    else:
                                        quality = page_quality
                                    sources[stream_url] = quality
        return sources
    
    def __get_real_url(self, stream_url):
        if not stream_url.startswith('http'):
            url = urlparse.urljoin(self.base_url, PLAYER_URL)
            params = {'u': stream_url, 'w': '100%', 'h': 420}
            html = self._http_get(url, params=params, headers=XHR, cache_limit=.25)
            js_data = scraper_utils.parse_json(html, url)
            if 'data' in js_data and js_data['data']:
                if 'files' in js_data['data'] and js_data['data']['files']:
                    return js_data['data']['files']
                elif js_data['data']:
                    return js_data['data']

        return None
    
    def _get_episode_url(self, season_url, video):
        episode_pattern = 'href="([^"]+)[^>]*title="Watch\s+Episode\s+%s"' % (video.episode)
        return self._default_get_episode_url(season_url, video, episode_pattern)
    
    def search(self, video_type, title, year, season=''):
        search_url = urlparse.urljoin(self.base_url, '/search/%s.html')
        search_url = search_url % (urllib.quote_plus(title))
        html = self._http_get(search_url, cache_limit=1)
        results = []
        fragment = dom_parser.parse_dom(html, 'div', {'class': 'movie'})
        if fragment:
            for item in dom_parser.parse_dom(fragment[0], 'li'):
                match_url = dom_parser.parse_dom(item, 'a', ret='href')
                match_title = dom_parser.parse_dom(item, 'span', {'class': 'text'})
                match_year = dom_parser.parse_dom(item, 'span', {'class': 'year'})
                if match_url and match_title:
                    match_url = match_url[0]
                    match_title = re.sub('</?strong>', '', match_title[0])
                    is_season = re.search('Season\s+(\d+)$', match_title, re.I)
                    if (not is_season and video_type == VIDEO_TYPES.MOVIE) or (is_season and video_type == VIDEO_TYPES.SEASON):
                        if video_type == VIDEO_TYPES.MOVIE:
                            if match_year:
                                match_year = match_year[0]
                            else:
                                match_year = ''
                        else:
                            if season and int(is_season.group(1)) != int(season):
                                continue
                            match_year = ''
                    
                        if not year or not match_year or year == match_year:
                            result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                            results.append(result)
        return results

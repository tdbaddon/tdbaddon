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
import base64
from salts_lib import dom_parser
from salts_lib import kodi
from salts_lib import scraper_utils
from salts_lib import log_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://tunemovie.is'
LINK_URL = '/ip.temp/swf/plugins/ipplugins.php'
XHR = {'X-Requested-With': 'XMLHttpRequest'}
GK_KEY = base64.b64decode('Q05WTmhPSjlXM1BmeFd0UEtiOGg=')

class TuneMovie_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.SEASON, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'tunemovie'

    def resolve_link(self, link):
        if self.base_url in link:
            html = self._http_get(link, cache_limit=0)
            fragment = dom_parser.parse_dom(html, 'div', {'id': 'player'})
            if fragment:
                match = re.search('<iframe[^>]*src="([^"]+)', fragment[0])
                if match:
                    link = match.group(1)

        return link

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        if 'views' in item and item['views']:
            label += ' (%s views)' % item['views']
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        sources = {}
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            sources = self.__get_gk_links(html, url)
            if not sources:
                sources = self.__get_gk_links2(html)
            
            sources.update(self.__get_iframe_links(html))
            
            for source in sources:
                host = self._get_direct_hostname(source)
                if host == 'gvideo':
                    direct = True
                    quality = sources[source]
                    stream_url = source + '|User-Agent=%s' % (scraper_utils.get_ua())
                else:
                    direct = False
                    stream_url = source
                    if self.base_url in source:
                        host = sources[source]
                        quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
                    else:
                        host = urlparse.urlparse(source).hostname
                        quality = sources[source]
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': direct}
                hosters.append(hoster)

        return hosters

    def __get_iframe_links(self, html):
        sources = {}
        fragment = dom_parser.parse_dom(html, 'div', {'id': 'total_version'})
        if fragment:
            names = dom_parser.parse_dom(fragment[0], 'p', {'class': 'server_servername'})
            links = dom_parser.parse_dom(fragment[0], 'p', {'class': 'server_play'})
            for name, link in zip(names, links):
                name = name.replace('Server ', '')
                match = re.search('href="([^"]+)', link)
                if match:
                    sources[match.group(1)] = name.lower()
        return sources
    
    def __get_gk_links(self, html, page_url):
        sources = {}
        for link in dom_parser.parse_dom(html, 'div', {'class': '[^"]*server_line[^"]*'}):
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
                        sources[js_data['s']] = QUALITIES.HIGH
                    else:
                        for link in js_data['s']:
                            stream_url = link['file']
                            if self._get_direct_hostname(stream_url) == 'gvideo':
                                quality = scraper_utils.gv_get_quality(stream_url)
                            elif 'label' in link:
                                quality = scraper_utils.height_get_quality(link['label'])
                            else:
                                quality = QUALITIES.HIGH
                            sources[stream_url] = quality
        return sources

    def __get_gk_links2(self, html):
        sources = {}
        match = re.search('base64\.decode\("([^"]+)', html, re.I)
        if match:
            match = re.search('proxy\.link=tunemovie\*([^&]+)', base64.b64decode(match.group(1)))
            if match:
                picasa_url = scraper_utils.gk_decrypt(self.get_name(), GK_KEY, match.group(1))
                g_links = self._parse_google(picasa_url)
                for link in g_links:
                    sources[link] = scraper_utils.gv_get_quality(link)
                
        return sources

    def get_url(self, video):
        return self._default_get_url(video)

    def _get_episode_url(self, season_url, video):
        episode_pattern = 'class="[^"]*episode_series_link[^"]*"\s+href="([^"]+)[^>]*>\s*%s\s*<' % (video.episode)
        return self._default_get_episode_url(season_url, video, episode_pattern)
    
    def search(self, video_type, title, year, season=''):
        search_url = urlparse.urljoin(self.base_url, '/search-movies/%s.html')
        search_url = search_url % (urllib.quote_plus(title))
        html = self._http_get(search_url, cache_limit=0)
        results = []
        for thumb in dom_parser.parse_dom(html, 'div', {'class': 'thumb'}):
            match_title = dom_parser.parse_dom(thumb, 'a', {'class': 'clip-link'}, ret='title')
            url = dom_parser.parse_dom(thumb, 'a', {'class': 'clip-link'}, ret='href')
            if match_title and url:
                match_title, url = match_title[0], url[0]
                is_season = re.search('Season\s+(\d+)$', match_title, re.I)
                if not is_season and video_type == VIDEO_TYPES.MOVIE or is_season and VIDEO_TYPES.SEASON:
                    match_year = ''
                    if video_type == VIDEO_TYPES.MOVIE:
                        match_year = dom_parser.parse_dom(thumb, 'div', {'class': '[^"]*status-year[^"]*'})
                        if match_year:
                            match_year = match_year[0]
                    else:
                        if season and int(is_season.group(1)) != int(season):
                            continue
                    
                    if not year or not match_year or year == match_year:
                        result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                        results.append(result)
        return results

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
from salts_lib.kodi import i18n
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://www.moviesub.net'
BASE_URL2 = 'http://www.moviesub.tv'
LINK_URL = '/ip.temp/swf/plugins/ipplugins.php'
LINK_URL2 = '/Htplugins/Loader.php'
XHR = {'X-Requested-With': 'XMLHttpRequest'}

class MovieSub_Scraper(scraper.Scraper):
    base_url = BASE_URL
    tv_base_url = BASE_URL2

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.tv_base_url = kodi.get_setting('%s-base_url2' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.SEASON, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'MovieSub'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        sources = {}
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.__get_base_url(video.video_type), source_url)
            html = self._http_get(url, cache_limit=.5)
            sources = self.__get_gk_links(html, url, video.video_type, video.episode)
            sources.update(self.__get_ht_links(html, url, video.video_type))
            
            for source in sources:
                host = self._get_direct_hostname(source)
                if host == 'gvideo':
                    direct = True
                else:
                    host = urlparse.urlparse(source).hostname
                    direct = False
                
                if host is not None:
                    stream_url = source + '|User-Agent=%s' % (scraper_utils.get_ua())
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': sources[source], 'views': None, 'rating': None, 'url': stream_url, 'direct': direct}
                    hosters.append(hoster)

        return hosters

    def __get_ht_links(self, html, page_url, video_type):
        sources = {}
        match = re.search('Htplugins_Make_Player\("([^"]+)', html)
        if match:
            data = {'data': match.group(1)}
            url = urlparse.urljoin(self.__get_base_url(video_type), LINK_URL2)
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
        
    def __get_gk_links(self, html, page_url, video_type, episode):
        sources = {}
        phimid = dom_parser.parse_dom(html, 'input', {'name': 'phimid'}, ret='value')
        if phimid and video_type == VIDEO_TYPES.EPISODE:
            url = urlparse.urljoin(self.tv_base_url, '/ajax.php')
            data = {'ipos_server': 1, 'phimid': phimid[0], 'keyurl': episode}
            headers = XHR
            headers['Referer'] = page_url
            html = self._http_get(url, data=data, headers=headers, cache_limit=.5)
            
        for link in dom_parser.parse_dom(html, 'div', {'class': '[^"]*server_line[^"]*'}):
            film_id = dom_parser.parse_dom(link, 'a', ret='data-film')
            name_id = dom_parser.parse_dom(link, 'a', ret='data-name')
            server_id = dom_parser.parse_dom(link, 'a', ret='data-server')
            if film_id and name_id and server_id:
                data = {'ipplugins': 1, 'ip_film': film_id[0], 'ip_server': server_id[0], 'ip_name': name_id[0]}
                headers = XHR
                headers['Referer'] = page_url
                url = urlparse.urljoin(self.__get_base_url(video_type), LINK_URL)
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

    def get_url(self, video):
        return self._default_get_url(video)

    def _get_episode_url(self, season_url, video):
        season_url = urlparse.urljoin(self.__get_base_url(video.video_type), season_url)
        episode_pattern = 'href="([^"]+)[^>]*title="Watch\s+Episode\s+\d+[^>]*>%s<' % (video.episode)
        return self._default_get_episode_url(season_url, video, episode_pattern)
    
    def search(self, video_type, title, year, season=''):
        results = []
        search_url = urlparse.urljoin(self.__get_base_url(video_type), '/search/%s.html' % (urllib.quote_plus(title)))
        html = self._http_get(search_url, cache_limit=1)
        fragment = dom_parser.parse_dom(html, 'ul', {'class': 'cfv'})
        if fragment:
            for item in dom_parser.parse_dom(fragment[0], 'li'):
                is_season = dom_parser.parse_dom(item, 'div', {'class': 'status'})
                if not is_season and video_type == VIDEO_TYPES.MOVIE or is_season and VIDEO_TYPES.SEASON:
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

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        name = cls.get_name()
        settings.append('         <setting id="%s-base_url2" type="text" label="    %s %s" default="%s" visible="eq(-4,true)"/>' % (name, i18n('tv_shows'), i18n('base_url'), cls.tv_base_url))
        return settings
    
    def __get_base_url(self, video_type):
        if video_type in [VIDEO_TYPES.SEASON, VIDEO_TYPES.EPISODE]:
            base_url = self.tv_base_url
        else:
            base_url = self.base_url
        return base_url

# -*- coding: utf-8 -*-
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
import kodi
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib import jsunpack
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
import scraper

BASE_URL = 'http://www.yabancidizi.net'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'YabanciDizi'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        sources = {}
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.05)
            sources = self.__get_sources(html, page_url)
             
            pages = []
            fragment = dom_parser.parse_dom(html, 'div', {'class': 'player-options'})
            if fragment:
                for li in dom_parser.parse_dom(fragment[0], 'li', {'class': ''}):
                    match = re.search('href="([^"]+)', li)
                    if match and match.group(1).startswith('http'):
                        pages.append(match.group(1))
            
            for page in pages:
                page_url = urlparse.urljoin(self.base_url, page)
                html = self._http_get(page_url, cache_limit=.05)
                sources.update(self.__get_sources(html, page_url))
            
        for source in sources:
            host = self._get_direct_hostname(source)
            if host == 'gvideo':
                quality = scraper_utils.gv_get_quality(source)
                direct = True
            elif sources[source]['direct']:
                quality = sources[source]['quality']
                direct = True
            else:
                quality = sources[source]['quality']
                direct = False
                host = urlparse.urlparse(source).hostname
            
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': source, 'direct': direct}
            if sources[source]['subs']: hoster['subs'] = 'Turkish Subtitles'
            hosters.append(hoster)
                
        return hosters

    def __get_sources(self, html, page_url):
        sources = {}
        subs = re.search('''"?kind"?\s*:\s*"?captions"?''', html) or 'ngilizce' in page_url
        for match in re.finditer('(eval\(function\(.*?)</script>', html, re.DOTALL):
            js_data = jsunpack.unpack(match.group(1))
            js_data = js_data.replace('\\', '')
            temp_sources = self._parse_sources_list(js_data)
            for source in temp_sources:
                temp_sources[source]['subs'] = subs
                if self._get_direct_hostname(source) == 'gvideo':
                    sources[source] = temp_sources[source]
                else:
                    headers = {'Referer': page_url}
                    redir_url = self._http_get(source, headers=headers, allow_redirect=False, method='HEAD')
                    if redir_url.startswith('http'):
                        sources[redir_url] = temp_sources[source]
        
        iframe_url = dom_parser.parse_dom(html, 'iframe', ret='src')
        if iframe_url:
            iframe_url = iframe_url[0]
            if self._get_direct_hostname(iframe_url) == 'gvideo':
                direct = True
            else:
                direct = False
            sources[iframe_url] = {'direct': direct, 'subs': subs, 'quality': QUALITIES.HD720}
            
        return sources
    
    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+/sezon-%s/bolum-%s(?!\d)[^"]*)"' % (video.season, video.episode)
        return self._default_get_episode_url(show_url, video, episode_pattern)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, cache_limit=48)
        norm_title = scraper_utils.normalize_title(title)
        for series in dom_parser.parse_dom(html, 'div', {'class': 'series-item'}):
            match_url = dom_parser.parse_dom(series, 'a', ret='href')
            match_title = dom_parser.parse_dom(series, 'h3')
            match_year = dom_parser.parse_dom(series, 'p')
            if match_url and match_title:
                match_url = match_url[0]
                match_title = match_title[0]
                if match_year:
                    match = re.search('\s*(\d{4})\s+', match_year[0])
                    if match:
                        match_year = match.group(1)
                    else:
                        match_year = ''
                else:
                    match_year = ''
                    
                if norm_title in scraper_utils.normalize_title(match_title):
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)

        return results

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
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://dizimag.co'
XHR = {'X-Requested-With': 'XMLHttpRequest'}

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
        return 'Dizimag'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.5)
            # exit early if trailer
            if re.search('Şu an fragman*', html, re.I):
                return hosters
            
            hosters = self.__get_embed_sources(html, page_url)
            if not hosters:
                hosters = self.__get_ajax_sources(html, page_url)
                
        return hosters

    def __get_embed_sources(self, html, page_url):
        hosters = []
        match = re.search('var\s+kaynaklar\d+\s*=\s*\[(.*?)\]', html, re.DOTALL)
        if match:
            for match in re.finditer('''['"]?file['"]?\s*:\s*['"]([^'"]+)['"][^}]*['"]?label['"]?\s*:\s*['"]([^'"]*)''', match.group(1), re.DOTALL):
                stream_url, label = match.groups()
                stream_url = stream_url.replace('\\x', '').decode('hex')
                hoster = self.__create_source(stream_url, label, page_url)
                hosters.append(hoster)
                    
        return hosters
        
    def __get_ajax_sources(self, html, page_url):
        hosters = []
        match = re.search('''url\s*:\s*"([^"]+)"\s*,\s*data:'id=''', html)
        if match:
            ajax_url = match.group(1)
            for data_id in re.findall("kaynakdegis\('([^']+)", html):
                url = urlparse.urljoin(self.base_url, ajax_url)
                data = {'id': data_id}
                headers = {'Referer': page_url}
                headers.update(XHR)
                result = self._http_get(url, data=data, headers=headers, cache_limit=.5)
                for match in re.finditer('"videolink\d*"\s*:\s*"([^"]+)","videokalite\d*"\s*:\s*"?(\d+)p?', result):
                    stream_url, height = match.groups()
                    hoster = self.__create_source(stream_url, height, page_url)
                    hosters.append(hoster)
        return hosters
        
    def __create_source(self, stream_url, height, page_url):
        stream_url = stream_url.replace('\\/', '/')
        if self._get_direct_hostname(stream_url) != 'gvideo':
            headers = {'Referer': page_url}
            redir_url = self._http_get(stream_url, headers=headers, allow_redirect=False, cache_limit=.25)
            if redir_url.startswith('http'):
                stream_url = redir_url
                stream_url += scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
            else:
                stream_url += scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua(), 'Referer': page_url, 'Cookie': self._get_stream_cookies()})

        host = self._get_direct_hostname(stream_url)
        if host == 'gvideo':
            quality = scraper_utils.gv_get_quality(stream_url)
        else:
            quality = scraper_utils.height_get_quality(height)
        hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
        return hoster
        
    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+/%s-sezon-%s-bolum[^"]*)"' % (video.season, video.episode)
        title_pattern = 'class="gizle".*?href="(?P<url>[^"]+)">(?P<title>[^<]+)'
        return self._default_get_episode_url(show_url, video, episode_pattern, title_pattern)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        html = self._http_get(self.base_url, cache_limit=48)
        results = []
        fragment = dom_parser.parse_dom(html, 'div', {'id': 'fil'})
        norm_title = scraper_utils.normalize_title(title)
        if fragment:
            for match in re.finditer('href="([^"]+)"\s+title="([^"]+)', fragment[0]):
                url, match_title = match.groups()
                if norm_title in scraper_utils.normalize_title(match_title):
                    result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(match_title), 'year': ''}
                    results.append(result)

        return results

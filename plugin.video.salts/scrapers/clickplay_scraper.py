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
import scraper
import re
import urlparse
import base64
import urllib
from salts_lib import kodi
from salts_lib import dom_parser
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES

BASE_URL = 'http://clickplay.to'
GK_KEY = base64.urlsafe_b64decode('bW5pcUpUcUJVOFozS1FVZWpTb00=')

class ClickPlay_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'clickplay.to'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s ' % (item['quality'], item['host'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)

            ele = dom_parser.parse_dom(html, 'video')
            if ele:
                stream_url = dom_parser.parse_dom(ele, 'source', ret='src')
                if stream_url:
                    hoster = {'multi-part': False, 'url': stream_url[0], 'class': self, 'quality': QUALITIES.HD720, 'host': self._get_direct_hostname(stream_url[0]), 'rating': None, 'views': None, 'direct': True}
                    if hoster['host'] == 'gvideo':
                        hoster['quality'] = self._gv_get_quality(hoster['url'])
                    hosters.append(hoster)
            
            sources = dom_parser.parse_dom(html, 'iframe', ret='src')
            for src in sources:
                if 'facebook' in src: continue
                host = urlparse.urlparse(src).hostname
                hoster = {'multi-part': False, 'url': src, 'class': self, 'quality': QUALITIES.HIGH, 'host': host, 'rating': None, 'views': None, 'direct': False}
                hosters.append(hoster)
                
            match = re.search('proxy\.link=([^"&]+)', html)
            if match:
                proxy_link = match.group(1)
                proxy_link = proxy_link.split('*', 1)[-1]
                stream_url = self._gk_decrypt(GK_KEY, proxy_link)
                if 'vk.com' in stream_url.lower():
                    hoster = {'multi-part': False, 'host': 'vk.com', 'class': self, 'url': stream_url, 'quality': QUALITIES.HD720, 'views': None, 'rating': None, 'direct': False}
                    hosters.append(hoster)
                if 'picasaweb' in stream_url.lower():
                    for source in self._parse_google(stream_url):
                        quality = self._gv_get_quality(source)
                        hoster = {'multi-part': False, 'url': source, 'class': self, 'quality': quality, 'host': self._get_direct_hostname(source), 'rating': None, 'views': None, 'direct': True}
                        hosters.append(hoster)
                if 'docs.google' in stream_url.lower():
                    for source in self.__parse_fmt(stream_url):
                        quality = self._gv_get_quality(source)
                        hoster = {'multi-part': False, 'url': source, 'class': self, 'quality': quality, 'host': self._get_direct_hostname(source), 'rating': None, 'views': None, 'direct': True}
                        hosters.append(hoster)
                
        return hosters

    def __parse_fmt(self, link):
        urls = {}
        html = self._http_get(link, cache_limit=.5)
        for match in re.finditer('\[\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\]', html):
            key, value = match.groups()
            if key == 'fmt_stream_map':
                items = value.split(',')
                for item in items:
                    source_fmt, source_url = item.split('|')
                    source_url = source_url.replace('\\u003d', '=').replace('\\u0026', '&')
                    source_url = urllib.unquote(source_url)
                    urls[source_url] = source_fmt
                    
        return urls

    def get_url(self, video):
        return super(ClickPlay_Scraper, self)._default_get_url(video)

    def _get_episode_url(self, show_url, video):
        season_url = show_url + 'season-%d/' % (int(video.season))
        episode_pattern = 'href="([^"]+/season-%d/episode-%d-[^"]+)' % (int(video.season), int(video.episode))
        title_pattern = 'href="(?P<url>[^"]+)"\s+title="[^"]+/\s*(?P<title>[^"]+)'
        return super(ClickPlay_Scraper, self)._default_get_episode_url(season_url, video, episode_pattern, title_pattern)

    def search(self, video_type, title, year):
        url = urlparse.urljoin(self.base_url, '/tv-series-a-z-list')
        html = self._http_get(url, cache_limit=8)

        results = []
        pattern = '<li>\s*<a.*?href="([^"]+)[^>]*>([^<]+)'
        norm_title = self._normalize_title(title)
        for match in re.finditer(pattern, html, re.DOTALL):
            url, match_title_year = match.groups()
            r = re.search('(.*?)\s+\((\d{4})\)', match_title_year)
            if r:
                match_title, match_year = r.groups()
            else:
                match_title = match_title_year
                match_year = ''

            if norm_title in self._normalize_title(match_title) and (not year or not match_year or year == match_year):
                result = {'url': self._pathify_url(url), 'title': match_title, 'year': match_year}
                results.append(result)

        return results

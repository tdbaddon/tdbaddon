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
import scraper
import re
import urlparse
import urllib
import urllib2
import time
import random
from salts_lib import log_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import XHR
from salts_lib import kodi

BASE_URL = 'http://sezonlukdizi.com'
SEARCH_URL = '/service/search?q=%s&_=%s'
GET_VIDEO_URL = '/service/get_video_part'

class SezonLukDizi_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'SezonLukDizi'

    def resolve_link(self, link):
        if 'v.asp' in link:
            try:
                headers = dict([item.split('=') for item in (link.split('|')[1]).split('&')])
                for key in headers: headers[key] = urllib.unquote(headers[key])
            except:
                headers = {}
            request = urllib2.Request(link.split('|')[0], headers=headers)
            response = urllib2.urlopen(request)
            return response.geturl()
        else:
            return link
            
    def format_source_label(self, item):
        return '[%s] %s' % (item['quality'], item['host'])

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=2)
            
            match1 = re.search('var\s+video_id\s*=\s*"([^"]+)', html)
            match2 = re.search('var\s+part_name\s*=\s*"([^"]+)', html)
            if match1 and match2:
                video_id = match1.group(1)
                part_name = match2.group(1)
                
                part_count, links = self.__get_video(video_id, part_name, 0)
                hosters += links
                
                for page in xrange(1, part_count):
                    _, links = self.__get_video(video_id, part_name, page)
                    hosters += links
        
            hosters = dict((stream['url'], stream) for stream in hosters).values()
        return hosters

    def __get_video(self, video_id, part_name, page):
        hosters = []
        part_count = 1
        video_url = urlparse.urljoin(self.base_url, GET_VIDEO_URL)
        data = {'video_id': video_id, 'part_name': part_name, 'page': page}
        html = self._http_get(video_url, data=data, headers=XHR, cache_limit=.25)
        js_result = self._parse_json(html, video_url)
        if 'part_count' in js_result:
            part_count = js_result['part_count']
            
        if 'part' in js_result and 'code' in js_result['part']:
            hosters = self.__get_links(js_result['part']['code'])
        return part_count, hosters
        
    def __get_links(self, url):
        sources = []
        match = re.search('src="([^"]+)', url)
        if match:
            url = match.group(1).replace('\\/', '/')
            html = self._http_get(url, cache_limit=0)
            match = re.search('<script\s+src="([^\']+)\'\+(\d+)\+\'([^\']+)', html)
            if match:
                page_url = ''.join(match.groups())
                page_url += str(random.random())
                html = self._http_get(page_url, cache_limit=0)
                
            for match in re.finditer('"?file"?\s*:\s*"([^"]+)"\s*,\s*"?label"?\s*:\s*"(\d+)p?"', html):
                stream_url, height = match.groups()
                stream_url = stream_url.replace('\\&', '&').replace('\\/', '/')
                if 'v.asp' in stream_url and 'ok.ru' not in url:
                    stream_redirect = self._http_get(stream_url, allow_redirect=False, cache_limit=0)
                    if stream_redirect: stream_url = stream_redirect

                if self._get_direct_hostname(stream_url) == 'gvideo':
                    quality = self._gv_get_quality(stream_url)
                else:
                    quality = self._height_get_quality(height)
                        
                host = self._get_direct_hostname(stream_url)
                stream_url += '|User-Agent=%s&Referer=%s' % (self._get_ua(), urllib.quote(url))
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
                sources.append(hoster)
        return sources
    
    def get_url(self, video):
        return super(SezonLukDizi_Scraper, self)._default_get_url(video)

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+(?:-|/)%s-sezon-%s-[^"]*bolum[^"]*)' % (video.season, video.episode)
        title_pattern = 'class="episode-name"\s+href="(?P<url>[^"]+)"\s+title="(?P<title>[^"]+)'
        return super(SezonLukDizi_Scraper, self)._default_get_episode_url(show_url, video, episode_pattern, title_pattern)

    def search(self, video_type, title, year):
        results = []
        search_url = urlparse.urljoin(self.base_url, SEARCH_URL)
        search_url = search_url % (urllib.quote_plus(title), str(int(time.time() * 1000)))
        html = self._http_get(search_url, headers=XHR, cache_limit=1)
        js_result = self._parse_json(html, search_url)
        if js_result:
            for item in js_result:
                result = {'url': self._pathify_url(item['url']), 'title': item['name'], 'year': ''}
                results.append(result)

        return results

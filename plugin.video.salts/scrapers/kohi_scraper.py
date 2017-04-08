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
import time
import math
import binascii
import re
import urlparse
import base64
import kodi
import dom_parser2
import log_utils  # @UnusedImport
from salts_lib import scraper_utils
from salts_lib import pyaes
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import XHR
import scraper

BASE_URL = 'http://kohimovie.info'
AJAX_URL = '/home/ajax/'
KEY = base64.b64decode('MDEyMzQ1Njc4OWFiY2RlZjAxMjM0NTY3ODlhYmNkZWY=')
IV = base64.b64decode('YWJjZGVmOTg3NjU0MzEyMGFiY2RlZjk4NzY1NDMxMjA=')

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.ajax_url = urlparse.urljoin(self.base_url, AJAX_URL)

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.SEASON, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'kohimovie'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        server_list, sources = self.__get_sources(source_url, video, '')
        for attrs, server in dom_parser2.parse_dom(server_list, 'a', req='href'):
            _server_list, streams = self.__get_sources(attrs['href'], video, server)
            sources.update(streams)
            
        for source, values in sources.iteritems():
            direct = values['direct']
            quality = values['quality']
            host = scraper_utils.get_direct_hostname(self, source) if direct else urlparse.urlparse(source).hostname
            stream_url = source + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': direct}
            hosters.append(hoster)

        return hosters
    
    def __get_sources(self, source_url, video, server):
        sources = {}
        page_url = urlparse.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=0)
        sign, alias, now = self.__get_attributes(html)
        server_list, streams = self.__get_streams(sign, alias, now, server, page_url)
        if video.video_type == VIDEO_TYPES.MOVIE:
            sources.update(self.__extract_sources(streams, video.video_type))
        else:
            if int(video.episode) == 1:
                sources.update(self.__extract_sources(streams, video.video_type))
            elif self.__episode_match(streams.get('html', ''), video):
                sign = self.__get_sign(sign, now, page_url)
                if sign.get('code') == 1:
                    streams = self.__get_episode_streams(sign['ke'], alias, now, server, video.episode, page_url)
                    sources.update(self.__extract_sources(streams, video.video_type))
                    
        return server_list, sources
    
    def __extract_sources(self, streams, video_type):
        stream_url = streams.get('streaming', '')
        if not stream_url: return {}
        
        if scraper_utils.get_direct_hostname(self, stream_url) == 'gvideo':
            source = {stream_url: {'quality': scraper_utils.gv_get_quality(stream_url), 'direct': True}}
        else:
            if video_type == VIDEO_TYPES.MOVIE:
                meta = scraper_utils.parse_movie_link(stream_url)
            else:
                meta = scraper_utils.parse_episode_link(stream_url)
            source = {stream_url: {'quality': scraper_utils.height_get_quality(meta['height']), 'direct': False}}
        return source
                
    def __get_streams(self, sign_new, alias, now, server, page_url):
        server_list = self.__get_server_list(sign_new, alias, now, server, page_url)
        sign = self.__get_sign(sign_new, now, page_url)
        if sign.get('code') != 1: return '', {}
        
        streams = self.__get_movie_streams(sign['ke'], alias, now, server, page_url)
        return server_list.get('html', ''), streams
    
    def __get_attributes(self, html):
        match = re.search("sign_new\s*=\s*'([^']+)", html)
        if not match: return '', ''
        sign_new = match.group(1)
        
        match = re.search("alias\s*=\s*'([^']+)", html)
        if not match: return '', ''
        alias = match.group(1)

        match = re.search("time\s*=\s*'([^']+)", html)
        if match:
            now = match.group(1)
        else:
            now = int(time.time())
            
        return sign_new, alias, now
        
    def __get_server_list(self, sign, alias, now, server, page_url):
        data = {'me': now, 'alias': alias, 'server': server, 'action': 'getlistserver'}
        bearer = sign + ',' + str(now) + ','
        return self.__ajax(data, page_url, bearer)
    
    def __get_sign(self, sign, now, page_url):
        sign_new = base64.b64decode("setRequestHeader") + str(now)
        sign_new = base64.b64encode(self.__encrypt(sign_new, KEY, IV))
        data = {'me': now, 'sign': sign_new, 'action': 'gttoeke'}
        bearer = sign + ',' + str(now) + ','
        return self.__ajax(data, page_url, bearer)
        
    def __get_movie_streams(self, ke, alias, now, server, page_url):
        h = base64.b64decode("setRequestHeader")
        sign = h + str(now)
        sign = base64.b64encode(self.__encrypt(sign, KEY, IV))
        data = {'me': now, 'alias': alias, 'server': server, 'action': 'fku'}
        bearer = base64.b64decode(ke) + ',' + str(now) + ',' + h
        return self.__ajax(data, page_url, bearer)
    
    def __get_episode_streams(self, ke, alias, now, server, index, page_url):
        h = base64.b64decode("setRequestHeader")
        sign = h + str(now)
        sign = base64.b64encode(self.__encrypt(sign, KEY, IV))
        data = {'me': now, 'alias': alias, 'server': server, 'action': 'new_episode', 'index': index}
        bearer = base64.b64decode(ke) + ',' + str(now) + ',' + alias + ',' + h + ','
        return self.__ajax(data, page_url, bearer)
    
    def __ajax(self, data, page_url, bearer):
        headers = {'Referer': page_url}
        headers.update(XHR)
        if bearer:
            bearer = base64.b64encode(self.__encrypt(bearer, KEY, IV))
            headers.update({'Authorization': 'Bearer ' + bearer})
            
        html = self._http_get(self.ajax_url, data=data, headers=headers, cache_limit=0)
        return scraper_utils.parse_json(html, data)
        
    def __encrypt(self, plain_text, key, iv):
        key = binascii.a2b_hex(key)
        iv = binascii.a2b_hex(iv)
        plain_text = ''.join(unichr(ord(c)) for c in plain_text).encode('utf-8')
        encrypter = pyaes.Encrypter(pyaes.AESModeOfOperationCBC(key, iv))
        cipher_text = encrypter.feed(plain_text)
        cipher_text += encrypter.feed()
        return cipher_text
        
    def __pad(self, text):
        diff = int(math.ceil(len(text) / 16.0) * 16) - len(text)
        return text + chr(diff) * diff
        
    def __episode_match(self, html, video):
        for _attrs, label in dom_parser2.parse_dom(html, 'span', {'class': 'title'}):
            if re.match('0*%s(?!\d)' % (video.episode), label) or scraper_utils.release_check(video, label, require_title=False):
                return True
        
        return False
    
    def _get_episode_url(self, season_url, video):
        season_url = urlparse.urljoin(self.base_url, season_url)
        html = self._http_get(season_url, cache_limit=0)
        sign, alias, now = self.__get_attributes(html)
        _server_list, sources = self.__get_streams(sign, alias, now, '', season_url)
        if self.__episode_match(sources.get('html', ''), video):
            return season_url
    
    def search(self, video_type, title, year, season=''):
        results = []
        search_url = urlparse.urljoin(self.base_url, '/search')
        html = self._http_get(search_url, params={'q': title}, cache_limit=8)
        for _attrs, item in dom_parser2.parse_dom(html, 'article', {'class': ['item', 'movies']}):
            try: is_season = 'EPS' in dom_parser2.parse_dom(item, 'span', {'class': 'quality'})[0].content
            except: is_season = False
            if (is_season and video_type == VIDEO_TYPES.MOVIE) or (not is_season and video_type == VIDEO_TYPES.SEASON):
                continue
            
            match_url = dom_parser2.parse_dom(item, 'a', req='href')
            match_title = dom_parser2.parse_dom(item, 'img', req='alt')
            if not match_url or not match_title: continue
            match_url = match_url[0].attrs['href']
            match_title = match_title[0].attrs['alt']
            
            match_year = ''
            if video_type == VIDEO_TYPES.MOVIE:
                for span in dom_parser2.parse_dom(item, 'span'):
                    if re.search('\d{4}', span.content): match_year = span.content
            else:
                match = re.search('season\s+(\d+)', match_title, re.I)
                if season and match and int(season) != int(match.group(1)): continue
                    
            if not year or not match_year or year == match_year:
                result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                results.append(result)
        return results

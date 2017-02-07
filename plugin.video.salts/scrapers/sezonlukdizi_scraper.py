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
import urllib
import urllib2
import urlparse
import kodi
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://sezonlukdizi.net'
SEARCH_URL = '/js/dizi.js'
SEASON_URL = '/ajax/dataDizi.asp'
EMBED_URL = '/ajax/dataEmbed.asp'
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
            
    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        sources = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=2)
            fragment = dom_parser.parse_dom(html, 'div', {'id': 'playerMenu'})
            if fragment:
                for data_id in dom_parser.parse_dom(fragment[0], 'div', {'class': '[^"]*item[^"]*'}, ret='data-id'):
                    embed_url = urlparse.urljoin(self.base_url, EMBED_URL)
                    data = {'id': data_id}
                    headers = {'Referer': page_url}
                    headers.update(XHR)
                    html = self._http_get(embed_url, data=data, headers=headers, cache_limit=.5)
                    iframe_url = dom_parser.parse_dom(html, 'iframe', ret='src')
                    if iframe_url:
                        iframe_url = iframe_url[0]
                        if urlparse.urlparse(self.base_url).hostname in iframe_url:
                            sources += self.__get_direct_links(iframe_url, page_url)
                        else:
                            sources += [{'stream_url': iframe_url, 'subs': 'Turkish subtitles', 'height': 480, 'direct': False}]
                            
            for source in sources:
                stream_url = source['stream_url'] + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
                if source['direct']:
                    host = self._get_direct_hostname(stream_url)
                    if host == 'gvideo':
                        quality = scraper_utils.gv_get_quality(stream_url)
                    else:
                        quality = scraper_utils.height_get_quality(source['height'])
                else:
                    host = urlparse.urlparse(source['stream_url']).hostname
                    quality = scraper_utils.height_get_quality(source['height'])
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': source['direct'], 'subs': source['subs']}
                hosters.append(hoster)
        return hosters
    
    def __get_direct_links(self, iframe_url, page_url):
        sources = []
        headers = {'Referer': page_url}
        html = self._http_get(iframe_url, headers=headers, cache_limit=.5)
        
        # if captions exist, then they aren't hardcoded
        subs = '' if re.search('kind\s*:\s*"captions"', html) else 'Turkish subtitles'
         
        for match in re.finditer('"?file"?\s*:\s*"([^"]+)"\s*,\s*"?label"?\s*:\s*"(\d+)p?[^"]*"', html):
            stream_url, height = match.groups()
            if 'v.asp' in stream_url:
                stream_redirect = self._http_get(stream_url, allow_redirect=False, method='HEAD', cache_limit=0)
                if stream_redirect: stream_url = stream_redirect
            sources.append({'stream_url': stream_url, 'subs': subs, 'height': height, 'direct': True})
        
        if not sources:
            sources = self.__get_cloud_links(html, iframe_url, subs)
            
        return sources
                    
    def __get_cloud_links(self, html, iframe_url, subs):
        sources = []
        match = re.search("url\s*:\s*'([^']+)", html)
        if match:
            url = match.group(1)
            headers = {'Referer': iframe_url}
            headers.update(XHR)
            html = self._http_get(url, headers=headers, cache_limit=.5)
            js_data = scraper_utils.parse_json(html, url)
            if 'variants' in js_data:
                for variant in js_data['variants']:
                    if 'hosts' in variant and variant['hosts']:
                        host = variant['hosts'][0]
                        stream_url = 'https://%s%s' % (host, variant['path'])
                        sources.append({'stream_url': stream_url, 'subs': subs, 'height': variant.get('height', 480), 'direct': True})
                    
        return sources
    
    def _get_episode_url(self, show_url, video):
        url = urlparse.urljoin(self.base_url, show_url)
        headers = {'Referer': self.base_url}
        html = self._http_get(url, headers=headers, cache_limit=.25)
        data_id = dom_parser.parse_dom(html, 'div', {'id': 'dizidetay'}, ret='data-id')
        data_dizi = dom_parser.parse_dom(html, 'div', {'id': 'dizidetay'}, ret='data-dizi')
        if data_id and data_dizi:
            queries = {'sekme': 'bolumler', 'id': data_id[0], 'dizi': data_dizi[0]}
            season_url = SEASON_URL + '?' + urllib.urlencode(queries)
            episode_pattern = '''href=['"]([^'"]*/%s-sezon-%s-[^'"]*bolum[^'"]*)''' % (video.season, video.episode)
            title_pattern = '''href=['"](?P<url>[^'"]+)[^>]*>(?P<title>[^<]+)'''
            airdate_pattern = '''href=['"]([^"']+)[^>]*>[^<]*</a>\s*</td>\s*<td class="right aligned">{p_day}\.{p_month}\.{year}'''
            headers = {'Referer': url, 'Content-Length': 0}
            headers.update(XHR)
            result = self._default_get_episode_url(season_url, video, episode_pattern, title_pattern, airdate_pattern, headers=headers, method='POST')
            if result and 'javascript:;' not in result:
                return result

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = urlparse.urljoin(self.base_url, SEARCH_URL)
        html = self._http_get(search_url, cache_limit=48)
        norm_title = scraper_utils.normalize_title(title)
        match_year = ''
        for match in re.finditer('d\s*:\s*"([^"]+).*?u\s*:\s*"([^"]+)', html):
            match_title, match_url = match.groups()
            if norm_title in scraper_utils.normalize_title(match_title) and (not year or not match_year or year == match_year):
                result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                results.append(result)
        return results

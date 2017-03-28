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
import urlparse
import urllib
import re
import kodi
import log_utils  # @UnusedImport
import dom_parser2
import base64
from salts_lib import scraper_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES

BASE_URL = 'http://putlockers.mn'
GK_URL = BASE_URL + '/media/plugins/gkpluginsphp.php'
HOST_SUB = {'dailymotion': 'idowatch.net', 'other': 'watchers.to', 'veoh': 'entervideo.net', 'mega': 'entervideo.net'}

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'MovieHubs'

    def resolve_link(self, link):
        if self.base_url in link:
            html = self._http_get(link, cache_limit=.25)
            fragment = dom_parser2.parse_dom(html, 'div', {'id': 'media-player'})
            if fragment:
                decode = self.__decode_link(fragment[0].content)
                iframe_url = dom_parser2.parse_dom(decode, 'iframe', req='src')
                if iframe_url:
                    return iframe_url[0].attrs['src']
                
                href = dom_parser2.parse_dom(fragment[0], 'a', {'target': '_blank'}, req='href')
                if href:
                    return href[0].attrs['href']

        return link
    
    def __decode_link(self, html):
        try:
            match = re.search('decode\("([^"]+)', html)
            html = base64.b64decode(match.group(1))
            return html
        except Exception as e:
            log_utils.log('MovieHubs Resolve Exception: (%s) - %s' % (e, html), log_utils.LOGDEBUG)
            return ''
        
    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = urlparse.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=8)
        hosts = [r.content for r in dom_parser2.parse_dom(html, 'p', {'class': 'server_servername'})]
        links = [r.content for r in dom_parser2.parse_dom(html, 'p', {'class': 'server_play'})]
        for host, link_frag in zip(hosts, links):
            stream_url = dom_parser2.parse_dom(link_frag, 'a', req='href')
            if not stream_url: continue
            
            stream_url = stream_url[0].attrs['href']
            host = re.sub('^Server\s*', '', host, re.I)
            host = re.sub('\s*Link\s+\d+', '', host)
            if host.lower() == 'google':
                sources = self.__get_gvideo_links(stream_url)
            else:
                sources = [{'host': host, 'link': stream_url}]
            
            for source in sources:
                stream_url = source['link']
                host = scraper_utils.get_direct_hostname(self, stream_url)
                if host == 'gvideo':
                    quality = scraper_utils.gv_get_quality(stream_url)
                    stream_url += scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
                    direct = True
                else:
                    host = HOST_SUB.get(source['host'].lower(), source['host'])
                    quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
                    direct = False
                hoster = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': direct}
                hosters.append(hoster)

        return hosters

    def __get_gvideo_links(self, link):
        sources = []
        html = self._http_get(link, cache_limit=1)
        html = self.__decode_link(html)
        match = re.search('{\s*link\s*:\s*"([^"]+)', html)
        if match:
            data = {'link': match.group(1)}
            headers = {'Referer': link}
            html = self._http_get(GK_URL, data=data, headers=headers, cache_limit=.5)
            js_data = scraper_utils.parse_json(html, data)
            for link in js_data.get('link', []):
                sources.append({'host': '', 'link': link['link']})
                    
        return sources
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = urlparse.urljoin(self.base_url, '/search-movies/%s.html' % (urllib.quote_plus(title)))
        html = self._http_get(search_url, cache_limit=8)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'ml-item'}):
            match_url = dom_parser2.parse_dom(item, 'a', req='href')
            match_title_year = re.search('onmouseover="([^"]+)', item)
            if match_url and match_title_year:
                match_url = match_url[0].attrs['href']
                match_title_year = match_title_year.group(1)
                match = re.search('<b>(?:<i>)?\s*(.*?)\s*(?:</i>)?</b>', match_title_year)
                if match:
                    match_title, match_year = scraper_utils.extra_year(match.group(1))
                    
                if not match_year:
                    match_year = re.search('>Release:\s*(\d{4})', match_title_year)
                    match_year = match_year.group(1) if match_year else ''
                                    
                if not year or not match_year or year == match_year:
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)

        return results

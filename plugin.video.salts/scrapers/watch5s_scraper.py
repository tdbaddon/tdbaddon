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
import hashlib
import urlparse
import kodi
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib import jsunpack
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper
import xml.etree.ElementTree as ET

BASE_URL = 'http://watch5s.to'
Q_MAP = {'TS': QUALITIES.LOW, 'CAM': QUALITIES.LOW, 'HDTS': QUALITIES.LOW, 'HD-720P': QUALITIES.HD720}

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.SEASON, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'Watch5s'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        sources = {}
        headers = {'Accept-Language': 'en-US,en;q=0.5'}
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, headers=headers, cache_limit=2)
            if video.video_type == VIDEO_TYPES.MOVIE:
                sources.update(self.__scrape_sources(html, page_url))
                pages = set(dom_parser.parse_dom(html, 'a', {'class': '[^"]*btn-eps[^"]*'}, ret='href'))
                active = set(dom_parser.parse_dom(html, 'a', {'class': '[^"]*active[^"]*'}, ret='href'))
                for page in list(pages - active):
                    page_url = urlparse.urljoin(self.base_url, page)
                    html = self._http_get(page_url, headers=headers, cache_limit=2)
                    sources.update(self.__scrape_sources(html, page_url))
            else:
                for page in self.__match_episode(video, html):
                    page_url = urlparse.urljoin(self.base_url, page)
                    html = self._http_get(page_url, headers=headers, cache_limit=2)
                    sources.update(self.__scrape_sources(html, page_url))
        
        for source in sources:
            if not source.lower().startswith('http'): continue
            if sources[source]['direct']:
                host = self._get_direct_hostname(source)
                if host != 'gvideo':
                    stream_url = source + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua(), 'Referer': page_url})
                else:
                    stream_url = source
            else:
                host = urlparse.urlparse(source).hostname
                stream_url = source
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': sources[source]['quality'], 'views': None, 'rating': None, 'url': stream_url, 'direct': sources[source]['direct']}
            hosters.append(hoster)
        return hosters

    def __scrape_sources(self, html, page_url):
        sources = {}
        headers = {'Referer': page_url, 'Origin': self.base_url}
        match = re.search('player_type\s*:\s*"([^"]+)', html)
        player_type = match.group(1) if match else ''
        if player_type == 'embed':
            sources = self.__get_embed_sources(html)
        else:
            cookie, grab_url = self.__get_grab_url(html, page_url)
            if cookie and grab_url:
                headers.update({'Cookie': cookie})
                sources = self.__get_links_from_playlist(grab_url, headers)

        return sources
    
    def __get_embed_sources(self, html):
        sources = {}
        for match in re.finditer('embed_src\s*:\s*"([^"]+)', html):
            sources[match.group(1)] = {'quality': QUALITIES.HIGH, 'direct': False}
        return sources
    
    def __get_grab_url(self, html, page_url):
        cookie = ''
        grab_url = ''
        episode_id = dom_parser.parse_dom(html, 'input', {'name': 'episodeID'}, ret='value')
        if episode_id:
            episode_id = episode_id[0]
            token = scraper_utils.get_token(hash_len=8)
            key = hashlib.md5('!@#$%^&*(' + episode_id + token).hexdigest()
            value = hashlib.md5(token + page_url + episode_id).hexdigest()
            cookie = '%s=%s' % (key, value)
            hostname = urlparse.urlparse(page_url).hostname
            headers = {'Referer': page_url}
            for js_url in self.__get_js_url(html):
                match = re.search('{\s*playlist\s*:\s*"([^"]+)".*?"([^"]+)', self.__get_js(js_url, headers, hostname), re.DOTALL)
                if match:
                    grab_url = match.group(1) + episode_id + match.group(2) + token
                    break
            
        return cookie, grab_url
    
    def __get_js_url(self, html):
        urls = []
        for match in re.finditer('''<script[^>]*src\s*=\s*(["'])(.*?)\\1''', html, re.I):
            js_url = match.group(2).strip()
            js_url = re.sub('''['"]''', '', js_url)
            if '/' not in js_url:
                js_url = js_url.strip('+')
                pattern = '''var\s+%s\s*=\s*(['"])(.*?)\\1''' % (js_url)
                match = re.search(pattern, html)
                if match:
                    js_url = match.group(2)
            urls.append(js_url)
        return urls
        
    def __get_js(self, js_url, headers, hostname):
        js = ''
        if js_url.startswith('//'):
            js_url = 'https:' + js_url
        elif not js_url.startswith('http'):
            base_url = 'https://' + hostname
            js_url = urlparse.urljoin(base_url, js_url)
        
        log_utils.log('Getting JS: |%s| - |%s|' % (js_url, headers))
        try: js = self._http_get(js_url, headers=headers)
        except: js = ''
        return js
    
    def __get_links_from_js(self, html, page_url):
        sources = {}
        for src_url in dom_parser.parse_dom(html, 'script', ret='src'):
            if 'slug=' in src_url:
                headers = {'Referer': page_url}
                js_src = self._http_get(src_url, headers=headers, cache_limit=.5)
                if jsunpack.detect(js_src):
                    unpacked_data = jsunpack.unpack(js_src)
                else:
                    unpacked_data = js_src
                    
                match = re.search('"?sourcesPlaylist?"\s*:\s*"([^"]+)', unpacked_data)
                if match:
                    sources.update(self.__get_links_from_playlist(match.group(1), headers))
                else:
                    match = re.search('"?sourcesEmbed?"\s*:\s*"([^"]+)', unpacked_data)
                    if match:
                        embed_url = match.group(1).replace('\\', '')
                        sources[embed_url] = {'quality': QUALITIES.HD720, 'direct': False}
                        
        return sources
    
    def __get_links_from_playlist(self, grab_url, headers):
        sources = {}
        grab_url = grab_url.replace('\\', '')
        grab_html = self._http_get(grab_url, headers=headers, cache_limit=.5)
        js_data = scraper_utils.parse_json(grab_html, grab_url)
        try: playlist = js_data['playlist'][0]['sources']
        except: playlist = []
        for item in playlist:
            stream_url = item.get('file')
            if stream_url:
                if stream_url.startswith('/'):
                    stream_url = urlparse.urljoin(self.base_url, stream_url)
                    redir_url = self._http_get(stream_url, headers=headers, allow_redirect=False, method='HEAD')
                    if redir_url.startswith('http'):
                        stream_url = redir_url
                
                if self._get_direct_hostname(stream_url) == 'gvideo':
                    quality = scraper_utils.gv_get_quality(stream_url)
                elif 'label' in item:
                    quality = scraper_utils.height_get_quality(item['label'])
                else:
                    quality = QUALITIES.HIGH
                
                log_utils.log('Adding stream: %s Quality: %s' % (stream_url, quality), log_utils.LOGDEBUG)
                sources[stream_url] = {'quality': quality, 'direct': True}
                if not kodi.get_setting('scraper_url'): break
        return sources
        
    def _get_episode_url(self, season_url, video):
        url = urlparse.urljoin(self.base_url, season_url)
        headers = {'Accept-Language': 'en-US,en;q=0.5'}
        html = self._http_get(url, headers=headers, cache_limit=8)
        if self.__match_episode(video, html):
            return scraper_utils.pathify_url(season_url)
        
    def __match_episode(self, video, html):
        matches = []
        links = dom_parser.parse_dom(html, 'a', {'class': '[^"]*btn-eps[^"]*'}, ret="href")
        labels = dom_parser.parse_dom(html, 'a', {'class': '[^"]*btn-eps[^"]*'})
        for ep_label, ep_url in zip(labels, links):
            match = re.search('Ep(?:isode)?\s+(\d+)', ep_label, re.I)
            if match:
                ep_num = match.group(1)
                try: ep_num = int(ep_num)
                except: ep_num = 0
                if int(video.episode) == ep_num:
                    matches.append(ep_url)
        return matches
        
    def search(self, video_type, title, year, season=''):
        results = []
        search_url = urlparse.urljoin(self.base_url, '/search/')
        headers = {'Accept-Language': 'en-US,en;q=0.5'}
        html = self._http_get(search_url, params={'q': title}, headers=headers, cache_limit=8)
        for item in dom_parser.parse_dom(html, 'div', {'class': 'ml-item'}):
            match_title = dom_parser.parse_dom(item, 'span', {'class': 'mli-info'})
            match_url = re.search('href="([^"]+)', item, re.DOTALL)
            year_frag = dom_parser.parse_dom(item, 'img', ret='alt')
            is_episodes = dom_parser.parse_dom(item, 'span', {'class': 'mli-eps'})
            
            if (video_type == VIDEO_TYPES.MOVIE and not is_episodes) or (video_type == VIDEO_TYPES.SEASON and is_episodes):
                if match_title and match_url:
                    match_url = match_url.group(1)
                    match_title = match_title[0]
                    match_title = re.sub('</?h2>', '', match_title)
                    match_title = re.sub('\s+\d{4}$', '', match_title)
                    if video_type == VIDEO_TYPES.SEASON:
                        if season and not re.search('Season\s+%s$' % (season), match_title): continue
                        
                    if not match_url.endswith('/'): match_url += '/'
                    match_url = urlparse.urljoin(match_url, 'watch/')
                    match_year = ''
                    if video_type == VIDEO_TYPES.MOVIE and year_frag:
                        match = re.search('\s*-\s*(\d{4})$', year_frag[0])
                        if match:
                            match_year = match.group(1)
    
                    if not year or not match_year or year == match_year:
                        result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                        results.append(result)

        return results

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
from salts_lib.constants import QUALITIES
import scraper

BASE_URL = 'http://www.dizist.net'
ALLOWED = [u'odnok', u'rodi', u'odnokaltyazısız']

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
        return 'Dizist'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        sources = {}
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=1)
            pages = self.__get_alt_pages(html, page_url)
            sources = self.__get_sources(html, page_url, pages.get(page_url, True))
            for page in pages:
                if page == page_url: continue
                page_url = urlparse.urljoin(self.base_url, page, pages[page])
                html = self._http_get(page_url, cache_limit=1)
                sources.update(self.__get_sources(html, page, pages[page]))
            
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

    def __get_alt_pages(self, html, page_url):
        pages = {}
        fragment = dom_parser.parse_dom(html, 'div', {'class': 'video-alternatives'})
        if fragment:
            active = dom_parser.parse_dom(fragment[0], 'div', {'class': 'active'})
            for div in dom_parser.parse_dom(fragment[0], 'div'):
                match = re.search('href="([^"]+)[^>]>(.*?)</a>', div, re.DOTALL)
                if match:
                    alt_url, alt_label = match.groups()
                    alt_label = alt_label.lower().strip()
                    alt_label = re.sub('</?span>', '', alt_label)
                    if alt_label not in ALLOWED: continue
                    
                    subs = False if u'altyazısız' in alt_label else True
                    if active and active[0] == div:
                        pages[page_url] = subs
                    else:
                        pages[alt_url] = subs
                        
        return pages
    
    def __get_sources(self, html, page_url, subs):
        sources = {}
        player_div = dom_parser.parse_dom(html, 'div', {'class': 'dzst-player'}, ret='data-dzst-player')
        if player_div:
            js_html = scraper_utils.cleanse_title(player_div[0])
            js_data = scraper_utils.parse_json(js_html, page_url)
            links = js_data.get('tr', {})
            for height in links:
                stream_url = links[height]
                if self._get_direct_hostname(stream_url) == 'gvideo':
                    quality = scraper_utils.gv_get_quality(stream_url)
                else:
                    quality = scraper_utils.height_get_quality(height)
                sources[stream_url] = {'direct': True, 'subs': subs, 'quality': quality}
        else:
            fragment = dom_parser.parse_dom(html, 'div', {'class': 'video-player'})
            if fragment:
                fragment = fragment[0]
                for div in dom_parser.parse_dom(fragment, 'div', {'class': 'ad-player'}):
                    fragment = fragment.replace(div, '')
    
                iframe_url = dom_parser.parse_dom(fragment, 'iframe', ret='src')
                if iframe_url:
                    iframe_url = iframe_url[0]
                    if iframe_url.startswith('//'): iframe_url = 'http:' + iframe_url
                    if self._get_direct_hostname(iframe_url) == 'gvideo':
                        direct = True
                    else:
                        direct = False
                    sources[iframe_url] = {'direct': direct, 'subs': subs, 'quality': QUALITIES.HD720}
            
        return sources
    
    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+-%s-sezon-%s-bolum[^"]*)"' % (video.season, video.episode)
        title_pattern = 'href="(?P<url>[^"]+).*?class="ep-t">(?P<title>[^<]+)'
        return self._default_get_episode_url(show_url, video, episode_pattern, title_pattern)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        url = urlparse.urljoin(self.base_url, '/arsiv')
        html = self._http_get(url, cache_limit=48)
        norm_title = scraper_utils.normalize_title(title)
        fragment = dom_parser.parse_dom(html, 'div', {'class': 'ts-list-content'})
        if fragment:
            items = dom_parser.parse_dom(fragment[0], 'h1', {'class': 'ts-list-name'})
            details = dom_parser.parse_dom(fragment[0], 'ul')
            for item, detail in zip(items, details):
                match = re.search('href="([^"]+)[^>]*>(.*?)</a>', item)
                match_year = re.search('<span>(\d{4})</span>', detail)
                if match:
                    match_url, match_title = match.groups()
                    if match_year:
                        match_year = match_year.group(1)
                    else:
                        match_year = ''
                    
                    if norm_title in scraper_utils.normalize_title(match_title):
                        result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                        results.append(result)

        return results

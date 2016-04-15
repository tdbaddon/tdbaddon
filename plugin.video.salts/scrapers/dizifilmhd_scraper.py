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
from salts_lib import scraper_utils
import urlparse
import re
import urllib
from salts_lib import kodi
from salts_lib import dom_parser
from salts_lib import log_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH

BASE_URL = 'http://dizifilmhd.net'
SEARCH_EXCLUDE = ['Dublaj', 'Yabancı Dizi', 'Yerli Dizi']
TITLE_STRIP = ['TEK', 'PARCA', 'IZLE', '1080P', 'PARÇA', 'PARACA', 'TÜRKÇE', 'DUBLAJ', 'HD', 'ALTYAZI']

class DiziFilmHD_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'DiziFilmHD'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        return '[%s] %s' % (item['quality'], item['host'])

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            tabs = dom_parser.parse_dom(html, 'a', {'href': '#div\d+'})
            labels = dom_parser.parse_dom(html, 'a', {'href': '#div\d+'}, ret='href')
            for tab, label in zip(tabs, labels):
                sources = {}
                if tab != 'Dublaj':
                    div = dom_parser.parse_dom(html, 'div', {'id': label[1:]})
                    if div:
                        iframe_url = dom_parser.parse_dom(div[0], 'iframe', ret='src')
                        if iframe_url:
                            sources = self.__get_links(iframe_url[0], url)
                
                for source in sources:
                    host = self._get_direct_hostname(source)
                    quality = sources[source]['quality']
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': source, 'direct': True}
                    hosters.append(hoster)
                        
        return hosters

    def __get_links(self, url, page_url):
        headers = {'Referer': page_url}
        html = self._http_get(url, headers=headers, cache_limit=.5)
        return self._parse_sources_list(html)

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year, season=''):
        results = []
        search_url = urlparse.urljoin(self.base_url, '/?s=')
        search_url += urllib.quote_plus(title)
        html = self._http_get(search_url, cache_limit=8)
        title_strip = [word.decode('utf-8') for word in TITLE_STRIP]
        for item in dom_parser.parse_dom(html, 'div', {'class': 'item'}):
            match_url = re.search('href="([^"]+)', item)
            match_title = dom_parser.parse_dom(item, 'span', {'class': 'tt'})
            if match_url and match_title:
                item_type = dom_parser.parse_dom(item, 'span', {'class': 'calidad2'})
                if item_type and item_type[0] in SEARCH_EXCLUDE: continue
                match_url = match_url.group(1)
                match_title = match_title[0]
                if 'SEZON' in match_title.upper(): continue

                year_frag = dom_parser.parse_dom(item, 'span', {'class': 'year'})
                if year_frag:
                    match_year = year_frag[0]
                else:
                    match_year = ''
                        
                match_title = ' '.join([word for word in match_title.split() if word.upper() not in title_strip])
                if (not year or not match_year or year == match_year):
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)
        
        return results

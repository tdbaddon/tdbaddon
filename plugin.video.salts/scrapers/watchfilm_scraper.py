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
import urlparse
import base64
import kodi
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
import scraper

BASE_URL = 'http://watchfilm.to'

class Scraper(scraper.Scraper):
    base_url = BASE_URL
    
    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'WatchFilm'

    def resolve_link(self, link):
        if not link.startswith('http'):
            link = urlparse.urljoin(self.base_url, link)
            html = self._http_get(link, cache_limit=0)
            match = re.search("window\.location\.href\s*=\s*'([^']+)", html)
            if match:
                return match.group(1)
            
        return link
    
    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.5)
            hosters += self.__get_embedded_sources(video.video_type, html, source_url)
            hosters += self.__get_linked_sources(video.video_type, html)
            
        return hosters

    def __get_embedded_sources(self, video_type, html, page_url):
        sources = {}
        hosters = []
        headers = {'Referer': page_url}
        fragment = dom_parser.parse_dom(html, 'ul', {'class': 'idTabs'})
        if fragment:
            for embed_url in dom_parser.parse_dom(fragment[0], 'a', ret='href'):
                html = self._http_get(embed_url, headers=headers, cache_limit=.5)
                sources.update(self._parse_sources_list(html))
                
                match = re.search('base64code\s*=\s*"([^"]+)', html)
                if match:
                    stream_url = base64.b64decode(match.group(1))
                    sources.update({stream_url: {'quality': QUALITIES.HIGH, 'direct': False}})
                    
                match = re.search('setup\(.*?\)', html, re.DOTALL)
                if match:
                    fragment = match.group(0)
                    match = re.search('''title\s*:\s*['"]([^"']+)''', fragment)
                    if match:
                        release = match.group(1)
                        if video_type == VIDEO_TYPES.MOVIE:
                            meta = scraper_utils.parse_movie_link(release)
                        else:
                            meta = scraper_utils.parse_episode_link(release)
                        quality = scraper_utils.height_get_quality(meta['height'])
                    else:
                        quality = QUALITIES.HIGH
                        
                    match = re.search('''file\s*:\s*["']([^'"]+)''', fragment)
                    if match:
                        sources.update({match.group(1): {'quality': quality, 'direct': True}})
                    
        for source in sources:
            quality = sources[source]['quality']
            direct = sources[source]['direct']
            host = self._get_direct_hostname(source) if direct else urlparse.urlparse(source).hostname
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': source, 'direct': direct}
            hosters.append(hoster)
        return hosters
    
    def __get_linked_sources(self, video_type, html):
        hosters = []
        attr = 'mov\d+' if video_type == VIDEO_TYPES.MOVIE else 'tvep\d+'
        for row in dom_parser.parse_dom(html, 'tr', {'id': attr}):
            source = dom_parser.parse_dom(row, 'a', ret='href')
            host = re.search('<img[^>]+>([^<]+)', row)
            if source and host:
                source = scraper_utils.pathify_url(source[0])
                host = host.group(1)
                quality = QUALITIES.HIGH
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': source, 'direct': False}
                hosters.append(hoster)
                
        return hosters

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+-0*%sx0*%s(?!\d)[^"]*)' % (video.season, video.episode)
        title_pattern = 'href="(?P<url>[^"]+-\d+x\d+[^"]*)[^>]+>(?P<title>[^<]+)'
        return self._default_get_episode_url(show_url, video, episode_pattern, title_pattern)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        media_type = 'tvshows' if video_type == VIDEO_TYPES.TVSHOW else 'movies'
        search_url = urlparse.urljoin(self.base_url, '/search/') + urllib.quote_plus(title)
        html = self._http_get(search_url, cache_limit=8)
        for item in dom_parser.parse_dom(html, 'div', {'class': 'result-item'}):
            if not dom_parser.parse_dom(item, 'span', {'class': media_type}): continue
            fragment = dom_parser.parse_dom(item, 'div', {'class': 'title'})
            if fragment:
                match = re.search('href="([^"]+)[^>]*>(.*?)</a>', fragment[0])
                if match:
                    match_url, match_title = match.groups()
                    match_year = dom_parser.parse_dom(item, 'span', {'class': 'year'})
                    match_year = match_year[0] if match_year else ''
                
                    if not year or not match_year or year == match_year:
                        result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                        results.append(result)
            
        return results

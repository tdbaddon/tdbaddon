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

BASE_URL = 'http://moviewatcher.io'

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
        return 'MovieWatcher'

    def resolve_link(self, link):
        url = urlparse.urljoin(self.base_url, link)
        html = self._http_get(url, allow_redirect=False, cache_limit=0)
        if html.startswith('http'):
            return html
        else:
            return link

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=1)
            for item in dom_parser.parse_dom(html, 'a', {'class': 'full-torrent1'}):
                stream_url = dom_parser.parse_dom(item, 'span', ret='onclick')
                host = dom_parser.parse_dom(item, 'div', {'class': 'small_server'})
                
                match = re.search('Views:\s*(?:</[^>]*>)?\s*(\d+)', item, re.I)
                views = match.group(1) if match else None
                
                match = re.search('Size:\s*(?:</[^>]*>)?\s*(\d+)', item, re.I)
                size = int(match.group(1)) * 1024 * 1024 if match else None
                
                if stream_url and host:
                    stream_url = stream_url[0]
                    host = host[0].lower()
                    host = host.replace('stream server: ', '')
                    match = re.search("'(/redirect/[^']+)", stream_url)
                    if match:
                        stream_url = match.group(1)
                    quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': views, 'rating': None, 'url': stream_url, 'direct': False}
                    if size is not None: hoster['size'] = scraper_utils.format_size(size, 'B')
                    hosters.append(hoster)
        return hosters

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]*/s0*%se0*%s(?!\d)[^"]*)' % (video.season, video.episode)
        return self._default_get_episode_url(show_url, video, episode_pattern)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = urlparse.urljoin(self.base_url, '/search')
        html = self._http_get(search_url, params={'query': title.lower()}, cache_limit=8)
        for item in dom_parser.parse_dom(html, 'div', {'class': 'one_movie-item'}):
            match_url = dom_parser.parse_dom(item, 'a', ret='href')
            match_title = dom_parser.parse_dom(item, 'img', ret='alt')
            media_type = dom_parser.parse_dom(item, 'div', {'class': 'movie-series'})
            if not media_type:
                media_type = VIDEO_TYPES.MOVIE
            elif media_type[0] == 'TV SERIE':
                media_type = VIDEO_TYPES.TVSHOW
                
            if match_url and match_title and video_type == media_type:
                match_url = match_url[0]
                match_title = match_title[0]
                
                match_year = re.search('-(\d{4})-', match_url)
                if match_year:
                    match_year = match_year.group(1)
                else:
                    match_year = ''
        
                if not year or not match_year or year == match_year:
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)

        return results

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
import urllib
from salts_lib import dom_parser
from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
import scraper

BASE_URL = 'http://moviewatcher.to'

class MovieWatcher_Scraper(scraper.Scraper):
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
        return link

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
#         if 'size' in item:
#             label += ' (%s)' % (item['size'])
        if 'views' in item:
            label += ' (%s views)' % (item['views'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.25)
            for item in dom_parser.parse_dom(html, 'div', {'class': 'stream-table__row'}):
                stream_url = dom_parser.parse_dom(item, 'a', ret='href')
                match = re.search('<span[^>]*>\s*Views:\s*</span>\s*(\d+)', item, re.I)
                if match:
                    views = match.group(1)
                else:
                    views = None
                    
                match = re.search('<span[^>]*>\s*Size:\s*</span>\s*(\d+)', item, re.I)
                if match:
                    size = int(match.group(1)) * 1024 * 1024
                else:
                    size = None
                    
                if stream_url:
                    stream_url = stream_url[0]
                    if 'webtracker' in stream_url: continue
                    host = urlparse.urlparse(stream_url).hostname
                    quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': views, 'rating': None, 'url': stream_url, 'direct': False}
                    if size is not None: hoster['size'] = scraper_utils.format_size(size, 'B')
                    hosters.append(hoster)
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def _get_episode_url(self, show_url, video):
        show_url = urlparse.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, cache_limit=24)
        match = re.search('href="([^"]*/season-%s(?!\d)[^"]*)' % (video.season), html)
        if match:
            season_url = match.group(1)
            episode_pattern = 'href="([^"]*season-%s/episode-%s(?!\d)[^"]*)' % (video.season, video.episode)
            title_pattern = 'href="(?P<url>[^"]*season-\d+/episode-\d+[^"]*).*?alt="(?P<title>[^"]+)'
            return self._default_get_episode_url(season_url, video, episode_pattern, title_pattern)

    def search(self, video_type, title, year, season=''):
        results = []
        search_url = urlparse.urljoin(self.base_url, '/search?q=')
        search_url += urllib.quote_plus(title)
        html = self._http_get(search_url, cache_limit=1)
        norm_title = scraper_utils.normalize_title(title)
        for item in dom_parser.parse_dom(html, 'div', {'class': 'video_item'}):
            match_url = dom_parser.parse_dom(item, 'a', ret='href')
            match_title = dom_parser.parse_dom(item, 'img', ret='alt')
            match_year = ''
            if match_url and match_title:
                match_url = match_url[0]
                match_title = match_title[0]
                if VIDEO_TYPES == VIDEO_TYPES.TVSHOW and '/tv-series/' not in match_url:
                    continue
                
                if match_year:
                    match_year = match_year[0]
                else:
                    match_year = ''
        
                if norm_title in scraper_utils.normalize_title(match_title) and (not year or not match_year or year == match_year):
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)

        return results

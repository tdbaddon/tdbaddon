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
from salts_lib import dom_parser
from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://moviehdmax.com'
XHR = {'X-Requested-With': 'XMLHttpRequest'}

class MoxieHDMax_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.SEASON, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'MovieMax'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        return '[%s] %s' % (item['quality'], item['host'])

    def get_sources(self, video):
        sources = []
        source_url = self.get_url(video)
        if source_url and source_url != FORCE_NO_MATCH:
            if video.video_type == VIDEO_TYPES.MOVIE:
                streams = self.__get_movie_sources(source_url)
            else:
                streams = self.__get_episode_sources(source_url)
            
            for stream_url in streams:
                stream_url2 = stream_url + '|User-Agent=%s' % (scraper_utils.get_ua())
                host = self._get_direct_hostname(stream_url)
                source = {'multi-part': False, 'url': stream_url2, 'host': host, 'class': self, 'quality': streams[stream_url], 'views': None, 'rating': None, 'direct': True}
                sources.append(source)

        return sources

    def __get_episode_sources(self, source_url):
        sources = {}
        url = urlparse.urljoin(self.base_url, source_url)
        html = self._http_get(url, headers=XHR, method='POST', cache_limit=0)
        js_data = scraper_utils.parse_json(html, url)
        if 'sources' in js_data:
            for source in js_data['sources']:
                stream_url = source['host']
                if self._get_direct_hostname(stream_url) == 'gvideo':
                    quality = scraper_utils.gv_get_quality(stream_url)
                elif 'quality' in source:
                    quality = scraper_utils.height_get_quality(source['quality'])
                else:
                    quality = QUALITIES.HIGH
                sources[source['host']] = quality
        return sources
    
    def __get_movie_sources(self, source_url):
        url = urlparse.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)
        sources = {}
        for match in re.finditer('''<source[^>]+src=['"]([^'"]+)([^>]+)''', html):
            source, extra = match.groups()
            host = self._get_direct_hostname(source)
            if host == 'gvideo':
                quality = scraper_utils.gv_get_quality(source)
            else:
                match = re.search('''data-res\s*=\s*["']([^"']+)''', extra)
                if match:
                    height = re.sub('(hd|px)', '', match.group(1))
                    quality = scraper_utils.height_get_quality(height)
                else:
                    quality = QUALITIES.HIGH
            sources[source] = quality
        return sources
        
    def get_url(self, video):
        return self._default_get_url(video)

    def _get_episode_url(self, season_url, video):
        url = urlparse.urljoin(self.base_url, season_url)
        html = self._http_get(url, cache_limit=8)
        for label in dom_parser.parse_dom(html, 'a', {'class': 'episodelink'}):
            if int(label) == int(video.episode):
                ep_url = season_url.replace('/watch/', '/getepisode/') + '?p=%s' % (video.episode)
                return ep_url
    
    def search(self, video_type, title, year, season=''):
        results = []
        search_url = urlparse.urljoin(self.base_url, '/search/result?s=%s&selected=false')
        search_url = search_url % (urllib.quote_plus(title))
        html = self._http_get(search_url, cache_limit=1)
        for item in dom_parser.parse_dom(html, 'p', {'class': 'txt4'}):
            match = re.search('href="([^"]+)[^>]*>([^<]+)', item)
            if match:
                match_url, match_title_year = match.groups()
                is_season = re.search('Season\s+\d+\s+', match_title_year, re.I)
                if (not is_season and video_type == VIDEO_TYPES.MOVIE) or (is_season and video_type == VIDEO_TYPES.SEASON):
                    match = re.search('(.*?)\s+\((\d{4})[^)]*\)$', match_title_year)
                    if match:
                        match_title, match_year = match.groups()
                    else:
                        match_title = match_title_year
                        match_year = ''

                    if video_type == VIDEO_TYPES.SEASON:
                        match_year = ''
                        if season and not re.search('Season\s+%s$' % (season), match_title, re.I):
                            continue
            
                    if not year or not match_year or year == match_year:
                        result = {'title': scraper_utils.cleanse_title(match_title), 'url': scraper_utils.pathify_url(match_url), 'year': match_year}
                        results.append(result)
        return results

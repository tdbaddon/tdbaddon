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
from salts_lib import dom_parser
from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://hdmovie14.net'
SEARCH_URL = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAwNjkxOTYxOTI2MzYxNzgyMDM4ODpkYmljLTZweGt4cyZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='

class Flixanity_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.SEASON, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'HDMovie14'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        return '[%s] %s' % (item['quality'], item['host'])

    def get_sources(self, video):
        source_url = self.get_url(video)
        sources = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            for fragment in dom_parser.parse_dom(html, 'div', {'class': 'player_wraper'}):
                iframe_url = dom_parser.parse_dom(fragment, 'iframe', ret='src')
                if iframe_url:
                    url = urlparse.urljoin(self.base_url, iframe_url[0])
                    html = self._http_get(url, cache_limit=.5)
                    for match in re.finditer('"(?:url|src)"\s*:\s*"([^"]+)[^}]+"res"\s*:\s*([^,]+)', html):
                        stream_url, height = match.groups()
                        host = self._get_direct_hostname(stream_url)
                        if host == 'gvideo':
                            quality = scraper_utils.gv_get_quality(stream_url)
                        else:
                            quality = scraper_utils.height_get_quality(height)
                        stream_url += '|User-Agent=%s' % (scraper_utils.get_ua())
                        source = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': True}
                        sources.append(source)

        return sources

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year, season=''):
        results = self.__search(video_type, title, year, season)
        if not results:
            results = self.__alt_search(video_type, title, year, season)
        return results
            
    def __search(self, video_type, title, year, season=''):
        search_url = base64.decodestring(SEARCH_URL) % (urllib.quote_plus(title))
        html = self._http_get(search_url, cache_limit=1)
        results = []
        js_data = scraper_utils.parse_json(html)
        if 'results' in js_data:
            norm_title = scraper_utils.normalize_title(title)
            for item in js_data['results']:
                if '/watch/' not in item['url'].lower(): continue
                is_season = re.search('Season\s+(\d+)', item['titleNoFormatting'], re.IGNORECASE)
                if not is_season and video_type == VIDEO_TYPES.MOVIE or is_season and VIDEO_TYPES.SEASON:
                    match_title_year = item['titleNoFormatting']
                    match_title_year = re.sub('^Watch\s+', '', match_title_year)
                    match_url = item['url']
                    match_year = ''
                    if video_type == VIDEO_TYPES.MOVIE:
                        match = re.search('(.*?)(?:\s+\(?(\d{4})\)?)', match_title_year)
                        if match:
                            match_title, match_year = match.groups()
                        else:
                            match_title = match_title_year
                    else:
                        if season and int(is_season.group(1)) != int(season):
                            continue
                        match = re.search('(.*?)\s+\(\d{4}\)', match_title_year)
                        if match:
                            match_title = match.group(1)
                        else:
                            match_title = match_title_year
                    
                    if norm_title in scraper_utils.normalize_title(match_title) and (not year or not match_year or year == match_year):
                        result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                        results.append(result)

        return results

    def __alt_search(self, video_type, title, year, season=''):
        results = []
        search_url = urlparse.urljoin(self.base_url, '/search?key=')
        search_key = title.lower()
        if year: search_key += ' %s' % (year)
        if video_type == VIDEO_TYPES.SEASON and season:
            search_key += ' Season %s' % (season)
        search_url += urllib.quote_plus(search_key)
        html = self._http_get(search_url, cache_limit=1)
        for item in dom_parser.parse_dom(html, 'div', {'class': 'caption'}):
            match = re.search('href="([^"]+)[^>]+>(.*?)<span[^>]*>', item)
            if match:
                match_url, match_title = match.groups()
                is_season = re.search('-season-\d+', match_url)
                if (video_type == VIDEO_TYPES.MOVIE and not is_season) or (video_type == VIDEO_TYPES.SEASON and is_season):
                    if video_type == VIDEO_TYPES.SEASON:
                        if season and not re.search('season-0*%s$' % (season), match_url): continue
                        
                    match_title = re.sub('</?[^>]*>', '', match_title)
                    match_title = re.sub('\s+Full\s+Movie', '', match_title)
                    match = re.search('-(\d{4})(?:$|-)', match_url)
                    if match:
                        match_year = match.group(1)
                    else:
                        match_year = ''
                    
                    if not year or not match_year or year == match_year:
                        result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                        results.append(result)

        return results
        
    def _get_episode_url(self, season_url, video):
        url = urlparse.urljoin(self.base_url, season_url)
        html = self._http_get(url, cache_limit=2)
        if int(video.episode) == 1:
            return scraper_utils.pathify_url(url)
        else:
            pattern = 'location\.href=&quot;([^&]*season-%s[^/]*/%s)&quot;' % (video.season, video.episode)
            match = re.search(pattern, html)
            if match:
                return scraper_utils.pathify_url(match.group(1))

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
import urllib
import urlparse
import re
from salts_lib import kodi
from salts_lib import dom_parser
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH

BASE_URL = 'http://moviefarsi.com'
TVSHOW_URLS = ['http://dl1.moviefarsi.com/serial/', 'http://dl1.moviefarsi.com/serial/best/', 'http://dl2.moviefarsi.com/serial/', 'http://dl3.moviefarsi.com/serial/', 'http://dl5.moviefarsi.com/serial/']

class MovieFarsi_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'MovieFarsi'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        if 'views' in item and item['views']:
            label += ' (%s views)' % item['views']
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            if video.video_type == VIDEO_TYPES.EPISODE:
                    sources = self.__get_files(source_url)
                    for source in sources:
                        _title, season, episode, height, _extra = self._parse_episode_link(source['link'])
                        if int(video.season) == int(season) and int(video.episode) == int(episode):
                            stream_url = source['url'] + '|User-Agent=%s' % (self._get_ua())
                            hoster = {'multi-part': False, 'host': self._get_direct_hostname(source['url']), 'class': self, 'quality': self._height_get_quality(height), 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
                            hosters.append(hoster)
            else:
                source_url = urlparse.urljoin(self.base_url, source_url)
                html = self._http_get(source_url, cache_limit=.5)
                for match in re.finditer('downloadicon.png.*?href="([^"]+)', html):
                    stream_url = match.group(1) + '|User-Agent=%s' % (self._get_ua())
                    _title, _year, height, _extra = self._parse_movie_link(stream_url)
                    hoster = {'multi-part': False, 'host': self._get_direct_hostname(stream_url), 'class': self, 'quality': self._height_get_quality(height), 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
                    hosters.append(hoster)
                    
        return hosters

    def get_url(self, video):
        return super(MovieFarsi_Scraper, self)._default_get_url(video)

    def _get_episode_url(self, show_url, video):
        force_title = self._force_title(video)
        if not force_title:
            html = self._http_get(show_url, cache_limit=24)
            match = re.search('href="(S%02d/?)"' % (int(video.season)), html)
            if match:
                season_url = urlparse.urljoin(show_url, match.group(1))
                for item in self.__get_files(season_url, cache_limit=1):
                    match = re.search('(\.|_| )S%02d(\.|_| )?E%02d(\.|_| )' % (int(video.season), int(video.episode)), item['title'], re.I)
                    if match:
                        return season_url
            
    def search(self, video_type, title, year):
        results = []
        norm_title = self._normalize_title(title)
        if video_type == VIDEO_TYPES.TVSHOW:
            for server_url in TVSHOW_URLS:
                for row in self.__parse_directory(self._http_get(server_url, cache_limit=48)):
                    match_year = ''
                    if norm_title in self._normalize_title(row['title']) and (not year or not match_year or year == match_year):
                        result = {'url': urlparse.urljoin(server_url, row['link']), 'title': row['title'], 'year': match_year}
                        results.append(result)
        else:
            search_url = urlparse.urljoin(self.base_url, '/?s=')
            search_url += urllib.quote_plus(title)
            html = self._http_get(search_url, cache_limit=1)
            for article in dom_parser.parse_dom(html, 'article', {'class': 'entry-body'}):
                link = dom_parser.parse_dom(article, 'a', {'class': 'more-link'}, 'href')
                content = dom_parser.parse_dom(article, 'div', {'class': 'post-content'})
                match = re.search('</a>\s*([^<]+)', content[0]) if content else ''
                info = dom_parser.parse_dom(article, 'div', {'class': 'post-info'})
                is_movie = re.search('/category/movies/', info[0]) if info else False
                if match and link and is_movie:
                    match_title_year = match.group(1)
                    match = re.search('(.*?)\s+\(?(\d{4})\)?', match_title_year)
                    if match:
                        match_title, match_year = match.groups()
                    else:
                        match_title = match_title_year
                        match_year = ''
                    
                    if not year or not match_year or year == match_year:
                        result = {'url': self._pathify_url(link[0]), 'title': match_title, 'year': match_year}
                        results.append(result)
        
        return results

    def __get_files(self, url, cache_limit=.5):
        sources = []
        for row in self.__parse_directory(self._http_get(url, cache_limit=cache_limit)):
            source_url = urlparse.urljoin(url, row['link'])
            if row['directory']:
                sources += self.__get_files(source_url)
            else:
                row['url'] = source_url
                sources.append(row)
        return sources
    
    def __parse_directory(self, html):
        rows = []
        for match in re.finditer('\s*<a\s+href="([^"]+)">([^<]+)</a>\s+(\d+-[a-zA-Z]+-\d+ \d+:\d+)\s+(-|\d+)', html):
            link, title, date, size = match.groups()
            if title.endswith('/'): title = title[:-1]
            row = {'link': link, 'title': title, 'date': date}
            if link.endswith('/'):
                row['directory'] = True
            else:
                row['directory'] = False

            if size == '-':
                row['size'] = None
            else:
                row['size'] = size
            rows.append(row)
        return rows
    
    def _http_get(self, url, cookies=None, cache_limit=8):
        html = super(MovieFarsi_Scraper, self)._cached_http_get(url, self.base_url, self.timeout, cookies=cookies, cache_limit=cache_limit)
        extra_cookies = self.__get_cookie(html)
        if extra_cookies is not None:
            if cookies is None: cookies = {}
            cookies.update(extra_cookies)
            html = super(MovieFarsi_Scraper, self)._cached_http_get(url, self.base_url, self.timeout, cookies=cookies, cache_limit=0)
        return html

    def __get_cookie(self, html):
        match = re.search('setCookie\(\s*"([^"]+)"\s*,\s*"([^"]+)', html)
        if match:
            return {match.group(1): match.group(2)}

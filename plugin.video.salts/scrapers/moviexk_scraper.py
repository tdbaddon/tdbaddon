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


BASE_URL = 'http://www.moviexk.net'

class MoxieXK_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'MovieXK'

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
            if video.video_type == VIDEO_TYPES.MOVIE:
                fragment = dom_parser.parse_dom(html, 'div', {'class': 'poster'})
                if fragment:
                    movie_url = dom_parser.parse_dom(fragment[0], 'a', ret='href')
                    if movie_url:
                        url = urlparse.urljoin(self.base_url, movie_url[0])
                        html = self._http_get(url, cache_limit=.5)
                        episodes = self.__get_episodes(html)
                        url = self.__get_best_page(episodes)
                        if not url:
                            return sources
                        else:
                            url = urlparse.urljoin(self.base_url, url)
                            html = self._http_get(url, cache_limit=.5)
            
            for match in re.finditer('''<source[^>]+src=['"]([^'"]+)([^>]+)''', html):
                stream_url, extra = match.groups()
                if 'video.php' in stream_url:
                    redir_url = self._http_get(stream_url, allow_redirect=False, method='HEAD', cache_limit=.25)
                    if redir_url.startswith('http'): stream_url = redir_url
                
                host = self._get_direct_hostname(stream_url)
                if host == 'gvideo':
                    quality = scraper_utils.gv_get_quality(stream_url)
                else:
                    match = re.search('''data-res\s*=\s*["']([^"']+)''', extra)
                    if match:
                        height = re.sub('(hd|px)', '', match.group(1))
                        quality = scraper_utils.height_get_quality(height)
                    else:
                        quality = QUALITIES.HIGH
                
                stream_url += '|User-Agent=%s' % (scraper_utils.get_ua())
                source = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': True}
                sources.append(source)

        return sources

    def __get_best_page(self, episodes):
        if 'EPTRAILER' in episodes: del episodes['EPTRAILER']
        if 'EPCAM' in episodes: del episodes['EPCAM']
        qualities = ['EPHD1080P', 'EPHD720P', 'EPHD', 'EPFULL']
        for q in qualities:
            if q in episodes:
                return episodes[q]
            
        if len(episodes) > 0:
            return episodes.items()[0][1]
        
    def __get_episodes(self, html):
        labels = dom_parser.parse_dom(html, 'a', {'data-type': 'watch'})
        labels = [label.replace(' ', '').upper() for label in labels]
        urls = dom_parser.parse_dom(html, 'a', {'data-type': 'watch'}, ret='href')
        return dict(zip(labels, urls))
        
    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year, season=''):
        results = []
        search_url = urlparse.urljoin(self.base_url, '/search/')
        search_url += urllib.quote_plus(title)
        html = self._http_get(search_url, cache_limit=1)
        for fragment in dom_parser.parse_dom(html, 'div', {'class': 'inner'}):
            name = dom_parser.parse_dom(fragment, 'div', {'class': 'name'})
            if name:
                match = re.search('href="([^"]+)[^>]+>(.*?)</a>', name[0])
                if match:
                    match_url, match_title_year = match.groups()
                    if 'tv-series' in match_url and video_type == VIDEO_TYPES.MOVIE: continue
                    
                    match_title_year = re.sub('</?[^>]*>', '', match_title_year)
                    match_title_year = re.sub('[Ww]atch\s+[Mm]ovie\s*', '', match_title_year)
                    match_title_year = match_title_year.replace('&#8217;', "'")
                    match = re.search('(.*?)\s+\((\d{4})[^)]*\)$', match_title_year)
                    if match:
                        match_title, match_year = match.groups()
                    else:
                        match_title = match_title_year
                        match_year = ''
    
                    if not match_year:
                        year_span = dom_parser.parse_dom(fragment, 'span', {'class': 'year'})
                        if year_span:
                            year_text = dom_parser.parse_dom(year_span[0], 'a')
                            if year_text:
                                match_year = year_text[0].strip()
    
                    if not year or not match_year or year == match_year:
                        result = {'title': scraper_utils.cleanse_title(match_title), 'url': scraper_utils.pathify_url(match_url), 'year': match_year}
                        results.append(result)

        return results

    def _get_episode_url(self, show_url, video):
        url = urlparse.urljoin(self.base_url, show_url)
        html = self._http_get(url, cache_limit=24)
        fragment = dom_parser.parse_dom(html, 'div', {'class': 'poster'})
        if fragment:
            show_url = dom_parser.parse_dom(fragment[0], 'a', ret='href')
            if show_url:
                episode_pattern = '<a[^>]+href="([^"]+)[^>]+>[Ee][Pp]\s*[Ss]0*%s-E?p?0*%s\s*<' % (video.season, video.episode)
                return self._default_get_episode_url(show_url[0], video, episode_pattern)

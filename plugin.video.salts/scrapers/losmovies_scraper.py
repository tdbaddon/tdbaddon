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
import dom_parser
import log_utils  # @UnusedImport
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://losmovies.club'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'LosMovies'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            fragment = ''
            if video.video_type == VIDEO_TYPES.EPISODE:
                pattern = 'Season\s+%s\s+Serie\s+%s<(.*?)</table>' % (video.season, video.episode)
                match = re.search(pattern, html, re.DOTALL)
                if match:
                    fragment = match.group(1)
            else:
                fragment = html

            if fragment:
                for match in re.finditer('data-width="([^"]+)"[^>]+>([^<]+)', fragment, re.DOTALL):
                    width, url = match.groups()
                    host = urlparse.urlsplit(url).hostname.replace('embed.', '')
                    url = url.replace('&amp;', '&')
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': scraper_utils.width_get_quality(width), 'views': None, 'rating': None, 'url': url, 'direct': False}
                    hoster['quality'] = scraper_utils.get_quality(video, host, hoster['quality'])
                    hosters.append(hoster)
        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = urlparse.urljoin(self.base_url, '/search')
        params = {'type': 'movies', 'q': title}
        html = self._http_get(search_url, params=params, cache_limit=8)
        for item in dom_parser.parse_dom(html, 'div', {'id': 'movie-\d+'}):
            is_tvshow = dom_parser.parse_dom(item, 'div', {'class': 'movieTV'})
            if video_type == VIDEO_TYPES.MOVIE and is_tvshow: continue
            
            match_url = re.search('href="([^"]+)', item)
            match_title = dom_parser.parse_dom(item, 'h4')
            if match_url and match_title:
                match_title = match_title[0]
                match_url = match_url.group(1)
                match_year = ''
                if not year or not match_year or year == match_year:
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)
        return results

    def _get_episode_url(self, show_url, video):
        return show_url

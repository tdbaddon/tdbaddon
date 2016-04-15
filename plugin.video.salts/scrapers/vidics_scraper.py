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
import urllib2
import urlparse

from salts_lib import dom_parser
from salts_lib import kodi
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://www.vidics.ch'
FRAGMENTS = {VIDEO_TYPES.MOVIE: '/film/', VIDEO_TYPES.TVSHOW: '/serie/'}

class Vidics_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'vidics.ch'

    def resolve_link(self, link):
        url = urlparse.urljoin(self.base_url, link)
        request = urllib2.Request(url)
        request.add_header('User-Agent', scraper_utils.get_ua())
        request.add_unredirected_header('Host', request.get_host())
        request.add_unredirected_header('Referer', url)
        response = urllib2.urlopen(request)
        return response.geturl()

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)

            fragments = dom_parser.parse_dom(html, 'div', {'class': 'lang'})
            if fragments:
                for match in re.finditer('class="movie_link.*?href="([^"]+)[^>]+>([^<]+)', fragments[0], re.DOTALL):
                    media_url, host = match.groups()
                    hosters.append({'multi-part': False, 'url': media_url, 'class': self, 'quality': scraper_utils.get_quality(video, host, QUALITIES.HIGH), 'host': host, 'rating': None, 'views': None, 'direct': False})

        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year, season=''):
        search_url = '/Category-FilmsAndTV/Genre-Any/Letter-Any/ByPopularity/1/Search-%s.htm' % (title)
        search_url = urlparse.urljoin(self.base_url, search_url)
        html = self._http_get(search_url, cache_limit=.25)

        results = []
        for result in dom_parser.parse_dom(html, 'div', {'class': 'searchResult'}):
            url = dom_parser.parse_dom(result, 'a', {'itemprop': 'url'}, ret='href')
            match_title = dom_parser.parse_dom(result, 'span', {'itemprop': 'name'})
            match_year = dom_parser.parse_dom(result, 'span', {'itemprop': 'copyrightYear'})
            if match_year:
                match_year = match_year[0]
            else:
                match_year = ''
            
            if url and match_title and (not year or not match_year or year == match_year):
                if FRAGMENTS[video_type] not in url[0].lower(): continue
                result = {'url': scraper_utils.pathify_url(url[0]), 'title': scraper_utils.cleanse_title(match_title[0]), 'year': match_year}
                results.append(result)
        return results

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="(/Serie/[^-]+-Season-%s-Episode-%s)' % (video.season, video.episode)
        title_pattern = 'class="episode"\s+href="(?P<url>[^"]+).*?class="episode_title">\s*-\s*(?P<title>.*?) \('
        airdate_pattern = 'class="episode"\s+(?:style="[^"]+")?\s+href="([^"]+)(?:[^>]+>){2}[^<]+\s+\({year} {month_name} {p_day}\)'
        return self._default_get_episode_url(show_url, video, episode_pattern, title_pattern, airdate_pattern)

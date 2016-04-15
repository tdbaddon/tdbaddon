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

from salts_lib import kodi
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://movie4k.to'
QUALITY_MAP = {None: None, '0': QUALITIES.LOW, '1': QUALITIES.LOW, '2': QUALITIES.MEDIUM, '3': QUALITIES.MEDIUM, '4': QUALITIES.HIGH, '5': QUALITIES.HIGH}

class Movie4K_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'Movie4K'

    def resolve_link(self, link):
        url = urlparse.urljoin(self.base_url, link)
        html = self._http_get(url, cache_limit=0)
        match = re.search('Check the mirror links on the left menu.*?(?:src|href)="([^"]+)', html, re.DOTALL)
        if match:
            return match.group(1)

    def format_source_label(self, item):
        return '[%s] %s' % (item['quality'], item['host'])

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)

            pattern = r'id="tablemoviesindex2".*?href="([^"]+).*?&nbsp;([^<]+)(.*)'
            for match in re.finditer(pattern, html):
                url, host, extra = match.groups()
                if not url.startswith('/'): url = '/' + url
                r = re.search('/smileys/(\d+)\.gif', extra)
                if r:
                    smiley = r.group(1)
                else:
                    smiley = None

                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': scraper_utils.get_quality(video, host, QUALITY_MAP[smiley]), 'views': None, 'rating': None, 'url': url, 'direct': False}
                hosters.append(hoster)
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year, season=''):
        search_url = urlparse.urljoin(self.base_url, '/movies.php?list=search&search=')
        search_url += urllib.quote_plus(title)
        cookies = {'onlylanguage': 'en', 'lang': 'en'}
        html = self._http_get(search_url, cookies=cookies, cache_limit=.25)
        results = []
        pattern = 'id="tdmovies">\s*<a\s+href="([^"]+)">([^<]+).*?id="f7">(.*?)</TD>'
        for match in re.finditer(pattern, html, re.DOTALL):
            url, title, extra = match.groups('')
            if (video_type == VIDEO_TYPES.MOVIE and '(TVshow)' in title) or (video_type == VIDEO_TYPES.TVSHOW and '(TVshow)' not in title):
                continue

            title = title.replace('(TVshow)', '')
            title = title.strip()

            r = re.search('>(\d{4})<', extra)
            if r:
                match_year = r.group(1)
            else:
                match_year = ''

            if not year or not match_year or year == match_year:
                result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(title), 'year': match_year}
                results.append(result)
        return results

    def _get_episode_url(self, show_url, video):
        if not scraper_utils.force_title(video):
            url = urlparse.urljoin(self.base_url, show_url)
            html = self._http_get(url, cache_limit=.25)
            match = re.search('<div id="episodediv%s"(.*?)</div>' % (video.season), html, re.DOTALL)
            if match:
                fragment = match.group(1)
                pattern = 'value="([^"]+)">Episode %s<' % (video.episode)
                match = re.search(pattern, fragment)
                if match:
                    return scraper_utils.pathify_url(match.group(1))

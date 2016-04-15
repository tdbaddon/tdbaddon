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
import string
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


QUALITY_MAP = {'HD': QUALITIES.HIGH, 'LOW': QUALITIES.LOW}
QUALITY_ICONS = {'fullhdbr.png': QUALITIES.HIGH, 'Blu-Ray.gif': QUALITIES.HIGH}
BASE_URL = 'http://uflix.org'

class UFlix_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'UFlix.org'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s (%s Up, %s Down)' % (item['quality'], item['host'], item['up'], item['down'])
        if item['rating'] is not None: label += ' (%s/100)' % (item['rating'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        sources = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)

            quality = None
            for key in QUALITY_ICONS:
                if key in html:
                    quality = QUALITY_ICONS[key]
                    break

            if quality is None:
                match = re.search('(?:qaulity|quality):\s*<span[^>]*>(.*?)</span>', html, re.DOTALL | re.I)
                if match:
                    quality = QUALITY_MAP.get(match.group(1).upper())

            pattern = '''href="[^"]+url=([^&]+)&domain=([^"&]+).*?fa-thumbs-o-up">\s*([^<]+).*?vote_bad_embedid_\d+'>([^<]+)'''
            for match in re.finditer(pattern, html, re.I | re.DOTALL):
                url, host, up, down = match.groups()
                up = ''.join([c for c in up if c in string.digits])
                down = ''.join([c for c in down if c in string.digits])
                url = url.decode('base-64')
                host = host.decode('base-64')

                # skip ad match
                if host.upper() == 'HDSTREAM':
                    continue

                up = int(up)
                down = int(down)
                source = {'multi-part': False, 'url': url, 'host': host, 'class': self, 'quality': scraper_utils.get_quality(video, host, quality), 'up': up, 'down': down, 'direct': False}
                rating = up * 100 / (up + down) if (up > 0 or down > 0) else None
                source['rating'] = rating
                source['views'] = up + down
                sources.append(source)

        return sources

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year, season=''):
        search_url = urlparse.urljoin(self.base_url, '/index.php?menu=search&query=')
        search_url += urllib.quote_plus(title)
        html = self._http_get(search_url, cache_limit=.25)
        results = []
        sections = {VIDEO_TYPES.MOVIE: 'movies', VIDEO_TYPES.TVSHOW: 'series'}
        
        fragment = dom_parser.parse_dom(html, 'div', {'id': sections[video_type]})
        if fragment:
            for item in dom_parser.parse_dom(fragment[0], 'figcaption'):
                match = re.search('title="([^"]+)[^>]+href="([^"]+)', item)
                if match:
                    match_title_year, url = match.groups()
                    match = re.search('(.*?)\s+\(?(\d{4})\)?', match_title_year)
                    if match:
                        match_title, match_year = match.groups()
                    else:
                        match_title = match_title_year
                        match_year = ''
                    if match_title.startswith('Watch '): match_title = match_title.replace('Watch ', '')
                    if match_title.endswith(' Online'): match_title = match_title.replace(' Online', '')
                    
                    if not year or not match_year or year == match_year:
                        result = {'title': scraper_utils.cleanse_title(match_title), 'url': scraper_utils.pathify_url(url), 'year': match_year}
                        results.append(result)
        return results

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'class="link"\s+href="([^"]+/show/[^"]+/season/%s/episode/%s)"' % (video.season, video.episode)
        title_pattern = 'class="link"\s+href="(?P<url>[^"]+).*?class="tv_episode_name"[^>]*>\s*(?P<title>[^<]+)'
        return self._default_get_episode_url(show_url, video, episode_pattern, title_pattern)

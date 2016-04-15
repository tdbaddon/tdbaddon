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
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://www.mintmovies.net'

class MintMovies_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'MintMovies'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        if item['views'] is not None:
            label += ' (%s Views)' % (item['views'])
        if item['rating'] is not None:
            label += ' (%s/100)' % (item['rating'])
        return label

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            hosters += self.__get_links(html)
            fragment = dom_parser.parse_dom(html, 'div', {'class': 'keremiya_part'})
            if fragment:
                for match in re.finditer('href="([^"]+)', fragment[0]):
                    html = self._http_get(match.group(1), cache_limit=.5)
                    hosters += self.__get_links(html)
                    
        return hosters

    def __get_links(self, html):
        hosters = []
        streams = []
        fragment = dom_parser.parse_dom(html, 'div', {'class': 'video-embed'})
        if fragment:
            match = re.search("id='(engima[^']+)", fragment[0])
            if match:
                enigma_id = match.group(1)
                match = re.search('<script[^>]+src="(http[^"]+mintmovies[^"]+)', html)
                if match:
                    js_html = self._http_get(match.group(1), cache_limit=.5)
                    pattern = "\('#%s'\)\.replaceWith\('([^']+)" % (enigma_id)
                else:
                    js_html = html
                    pattern = "\('#engimadiv[^']+'\)\.replaceWith\('([^']+)"
                    
                match = re.search(pattern, js_html)
                if match:
                    fragment = [match.group(1).decode('unicode_escape')]
            
            match = re.search('src="([^"]+)', fragment[0])
            if match:
                streams.append(match.group(1))
            
            for match in re.finditer("window.open\('([^']+)", fragment[0]):
                streams.append(match.group(1))

        for stream_url in streams:
            if self._get_direct_hostname(stream_url) == 'gvideo':
                quality = scraper_utils.gv_get_quality(stream_url)
                host = self._get_direct_hostname(stream_url)
                direct = True
            else:
                host = urlparse.urlparse(stream_url).hostname
                if host is None: continue
                quality = QUALITIES.HIGH
                direct = False

            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': direct}
            
            match = re.search('class="views-infos">(\d+)', html, re.DOTALL)
            if match:
                hoster['views'] = int(match.group(1))
    
            match = re.search('class="rating">(\d+)%', html, re.DOTALL)
            if match:
                hoster['rating'] = match.group(1)
            hosters.append(hoster)
        return hosters
    
    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year, season=''):
        search_url = urlparse.urljoin(self.base_url, '/?s=')
        search_url += urllib.quote_plus('%s %s' % (title, year))
        html = self._http_get(search_url, cache_limit=.25)
        results = []
        if not re.search('Sorry, but nothing matched', html):
            norm_title = scraper_utils.normalize_title(title)
            for item in dom_parser.parse_dom(html, 'li', {'class': '[^"]*box-shadow[^"]*'}):
                match = re.search('href="([^"]+)"\s+title="([^"]+)', item)
                if match:
                    url, match_title_year = match.groups()
                    if re.search('S\d{2}E\d{2}', match_title_year): continue  # skip episodes
                    if re.search('TV\s*SERIES', match_title_year, re.I): continue  # skip shows
                    match = re.search('(.*?)\s+\(?(\d{4})\)?', match_title_year)
                    if match:
                        match_title, match_year = match.groups()
                    else:
                        match_title = match_title_year
                        match_year = ''

                    if (not year or not match_year or year == match_year) and norm_title in scraper_utils.normalize_title(match_title):
                        result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(url)}
                        results.append(result)

        return results

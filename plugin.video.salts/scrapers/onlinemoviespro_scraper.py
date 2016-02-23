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
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://onlinemovies-pro.com'

class OnlineMoviesPro_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'OnlineMoviesPro'

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
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            match = re.search('class="video-embed".*?src="([^"]+)', html, re.DOTALL)
            if match:
                stream_url = match.group(1)
                host = urlparse.urlparse(stream_url).hostname
                q_str = 'HDRIP'
                match = re.search('>Quality(.*?)<br\s*/>', html, re.I)
                if match:
                    q_str = match.group(1)
                    q_str = q_str.decode('utf-8').encode('ascii', 'ignore')
                    q_str = re.sub('(</?strong[^>]*>|:|\s)', '', q_str, re.I | re.U)
                    
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': scraper_utils.blog_get_quality(video, q_str, host), 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
                
                match = re.search('class="views-infos">(\d+).*?class="rating">(\d+)%', html, re.DOTALL)
                if match:
                    hoster['views'] = int(match.group(1))
                    hoster['rating'] = match.group(2)

                hosters.append(hoster)
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year):
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
                        result = {'title': match_title, 'year': match_year, 'url': scraper_utils.pathify_url(url)}
                        results.append(result)

        return results

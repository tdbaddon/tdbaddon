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
import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://putlocker-9.site'

class Scraper(scraper.Scraper):
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

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            fragment = dom_parser.parse_dom(html, 'div', {'class': 'video-embed'})
            if fragment:
                iframe_url = dom_parser.parse_dom(fragment[0], 'iframe', ret='src')
                if iframe_url:
                    stream_url = iframe_url[0]
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

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, params={'s': title}, cache_limit=1)
        fragment = dom_parser.parse_dom(html, 'ul', {'class': '[^"]*listing-videos[^"]*'})
        if fragment:
            log_utils.log(fragment)
            for match in re.finditer('href="([^"]+)[^>]+>(.*?)</a>', fragment[0], re.DOTALL):
                match_url, match_title_year = match.groups()
                log_utils.log(match.groups())
                match_title_year = re.sub('</?span[^>]*>', '', match_title_year)
                match_title, match_year = scraper_utils.extra_year(match_title_year)
                result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                results.append(result)

        return results

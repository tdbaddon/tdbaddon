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
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
from salts_lib.constants import Q_ORDER
import scraper


BASE_URL = 'http://www.seehd.se'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'SeeHD'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        sources = {}
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            for div in dom_parser.parse_dom(html, 'div', {'class': 'tabcontent'}):
                for source in dom_parser.parse_dom(div, 'source', ret='src'):
                    source += scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
                    sources[source] = {'quality': None, 'direct': True}
                
                iframe_url = dom_parser.parse_dom(div, 'iframe', ret='src')
                if iframe_url:
                    iframe_url = iframe_url[0]
                    if 'songs2dl' in iframe_url:
                        headers = {'Referer': url}
                        iframe_html = self._http_get(iframe_url, headers=headers, cache_limit=1)
                        sources.update(self._parse_sources_list(iframe_html))
                    else:
                        sources[iframe_url] = {'quality': None, 'direct': False}
                    
            page_quality = self.__get_best_quality(sources)
            for source in sources:
                if sources[source]['quality'] is None:
                    sources[source]['quality'] = page_quality
                    
            sources.update(self.__get_mirror_links(html, page_quality, video))
        for source in sources:
            direct = sources[source]['direct']
            if direct:
                host = self._get_direct_hostname(source)
            else:
                host = urlparse.urlparse(source).hostname
                
            hoster = {'multi-part': False, 'host': host, 'class': self, 'views': None, 'url': source, 'rating': None, 'quality': sources[source]['quality'], 'direct': direct}
            hosters.append(hoster)

        return hosters

    def __get_best_quality(self, sources):
        best = QUALITIES.HIGH
        best_order = 3
        for source in sources:
            quality = sources[source]['quality']
            if quality is not None:
                if Q_ORDER[quality] > best_order:
                    best = quality
                    best_order = Q_ORDER[quality]
        return best
            
    def __get_mirror_links(self, html, page_quality, video):
        sources = {}
        for image in dom_parser.parse_dom(html, 'img', ret='src'):
            if image.endswith('/mirrors.png'):
                match = re.search('%s.*?<p>(.*?)</p>' % (image), html, re.DOTALL)
                if match:
                    for link in dom_parser.parse_dom(match.group(1), 'a', ret='href'):
                        host = urlparse.urlparse(link).hostname
                        sources[link] = {'quality': scraper_utils.get_quality(video, host, page_quality), 'direct': False}
        return sources
    
    def get_url(self, video):
        return self._blog_get_url(video)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        html = self._http_get(self.base_url, params={'s': title}, cache_limit=2)
        pattern = 'class="entry-title">\s*<a[^>]+href="(?P<url>[^"]+)[^>]*>\s*(?P<post_title>[^<]+)'
        return self._blog_proc_results(html, pattern, '', video_type, title, year)

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


BASE_URL = 'http://movieswatchmovie.com'
LINK_URL = '/watchmovieplayer/gkpluginsphp.php'

class MWM_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'MWM'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        sources = {}
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            sources.update(self.__get_gk_links(html, url))
            sources.update(self.__get_iframe_links(html))
            
            for source in sources:
                host = self._get_direct_hostname(source)
                stream_url = source + '|User-Agent=%s' % (scraper_utils.get_ua())
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': sources[source], 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
                hosters.append(hoster)

        return hosters

    def __get_iframe_links(self, html):
        sources = {}
        for iframe_url in dom_parser.parse_dom(html, 'iframe', ret='src'):
            html = self._http_get(iframe_url, cache_limit=.25)
            for match in re.finditer('"file"\s*:\s*"([^"]+)"\s*,\s*"label"\s*:\s*"([^"]+)', html, re.DOTALL):
                stream_url, height = match.groups()
                stream_url = re.sub('; .*', '', stream_url)
                if self._get_direct_hostname(stream_url) == 'gvideo':
                    quality = scraper_utils.gv_get_quality(stream_url)
                else:
                    quality = scraper_utils.height_get_quality(height)
                sources[stream_url] = quality
        return sources
    
    def __get_gk_links(self, html, page_url):
        sources = {}
        match = re.search('{link\s*:\s*"([^"]+)', html)
        if match:
            data = {'link': match.group(1)}
            url = urlparse.urljoin(self.base_url, LINK_URL)
            headers = {'Referer': page_url}
            html = self._http_get(url, data=data, headers=headers, cache_limit=.25)
            js_data = scraper_utils.parse_json(html, url)
            if 'link' in js_data:
                for link in js_data['link']:
                    if 'type' in link and link['type'] == 'mp4' and 'link' in link:
                        if self._get_direct_hostname(link['link']) == 'gvideo':
                            quality = scraper_utils.gv_get_quality(link['link'])
                        elif 'label' in link:
                            quality = scraper_utils.height_get_quality(link['label'])
                        else:
                            quality = QUALITIES.HIGH
                        sources[link['link']] = quality
        return sources

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year):
        search_url = urlparse.urljoin(self.base_url, '/?s=%s' % (urllib.quote_plus(title)))
        html = self._http_get(search_url, cache_limit=1)
        results = []
        for item in dom_parser.parse_dom(html, 'div', {'class': '[^"]*news-summary[^"]*'}):
            match = re.search('href="([^"]+)[^>]+>([^<]+)', item)
            if match:
                match_url, match_title_year = match.groups()
                match = re.search('(.*?)\s+\(?(\d{4})\)?', match_title_year)
                if match:
                    match_title, match_year = match.groups()
                else:
                    match_title = match_title_year
                    match_year = ''
                
                match_title = match_title.replace('Full Movie', '').replace('Watch Online', '').replace('&#8217;', "'")
                if not year or not match_year or year == match_year:
                    if any((item for item in results if item['title'] == match_title and item['year'] == match_year)):
                        continue
                    
                    result = {'title': match_title.strip(), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)

        return results

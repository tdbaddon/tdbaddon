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
import kodi
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import XHR
import scraper

VIDEO_URL = '/video_info/iframe'

class Scraper(scraper.Scraper):
    OPTIONS = ['https://xmovies8.org', 'http://genvideos.org', 'https://putlockerhd.co']
    
    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'xmovies8'

    def resolve_link(self, link):
        link = link.split('|', 1)[0]
        html = self._http_get(link, allow_redirect=False, method='HEAD', cache_limit=0)
        if html.startswith('http'):
            return html
        else:
            return link

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.5)
            match = re.search('var\s*video_id="([^"]+)', html)
            if match:
                video_id = match.group(1)
                url = urlparse.urljoin(self.base_url, VIDEO_URL)
                headers = {'Referer': page_url}
                headers.update(XHR)
                html = self._http_get(url, data={'v': video_id}, headers=headers, cache_limit=.5)
                sources = scraper_utils.parse_json(html, url)
                for source in sources:
                    match = re.search('url=(.*)', sources[source])
                    if match:
                        stream_url = urllib.unquote(match.group(1))
                        host = self._get_direct_hostname(stream_url)
                        if host == 'gvideo':
                            quality = scraper_utils.gv_get_quality(stream_url)
                        else:
                            quality = scraper_utils.height_get_quality(source)
                        stream_url += scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
                        hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
                        hosters.append(hoster)
        return hosters
        
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        search_url = urlparse.urljoin(self.base_url, '/results')
        html = self._http_get(search_url, params={'q': title}, cache_limit=1)
        results = []
        for result in dom_parser.parse_dom(html, 'div', {'class': 'cell'}):
            match = re.search('class="video_title".*?href="([^"]+)"[^>]*>\s*([^<]+)', result, re.DOTALL)
            if match:
                url, match_title_year = match.groups()
                match_title, match_year = scraper_utils.extra_year(match_title_year)
                if not match_year:
                    match = re.search('class="video_quality".*?Year\s*(?:</b>)?\s*:\s*(\d{4})', result, re.DOTALL)
                    if match:
                        match_year = match.group(1)
                    else:
                        match_year = ''

                if not year or not match_year or year == match_year:
                    result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)
        return results

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        settings.append('         <setting id="%s-default_url" type="text" visible="false"/>' % (cls.get_name()))
        return settings

scraper_utils.set_default_url(Scraper)

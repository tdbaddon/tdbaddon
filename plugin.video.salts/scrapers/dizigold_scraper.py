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

from salts_lib import dom_parser
from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://www.dizigold.net'
AJAX_URL = '/sistem/ajax.php'
XHR = {'X-Requested-With': 'XMLHttpRequest'}

class Dizigold_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.ajax_url = urlparse.urljoin(self.base_url, AJAX_URL)

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'Dizigold'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        sources = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.25)
            match = re.search('var\s+view_id\s*=\s*"([^"]+)', html)
            if match:
                view_data = {'id': match.group(1), 'tip': 'view', 'dil': 'or'}
                html = self._http_get(self.ajax_url, data=view_data, headers=XHR, cache_limit=.25)
                html = html.strip()
                html = re.sub(r'\\n|\\t', '', html)
                match = re.search('var\s+sources\s*=\s*(\[.*?\])', html)
                if match:
                    raw_data = match.group(1)
                    raw_data = raw_data.replace('\\', '')
                else:
                    raw_data = html
                
                js_data = scraper_utils.parse_json(raw_data, self.ajax_url)
                if 'data' in js_data:
                    src = dom_parser.parse_dom(js_data['data'], 'iframe', ret='src')
                    if src:
                        html = self._http_get(src[0], cache_limit=.25)
                        match = re.search('url=([^"]+)', html)
                        if match:
                            stream_url = match.group(1).replace('&gt;', '')
                            sources.append({'label': '720p', 'file': stream_url})
                            direct = False
                        else:
                            src = dom_parser.parse_dom(html, 'iframe', ret='src')
                            if src:
                                sources.append({'label': '720p', 'file': src[0]})
                                direct = False
                            else:
                                for match in re.finditer('"file"\s*:\s*"([^"]+)"\s*,\s*"label"\s*:\s*"([^"]+)', html):
                                    sources.append({'label': match.group(2), 'file': match.group(1)})
                                direct = True
                else:
                    sources = js_data
                    direct = True

                for source in sources:
                    stream_url = source['file'] + '|User-Agent=%s' % (scraper_utils.get_ua())
                    if direct:
                        host = self._get_direct_hostname(stream_url)
                        if host == 'gvideo':
                            quality = scraper_utils.gv_get_quality(stream_url)
                        else:
                            quality = scraper_utils.height_get_quality(source['label'])
                    else:
                        host = urlparse.urlparse(stream_url).hostname
                        quality = scraper_utils.height_get_quality(source['label'])
                
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': direct}
                    hosters.append(hoster)
    
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+/%s-sezon/%s-[^"]*bolum[^"]*)' % (video.season, video.episode)
        title_pattern = 'href="(?P<url>[^"]+)"\s+class="realcuf".*?<p\s+class="realcuf">(?P<title>[^<]+)'
        return self._default_get_episode_url(show_url, video, episode_pattern, title_pattern)

    def search(self, video_type, title, year, season=''):
        html = self._http_get(self.base_url, cache_limit=48)
        results = []
        fragment = dom_parser.parse_dom(html, 'div', {'class': 'dizis'})
        norm_title = scraper_utils.normalize_title(title)
        if fragment:
            for match in re.finditer('href="([^"]+)[^>]+>([^<]+)', fragment[0]):
                url, match_title = match.groups()
                if norm_title in scraper_utils.normalize_title(match_title):
                    result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(match_title), 'year': ''}
                    results.append(result)

        return results

# -*- coding: utf-8 -*-
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
import scraper

BASE_URL = 'http://diziay.com'
SEASON_URL = '/posts/filmgonder.php?action=sezongets'
AJAX_URL = 'http://dizipas.org/player/ajax.php'
XHR = {'X-Requested-With': 'XMLHttpRequest'}

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'Diziay'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        sources = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=1)
            fragment = dom_parser.parse_dom(html, 'div', {'class': 'player'})
            if fragment:
                iframe_url = dom_parser.parse_dom(fragment[0], 'iframe', ret='src')
                if iframe_url:
                    html = self._http_get(iframe_url[0], cache_limit=.5)
                    sources.append(self.__get_embedded_sources(html))
                    sources.append(self.__get_linked_sources(html))
                    for source in sources:
                        for stream_url in source['sources']:
                            host = self._get_direct_hostname(stream_url)
                            if host == 'gvideo':
                                quality = scraper_utils.gv_get_quality(stream_url)
                                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
                                hoster['subs'] = source.get('subs', True)
                                hosters.append(hoster)
    
        return hosters

    def __get_embedded_sources(self, html):
        sources = []
        # if captions exist, then they aren't hardcoded
        subs = '' if re.search('''"?kind"?\s*:\s*"?captions"?''', html) else 'Turkish subtitles'
        for stream_url in dom_parser.parse_dom(html, 'source', {'type': 'video/mp4'}, ret='src'):
            sources.append(stream_url)
        return {'sources': sources, 'subs': subs}
        
    def __get_linked_sources(self, html):
        sources = []
        subs = 'Turkish subtitles'
        match = re.search('fvid\s*=\s*"([^"]+)', html)
        if match:
            html = self._http_get(AJAX_URL, params={'dizi': match.group(1)}, headers=XHR, cache_limit=.5)
            js_result = scraper_utils.parse_json(html, AJAX_URL)
            # subs are hardcoded if none exist
            subs = '' if 'altyazi' in js_result and js_result['altyazi'] else 'Turkish subtitles'
            for source in js_result.get('success', []):
                if 'src' in source:
                    sources.append(source['src'])
                        
        return {'sources': sources, 'subs': subs}
    
    def _get_episode_url(self, show_url, video):
        url = urlparse.urljoin(self.base_url, show_url)
        html = self._http_get(url, cache_limit=24)
        show_id = dom_parser.parse_dom(html, 'div', {'id': 'icerikid'}, ret='value')
        if show_id:
            data = {'sezon_id': video.season, 'dizi_id': show_id[0], 'tip': 'dizi', 'bolumid': ''}
            episode_pattern = 'href="([^"]+/[^"]*%s-sezon-%s-bolum[^"]*)"' % (video.season, video.episode)
            title_pattern = 'href="(?P<url>[^"]*-\d+-sezon-\d+-bolum[^"]*)[^>]*>.*?class="realcuf">(?P<title>[^<]*)'
            return self._default_get_episode_url(SEASON_URL, video, episode_pattern, title_pattern, data=data, headers=XHR)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        html = self._http_get(self.base_url, cache_limit=8)
        results = []
        fragment = dom_parser.parse_dom(html, 'div', {'class': '[^"]*dizis[^"]*'})
        norm_title = scraper_utils.normalize_title(title)
        if fragment:
            for match in re.finditer('href="([^"]+)[^>]*>([^<]+)', fragment[0]):
                url, match_title = match.groups()
                if norm_title in scraper_utils.normalize_title(match_title):
                    result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(match_title), 'year': ''}
                    results.append(result)

        return results

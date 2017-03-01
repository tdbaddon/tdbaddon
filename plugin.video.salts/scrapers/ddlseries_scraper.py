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
import log_utils  # @UnusedImport
import kodi
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
from salts_lib.constants import Q_ORDER
import scraper

BASE_URL = 'http://www.ddlseries.me'
QUALITY_MAP = {'SD-XVID': QUALITIES.MEDIUM, 'DVD9': QUALITIES.HIGH, 'SD-X264': QUALITIES.HIGH,
               'HD-720P': QUALITIES.HD720, 'HD-1080P': QUALITIES.HD1080}
HEADER_MAP = {'ul.png': 'uploaded.net', 'tb.png': 'turbobit.net', 'utb.png': 'uptobox.com'}

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.max_qorder = 5 - int(kodi.get_setting('%s_quality' % VIDEO_TYPES.EPISODE))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.SEASON, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'DDLSeries'

    def resolve_link(self, link):
        if 'protect-links' in link:
            html = self._http_get(link, require_debrid=True, cache_limit=0)
            item = dom_parser.parse_dom(html, 'li')
            if item:
                stream_url = dom_parser.parse_dom(item[0], 'a', ret='href')
                if stream_url:
                    return stream_url[0]
        else:
            return link
    
    def get_sources(self, video):
        source_url = self.get_url(video)
        if source_url and source_url != FORCE_NO_MATCH:
            hosters = self.__get_sources(source_url, video)
        else:
            hosters = []
                
        return hosters

    def __get_sources(self, season_url, video):
        hosters = []
        url = urlparse.urljoin(self.base_url, season_url)
        html = self._http_get(url, require_debrid=True, cache_limit=.5)
        _part, quality = self.__get_quality(url)
        pattern = '<img[^>]+src="([^"]+)[^>]+alt="[^"]+Download Links"[^>]*>(.*?)(?=<img|</div>)'
        for match in re.finditer(pattern, html, re.I | re.DOTALL):
            image, fragment = match.groups()
            image = image.split('/')[-1]
            host = HEADER_MAP.get(image)
            if host:
                ep_pattern = 'href="([^"]+)[^>]*>\s*Episode\s+0*%s<' % (video.episode)
                for match in re.finditer(ep_pattern, fragment):
                    stream_url = match.group(1)
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'views': None, 'url': stream_url, 'rating': None, 'quality': quality, 'direct': False}
                    hosters.append(hoster)
                
        return hosters
    
    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        settings = scraper_utils.disable_sub_check(settings)
        return settings

    def _get_episode_url(self, season_url, video):
        if self.__get_sources(season_url, video):
            return season_url
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        try: season = int(season)
        except: season = 0
        query = '%s season %s' % (title, season)
        data = {'story': query, 'do': 'search', 'subaction': 'search'}
        html = self._http_get(self.base_url + '/', data=data, require_debrid=True, cache_limit=8)
        for div in dom_parser.parse_dom(html, 'div', {'class': 'cover_infos_title'}):
            for match in re.finditer('href="([^"]+)[^>]*>(.*?)</a>', div):
                match_url, match_title = match.groups()
                if '/tv-pack/' in match_url: continue
                
                match_title = re.sub('(</?span[^>]*>|</?b>)', '', match_title)
                match_season = re.search('Season\s+(\d+)', match_title, re.I)
                if match_season:
                    match_season = int(match_season.group(1))
                    if not season or season == match_season:
                        _q_str, quality = self.__get_quality(match_url)
                        if Q_ORDER[quality] <= self.max_qorder:
                            result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': '', 'quality': quality}
                            results.append(result)
        
        results.sort(key=lambda x: Q_ORDER[x['quality']], reverse=True)
        return results

    def __get_quality(self, match_url):
        for part in match_url.split('/'):
            part = part.upper()
            if part in QUALITY_MAP:
                return part, QUALITY_MAP[part]
        
        return '', QUALITIES.HIGH
    
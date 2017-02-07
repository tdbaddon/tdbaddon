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
QUALITY_MAP = {'SDXVID': QUALITIES.MEDIUM, 'DVD9': QUALITIES.HIGH, 'SDX264': QUALITIES.HIGH, 'HD720P': QUALITIES.HD720, 'HD1080P': QUALITIES.HD1080}
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
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            hosters = self.__get_sources(source_url, video)
                
        return hosters

    def __get_sources(self, season_url, video):
        hosters = []
        url = urlparse.urljoin(self.base_url, season_url)
        html = self._http_get(url, require_debrid=True, cache_limit=.5)
        quality = QUALITIES.HIGH
        titles = dom_parser.parse_dom(html, 'span', {'itemprop': 'title'})
        for title in titles:
            title = title.replace(' ', '').upper()
            quality = QUALITY_MAP.get(title)
            if quality is not None:
                break
        else:
            page_title = dom_parser.parse_dom(html, 'title')
            if page_title:
                _title, _season, q_str, _is_pack = self.__get_title_parts(page_title[0])
                for key in QUALITY_MAP:
                    if key in q_str:
                        quality = QUALITY_MAP[key]
                        break
        
        pattern = '<img[^>]+src="([^"]+)[^>]+alt="[^"]+Download Links">(.*?)(?=<img|</div>)'
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
        if video_type == VIDEO_TYPES.SEASON and title:
            url = urlparse.urljoin(self.base_url, '/tv-series-list.html')
            html = self._http_get(url, require_debrid=True, cache_limit=24)
            fragment = dom_parser.parse_dom(html, 'div', {'class': 'downpara-list'})
            norm_title = scraper_utils.normalize_title(title)
            if fragment:
                for match in re.finditer('href="([^"]+)[^>]*>(.*?)</a>', fragment[0]):
                    match_url, match_title_extra = match.groups()
                    match_title, match_season, q_str, is_pack = self.__get_title_parts(match_title_extra)
                    if is_pack: continue
                    
                    if norm_title in scraper_utils.normalize_title(match_title) and (not season or season == int(match_season)):
                        quality = QUALITY_MAP.get(q_str, QUALITIES.HIGH)
                        if Q_ORDER[quality] <= self.max_qorder:
                            match_title = '%s - Season %s [%s]' % (match_title, match_season, q_str)
                            result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': '', 'quality': quality}
                            results.append(result)
        
        results.sort(key=lambda x: Q_ORDER[x['quality']], reverse=True)
        return results

    def __get_title_parts(self, title):
        title = re.sub('</?span[^>]*>', '', title)
        title = title.replace('&nbsp;', ' ')
        match = re.search('(.*?)\s*-?\s*Season\s+(\d+)\s*(.*)', title)
        if match:
            match_title, match_season, extra = match.groups()
            extra = extra.replace(' ', '').upper()
            is_pack = True if '(PACK)' in extra else False
            for s in ('[', ']', '(PACK)', 'EPISODES'):
                extra = extra.replace(s, '')
            return match_title, match_season, extra, is_pack
        else:
            return title, 0, '', False

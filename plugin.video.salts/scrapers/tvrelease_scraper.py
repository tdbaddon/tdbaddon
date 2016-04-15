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
from salts_lib import log_utils
from salts_lib import dom_parser
from salts_lib import kodi
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
from salts_lib.kodi import i18n
import scraper


BASE_URL = 'http://tv-release.net'
QUALITY_MAP = {'MOVIES-XVID': QUALITIES.MEDIUM, 'TV-XVID': QUALITIES.HIGH, 'TV-MP4': QUALITIES.HIGH, 'TV-480P': QUALITIES.HIGH,
               'TV-X265': QUALITIES.HD720, 'MOVIES-480P': QUALITIES.HIGH, 'TV-720P': QUALITIES.HD720, 'MOVIES-720P': QUALITIES.HD720}

class TVReleaseNet_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'TVRelease.Net'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        if 'size' in item:
            label += ' (%s)' % (item['size'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        host_count = {}
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)

            q_str = ''
            match = re.search('>Release.*?td_col">([^<]+)', html)
            if match:
                q_str = match.group(1).upper()
                
            size = ''
            match = re.search('>Size.*?td_col">([^<]+)', html)
            if match:
                size = match.group(1).upper()
            
            fragment = dom_parser.parse_dom(html, 'table', {'id': 'download_table'})
            if fragment:
                for match in re.finditer('''href=['"]([^'"]+)''', fragment[0]):
                    stream_url = match.group(1)
                    if re.search('\.rar(\.|$)', stream_url):
                        continue
    
                    host = urlparse.urlsplit(stream_url).hostname
                    if q_str:
                        if video.video_type == VIDEO_TYPES.EPISODE:
                            _title, _season, _episode, height, _extra = scraper_utils.parse_episode_link(q_str)
                        else:
                            _title, _year, height, _extra = scraper_utils.parse_movie_link(q_str)
                        quality = scraper_utils.height_get_quality(height)
                    else:
                        quality = QUALITY_MAP.get(match.group(1).upper(), QUALITIES.HIGH)
                    quality = scraper_utils.get_quality(video, host, quality)
                    host_count[host] = host_count.get(host, 0) + 1
                    hoster = {'multi-part': False, 'class': self, 'host': host, 'quality': quality, 'views': None, 'url': stream_url, 'rating': None, 'direct': False}
                    if size: hoster['size'] = size
                    hosters.append(hoster)

        new_hosters = [hoster for hoster in hosters if host_count[hoster['host']] <= 1]
        return new_hosters

    def get_url(self, video):
        return self._blog_get_url(video, delim=' ')

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        settings = scraper_utils.disable_sub_check(settings)
        name = cls.get_name()
        settings.append('         <setting id="%s-filter" type="slider" range="0,180" option="int" label="     %s" default="30" visible="eq(-4,true)"/>' % (name, i18n('filter_results_days')))
        settings.append('         <setting id="%s-select" type="enum" label="     %s" lvalues="30636|30637" default="0" visible="eq(-5,true)"/>' % (name, i18n('auto_select')))
        return settings

    def search(self, video_type, title, year, season=''):
        search_url = urlparse.urljoin(self.base_url, '/?s=')
        search_url += urllib.quote(title)
        if video_type == VIDEO_TYPES.EPISODE:
            search_url += '&cat=TV-XviD,TV-Mp4,TV-720p,TV-480p,'
        else:
            search_url += '&cat=Movies-XviD,Movies-720p,Movies-480p'
        html = self._http_get(search_url, cache_limit=.25)
        tables = dom_parser.parse_dom(html, 'table', {'class': 'posts_table'})
        if tables:
            html = ''.join(tables)
            pattern = "<a[^>]+>(?P<quality>[^<]+).*?href='(?P<url>[^']+)'>(?P<post_title>[^<]+).*?(?P<date>[^>]+)</td></tr>"
            date_format = '%Y-%m-%d %H:%M:%S'
            return self._blog_proc_results(html, pattern, date_format, video_type, title, year)
        else:
            return []

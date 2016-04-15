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

from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.kodi import i18n
import scraper


BASE_URL = 'http://members.easynews.com'
SORT = 's1=relevance&s1d=-&s2=dsize&s2d=-&s3=dtime&s3d=-'
VID_FILTER = 'fex=mkv%%2C+mp4%%2C+avi'
# RANGE_FILTERS = 'd1=&d1t=&d2=&d2t=&b1=&b1t=&b2=&b2t=&px1=&px1t=&px2=&px2t=&fps1=&fps1t=&fps2=&fps2t=&bps1=&bps1t=&bps2=&bps2t=&hz1=&hz1t=&hz2=&hz2t=&rn1=&rn1t=1&rn2=&rn2t='
SEARCH_URL = '/2.0/search/solr-search/advanced?st=adv&safeO=0&sb=1&%s&%s&fty[]=VIDEO&spamf=1&u=1&gx=1&pby=100&pno=1&sS=3' % (VID_FILTER, SORT)
SEARCH_URL += '&gps=%s&sbj=%s'

class EasyNews_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.username = kodi.get_setting('%s-username' % (self.get_name()))
        self.password = kodi.get_setting('%s-password' % (self.get_name()))
        self.cookie = {'chickenlicker': '%s%%3A%s' % (self.username, self.password)}

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'EasyNews'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        if 'format' in item:
            label = '[%s] (%s) %s' % (item['quality'], item['format'], item['host'])
        else:
            label = '[%s] %s' % (item['quality'], item['host'])
        if 'size' in item:
            label += ' (%s)' % (item['size'])
        if 'extra' in item:
            label += ' [%s]' % (item['extra'])
        return label

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if source_url and source_url != FORCE_NO_MATCH:
            params = urlparse.parse_qs(urlparse.urlparse(source_url).query)
            if 'title' in params:
                query = params['title'][0].replace("'", "")
                if video.video_type == VIDEO_TYPES.MOVIE:
                    if 'year' in params: query += ' %s' % (params['year'][0])
                else:
                    sxe = ''
                    if 'season' in params:
                        sxe = 'S%02d' % (int(params['season'][0]))
                    if 'episode' in params:
                        sxe += 'E%02d' % (int(params['episode'][0]))
                    if sxe: query = '%s %s' % (query, sxe)
                query = urllib.quote_plus(query)
                query_url = '/search?query=%s' % (query)
                hosters = self.__get_links(query_url, video)
                if not hosters and video.video_type == VIDEO_TYPES.EPISODE and params['air_date'][0]:
                    query = urllib.quote_plus('%s %s' % (params['title'][0], params['air_date'][0].replace('-', '.')))
                    query_url = '/search?query=%s' % (query)
                    hosters = self.__get_links(query_url, video)

        return hosters
    
    def __get_links(self, url, video):
        hosters = []
        search_url = self.__translate_search(url)
        html = self._http_get(search_url, cache_limit=.5)
        js_result = scraper_utils.parse_json(html, search_url)
        if 'data' in js_result:
            for item in js_result['data']:
                post_hash, size, post_title, ext, duration = item['0'], item['4'], item['10'], item['11'], item['14']
                checks = [False] * 6
                if not scraper_utils.title_check(video, post_title): checks[0] = True
                if 'alangs' in item and item['alangs'] and 'eng' not in item['alangs']: checks[1] = True
                if re.match('^\d+s', duration) or re.match('^[0-5]m', duration): checks[2] = True
                if 'passwd' in item and item['passwd']: checks[3] = True
                if 'virus' in item and item['virus']: checks[4] = True
                if 'type' in item and item['type'].upper() != 'VIDEO': checks[5] = True
                if any(checks):
                    log_utils.log('EasyNews Post excluded: %s - |%s|' % (checks, item), log_utils.LOGDEBUG)
                    continue
                
                stream_url = urllib.quote('%s%s/%s%s' % (post_hash, ext, post_title, ext))
                stream_url = 'http://members.easynews.com/dl/%s' % (stream_url)
                stream_url = stream_url + '|Cookie=%s' % (self._get_stream_cookies())
                host = self._get_direct_hostname(stream_url)
                quality = None
                if 'width' in item:
                    try: width = int(item['width'])
                    except: width = 0
                    if width:
                        quality = scraper_utils.width_get_quality(width)
                
                if quality is None:
                    if video.video_type == VIDEO_TYPES.MOVIE:
                        _title, _year, height, _extra = scraper_utils.parse_movie_link(post_title)
                    else:
                        _title, _season, _episode, height, _extra = scraper_utils.parse_episode_link(post_title)
                    quality = scraper_utils.height_get_quality(height)
                    
                hoster = {'multi-part': False, 'class': self, 'views': None, 'url': stream_url, 'rating': None, 'host': host, 'quality': quality, 'direct': True}
                if any(i for i in ['X265', 'HEVC'] if i in post_title.upper()): hoster['format'] = 'x265'
                if size: hoster['size'] = size
                if post_title: hoster['extra'] = post_title
                hosters.append(hoster)
        return hosters
    
    def get_url(self, video):
        url = None
        self.create_db_connection()
        result = self.db_connection.get_related_url(video.video_type, video.title, video.year, self.get_name(), video.season, video.episode)
        if result:
            url = result[0][0]
            log_utils.log('Got local related url: |%s|%s|%s|%s|%s|' % (video.video_type, video.title, video.year, self.get_name(), url), log_utils.LOGDEBUG)
        else:
            if video.video_type == VIDEO_TYPES.MOVIE:
                query = 'title=%s&year=%s' % (urllib.quote_plus(video.title), video.year)
            else:
                query = 'title=%s&season=%s&episode=%s&air_date=%s' % (urllib.quote_plus(video.title), video.season, video.episode, video.ep_airdate)
            url = '/search?%s' % (query)
            self.db_connection.set_related_url(video.video_type, video.title, video.year, self.get_name(), url, video.season, video.episode)
        return url

    def search(self, video_type, title, year, season=''):
        return []

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        settings = scraper_utils.disable_sub_check(settings)
        name = cls.get_name()
        settings.append('         <setting id="%s-username" type="text" label="     %s" default="" visible="eq(-4,true)"/>' % (name, i18n('username')))
        settings.append('         <setting id="%s-password" type="text" label="     %s" option="hidden" default="" visible="eq(-5,true)"/>' % (name, i18n('password')))
        return settings

    def _http_get(self, url, cache_limit=8):
        if not self.username or not self.password:
            return ''
        
        return self._cached_http_get(url, self.base_url, self.timeout, cookies=self.cookie, cache_limit=cache_limit)

    def __translate_search(self, url):
        query = urllib.quote_plus(urlparse.parse_qs(urlparse.urlparse(url).query)['query'][0])
        url = urlparse.urljoin(self.base_url, SEARCH_URL % (query, query))
        return url

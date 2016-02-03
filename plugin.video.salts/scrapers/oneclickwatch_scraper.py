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
import scraper
import urllib
import urlparse
import re
from salts_lib import kodi
from salts_lib import log_utils
from salts_lib.trans_utils import i18n
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH

BASE_URL = 'http://oneclickwatch.ws'

class OneClickWatch_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'OneClickWatch'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        return '[%s] %s' % (item['quality'], item['host'])

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            headers = {'Referer': self.base_url}
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, headers=headers, cache_limit=.5)

            q_str = ''
            match = re.search('class="title">([^<]+)', html)
            if match:
                q_str = match.group(1)

            pattern = '^<a\s+href="([^"]+)"\s+rel="nofollow"'
            for match in re.finditer(pattern, html, re.M):
                url = match.group(1)
                hoster = {'multi-part': False, 'class': self, 'views': None, 'url': url, 'rating': None, 'direct': False}
                hoster['host'] = urlparse.urlsplit(url).hostname
                hoster['quality'] = self._blog_get_quality(video, q_str, hoster['host'])
                hosters.append(hoster)

        return hosters

    def get_url(self, video):
        return self._blog_get_url(video)

    @classmethod
    def get_settings(cls):
        settings = super(OneClickWatch_Scraper, cls).get_settings()
        settings = cls._disable_sub_check(settings)
        name = cls.get_name()
        settings.append('         <setting id="%s-filter" type="slider" range="0,180" option="int" label="     %s" default="30" visible="eq(-4,true)"/>' % (name, i18n('filter_results_days')))
        settings.append('         <setting id="%s-select" type="enum" label="     %s" lvalues="30636|30637" default="0" visible="eq(-5,true)"/>' % (name, i18n('auto_select')))
        return settings

    def search(self, video_type, title, year):
        search_url = urlparse.urljoin(self.base_url, '/?search=%s' % (urllib.quote_plus(title)))
        headers = {'Referer': self.base_url}
        html = self._http_get(search_url, headers=headers, cache_limit=.25)
        pattern = 'class="title"><a href="(?P<url>[^"]+)[^>]+>(?P<post_title>[^<]+).*?rel="bookmark">(?P<date>[^<]+)'
        date_format = '%B %d, %Y'
        return self._blog_proc_results(html, pattern, date_format, video_type, title, year)

    def _http_get(self, url, headers=None, cache_limit=8):
        html = super(OneClickWatch_Scraper, self)._cached_http_get(url, self.base_url, self.timeout, headers=headers, cache_limit=cache_limit)
        cookie = self._get_sucuri_cookie(html)
        if cookie:
            log_utils.log('Setting OCW cookie: %s' % (cookie), log_utils.LOGDEBUG)
            html = super(OneClickWatch_Scraper, self)._cached_http_get(url, self.base_url, self.timeout, cookies=cookie, headers=headers, cache_limit=0)
        return html

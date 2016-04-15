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
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://rlsblog.net'

class RLSSource_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'RLSSource.net'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        return '[%s] %s' % (item['quality'], item['host'])

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            
            q_str = ''
            match = re.search('class="entry-title">([^<]+)', html)
            if match:
                q_str = match.group(1)

            pattern = 'href="?([^" ]+)(?:[^>]+>){2}\s+\|'
            for match in re.finditer(pattern, html, re.DOTALL):
                url = match.group(1)
                if 'adf.ly' in url:
                    continue
                
                hoster = {'multi-part': False, 'class': self, 'views': None, 'url': url, 'rating': None, 'quality': None, 'direct': False}
                hoster['host'] = urlparse.urlsplit(url).hostname
                hoster['quality'] = scraper_utils.blog_get_quality(video, q_str, hoster['host'])
                hosters.append(hoster)

        return hosters

    def get_url(self, video):
        return self._blog_get_url(video, delim=' ')

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        settings = scraper_utils.disable_sub_check(settings)
        name = cls.get_name()
        settings.append('         <setting id="%s-filter" type="slider" range="0,180" option="int" label="     Filter results older than (0=No Filter) (days)" default="30" visible="eq(-4,true)"/>' % (name))
        settings.append('         <setting id="%s-select" type="enum" label="     Automatically Select" values="Most Recent|Highest Quality" default="0" visible="eq(-5,true)"/>' % (name))
        return settings

    def search(self, video_type, title, year, season=''):
        search_url = urlparse.urljoin(self.base_url, '/?s=%s&go=Search' % (urllib.quote_plus(title)))
        html = self._http_get(search_url, cache_limit=1)
        pattern = 'href="(?P<url>[^"]+)[^>]+rel="bookmark">(?P<post_title>[^<]+).*?class="entry-date">(?P<date>\d+/\d+/\d+)'
        date_format = '%m/%d/%Y'
        return self._blog_proc_results(html, pattern, date_format, video_type, title, year)

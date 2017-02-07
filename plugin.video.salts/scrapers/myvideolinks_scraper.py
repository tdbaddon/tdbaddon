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
from salts_lib.utils2 import i18n
import scraper


BASE_URL = 'http://newmyvideolink.xyz/dl'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.base_url = self.__check_base()

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'MyVideoLinks.eu'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)

            views = None
            pattern = '</i>\s*(\d+)\s*views'
            match = re.search(pattern, html, re.I)
            if match:
                views = int(match.group(1))

            if video.video_type == VIDEO_TYPES.MOVIE:
                return self.__get_movie_links(video, views, html)
            else:
                return self.__get_episode_links(video, views, html)
        return hosters

    def __get_movie_links(self, video, views, html):
        post_title = dom_parser.parse_dom(html, 'h1', {'class': '[^"]*post-title[^"]*'})
        q_str = post_title[0] if post_title else ''
        
        fragment = html
        entry = dom_parser.parse_dom(html, 'div', {'class': 'entry-content'})
        if entry:
            ul = dom_parser.parse_dom(entry[0], 'ul')
            if ul: fragment = ul[0]
            
        return self.__get_links(video, views, fragment, q_str)

    def __get_episode_links(self, video, views, html):
        pattern = '<h1>(.*?)</h1>\s*<ul>(.*?)</ul>'
        hosters = []
        for match in re.finditer(pattern, html, re.DOTALL):
            q_str, fragment = match.groups()
            hosters += self.__get_links(video, views, fragment, q_str)
        return hosters

    def __get_links(self, video, views, html, q_str):
        pattern = 'li>\s*<a\s+href="(http[^"]+)'
        hosters = []
        for match in re.finditer(pattern, html, re.DOTALL):
            url = match.group(1)
            hoster = {'multi-part': False, 'class': self, 'views': views, 'url': url, 'rating': None, 'quality': None, 'direct': False}
            hoster['host'] = urlparse.urlsplit(url).hostname
            hoster['quality'] = scraper_utils.blog_get_quality(video, q_str, hoster['host'])
            hosters.append(hoster)
        return hosters

    def __check_base(self):
        try:
            html = self._http_get(self.base_url, cache_limit=24)
            fragment = dom_parser.parse_dom(html, 'meta', {'http-equiv': 'refresh'}, ret='content')
            match = re.search('''URL\s*=\s*['"]([^"'])''', fragment[0])
            base_url = match.group(1)
        except:
            base_url = self.base_url
        return base_url
        
    def get_url(self, video):
        return self._blog_get_url(video)

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        settings = scraper_utils.disable_sub_check(settings)
        name = cls.get_name()
        settings.append('         <setting id="%s-filter" type="slider" range="0,180" option="int" label="     %s" default="30" visible="eq(-4,true)"/>' % (name, i18n('filter_results_days')))
        settings.append('         <setting id="%s-select" type="enum" label="     %s" lvalues="30636|30637" default="0" visible="eq(-5,true)"/>' % (name, i18n('auto_select')))
        return settings

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        html = self._http_get(self.base_url, params={'s': title}, cache_limit=1)
        pattern = 'class="post-title">\s*<a\s+href="(?P<url>[^"]*?(?P<post_date>\d{4}/\d{2}/\d{2})[^"]*)[^>]+title="(?:Permanent Link to )?(?P<post_title>[^"]+)'
        date_format = '%Y/%m/%d'
        return self._blog_proc_results(html, pattern, date_format, video_type, title, year)

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
import datetime
import re
import urlparse
import kodi
import utils
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.utils2 import i18n
import scraper


BASE_URL = 'http://scenehdtv.download'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'SceneHDTV'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        sources = {}
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, require_debrid=True, cache_limit=.5)
            fragment = dom_parser.parse_dom(html, 'div', {'class': 'entry-content'})
            if fragment:
                for td in dom_parser.parse_dom(fragment[0], 'td'):
                    for stream_url in dom_parser.parse_dom(td, 'a', ret='href'):
                        meta = scraper_utils.parse_episode_link(stream_url)
                        sources[stream_url] = scraper_utils.height_get_quality(meta['height'])

        for source in sources:
            if source:
                if scraper_utils.excluded_link(source): continue
                host = urlparse.urlparse(source).hostname
                hoster = {'multi-part': False, 'host': host, 'class': self, 'views': None, 'url': source, 'rating': None, 'quality': sources[source], 'direct': False}
                hosters.append(hoster)
        return hosters

    def get_url(self, video):
        return self._blog_get_url(video)

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        settings = scraper_utils.disable_sub_check(settings)
        name = cls.get_name()
        settings.append('         <setting id="%s-filter" type="slider" range="0,180" option="int" label="     %s" default="60" visible="eq(-3,true)"/>' % (name, i18n('filter_results_days')))
        settings.append('         <setting id="%s-select" type="enum" label="     %s" lvalues="30636|30637" default="0" visible="eq(-4,true)"/>' % (name, i18n('auto_select')))
        return settings

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        posts = []
        html = self._http_get(self.base_url, params={'s': title}, require_debrid=True, cache_limit=2)
        for post in dom_parser.parse_dom(html, 'header', {'class': 'entry-header'}):
            if self.__too_old(post): continue
            posts += dom_parser.parse_dom(post, 'h2', {'class': 'entry-title'})
            
        return self._blog_proc_results('\n'.join(posts), 'href="(?P<url>[^"]+)[^>]+>(?P<post_title>.*?)</a>', '', video_type, title, year)

    def __too_old(self, post):
        filter_days = datetime.timedelta(days=int(kodi.get_setting('%s-filter' % (self.get_name()))))
        post_date = dom_parser.parse_dom(post, 'time', {'class': 'updated'}, ret='datetime')
        if filter_days and post_date:
            today = datetime.date.today()
            try:
                post_date = datetime.date.fromtimestamp(utils.iso_2_utc(post_date[0]))
                if today - post_date > filter_days:
                    return True
            except ValueError:
                return False
        return False

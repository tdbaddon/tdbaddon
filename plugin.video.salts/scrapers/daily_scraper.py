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

BASE_URL = 'http://dailyreleases.net'

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
        return 'DailyReleases'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, require_debrid=True, cache_limit=.5)
            sources = self.__get_post_links(html, video)
            for source in sources:
                if re.search('\.part\.?\d+', source) or '.rar' in source or 'sample' in source or source.endswith('.nfo'): continue
                host = urlparse.urlparse(source).hostname
                hoster = {'multi-part': False, 'host': host, 'class': self, 'views': None, 'url': source, 'rating': None, 'quality': sources[source], 'direct': False}
                hosters.append(hoster)
        return hosters

    def __get_post_links(self, html, video):
        sources = {}
        post = dom_parser.parse_dom(html, 'div', {'class': 'post-body'})
        if post:
            for fragment in re.finditer('<hr\s*/>(.*?)(?=<hr\s*/>)', post[0], re.DOTALL):
                fragment = fragment.group(1)
                release = dom_parser.parse_dom(fragment, 'strong')
                if release:
                    meta = scraper_utils.parse_episode_link(release[0])
                    release_quality = scraper_utils.height_get_quality(meta['height'])
                    for link in dom_parser.parse_dom(fragment, 'a', ret='href'):
                        host = urlparse.urlparse(link).hostname
                        quality = scraper_utils.get_quality(video, host, release_quality)
                        sources[link] = quality
        return sources
        
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
        html = self._http_get(self.base_url, params={'s': title}, require_debrid=True, cache_limit=1)
        post_pattern = 'href=[\'"](?P<url>[^\'"]+)[^>]+class=[\'"]post_ttl["\'][^>]*>(?P<post_title>[^/]+).*?class=[\'"]post-date[\'"]\s*>(?P<date>[^<]+)'
        return self._blog_proc_results(html, post_pattern, '', video_type, title, year)

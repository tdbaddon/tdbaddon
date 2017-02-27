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
import base64
import urllib
import kodi
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://scenedown.in'
SEARCH_URL = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAxNjA3NTg1ODQxODU0MjAzNDgxODpiX21vd3ZnZDFkbSZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='

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
        return 'SceneDown'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, require_debrid=True, cache_limit=.5)
            sources = self.__get_post_links(html, video)
            for source in sources:
                if scraper_utils.excluded_link(source): continue
                host = urlparse.urlparse(source).hostname
                hoster = {'multi-part': False, 'host': host, 'class': self, 'views': None, 'url': source, 'rating': None, 'quality': sources[source], 'direct': False}
                hosters.append(hoster)
        return hosters

    def __get_post_links(self, html, video):
        sources = {}
        post = dom_parser.parse_dom(html, 'div', {'class': 'postContent'})
        if post:
            for fragment in re.finditer('<strong>(.*?)(?=<strong>|$)', post[0], re.DOTALL):
                fragment = '<strong>' + fragment.group(1)
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
        return settings

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = base64.decodestring(SEARCH_URL) % (urllib.quote_plus(title))
        html = self._http_get(search_url, cache_limit=2)
        js_data = scraper_utils.parse_json(html)
        search_meta = scraper_utils.parse_episode_link(title)
        for item in js_data.get('results', []):
            match_title = item.get('metatags', {}).get('ogTitle', '')
            if not match_title:
                match_title = item['titleNoFormatting']
                match_title = re.sub(re.compile('\s*-\s*Scene\s*Down$', re.I), '', match_title)
            match_url = item['url']
            match_year = ''
            item_meta = scraper_utils.parse_episode_link(match_title)
            if scraper_utils.meta_release_check(video_type, search_meta, item_meta):
                result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                results.append(result)
            
        return results


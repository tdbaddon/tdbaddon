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
import random
import re
import time
import urlparse

from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import BR_VERS
from salts_lib.constants import FEATURES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import RAND_UAS
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import WIN_VERS
import scraper


BASE_URL = 'http://twomovies.us'
AJAX_URL = '/Xajax/aj0001'
LOCAL_USER_AGENT = 'SALTS for Kodi/%s' % (kodi.get_version())
XHR = {'X-Requested-With': 'XMLHttpRequest'}

class TwoMovies_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'TwoMovies.us'

    def resolve_link(self, link):
        url = urlparse.urljoin(self.base_url, link)
        html = self._http_get(url, cookies={'links_tos': '1'}, cache_limit=0)
        match = re.search('''<iframe[^<]+src=(?:"|')([^"']+)''', html, re.DOTALL | re.I)
        if match:
            return match.group(1)
        else:
            match = re.search('href="[^"]*/go_away/\?go=([^"]+)', html)
            if match:
                return match.group(1)

    def format_source_label(self, item):
        return '[%s] %s' % (item['quality'], item['host'])

    def get_sources(self, video):
        sources = []
        source_url = self.get_url(video)
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=24)
            pattern = 'class="playDiv3".*?href="([^"]+).*?>(.*?)</a>'
            for match in re.finditer(pattern, html, re.DOTALL | re.I):
                url, host = match.groups()
                source = {'multi-part': False, 'url': scraper_utils.pathify_url(url), 'host': host, 'class': self, 'quality': scraper_utils.get_quality(video, host, QUALITIES.HIGH), 'rating': None, 'views': None, 'direct': False}
                sources.append(source)
        return sources

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year):
        results = []
        html = self._http_get(self.base_url, cache_limit=1)
        match = re.search('xajax.config.requestURI\s*=\s*"([^"]+)', html)
        if match:
            ajax_url = match.group(1)
        else:
            ajax_url = AJAX_URL
            
        search_url = urlparse.urljoin(self.base_url, ajax_url)
        xjxr = str(int(time.time() * 1000))
        search_arg = 'S<![CDATA[%s]]>' % (title)
        data = {'xjxfun': 'search_suggest', 'xjxr': xjxr, 'xjxargs[]': [search_arg, 'Stitle']}
        html = self._http_get(search_url, data=data, headers=XHR, cache_limit=12)
        if video_type == VIDEO_TYPES.MOVIE:
            marker = '/watch_movie/'
        else:
            marker = '/watch_tv_show/'
        
        for match in re.finditer('href="([^"]+)[^>]+>(.*?)</div>', html):
            url, match_title_year = match.groups()
            if marker not in url: continue
            match_title_year = re.sub('(<b>|</b>)', '', match_title_year)
             
            match = re.search('(.*?)\s+\(?(\d{4})\)?', match_title_year)
            if match:
                match_title, match_year = match.groups()
            else:
                match_title = match_title_year
                match_year = ''
            
            if not year or not match_year or year == match_year:
                result = {'url': scraper_utils.pathify_url(url), 'title': match_title, 'year': match_year}
                results.append(result)

        return results

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'class="linkname\d*" href="([^"]+/watch_episode/[^/]+/%s/%s/)"' % (video.season, video.episode)
        title_pattern = 'class="linkname"\s+href="(?P<url>[^"]+)">Episode_\d+\s+-\s+(?P<title>[^<]+)'
        headers = {'Referer': urlparse.urljoin(self.base_url, show_url)}
        return self._default_get_episode_url(show_url, video, episode_pattern, title_pattern, headers=headers)
    
    def _http_get(self, url, cookies=None, data=None, multipart_data=None, headers=None, allow_redirect=True, cache_limit=8):
        if headers is None: headers = {}
        if 'Referer' not in headers: headers['Referer'] = urlparse.urljoin(self.base_url, '/')
        headers.update({'User-Agent': LOCAL_USER_AGENT})
        return super(self.__class__, self)._http_get(url, cookies=cookies, data=data, multipart_data=multipart_data, headers=headers, allow_redirect=allow_redirect, cache_limit=cache_limit)

    def __randomize_ua(self):
        index = random.randrange(len(RAND_UAS))
        user_agent = RAND_UAS[index].format(win_ver=random.choice(WIN_VERS), feature=random.choice(FEATURES), br_ver=random.choice(BR_VERS[index]))
        log_utils.log('2Movies User Agent: %s' % (user_agent), log_utils.LOGDEBUG)
        return user_agent

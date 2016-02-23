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
from string import capwords
import urllib
import urlparse

from salts_lib import dom_parser
from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://www.streamlord.com'

class StreamLord_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'StreamLord'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=1)
            match = re.search('"file"\s*:\s*"([^"]+)', html)
            if match:
                if video.video_type == VIDEO_TYPES.MOVIE:
                    quality = QUALITIES.HD720
                else:
                    quality = QUALITIES.HIGH
                stream_url = match.group(1) + '|User-Agent=%s&Referer=%s' % (scraper_utils.get_ua(), urllib.quote(url))
                hoster = {'multi-part': False, 'host': self._get_direct_hostname(stream_url), 'class': self, 'url': stream_url, 'quality': quality, 'views': None, 'rating': None, 'direct': True}
                hosters.append(hoster)

        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="(episode[^"]*-[Ss]%02d[Ee]%02d-[^"]+)' % (int(video.season), int(video.episode))
        title_pattern = 'class="head".*?</span>(?P<title>.*?)</a>.*?href="(?P<url>[^"]+)'
        return self._default_get_episode_url(show_url, video, episode_pattern, title_pattern)
        
    def search(self, video_type, title, year):
        results = []
        url = urlparse.urljoin(self.base_url, '/search.html')
        data = {'search': title}
        html = self._http_get(url, data=data, cache_limit=2)
        if video_type == VIDEO_TYPES.MOVIE:
            query_type = 'watch-movie-'
        else:
            query_type = 'watch-tvshow-'

        norm_title = scraper_utils.normalize_title(title)
        for item in dom_parser.parse_dom(html, 'div', {'class': 'item movie'}):
            match = re.search('href="(%s[^"]+)' % (query_type), item)
            if match:
                link = match.group(1)
                match_title = self.__make_title(link, query_type)
                match_year = ''
                if norm_title in scraper_utils.normalize_title(match_title) and (not year or not match_year or int(year) == int(match_year)):
                    result = {'url': scraper_utils.pathify_url(link), 'title': match_title, 'year': match_year}
                    results.append(result)

        return results

    def __make_title(self, link, query_type):
        link = link.replace(query_type, '')
        link = re.sub('-\d+\.html', '', link)
        link = link.replace('-', ' ')
        link = capwords(link)
        return link

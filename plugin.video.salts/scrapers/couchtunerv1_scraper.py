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

from salts_lib import dom_parser
from salts_lib import kodi
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://www.couchtuner.ch'
BASE_URL2 = 'http://www.couchtuner.city'

class CouchTunerV1_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'CouchTunerV1'

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
            entry = ''
            while True:
                html = self._http_get(url, cache_limit=.5)
                if not html:
                    url = urlparse.urljoin(BASE_URL2, source_url)
                    html = self._http_get(url, cache_limit=.5)
                entry = dom_parser.parse_dom(html, 'div', {'class': 'entry'})
                if entry:
                    entry = entry[0]
                    match = re.search('Watch it here\s*:.*?href="([^"]+)', entry, re.I)
                    if match:
                        url = match.group(1)
                    else:
                        break
                else:
                    entry = ''
                    break
    
            for tab in dom_parser.parse_dom(entry, 'div', {'class': '''[^'"]*postTabs_divs[^'"]*'''}):
                match = re.search('<iframe[^>]*src="([^"]+)', tab, re.I | re.DOTALL)
                if match:
                    link = match.group(1)
                    host = urlparse.urlparse(link).hostname
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': scraper_utils.get_quality(video, host, QUALITIES.HIGH), 'views': None, 'rating': None, 'url': link, 'direct': False}
                    hosters.append(hoster)

        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+[sS](?:eason-)?%s-[eE](?:pisode-)?%s-[^"]+)' % (video.season, video.episode)
        title_pattern = 'href="(?P<url>[^"]+season-\d+-episode-\d+-[^"]+).*?8211;\s*(?P<title>[^<]+)'
        return self._default_get_episode_url(show_url, video, episode_pattern, title_pattern)

    def search(self, video_type, title, year):
        show_list_url = urlparse.urljoin(self.base_url, '/tv-lists/')
        html = self._http_get(show_list_url, cache_limit=8)
        results = []
        norm_title = scraper_utils.normalize_title(title)
        items = dom_parser.parse_dom(html, 'li')
        for item in items:
            match = re.search('href="([^"]+)">(.*?)</a>', item)
            if match:
                url, match_title = match.groups()
                match_title = match_title.replace('<strong>', '').replace('</strong>', '')
                if norm_title in scraper_utils.normalize_title(match_title):
                    result = {'url': scraper_utils.pathify_url(url), 'title': match_title, 'year': ''}
                    results.append(result)

        return results

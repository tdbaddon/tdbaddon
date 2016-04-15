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
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://dayt.se'

class DayT_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'DayT.se'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        sources = []
        if source_url and source_url != FORCE_NO_MATCH:
            source_url = '/forum' + source_url
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.25)
            iframes = dom_parser.parse_dom(html, 'iframe', ret='src')
            for iframe_url in iframes:
                if 'docs.google.com' in iframe_url:
                    sources = self._parse_google(iframe_url)
                    break
                elif 'banner' in iframe_url or not iframe_url.startswith('http'):
                    pass
                else:
                    html = self._http_get(iframe_url, cache_limit=.25)
                    iframes += dom_parser.parse_dom(html, 'iframe', ret='src')

            for source in sources:
                host = self._get_direct_hostname(source)
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': scraper_utils.gv_get_quality(source), 'views': None, 'rating': None, 'url': source, 'direct': True}
                hosters.append(hoster)
    
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def _get_episode_url(self, show_url, video):
        show_url = '/forum' + show_url
        episode_pattern = 'href="([^"]*[Ss]%02d[Ee]%02d[^"]*)' % (int(video.season), int(video.episode))
        return self._default_get_episode_url(show_url, video, episode_pattern)

    def search(self, video_type, title, year, season=''):
        results = []
        url = urlparse.urljoin(self.base_url, '/forum/forum.php')
        html = self._http_get(url, cache_limit=48)
        norm_title = scraper_utils.normalize_title(title)
        for span in dom_parser.parse_dom(html, 'span', {'class': 'sectiontitle'}):
            match = re.search('href="([^"]+)[^>]+>([^<]+)', span)
            if match:
                url, match_title = match.groups()
                if norm_title in scraper_utils.normalize_title(match_title):
                    result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(match_title), 'year': ''}
                    results.append(result)

        return results

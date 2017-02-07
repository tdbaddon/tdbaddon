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
from salts_lib.constants import QUALITIES
import scraper

BASE_URL = 'http://tvrush.eu'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'tvrush'

    def resolve_link(self, link):
        url = urlparse.urljoin(self.base_url, link)
        html = self._http_get(url, cache_limit=.5)
        stream = dom_parser.parse_dom(html, 'a', {'class': '[^"]*hostLink[^"]*'}, ret='href')
        if stream:
            return stream[0]
        else:
            return link

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.5)
            fragment = dom_parser.parse_dom(html, 'div', {'class': 'embeds'})
            if fragment:
                links = dom_parser.parse_dom(fragment[0], 'a', ret='href')
                hosts = dom_parser.parse_dom(fragment[0], 'div', {'class': 'searchTVname'})
                for stream_url, host in map(None, links, hosts):
                    quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
                    hosters.append(hoster)
    
        return hosters

    def _get_episode_url(self, show_url, video):
        episode_pattern = '''href=['"]([^'"]+season-%s-episode-%s(?!\d)[^'"]*)''' % (video.season, video.episode)
        title_pattern = '''<a\s+title="[^"]+Episode\s+\d+\s*-\s*(?P<title>[^"]+)"\s+href="(?P<url>[^"]+)'''
        airdate_pattern = '''class="episode">\s*<a[^>]+href=['"]([^'"]+)[^>]+>{short_month}\s+{p_day}\s*,\s+{year}'''
        return self._default_get_episode_url(show_url, video, episode_pattern, title_pattern, airdate_pattern)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        if title:
            first_letter = title[:1].upper()
            if first_letter.isdigit(): first_letter = '#'
            search_url = '/series-%s' % (first_letter)
            search_url = urlparse.urljoin(self.base_url, search_url)
            html = self._http_get(search_url, cache_limit=48)
            norm_title = scraper_utils.normalize_title(title)
            for table in dom_parser.parse_dom(html, 'table'):
                for td in dom_parser.parse_dom(table, 'td'):
                    match_url = re.search('href="([^"]+)', td)
                    match_title = dom_parser.parse_dom(td, 'div', {'class': 'searchTVname'})
                    match_year = dom_parser.parse_dom(td, 'span', {'class': 'right'})
                    if match_url and match_title:
                        match_url = match_url.group(1)
                        match_title = match_title[0]
                        match_year = match_year[0] if match_year else ''
                    
                        if norm_title in scraper_utils.normalize_title(match_title) and (not year or not match_year or year == match_year):
                            result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                            results.append(result)

        return results

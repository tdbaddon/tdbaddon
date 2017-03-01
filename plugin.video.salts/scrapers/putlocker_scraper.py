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
from salts_lib import scraper_utils
import dom_parser
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://putlocker9.is'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'Putlocker'

    def resolve_link(self, link):
        if not link.startswith('http'):
            stream_url = urlparse.urljoin(self.base_url, link)
            html = self._http_get(stream_url, cache_limit=0)
            iframe_url = dom_parser.parse_dom(html, 'iframe', ret='src')
            if iframe_url:
                return iframe_url[0]
        else:
            return link
        
    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.5)
            fragment = dom_parser.parse_dom(html, 'div', {'class': 'alternativesc'})
            if fragment:
                for item in dom_parser.parse_dom(fragment[0], 'div', {'class': 'altercolumn'}):
                    link = dom_parser.parse_dom(item, 'a', {'class': 'altercolumnlink'}, ret='href')
                    host = dom_parser.parse_dom(item, 'span')
                    if link and host:
                        link = link[0]
                        if not link.startswith('http'):
                            link = source_url + link
                        host = host[0]
                        quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
                        hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': link, 'direct': False}
                        hosters.append(hoster)

        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        headers = {'Referer': self.base_url}
        params = {'search': title}
        html = self._http_get(self.base_url, params=params, headers=headers, cache_limit=8)
        for item in dom_parser.parse_dom(html, 'div', {'class': 'listCard'}):
            match_title = dom_parser.parse_dom(item, 'p', {'class': 'extraTitle'})
            match_url = dom_parser.parse_dom(item, 'a', ret='href')
            match_year = dom_parser.parse_dom(item, 'p', {'class': 'cardYear'})
            if match_url and match_title:
                match_url = match_url[0]
                match_title = match_title[0]
                match_year = match_year[0] if match_year else ''
                if not year or not match_year or year == match_year:
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)
        return results

    def _get_episode_url(self, show_url, video):
        show_url = urlparse.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, headers={'Referer': self.base_url}, cache_limit=24 * 7)
        match = re.search('href="([^"]*season=0*%s(?!\d))[^"]*' % (video.season), html)
        if match:
            season_url = show_url + match.group(1)
            episode_pattern = 'href="([^"]*/0*%s-0*%s/[^"]*)' % (video.season, video.episode)
            title_pattern = 'class="episodeDetail">.*?href="(?P<url>[^"]+)[^>]*>\s*(?P<title>.*?)\s*</a>'
            headers = {'Referer': show_url}
            return self._default_get_episode_url(season_url, video, episode_pattern, title_pattern, headers=headers)

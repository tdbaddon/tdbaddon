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
import urllib
from salts_lib import dom_parser
from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
import scraper


XHR = {'X-Requested-With': 'XMLHttpRequest'}
BASE_URL = 'http://www.watchepisodes.com'

class WatchEpisodes_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'WatchEpisodes'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        if item['views'] is not None:
            label += ' (%s views)' % (item['views'])
        if item['rating'] is not None:
            label += ' (%s/100)' % (item['rating'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.25)
            for link in dom_parser.parse_dom(html, 'div', {'class': '[^"]*ldr-item[^"]*'}):
                stream_url = dom_parser.parse_dom(link, 'a', ret='data-actuallink')
                
                views = None
                watched = dom_parser.parse_dom(link, 'div', {'class': 'click-count'})
                if watched:
                    match = re.search(' (\d+) ', watched[0])
                    if match:
                        views = match.group(1)
                        
                score = dom_parser.parse_dom(link, 'div', {'class': '\s*point\s*'})
                if score:
                    score = int(score[0])
                    rating = score * 10 if score else None
                
                if stream_url:
                    stream_url = stream_url[0]
                    host = urlparse.urlparse(stream_url).hostname
                    quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': views, 'rating': rating, 'url': stream_url, 'direct': False}
                    hosters.append(hoster)

        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def _get_episode_url(self, show_url, video):
        url = urlparse.urljoin(self.base_url, show_url)
        html = self._http_get(url, cache_limit=2)
        if html:
            force_title = scraper_utils.force_title(video)
            episodes = dom_parser.parse_dom(html, 'div', {'class': '\s*el-item\s*'})
            if not force_title:
                episode_pattern = 'href="([^"]*-[sS]%02d[eE]%02d(?!\d)[^"]*)' % (int(video.season), int(video.episode))
                match = re.search(episode_pattern, html)
                if match:
                    return scraper_utils.pathify_url(match.group(1))
                
                if kodi.get_setting('airdate-fallback') == 'true' and video.ep_airdate:
                    airdate_pattern = '%02d-%02d-%d' % (video.ep_airdate.day, video.ep_airdate.month, video.ep_airdate.year)
                    for episode in episodes:
                        ep_url = dom_parser.parse_dom(episode, 'a', ret='href')
                        ep_airdate = dom_parser.parse_dom(episode, 'div', {'class': 'date'})
                        if ep_url and ep_airdate:
                            ep_airdate = ep_airdate[0].strip()
                            if airdate_pattern == ep_airdate:
                                return scraper_utils.pathify_url(ep_url[0])

            if (force_title or kodi.get_setting('title-fallback') == 'true') and video.ep_title:
                norm_title = scraper_utils.normalize_title(video.ep_title)
                for episode in episodes:
                    ep_url = dom_parser.parse_dom(episode, 'a', ret='href')
                    ep_title = dom_parser.parse_dom(episode, 'div', {'class': 'e-name'})
                    if ep_url and ep_title and norm_title == scraper_utils.normalize_title(ep_title[0]):
                        return scraper_utils.pathify_url(ep_url[0])

    def search(self, video_type, title, year, season=''):
        results = []
        search_url = urlparse.urljoin(self.base_url, '/search/ajax_search?q=')
        search_url += urllib.quote_plus(title)
        html = self._http_get(search_url, headers=XHR, cache_limit=1)
        js_result = scraper_utils.parse_json(html, search_url)
        match_year = ''
        if 'series' in js_result:
            for series in js_result['series']:
                if 'seo' in series and 'label' in series:
                    if not year or not match_year or year == match_year:
                        result = {'url': scraper_utils.pathify_url('/' + series['seo']), 'title': scraper_utils.cleanse_title(series['label']), 'year': match_year}
                        results.append(result)

        return results

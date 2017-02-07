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
import datetime
import kodi
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
from salts_lib.constants import XHR
import scraper

BASE_URL = 'http://www.filmovizija.ws'
EP_URL = '/episode.php?vid=%s'
LINK_URL = '/morgan.php'

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
        return 'Filmovizija'

    def resolve_link(self, link):
        if link.startswith('http'):
            return link
        else:
            link_url = urlparse.urljoin(self.base_url, LINK_URL)
            data = {'redirect': link}
            html = self._http_get(link_url, data=data, headers=XHR)
            if html.startswith('http'):
                return html.strip()
    
    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.5)
            for row in dom_parser.parse_dom(html, 'tr', {'id': 'linktr'}):
                redirect = dom_parser.parse_dom(row, 'span', ret='id')
                link = dom_parser.parse_dom(row, 'a', ret='href')
                if link and link[0].startswith('http'):
                    stream_url = link[0]
                elif redirect:
                    stream_url = redirect[0]
                else:
                    stream_url = ''

                if stream_url.startswith('http'):
                    host = urlparse.urlparse(stream_url).hostname
                else:
                    host = dom_parser.parse_dom(row, 'h9')
                    host = host[0] if host else ''
                    
                if stream_url and host:
                    quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
                    hosters.append(hoster)
            
        return hosters

    def _get_episode_url(self, show_url, video):
        url = urlparse.urljoin(self.base_url, show_url)
        html = self._http_get(url, cache_limit=8)
        pattern = "<a[^>]*class='dropdown-toggle'[^>]*>Season\s+%s<(.*?)<li\s+class='divider'>" % (video.season)
        match = re.search(pattern, html, re.DOTALL)
        if match:
            fragment = match.group(1)
            ep_ids = dom_parser.parse_dom(fragment, 'a', {'id': 'epiloader'}, ret='class')
            episodes = dom_parser.parse_dom(fragment, 'a', {'id': 'epiloader'})
            airdates = dom_parser.parse_dom(fragment, 'span', {'class': 'airdate'})
            ep_airdate = video.ep_airdate.strftime('%Y-%m-%d') if isinstance(video.ep_airdate, datetime.date) else ''
            norm_title = scraper_utils.normalize_title(video.ep_title)
            num_id, airdate_id, title_id = '', '', ''
            for episode, airdate, ep_id in zip(episodes, airdates, ep_ids):
                if ep_airdate and ep_airdate == airdate: airdate_id = ep_id
                match = re.search('(?:<span[^>]*>)?(\d+)\.\s*([^<]+)', episode)
                if match:
                    ep_num, ep_title = match.groups()
                    if int(ep_num) == int(video.episode): num_id = ep_id
                    if norm_title and norm_title in scraper_utils.normalize_title(ep_title): title_id = ep_id

            best_id = ''
            if not scraper_utils.force_title(video):
                if num_id: best_id = num_id
                if kodi.get_setting('airdate-fallback') == 'true' and airdate_id: best_id = airdate_id
                if kodi.get_setting('title-fallback') == 'true' and title_id: best_id = title_id
            else:
                if title_id: best_id = title_id
            
            if best_id:
                return EP_URL % (best_id)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        if video_type == VIDEO_TYPES.MOVIE:
            results = self.__movie_search(title, year)
        else:
            results = self.__tv_search(title, year)
        return results

    def __movie_search(self, title, year):
        results = []
        search_url = urlparse.urljoin(self.base_url, '/search1.php')
        params = {'keywords': title, 'ser': 506}
        html = self._http_get(search_url, params=params, cache_limit=8)
        fragment = dom_parser.parse_dom(html, 'ul', {'class': 'cbp-rfgrid'})
        if fragment:
            for item in dom_parser.parse_dom(fragment[0], 'li'):
                match_url = dom_parser.parse_dom(item, 'a', ret='href')
                match_title_year = ''
                link_frag = dom_parser.parse_dom(item, 'a')
                if link_frag:
                    match_title_year = dom_parser.parse_dom(link_frag[0], 'div')
                    
                if match_url and match_title_year:
                    match_url = match_url[0]
                    match_title, match_year = scraper_utils.extra_year(match_title_year[0])
                    if not year or not match_year or year == match_year:
                        result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                        results.append(result)

        return results
    
    def __tv_search(self, title, year):  # @UnusedVariable
        results = []
        url = urlparse.urljoin(self.base_url, '/tvshows.html')
        html = self._http_get(url, cache_limit=48)
        fragment = dom_parser.parse_dom(html, 'div', {'class': 'series-top'})
        if fragment:
            norm_title = scraper_utils.normalize_title(title)
            for match in re.finditer("href='([^']+)[^>]*>(.*?)</a>", fragment[0]):
                match_url, match_title = match.groups()
                match_year = ''
                if norm_title in scraper_utils.normalize_title(match_title):
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)
        return results

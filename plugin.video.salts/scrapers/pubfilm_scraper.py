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
import urllib
import urlparse

from salts_lib import dom_parser
from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
import scraper

BASE_URL = 'http://pubfilm.com'
GK_URL = 'http://player.pubfilm.com/smplayer/plugins/gkphp/plugins/gkpluginsphp.php'
XHR = {'X-Requested-With': 'XMLHttpRequest'}

class PubFilm_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.SEASON, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'pubfilm'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        if 'views' in item and item['views']:
            label += ' (%s views)' % item['views']
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            
            views = None
            fragment = dom_parser.parse_dom(html, 'span', {'class': 'post-views'})
            if fragment:
                fragment = fragment[0]
                views = re.sub('[^\d]', '', fragment)
            
            iframe_url = ''
            if video.video_type == VIDEO_TYPES.MOVIE:
                iframe_url = dom_parser.parse_dom(html, 'a', {'target': 'EZWebPlayer'}, ret='href')
                if iframe_url:
                    iframe_url = iframe_url[0]
            else:
                for label, link in self.__get_episode_links(html):
                    if int(label) == int(video.episode):
                        iframe_url = link
                        break
                
            if iframe_url:
                headers = {'Referer': iframe_url}
                html = self._http_get(iframe_url, headers=headers, cache_limit=5)
                match = re.search('{link\s*:\s*"([^"]+)', html)
                if match:
                    sources = self.__get_gk_links(match.group(1))
                else:
                    sources = self._parse_sources_list(html)
                    
                for source in sources:
                    stream_url = source + '|User-Agent=%s' % (scraper_utils.get_ua())
                    direct = sources[source]['direct']
                    quality = sources[source]['quality']
                    if sources[source]['direct']:
                        host = self._get_direct_hostname(source)
                    else:
                        host = urlparse.urlparse(source).hostname
                    hoster = {'multi-part': False, 'url': stream_url, 'class': self, 'quality': quality, 'host': host, 'rating': None, 'views': views, 'direct': direct}
                    hosters.append(hoster)

        return hosters

    def __get_gk_links(self, iframe_url):
        sources = {}
        data = {'link': iframe_url}
        headers = {'Referer': iframe_url}
        html = self._http_get(GK_URL, data=data, headers=headers, cache_limit=.5)
        js_data = scraper_utils.parse_json(html, GK_URL)
        if 'link' in js_data:
            if isinstance(js_data['link'], basestring):
                sources[js_data['link']] = {'quality': QUALITIES.HIGH, 'direct': False}
            else:
                for link in js_data['link']:
                    stream_url = link['link']
                    if self._get_direct_hostname(stream_url) == 'gvideo':
                        quality = scraper_utils.gv_get_quality(stream_url)
                    elif 'label' in link:
                        quality = scraper_utils.height_get_quality(link['label'])
                    else:
                        quality = QUALITIES.HIGH
                sources[stream_url] = {'quality': quality, 'direct': True}
        return sources
        
    def get_url(self, video):
        return self._default_get_url(video)

    def _get_episode_url(self, season_url, video):
        url = urlparse.urljoin(self.base_url, season_url)
        html = self._http_get(url, cache_limit=8)
        for label, _links in self.__get_episode_links(html):
            if int(label) == int(video.episode):
                return season_url
    
    def __get_episode_links(self, html):
        links = dom_parser.parse_dom(html, 'a', {'target': 'EZWebPlayer'}, ret='href')
        labels = dom_parser.parse_dom(html, 'input', {'class': '[^"]*abutton[^"]*'}, ret='value')
        labels = [re.sub('[^\d]', '', label) for label in labels]
        return zip(labels, links)
    
    def search(self, video_type, title, year, season=''):
        results = []
        search_url = urlparse.urljoin(self.base_url, '/?s=%s')
        search_url = search_url % (urllib.quote(title))
        html = self._http_get(search_url, cache_limit=1)
        for item in dom_parser.parse_dom(html, 'h3', {'class': 'post-box-title'}):
            match = re.search('href="([^"]+)[^>]*>([^<]+)', item)
            if match:
                match_url, match_title_year = match.groups()
                is_season = re.search('Season\s+(\d+)$', match_title_year, re.I)
                if not is_season and video_type == VIDEO_TYPES.MOVIE or is_season and VIDEO_TYPES.SEASON:
                    match_year = ''
                    if video_type == VIDEO_TYPES.SEASON:
                        match_title = match_title_year
                        if season and int(is_season.group(1)) != int(season):
                            continue
                    else:
                        match = re.search('(.*?)\s+(\d{4})$', match_title_year)
                        if match:
                            match_title, match_year = match.groups()
                        else:
                            match_title = match_title_year
                            match_year = ''
        
                    if not year or not match_year or year == match_year:
                        result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                        results.append(result)
        return results

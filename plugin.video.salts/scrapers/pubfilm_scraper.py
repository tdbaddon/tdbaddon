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
import datetime
import re
import urlparse
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
from salts_lib.constants import USER_AGENT
from salts_lib.constants import XHR
import scraper

BASE_URL = 'http://pubfilm.ac'
GK_URL = 'http://player.pubfilm.ac/smplayer/plugins/gkphp/plugins/gkpluginsphp.php'

class Scraper(scraper.Scraper):
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

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)
        
        views = None
        fragment = dom_parser2.parse_dom(html, 'span', {'class': 'post-views'})
        if fragment:
            views = re.sub('[^\d]', '', fragment[0].content)
        
        iframe_urls = []
        if video.video_type == VIDEO_TYPES.MOVIE:
            iframe_urls = [r.attrs['href'] for r in dom_parser2.parse_dom(html, 'a', {'class': ['orange', 'abutton']}, req='href')]
        else:
            for label, link in self.__get_episode_links(html):
                if int(label) == int(video.episode):
                    iframe_urls.append(link)
            
        for iframe_url in iframe_urls:
            headers = {'Referer': url}
            html = self._http_get(iframe_url, headers=headers, cache_limit=.5)
            match = re.search('{link\s*:\s*"([^"]+)', html)
            if match:
                sources = self.__get_gk_links(match.group(1), iframe_url)
            else:
                sources = scraper_utils.parse_sources_list(self, html)
                
            for source in sources:
                stream_url = source + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
                direct = sources[source]['direct']
                quality = sources[source]['quality']
                if sources[source]['direct']:
                    host = scraper_utils.get_direct_hostname(self, source)
                else:
                    host = urlparse.urlparse(source).hostname
                hoster = {'multi-part': False, 'url': stream_url, 'class': self, 'quality': quality, 'host': host, 'rating': None, 'views': views, 'direct': direct}
                hosters.append(hoster)

        return hosters

    def __get_gk_links(self, link, iframe_url):
        sources = {}
        data = {'link': link}
        headers = XHR
        headers.update({'Referer': iframe_url, 'User-Agent': USER_AGENT})
        html = self._http_get(GK_URL, data=data, headers=headers, cache_limit=.25)
        js_data = scraper_utils.parse_json(html, GK_URL)
        if 'link' in js_data:
            if isinstance(js_data['link'], basestring):
                stream_url = js_data['link']
                if scraper_utils.get_direct_hostname(self, stream_url) == 'gvideo':
                    for source in scraper_utils.parse_google(self, stream_url):
                        sources[source] = {'quality': scraper_utils.gv_get_quality(source), 'direct': True}
                else:
                    sources[stream_url] = {'quality': QUALITIES.HIGH, 'direct': False}
            else:
                for link in js_data['link']:
                    stream_url = link['link']
                    if scraper_utils.get_direct_hostname(self, stream_url) == 'gvideo':
                        quality = scraper_utils.gv_get_quality(stream_url)
                    elif 'label' in link:
                        quality = scraper_utils.height_get_quality(link['label'])
                    else:
                        quality = QUALITIES.HIGH
                    sources[stream_url] = {'quality': quality, 'direct': True}
        return sources
        
    def _get_episode_url(self, season_url, video):
        url = scraper_utils.urljoin(self.base_url, season_url)
        html = self._http_get(url, cache_limit=2)
        for label, _links in self.__get_episode_links(html):
            if int(label) == int(video.episode):
                return season_url
    
    def __get_episode_links(self, html):
        episodes = [(re.sub('[^\d]', '', label), attrs['href']) for attrs, label in dom_parser2.parse_dom(html, 'a', {'class': ['orange', 'abutton']}, req='href')]
        return [episode for episode in episodes if episode[0].isdigit()]
    
    def search(self, video_type, title, year, season=''):
        results = []
        headers = {'Referer': self.base_url}
        html = self._http_get(self.base_url, params={'s': title}, headers=headers, cache_limit=8)
        log_utils.log(html)
        norm_title = scraper_utils.normalize_title(title)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'recent-item'}):
            fragment = dom_parser2.parse_dom(item, 'h\d+')
            if not fragment: continue
            
            match = dom_parser2.parse_dom(fragment[0].content, 'a', {'rel': 'bookmark'}, req='href')
            if match:
                match_title_year = match[0].content
                match_url = match[0].attrs['href']
                match_title_year = re.sub('</?[^>]*>', '', match_title_year)
                is_season = re.search('Season\s+(\d+)\s*', match_title_year, re.I)
                if (not is_season and video_type == VIDEO_TYPES.MOVIE) or (is_season and video_type == VIDEO_TYPES.SEASON):
                    match_year = ''
                    if video_type == VIDEO_TYPES.SEASON:
                        match_title = match_title_year
                        if season and int(is_season.group(1)) != int(season):
                            continue
                    else:
                        match_title, match_year = scraper_utils.extra_year(match_title_year)

                    match_norm_title = scraper_utils.normalize_title(match_title)
                    title_match = (norm_title in match_norm_title) or (match_norm_title in norm_title)
                    if title_match and (not year or not match_year or year == match_year):
                        result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                        results.append(result)
        return results

    def __cache_header(self, max_age):
        return (datetime.datetime.utcnow() - datetime.timedelta(hours=float(max_age))).strftime('%a, %d %b %Y %H:%M:%S GMT')
        
    def _http_get(self, url, params=None, data=None, multipart_data=None, headers=None, cookies=None, allow_redirect=True, method=None, require_debrid=False, read_error=False, cache_limit=8):
        if headers is None: headers = {}
        headers.update({'If-Modified-Since': self.__cache_header(cache_limit)})
        return scraper.Scraper._http_get(self, url, params=params, data=data, multipart_data=multipart_data, headers=headers, cookies=cookies, allow_redirect=allow_redirect, method=method, require_debrid=require_debrid, read_error=read_error, cache_limit=cache_limit)
    
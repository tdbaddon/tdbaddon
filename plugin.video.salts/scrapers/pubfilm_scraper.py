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
import kodi
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
from salts_lib.constants import USER_AGENT
import scraper

GK_URL = 'http://player.pubfilm.com/smplayer/plugins/gkphp/plugins/gkpluginsphp.php'
XHR = {'X-Requested-With': 'XMLHttpRequest'}

class Scraper(scraper.Scraper):
    OPTIONS = ['http://pubfilm.com', 'http://pidtv.com']
    
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
            
            iframe_urls = []
            if video.video_type == VIDEO_TYPES.MOVIE:
                iframe_urls = dom_parser.parse_dom(html, 'a', {'target': 'EZWebPlayer'}, ret='href')
            else:
                for label, link in self.__get_episode_links(html):
                    if int(label) == int(video.episode):
                        iframe_urls.append(link)
                
            for iframe_url in iframe_urls:
                headers = {'Referer': iframe_url}
                html = self._http_get(iframe_url, headers=headers, cache_limit=.5)
                match = re.search('{link\s*:\s*"([^"]+)', html)
                if match:
                    sources = self.__get_gk_links(match.group(1), iframe_url)
                else:
                    sources = self._parse_sources_list(html)
                    
                for source in sources:
                    stream_url = source + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
                    direct = sources[source]['direct']
                    quality = sources[source]['quality']
                    if sources[source]['direct']:
                        host = self._get_direct_hostname(source)
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
                if self._get_direct_hostname(stream_url) == 'gvideo':
                    temp = self._parse_google(stream_url)
                    for source in temp:
                        sources[source] = {'quality': scraper_utils.gv_get_quality(source), 'direct': True}
                else:
                    sources[stream_url] = {'quality': QUALITIES.HIGH, 'direct': False}
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
        
    def _get_episode_url(self, season_url, video):
        url = urlparse.urljoin(self.base_url, season_url)
        html = self._http_get(url, cache_limit=8)
        for label, _links in self.__get_episode_links(html):
            if int(label) == int(video.episode):
                return season_url
    
    def __get_episode_links(self, html):
        links = dom_parser.parse_dom(html, 'a', {'target': 'EZWebPlayer'}, ret='href')
        labels = dom_parser.parse_dom(html, 'a', {'target': 'EZWebPlayer'})
        labels = [re.sub('[^\d]', '', label) for label in labels]
        episodes = [(label, link) for label, link in zip(labels, links) if label.isdigit()]
        return episodes
    
    def search(self, video_type, title, year, season=''):
        results = []
        search_url = urlparse.urljoin(self.base_url, '/search/%s' % (urllib.quote(title)))
        headers = {'Referer': self.base_url}
        html = self._http_get(search_url, headers=headers, cache_limit=8)
        norm_title = scraper_utils.normalize_title(title)
        for item in dom_parser.parse_dom(html, 'div', {'class': 'recent-item'}):
            fragment = dom_parser.parse_dom(item, 'h\d+')
            if not fragment: continue
            
            match_title_year = dom_parser.parse_dom(fragment[0], 'a', {'rel': 'bookmark'})
            match_url = dom_parser.parse_dom(fragment[0], 'a', {'rel': 'bookmark'}, ret='href')
            if match_title_year and match_url:
                match_title_year = match_title_year[0]
                match_url = match_url[0]
                match_title_year = re.sub('</?span[^>]*>', '', match_title_year)
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
                        if (norm_title not in match_norm_title) and (match_norm_title not in norm_title): continue
        
                    if not year or not match_year or year == match_year:
                        result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                        results.append(result)
        return results

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        settings.append('         <setting id="%s-default_url" type="text" visible="false"/>' % (cls.get_name()))
        return settings

scraper_utils.set_default_url(Scraper)

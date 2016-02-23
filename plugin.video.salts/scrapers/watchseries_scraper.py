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
import base64
import hashlib
import re
import urllib
import urlparse

from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://watchseries.ag'
REAL_URL = base64.decodestring('aHR0cDovL3dzLm1n')
WS_USER_AGENT = base64.decodestring('V1MgTW9iaWxl')
HASH_PART1 = base64.decodestring('MzI4aiVHdVMq')
HASH_PART2 = base64.decodestring('ZkEyNDMxNDJmbyMyMyU=')

class WS_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'WatchSeries'

    def resolve_link(self, link):
        return link
    
    def format_source_label(self, item):
        return '[%s] %s' % (item['quality'], item['host'])

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            html = self._http_get(source_url, cache_limit=.5)
            js_result = scraper_utils.parse_json(html, source_url)
            if 'results' in js_result and '0' in js_result['results'] and 'links' in js_result['results']['0']:
                for link in js_result['results']['0']['links']:
                    if 'lang' not in link or link['lang'].lower() == 'english':
                        host = urlparse.urlparse(link['url']).hostname
                        hoster = {'multi-part': False, 'url': link['url'], 'class': self, 'quality': scraper_utils.get_quality(video, host, QUALITIES.HIGH), 'host': host, 'rating': None, 'views': None, 'direct': False}
                        hosters.append(hoster)
            
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year):
        results = []
        search_url = '/search/%s/page/1' % (urllib.quote_plus(title))
        html = self._http_get(search_url, cache_limit=.25)
        js_result = scraper_utils.parse_json(html, search_url)
        if 'results' in js_result:
            matches = [item[1] for item in sorted(js_result['results'].items(), key=lambda x:x[0])]
            for match in matches:
                url, match_title, match_year = match['href'], match['name'], match['year']
                if not year or not match_year or year == match_year:
                    url = scraper_utils.pathify_url(url)
                    url = url.replace('/json', '')
                    result = {'url': url, 'title': match_title, 'year': match_year}
                    results.append(result)
        return results

    def _get_episode_url(self, show_url, video):
        log_utils.log('WS Episode Url: |%s|%s|' % (show_url, str(video).decode('utf-8', 'replace')), log_utils.LOGDEBUG)
        html = self._http_get(show_url, cache_limit=2)
        js_result = scraper_utils.parse_json(html, show_url)
        if 'results' in js_result and '0' in js_result['results'] and 'episodes' in js_result['results']['0']:
            seasons = js_result['results']['0']['episodes']
            force_title = scraper_utils.force_title(video)
            if not force_title:
                if str(video.season) in seasons:
                    season = seasons[str(video.season)]
                    if isinstance(season, list):
                        season = dict((ep['episode'], ep) for ep in season)
        
                    if str(video.episode) in season:
                        url = season[str(video.episode)]['url']
                        return scraper_utils.pathify_url(url.replace('/json', ''))
        
                if kodi.get_setting('airdate-fallback') == 'true' and video.ep_airdate:
                    airdate_pattern = video.ep_airdate.strftime('%d/%M/%Y')
                    for season in seasons:
                        if season.lower() == 'epcount': continue
                        episodes = seasons[season]
                        if isinstance(episodes, dict):
                            episodes = [episodes[key] for key in episodes]
                        for episode in episodes:
                            if airdate_pattern == episode['release']:
                                url = episode['url']
                                return scraper_utils.pathify_url(url.replace('/json', ''))
            else:
                log_utils.log('Skipping S&E matching as title search is forced on: %s' % (video.trakt_id), log_utils.LOGDEBUG)
        
            if (force_title or kodi.get_setting('title-fallback') == 'true') and video.ep_title:
                norm_title = scraper_utils.normalize_title(video.ep_title)
                for season in seasons:
                    if season.lower() == 'epcount': continue
                    episodes = seasons[season]
                    if isinstance(episodes, dict):
                        episodes = [episodes[key] for key in episodes]
                    for episode in episodes:
                        if episode['name'] is not None and norm_title == scraper_utils.normalize_title(episode['name']):
                            url = episode['url']
                            return scraper_utils.pathify_url(url.replace('/json', ''))

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        settings = scraper_utils.disable_sub_check(settings)
        return settings
    
    def _http_get(self, url, cache_limit=8):
        url = self.__translate_url(url)
        headers = {'User-Agent': WS_USER_AGENT}
        result = super(self.__class__, self)._http_get(url, headers=headers, cache_limit=cache_limit)
        result = re.sub('<script.*?</script>', '', result)
        return result
    
    def __translate_url(self, url):
        if not url.startswith('/json'):
            url = '/json' + url
        
        url_hash = hashlib.md5(HASH_PART1 + url + HASH_PART2).hexdigest()
        url = '/' + url_hash + url
        return urlparse.urljoin(REAL_URL, url)

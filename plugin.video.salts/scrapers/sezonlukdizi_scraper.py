# -*- coding: utf-8 -*-
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
import random
import re
import urllib
import urllib2
import urlparse

from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib import dom_parser
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://sezonlukdizi.com'
SEARCH_URL = '/diziler.asp?adi='
SEASON_URL = '/ajax/dataDizi.asp'
GET_VIDEO_URL = '/service/get_video_part'

class SezonLukDizi_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'SezonLukDizi'

    def resolve_link(self, link):
        if 'v.asp' in link:
            try:
                headers = dict([item.split('=') for item in (link.split('|')[1]).split('&')])
                for key in headers: headers[key] = urllib.unquote(headers[key])
            except:
                headers = {}
            request = urllib2.Request(link.split('|')[0], headers=headers)
            response = urllib2.urlopen(request)
            return response.geturl()
        else:
            return link
            
    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        if 'subs' in item and item['subs']:
            label += ' (Turkish subtitles)'
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=2)
            fragment = dom_parser.parse_dom(html, 'div', {'id': 'embed'})
            if fragment:
                    iframe_url = dom_parser.parse_dom(fragment[0], 'iframe', ret='src')
                    if iframe_url:
                        html = self._http_get(iframe_url[0], cache_limit=.25)
                        seen_urls = {}
                        # if captions exist, then they aren't hardcoded
                        if re.search('kind\s*:\s*"captions"', html):
                            subs = False
                        else:
                            subs = True
                            
                        for match in re.finditer('"?file"?\s*:\s*"([^"]+)"\s*,\s*"?label"?\s*:\s*"(\d+)p?[^"]*"', html):
                            stream_url, height = match.groups()
                            if stream_url not in seen_urls:
                                seen_urls[stream_url] = True
                                if 'v.asp' in stream_url:
                                    stream_redirect = self._http_get(stream_url, allow_redirect=False, cache_limit=0)
                                    if stream_redirect: stream_url = stream_redirect
                                    
                                stream_url += '|User-Agent=%s' % (scraper_utils.get_ua())
                                host = self._get_direct_hostname(stream_url)
                                if host == 'gvideo':
                                    quality = scraper_utils.gv_get_quality(stream_url)
                                else:
                                    quality = scraper_utils.height_get_quality(height)
                                hoster = {'multi-part': False, 'host': self._get_direct_hostname(stream_url), 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True, 'subs': subs}
                                
                                hosters.append(hoster)
        return hosters
    
    def get_url(self, video):
        return self._default_get_url(video)

    def _get_episode_url(self, show_url, video):
        url = urlparse.urljoin(self.base_url, show_url)
        html = self._http_get(url, cache_limit=1)
        data_id = dom_parser.parse_dom(html, 'div', {'id': 'dizidetay'}, ret='data-id')
        data_dizi = dom_parser.parse_dom(html, 'div', {'id': 'dizidetay'}, ret='data-dizi')
        if data_id and data_dizi:
            queries = {'sekme': 'bolumler', 'id': data_id[0], 'dizi': data_dizi[0]}
            season_url = SEASON_URL + '?' + urllib.urlencode(queries)
            episode_pattern = '''href=['"]([^'"]*/%s-sezon-%s-[^'"]*bolum[^'"]*)''' % (video.season, video.episode)
            title_pattern = '''href=['"](?P<url>[^'"]+)[^>]*>(?P<title>[^<]+)'''
            airdate_pattern = '''href=['"]([^"']+)[^>]*>[^<]*</a>\s*</td>\s*<td class="right aligned">{p_day}\.{p_month}\.{year}'''
            result = self._default_get_episode_url(season_url, video, episode_pattern, title_pattern, airdate_pattern)
            if result and 'javascript:;' not in result:
                return result

    def search(self, video_type, title, year):
        results = []
        search_url = urlparse.urljoin(self.base_url, SEARCH_URL)
        search_url += urllib.quote_plus(title)
        html = self._http_get(search_url, cache_limit=8)
        fragment = dom_parser.parse_dom(html, 'div', {'class': '[^"]*items[^"]*'})
        if fragment:
            for item in dom_parser.parse_dom(fragment[0], 'div', {'class': 'item'}):
                match_url = dom_parser.parse_dom(item, 'a', {'class': 'header'}, ret='href')
                match_title_year = dom_parser.parse_dom(item, 'a', {'class': 'header'})
                if match_url and match_title_year:
                    match_url = match_url[0]
                    match_title_year = match_title_year[0]
                    r = re.search('(.*?)\s+\((\d{4})\)', match_title_year)
                    if r:
                        match_title, match_year = r.groups()
                    else:
                        match_title = match_title_year
                        match_year = ''
                    
                    if not year or not match_year or year == match_year:
                        result = {'url': scraper_utils.pathify_url(match_url), 'title': match_title, 'year': match_year}
                        results.append(result)

        return results

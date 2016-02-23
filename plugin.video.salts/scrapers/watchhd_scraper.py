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
import re
import urllib
import urlparse

import xbmcgui

from salts_lib import dom_parser
from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import Q_ORDER
from salts_lib.constants import VIDEO_TYPES
from salts_lib.utils2 import i18n
import scraper


BASE_URL = 'http://watch1080p.com'

class WatchHD_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.auto_pick = kodi.get_setting('%s-auto_pick' % (self.get_name())) == 'true'

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'WatchHD'

    def resolve_link(self, link):
        try:
            headers = dict([item.split('=') for item in (link.split('|')[1]).split('&')])
            for key in headers: headers[key] = urllib.unquote(headers[key])
            link = link.split('|')[0]
        except:
            headers = {}

        html = self._http_get(link, headers=headers, cache_limit=.5)
        fragment = dom_parser.parse_dom(html, 'div', {'class': 'player'})
        if fragment:
            iframe_url = dom_parser.parse_dom(fragment[0], 'iframe', ret='src')
            if iframe_url:
                headers = {'Referer': link}
                html = self._http_get(iframe_url[0], headers=headers, cache_limit=.5)
                match = re.search("window\.atob\('([^']+)", html)
                if match:
                    func_count = len(re.findall('window\.atob', html))
                    html = match.group(1)
                    for _i in xrange(func_count):
                        html = base64.decodestring(html)
                
                streams = []
                for match in re.finditer('''<source[^>]+src=["']([^'"]+)[^>]+label=['"]([^'"]+)''', html):
                    streams.append(match.groups())
                
                if len(streams) > 1:
                    if not self.auto_pick:
                        result = xbmcgui.Dialog().select(i18n('choose_stream'), [e[1] for e in streams])
                        if result > -1:
                            return streams[result][0]
                    else:
                        best_stream = ''
                        best_q = 0
                        for stream in streams:
                            stream_url, label = stream
                            if Q_ORDER[scraper_utils.height_get_quality(label)] > best_q:
                                best_q = Q_ORDER[scraper_utils.height_get_quality(label)]
                                best_stream = stream_url
                        
                        if best_stream:
                            return best_stream
                elif streams:
                    return streams[0][0]

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        if 'title' in item:
            label += ' (%s)' % (item['title'])
        if 'views' in item and item['views']:
            label += ' (%s views)' % item['views']
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            match = re.search('<b>Views:.*?([\d,]+)', html)
            if match:
                views = int(match.group(1).replace(',', ''))
            else:
                views = None
            button = dom_parser.parse_dom(html, 'a', {'class': '[^"]*btn_watch_detail[^"]*'}, ret='href')
            if button:
                html = self._http_get(button[0], cache_limit=.5)
                for match in re.finditer('<span class="svname">\s*(.*?)\s*:?\s*</span>(.*?)(?=<span class="svname">|</div>)', html):
                    title, fragment = match.groups()
                    for match in re.finditer('<a[^>]+id="ep_\d+"[^>]+href="([^"]+)[^>]+>\s*([^<]+)', fragment):
                        stream_url, name = match.groups()
                        match = re.search('(\d+)', name)
                        if match:
                            quality = scraper_utils.height_get_quality(match.group(1))
                        else:
                            quality = QUALITIES.HIGH
                        stream_url += '|User-Agent=%s&Referer=%s&Cookie=%s' % (scraper_utils.get_ua(), url, self._get_stream_cookies())
                        hoster = {'multi-part': False, 'host': self._get_direct_hostname(stream_url), 'class': self, 'quality': quality, 'views': views, 'rating': None, 'url': stream_url, 'direct': True}
                        hoster['title'] = title
                        hosters.append(hoster)
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year):
        search_url = urlparse.urljoin(self.base_url, '/search/%s' % (urllib.quote_plus(title)))
        html = self._http_get(search_url, cache_limit=.25)
        results = []
        for item in dom_parser.parse_dom(html, 'div', {'class': 'name_top'}):
            match = re.search('href="([^"]+)[^>]+>([^<]+)', item)
            if match:
                url, match_title_year = match.groups()
                if re.search('Season\s+\d+', match_title_year, re.IGNORECASE): continue
                match = re.search('(.*?)(?:\s+\(?(\d{4})\)?)', match_title_year)
                if match:
                    match_title, match_year = match.groups()
                else:
                    match_title = match_title_year
                    match_year = ''
                
                if not year or not match_year or year == match_year:
                    result = {'title': match_title, 'year': match_year, 'url': scraper_utils.pathify_url(url)}
                    results.append(result)

        return results

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        name = cls.get_name()
        settings.append('         <setting id="%s-auto_pick" type="bool" label="    %s" default="false" visible="eq(-4,true)"/>' % (name, i18n('auto_pick')))
        return settings

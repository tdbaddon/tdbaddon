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
import scraper


BASE_URL = 'http://movie.pubfilmno1.com'
GK_URL = 'http://player.pubfilm.com/smplayer/plugins/gkphp/plugins/gkpluginsphp.php'
XHR = {'X-Requested-With': 'XMLHttpRequest'}

class PubFilm_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

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
                
            iframe_items = set(dom_parser.parse_dom(html, 'iframe', ret='src'))
            link_items = set(dom_parser.parse_dom(html, 'a', {'target': 'EZWebPlayer'}, ret='href'))
            items = list(iframe_items | link_items)
            for item in items:
                if item:
                    links = self.__get_links(item)
                    for link in links:
                        hoster = {'multi-part': False, 'url': link, 'class': self, 'quality': scraper_utils.height_get_quality(links[link]), 'host': self._get_direct_hostname(link), 'rating': None, 'views': views, 'direct': True}
                        hosters.append(hoster)

        return hosters

    def __get_links(self, url):
        links = {}
        url = url.replace('&#038;', '&')
        html = self._http_get(url, cache_limit=.5)
        if 'gkpluginsphp' in html:
            match = re.search('link\s*:\s*"([^"]+)', html)
            if match:
                data = {'link': match.group(1)}
                headers = XHR
                headers['Referer'] = url
                html = self._http_get(GK_URL, data=data, headers=headers, cache_limit=.25)
                js_result = scraper_utils.parse_json(html, GK_URL)
                if 'link' in js_result:
                    for link in js_result['link']:
                        links[link['link']] = link['label']
                
        return links

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year):
        search_url = urlparse.urljoin(self.base_url, '/feeds/posts/summary?alt=json&q=%s&max-results=9999&callback=showResult')
        search_url = search_url % (urllib.quote(title))
        html = self._http_get(search_url, cache_limit=0)
        results = []
        match = re.search('showResult\((.*)\)', html)
        if match:
            js_data = scraper_utils.parse_json(match.group(1), search_url)
            if 'feed' in js_data and 'entry' in js_data['feed']:
                for entry in js_data['feed']['entry']:
                    for category in entry['category']:
                        if category['term'].upper() == 'MOVIES':
                            break
                    else:
                        # if no movies category found, skip entry
                        continue
                    
                    for link in entry['link']:
                        if link['rel'] == 'alternate' and link['type'] == 'text/html':
                            match = re.search('(.*?)\s*(\d{4})\s*-\s*', link['title'])
                            if match:
                                match_title, match_year = match.groups()
                            else:
                                match_title = link['title']
                                match_year = ''
                            
                            if not year or not match_year or year == match_year:
                                result = {'url': scraper_utils.pathify_url(link['href']), 'title': match_title, 'year': match_year}
                                results.append(result)
        return results

    def _http_get(self, url, data=None, headers=None, cache_limit=8):
        html = self._cached_http_get(url, self.base_url, self.timeout, data=data, cache_limit=cache_limit)
        cookie = scraper_utils.get_sucuri_cookie(html)
        if cookie:
            log_utils.log('Setting Pubfilm cookie: %s' % (cookie), log_utils.LOGDEBUG)
            html = self._cached_http_get(url, self.base_url, self.timeout, cookies=cookie, data=data, headers=headers, cache_limit=0)
        return html

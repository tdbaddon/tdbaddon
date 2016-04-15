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
import HTMLParser
import random
import re
import string
import urllib
import urlparse

from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


QUALITY_MAP = {'HD 720P': QUALITIES.HD720, 'HD 720P+': QUALITIES.HD720, 'DVDRIP / STANDARD DEF': QUALITIES.HIGH, 'DVD SCREENER': QUALITIES.HIGH}
BASE_URL = 'http://www.icefilms.info'
LIST_URL = BASE_URL + '/membersonly/components/com_iceplayer/video.php?h=374&w=631&vid=%s&img='
AJAX_URL = '/membersonly/components/com_iceplayer/video.phpAjaxResp.php?id=%s&s=%s&iqs=&url=&m=%s&cap= &sec=%s&t=%s'

class IceFilms_Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'IceFilms'

    def resolve_link(self, link):
        url, query = link.split('?', 1)
        data = urlparse.parse_qs(query, True)
        url = urlparse.urljoin(self.base_url, url)
        url += '?s=%s&t=%s&app_id=SALTS' % (data['id'][0], data['t'][0])
        list_url = LIST_URL % (data['t'][0])
        headers = {'Referer': list_url}
        html = self._http_get(url, data=data, headers=headers, cache_limit=.25)
        match = re.search('url=(.*)', html)
        if match:
            url = urllib.unquote_plus(match.group(1))
            return url

    def format_source_label(self, item):
        label = '[%s] %s%s' % (item['quality'], item['label'], item['host'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        sources = []
        if source_url and source_url != FORCE_NO_MATCH:
            try:
                url = urlparse.urljoin(self.base_url, source_url)
                html = self._http_get(url, cache_limit=.5)

                pattern = '<iframe id="videoframe" src="([^"]+)'
                match = re.search(pattern, html)
                frame_url = match.group(1)
                url = urlparse.urljoin(self.base_url, frame_url)
                html = self._http_get(url, cache_limit=.1)

                match = re.search('lastChild\.value="([^"]+)"(?:\s*\+\s*"([^"]+))?', html)
                secret = ''.join(match.groups(''))

                match = re.search('"&t=([^"]+)', html)
                t = match.group(1)
                
                match = re.search('(?:\s+|,)s\s*=(\d+)', html)
                s_start = int(match.group(1))
                
                match = re.search('(?:\s+|,)m\s*=(\d+)', html)
                m_start = int(match.group(1))
                
                pattern = '<div class=ripdiv>(.*?)</div>'
                for container in re.finditer(pattern, html):
                    fragment = container.group(0)
                    match = re.match('<div class=ripdiv><b>(.*?)</b>', fragment)
                    if match:
                        quality = QUALITY_MAP.get(match.group(1).upper(), QUALITIES.HIGH)
                    else:
                        quality = None

                    pattern = '''onclick='go\((\d+)\)'>([^<]+)(<span.*?)</a>'''
                    for match in re.finditer(pattern, fragment):
                        link_id, label, host_fragment = match.groups()
                        source = {'multi-part': False, 'quality': quality, 'class': self, 'label': label, 'rating': None, 'views': None, 'direct': False}
                        source['host'] = re.sub('(<[^>]+>|</span>)', '', host_fragment)
                        s = s_start + random.randint(3, 1000)
                        m = m_start + random.randint(21, 1000)
                        url = AJAX_URL % (link_id, s, m, secret, t)
                        source['url'] = url
                        sources.append(source)
            except Exception as e:
                log_utils.log('Failure (%s) during icefilms get sources: |%s|' % (str(e), video), log_utils.LOGWARNING)
        return sources

    def get_url(self, video):
        return self._default_get_url(video)

    def search(self, video_type, title, year, season=''):
        if video_type == VIDEO_TYPES.MOVIE:
            url = urlparse.urljoin(self.base_url, '/movies/a-z/')
        else:
            url = urlparse.urljoin(self.base_url, '/tv/a-z/')

        if title.upper().startswith('THE '):
            first_letter = title[4:5]
        elif title.upper().startswith('A '):
            first_letter = title[2:3]
        elif title[:1] in string.digits:
            first_letter = '1'
        else:
            first_letter = title[:1]
        url = url + first_letter.upper()
        
        html = self._http_get(url, cache_limit=.25)
        h = HTMLParser.HTMLParser()
        html = unicode(html, 'windows-1252')
        html = h.unescape(html)
        norm_title = scraper_utils.normalize_title(title)
        pattern = 'class=star.*?href=([^>]+)>(.*?)(?:\s*\((\d+)\))?</a>'
        results = []
        for match in re.finditer(pattern, html, re.DOTALL):
            url, match_title, match_year = match.groups('')
            if norm_title in scraper_utils.normalize_title(match_title) and (not year or not match_year or year == match_year):
                result = {'url': url, 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                results.append(result)
        return results

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href=(/ip\.php[^>]+)>%sx0?%s\s+' % (video.season, video.episode)
        title_pattern = 'class=star>\s*<a href=(?P<url>[^>]+)>(?:\d+x\d+\s+)+(?P<title>[^<]+)'
        return self._default_get_episode_url(show_url, video, episode_pattern, title_pattern)

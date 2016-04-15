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
import xbmcgui
from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib import dom_parser
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
from salts_lib.kodi import i18n
import scraper

BASE_URL = 'premiumize.me'
CHECKHASH_URL = '/api/torrent/checkhashes?'
ADD_URL = '/api/transfer/create?type=torrent'
BROWSE_URL = '/api/torrent/browse?hash=%s'
LIST_URL = '/api/transfer/list'

BASE_UR2 = 'https://yts.ag'
MOVIE_SEARCH_URL = '/api/v2/list_movies.json?query_term=%s&sort_by=seeders&order_by=desc'
MOVIE_DETAILS_URL = '/api/v2/movie_details.json?movie_id=%s'

BASE_URL3 = 'https://eztv.ag'

MAGNET_LINK = 'magnet:?xt=urn:btih:%s'
VIDEO_EXT = ['MKV', 'AVI', 'MP4']
QUALITY_MAP = {'1080p': QUALITIES.HD1080, '720p': QUALITIES.HD720, '3D': QUALITIES.HD1080}

class Premiumize_Scraper(scraper.Scraper):
    base_url = BASE_URL
    movie_base_url = BASE_UR2
    tv_base_url = BASE_URL3

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        if kodi.get_setting('%s-use_https' % (self.get_name())) == 'true':
            scheme = 'https'
            prefix = 'www'
        else:
            scheme = 'http'
            prefix = 'http'
        base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.base_url = scheme + '://' + prefix + '.' + base_url
        self.movie_base_url = kodi.get_setting('%s-base_url2' % (self.get_name()))
        self.tv_base_url = kodi.get_setting('%s-base_url3' % (self.get_name()))
        self.username = kodi.get_setting('%s-username' % (self.get_name()))
        self.password = kodi.get_setting('%s-password' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'Premiumize.me'

    def resolve_link(self, link):
        query = urlparse.parse_qs(link)
        if 'hash_id' in query:
            hash_id = query['hash_id'][0].lower()
            if self.__add_torrent(hash_id):
                browse_url = BROWSE_URL % (hash_id)
                browse_url = urlparse.urljoin(self.base_url, browse_url)
                js_data = self._json_get(browse_url, cache_limit=0)
                if 'content' in js_data:
                    videos = self.__get_videos(js_data['content'])
                    
                    if len(videos) > 1:
                        result = xbmcgui.Dialog().select(i18n('choose_stream'), [video['label'] for video in videos])
                        if result > -1:
                            return videos[result]['url']
                    elif videos:
                        return videos[0]['url']
                
    def __add_torrent(self, hash_id):
        list_url = urlparse.urljoin(self.base_url, LIST_URL)
        js_data = self._json_get(list_url, cache_limit=0)
        if 'transfers' in js_data:
            for transfer in js_data['transfers']:
                if transfer['hash'].lower() == hash_id:
                    return True
         
        add_url = urlparse.urljoin(self.base_url, ADD_URL)
        data = {'src': MAGNET_LINK % hash_id}
        js_data = self._json_get(add_url, data=data, cache_limit=0)
        if 'status' in js_data and js_data['status'] == 'success':
            return True
        else:
            return False
    
    def __get_videos(self, content):
        videos = []
        for key in content:
            item = content[key]
            if item['type'].lower() == 'dir':
                videos += self.__get_videos(item['children'])
            else:
                if item['ext'].upper() in VIDEO_EXT:
                    label = '(%s) %s' % (scraper_utils.format_size(item['size'], 'B'), item['name'])
                    video = {'label': label, 'url': item['url']}
                    videos.append(video)
                    if 'transcoded' in item and item['transcoded']:
                        transcode = item['transcoded']
                        if 'size' in transcode:
                            label = '(%s) (Transcode) %s' % (scraper_utils.format_size(transcode['size'], 'B'), item['name'])
                        else:
                            label = '(Transcode) %s' % (item['name'])
                        video = {'label': label, 'url': transcode['url']}
                        videos.append(video)
        return videos

    def format_source_label(self, item):
        label = '[%s] %s' % (item['quality'], item['host'])
        if '3D' in item and item['3D']:
            label += ' (3D)'
        if 'size' in item:
            label += ' (%s)' % (item['size'])
        if 'extra' in item:
            label += ' [%s]' % (item['extra'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        if source_url and source_url != FORCE_NO_MATCH:
            if video.video_type == VIDEO_TYPES.MOVIE:
                return self.__get_movie_sources(source_url)
            else:
                return self.__get_episode_sources(source_url, video)
    
    def __get_episode_sources(self, source_url, video):
        hosters = []
        links = self.__find_episode(source_url, video)
        if links:
            hash_data = self.__get_hash_data([link[0] for link in links])
            for link in links:
                try: status = hash_data['hashes'][link[0]]['status']
                except KeyError: status = ''
                if status.lower() == 'finished':
                    stream_url = 'hash_id=%s' % (link[0])
                    host = self._get_direct_hostname(stream_url)
                    quality = scraper_utils.blog_get_quality(video, link[1], '')
                    hoster = {'multi-part': False, 'class': self, 'views': None, 'url': stream_url, 'rating': None, 'host': host, 'quality': quality, 'direct': True}
                    hoster['extra'] = link[1]
                    hosters.append(hoster)
        return hosters
    
    def __get_movie_sources(self, source_url):
        hosters = []
        query = urlparse.parse_qs(urlparse.urlparse(source_url).query)
        if 'movie_id' in query:
            movie_id = query['movie_id']
        else:
            movie_id = self.__get_movie_id(source_url)
        
        if movie_id:
            details_url = MOVIE_DETAILS_URL % (movie_id[0])
            details_url = urlparse.urljoin(self.movie_base_url, details_url)
            detail_data = self._json_get(details_url, cache_limit=24)
            try: torrents = detail_data['data']['movie']['torrents']
            except KeyError: torrents = []
            try: hashes = [torrent['hash'].lower() for torrent in torrents]
            except KeyError: hashes = []
            hash_data = self.__get_hash_data(hashes)
            for torrent in torrents:
                hash_id = torrent['hash'].lower()
                try: status = hash_data['hashes'][hash_id]['status']
                except KeyError: status = ''
                if status.lower() == 'finished':
                    stream_url = 'hash_id=%s' % (hash_id)
                    host = self._get_direct_hostname(stream_url)
                    quality = QUALITY_MAP.get(torrent['quality'], QUALITIES.HD720)
                    hoster = {'multi-part': False, 'class': self, 'views': None, 'url': stream_url, 'rating': None, 'host': host, 'quality': quality, 'direct': True}
                    if 'size_bytes' in torrent: hoster['size'] = scraper_utils.format_size(torrent['size_bytes'], 'B')
                    if torrent['quality'] == '3D': hoster['3D'] = True
                    hosters.append(hoster)
        return hosters
    
    def __get_movie_id(self, source_url):
        url = urlparse.urljoin(self.movie_base_url, source_url)
        html = self._http_get(url, cache_limit=24)
        return dom_parser.parse_dom(html, 'div', {'id': 'movie-info'}, ret='data-movie-id')

    def __get_hash_data(self, hashes):
        new_data = {}
        if hashes:
            check_url = CHECKHASH_URL + urllib.urlencode([('hashes[]', hashes)], doseq=True)
            check_url = urlparse.urljoin(self.base_url, check_url)
            new_data = hash_data = self._json_get(check_url, cache_limit=.1)
            if 'hashes' in hash_data:
                new_data['hashes'] = dict((hash_id.lower(), hash_data['hashes'][hash_id]) for hash_id in hash_data['hashes'])
        return new_data
    
    def get_url(self, video):
        return self._default_get_url(video)

    def _get_episode_url(self, show_url, video):
        result = self.__find_episode(show_url, video)
        if result:
            return show_url
    
    def __find_episode(self, show_url, video):
        url = urlparse.urljoin(self.tv_base_url, show_url)
        html = self._http_get(url, cache_limit=2)
        magnets = dom_parser.parse_dom(html, 'a', {'class': 'magnet'}, ret='href')
        titles = dom_parser.parse_dom(html, 'a', {'class': 'magnet'}, ret='title')
        titles = [re.sub('\s+[Mm]agnet\s+[Ll]ink', '', title) for title in titles]
        hashes = []
        for i, magnet in enumerate(magnets):
            match = re.search('urn:btih:(.*?)(?:&|$)', magnet, re.I)
            if match:
                hashes.append((match.group(1), titles[i]))
        
        episode_pattern = 'S%02dE%02d' % (int(video.season), int(video.episode))
        if video.ep_airdate:
            airdate_pattern = '%d(-|.| )%02d(-|.| )%02d' % (video.ep_airdate.year, video.ep_airdate.month, video.ep_airdate.day)
        else:
            airdate_pattern = ''
            
        matches = [link for link in hashes if re.search(episode_pattern, link[1], re.I)]
        if not matches and airdate_pattern:
            matches = [link for link in hashes if re.search(airdate_pattern, link[1])]
        return matches

    def search(self, video_type, title, year, season=''):
        if video_type == VIDEO_TYPES.MOVIE:
            return self.__movie_search(title, year)
        else:
            return self.__tv_search(title, year)

    def __movie_search(self, title, year):
        results = []
        search_url = MOVIE_SEARCH_URL % (urllib.quote_plus(title))
        search_url = urlparse.urljoin(self.movie_base_url, search_url)
        js_data = self._json_get(search_url, cache_limit=1)
        if 'data' in js_data and 'movies' in js_data['data']:
            for movie in js_data['data']['movies']:
                match_year = str(movie['year'])
                match_url = movie['url'] + '?movie_id=%s' % (movie['id'])
                if 'title_english' in movie:
                    match_title = movie['title_english']
                else:
                    match_title = movie['title']
                    
                if not year or not match_year or year == match_year:
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)
        
        return results
        
    def __tv_search(self, title, year):
        results = []
        search_url = urlparse.urljoin(self.tv_base_url, '/showlist/')
        html = self._http_get(search_url, cache_limit=48)
        match_year = ''
        norm_title = scraper_utils.normalize_title(title)
        for item in dom_parser.parse_dom(html, 'td', {'class': 'forum_thread_post'}):
            match = re.search('href="([^"]+)[^>]+>([^<]+)', item)
            if match:
                match_url, match_title = match.groups()
                if match_title.upper().endswith(', THE'):
                    match_title = 'The ' + match_title[:-5]
        
                if norm_title in scraper_utils.normalize_title(match_title) and (not year or not match_year or year == match_year):
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)
        return results

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        settings = scraper_utils.disable_sub_check(settings)
        name = cls.get_name()
        settings.append('         <setting id="%s-use_https" type="bool" label="     %s" default="false" visible="eq(-4,true)"/>' % (name, i18n('use_https')))
        settings.append('         <setting id="%s-username" type="text" label="     %s" default="" visible="eq(-5,true)"/>' % (name, i18n('username')))
        settings.append('         <setting id="%s-password" type="text" label="     %s" option="hidden" default="" visible="eq(-6,true)"/>' % (name, i18n('password')))
        settings.append('         <setting id="%s-base_url2" type="text" label="     %s %s" default="%s" visible="eq(-7,true)"/>' % (name, i18n('movies'), i18n('base_url'), cls.movie_base_url))
        settings.append('         <setting id="%s-base_url3" type="text" label="     %s %s" default="%s" visible="eq(-8,true)"/>' % (name, i18n('tv_shows'), i18n('base_url'), cls.tv_base_url))
        return settings

    def _json_get(self, url, data=None, allow_redirect=True, cache_limit=8):
        if not self.username or not self.password:
            return {}
        
        if data is None: data = {}
        if 'premiumize.me' in url.lower():
            data.update({'customer_id': self.username, 'pin': self.password})
        result = super(self.__class__, self)._http_get(url, data=data, allow_redirect=allow_redirect, cache_limit=cache_limit)
        js_result = scraper_utils.parse_json(result, url)
        if 'status' in js_result and js_result['status'] == 'error':
            msg = js_result.get('message', js_result.get('status_message', 'Unknown Error'))
            log_utils.log('Premiumize Scraper Error: %s - (%s)' % (url, msg), log_utils.LOGWARNING)
            js_result = {}
            
        return js_result

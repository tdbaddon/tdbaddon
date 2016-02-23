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

import xbmc

from salts_lib import kodi
from salts_lib import log_utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import SORT_KEYS
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = ''

class Local_Scraper(scraper.Scraper):
    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.def_quality = int(kodi.get_setting('%s-def-quality' % (self.get_name())))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'Local'

    def resolve_link(self, link):
        return link

    def format_source_label(self, item):
        return '[%s] %s (%s views)' % (item['quality'], item['host'], item['views'])

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            params = urlparse.parse_qs(source_url)
            if video.video_type == VIDEO_TYPES.MOVIE:
                cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"movieid": %s, "properties" : ["file", "playcount", "streamdetails"]}, "id": "libMovies"}'
                result_key = 'moviedetails'
            else:
                cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodeDetails", "params": {"episodeid": %s, "properties" : ["file", "playcount", "streamdetails"]}, "id": "libTvShows"}'
                result_key = 'episodedetails'

            run = cmd % (params['id'][0])
            meta = xbmc.executeJSONRPC(run)
            meta = scraper_utils.parse_json(meta)
            log_utils.log('Source Meta: %s' % (meta), log_utils.LOGDEBUG)
            if 'result' in meta and result_key in meta['result']:
                details = meta['result'][result_key]
                def_quality = [item[0] for item in sorted(SORT_KEYS['quality'].items(), key=lambda x:x[1])][self.def_quality]
                host = {'multi-part': False, 'class': self, 'url': details['file'], 'host': 'XBMC Library', 'quality': def_quality, 'views': details['playcount'], 'rating': None, 'direct': True}
                stream_details = details['streamdetails']
                if len(stream_details['video']) > 0 and 'width' in stream_details['video'][0]:
                    host['quality'] = scraper_utils.width_get_quality(stream_details['video'][0]['width'])
                hosters.append(host)
        return hosters

    def get_url(self, video):
        return self._default_get_url(video)

    def _get_episode_url(self, show_url, video):
        params = urlparse.parse_qs(show_url)
        cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"tvshowid": %s, "season": %s, "filter": {"field": "%s", "operator": "is", "value": "%s"}, \
        "limits": { "start" : 0, "end": 25 }, "properties" : ["title", "season", "episode", "file", "streamdetails"], "sort": { "order": "ascending", "method": "label", "ignorearticle": true }}, "id": "libTvShows"}'
        base_url = 'video_type=%s&id=%s'
        episodes = []
        force_title = scraper_utils.force_title(video)
        if not force_title:
            run = cmd % (params['id'][0], video.season, 'episode', video.episode)
            meta = xbmc.executeJSONRPC(run)
            meta = scraper_utils.parse_json(meta)
            log_utils.log('Episode Meta: %s' % (meta), log_utils.LOGDEBUG)
            if 'result' in meta and 'episodes' in meta['result']:
                episodes = meta['result']['episodes']
        else:
            log_utils.log('Skipping S&E matching as title search is forced on: %s' % (video.trakt_id), log_utils.LOGDEBUG)

        if (force_title or kodi.get_setting('title-fallback') == 'true') and video.ep_title and not episodes:
            run = cmd % (params['id'][0], video.season, 'title', video.ep_title)
            meta = xbmc.executeJSONRPC(run)
            meta = scraper_utils.parse_json(meta)
            log_utils.log('Episode Title Meta: %s' % (meta), log_utils.LOGDEBUG)
            if 'result' in meta and 'episodes' in meta['result']:
                episodes = meta['result']['episodes']

        for episode in episodes:
            if episode['file'].endswith('.strm'):
                continue
            
            return base_url % (video.video_type, episode['episodeid'])

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        name = cls.get_name()
        settings.append('         <setting id="%s-def-quality" type="enum" label="     Default Quality" values="None|Low|Medium|High|HD720|HD1080" default="0" visible="eq(-4,true)"/>' % (name))
        return settings

    def search(self, video_type, title, year):
        filter_str = '{{"field": "title", "operator": "contains", "value": "{search_title}"}}'
        if year: filter_str = '{{"and": [%s, {{"field": "year", "operator": "is", "value": "%s"}}]}}' % (filter_str, year)
        if video_type == VIDEO_TYPES.MOVIE:
            cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": { "filter": %s, "limits": { "start" : 0, "end": 25 }, "properties" : ["title", "year", "file", "streamdetails"], \
            "sort": { "order": "ascending", "method": "label", "ignorearticle": true } }, "id": "libMovies"}'
            result_key = 'movies'
            id_key = 'movieid'
        else:
            cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": { "filter": %s, "limits": { "start" : 0, "end": 25 }, "properties" : ["title", "year"], \
            "sort": { "order": "ascending", "method": "label", "ignorearticle": true } }, "id": "libTvShows"}'
            result_key = 'tvshows'
            id_key = 'tvshowid'

        command = cmd % (filter_str.format(search_title=title))
        results = self.__get_results(command, result_key, video_type, id_key)
        norm_title = self.__normalize_title(title)
        if not results and norm_title and norm_title != title:
            command = cmd % (filter_str.format(search_title=norm_title))
            results = self.__get_results(command, result_key, video_type, id_key)
        return results
    
    def __normalize_title(self, title):
        norm_title = re.sub('[^A-Za-z0-9 ]', ' ', title)
        return re.sub('\s+', ' ', norm_title)
    
    def __get_results(self, cmd, result_key, video_type, id_key):
        results = []
        log_utils.log('Search Command: %s' % (cmd), log_utils.LOGDEBUG)
        meta = xbmc.executeJSONRPC(cmd)
        meta = scraper_utils.parse_json(meta)
        log_utils.log('Search Meta: %s' % (meta), log_utils.LOGDEBUG)
        if 'result' in meta and result_key in meta['result']:
            for item in meta['result'][result_key]:
                if video_type == VIDEO_TYPES.MOVIE and item['file'].endswith('.strm'):
                    continue

                result = {'title': item['title'], 'year': item['year'], 'url': 'video_type=%s&id=%s' % (video_type, item[id_key])}
                results.append(result)
        return results

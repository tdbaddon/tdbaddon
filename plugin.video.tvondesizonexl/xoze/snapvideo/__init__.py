'''
Created on Dec 21, 2013

@author: ajdeveloped@gmail.com

This file is part of XOZE. 

XOZE is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

XOZE is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with XOZE.  If not, see <http://www.gnu.org/licenses/>.
'''
from xoze.utils import http
import logging
import re
import sys
import elementtree.ElementTree as ET
from xoze.lib import importlib

STREAM_QUAL_LOW = 'LOW'
STREAM_QUAL_SD = 'STANDARD'
STREAM_QUAL_HD_720 = '720p'
STREAM_QUAL_HD_1080 = '1080p'
XBMC_EXECUTE_PLUGIN = 'execute_plugin'

class VideoHost:
    """Holds the information read from xoze.xml."""

    def __init__(self):
        self.__icon = None
        self.__name = None

    def get_icon(self):
        return self.__icon


    def get_name(self):
        return self.__name


    def set_icon(self, value):
        self.__icon = value


    def set_name(self, value):
        self.__name = value


    def del_icon(self):
        del self.__icon


    def del_name(self):
        del self.__name

    icon = property(get_icon, set_icon, del_icon, "icon's docstring")
    name = property(get_name, set_name, del_name, "name's docstring")
        
class Video:
    
    def __init__(self):
        self.__thumb_image = None
        self.__id = None
        self.__url = None
        self.__name = None
        self.__stopped = True
        self.__streams = {}
        self.__video_host = None

    def get_video_host(self):
        return self.__video_host


    def set_video_host(self, value):
        self.__video_host = value


    def del_video_host(self):
        del self.__video_host


    def get_streams(self):
        return self.__streams


    def set_streams(self, value):
        self.__streams = value


    def del_streams(self):
        del self.__streams


    def get_thumb_image(self):
        return self.__thumb_image


    def get_id(self):
        return self.__id


    def get_url(self):
        return self.__url


    def get_name(self):
        return self.__name


    def get_stopped(self):
        return self.__stopped


    def set_thumb_image(self, value):
        self.__thumb_image = value


    def set_id(self, value):
        self.__id = value


    def set_url(self, value):
        self.__url = value


    def set_name(self, value):
        self.__name = value


    def set_stopped(self, value):
        self.__stopped = value


    def del_thumb_image(self):
        del self.__thumb_image


    def del_id(self):
        del self.__id


    def del_url(self):
        del self.__url


    def del_name(self):
        del self.__name


    def del_stopped(self):
        del self.__stopped
        
        
    
    def get_stream_link(self, stream_qualilty):
        if self.__streams.has_key(stream_qualilty):
            return self.__streams[stream_qualilty]
        else:
            return None

    def add_stream_link(self, stream_qualilty, stream_link, addUserAgent=False, addReferer=False, refererUrl=None):
        if addUserAgent:
            video_link = stream_link.replace(' ', '%20') + '|' + http.getUserAgentForXBMCPlay()
            if addReferer and refererUrl is not None:
                video_link = video_link + '&Referer=' + refererUrl
        self.__streams[stream_qualilty] = stream_link

    thumb_image = property(get_thumb_image, set_thumb_image, del_thumb_image, "thumb_image's docstring")
    id = property(get_id, set_id, del_id, "id's docstring")
    url = property(get_url, set_url, del_url, "url's docstring")
    name = property(get_name, set_name, del_name, "name's docstring")
    stopped = property(get_stopped, set_stopped, del_stopped, "stopped's docstring")
    streams = property(get_streams, set_streams, del_streams, "streams's docstring")
    video_host = property(get_video_host, set_video_host, del_video_host, "video_host's docstring")
    
    
'''Snapper object'''
class Snapper(object):
    def __init__(self, snapper_Tag, addon_path):
        modulePath = snapper_Tag.attrib['module']
        functionName = snapper_Tag.attrib['function']
        self.__video_id_regex_list = []
        for video_id_elem in snapper_Tag.getchildren():
            self.__video_id_regex_list.append(video_id_elem.attrib['regex'])
        self.__is_playlist = False
        if snapper_Tag.attrib.has_key('playlist') and snapper_Tag.attrib['playlist'] == 'true':
            self.__is_playlist = True
        
        self.__snapper_module = importlib.import_module(modulePath, addon_path)
        self.__snapper_modulepath = modulePath
        self.__getVideoInfo = getattr(self.__snapper_module, functionName)
        self.getVideoHostingInfo = getattr(self.__snapper_module, 'getVideoHost')
        logging.getLogger().debug('Snapper loaded = ' + modulePath)

    def isPlaylistSnapper(self):
        return self.__is_playlist
    
    def getModuleName(self):
        return self.__snapper_modulepath
    
    def isVideoHostedByYou(self, video_url):
        isVideoHoster = False
        videoId = self.getVideoId(video_url)
        if videoId is not None:
            logging.getLogger().debug('Snapper selected = ' + self.getModuleName() + ' for video URL = ' + video_url)
            isVideoHoster = True
        return isVideoHoster
    
    def getVideoInfo(self, video_url):
        videoInfo = None
        videoId = self.getVideoId(video_url)
        if videoId is not None:
            logging.getLogger().debug('Snapper selected = ' + self.getModuleName() + ' for video URL = ' + video_url)
            videoInfo = self.__getVideoInfo(videoId)
        return videoInfo
    
    def getVideoId(self, video_url):
        videoId = None
        for video_id_regex in self.__video_id_regex_list:
            if video_id_regex == '*':
                func = getattr(self.__snapper_module, 'isUrlResolvable')
                if func(video_url):
                    videoId = video_url
            else:
                match = re.compile(video_id_regex).findall(video_url + '&')
                if len(match) > 0:
                    videoId = match[0]
                    break
        return videoId
    
    def do_clean(self):
        del self.__video_id_regex_list
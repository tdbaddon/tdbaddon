'''
Created on Feb 1, 2014

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
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD
from xoze.utils import http
import logging
import re

VIDEO_HOST_NAME = 'Nowvideo'

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://www.nowvideo.ch/images/logo.png')
    video_host.set_name(VIDEO_HOST_NAME)
    return video_host


def retrieveVideoInfo(video_id):
    
    video = Video()
    video.set_video_host(getVideoHost())
    video.set_id(video_id)
    try:
        http.HttpClient().enable_cookies()
        video_info_link = 'http://www.nowvideo.ch/video/' + str(video_id)
        logging.getLogger().debug(video_info_link)
        html = http.HttpClient().get_html_content(url=video_info_link)
        if re.search(r'Video hosting is expensive. We need you to prove you\'re human.', html):
            html = http.HttpClient().get_html_content(url=video_info_link)
        
        domainStr = re.compile('flashvars.domain="(.+?)"').findall(html)[0]
        fileStr = re.compile('flashvars.file="(.+?)"').findall(html)[0]
        filekey = re.compile('flashvars.filekey="(.+?)"').findall(html)
        filekeyStr = None
        if len(filekey) == 0:
            filekeyStr = re.compile('flashvars.filekey=(.+?);').findall(html)[0]
            filekeyStr = re.compile('var ' + filekeyStr + '="(.+?)"').findall(html)[0]
        else:
            filekeyStr = filekey[0]
        
        video_info_link = domainStr + '/api/player.api.php?user=undefined&pass=undefined&codes=1&file=' + fileStr + '&key=' + filekeyStr
        logging.getLogger().debug(video_info_link)
        html = http.HttpClient().get_html_content(url=video_info_link)
        video_link = re.compile(r'url=(.+?)&').findall(html)[0]
        http.HttpClient().disable_cookies()
        
        video.set_stopped(False)
        video.add_stream_link(STREAM_QUAL_SD, video_link)
    except: 
        video.set_stopped(True)
    return video

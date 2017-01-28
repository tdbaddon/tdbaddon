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
from xoze.utils import http, encoders
import logging
import re

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://movzap.com/images/logo.png')
    video_host.set_name('Movzap')
    return video_host

def retrieveVideoInfo(video_id):
    
    video = Video()
    video.set_video_host(getVideoHost())
    video.set_id(video_id)
    try:
        video_info_link = 'http://movzap.com/' + str(video_id)
        html = http.HttpClient().get_html_content(url=video_info_link)
        video_link = None
        paramSet = re.compile("return p\}\(\'(.+?)\',(\d+),(\d+),\'(.+?)\'").findall(html)
        if len(paramSet) > 0:
            video_info_link = encoders.parse_packed_value(paramSet[0][0], int(paramSet[0][1]), int(paramSet[0][2]), paramSet[0][3].split('|')).replace('\\', '').replace('"', '\'')
            
            img_data = re.compile(r"image:\'(.+?)\'").findall(video_info_link)
            if len(img_data) == 1:
                video.set_thumb_image(img_data[0])
            video_link = re.compile(r"file:\'(.+?)\'").findall(video_info_link)[0]
        else:
            video_link = re.compile("'file': '(.+?)'").findall(html)[0]
        video.set_stopped(False)
        video.add_stream_link(STREAM_QUAL_SD, video_link)
        
    except Exception, e:
        logging.getLogger().error(e)
        video.set_stopped(True)
    return video

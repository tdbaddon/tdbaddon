'''
Created on Jun 17, 2015

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


def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('')
    video_host.set_name('DittoTV')
    return video_host
    
def retrieveVideoInfo(video_id):
    
    video = Video()
    video.set_video_host(getVideoHost())
    video.set_id(video_id)
    try:
        http.HttpClient().enable_cookies()
        video_info_link = 'http://www.dittotv.com/' + str(video_id)
        html = http.HttpClient().get_html_content(url=video_info_link)
        video_link = re.compile('"file"\:"(.+?)"').findall(html)[0]
        video.set_stopped(False)
        video.add_stream_link(STREAM_QUAL_SD, video_link)
    except Exception, e:
        logging.exception(e)
        video.set_stopped(True)
    return video
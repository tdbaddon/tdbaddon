'''
Created on Dec 27, 2013

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

from xoze.snapvideo import VideoHost, UrlResolverDelegator

VIDEO_HOSTING_NAME = 'Mega'

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('https://eu.static.mega.co.nz/images/mega/logo.png')
    video_host.set_name(VIDEO_HOSTING_NAME)
    return video_host

def retrieveVideoInfo(video_id):
    videoUrl = "https://mega.co.nz/" + video_id
#     plugin://plugin.video.mega/?action=stream&url=
    return UrlResolverDelegator.retrieveVideoInfo(videoUrl)
'''
Created on Jan 13, 2014

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



'''
Created on Dec 25, 2011

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD

VIDEO_HOSTING_NAME = 'VideoPress'

def getVideoHost():
    video_hosting_info = VideoHost()
    video_hosting_info.set_icon('http://s2.wp.com/wp-content/themes/a8c/videopress4/img/logo-footer.png?m=1340912836g')
    video_hosting_info.set_name('VideoPress')
    return video_hosting_info
    
def retrieveVideoInfo(video_id):
    
    video_info = Video()
    video_info.set_video_host(getVideoHost())
    video_info.set_id(video_id)
    try:
        video_link = 'http://videos.videopress.com/' + str(video_id) + '.mp4'
        print video_link
        video_info.add_stream_link(STREAM_QUAL_SD, video_link)
        video_info.set_stopped(False)
        
    except: 
        video_info.set_stopped(True)
    return video_info

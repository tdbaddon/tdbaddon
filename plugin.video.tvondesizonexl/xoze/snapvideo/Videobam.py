'''
Created on Dec 25, 2011

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD, STREAM_QUAL_HD_720
from xoze.utils import http
import re

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('')
    video_host.set_name('Videobam')
    return video_host
    
def retrieveVideoInfo(video_id):
    video_info = Video()
    video_info.set_video_host(getVideoHost())
    video_info.set_id(video_id)
    try:
        video_info_link = 'http://videobam.com/' + str(video_id)
        html = http.HttpClient().get_html_content(url=video_info_link)
        streams = re.compile('(low|high): \'(.+?)\'').findall(html)
        for streamType, streamUrl in streams:
            if streamType == 'low':
                video_info.add_stream_link(STREAM_QUAL_SD, streamUrl)
            elif streamType == 'high':
                video_info.add_stream_link(STREAM_QUAL_HD_720, streamUrl)
        video_info.set_stopped(False)
        
    except: 
        video_info.set_stopped(True)
    return video_info

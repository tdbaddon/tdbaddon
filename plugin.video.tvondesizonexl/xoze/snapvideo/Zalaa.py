'''
Created on Dec 25, 2011

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD
from xoze.utils import http
import re


def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('')
    video_host.set_name('Zalaa')
    return video_host

def retrieveVideoInfo(video_id):
    
    video_info = Video()
    video_info.set_video_host(getVideoHost())
    video_info.set_id(video_id)
    try:
        video_info_link = 'http://www.zalaa.com/' + str(video_id)
        html = http.HttpClient().get_html_content(url=video_info_link)
        link = ''.join(html.splitlines()).replace('\'', '"')
        video_link = re.compile('s1.addVariable\("file","(.+?)"\);').findall(link)[0]
        video_info.add_stream_link(STREAM_QUAL_SD, video_link)
        video_info.set_stopped(False)
        
    except: 
        video_info.set_video_stopped(True)
    return video_info

'''
Created on Nov 2, 2014

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD
from xoze.utils import http
import re

VIDEO_HOST_NAME = 'vShare'

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://vshare.io/static/logo-small.png')
    video_host.set_name(VIDEO_HOST_NAME)
    return video_host

def retrieveVideoInfo(video_id):
    video_info = Video()
    video_info.set_video_host(getVideoHost())
    video_info.set_id(video_id)
    try:
        video_link = 'http://vshare.io/d/' + str(video_id)
        html = http.HttpClient().get_html_content(url=video_link)
        match = re.compile('document.getElementById\(\'download-link\'\).innerHTML = \'<a style="text-decoration:none;" href="(.+?)"').findall(html)
        video_link = match[0]
        video_info.set_stopped(False)
        video_info.add_stream_link(STREAM_QUAL_SD, video_link)
    except:
        video_info.set_stopped(True)
    return video_info

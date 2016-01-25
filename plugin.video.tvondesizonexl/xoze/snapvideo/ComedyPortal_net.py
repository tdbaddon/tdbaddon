'''
Created on Jun 11, 2013

@author: PK
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD
from xoze.utils import http
import re

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://www.comedyportal.net/themes/berylizer/gfx/logo.png')
    video_host.set_name('ComedyPortal')
    return video_host

def retrieveVideoInfo(video_id):
    video = Video()
    video.set_video_host(getVideoHost())
    video.set_id(video_id)
    try:
        video_link = 'http://www.comedyportal.net/' + str(video_id)
        html = http.HttpClient().get_html_content(url=video_link)
        match = re.compile("id='pl'.+?data='(.+?)'").findall(html)
        html = http.HttpClient().get_html_content(url=match[0].replace(' ', '%20'))
        video_link = re.compile("file : '(.+?)'").findall(html)[0].replace(' ', '%20')
        video.set_stopped(False)
        video.add_stream_link(STREAM_QUAL_SD, video_link)
    except:
        video.set_stopped(True)
    return video

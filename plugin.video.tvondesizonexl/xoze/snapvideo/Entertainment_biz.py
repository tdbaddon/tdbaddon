'''
Created on Jul 10, 2013

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD
from xoze.utils import http
import re
import urllib

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://my-entertainment.biz/forum/images/misc/vbulletin4_logo.png')
    video_host.set_name('My-Entertainment Biz')
    return video_host

def retrieveVideoInfo(video_id):
    video = Video()
    video.set_video_host(getVideoHost())
    video.set_id(video_id)
    try:
        video_link = 'http://my-entertainment.biz/' + str(video_id)
        http.HttpClient().enable_cookies()
        http.HttpClient().get_html_content(url='http://my-entertainment.biz/forum/content.php')
        html = http.HttpClient().get_html_content(url=video_link)
        match = re.compile("file=(.+?)&&").findall(html)
        video_link = urllib.unquote(match[0])
        video.set_stopped(False)
        video.add_stream_link(STREAM_QUAL_SD, video_link)
    except:
        video.set_stopped(True)
    return video

'''
Created on Nov 6, 2011

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD
from xoze.utils import http
import re

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://www.digitaldeparture.com/wp-content/images/zshare.jpg')
    video_host.set_name('ZShare')
    return video_host

def retrieveVideoInfo(video_id):
    video_info = Video()
    video_info.set_video_host(getVideoHost())
    video_info.set_id(video_id)
    try:
        video_link = 'http://www.zshare.net/video/' + str(video_id)
        html = http.HttpClient().get_html_content(url=video_link)
        match = re.compile('<iframe src="http://www.zshare.net/videoplayer/player.php(.+?)"').findall(html)
        html = http.HttpClient().get_html_content(url=('http://www.zshare.net/videoplayer/player.php' + match[0].replace(' ', '%20')))
        video_link = re.compile('file: "(.+?)"').findall(html)[0].replace(' ', '%20')
        video_info.set_stopped(False)
        video_info.add_stream_link(STREAM_QUAL_SD, video_link)
    except:
        video_info.set_stopped(True)
    return video_info

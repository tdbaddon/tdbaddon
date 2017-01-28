'''
Created on Jan 3, 2012

@author: ajju
'''
from xoze.snapvideo import VideoHost, STREAM_QUAL_SD, Video
from xoze.utils import http
import re

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://userlogos.org/files/logos/jumpordie/stagevu-iphone.png')
    video_host.set_name('StageVU')
    return video_host

def retrieveVideoInfo(video_id):
    
    video_info = Video()
    video_info.set_video_host(getVideoHost())
    video_info.set_id(video_id)
    try:
        video_info_link = 'http://stagevu.com/video/' + str(video_id)
        html = http.HttpClient().get_html_content(url=video_info_link)
        html = ''.join(html.splitlines()).replace('\t', '').replace('\'', '"')
        match = re.compile('<param name="src" value="(.+?)"(.+?)<param name="movieTitle" value="(.+?)"(.+?)<param name="previewImage" value="(.+?)"').findall(html)
        video_info.add_stream_link(STREAM_QUAL_SD, match[0][0])
        video_info.set_name(match[0][2])
        video_info.set_thumb_image(match[0][4])
        video_info.set_stopped(False)
        
    except: 
        video_info.set_stopped(True)
    return video_info

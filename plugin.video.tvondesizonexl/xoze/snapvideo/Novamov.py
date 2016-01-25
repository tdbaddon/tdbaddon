'''
Created on Dec 23, 2011

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD
from xoze.utils import http
import re

VIDEO_HOST_NAME = 'Novamov'

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://www.novamov.com/images/logo_novamov.jpg')
    video_host.set_name(VIDEO_HOST_NAME)
    return video_host


def retrieveVideoInfo(video_id):
    
    video = Video()
    video.set_video_host(getVideoHost())
    video.set_id(video_id)
    try:
        http.HttpClient().enable_cookies()
        video_info_link = 'http://www.novamov.com/video/' + str(video_id)
        html = http.HttpClient().get_html_content(url=video_info_link)
        if re.search(r'Video hosting is expensive. We need you to prove you\'re human.', html):
            html = http.HttpClient().get_html_content(url=video_info_link)

        domainStr = re.compile('flashvars.domain="(.+?)"').findall(html)[0]
        fileStr = re.compile('flashvars.file="(.+?)"').findall(html)[0]
        filekey = re.compile('flashvars.filekey="(.+?)"').findall(html)
        filekeyStr = None
        if len(filekey) == 0:
            filekeyStr = re.compile('flashvars.filekey=(.+?);').findall(html)[0]
            filekeyStr = re.compile('var ' + filekeyStr + '="(.+?)"').findall(html)[0]
        else:
            filekeyStr = filekey[0]
        video_info_link = domainStr + '/api/player.api.php?user=undefined&pass=undefined&codes=1&file=' + fileStr + '&key=' + filekeyStr
        html = http.HttpClient().get_html_content(url=video_info_link)
        video_link = re.compile(r'url=(.+?)&').findall(html)[0]
        http.HttpClient().disable_cookies()
        
        video.set_stopped(False)
        video.add_stream_link(STREAM_QUAL_SD, video_link)
    except: 
        video.set_stopped(True)
    return video


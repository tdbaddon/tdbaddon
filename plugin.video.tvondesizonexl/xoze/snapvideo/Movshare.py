'''
Created on Dec 22, 2011

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD
from xoze.utils import http
import re

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://www.movshare.net/images/logo.png')
    video_host.set_name('Movshare')
    return video_host

def retrieveVideoInfo(video_id):
    
    video = Video()
    video.set_video_host(getVideoHost())
    video.set_id(video_id)
    try:
        http.HttpClient().enable_cookies()
        video_info_link = 'http://www.movshare.net/video/' + str(video_id)
        html = http.HttpClient().get_html_content(url=video_info_link)
        if re.search(r'Video hosting is expensive. We need you to prove you\'re human.', html):
            html = http.HttpClient().get_html_content(url=video_info_link)

        video_info_link = re.compile('<embed type="video/divx" src="(.+?)"').findall(html)
        video_link = ''
        if len(video_info_link) == 0:
            domainStr = re.compile('flashvars.domain="(.+?)"').findall(html)[0]
            fileStr = re.compile('flashvars.file="(.+?)"').findall(html)[0]
            filekeyStr = re.compile('flashvars.filekey="(.+?)"').findall(html)[0]
            
            video_info_link = domainStr + '/api/player.api.php?user=undefined&pass=undefined&codes=1&file=' + fileStr + '&key=' + filekeyStr
            html = http.HttpClient().get_html_content(url=video_info_link)
            video_link = re.compile(r'url=(.+?)&').findall(html)[0]
        else:
            video_link = video_info_link[0]
            
        http.HttpClient().disable_cookies()
        
        video.set_stopped(False)
        video.add_stream_link(STREAM_QUAL_SD, video_link)
    except: 
        video.set_stopped(True)
    return video

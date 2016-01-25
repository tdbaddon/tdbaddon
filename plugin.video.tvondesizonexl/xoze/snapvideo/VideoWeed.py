'''
Created on Dec 23, 2011

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD
import re
from xoze.utils import http

VIDEO_HOST_NAME = 'VideoWeed'

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://www.videoweed.es/images/logo.png')
    video_host.set_name(VIDEO_HOST_NAME)
    return video_host

    
def retrieveVideoInfo(video_id):
    
    video_info = Video()
    video_info.set_video_host(getVideoHost())
    video_info.set_id(video_id)
    try:
        http.HttpClient().enable_cookies()
        video_info_link = 'http://www.videoweed.es/file/' + str(video_id)
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
        
        video_info.set_stopped(False)
        video_info.add_stream_link(STREAM_QUAL_SD, video_link)
    except: 
        video_info.set_stopped(True)
    return video_info

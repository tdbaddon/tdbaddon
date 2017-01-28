'''
Created on Dec 23, 2011

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD
from xoze.utils import http
import logging
import re

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://www.divxstage.eu/images/logo.jpg')
    video_host.set_name('DivXStage')
    return video_host
    
def retrieveVideoInfo(video_id):
    
    video = Video()
    video.set_video_host(getVideoHost())
    video.set_id(video_id)
    try:
        http.HttpClient().enable_cookies()
        video_info_link = 'http://www.divxstage.eu/video/' + str(video_id)
        html = http.HttpClient().get_html_content(url=video_info_link)
        if re.search(r'Video hosting is expensive. We need you to prove you\'re human.', html):
            html = http.HttpClient().get_html_content(url=video_info_link)
        
        http.HttpClient().disable_cookies()
        fileKey = re.compile('flashvars.filekey="(.+?)";').findall(html)[0]
        video_info_link = 'http://www.divxstage.eu/api/player.api.php?file=' + video_id + '&key=' + fileKey
        html = http.HttpClient().get_html_content(url=video_info_link)
        video_link = re.compile('url=(.+?)&').findall(html)[0]
        video.set_stopped(False)
        video.add_stream_link(STREAM_QUAL_SD, video_link)
    except Exception, e:
        logging.exception(e)
        video.set_stopped(True)
    return video

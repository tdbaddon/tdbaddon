'''
Created on Nov 21, 2012

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_HD_720
from xoze.utils import http
import logging
import re

VIDEO_HOSTING_NAME = 'TVlogy'

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://i.imgur.com/BQ75a3I.jpg')
    video_host.set_name(VIDEO_HOSTING_NAME)
    return video_host


def retrieveVideoInfo(video_id):
    video = Video()
    video.set_video_host(getVideoHost())
    video.set_id(video_id)
    try:
        video_link = 'http://tvlogy.com/watch.php?v=' + str(video_id)
        html = http.HttpClient().get_html_content(url=video_link)
        video_link = re.compile("file: '(.+?)',").findall(html)[0]
        logging.debug('get video info: ' + video_link)
        logging.getLogger().debug('video_link ' + str(video_link))

        video.set_stopped(False)
        video.set_name("TVlogy Video")
        video.add_stream_link(STREAM_QUAL_HD_720, video_link)
    except:
        video.set_stopped(True)
    return video


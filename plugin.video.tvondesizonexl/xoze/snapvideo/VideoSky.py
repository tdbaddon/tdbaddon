'''
Created on May 6, 2015

@author: jchirag
'''

from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD
from xoze.utils import http
import logging, urllib2, urllib
import re

VIDEO_HOSTING_NAME = 'VIDEOSKY'

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://i1068.photobucket.com/albums/u460/chirag1983/video_sky_logo_zpsu5rb6qzk.png')
    video_host.set_name(VIDEO_HOSTING_NAME)
    return video_host

def retrieveVideoInfo(video_id):
    video = Video()
    video.set_video_host(getVideoHost())
    video.set_id(video_id)
    try:
        video_link = 'http://www.videosky.to/embed.php?id=' + str(video_id)
        mobileagent = urllib.quote_plus('AppleCoreMedia/1.0.0.10B146 (iPad; U; CPU OS 6_1_2 like Mac OS X; en_us)')
        req = urllib2.Request(video_link)
        req.add_header('User-Agent', mobileagent)
        response = urllib2.urlopen(req)
        html=response.read()
        response.close()
        video_link = re.compile('source src=\"(.+?)\?cloudy_stream=true').findall(html)[0]
        video.set_stopped(False)
        video.set_thumb_image('')
        video.set_name("Video Sky Video")
        video.add_stream_link(STREAM_QUAL_SD, video_link)
    except:
        video.set_stopped(True)
    return video


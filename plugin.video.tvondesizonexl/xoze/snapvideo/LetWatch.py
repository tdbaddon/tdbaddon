'''
Created on Apr 30, 2015

@author: jchirag
'''

#from xoze.snapvideo import VideoHost
import logging
import re

from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_HD_720, STREAM_QUAL_SD
from xoze.utils import http, encoders


VIDEO_HOST_NAME = 'letwatch'

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://letwatch.us/images/logo.png')
    video_host.set_name(VIDEO_HOST_NAME)
    return video_host

def retrieveVideoInfo(video_id):
    import urlresolver
    videoUrl =  'http://letwatch.us/embed-' + str(video_id) + '-595x430.html'
    media = urlresolver.HostedMediaFile(url=videoUrl, title='')       

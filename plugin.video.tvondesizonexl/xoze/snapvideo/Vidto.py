'''
Created on Nov 2, 2014

@author: ajju
'''
from xoze.snapvideo import VideoHost, UrlResolverDelegator

VIDEO_HOST_NAME = 'vidto'

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://static.vidto.me/static/images/header-logo.png')
    video_host.set_name(VIDEO_HOST_NAME)
    return video_host

def retrieveVideoInfo(video_id):
    videoUrl = 'http://vidto.me/' + str(video_id) + '.html'
    return UrlResolverDelegator.retrieveVideoInfo(videoUrl)

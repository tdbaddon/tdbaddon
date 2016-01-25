'''
Created on Nov 21, 2012

@author: ajju
'''
from xoze.snapvideo import VideoHost, UrlResolverDelegator

VIDEO_HOSTING_NAME = 'PutLocker'

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://static.putlocker.com/images/v1_r2_c5.png')
    video_host.set_name(VIDEO_HOSTING_NAME)
    return video_host

def retrieveVideoInfo(video_id):
    videoUrl = "http://www.putlocker.com/file/" + video_id
    return UrlResolverDelegator.retrieveVideoInfo(videoUrl)
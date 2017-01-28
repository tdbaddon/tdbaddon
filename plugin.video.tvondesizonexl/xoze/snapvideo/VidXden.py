'''
Created on Dec 23, 2011

@author: ajju
'''
from xoze.snapvideo import VideoHost, UrlResolverDelegator

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('')
    video_host.set_name('VidXden')
    return video_host

def retrieveVideoInfo(video_id):
    videoUrl = 'http://www.vidxden.com/' + str(video_id)
    return UrlResolverDelegator.retrieveVideoInfo(videoUrl)

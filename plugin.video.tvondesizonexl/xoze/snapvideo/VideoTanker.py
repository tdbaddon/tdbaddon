'''
Created on Jan 22, 2015

@author: jchirag
'''
from xoze.snapvideo import VideoHost, UrlResolverDelegator

VIDEO_HOST_NAME = 'VideoTanker'

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://videotanker.co/images/plaery-logo.png')
    video_host.set_name(VIDEO_HOST_NAME)
    return video_host

def retrieveVideoInfo(video_id):

    videoUrl = 'http://videotanker.co/player/embed_player.php?vid=' + str(video_id)
    return UrlResolverDelegator.retrieveVideoInfo(videoUrl)

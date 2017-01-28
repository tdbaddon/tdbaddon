'''
Created on Nov 21, 2012

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD
import logging
try:
    import urlresolver  # @UnresolvedImport
except:
    import xoze.alternatives.urlresolverdummy as urlresolver

def isUrlResolvable(videoUrl):
    return urlresolver.HostedMediaFile(url=videoUrl).valid_url()

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('')
    video_host.set_name('Finding Link using urlresolver')
    return video_host

def retrieveVideoInfo(videoUrl):
    
    video_info = Video()
    video_info.set_video_host(getVideoHost())
    video_info.set_id(videoUrl)
    
    sources = []
    hosted_media = urlresolver.HostedMediaFile(url=videoUrl)
    sources.append(hosted_media)
    source = urlresolver.choose_source(sources)
    stream_url = ''
    if source: 
        stream_url = source.resolve()

    video_info.set_stopped(False)
    video_info.set_thumb_image('')
    video_info.set_name(' ')
    video_info.add_stream_link(STREAM_QUAL_SD, stream_url)
    return video_info


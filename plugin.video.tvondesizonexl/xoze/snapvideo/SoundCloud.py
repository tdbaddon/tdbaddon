'''
Created on Jun 29, 2012

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD
from xoze.utils import http
import logging

try:
    import json
except ImportError:
    import simplejson as json
    
def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('')
    video_host.set_name('SoundCloud')
    return video_host

def retrieveAudioInfo(audioUrl):
    url = 'https://api.soundcloud.com/' + audioUrl
    jObj = json.loads(http.HttpClient().get_html_content(url=url))
    
    video_info = Video()
    video_info.set_video_host(getVideoHost())
    video_info.set_id(url)
    video_info.add_stream_link(STREAM_QUAL_SD, jObj['http_mp3_128_url'])
    video_info.set_thumb_image('')
    video_info.set_name('')
    
    logging.getLogger().debug(jObj['http_mp3_128_url'])
    video_info.set_stopped(False)
    return video_info

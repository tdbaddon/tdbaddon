'''
Created on Nov 21, 2012

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_LOW, \
    STREAM_QUAL_SD
from xoze.utils import http
import logging
import re

try:
    import json
except ImportError:
    import simplejson as json

VIDEO_HOSTING_NAME = 'PLAYWIRE'

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://cdn.intergi.com/playwire/playwire-logo-subhed.png')
    video_host.set_name(VIDEO_HOSTING_NAME)
    return video_host


def retrieveVideoInfo(video_id):
    video = Video()
    video.set_video_host(getVideoHost())
    video.set_id(video_id)
    try:
        video_link = 'https://config.playwire.com/videos/v2/%s/player.json' % str(video_id)
        logging.debug('get video info: ' + video_link)
        html = http.HttpClient().get_html_content(url=video_link)
        jsonObj = json.loads(html)
        video_link = str(jsonObj['src'])
        video_info = re.compile('config.playwire.com/(.+?)/videos/v2/(.+?)/manifest.f4m').findall(video_link)[0]        
        video_link = 'http://cdn.phoenix.intergi.com/' + video_info[0] + '/videos/' + video_info[1] + '/video-sd.mp4?hosting_id=' + video_info[0]
        img_link = ""
        if 'poster' in jsonObj:
            img_link = str(jsonObj['poster'])
        else:
            img_link = 'http://cdn.intergi.com/playwire/playwire-logo-subhed.png'
        name = str(jsonObj['title'])
        video.add_stream_link(STREAM_QUAL_SD, video_link)        
        video.set_stopped(False)
        if img_link != "":
            video.set_thumb_image(img_link)
        
    except Exception, e:
        logging.getLogger().error(e)
        video.set_stopped(True)
    return video

print retrieveVideoInfo('4521893')

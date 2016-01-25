'''
Created on Nov 21, 2012

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_HD_720
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
        video_link = 'http://config.playwire.com/' + str(video_id) + '.json'
        html = http.HttpClient().get_html_content(url=video_link)
        jsonObj = json.loads(html)
        logging.getLogger().debug(jsonObj)
        img_link = str(jsonObj['poster'])
        video_link = str(jsonObj['src'])
        logging.debug('get video info: ' + video_link)
        video_info = re.compile('config.playwire.com/(.+?)/videos/v2/(.+?)/manifest.f4m').findall(video_link)[0]
        
        logging.getLogger().debug('video_serial_no ' + str(video_info))
 
        video_link = 'http://cdn.phoenix.intergi.com/' + video_info[0] + '/videos/' + video_info[1] + '/video-sd.mp4?hosting_id=' + video_info[0]
        logging.getLogger().debug('video_link ' + str(video_link))

        video.set_stopped(False)
        video.set_thumb_image(img_link)
        video.set_name("PLAYWIRE Video")
        if re.search(r'\Artmp', video_link):
            video.add_stream_link(STREAM_QUAL_HD_720, video_link)
        else:
            video.add_stream_link(STREAM_QUAL_HD_720, video_link)
    except:
        video.set_stopped(True)
    return video


'''
Created on Nov 21, 2012

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_LOW, \
    STREAM_QUAL_SD
from xoze.utils import http
import logging

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
        video_link = 'https://config.playwire.com/videos/v2/%s/zeus.json' % str(video_id)
        logging.debug('get video info: ' + video_link)
        html = http.HttpClient().get_html_content(url=video_link)
        jsonObj = json.loads(html)
        img_link = str(jsonObj['content']['poster'])
        video_link = str(jsonObj['content']['media']['f4m'])
        name = str(jsonObj['settings']['title'])
        logging.getLogger().debug('video info ' + str(video_link))
        
        soup = http.HttpClient().get_beautiful_soup(url=video_link)
        baseurl = soup.findChild('baseurl')
        logging.getLogger().debug(str(baseurl.text))
        medias = soup.findChildren('media')
        for mediaInfo in medias:
            video_link = str(baseurl.text) + '/' + mediaInfo['url']
            logging.getLogger().debug(video_link)
            if mediaInfo['bitrate'] == '1200':
                video.add_stream_link(STREAM_QUAL_SD, video_link)
            else:
                video.add_stream_link(STREAM_QUAL_LOW, video_link)
        
        video.set_stopped(False)
        video.set_thumb_image(img_link)
        video.set_name(name)
        
    except Exception, e:
        logging.getLogger().error(e)
        video.set_stopped(True)
    return video

print retrieveVideoInfo('4521893')

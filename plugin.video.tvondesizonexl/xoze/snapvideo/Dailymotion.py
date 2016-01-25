'''
Created on Oct 29, 2011

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_LOW, STREAM_QUAL_SD, \
    STREAM_QUAL_HD_720, STREAM_QUAL_HD_1080
from xoze.utils import http
import logging
import re
try:
    import json
except ImportError:
    import simplejson as json

VIDEO_HOSTING_NAME = 'Dailymotion'

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://fontslogo.com/wp-content/uploads/2013/02/Dailymotion-LOGO.jpg')
    video_host.set_name(VIDEO_HOSTING_NAME)
    return video_host
    
def retrieveVideoInfo(video_id):
    video = Video()
    video.set_video_host(getVideoHost())
    video.set_id(video_id)
    try:
        video_link = 'http://www.dailymotion.com/embed/video/' + str(video_id)
        html = http.HttpClient().get_html_content(url=video_link)
        http.HttpClient().disable_cookies()
        
        player = re.compile('document\.getElementById\(\'player\'\), (.+?)\);').findall(html)
        player_obj = json.loads(player[0])
        video_qual = player_obj['metadata']['qualities']
        print video_qual
        dm_LD = None
        if video_qual.has_key('380'):
            dm_LD = video_qual['380'][0]['url']
        dm_SD = None
        if video_qual.has_key('480'):
            dm_SD = video_qual['480'][0]['url']
        dm_720 = None
        if video_qual.has_key('720'):
            dm_720 = video_qual['720'][0]['url']
        dm_1080 = None
        if video_qual.has_key('1080'):
            dm_1080 = video_qual['1080'][0]['url']
        
        if dm_LD is not None:
            video.add_stream_link(STREAM_QUAL_LOW, dm_LD, addUserAgent=False , addReferer=False, refererUrl=video_link)
        if dm_SD is not None:
            video.add_stream_link(STREAM_QUAL_SD, dm_SD, addUserAgent=False , addReferer=False, refererUrl=video_link)
        if dm_720 is not None:
            video.add_stream_link(STREAM_QUAL_HD_720, dm_720, addUserAgent=False , addReferer=False, refererUrl=video_link)
        if dm_1080 is not None:
            video.add_stream_link(STREAM_QUAL_HD_1080, dm_1080, addUserAgent=False , addReferer=False, refererUrl=video_link)
        if len(video.get_streams()) == 0:
            video.set_stopped(True)
        else:
            video.set_stopped(False)
    except Exception, e:
        logging.getLogger().error(e)
        video.set_stopped(True)
    return video


def retrievePlaylistVideoItems(playlistId):
    html = http.HttpClient().get_html_content(url='https://api.dailymotion.com/playlist/' + playlistId + '/videos')
    playlistJsonObj = json.loads(html)
    videoItemsList = []
    for video in playlistJsonObj['list']:
        videoItemsList.append('http://www.dailymotion.com/video/' + str(video['id']))
    return videoItemsList


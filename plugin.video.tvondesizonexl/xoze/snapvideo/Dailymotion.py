'''
Created on Oct 29, 2011

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_LOW, STREAM_QUAL_SD, \
    STREAM_QUAL_HD_720, STREAM_QUAL_HD_1080
from xoze.utils import http
import logging
import urllib
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
        
        matchHDLink = ''
        matchHQLink = ''
        matchSDLink = ''
        matchLDLink = ''

        matchHD = re.compile('720\"\:\[\{\"type\"\:\"application\\\/x\-mpegURL\"\,\"url\"\:\"(.+?)\"\}\,\{\"type\"\:\"video\\\/mp4\"\,\"url\"\:\"(.+?)\"', re.DOTALL).findall(html)
        matchHQ = re.compile('480\"\:\[\{\"type\"\:\"application\\\/x\-mpegURL\"\,\"url\"\:\"(.+?)\"\}\,\{\"type\"\:\"video\\\/mp4\"\,\"url\"\:\"(.+?)\"', re.DOTALL).findall(html)
        matchSD = re.compile('380\"\:\[\{\"type\"\:\"application\\\/x\-mpegURL\"\,\"url\"\:\"(.+?)\"\}\,\{\"type\"\:\"video\\\/mp4\"\,\"url\"\:\"(.+?)\"', re.DOTALL).findall(html)
        matchLD = re.compile('240\"\:\[\{\"type\"\:\"application\\\/x\-mpegURL\"\,\"url\"\:\"(.+?)\"\}\,\{\"type\"\:\"video\\\/mp4\"\,\"url\"\:\"(.+?)\"', re.DOTALL).findall(html)

        try:
            if matchHD[0][1]:
                matchHDLink = matchHD[0][1]
        except:
            print "No Dailymotion HD Link"

        try:
            if matchHQ[0][1]:
                matchHQLink = matchHQ[0][1]
        except:
            print "No Dailymotion HQ Link"

        try:
            if matchSD[0][1]:
                matchSDLink = matchSD[0][1]
        except:
            print "No Dailymotion SD Link"

        try:
            if matchLD[0][1]:
                matchLDLink = matchLD[0][1]
        except:
            print "No Dailymotion LD Link"

        matchHDLink = matchHDLink.replace('\/', '/')
        matchHQLink = matchHQLink.replace('\/', '/')
        matchSDLink = matchSDLink.replace('\/', '/')
        matchLDLink = matchLDLink.replace('\/', '/')

        dm_LD = None
        dm_SD = None
        dm_HQ = None    
        dm_720 = None
        final_url = None

        if matchHDLink:
            dm_720 = urllib.unquote_plus(matchHDLink).replace("\\", "")
        if dm_720 is None and matchHQ:
            dm_720 = urllib.unquote_plus(matchHQLink).replace("\\", "")
        if matchSD:
            dm_SD = urllib.unquote_plus(matchSDLink).replace("\\", "")
        if matchLD:
            dm_LD = urllib.unquote_plus(matchLDLink).replace("\\", "")

        if final_url is None and dm_720 is not None:
            final_url = dm_720
        if final_url is None and dm_HQ is not None:
            final_url = dm_HQ
        if final_url is None and dm_SD is not None:
            final_url = dm_SD
        if final_url is None and dm_LD is not None:
            final_url = dm_LD


        video.add_stream_link(STREAM_QUAL_HD_1080, final_url, addUserAgent=False , addReferer=False, refererUrl=video_link)
        video.set_thumb_image('http://fontslogo.com/wp-content/uploads/2013/02/Dailymotion-LOGO.jpg')
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


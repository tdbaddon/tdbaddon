'''
Created on Dec 23, 2011

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD, STREAM_QUAL_HD_720
from xoze.utils import http
import logging
import re
import urllib

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://www.koreaittimes.com/images/imagecache/medium/facebook-video-player-logo.png')
    video_host.set_name('Facebook')
    return video_host
    
def retrieveVideoInfo(video_id):
    
    video = Video()
    video.set_video_host(getVideoHost())
    video.set_id(video_id)
    try:
        
        video_info_link = 'http://www.facebook.com/video/video.php?v=' + str(video_id)
        html = urllib.unquote_plus(http.HttpClient().get_html_content(url=video_info_link).replace('\u0025', '%'))

        video_title = re.compile('addVariable\("video_title"\, "(.+?)"').findall(html)[0]
        img_link = re.compile('addVariable\("thumb_url"\, "(.+?)"').findall(html)[0]
        high_video_link = re.compile('addVariable\("highqual_src"\, "(.+?)"').findall(html)
        low_video_link = re.compile('addVariable\("lowqual_src"\, "(.+?)"').findall(html)
        video_link = re.compile('addVariable\("video_src"\, "(.+?)"').findall(html)
        if len(high_video_link) > 0:
            video.add_stream_link(STREAM_QUAL_HD_720, high_video_link[0])
        if len(low_video_link) > 0:
            video.add_stream_link(STREAM_QUAL_SD, low_video_link[0])
        if len(video_link) > 0:
            video.add_stream_link(STREAM_QUAL_SD, video_link[0])

        video.set_stopped(False)
        video.set_name(video_title)
        video.set_thumb_image(img_link)
    except Exception, e:
        video.set_stopped(True)
        logging.getLogger().error(e)
    return video


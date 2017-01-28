'''
@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_LOW, STREAM_QUAL_SD, \
    STREAM_QUAL_HD_720, STREAM_QUAL_HD_1080
from xoze.utils import http
import logging
import re

VIDEO_HOSTING_NAME = 'Google Docs'

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://oakhill.newton.k12.ma.us/sites/oakhill.newton.k12.ma.us/files/users/3/google_docs_image.png')
    video_host.set_name(VIDEO_HOSTING_NAME)
    return video_host
    
def retrieveVideoInfo(video_id):
    
    video = Video()
    video.set_video_host(getVideoHost())
    video.set_id(video_id)
    try:
        html = http.HttpClient().get_html_content(url='https://docs.google.com/file/' + str(video_id) + '?pli=1')
        title = re.compile("'title': '(.+?)'").findall(html)[0]
        video.set_name(title)
        stream_map = re.compile('fmt_stream_map":"(.+?)"').findall(html)[0].replace("\/", "/")
        formatArray = stream_map.split(',')
        for formatContent in formatArray:
            formatContentInfo = formatContent.split('|')
            qual = formatContentInfo[0]
            url = formatContentInfo[1]
            if(qual == '13'):  # 176x144
                video.add_stream_link(STREAM_QUAL_LOW, url)
            elif(qual == '17'):  # 176x144
                video.add_stream_link(STREAM_QUAL_LOW, url)
            elif(qual == '36'):  # 320x240
                video.add_stream_link(STREAM_QUAL_LOW, url)
            elif(qual == '5'):  # 400\\327226
                video.add_stream_link(STREAM_QUAL_LOW, url)
            elif(qual == '34'):  # 480x360 FLV
                video.add_stream_link(STREAM_QUAL_SD, url)
            elif(qual == '6'):  # 640\\327360 FLV
                video.add_stream_link(STREAM_QUAL_SD, url)
            elif(qual == '35'):  # 854\\327480 HD
                video.add_stream_link(STREAM_QUAL_SD, url)
            elif(qual == '18'):  # 480x360 MP4
                video.add_stream_link(STREAM_QUAL_SD, url)
            elif(qual == '22'):  # 1280x720 MP4
                video.add_stream_link(STREAM_QUAL_HD_720, url)
            elif(qual == '37'):  # 1920x1080 MP4
                video.add_stream_link(STREAM_QUAL_HD_1080, url)
            elif(qual == '38' and video.get_video_link(STREAM_QUAL_HD_1080) is None):  # 4096\\3272304 EPIC MP4
                video.add_stream_link(STREAM_QUAL_HD_1080, url)
            elif(qual == '43' and video.get_video_link(STREAM_QUAL_SD) is None):  # 360 WEBM
                video.add_stream_link(STREAM_QUAL_SD, url)
            elif(qual == '44'):  # 480 WEBM
                video.add_stream_link(STREAM_QUAL_SD, url)
            elif(qual == '45' and video.get_video_link(STREAM_QUAL_HD_720) is None):  # 720 WEBM
                video.add_stream_link(STREAM_QUAL_HD_720, url)
            elif(qual == '46' and video.get_video_link(STREAM_QUAL_HD_1080) is None):  # 1080 WEBM
                video.add_stream_link(STREAM_QUAL_HD_1080, url)
            elif(qual == '120' and video.get_video_link(STREAM_QUAL_HD_720) is None):  # New video qual
                video.add_stream_link(STREAM_QUAL_HD_720, url)
                # 3D streams - MP4
                # 240p -> 83
                # 360p -> 82
                # 520p -> 85
                # 720p -> 84
                # 3D streams - WebM
                # 360p -> 100
                # 360p -> 101
                # 720p -> 102
            else:  # unknown quality
                video.add_stream_link(STREAM_QUAL_SD, url)

            video.set_stopped(False)
    except Exception, e:
        logging.exception(e)
        video.set_stopped(True)
    return video


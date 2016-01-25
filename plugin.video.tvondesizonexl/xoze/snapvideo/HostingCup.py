'''
Created on Dec 24, 2011

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD
from xoze.utils import http, encoders
import re

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon()
    video_host.set_name('HostingCup')
    return video_host

def retrieveVideoInfo(video_id):
    
    video = Video()
    video.set_video_host(getVideoHost())
    video.set_id(video_id)
    try:
        video_info_link = 'http://www.vidpe.com/' + str(video_id)
        html = http.HttpClient().get_html_content(url=video_info_link)
        video_link = None
        paramSet = re.compile("return p\}\(\'(.+?)\',(\d+),(\d+),\'(.+?)\'").findall(html)
        if len(paramSet) > 0:
            video_info_link = encoders.parse_packed_value(paramSet[0][0], int(paramSet[0][1]), int(paramSet[0][2]), paramSet[0][3].split('|')).replace('\\', '').replace('"', '\'')
            
            img_data = re.compile(r"image:\'(.+?)\'").findall(video_info_link)
            if len(img_data) == 1:
                video.set_thumb_image(img_data[0])
            video_link = re.compile(r"file:\'(.+?)\'").findall(video_info_link)[0]
        else:
            video_link = re.compile("'file': '(.+?)'").findall(html)[0]
        video.set_stopped(False)
        video.add_stream_link(STREAM_QUAL_SD, video_link)
        
    except: 
        video.set_stopped(True)
    return video

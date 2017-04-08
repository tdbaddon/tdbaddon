'''
Created on Dec 24, 2011

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD
from xoze.utils import http, encoders
import re

VIDEO_HOSTING_NAME = 'WatchVideo2US'

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://watchvideo.us/img/logo.png')
    video_host.set_name(VIDEO_HOSTING_NAME)
    return video_host

def retrieveVideoInfo(video_id):
    
    video = Video()
    video.set_video_host(getVideoHost())
    video.set_id(video_id)
    try:
        video_info_link = 'http://watchvideo2.us/embed-' + str(video_id) + '-540x304.html'
        html = http.HttpClient().get_html_content(url=video_info_link)
        html = html.replace(' ', '')
        html = html.replace('\'', '"')
        try:
            video_link = 'http' + re.compile('file:"http(.+?)m3u8"').findall(html)[0] + 'm3u8'
            img_link = re.compile('image:"(.+?)"').findall(html)[0]
            video.set_thumb_image(img_link)
        except:
            video_link = 'http' + re.compile('file:"http(.+?)mp4"').findall(html)[0] + 'mp4'

        if ('.m3u8' in video_link):
            try:
                html = http.HttpClient().get_html_content(url=video_link)
                html = html.replace(' ', '')
                html = html.replace('\'', '"')
                final_video_link = 'http' + re.compile('http(.+?)m3u8').findall(html)[0] + 'm3u8'
            except:
                final_video_link = video_link

        if final_video_link == '' or final_video_link == None:
            paramSet = re.compile("return p\}\(\'(.+?)\',(\d+),(\d+),\'(.+?)\'").findall(html)
            try:
                if len(paramSet) > 0:
                    video_info_link = encoders.parse_packed_value(paramSet[0][0], int(paramSet[0][1]), int(paramSet[0][2]), paramSet[0][3].split('|')).replace('\\', '').replace('"', '\'')
                    img_data = re.compile(r"image:\'(.+?)\'").findall(video_info_link)
                    if len(img_data) == 1:
                        video.set_thumb_image(img_data[0])
                    sources = re.compile(r"sources\:\[(.+?)\]").findall(video_info_link)[0]
                    try:
                        video_link = re.compile(r"file:\'(.+?)\'").findall(sources)[1]
                    except:
                        video_link = re.compile(r"file:\'(.+?)\'").findall(sources)[0]
            except:
                final_video_link = ''

        if final_video_link == '' or final_video_link == None:
            final_video_link = video_link

        video.set_stopped(False)
        video.add_stream_link(STREAM_QUAL_SD, final_video_link)
        
    except: 
        video.set_stopped(True)
    return video

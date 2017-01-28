'''
Created on Dec 24, 2011

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD, STREAM_QUAL_HD_720
from xoze.utils import http
import logging
import re

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://cdn1.iconfinder.com/data/icons/Social_Networking_Icons_PNG/PNG/Vimeo.png')
    video_host.set_name('Vimeo')
    return video_host

def retrieveVideoInfo(video_id):
    
    video_info = Video()
    video_info.set_video_host(getVideoHost())
    video_info.set_id(video_id)
    try:

        html = http.HttpClient().get_html_content(url='http://vimeo.com/' + str(video_id))
        referrerObj = re.compile('"timestamp":(.+?),"signature":"(.+?)"').findall(html)[0]
        req_sig_exp = referrerObj[0]
        req_sig = referrerObj[1]
        
        img_link = re.compile('itemprop="thumbnailUrl" content="(.+?)"').findall(html)[0]
        video_title = re.compile('"title":"(.+?)"').findall(html)[0]
        
        qual = 'sd'
        video_link = "http://player.vimeo.com/play_redirect?clip_id=%s&sig=%s&time=%s&quality=%s&codecs=H264,VP8,VP6&type=moogaloop_local&embed_location=" % (video_id, req_sig, req_sig_exp, qual)
        video_info.add_stream_link(STREAM_QUAL_SD, video_link)
        
        if(re.search('"hd":1', html)):
            qual = 'hd'
            video_link = "http://player.vimeo.com/play_redirect?clip_id=%s&sig=%s&time=%s&quality=%s&codecs=H264,VP8,VP6&type=moogaloop_local&embed_location=" % (video_id, req_sig, req_sig_exp, qual)
            video_info.add_stream_link(STREAM_QUAL_HD_720, video_link)
            
        video_info.set_stopped(False)
        video_info.set_thumb_image(img_link)
        video_info.set_name(video_title)
        
    except Exception, e:
        logging.getLogger().error(e)
        video_info.set_stopped(True)
    return video_info

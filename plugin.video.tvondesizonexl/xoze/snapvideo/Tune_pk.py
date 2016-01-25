'''
Created on Dec 24, 2011

@author: ajju
'''

from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_LOW, STREAM_QUAL_SD, \
    STREAM_QUAL_HD_720, STREAM_QUAL_HD_1080
from xoze.utils import http
import logging
import re


VIDEO_HOSTING_NAME = 'Tune.pk'

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://tune.pk/styles/tunev3/images/logo.png')
    video_host.set_name('Tune.pk')
    return video_host

def retrieveVideoInfo(video_id):
    
    video_info = Video()
    video_info.set_video_host(getVideoHost())
    video_info.set_id(video_id)
    try:
        video_info_link = 'http://embed.tune.pk/play/' + str(video_id) + '?autoplay=no'
        html = http.HttpClient().get_html_content(url=video_info_link)
        image = re.compile("preview_img = '(.+?)';").findall(html)
        if image is not None and len(image) == 1:
            video_info.set_thumb_image(str(image[0]))
        html = html.replace('\n\r', '').replace('\r', '').replace('\n', '').replace('"','').replace('\\/','/')
        sources = re.compile("{(.+?)}").findall(re.compile("sources = (.+?)]").findall(html)[0])
        for source in sources:
            video_link = str(re.compile("file:(.+?).mp4").findall(source)[0]) + '.mp4'
	    label_text = str(re.compile("label:(.+?)p").findall(source)[0]) + 'p'
            if label_text is not None and len(label_text) == 1:
                label = str(label_text[0])
                logging.getLogger().debug(label)
                if label == '240p':
                    video_info.add_stream_link(STREAM_QUAL_LOW, video_link)
                elif label == '360p' and video_info.get_stream_link(STREAM_QUAL_SD) is None:
                    video_info.add_stream_link(STREAM_QUAL_SD, video_link)
                elif label == '480p' or label == 'SD':
                    video_info.add_stream_link(STREAM_QUAL_SD, video_link)
                elif label == '720p' or label == 'HD':
                    video_info.add_stream_link(STREAM_QUAL_HD_720, video_link)
                elif label == '1080p':
                    video_info.add_stream_link(STREAM_QUAL_HD_1080, video_link)
                else:
                    video_info.add_stream_link(STREAM_QUAL_SD, video_link)
                    
            else:
                video_info.add_stream_link(STREAM_QUAL_SD, video_link)
        video_info.set_stopped(False)
        
    except Exception, e:
        logging.getLogger().error(e)
        video_info.set_stopped(True)
    return video_info

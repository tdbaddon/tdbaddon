'''
Created on Feb 10, 2012

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD
from xoze.utils import http

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://s18.postimage.org/lgklzy6s5/vplay.png')
    video_host.set_name('VPlay')
    return video_host

def retrieveVideoInfo(video_id):
    video_info = Video()
    video_info.set_video_host(getVideoHost())
    video_info.set_id(video_id)
    try:
        http.HttpClient().enable_cookies()
        html = http.HttpClient().get_html_content(url='http://www.vplay.ro/watch/' + str(video_id))
        html = http.HttpClient().get_html_content(url='http://www.vplay.ro/play/dinosaur.do', params={'key':str(video_id)})
        params = http.parse_url_params(html)
        video_link = http.get_redirected_url(url=params['nqURL'])
        http.HttpClient().disable_cookies()
        video_info.set_stopped(False)
        video_info.add_stream_link(STREAM_QUAL_SD, video_link)
        video_info.set_thumb_image(params['th'])
    except:
        video_info.set_stopped(True)
    return video_info

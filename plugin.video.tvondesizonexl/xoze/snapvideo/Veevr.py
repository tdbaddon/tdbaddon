'''
Created on Jan 3, 2012

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD
from xoze.utils import http

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://profile.ak.fbcdn.net/hprofile-ak-snc4/50313_127613750585226_4787_n.jpg')
    video_host.set_name('veevr')
    return video_host

def retrieveVideoInfo(video_id):
    
    video_info = Video()
    video_info.set_video_host(getVideoHost())
    video_info.set_id(video_id)
    try:
        video_info_link = 'http://veevr.com/embed/' + str(video_id)
        soup = http.HttpClient().get_beautiful_soup(url=video_info_link)
        thumbTag = soup.findChild('img', attrs={'id':'vid-thumb'})
        imageUrl = thumbTag['src']
        videoTitle = thumbTag['alt']
        
        vidTag = soup.findChild('img', attrs={'id':'smil-load'})
        videoUrl = vidTag['src']
        video_info.add_stream_link(STREAM_QUAL_SD, videoUrl)
        video_info.set_name(videoTitle)
        video_info.set_thumb_image(imageUrl)
        video_info.set_stopped(False)
        
    except: 
        video_info.set_stopped(True)
    return video_info


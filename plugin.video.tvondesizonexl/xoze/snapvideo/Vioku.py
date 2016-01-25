'''
Created on Dec 25, 2011

@author: ajju
'''
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('')
    video_host.set_name('Vioku')
    return video_host
    
def retrieveVideoInfo(video_id):
    
    video_info = Video()
    video_info.set_video_host(getVideoHost())
    video_info.set_id(video_id)
    try:
        
        video_link = 'http://www.vioku.com/flvideo/' + video_id
        video_info.add_stream_link(STREAM_QUAL_SD, video_link)
        video_info.set_stopped(False)
        
    except: 
        video_info.set_stopped(True)
    return video_info

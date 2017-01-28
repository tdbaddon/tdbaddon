'''
Created on Dec 24, 2011

@author: ajju
'''
from BeautifulSoup import BeautifulStoneSoup
from xoze.snapvideo import VideoHost, Video, STREAM_QUAL_SD
from xoze.utils import http

API_KEY = 'E97FCECD-875D-D5EB-035C-8EF241F184E2'

def getVideoHost():
    video_host = VideoHost()
    video_host.set_icon('http://blog.toggle.com/wp-content/uploads/2011/05/veoh_logo.png')
    video_host.set_name('Veoh')
    return video_host
    
def retrieveVideoInfo(video_id):
    
    video_info = Video()
    video_info.set_video_host(getVideoHost())
    video_info.set_id(video_id)
    try:
        video_info_link = 'http://www.veoh.com/rest/v2/execute.xml?method=veoh.video.findByPermalink&permalink=' + str(video_id) + '&apiKey=' + API_KEY
        soup = BeautifulStoneSoup(http.HttpClient().get_html_content(url=video_info_link), convertEntities=BeautifulStoneSoup.XML_ENTITIES)
        
        videoObj = soup.findChild(name='video')
        video_link = http.get_redirected_url(str(videoObj['ipodurl']))
        img_link = str(videoObj['highresimage'])
        video_title = str(videoObj['title'])
        
        video_info.set_stopped(False)
        video_info.set_thumb_image(img_link)
        video_info.set_name(video_title)
        video_info.add_stream_link(STREAM_QUAL_SD, video_link)
        
    except: 
        video_info.set_stopped(True)
    return video_info

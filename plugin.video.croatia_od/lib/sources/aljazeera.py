# -*- coding: utf-8 -*-

from lib.modules.webutils import *
import re

def yt_video_id(value):
    id=re.compile('((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)').findall(value)[0]
    return id[3]

def aj_get_eps(url):
    eps=[]
    html=read_url(url)
    soup=get_soup(url)
    lis=soup.findAll('li')
    for li in lis:
        try:
            thumb=li.find('img')['src']
            url=li.findAll('a')[1]['href']
            title=li.find('h2').getText()
            eps.append([url,thumb,title])
        except:
            pass
    try:
        next_page='http://balkans.aljazeera.net' + re.compile('<li class="pager-next"><a href="(.+?)"').findall(html)[0]
    except:
        next_page=0
    return eps,next_page

def resolve_aj(url):
    html=read_url(url)
    soup=get_soup(url)
    try:
        rreg='<param name="playerID" value="(.+?)" /><param name="@videoPlayer" value="(.+?)" />'
        ids=re.compile(rreg).findall(html)[0]
        l='http://c.brightcove.com/services/viewer/federated_f9?&width=690&height=388&flashID=bcExperienceObj0&bgcolor=%23FFFFFF&ConvivaConfig.events=%20%3CConvivaEventsMap%3E%20%3Cevent%20name%3D%22mediaPlay%22%20module%3D%22videoPlayer%22%20eventType%3D%22mediaPlay%22%3E%20%3C%2Fevent%3E%20%3Cevent%20name%3D%22mediaError%22%20module%3D%22videoPlayer%22%20eventType%3D%22mediaError%22%3E%20%3Cattr%20key%3D%22errorCode%22%20type%3D%22eventField%22%20value%3D%22code%22%2F%3E%20%3C%2Fevent%3E%20%3C%2FConvivaEventsMap%3E%20&playerID='+ids[0]+'&%40videoPlayer='+ids[1]+ '&isVid=true&isUI=true&playerKey=AQ~~%2CAAAA1DWaSzk~%2CCZSkTksiPhQqITLsbi03E4KbEIFdh_zL'
        return l
    except:
        link=soup.find('iframe',{'class':'media-youtube-player'})['src']
        yt_id= yt_video_id(link)
        video='plugin://plugin.video.youtube/play/?video_id='+yt_id
        return video    
def aj_get_meta(url):
    html=read_url(url)
    soup=get_soup(url)
    title=soup.find('h3',{'class':'title'}).getText()
    desc=re.compile('<meta property="og:description" content="(.+?)" />').findall(html)[0]
    return title,desc    
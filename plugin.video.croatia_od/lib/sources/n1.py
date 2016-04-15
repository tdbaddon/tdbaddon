# -*- coding: utf-8 -*-
from lib.modules.webutils import *

def n1_shows():
    emisije=[['Pressing','http://hr.n1info.com/a3525/TV-Emisije/Pressing/Pressing.html','http://i.imgur.com/3nm5bcu.jpg'],
    ['Dnevnik u 19','http://hr.n1info.com/a3658/TV-Emisije/Dnevnik-u-19/Dnevnik-u-19h.html','http://i.imgur.com/LeS4fXI.jpg']]
    return emisije
def yt_video_id(value):
    id=re.compile('((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)').findall(value)[0]
    return id[3]
def get_n1_eps(url):
    html=read_url(url)
    soup=bs(html)
    tag=soup.find('div',{'data-ajax-param':'Epizode'})
    eps=tag.findAll('article')
    out=[]
    for ep in eps:
        url=ep.find('a')['href']
        thumb=ep.find('img')['src']
        title=ep.find('h1').getText()
        out+=[[title,url,thumb]]

    return out
def resolve_n1(url):
    html=read_url(url)
    soup=bs(html)
    video=soup.find('iframe')['src']
    if 'youtube' in video:
        yt_id= yt_video_id(video)
        video='plugin://plugin.video.youtube/play/?video_id='+yt_id
    return video

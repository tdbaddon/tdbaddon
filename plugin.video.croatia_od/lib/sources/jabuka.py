# -*- coding: utf-8 -*-
from lib.modules.webutils import *


def convert(string):

    string=string.replace('%3A',':')
    string=string.replace('%3B',';')
    string=string.replace('%3C','<')
    string=string.replace('%3D','=')
    string=string.replace('%3E','>')
    string=string.replace('%3F','?')
    string=string.replace('%3D','=')
    string=string.replace('%3d','=')
    string=string.replace('%2A','*')
    string=string.replace('%2B','+')
    string=string.replace('%2C',',')
    string=string.replace('%2D','-')
    string=string.replace('%2E','.')
    string=string.replace('%2F','/')
    string=string.replace('%26','&')
    string=string.replace('%23','#')
    string=string.replace('%25','%')
    string=string.replace('%40','@')
    return string


def get_video_links_from_jabuka_show(show):
    soup=get_soup(show)
    tag=soup.findAll('div',{'class':'media-details-view'})[0]
    h2s=tag.findAll('h2')
    linksout=[]
    for i in range(len(h2s)):
        title=h2s[i]['title']
        link='http://videoteka.jabukatv.hr'+(h2s[i].findAll('a')[0]['href'])
        title=title.replace(':','')
        linksout+=[[link,title]]
    
    return linksout

def resolve_otv_link(link):
    soup=get_soup(link)
    tag=soup.findAll('meta',{'property':'og:video:url'})[0]['content']
    
    link=convert(tag)
    index=link.index('file=')
    link=link[index+5:]
    return(link)

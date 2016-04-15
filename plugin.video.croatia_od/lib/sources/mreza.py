# -*- coding: utf-8 -*-
from lib.modules.webutils import *

def get_shows_mreza(tagy):
    url='http://mreza.tv/video/'
    shows=[]
    
    soup=get_soup(url)

    tag=soup.find("div", {"id":"wrapper-glavni"})
    tag=tag.find("section",{"class":"%s"%tagy})
   
    pom=tag.findAll("li")
    for i in range(len(pom)):
        pomy=pom[i].find("a")
        ime=pom[i].findAll('a')[1]['title']
        link=pomy['href']
        img=pom[i].find('img')['src']
        shows+=[[link,ime,img]]
    return shows
def normal(string):
    string=string.replace('Š','S').replace('Ž','Z').replace('Č','C').replace('Ć','C').replace('Đ','D')
    return string.replace('š','s').replace('ž','z').replace('č','c').replace('ć','c').replace('đ','d')
def get_episodes_mreza(url):
    
    reg1='"title":"(.+?)"'
    pat1=re.compile(reg1)

    reg2='"file":"(.+?)"'
    pat2=re.compile(reg2)

    reg3='"image":"(.+?)"'
    pat3=re.compile(reg3)

    return_lista=[]
    html=read_url(url)
    
    titles=re.findall(pat1,html)
    links=re.findall(pat2,html)
    images=re.findall(pat3,html)
    for i in range(len(titles)):
        title=normal(titles[i])
        link=str(links[i])
        image=str(images[i])
        return_lista+=[[link,title,image]]

    return return_lista


# -*- coding: utf-8 -*-
from lib.modules.webutils import *

def get_shows_movinized(url):
    soup=get_soup(url)
    table=soup.find('div',{'class':'td-ss-main-content'})
    link_tab=table.findAll('h4')
    pics=table.findAll('p')
    shows=[]
    for i in range(len(link_tab)):
        try:
            link=link_tab[i].find('a')['href']
            title=link_tab[i].find('a').getText().lower().title()
            img=pics[i].find('a')['href']
            if 'cat' in img:
                img='http:' +pics[i].find('img')['src']

            shows+=[[link,title,img]]
        except:
            pass
    return shows

def get_movienized_eps(url,next):
    soup=get_soup(url)
    tag=soup.findAll('div',{'class':'td-pb-row'})[1]

    lis=tag.findAll('div',{'class':'td-module-thumb'})
    eps=[]
    if next==0:
        for li in lis:
            link=li.find('a')['href']
            title=li.find('a')['title']
            img='http:'+ li.find('img')['src']
            eps+=[[link,title,img]]

    tag=soup.find('div',{'class':'td-pb-span8 td-main-content'})
    lis=tag.findAll('div',{'class':'td-module-thumb'})
    for li in lis:
        link=li.find('a')['href']
        title=li.find('a')['title']
        img='http:'+ li.find('img')['src']
        eps+=[[link,title,img]]
    try:
        next_page=soup.find('span',{'class':'current'}).findNext('a')['href']
        clasa=soup.find('span',{'class':'current'}).findNext('a')['class']
        if clasa!='page':
            raise
    except:
        next_page='0'

    return eps,next_page

def get_movinized_ep(url):
    soup=get_soup(url)
    try:
        reg='value="baseW=http://movienized.com&id=(.+?)"'
        id=re.compile(reg).findall(html)
        id=id[0]
        url1='http://movienized.com/?view=config&wid=%srxx/'%id
        htm=read_url(url1)
        reg2='<playListXml>(.+?)</playListXml>'
        url2=re.compile(reg2).findall(htm)[0]
        htmm=read_url(url2)
        reg3='<video>(.+?)</video>'
        link=[re.compile(reg3).findall(htmm)[0]]
        title=re.compile('<title>(.+?)</title>').findall(htmm)[0]
        thumb=re.compile('<preview>(.+?)</preview>').findall(htmm)[0]

        return title,link,thumb
    except:
        title=soup.find('title').getText().replace(' | Movienized','')
        # links=re.compile('<(?:iframe|IFRAME) (?:src|SRC)="(.+?)"').findall(html)
        # for link in links:
        #     if 'dailymotion' in link:
        #         linky='http:'+ link
        #         ind=linky.index('?')
        #         linky=linky[:ind]
        #         break
        links=[]
        frames=soup.findAll('iframe',{'allowfullscreen':''})
        try:
            il=frames[0]
        except:
            frames=soup.findAll('iframe')
        if len(frames)>1:
            for frame in frames:
                if 'facebook' not in frame['src']:
                    link='http:' + frame['src']

                    links+=[link]
        else:

            if u'facebook' not in frames[0]['src']:
                link='http:' + frames[0]['src']
            
            
                links+=[link]

        thumb='none'
        return title,links,thumb
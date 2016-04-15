# -*- coding: utf-8 -*-
from lib.modules.webutils import *
import urllib2


def resolve_rtl_link(link):
    end_url='?domain=www.rtl.hr&xml=1'
    link=link+end_url
    try:
        resp = urllib2.urlopen(link)
        contents = resp.read()
    except urllib2.HTTPError, error:
        contents = error.read()
    html=contents
    
    sp=bs(html)
    vid=sp.findAll('video')[0]
    link=vid.getText()
    return link





def get_all_show_rtl():
    url='http://www.sada.rtl.hr/programi/'
    soup=get_soup(url)
    lis=soup.findAll('li')
    shows=[]
    for li in lis:
        try:
            title=li.find('p',{'class':'News-title'}).getText()
            url=li.find('a')['href']
            try:
                img=li.find('picture').find('img')['srcset']
            except:
                img=li.find('picture').find('img')['data-srcset']
            if 'http' not in img:
                img='http://www.sada.rtl.hr'+img
            shows+=[[title,url,img]]
        except:
            pass
    return shows

def rtl_get_cats():
    url='http://www.sada.rtl.hr/programi/?group=category'
    soup=get_soup(url)
    lis=soup.findAll('h2',{'class':'h-4 Container-title'})
    cats=[]
    for li in lis:
        name=li.getText()
        id=li['id']

        cats+=[[name,id]]
    return cats

def rtl_get_chans():
    url='http://www.sada.rtl.hr/programi/?group=channel'
    soup=get_soup(url)
    lis=soup.findAll('h2',{'class':'h-4 Container-title'})
    cats=[]
    for li in lis:
        name=li.getText()
        id=li['id']

        cats+=[[name,id]]
    return cats
def rtl_get_from_chan(id):
    url='http://www.sada.rtl.hr/programi/?group=channel'
    soup=get_soup(url)
    lis=soup.find('h2',{'class':'h-4 Container-title', 'id':id}).findNext('ul').findAll('li')
    shows=[]
    for li in lis:
        try:
            title=li.find('p',{'class':'News-title'}).getText()
            url=li.find('a')['href']
            try:
                img=li.find('picture').find('img')['srcset']
            except:
                img=li.find('picture').find('img')['data-srcset']
            if 'http' not in img:
                img='http://www.sada.rtl.hr'+img
            shows+=[[title,url,img]]
        except:
            pass
    return shows
def rtl_get_from_cat(id):
    url='http://www.sada.rtl.hr/programi/?group=category'
    soup=get_soup(url)
    lis=soup.find('h2',{'class':'h-4 Container-title', 'id':id}).findNext('ul').findAll('li')
    shows=[]
    for li in lis:
        try:
            title=li.find('p',{'class':'News-title'}).getText()
            url=li.find('a')['href']
            try:
                img=li.find('picture').find('img')['srcset']
            except:
                img=li.find('picture').find('img')['data-srcset']
            if 'http' not in img:
                img='http://www.sada.rtl.hr'+img
            shows+=[[title,url,img]]
        except:
            pass
    return shows

def rtl_get_it(url):
    soup=get_soup(url)
    lis=soup.findAll('li')
    shows=[]
    for li in lis:
        try:
            title=li.find('p',{'class':'News-title'}).getText()
            subtitle=li.find('p',{'class':'News-title'}).findNext('p').getText().strip()
            try:
                episode=li.find('span',{'class':'Catchup-episodeTitle'}).getText().strip()
                subtitle=subtitle.replace(episode,'')
                subtitle='%s %s'%(subtitle,episode)
            except:
                pass

            if subtitle!='':
                title='%s (%s)'%(title,subtitle)
            url=li.find('a')['href']
            try:
                img=li.find('picture').find('img')['srcset']
            except:
                img=li.find('picture').find('img')['data-srcset']
            if 'http' not in img:
                img='http://www.sada.rtl.hr'+img
            try:
       
                regex='style="background-image: url((.+?))"'
                imgg=re.findall(re.compile(regex),unicode(soup))[0]
                imgg=imgg[0].replace('(','').replace(')','')
            except:
                imgg=''
            shows+=[[url,title,img,imgg]]

        except:
            pass
    return shows

def rtl_get_new():
    url='http://www.sada.rtl.hr'
    soup=get_soup(url)
    lis=soup.findAll('li')
    shows=[]
    for li in lis:
        try:
            title=li.find('p',{'class':'News-title'}).getText()
            subtitle=li.find('p',{'class':'News-title'}).findNext('p').getText().strip()
            try:
                episode=li.find('span',{'class':'Catchup-episodeTitle'}).getText().strip()
                subtitle=subtitle.replace(episode,'')
                subtitle='%s %s'%(subtitle,episode)
            except:
                pass

            title='%s (%s)'%(title,subtitle)
            url=li.find('a')['href']
            try:
                img=li.find('picture').find('img')['srcset']
            except:
                img=li.find('picture').find('img')['data-srcset']
            if 'http' not in img:
                img='http://www.sada.rtl.hr'+img
            try:
       
                regex='style="background-image: url((.+?))"'
                imgg=re.findall(re.compile(regex),unicode(soup))[0]
                imgg=imgg[0].replace('(','').replace(')','')
            except:
                imgg=''
            shows+=[[url,title,img,imgg]]

        except:
            pass
    return shows

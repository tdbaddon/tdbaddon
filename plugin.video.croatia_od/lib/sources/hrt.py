# -*- coding: utf-8 -*-

from lib.modules.webutils import *
import re
import itertools


def hrt_get_shows_letter(letter):#=====>  vraca listu tipa likovi[index]=[link_emisije[index],ime_emisije[index]]
        br=0
        linksout = []
        soup=get_soup('http://www.hrt.hr/enz/dnevnik/')
        tag = soup.find("div", {"class":"all_shows"})
        if letter=='Š':
            letters=tag.find('ul',{'data-letter':'S'})
            letters=letters.findNext('ul')
        else:   letters=tag.find('ul',{'data-letter':'%s'%letter})


        emisija=[None]*len(letters)
        emisije=[None]*200
        name=[None]*200
        
        emisije_tags=letters.findAll('li')
        
        for j in range(len(emisije_tags)):
            css=emisije_tags[j].findAll('a')
            for a in css:
                    link=a['href']
                    br+=1
                    link='http:'+link
                    emisije[br]=link
                    name[br]=emisije_tags[j].getText()
               
                
        emisije = [x for x in emisije if x != None]
        name = [x for x in name if x != None]
        linkovi=[None]*len(emisije)
        for g in range(len(emisije)):
            linkovi[g]=[emisije[g],name[g]]
        
        return linkovi


def hrt_get_all():
    linksout,br = [],0
    soup=get_soup('http://www.hrt.hr/enz/dnevnik/')
    tag = soup.find("div", {"class":"all_shows"})
    emisije_tags=tag.findAll('li')
    emisije=[None]*1000
    name=[None]*1000
    for j in range(len(emisije_tags)):
        css=emisije_tags[j].findAll('a')
        for a in css:
            link=a['href']
            br+=1
            link='http:'+link
            emisije[br]=link
            name[br]=emisije_tags[j].getText()
    emisije = [x for x in emisije if x != None]
    name = [x for x in name if x != None]
    linkovi=[None]*len(emisije)
    for g in range(len(emisije)):
        linkovi[g]=[emisije[g],name[g]]
    
    return linkovi
               
def get_episodes_hrt(link,broj_rez): #======> vraca listu tipa linkovi[0]=[link_epizode[0],ime_epizode[0]]
        reg='value="(.+?)"'
        pattern=re.compile(reg)
        reg2='">(.+?)<option value='
        pattern2=re.compile(reg2)
        

        try:
            soup=get_soup(link)
        except urllib2.HTTPError, e:
            return []
            
    
       

        tag = soup.find("table", {"class":"show_info"})
        eps=tag.findAll('select')
        gg=eps[0]
            
        stri=str(gg)
        
        br=0
        br1=0
        values=[None]*(int(broj_rez)+1)
        names=[None]*(int(broj_rez)+1)
        for m in itertools.islice(re.finditer(pattern, stri), (int(broj_rez)+1)):
            values[br]=m.group(1)
            br+=1
        for v in itertools.islice(re.finditer(pattern2, stri), (int(broj_rez)+1)):
            names[br1]=v.group(1)
            br1+=1
        
        values = [x for x in values if x is not None]
        values.pop()
        names = [x for x in names if x is not None]
        
        
        

        
        epizoda=[None]*len(values)
        linkovi=[None]*len(values)
        
        for f in range(len(values)):
            epizoda[f]=link+values[f]
            linkovi[f]=[epizoda[f],names[f]]
        
        if len(values)==0:
            return '123445'
        return linkovi

       # except:
        #    return ('No episodes available')

def get_show_name(url):
    soup=get_soup(url)
    return soup.find('td',{'class':'show_name'}).getText()

def get_episode_link(link):                #====> vraca .mp4 link
        soup=get_soup(link)
        
        tag=soup.find("video")
        try:
            linka=tag['data-url']
        except:
            try:
                linka=tag['src']
            except:
                linka=tag['data-src']

        return linka
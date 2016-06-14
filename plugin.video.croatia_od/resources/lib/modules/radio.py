# -*- coding: utf-8 -*-
from resources.lib.modules import webutils,client
import re

def get_links_country(link):


    reg='<a href="(.+?)"'
    pattern=re.compile(reg)
    reg2='<b>(.+?)</b>'
    pattern2=re.compile(reg2)
    site = "http://www.listenlive.eu/"+link+".html"
    html = client.request(site)
    soup = webutils.bs(html)
    table = soup.find("div", {"class":"thetable3"})
    tab=table.findAll('tr')

    stanice=[None]*(len(tab)+1)
    for i in range (len(tab)):
        stanice[i] =tab[i].findAll('td')
    
    links=[None]*(len(stanice)+1)
    imena=[None]*(len(stanice)+1)
    imenak=[None]*(len(stanice)+1)
    gradovi=[None]*(len(stanice)+1)
    lk=[None]*(len(stanice)+1)
    imena_st=[None]*(len(stanice)+1)
    linksout=[None]*600
    linkk=''
    grad=''
    for i in range (len(stanice)-1):
        links[i]=stanice[i][3]
        link=str(links[i])
        link=re.findall(pattern,link)
        
        if (i!=0):
            linkk=link[0]
        imena[i]=stanice[i][0]
        imenak[i]=stanice[i][3]
        gradovi[i]=stanice[i][1]
        if i!=0:
            grad=gradovi[i].getText().encode('utf-8')
        imena[i]=str(imena[i])
        ime=re.findall(pattern2,imena[i])
        #imenak[i]=str(imenak[i])
        kvaliteta=imenak[i].getText()
        if kvaliteta=='WebPlayer':
            kvaliteta='64 Kbps'
        if kvaliteta.count('Kbps')>1:
            a=kvaliteta.index('Kbps')
            kvaliteta=kvaliteta[:a+4]
        if '>' in ime[0]:
            l=len(ime[0])
            g=ime[0].index('>')
            ime[0]=ime[0][g+1:l]
        if '>' in ime[0]:
            l=len(ime[0])
            g=ime[0].index('>')
            ime[0]=ime[0][g+1:l].encode('utf-8')
        
        linksout += [[linkk, ime[0].decode('utf-8'),kvaliteta,grad.decode('utf-8')]]
    
    del linksout[0]
    del linksout[0]
    linksout=[x for x in linksout if x !=None]

    linksout+=get_additional()
    return linksout

def get_additional():
    url='https://github.com/natko1412/cod/raw/master/radio.txt'
    html=client.request(url)
    regex=re.compile("\[\'(.+?)\'\s*,\s*\'(.+?)\'\s*,\s*\'(.+?)\'\s*,\s*\'(.+?)\'\]")

    items=re.findall(regex,html)
    return items
# -*- coding: utf-8 -*-
from lib.modules.webutils import *
from lib.modules import client


def get_izet():
    
    lista=[]
    html=client.request('http://zbunjenludnormalan.blogspot.com')
    soup=bs(html)
    list=soup.findAll('li')

    for i in range(len(list)):
        try:
            link=list[i].find('a')['href']
            name=list[i].getText()
            if 'Sve epizode' not in name and 'uloge' not in name:
                num=int(name.replace('Epizoda ','').replace('LZN ',''))
                lista+=[[link,name,num]]
        except:
            pass
    
    lista=sorted(lista, key = lambda x: x[2],reverse=True)
    return lista

def get_izet_video(url):
    html=read_url(url)

    try:
        reg="<(?:iframe|IFRAME).+?(?:src|SRC)=(?:'|\")(.+?)(?:'|\")"
        listy=re.findall(re.compile(reg),html)[0]
    except:

        reg="<IFRAME SRC='(.+?)'"
        listy=re.findall(re.compile(reg),html)[0]
    return listy
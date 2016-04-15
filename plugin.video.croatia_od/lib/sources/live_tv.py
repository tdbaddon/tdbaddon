
# -*- coding: utf-8 -*-
from lib.modules.webutils import *
import xbmc,xbmcgui,xbmcaddon
import os

my_addon = xbmcaddon.Addon()
addon_path = my_addon.getAddonInfo('path')
addon_id= my_addon.getAddonInfo('id')
zipPath = xbmc.translatePath("special://profile/addon_data/"+addon_id)
zipFile= os.path.join(zipPath,'data.zip')

def resolve_live(url,title):
    if 'm3u8' in url or 'rtmp' in url or 'flv' in url or 'mp4' in url:
        return url
    elif 'sipragezabava' in url or 'netraja' in url:
        return resolve_siprage(url)
    
    elif 'lshstream' in url:
        from lib.resolvers import lshunter
        return lshunter.resolve(url)
    elif 'abcast' in url:
        from lib.resolvers import abcast
        return abcast.resolve(url)
    elif 'filmon' in url:
        from lib.resolvers import filmon
        return filmon.resolve(url)
    elif 'hdcast' in url:
        from lib.resolvers import hdcast
        return hdcast.resolve(url)
    elif 'sawlive' in url:
        from lib.resolvers import sawlive
        return sawlive.resolve(url)
    elif 'vaughn' in url:
        from lib.resolvers import vaughnlive
        return vaughnlive.resolve(url)
    elif 'p2pcast' in url:
        from lib.resolvers import p2pcast
        return p2pcast.resolve(url)
    elif 'veetle' in url:
        from lib.resolvers import veetle
        return veetle.resolve(url)
    elif 'mybeststream' in url:
        from lib.resolvers import mybeststream
        return mybeststream.resolve(url)
    elif 'dailymotion' in url:
        from lib.resolvers import dailymotion
        return dailymotion.resolve(url)
    elif 'youtube' in url:
        from lib.resolvers import youtube
        return youtube.resolve(url)
    elif 'acestream://' in url or 'sop://' in url:
        from lib.resolvers import sop_ace
        return sop_ace.resolve(url,title)
    elif 'serbiaplus' in url:
        from lib.sources import serbiaplus
        return serbiaplus.resolve_serbiaplus(url,title)


    else:
        try:
            return resolve_siprage(url)
        except:
            return url
    return url
def resolve_siprage(url):
    try:
        soup=get_soup(url)
        try:
            link=soup.find('embed',{'id':'vlc'})
            link=link['target']

        except:
            link=soup.find('embed',{'name':'vlc'})
            link=link['target']            
    except:
        link=url
    return link

def get_current_epg(id):
    from datetime import datetime,timedelta
    now = datetime.now()
    year,month,day,hour,minute,seconds=now.strftime("%Y"),now.strftime("%m"),now.strftime("%d"),now.strftime("%H"),now.strftime("%M"),now.strftime("%S")
    date='%s.%s.%s.'%(day,month,year)
    if int(hour)<7:
        yesterday=datetime.now() - timedelta(days=1)
        year,month,dayy= yesterday.strftime("%Y"),yesterday.strftime("%m"),yesterday.strftime("%d")
        date='%s.%s.%s.'%(dayy,month,year)
    url='http://mojtv.hr/xmltv/service.ashx?kanal_id=%s&date=%s'%(id,date)
    if '.xml' in id:
        url=id
    from lib.modules import cache
    channel_xml=cache.get(read_url,12,url)

    reg='<programme channel=".+?" start="(.+?)" stop="(.+?)">\s*<title>(.*?)<\/title>'
    infos=re.findall(reg,channel_xml)
    
    time_now=int('%s%s%s%s%s%s'%(year,month,day,hour,minute,seconds))
    title='Nema informacija'
    for info in infos:
        start = int(re.sub('\s\+\d{4}', '', info[0]))
        stop = int(re.sub('\s\+\d{4}', '', info[1]))
        

        if start<=time_now and stop>=time_now:
            title = info[2].decode('utf-8')
            break
        
    
    return title

def get_epg(id):
    from datetime import datetime,timedelta
    now = datetime.now()
    year,month,day,hour,minute,seconds=now.strftime("%Y"),now.strftime("%m"),now.strftime("%d"),now.strftime("%H"),now.strftime("%M"),now.strftime("%S")
    if int(hour)<8:
        yesterday=datetime.now() - timedelta(days=1)
        year,month,day= yesterday.strftime("%Y"),yesterday.strftime("%m"),yesterday.strftime("%d")
    date='%s.%s.%s.'%(day,month,year)
    
    url='http://mojtv.hr/xmltv/service.ashx?kanal_id=%s&date=%s'%(id,date)
    if '.xml' in id:
        url=id
    from lib.modules import cache
    channel_xml=cache.get(read_url,12,url)
    epg=''
    reg='<programme channel=".+?" start="(.+?)" stop="(.+?)">\s*<title>(.*?)<\/title>'
    infos=re.findall(reg,channel_xml)
    for info in infos:
        
        start=re.sub('00\s\+\d{4}', '', info[0])[8:]
        stop=re.sub('00\s\+\d{4}', '', info[1])[8:]

        start_hour,start_minute=start[:2],start[2:]
        stop_hour,stop_minute=stop[:2] ,stop[2:]
    

        title = info[2].decode('utf-8')

        epg+='\n(%s:%s - %s:%s) %s\n'%(start_hour,start_minute,stop_hour,stop_minute,title)
    return epg

def present_epg(heading,anounce):
    class TextBox():

            """Thanks to BSTRDMKR for this code:)"""
            WINDOW=10147; CONTROL_LABEL=1; CONTROL_TEXTBOX=5 # constants
            def __init__(self,*args,**kwargs):
                xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW,)) # activate the text viewer window
                self.win=xbmcgui.Window(self.WINDOW) # get window
                xbmc.sleep(500) # give window time to initialize
                self.setControls()
            def setControls(self):
                self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
                try: f=open(anounce); text=f.read()
                except: text=anounce
                self.win.getControl(self.CONTROL_TEXTBOX).setText(text); return
    TextBox()



def search_m3u(query,shows):
    words=query.lower().split(' ')
    br=0
    pom=0
    out=[]
    for show in shows:

        for word in words:
            try:
                if word in show.title.lower():
                    br+=1
            except:
                pass

        if br>0:
            tup=(br,pom)
            out.append(tup)
        br=0
        pom+=1
    from operator import itemgetter
    out=sorted(out,key=lambda x: x[0], reverse=True)
    outt=[]
    for i in range(len(out)):
        outt+=[shows[out[i][1]]]

    return outt

def get_current_bleb(id):
    from datetime import datetime,timedelta
    now = datetime.now() - timedelta(hours=1)
    year,month,day,hour,minute,seconds=now.strftime("%Y"),now.strftime("%m"),now.strftime("%d"),now.strftime("%H"),now.strftime("%M"),now.strftime("%S")
    
    id=id.replace('bleb-','')
    url='http://bleb.org/tv/data/listings?days=-1,0,1&format=XMLTV&channels=' + id
    import urllib
    urllib.urlretrieve (url, zipFile)
    import zipfile
    file = zipfile.ZipFile(zipFile, "r")
    channel_xml = file.read('data.xml')
    epg=''
    reg='<programme start="(.+?)" stop="(.+?)" channel=".+?">\s*<title lang="en">(.*?)<\/title>'
    infos=re.findall(reg,channel_xml)
    time_now=int('%s%s%s%s%s%s'%(year,month,day,hour,minute,seconds))
    title='Nema informacija'
    for info in infos:
        start=int(re.sub('\s\+\d{4}', '', info[0]))
        stop=int(re.sub('\s\+\d{4}', '', info[1]))
        
        if start<=time_now and stop>=time_now:
            title = info[2].decode('utf-8')
            break
        
    
    return title

def get_epg_bleb(id):
    id=id.replace('bleb-','')
    url='http://bleb.org/tv/data/listings?days=0&format=XMLTV&channels=' + id
    import urllib
    urllib.urlretrieve (url, zipFile)
    import zipfile
    file = zipfile.ZipFile(zipFile, "r")
    channel_xml = file.read('data.xml')
    reg='<programme start="(.+?)" stop="(.+?)" channel=".+?">\s*<title lang="en">(.*?)<\/title>'
    epg=''
    infos=re.findall(reg,channel_xml)
    for info in infos:
        start=re.sub('\s\+\d{4}', '', info[0])[8:]
        stop=re.sub('\s\+\d{4}', '', info[1])[8:]
        start_hour,start_minute=int(start[:2]),int(start[2:])
        stop_hour,stop_minute=int(stop[:2]) ,int(stop[2:])
        start_hour=start_hour+1
        stop_hour=stop_hour+1
        title = info[2].decode('utf-8')

        epg+='\n(%02d:%02d - %02d:%02d) %s\n'%(start_hour,start_minute,stop_hour,stop_minute,title)
    return epg

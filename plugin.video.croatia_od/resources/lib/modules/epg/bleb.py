
# -*- coding: utf-8 -*-
from resources.lib.modules.webutils import *
from resources.lib.modules.log_utils import log
from resources.lib.modules import cache,control
import xbmc,xbmcgui,xbmcaddon
import os

addon_path = control.addonPath
zipPath = control.dataPath
zipFile= os.path.join(zipPath,'data.zip')

def get_current_epg(id):
    from datetime import datetime,timedelta
    import time
    now = time.gmtime()
    now = datetime.fromtimestamp(time.mktime(now))
    year,month,day,hour,minute,seconds=now.strftime("%Y"),now.strftime("%m"),now.strftime("%d"),now.strftime("%H"),now.strftime("%M"),now.strftime("%S")
    
    url='http://bleb.org/tv/data/listings?days=-1,0,1&format=XMLTV&channels=' + id
    channel_xml = cache.get(get_xmll,36,url)
    epg=''
    reg='<programme start="(.+?)" stop="(.+?)" channel=".+?">\s*<title lang="en">(.*?)<\/title>'
    infos=re.findall(reg,channel_xml)
    time_now=int('%s%s%s%s%s%s'%(year,month,day,hour,minute,seconds))
    title='Nema informacija'
    for info in infos:
        start = eval(info[0].replace('+0100','+ 10000').replace('+','-'))
        stop =  eval(info[1].replace('+0100','+ 10000').replace('+','-'))
        
        if start<=time_now and stop>=time_now:
            title = info[2].decode('utf-8')
            break
        
    
    return title

def get_xmll(url):
    import urllib
    urllib.urlretrieve (url, zipFile)
    import zipfile
    file = zipfile.ZipFile(zipFile, "r")
    channel_xml = file.read('data.xml')
    return channel_xml


# -*- coding: utf-8 -*-
from resources.lib.modules.webutils import *
from resources.lib.modules.log_utils import log
from resources.lib.modules import cache,control
import os

def get_current_epg(id):
    categ,id = id.split(',')


    from datetime import datetime,timedelta
    import time
    now = time.gmtime()
    now = datetime.fromtimestamp(time.mktime(now))
    year,month,day,hour,minute,seconds = now.strftime("%Y"),now.strftime("%m"),now.strftime("%d"),now.strftime("%H"),now.strftime("%M"),now.strftime("%S")
    
    url = 'https://www.mts.rs/tv/mtstv/epg/Tv/%s/%s-%s-%s'%(categ,day.lstrip('0'),month.lstrip('0'),year)

    channel_xml = cache.get(client.request,10000,url)
    channels = client.parseDOM(channel_xml,'div',attrs={'class':'program-id'})
    i = 0
    for c in channels:
        x = client.parseDOM(c,'aside')[1]
        current_id = re.findall('<span>(\d+)<',x)[0]

        if current_id==id:
            channel_xml = channels = client.parseDOM(channel_xml,'div',attrs={'class':'schedule'})[i]
            break
        i += 1

    epg = ''
    reg = 'time[\"\']>([^-]+)-([^<]+).+\s*.+name[\"\']>([^<]+)'
    infos = re.findall(reg,channel_xml)
    time_now = int(hour)*60 + int(minute) + 60
    title='Nema informacija'
    for info in infos:
        ss = info[0].strip().split(':')
        ee = info[1].strip().split(':')

        start = int(ss[0])*60 + int(ss[1])
        stop = int(ee[0])*60 + int(ee[1])
        
        if start <= time_now and stop>=time_now:
            title = info[2].strip()
            break
        
    
    return title



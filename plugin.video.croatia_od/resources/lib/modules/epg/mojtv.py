
# -*- coding: utf-8 -*-
from resources.lib.modules import cache,client
from resources.lib.modules.log_utils import log
import re

def get_current_epg(id):
    from datetime import datetime,timedelta
    import time
    now = time.gmtime()
    now = datetime.fromtimestamp(time.mktime(now))
    year,month,day,hour,minute,seconds=now.strftime("%Y"),now.strftime("%m"),now.strftime("%d"),now.strftime("%H"),now.strftime("%M"),now.strftime("%S")
    date='%s.%s.%s.'%(day.lstrip('0'),month.lstrip('0'),year)
    if int(hour)<7:
        yesterday=datetime.now() - timedelta(days=1)
        year,month,dayy= yesterday.strftime("%Y"),yesterday.strftime("%m"),yesterday.strftime("%d")
        date='%s.%s.%s.'%(dayy.lstrip('0'),month.lstrip('0'),year)

    url='http://mojtv.hr/xmltv/service.ashx?kanal_id=%s&date=%s'%(id,date)
    if '.xml' in id:
        url=id
    channel_xml=cache.get(client.request,12,url)
    
    reg='<programme channel=".+?" start="(.+?)" stop="(.+?)">\s*<title>([^<]+)<\/title>'
    infos=re.findall(reg,channel_xml)

    time_now=int('%s%s%s%s%s%s'%(year,month,day,hour,minute,seconds))

    title='Nema informacija'
    for info in infos:
        start = eval(info[0].replace('+0200','+ 10000').replace('+','-'))
        stop =  eval(info[1].replace('+0200','+ 10000').replace('+','-'))
        if start<=time_now and stop>=time_now:

            title = info[2].decode('utf-8').strip()
            break
        
    
    return title

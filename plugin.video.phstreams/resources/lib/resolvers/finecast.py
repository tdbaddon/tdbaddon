# -*- coding: utf-8 -*-


import re,urlparse,urllib
from resources.lib.libraries import client
from resources.lib.libraries import jsunpack

def resolve(url):
    try:
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer=url
        id = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
        url = 'http://www.finecast.tv/embed4.php?u=%s&vw=640&vh=450'%id
        result = client.request(url, referer=referer)
        unpacked = ''
        packed = result.split('\n')
        for i in packed: 
            try: unpacked += jsunpack.unpack(i)
            except: pass
        result += unpacked
        result=result.replace('"+"','+').replace('+"','+').replace('"+','+')
        var = re.compile('var\s(.+?)\s*=\s*(?:\'|\"|\s*)(.+?)(?:\'|\"|\s*);').findall(result)
        result = re.sub(r"'(.+?)'", r'\1', result)

        rtmp=re.findall('file:\s*(.+?),',result)[0]
        m3u8=re.findall('file:\s*(.+?),',result)[1]
        
        #url = m3u8 + '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': referer})
        url = rtmp + ' swfUrl=http://www.finecast.tv/player6/jwplayer.flash.swf flashver=WIN\2019,0,0,185 live=1 timeout=14 swfVfy=1 pageUrl=http://www.finecast.tv/'

        for i in range(100):
            for v in var: result = result.replace('+%s+' % v[0], v[1])
            for v in var: result = result.replace('%s+' % v[0], v[1])
            for v in var: result = result.replace('+%s' % v[0], v[1])
        var = re.compile('var\s(.+?)\s*=\s*(?:\'|\"|\s*)(.+?)(?:\'|\"|\s*);').findall(result)
        for i in range(100):
            for v in var: url = url.replace('+%s+' % v[0], v[1])
            for v in var: url = url.replace('%s+' % v[0], v[1])
            for v in var: url = url.replace('+%s' % v[0], v[1])
        
        return url
    except:
        return



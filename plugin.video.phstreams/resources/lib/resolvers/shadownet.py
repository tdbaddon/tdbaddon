# -*- coding: utf-8 -*-


import re,urlparse,urllib
from resources.lib.libraries import client



def resolve(url):
    try:
        
        result = client.request(url)
        iframe = client.parseDOM(result, 'div', attrs = {'class': 'player.+?'})
        iframe = client.parseDOM(iframe, 'iframe', ret='src')[-1]
        result = client.request(iframe, referer=url)
        source = client.parseDOM(result, 'source', ret='src', attrs = {'type': 'video.+?'})[-1]
        if source == "#":source = re.findall("src : '(.+?)'",result)[0]
        result = client.request(source, referer=iframe)
        url = re.compile('(http.+?)\n').findall(result)[-1]
       
        return url
    except:
        return None


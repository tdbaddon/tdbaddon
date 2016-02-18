from resources.lib.modules import client
from resources.lib.modules import cloudflare
import re,sys,urllib,urlparse,base64,urllib2


domains = ['iptvlinks.tk']


def resolve(url):
    try:
        result = cloudflare.request(url)
       
        items = client.parseDOM(result, 'video', attrs={'id': 'player'})
           
        items = client.parseDOM(items, 'source', ret='src')[1]
        if ('http') in items: return items
        if items[0]!='/':
            url='http://www.iptvlinks.tk/'+items
        else:
            url='http://www.iptvlinks.tk'+items
     
        return url
    except:
        return None

from resources.lib.modules import client
from resources.lib.modules import cloudflare
import re,sys,urllib,urlparse,base64,urllib2


domains = ['stream4free.pro', 'stream4free.eu']


def resolve(url):

    try:
        result = cloudflare.request(url)
        items = client.parseDOM(result, 'video', attrs={'id': 'live_player'})
        url = client.parseDOM(items, 'source', ret='src')[0]
        if ('http') in url: return url+'|User-Agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
    except:
        return None

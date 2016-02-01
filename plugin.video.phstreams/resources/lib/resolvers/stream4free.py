from resources.lib.libraries import client
from resources.lib.libraries import cloudflare
import re,sys,urllib,urlparse,base64,urllib2


def resolve(url):

    try:
        result = cloudflare.request(url)
        items = client.parseDOM(result, 'video', attrs={'id': 'live_player'})
        url = client.parseDOM(items, 'source', ret='src')[0]
        if ('http') in url: return url+'|User-Agent=Mozilla/5.0 (compatible; CloudFlare-AlwaysOnline/1.0; +https://www.cloudflare.com/always-online) AppleWebKit/534.34'
    except:
        return None

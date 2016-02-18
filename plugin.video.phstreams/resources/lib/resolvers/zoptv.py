from resources.lib.modules import client
from resources.lib.modules import cloudflare
import re,sys,urllib,urlparse,base64,urllib2,cookielib


domains = ['zoptv.com']


def resolve(url):
    test = '|User-Agent=Mozilla/5.0 (compatible; CloudFlare-AlwaysOnline/1.0; +https://www.cloudflare.com/always-online) AppleWebKit/534.34'
    try:
        
        result = cloudflare.request(url)
        uri = re.findall("decodeURIComponent\(atob\('(.+?)'",result)[0]
        while not ('http') in uri:
            uri = base64.b64decode(uri)
            if not ('http') in uri:
                uri = re.findall("'(.+?)'",uri)[0]
            else:
                pass
        murl = re.findall('"src":"(.+?)"',uri)[0]  
            
    except:
        return None
    try:
        result = cloudflare.request(murl)
        items = client.parseDOM(result, 'video', attrs={'id': 'player'})
        url = client.parseDOM(items, 'source', ret='src')[0]
        if ('http') in url: return url+test
        if url[0]!='/':
            url='http://www.iptvlinks.tk/'+url+test
        else:
            url='http://www.iptvlinks.tk'+url+test      
        return url
    except:
        return None

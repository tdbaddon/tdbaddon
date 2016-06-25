# -*- coding: utf-8 -*-


import re,urlparse,json,requests,cookielib
from resources.lib.modules import client,control,constants

from resources.lib.modules.log_utils import log
import urllib,sys,os

cookieFile = os.path.join(control.dataPath, 'streamlivecookie.lwp')


def resolve(url):
    
    try:
        page = url

        user, password = get_account()
        

        try: 
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
            url = url.replace(referer,'').replace('?referer=','').replace('&referer=','')
        except:
            referer = url


        post_data = 'username=%s&password=%s&accessed_by=web&submit=Login'%(user,password)

        cj = get_cj()
        result = client.request(url,cj=cj,headers={'referer':'http://www.streamlive.to', 'Content-type':'application/x-www-form-urlencoded', 'Origin': 'http://www.streamlive.to', 'Host':'www.streamlive.to', 'User-agent':client.agent()})
        if 'this channel is a premium channel.' in result.lower():
          control.infoDialog('Premium channel. Upgrade your account to watch it!', heading='Streamlive.to')
          return 

        if 'not logged in yet' in result.lower() or 'you have reached the limit today' in result.lower():
            #Cookie expired or not valid, request new cookie
            cj = login(cj,post_data)
            cj.save (cookieFile,ignore_discard=True)
            result = client.request(url,cj=cj)

        log(result)
        token_url = re.compile('getJSON\("(.+?)"').findall(result)[0]
        r2 = client.request(token_url,referer=referer)
        token = json.loads(r2)["token"]

        file = re.compile('(?:[\"\'])?file(?:[\"\'])?\s*:\s*(?:\'|\")(.+?)(?:\'|\")').findall(result)[0].replace('.flv','')
        rtmp = re.compile('streamer\s*:\s*(?:\'|\")(.+?)(?:\'|\")').findall(result)[0].replace(r'\\','\\').replace(r'\/','/')
        app = re.compile('.*.*rtmp://[\.\w:]*/([^\s]+)').findall(rtmp)[0]
        url=rtmp + ' app=' + app + ' playpath=' + file + ' swfUrl=http://www.streamlive.to/ads/streamlive.swf flashver=' + constants.flash_ver() + ' live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl='+page

        
        return url
    except:
        return



def login(cookies,post_data):
    log('Making new login token.')
    cj = client.request('http://www.streamlive.to/login.php', post=post_data, headers = {'referer':'http://www.streamlive.to/login', 'Content-type':'application/x-www-form-urlencoded', 'Origin': 'http://www.streamlive.to', 'Host':'www.streamlive.to', 'User-agent':client.agent()},cj=cookies,output='cj')
    return cj

def get_cj():
    cookieJar=None
    try:
        cookieJar = cookielib.LWPCookieJar()
        cookieJar.load(cookieFile,ignore_discard=True)
    except: 
        cookieJar=None

    if not cookieJar:
        cookieJar = cookielib.LWPCookieJar()
    return cookieJar

def get_account():
    import random
    accounts = [('cod11','croatia_on_demand1'),('cod1','croatia_on_demand1'),('cod2','croatia_on_demand2'),('cod3','croatia_on_demand3'),('cod22','croatia_on_demand'),('cod33','croatia_on_demand'),('cod44','croatia_on_demand')]
    return random.choice(accounts)
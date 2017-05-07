import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcvfs,os,sys,datetime,string,hashlib,net,traceback
from resources.lib.modules.plugintools import *
import xbmcaddon
import json
from cookielib import CookieJar,LWPCookieJar

from resources.lib.modules.common import *

ADDON     = xbmcaddon.Addon(id='plugin.video.freeview')
DATA_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.freeview'), '')
TVPCOOKIEFILE='TVPCookieFile.lwp'
TVPCOOKIEFILE=os.path.join(DATA_PATH, TVPCOOKIEFILE)

def getTVPCookieJar(updatedUName=False):
    cookieJar=None
    print 'updatedUName',updatedUName
    try:
        cookieJar = LWPCookieJar()
        if not updatedUName:
            cookieJar.load(TVPCOOKIEFILE,ignore_discard=True)
    except: 
        cookieJar=None

    if not cookieJar:
        cookieJar = LWPCookieJar()
    return cookieJar
    
def performTVPLogin():
    cookieJar = LWPCookieJar()
    try:
        
        url="https://tvplayer.com/account"
        username=ADDON.getSetting( "tvpusername" ) 
        if username=="": return False,cookieJar
        pwd=ADDON.getSetting( "tvppwd" ) 
        lasstusername=ADDON.getSetting( "lasttvpusername" )
        lasstpwd=ADDON.getSetting( "lasttvppwd" )         
        cookieJar=getTVPCookieJar(lasstusername!=username or lasstpwd!= pwd)
        mainpage = open_url(url,cj=cookieJar)
        

        if 'Login to TVPlayer' in mainpage:
            token   = urllib.unquote(re.findall('name="token" value="(.*?)"' ,mainpage)[0])
            print 'LOGIN NOW'
            url="https://tvplayer.com/account/login"
            headers={'Referer':"https://tvplayer.com/account/login",'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36','Origin':'https://tvplayer.com'}            
            post = {'email':username,'password':pwd,'token':token}
            post = urllib.urlencode(post)
            mainpage = open_url(url,cj=cookieJar,data=post,headers=headers )
            cookieJar.save (TVPCOOKIEFILE,ignore_discard=True)
            ADDON.setSetting( id="lasttvpusername" ,value=username)
            ADDON.setSetting( id="lasttvppwd" ,value=pwd)
        
        return not '>Login</a>' in mainpage,cookieJar
    except: 
            traceback.print_exc(file=sys.stdout)
    return False,cookieJar

def tvplayer(url):
    print 'url',url
    import re,urllib,json
    islogin,cj=performTVPLogin()
    
    watchHtml = open_url("http://tvplayer.com/watch/",cj=cj)
    channelid=url#re.findall('data-resource="(.*?)"' ,watchHtml)[0]
    #token=re.findall('var validate = "(.*?)"' ,watchHtml)[0]
    token='null'
    try:
        token=re.findall('data-token="(.*?)"' ,watchHtml)[0]
    except: pass
    headers   = {'Referer':'http://tvplayer.com/watch/','Origin':'http://tvplayer.com','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    
    contextjs=open_url("https://tvplayer.com/watch/context?resource=%s&nonce=%s"%(channelid,token),headers=headers,cj=cj);  
    contextjs=json.loads(contextjs)
    validate=contextjs["validate"]
    #cj        = CookieJar()
    data = urllib.urlencode({'service':'1','platform':'chrome','validate':validate ,'id' : channelid})
    retjson   = open_url("http://api.tvplayer.com/api/v2/stream/live",data=data, headers=headers,cj=cj);
    jsondata  = json.loads(retjson)
    #    print cj
    #cj        = CookieJar()
    playurl   = jsondata["tvplayer"]["response"]["stream"]
    open_url(playurl, headers=headers,cj=cj);
    playurl   = playurl+'|Cookie=%s&User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36&X-Requested-With=ShockwaveFlash/22.0.0.209&Referer=http://tvplayer.com/watch/'%getCookiesString(cj)
    play(playurl)
    return
        
def tvplayerFlashVersion(url):
    import re,urllib,json
    islogin,cj=performTVPLogin()
    watchHtml = open_url('http://tvplayer.com/watch/')
    hashval   = urllib.unquote(re.findall('hash = "(.*?)"' ,watchHtml)[0])
    expval    = re.findall('exp = "(.*?)"' ,watchHtml)[0]
    keyval    = generateKey(expval)
    #cj        = CookieJar()
    data      = urllib.urlencode({'id' : url})
    headers   = {'Token-Expiry':expval ,'Hash': hashval,'Key':keyval,'Referer':'http://assets.tvplayer.com/web/flash/tvplayer/TVPlayer-DFP-3.swf','X-Requested-With':'ShockwaveFlash/22.0.0.209'}
    retjson   = open_url("http://live.tvplayer.com/stream-web-encrypted.php",data=data, headers=headers,cj=cj);
    jsondata  = json.loads(retjson)
#    print cj
    url       = jsondata["tvplayer"]["response"]["stream"]
    play(url+'|Cookie=%s&User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36&X-Requested-With=ShockwaveFlash/22.0.0.209&Referer=http://tvplayer.com/watch/'%getCookiesString(cj))
    return 
    
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcvfs,os,sys,datetime,string,hashlib,net
from resources.lib.modules.plugintools import *
import xbmcaddon
import liveresolver
import json
from cookielib import CookieJar
from resources.lib.modules.common import *

def tvplayer(url):
    import re,urllib,json
    watchHtml = open_url("http://tvplayer.com/watch/")
    channelid = url#re.findall('resourceId = "(.*?)"' ,watchHtml)[0]
    validate  = re.findall('var validate = "(.*?)"' ,watchHtml)[0]
    cj        = CookieJar()
    data      = urllib.urlencode({'service':'1','platform':'website','token':'null','validate':validate ,'id' : channelid})
    headers   = {'Referer':'http://tvplayer.com/watch/','Origin':'http://tvplayer.com','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    retjson   = open_url("http://api.tvplayer.com/api/v2/stream/live",data=data, headers=headers,cj=cj);
    jsondata  = json.loads(retjson)
    #    print cj
    cj        = CookieJar()
    playurl   = jsondata["tvplayer"]["response"]["stream"]
    open_url(playurl, headers=headers,cj=cj);
    playurl   = playurl+'|Cookie=%s&User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36&X-Requested-With=ShockwaveFlash/22.0.0.209&Referer=http://tvplayer.com/watch/'%getCookiesString(cj)
    play(playurl)
    return
        
def tvplayerFlashVersion(url):
    import re,urllib,json
    watchHtml = open_url('http://tvplayer.com/watch/')
    hashval   = urllib.unquote(re.findall('hash = "(.*?)"' ,watchHtml)[0])
    expval    = re.findall('exp = "(.*?)"' ,watchHtml)[0]
    keyval    = generateKey(expval)
    cj        = CookieJar()
    data      = urllib.urlencode({'id' : url})
    headers   = {'Token-Expiry':expval ,'Hash': hashval,'Key':keyval,'Referer':'http://assets.tvplayer.com/web/flash/tvplayer/TVPlayer-DFP-3.swf','X-Requested-With':'ShockwaveFlash/22.0.0.209'}
    retjson   = open_url("http://live.tvplayer.com/stream-web-encrypted.php",data=data, headers=headers,cj=cj);
    jsondata  = json.loads(retjson)
#    print cj
    url       = jsondata["tvplayer"]["response"]["stream"]
    play(url+'|Cookie=%s&User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36&X-Requested-With=ShockwaveFlash/22.0.0.209&Referer=http://tvplayer.com/watch/'%getCookiesString(cj))
    return 
    
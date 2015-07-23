__author__ = 'traitravinh'
import urllib, urllib2, re, os, sys,json
import xbmc
import xbmcaddon,xbmcplugin,xbmcgui
from bs4 import BeautifulSoup

rootlink = 'http://hplus.com.vn/'
homelink = 'http://hplus.com.vn/en/categories/live-tv'
logo = 'http://static.hplus.com.vn/themes/front/images/logoFooter.png'

def home():
    apilink = "http://api.htvonline.com.vn/tv_channels"
    reqdata = '{"pageCount":200,"category_id":"-1","startIndex":0}'
    data = getContent ( apilink , reqdata)
    print data
    for d in data ["data"] :
        res = d["link_play"][0]["resolution"]
        img = d["image"]
        title = d["name"]+' ('+res+')'
        link = d["link_play"][0]["mp3u8_link"]
        addLink(title.encode('utf-8'), link,2,img)

def getContent(url, requestdata):
    req = urllib2 . Request(urllib . unquote_plus(url))
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    req.add_header('Authorization', 'Basic YXBpaGF5aGF5dHY6NDUlJDY2N0Bk')
    req.add_header('User-Agent', 'Apache-HttpClient/UNAVAILABLE (java 1.4)')
    link = urllib . urlencode({'request': requestdata})
    resp = urllib2 . urlopen(req, link, 120)
    content = resp . read()
    resp . close()
    content = '' . join(content . splitlines())
    data = json . loads(content)
    return data

def index(url):
    link = urllib2.urlopen(url).read()
    soup = BeautifulSoup(link.decode('utf-8'))
    divpanel = soup('div',{'class':'panel'})
    for d in range(1,len(divpanel)):
        dsoup = BeautifulSoup(str(divpanel[d]))
        dlink = rootlink+dsoup('a')[1]['href']
        dtitle = dsoup('a')[1].contents[0].encode('utf-8')
        dimage = re.compile("background-image: url\('(.+?)'\)").findall(str(dsoup('a')[0]['style'].encode('utf-8')))[0]
        addLink(dtitle,dlink,2,dimage)

def videoLink(url):
    link = urllib2.urlopen(url).read()
    vlink= re.compile('iosUrl = "(.+?)";').findall(link)
    return vlink[0]

def play(url):
    try:
        # videoId = videoLink(url)
        videoId=url
        listitem = xbmcgui.ListItem(name,iconImage='DefaultVideo.png',thumbnailImage=iconimage)
        listitem.setPath(videoId)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    except:pass

def addLink(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name})#, "overlay":6,"watched":False})
    liz.setProperty('mimetype', 'video/x-msvideo')
    liz.setProperty("IsPlayable","true")
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=False)
    return ok

def addDir(name, url, mode, iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=logo, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]

        return param

params=get_params()
url=None
name=None
mode=None
iconimage=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

sysarg=str(sys.argv[1])

if mode==None or url==None or len(url)<1:
    home()
elif mode==1:
    index(url)
elif mode==2:
    play(url)

xbmcplugin.endOfDirectory(int(sysarg))
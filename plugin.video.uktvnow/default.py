import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,json,random,string,base64
import net
net = net.Net()

AddonID ='plugin.video.uktvnow'
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID, 'icon.png'))
artpath = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID + '/resources/art/'))
dialog = xbmcgui.Dialog()
selfAddon = xbmcaddon.Addon(id=AddonID)
user = selfAddon.getSetting('username')
passw = selfAddon.getSetting('password')

def local_time(zone='Asia/Karachi'):
    from datetime import datetime
    from pytz import timezone
    other_zone = timezone(zone)
    other_zone_time = datetime.now(other_zone)
    return other_zone_time.strftime('%B-%d-%Y')
    
def getAPIToken( url,  username):
    from pytz import timezone
    dt=local_time()
    s = "uktvnow-token-"+ dt + "-"+ "_|_-" + url + "-" + username +"-" + "_|_"+ "-"+ base64.b64decode("MTIzNDU2IUAjJCVedWt0dm5vd14lJCNAITY1NDMyMQ==")
    import hashlib
    return hashlib.md5(s).hexdigest()

def Main():
    addDir('All Channels','0',1,artpath+'all.PNG',fanart)
    addDir('Entertainment','1',1,artpath+'ent.PNG',fanart)
    addDir('Movies','2',1,artpath+'mov.PNG',fanart)
    addDir('Music','3',1,artpath+'mus.PNG',fanart)
    addDir('News','4',1,artpath+'news.PNG',fanart)
    addDir('Sports','5',1,artpath+'sport.PNG',fanart)
    addDir('Documentary','6',1,artpath+'doc.PNG',fanart)
    addDir('Kids Corner','7',1,artpath+'kids.PNG',fanart)
    addDir('Food','8',1,artpath+'food.PNG',fanart)
    addDir('Religious','9',1,artpath+'rel.PNG',fanart)
    addDir('USA Channels','10',1,artpath+'us.PNG',fanart)
    addDir('Others','11',1,artpath+'others.PNG',fanart)
    xbmc.executebuiltin('Container.SetViewMode(500)')
 
        
def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    try :return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))
    except:return re.sub("(?i)&#\w+;", fixup, text.encode("ascii", "ignore").encode('utf-8'))
    
def GetContent():
    token=getAPIToken('https://app.uktvnow.net/v1/get_all_channels','metalkettle2')
    headers={'User-Agent':'USER-AGENT-UKTVNOW-APP-V1',
             'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
             'Accept-Encoding' : 'gzip',
             'app-token':token,
             'Connection':'Keep-Alive',
             'Host':'app.uktvnow.net'}
    postdata={'username':'metalkettle2'}
    channels = net.http_POST('https://app.uktvnow.net/v1/get_all_channels',postdata, headers).content
    channels = channels.replace('\/','/')
    match=re.compile('"channel_name":"(.+?)","img":"(.+?)","http_stream":"(.+?)","rtmp_stream":"(.+?)","cat_id":"(.+?)"').findall(channels)
    return match

def GetChannels(url):
    match = GetContent()
    for name,iconimage,stream1,stream2,cat in match:
        if name=='null':name='Channel'
        name=name.replace('"','')
        thumb='https://app.uktvnow.net/'+iconimage+'|User-Agent=Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G920F Build/LMY47X)'     
        if url=='0':
            addLink(name,'url',2,thumb,fanart)
        if cat==url:
            addLink(name,'url',2,thumb,fanart)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
    xbmc.executebuiltin('Container.SetViewMode(500)')

def GetStreams(name):
    match = GetContent()
    for name2,iconimage,stream1,stream2,cat in match:      
        name2=name2.replace('"','')
        thumb='https://app.uktvnow.net/'+iconimage+'|User-Agent=Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G920F Build/LMY47X)'     
        streamname=[]
        streamurl=[]
        streamthumb=[]
        if name2 == name:
            streamurl.append( stream1 )
            streamurl.append( stream2 )
            streamname.append( 'Stream 1' )
            streamname.append( 'Stream 2' )
            streamthumb.append( thumb )
            streamthumb.append( thumb )
            select = dialog.select(name2,streamname)
            if select == -1:
                return
            else:
                url = streamurl[select]
                iconimage = streamthumb[select]
                ok=True
                liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
                xbmc.Player().play(url, liz, False)
                return ok

def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addDir(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
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
description=None

try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:mode=int(params["mode"])
except:pass
try:iconimage=urllib.unquote_plus(params["iconimage"])
except:pass

if mode==None or url==None or len(url)<1:Main()
elif mode==1:GetChannels(url)
elif mode==2:GetStreams(name)
elif mode==3:Schedule(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))

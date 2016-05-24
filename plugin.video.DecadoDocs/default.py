import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,os
from t0mm0.common.addon import Addon

addon_id = 'plugin.video.DecadoDocs'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
ADDON2=xbmcaddon.Addon(id='plugin.video.DecadoDocs')
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
base = 'http://topdocumentaryfilms.com/'

def CATEGORIES():
        addDir('Latest Documentaries','http://topdocumentaryfilms.com/all/',1,icon,fanart)
        addDir('Highest Rated Documentaries','http://topdocumentaryfilms.com/all/?r_sortby=highest_rated&r_orderby=desc',1,icon,fanart)
        addLink('','url','mode',icon,fanart)
        link = open_url(base)
        match=re.compile('<a href="(.+?)" >(.+?)</a></li><li>').findall(link)
        for url,name in match:
                if 'category' in url:
                        addDir(name,url,1,icon,fanart)
               
def CATDOCS(url):
        link = open_url(url)
        match=re.compile('<h2><a href="(.+?)" title="(.+?)">.+?</a></h2>.+?src="(.+?)"',re.DOTALL).findall(link)
        for url,name,thumb in match:
                name=name.replace('&#039;','')
                addLink(name,url,2,thumb,fanart)
        try:
                match=re.compile('<a href="(.+?)">Next</a></div>').findall(link)
                for url in match:
                        addDir('Next Page >>>',url,1,icon,fanart)
        except: pass

def PLAYDOCS(url,name):
    try:
        link = open_url(url)
        match=re.compile('src="(.+?)"').findall(link)
        for url in match:
                if 'youtube'in url:
                        found = url
        if 'videoseries' in found:
                if not 'http:' in found:
                        found = 'http:'+found
                link = open_url(found)
                youtube=re.compile('VIDEO_ID\'\: "(.+?)"\,').findall(link)[0]
        if 'videoseries' not in found:
                youtube=found.split('/')[4].split('?')[0]
        playback_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % youtube     
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        playlist.add(playback_url,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)
    except:
        dialog = xbmcgui.Dialog()
        dialog.ok('Decado Documentaries','','Documentary has been removed','')
    
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

def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")

def addDir(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)

        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        
def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON2.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON2.getSetting(viewType) )

params=get_params(); url=None; name=None; mode=None; site=None; iconimage=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

print "Site: "+str(site); print "Mode: "+str(mode); print "URL: "+str(url); print "Name: "+str(name)
print params

if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: CATDOCS(url)
elif mode==2: PLAYDOCS(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))


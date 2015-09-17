import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,sys,xbmc,xbmcaddon,os
from t0mm0.common.addon import Addon
from metahandler import metahandlers

addon_id = 'plugin.video.moviexk'
selfAddon = xbmcaddon.Addon(id=addon_id)
metaget = metahandlers.MetaData(preparezip=False)
addon = Addon(addon_id, sys.argv)
ADDON2=xbmcaddon.Addon(id='plugin.video.moviexk')
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
metaset = selfAddon.getSetting('enable_meta')

def CATEGORIES():
        addDir2('Latest Cinema Releases','http://www.moviexk.net/cinema/',1,icon,'',fanart)
        addDir2('Recently Added','http://www.moviexk.net/new-movies/',1,icon,'',fanart)
        addDir2('Most Viewed','http://www.moviexk.net/popular-movies/',1,icon,'',fanart)
        addDir2('HD Movies','http://www.moviexk.net/movies-hd/',1,icon,'',fanart)
        addDir2('Genres','http://www.moviexk.net',2,icon,'',fanart)      
        addDir2('Search','url',3,icon,'',fanart)
        xbmc.executebuiltin('Container.SetViewMode(50)')
               
def GETMOVIES(url,name):
        metaset = selfAddon.getSetting('enable_meta')
        link = open_url(url)
        match=re.compile('<a href="(.+?)" title="Movie (.+?)"><img class="lazy"').findall(link)
        for url,name in match:
                name=cleanHex(name)
                if metaset=='false':
                        addDir(name,url,100,icon,len(match),isFolder=False)
                else: addDir(name,url,100,'',len(match),isFolder=False)
        try:
                match=re.compile("<a href='(.+?)' class='nextpostslink'>").findall(link)
                for np in match:
                        npurl = np.split("href='")[-1]
                        addDir2('Next Page>>>',npurl,1,icon,'',fanart)              
        except: pass
        if metaset=='true':
                setView('movies', 'MAIN')
        else: xbmc.executebuiltin('Container.SetViewMode(50)')

def GENRES(url):
        link = open_url(url)
        match=re.compile('<li id="menu-item" class="menu-item"><h3><a href="(.+?)">(.+?)</a></h3></li>').findall(link)
        for url,name in match:
                addDir2(name,url,1,icon,'',fanart)

def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))

def SEARCH():
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'Search Movies XK')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
    if len(search_entered)>1:
        url = 'http://www.moviexk.net/search/'+ search_entered
        link = open_url(url)
        GETMOVIES(url,name)

def PLAYLINK(name,url,iconimage):
        link = open_url(url)
        match=re.compile('<a href="(.+?)" title=".+?">').findall(link)[2]
        link = open_url(match)
        try:
                stream_url=re.compile('<source src="(.+?)"').findall(link)[0]
        except:
                stream_url=re.compile('<iframe src="(.+?)" scrolling').findall(link)[0]
                stream_url=resolve(stream_url)
        
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)

def resolve(url):
        # Thanks to Lambda for the resolver :)
        O = {
            '___': 0,
            '$$$$': "f",
            '__$': 1,
            '$_$_': "a",
            '_$_': 2,
            '$_$$': "b",
            '$$_$': "d",
            '_$$': 3,
            '$$$_': "e",
            '$__': 4,
            '$_$': 5,
            '$$__': "c",
            '$$_': 6,
            '$$$': 7,
            '$___': 8,
            '$__$': 9,
            '$_': "constructor",
            '$$': "return",
            '_$': "o",
            '_': "u",
            '__': "t",
        }
        url = url.replace('/f/', '/embed/')
        import client,jsunpack
        result = client.request(url)
        result = re.search('>\s*(eval\(function.*?)</script>', result, re.DOTALL).group(1)
        result = jsunpack.unpack(result)
        result = result.replace('\\\\', '\\')
        result = re.search('(O=.*?)(?:$|</script>)', result, re.DOTALL).group(1)
        result = re.search('O\.\$\(O\.\$\((.*?)\)\(\)\)\(\);', result)
        s1 = result.group(1)
        s1 = s1.replace(' ', '')
        s1 = s1.replace('(![]+"")', 'false')
        s3 = ''
        for s2 in s1.split('+'):
            if s2.startswith('O.'):
                s3 += str(O[s2[2:]])
            elif '[' in s2 and ']' in s2:
                key = s2[s2.find('[') + 3:-1]
                s3 += s2[O[key]]
            else:
                s3 += s2[1:-1]
        s3 = s3.replace('\\\\', '\\')
        s3 = s3.decode('unicode_escape')
        s3 = s3.replace('\\/', '/')
        s3 = s3.replace('\\\\"', '"')
        s3 = s3.replace('\\"', '"')
        url = re.search('<source\s+src="([^"]+)', s3).group(1)
        return url

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

def addDir2(name,url,mode,iconimage,description,fanart):
        xbmc.executebuiltin('Container.SetViewMode(50)')
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir(name,url,mode,iconimage,itemcount,isFolder=False):
        if metaset=='true':
            splitName=name.partition('(')
            simplename=""
            simpleyear=""
            if len(splitName)>0:
                simplename=splitName[0]
                simpleyear=splitName[2].partition(')')
            if len(simpleyear)>0:
                simpleyear=simpleyear[0]
            meta = metaget.get_meta('movie', simplename ,simpleyear)
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
            ok=True
            liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=iconimage)
            liz.setInfo( type="Video", infoLabels= meta )
            contextMenuItems = []
            contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
            liz.addContextMenuItems(contextMenuItems, replaceItems=True)
            if not meta['backdrop_url'] == '': liz.setProperty('fanart_image', meta['backdrop_url'])
            else: liz.setProperty('fanart_image', fanart)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder,totalItems=itemcount)
            return ok
        else:
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
            ok=True
            liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
            liz.setInfo( type="Video", infoLabels={ "Title": name } )
            liz.setProperty('fanart_image', fanart)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
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
elif mode==1: GETMOVIES(url,name)
elif mode==2: GENRES(url)
elif mode==3: SEARCH()
elif mode==100: PLAYLINK(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))


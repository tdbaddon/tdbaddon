import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,sys,xbmc,xbmcaddon,os,random,urlparse
from t0mm0.common.addon import Addon
from metahandler import metahandlers

addon_id = 'plugin.video.movieshd'
selfAddon = xbmcaddon.Addon(id=addon_id)
datapath= xbmc.translatePath(selfAddon.getAddonInfo('profile'))
metaget = metahandlers.MetaData(preparezip=False)
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
artpath = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
metaset = selfAddon.getSetting('enable_meta')

def CATEGORIES():
        addDir2('Featured','http://movieshd.eu/movies/category/featured',1,icon,'',fanart)
        addDir2('Recently Added','http://movieshd.eu/?filtre=date&cat=0',1,icon,'',fanart)
        addDir2('Most Viewed','http://movieshd.eu/?display=tube&filtre=views',1,icon,'',fanart)
        addDir2('Bollywood','http://movieshd.eu/bollywood/',1,icon,'',fanart) 
        addDir2('Genres','url',2,icon,'',fanart)
        addDir2('Years','http://movieshd.eu/year/',5,icon,'',fanart)
        addDir2('Search','url',3,icon,'',fanart)
        addLink('[COLOR blue]Twitter[/COLOR] Feed','url',4,icon,fanart)
        xbmc.executebuiltin('Container.SetViewMode(50)')

def BOLLYWOOD():
        addDir2('Featured','url',7,icon,'',fanart)
        addDir2('Recently Added','url',7,icon,'',fanart)
        addDir2('Action','url',7,icon,'',fanart)
        addDir2('Comedy ','url',7,icon,'',fanart)
        addDir2('Romance','url',7,icon,'',fanart)
        addDir2('Punjabi','url',7,icon,'',fanart)

def GETBOLLYWOOD(name):
        link = open_url('http://movieshd.eu/bollywood/')
        regexstring = '<div class="content-widget"><div class="widget-title"><span>'+name+'</span></div>(.+?)</ul>'
        cat=re.compile(regexstring,re.DOTALL).findall(link)[0]
        match=re.compile('<img src=".+?" alt=".+?" title="(.+?)"/><a href="(.+?)"').findall(cat)
        items = len(match)
        for name,url in match:
                name2 = cleanHex(name)
                addDir(name2,url,100,'',len(match))
        try:
                match=re.compile('"nextLink":"(.+?)"').findall(link)
                url= match[0]
                url = url.replace('\/','/')
                addDir('Next Page>>',url,1,artpath+'nextpage.png',items,isFolder=True)
        except: pass
        if metaset=='true':
                setView('movies', 'MAIN')
        else: xbmc.executebuiltin('Container.SetViewMode(50)')
                     
def TWITTER():
        text = ''
        twit = 'https://script.google.com/macros/s/AKfycbyBcUa5TlEQudk6Y_0o0ZubnmhGL_-b7Up8kQt11xgVwz3ErTo/exec?560774256146272257'
        link = open_url(twit)
        match=re.compile("<title>(.+?)</title>.+?<pubDate>(.+?)</pubDate>",re.DOTALL).findall(link)[1:]
        for status, dte in match:
            dte = dte[:-15]
            dte = '[COLOR blue][B]'+dte+'[/B][/COLOR]'
            text = text+dte+'\n'+status+'\n'+'\n'
        showText('@movieshd_co', text)

def GETMOVIES(url,name):
        link = open_url(url)
        match=re.compile('<img src=".+?" alt=".+?" title="(.+?)"/><a href="(.+?)"').findall(link)
        items = len(match)
        for name,url in match:
                name2 = cleanHex(name)
                addDir(name2,url,100,'',len(match))
        try:
                match=re.compile('"nextLink":"(.+?)"').findall(link)
                url= match[0]
                url = url.replace('\/','/')
                addDir('Next Page>>',url,1,artpath+'nextpage.png',items,isFolder=True)
        except: pass
        if metaset=='true':
                setView('movies', 'MAIN')
        else: xbmc.executebuiltin('Container.SetViewMode(50)')
        
def GENRES(url):
        addDir2('Action / Adventure','http://movieshd.eu/movies/category/action-adventure/',1,artpath+'action.png','',fanart)
        addDir2('Animation','http://movieshd.eu/movies/category/animation/',1,artpath+'animation.png','',fanart)
        addDir2('Biography','http://movieshd.eu/movies/category/biography/',1,artpath+'biography.png','',fanart)
        addDir2('Comedy','http://movieshd.eu/movies/category/comedy/',1,artpath+'comedy.png','',fanart)
        addDir2('Crime','http://movieshd.eu/movies/category/crime/',1,artpath+'crime.png','',fanart)
        addDir2('Drama','http://movieshd.eu/movies/category/drama/',1,artpath+'drama.png','',fanart)
        addDir2('Family','http://movieshd.eu/movies/category/family/',1,artpath+'family.png','',fanart)
        addDir2('Fantasy','http://movieshd.eu/movies/category/fantasy/',1,artpath+'fantasy.png','',fanart)
        addDir2('History','http://movieshd.eu/movies/category/history/',1,artpath+'history.png','',fanart)
        addDir2('Horror','http://movieshd.eu/movies/category/horror/',1,artpath+'horror.png','',fanart)
        addDir2('Music','http://movieshd.eu/movies/category/music/',1,artpath+'musical.png','',fanart)
        addDir2('Mystery','http://movieshd.eu/movies/category/mystery/',1,artpath+'mystery.png','',fanart)
        addDir2('Romance','http://movieshd.eu/movies/category/romance/',1,artpath+'romance.png','',fanart)
        addDir2('Sci-Fi','http://movieshd.eu/movies/category/sci-fi/',1,artpath+'sci-fi.png','',fanart)
        addDir2('Sports','http://movieshd.eu/movies/category/sports/',1,artpath+'sport.png','',fanart)
        addDir2('Thriller','http://movieshd.eu/movies/category/thriller/',1,artpath+'thriller.png','',fanart)
        addDir2('War','http://movieshd.eu/movies/category/war/',1,artpath+'war.png','',fanart)
        addDir2('Western','http://movieshd.eu/movies/category/western/',1,artpath+'western.png','',fanart)
        xbmc.executebuiltin('Container.SetViewMode(500)')

def YEARS(url):
        link = open_url(url)
        match=re.compile('<li class="border-radius-5"><img src="(.+?)"/><br/><a href="(.+?)"><span>YEAR (.+?)</span></a>').findall(link)
        for thumb,url,year in match:
                url = url.replace('https','http')
                addDir2(year,url,1,thumb,'',fanart)
        xbmc.executebuiltin('Container.SetViewMode(500)')

def SEARCH():
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'Search Movies HD')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
    if len(search_entered)>1:
        url = 'http://movieshd.eu/?s='+ search_entered
        link = open_url(url)
        GETMOVIES(url,name)

def PLAYLINK(name,url,iconimage):
    link = open_url(url)
    olurl=re.compile('<p><iframe src="(.+?)"').findall(link)[0]
    print olurl
    stream_url=resolve(olurl)
    print stream_url
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    xbmc.Player ().play(stream_url, liz, False)

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
            

def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
    
def showText(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            retry -= 1
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            return
        except:
            pass
        
def open_url(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link = link.replace('\n','')
        link = link.decode('utf-8').encode('utf-8').replace('&#39;','\'').replace('&#10;',' - ').replace('&#x2026;','')
        response.close()
        return link
                
def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))

def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if selfAddon.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % selfAddon.getSetting(viewType) )

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
elif mode==4: TWITTER()
elif mode==5: YEARS(url)
elif mode==6: BOLLYWOOD()
elif mode==7: GETBOLLYWOOD(name)

elif mode==100: PLAYLINK(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))


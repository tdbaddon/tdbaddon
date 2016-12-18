import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,os,cloudflare,net
from t0mm0.common.addon import Addon

net = net.Net()
addon_id = 'plugin.video.cartoons8'
selfAddon = xbmcaddon.Addon(id=addon_id)
datapath= xbmc.translatePath(selfAddon.getAddonInfo('profile'))
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
cartoon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'cartoon.png'))
anime = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'anime.png'))
try:os.mkdir(datapath)
except:pass
file_var = open(xbmc.translatePath(os.path.join(datapath, 'cookie.lwp')), "a")
cookie_file = os.path.join(os.path.join(datapath,''), 'cookie.lwp')

def INDEX():
        addDir('Cartoons','url',9,cartoon,fanart)
        addDir('Anime','url',10,anime,fanart)

def CCATEGORIES():
        addDir('Cartoon - New & Hot','http://9cartoon.me/CartoonList/NewAndHot?page=1',1,cartoon,fanart)
	addDir('Cartoon - New Added','http://9cartoon.me/CartoonList/New?page=1',1,cartoon,fanart)
	addDir('Cartoon - Popular','http://9cartoon.me/CartoonList/MostViewed?page=1',1,cartoon,fanart)
	addDir('Cartoon - A - Z','http://9cartoon.me/CartoonList',5,cartoon,fanart)
	addDir('Cartoon - Genres','http://9cartoon.me',6,cartoon,fanart)
        addDir('Cartoon - Search','http://9cartoon.me/Search?s=',8,cartoon,fanart)

def ACATEGORIES():
        addDir('Anime - New & Hot','http://gogoanime.ch/AnimeList/NewAndHot?page=1',1,anime,fanart)
	addDir('Anime - New Added','http://gogoanime.ch/AnimeList/New?page=1',1,anime,fanart)
	addDir('Anime - Popular','http://gogoanime.ch/AnimeList/MostViewed?page=1',1,anime,fanart)
	addDir('Anime - A - Z','http://gogoanime.ch/AnimeList',5,anime,fanart)
	addDir('Anime - Genres','http://gogoanime.ch/',6,anime,fanart)
        addDir('Anime - Search','http://gogoanime.ch/Search?s=',8,anime,fanart)

def GETMOVIES(url,name):
        link = open_url(url)
        link = link.replace("'",'"')
        match=re.compile('<li title="<div class="thumnail_tool"><img src="(.+?)" onerror="this.className=`hide`"></div><div style="float: left; width: 300px"><a class="bigChar" href="(.+?)">(.+?)</a>').findall(link)
        for iconimage, murl, name in match:
                iconimage=iconimage+"|User-Agent=Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0&Cookie=%s"%getCookiesString()
                name = cleanHex(name)
                addDir(name,murl,2,iconimage,iconimage)
        try:
                pagenum = url.split('?page=')
                curpage = int(pagenum[1])
                nextpage = curpage + 1
                nextpageurl = pagenum[0]+'?page='+str(nextpage)
                addDir('Next >> Page '+str(nextpage),nextpageurl,1,icon,fanart)
        except: pass

def GETEPISODES(url,name,iconimage):
        link = open_url(url)
        link = link.replace('\n','').replace('  ','').replace('\t','').replace('\r','')
        match=re.compile('<ul id="episode_related">(.+?)</ul></div>').findall(link)[0]      
        match=re.compile('<a href="(.+?)">(.+?)</a>').findall(match)
        match=list(reversed(match))
        for url, name2 in match:
                if len(match)==1:
                        GETPLAYLINK(name,url,iconimage)
                        quit()
                else:
                        name = cleanHex(name)
                        addLink(name2,url,100,iconimage,iconimage)
def SEARCH(url):
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'Search')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
    if len(search_entered)>1:
        url = url + search_entered + '&page=1'
        GETGENREMOVIES(url)

def getCookiesString():
    cookieString=""
    import cookielib
    try:
        cookieJar = cookielib.LWPCookieJar()
        cookieJar.load(cookie_file,ignore_discard=True)
        for index, cookie in enumerate(cookieJar):
            cookieString+=cookie.name + "=" + cookie.value +";"
    except: 
        import sys,traceback
        traceback.print_exc(file=sys.stdout)
    return cookieString

def GETGENRES(url,iconimage):
        link = open_url(url)
        match=re.compile('<a href="(.+?)" title="(.+?)">').findall(link)
        for url, name in match:
                if 'genre' in url:
                        url=url+'?page=1'
                        addDir(name,url,7,iconimage,fanart)

def GETGENREMOVIES(url):
	url2=url
        link = open_url(url)        
        match=re.compile('<img src="(.+?)">.+?<a href="(.+?)" title="(.+?)">',re.DOTALL).findall(link)[3:]
        for iconimage, url, name  in match:
                iconimage=iconimage+"|User-Agent=Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0&Cookie=%s"%getCookiesString()
                addDir(name,url,2,iconimage,fanart)
	try:
                pagenum = url2.split('?page=')[1]
                genre = url2.split('?page=')[0]
                curpage = int(pagenum)
                nextpage = curpage + 1
                nextpageurl = genre+'?page='+str(nextpage)
                addDir('Next >> Page '+str(nextpage),nextpageurl,7,icon,fanart)
        except: pass

def GETFULL(url,name):
        link = open_url(url)
        match=re.compile('<li class="first-char"><a  href="(.+?)">(.+?)</a></li>').findall(link)
        for url, name in match:
                url=url+'&page=1'
                addDir(name,url,11,iconimage,fanart)
              
def AZ(url,name):
        link = open_url(url)
        link = link.replace("'",'"')
        match=re.compile('<li title="<div class=".+?"><img src="(.+?)".+?href="(.+?)">(.+?)</a',re.DOTALL).findall(link)
        for iconimage, murl, name in match:
                iconimage=iconimage+"|User-Agent=Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0&Cookie=%s"%getCookiesString()
                name = cleanHex(name)
                addDir(name,murl,2,iconimage,fanart)
        try:
                pagenum = url.split('&page=')
                curpage = int(pagenum[1])
                nextpage = curpage + 1
                nextpageurl = pagenum[0]+'&page='+str(nextpage)
                addDir('Next >> Page '+str(nextpage),nextpageurl,11,icon,fanart)
        except: pass
    
def GETPLAYLINK(name,url,iconimage):
        link = open_url(url)
        if '9cartoon.me' in url:
                stream_url = re.compile('<a href="(.+?)" target="_blank"').findall(link)[-1]
        else:
                holderpage=re.compile('<iframe src="(.+?)" scrolling="no" frameborder="0" width="1008" height="640" allowfullscreen="true"></iframe>').findall(link)[0]
                link = open_url(holderpage)
                stream_url = re.compile('<a href="(.+?)" target="_blank"').findall(link)[-1]
        PLAYLINK(name,stream_url,iconimage)

def PLAYLINK(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.Player ().play(url+"|User-Agent=Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0&Cookie=%s"%getCookiesString(), liz, False)

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

def addDir(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name.strip(), iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name.strip(), iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        
def open_url(url):
        try:
                net.set_cookies(cookie_file)
                link = net.http_GET(url).content
                link = cleanHex(link)
                return link
        except:
                import cloudflare
                cloudflare.createCookie(url,cookie_file,'Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0')
                net.set_cookies(cookie_file)
                link = net.http_GET(url).content
                link = cleanHex(link)
                return link
	
def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    try :return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))
    except:return re.sub("(?i)&#\w+;", fixup, text.encode("ascii", "ignore").encode('utf-8'))
    

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

if mode==None or url==None or len(url)<1: INDEX()
elif mode==1: GETMOVIES(url,name)
elif mode==2: GETEPISODES(url,name,iconimage)
elif mode==5: GETFULL(url,name)
elif mode==6: GETGENRES(url,iconimage)
elif mode==7: GETGENREMOVIES(url)
elif mode==8: SEARCH(url)
elif mode==9: CCATEGORIES()
elif mode==10: ACATEGORIES()
elif mode==11: AZ(url,name)
elif mode==100: GETPLAYLINK(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,os,cloudflare,net
from t0mm0.common.addon import Addon

net = net.Net()
addon_id = 'plugin.video.cartoons8'
selfAddon = xbmcaddon.Addon(id=addon_id)
datapath= xbmc.translatePath(selfAddon.getAddonInfo('profile'))
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
try:os.mkdir(datapath)
except:pass
file_var = open(xbmc.translatePath(os.path.join(datapath, 'cookie.lwp')), "a")
cookie_file = os.path.join(os.path.join(datapath,''), 'cookie.lwp')
base = 'http://cartoons8.me'

def CATEGORIES():
        open_url(base)
        addDir('Top Cartoons','http://cartoons8.me/top/page/1',1,icon,fanart)
	#addDir('Top Movies','http://cartoons8.me/genres/movie/page/1',7,icon,fanart)
	addDir('Top OVAs','http://cartoons8.me/search/page/1?s=ova',9,icon,fanart)
	addDir('Top Dubbed Anime','http://cartoons8.me/search/page/1?s=dubbed',9,icon,fanart)
	addDir('Top Subbed Anime','http://cartoons8.me/search/page/1?s=subbed',9,icon,fanart)
	addDir('Cartoon List','http://cartoons8.me/list/page/1',5,icon,fanart)
	addDir('Most Viewed','http://cartoons8.me/most-viewed/page/1',1,icon,fanart)
	addDir('New','http://cartoons8.me/new/page/1',1,icon,fanart)
	addDir('Genres','http://cartoons8.me',6,icon,fanart)
	addDir('TV Series','http://cartoons8.me/series/page/1',1,icon,fanart)
        addDir('Anime','http://cartoons8.me/anime/page/1',1,icon,fanart)
	addDir('Latest Updates','http://cartoons8.me/latestupdate/page/1',4,icon,fanart)
        addDir('Search','http://cartoons8.me',8,icon,fanart) 
      
def GETMOVIES(url,name):
        pagenum = url.split('page/')
        curpage = int(pagenum[1])
        nextpage = curpage + 1
        nextpageurl = pagenum[0]+'page/'+str(nextpage)
        link = open_url(url)
        match=re.compile('<div class="thumbs"><a href="(.+?)"><img alt=".+?" title="(.+?)" src="(.+?)" /></a></div>').findall(link)
        for url, name, iconimage in match:
                iconimage=iconimage+"|User-Agent=Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0&Cookie=%s"%getCookiesString()
                name = cleanHex(name)
                addDir(name,url,2,iconimage,fanart)
        try:
                addDir('Next >> Page '+str(nextpage),nextpageurl,1,icon,fanart)
        except: pass

def GETEPISODES(url,name,iconimage):
        link = open_url(url)
        match=re.compile('<a  title="(.+?)" href="(.+?)">.+?</a>',re.DOTALL).findall(link)
        match=list(reversed(match))
        for name, url in match:
                if len(match)==1:
                        PLAYLINK(name,url)
                        quit()
                else:
                        

                        name = cleanHex(name)
                        addLink(name,url,100,iconimage,fanart)

def GETLATEST(url,name):
	pagenum = url.split('page/')
        curpage = int(pagenum[1])
        nextpage = curpage + 1
        nextpageurl = pagenum[0]+'page/'+str(nextpage)
        link = open_url(url)
        link=link.replace('\n','')
        match=re.compile('<a style="float: left" title="" href=".+?">(.+?)&nbsp;.+?<a class="cartoon_ep" href="(.+?)">(.+?)</a></span>').findall(link)
        for name, url, episode in match:
                name = cleanHex(name)+' - '+episode
                addLink(name,url,100,icon,fanart)
        if len(match)==1:PLAYLINK(name,url)
	try:
                addDir('Next >> Page '+str(nextpage),nextpageurl,4,icon,fanart)
        except: pass

def GETFULL(url,name):
        pagenum = url.split('page/')
        curpage = int(pagenum[1])
        nextpage = curpage + 1
        nextpageurl = pagenum[0]+'page/'+str(nextpage)
        link = open_url(url)
        link=link.replace('\n','')
        match=re.compile('<a style="float: left" title="" href="(.+?)">(.+?)</a>').findall(link)
        for url, name in match:
                addDir(name,url,2,iconimage,fanart)
        try:
                addDir('Next >> Page '+str(nextpage),nextpageurl,5,icon,fanart)
        except: pass


def GETGENRES(url):
        link = open_url(url)
        match=re.compile('href="(.+?)">(.+?)</a>').findall(link)
        for url, name in match:
                if 'genres' in url:
                        addDir(name,url,7,icon,fanart)

def GETCUSTCAT(url):
	search = url.split('?s=')
	pagenum = url.split('page/')
	pagenum[1] = pagenum[1].strip('?s='+str(search[1]))
	curpage = int(pagenum[1])
        nextpage = curpage + 1
        nextpageurl = pagenum[0]+'page/'+str(nextpage)+'?s='+str(search[1])
        link = open_url(url)
        match=re.compile('<img src="(.+?)".+?<a href="(.+?)".+?"title">(.+?)</span>',re.DOTALL).findall(link)
        for iconimage,url, name in match:
                iconimage=iconimage+"|User-Agent=Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0&Cookie=%s"%getCookiesString()
                addDir(name,url,2,iconimage,fanart)
	try:
                addDir('Next >> Page '+str(nextpage),nextpageurl,9,icon,fanart)
        except: pass
                
def GETGENREMOVIES(url):
	pagenum = url
        link = open_url(url)
        match=re.compile('<img src="(.+?)".+?<a href="(.+?)".+?"title">(.+?)</span>',re.DOTALL).findall(link)
        for iconimage,url, name in match:
                iconimage=iconimage+"|User-AgentMozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0&Cookie=%s"%getCookiesString()
                addDir(name,url,2,iconimage,fanart)  #
	try:
               addDir('Next >> Page 2',pagenum+'/'+'2',10,icon,fanart)
        except: pass

def GETGENRENEXT(url):
	pagenum = url.split('/')
	curpage = int(pagenum[5])
	nextpage = curpage + 1
	nextpageurl = 'http://cartoons8.me/genres/'+str(pagenum[4])+'/'+str(nextpage)
        link = open_url(url)
        match=re.compile('<img src="(.+?)".+?<a href="(.+?)".+?"title">(.+?)</span>',re.DOTALL).findall(link)
        for iconimage,url, name in match:
                iconimage=iconimage+"|User-Agent=Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0&Cookie=%s"%getCookiesString()
                addDir(name,url,2,iconimage,fanart)  
	try:
                addDir('Next >> Page '+str(nextpage),nextpageurl,10,icon,fanart)
        except: pass  

def SEARCH():
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'Search Cartoons')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
    if len(search_entered)>1:
        url = 'http://cartoons8.me/search/page/1?s='+ search_entered
        GETCUSTCAT(url)

def getCookiesString():
    cookieString=""
    import cookielib
    try:
        cookieJar = cookielib.LWPCookieJar()
        cookieJar.load(cookie_file,ignore_discard=True)
        #print cookieJar
        for index, cookie in enumerate(cookieJar):
            cookieString+=cookie.name + "=" + cookie.value +";"
    except: 
        import sys,traceback
        traceback.print_exc(file=sys.stdout)
    #print 'cookieString',cookieString
    return cookieString
        
def PLAYLINK(name,url):
        link = open_url(url)
        posturl = re.compile('url: "(.+?)",').findall(link)[0]
        postparams = re.compile("data: '(.+?)',").findall(link)[0]
        req = urllib2.Request(posturl,postparams)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        if 'redirector' in link:
                stream_url = re.compile('<a href="(.+?)" target=".+?" rel=".+?">.+?</a>').findall(link)[-1]
        elif 'dscw' in link:
                vid = re.compile('id="dscw" value="(.+?)"').findall(link)[0]
                url='https://docs.google.com/get_video_info?docid='+vid
                link = open_url(url)
                stream_url = urllib.unquote(urllib.unquote(link)).split('|')[1]
        else:
                stream_url = 'http://cartoons8.me/vload/?token='+re.compile('<a href="http://cartoons8.me/vload/\?token=(.+?)"').findall(link)[-1]
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.Player ().play(stream_url+"|User-Agent=Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0&Cookie=%s"%getCookiesString(), liz, False)

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

def addDir(name,url,mode,iconimage,description=''):
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

if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: GETMOVIES(url,name)
elif mode==2: GETEPISODES(url,name,iconimage)
elif mode==3: SEARCH()
elif mode==4: GETLATEST(url,name)
elif mode==5: GETFULL(url,name)
elif mode==6: GETGENRES(url)
elif mode==7: GETGENREMOVIES(url)
elif mode==8: SEARCH()
elif mode==9: GETCUSTCAT(url)
elif mode==10: GETGENRENEXT(url)
elif mode==100: PLAYLINK(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))


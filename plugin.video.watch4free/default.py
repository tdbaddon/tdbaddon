import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,sys,xbmc,xbmcaddon,os,urlparse,random
from t0mm0.common.addon import Addon
from metahandler import metahandlers
from t0mm0.common.net import Net
import time
addon_id = 'plugin.video.watch4free'
try:
    import StorageServer
except:
    import storageserverdummy as StorageServer
cache = StorageServer.StorageServer(addon_id)
from resources.lib.libraries import control
from resources.lib.libraries import client

selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
icon2 = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'art/tv.png'))
icon3 = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'art/movies.png'))
icon4 = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'art/search.png'))
icon5 = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'art/play.png'))
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/art/'))
metaset = selfAddon.getSetting('enable_meta')
addon = Addon(addon_id, sys.argv)
net = Net()
basepage = "/date/1"
baseurl2 = "http://www.watchfree.to"
def CATEGORIES():
        addDir2('[COLOR lime]TV Shows [/COLOR]','http://www.watchfree.to/?tv=&page=1',1,icon2,fanart)
        addDir2('[COLOR lime]Movies [/COLOR]','http://www.watchfree.to/?page=1',3,icon3,fanart)

        addDir2('[COLOR yellow]>>> Search[/COLOR]','http://www.vodlockerx.com/tv-shows',4,icon4,fanart)

        

def GETINDEXMOVIES(url,name):
	try:
			actualpage = str(url)
			
			pagenum = actualpage.split('?page=')
			
			curpage = int(pagenum[1])
			nextpage = curpage + 1
			nextpageurl = pagenum[0]+'?page='+str(nextpage)
	except:pass
        link = open_url(url)
        match=re.compile('<div class="item"><a href="(.+?)" title="(.+?)">').findall(link)
        
        metaset = selfAddon.getSetting('enable_meta')
        
        
        for url,name in match:
                name=cleanHex(name)
                name=re.sub('Full Movie Watch Online','',name)
                name=re.sub('Watch','',name)
                name=re.sub('online','',name)
                name=re.sub('free','',name)
                name=re.sub('putlocker','',name)
                name=re.sub('xmovie8','',name)
                name=re.sub('xmovies8','',name)
				
                url = "http://www.watchfree.to" + url
                if metaset=='false':
                        try:
                                addDir2(name,url,99,iconimage,fanart)
                        except:pass
                else:
                        try:
                                addDirM(name,url,99,'',len(match),isFolder=True)
                        except:pass
	try:
               
					addLink('NEXT >>',nextpageurl,3,icon,'')
					
	except: pass						

def GETINDEX(url,name):
	try:
			actualpage = str(url)
			
			pagenum = actualpage.split('?tv=&page=')
			
			curpage = int(pagenum[1])
			nextpage = curpage + 1
			nextpageurl = pagenum[0]+'?tv=&page='+str(nextpage)
	except:pass
        link = open_url(url)
        match=re.compile('<div class="item"><a href="(.+?)" title="(.+?)">').findall(link)
        
        metaset = selfAddon.getSetting('enable_meta')
        
        
        for url,name in match:
                name=cleanHex(name)
                name=re.sub('Full Movie Watch Online','',name)
                name=re.sub('Watch','',name)
                name=re.sub('online','',name)
                name=re.sub('free','',name)
                name=re.sub('putlocker','',name)
                name=re.sub('xmovie8','',name)
                name=re.sub('xmovies8','',name)
				
                url = "http://www.watchfree.to" + url
                if metaset=='false':
                        try:
                                addDir2(name,url,2,iconimage,fanart)
                        except:pass
                else:
                        try:
                                addDir(name,url,2,'',len(match),isFolder=True)
                        except:pass
	try:
               
					addLink('NEXT >>',nextpageurl,1,icon,'')
					
	except: pass						


def GETSEASONS(url,name,iconimage):
	try:
			actualpage = str(url)
			actualpage = re.sub('#genre','',actualpage)
			pagenum = actualpage.split('?page=')
			
			curpage = int(pagenum[1])
			nextpage = curpage + 1
			nextpageurl = pagenum[0]+'?page='+str(nextpage)+'#genre'
	except:pass
        iconimage = iconimage
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('class="season-toggle" href="(.+?)">(.+?)<span').findall(link)
        
        metaset = selfAddon.getSetting('enable_meta')
        
        
        for url,name in match:
                name=cleanHex(name)
                name=re.sub('Full Movie Watch Online','',name)
                name=re.sub('watch','',name)
                name=re.sub('online','',name)
                name=re.sub('free','',name)
                name=re.sub('putlocker','',name)
                name=re.sub('xmovie8','',name)
                name=re.sub('xmovies8','',name)
				
                url = "http://www.watchfree.to" + url
                if metaset=='false':
                        try:
                                addDir2(name,url,6,icon,fanart)
                        except:pass
                else:
                        try:
                                addDir2(name,url,6,icon5,fanart)
                        except:pass
	try:
               
					addLink('NEXT >>',nextpageurl,1,icon,'')
					
	except: pass						

def GETEP(url,name,iconimage):
	try:
			actualpage = str(url)
			actualpage = re.sub('#genre','',actualpage)
			pagenum = actualpage.split('?page=')
			
			curpage = int(pagenum[1])
			nextpage = curpage + 1
			nextpageurl = pagenum[0]+'?page='+str(nextpage)+'#genre'
	except:pass
        iconimage = iconimage
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<div class="tv_episode_item">\s*<a href="(.+?)">(.+?)<span class="tv_episode_name">(.+?)</span>').findall(link)
        
        metaset = selfAddon.getSetting('enable_meta')
        
        
        for url,ep,name in match:
                name=cleanHex(name)
                name=re.sub('Full Movie Watch Online','',name)
                name=re.sub('watch','',name)
                name=re.sub('online','',name)
                name=re.sub('free','',name)
                name=re.sub('putlocker','',name)
                name=re.sub('xmovie8','',name)
                name=re.sub('xmovies8','',name)
				
                url = "http://www.watchfree.to" + url
                if metaset=='false':
                        try:
                                addDir2(ep + " " + name,url,99,icon,fanart)
                        except:pass
                else:
                        try:
                                addDir2(ep + " " + name,url,99,icon5,fanart)
                        except:pass
	try:
               
					addLink('NEXT >>',nextpageurl,1,icon,'')
					
	except: pass						

		
def GETLINKS(url,name,iconimage):
        storedname = name
        resolved=None
        randomitem = []
        link=open_url(url)
        match=re.compile('<a href="(.+?)" rel="nofollow" title="(.+?)" target="_blank">').findall(link)
        match2=re.compile('<a href=".+?" rel="nofollow" title="(.+?)" target="_blank">').findall(link)
        # match2.group()
        originalep = name
        autoplay = selfAddon.getSetting('enable_autoplay')
        for url,name in match:
           url = "http://www.watchfree.to" + url
           randomitem.append([url, name])
        index = random.randrange(1, len(randomitem))
        playrandom = randomitem[index][0]
		
        for url,name in match:
				if xbmc.Player().isPlaying(): return
				if autoplay=='false':
					url = "http://www.watchfree.to" + url
					url2 = "autoplay"
					host=url.split('/')[2].replace('www.','').capitalize()
					addLink(originalep +' >>> ' ,url,100,icon5,fanart)
				else:
					if not xbmc.Player().isPlaying():
						try:
							stdurl = url
							url = "http://www.watchfree.to" + url
							index = random.randrange(1, len(match))
							playrandom = randomitem[index][0]
							progressDialog = control.progressDialog
							progressDialog.create(control.addonInfo('name'), '')
							progressDialog.update(0, 'Trying: sources', 'Please wait...')
							req = urllib2.Request(playrandom)
							req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
							response = urllib2.urlopen(req)
							link=response.geturl()
							xbmc.sleep(1000)
							liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": storedname } )
							stream_url = urlresolver.HostedMediaFile(link).resolve()
							xbmc.Player ().play(stream_url, liz, False)
							
							xbmc.sleep(1000)
							addDir('Testlog:'+url,'',8,'','')
						except:addDir(url +' not working','',8,'','')
	addDir('Press Here to Exit','',8,'','')
						 
		# while not xbmc.Player().isPlaying():
			# index = random.randrange(0, len(randomitem))
			# playrandom = randomitem[index][0]
			# progressDialog = control.progressDialog
			# progressDialog.create(control.addonInfo('name'), '')
			# progressDialog.update(1, 'Please Wait...', 'Auto playing sources...')

									
			# try:
				
					
				# req = urllib2.Request(playrandom)
				# req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
				# response = urllib2.urlopen(req)
				# link=response.geturl()
				# stream_url = urlresolver.HostedMediaFile(link).resolve()
				# xbmc.Player().play(stream_url)
			
				# addDir2('Press Back to exit','',8,'','')
		 
			# except: pass
			

	
	
	
	
	# ------------------------------------------------------- MEGA SEARCH --------------------------------------------------------
 # ------------------------------------------------------- MEGA SEARCH --------------------------------------------------------
 # ------------------------------------------------------- MEGA SEARCH --------------------------------------------------------
 # ------------------------------------------------------- MEGA SEARCH --------------------------------------------------------
 # ------------------------------------------------------- MEGA SEARCH --------------------------------------------------------
 # ------------------------------------------------------- MEGA SEARCH -------------------------------------------------------- 
def SEARCH():
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'Search 4 Free')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
    if len(search_entered)>1:
    
    	url = 'http://www.watchfree.to/?keyword=' + search_entered
        

        GETINDEX(url,name)


def sourcesResolve(self, url, provider):
        try:
            provider = provider.lower()

            if not provider.endswith(('_mv', '_tv', '_mv_tv')):
                sourceDict = []
                for package, name, is_pkg in pkgutil.walk_packages(__path__): sourceDict.append((name, is_pkg))
                provider = [i[0] for i in sourceDict if i[1] == False and i[0].startswith(provider + '_')][0]

            source = __import__(provider, globals(), locals(), [], -1).source()
            url = source.resolve(url)

            try: headers = dict(urlparse.parse_qsl(url.rsplit('|', 1)[1]))
            except: headers = dict('')

            result = client.request(url.split('|')[0], headers=headers, output='chunk', timeout='20')
            if result == None: raise Exception()
            url = url
            return url
        except:
            return		
def PLAYLINK(name,url,iconimage):
			try:
						
				 req = urllib2.Request(url)
				 req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
				 response = urllib2.urlopen(req)
				 link=response.geturl()
				 stream_url = urlresolver.HostedMediaFile(link).resolve()
				 xbmc.Player().play(stream_url)
			except: xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Cannot play the link![/B][/COLOR],[COLOR lime][B]Try another one from the list!![/B][/COLOR],2000,"")")
	
       
        
def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))

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

def addDir2(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(name,url,mode,iconimage,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        liz.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
def addDirM(name,url,mode,iconimage,itemcount,isFolder=False):
        try:
          if not 'COLOR' in name:
            splitName=name.partition('(')
            simplename=""
            simpleyear=""
            if len(splitName)>0:
                simplename=splitName[0]
                simpleyear=splitName[2].partition(')')
            if len(simpleyear)>0:
                simpleyear=simpleyear[0]
            mg = metahandlers.MetaData()
          
            meta = mg.get_meta('movie', name=simplename ,year=simpleyear)
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
            ok=True
            liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
            liz.setInfo( type="Video", infoLabels= meta )
            liz.setProperty("IsPlayable","true")
            contextMenuItems = []
            contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
            liz.addContextMenuItems(contextMenuItems, replaceItems=False)
            if not meta['backdrop_url'] == '': liz.setProperty('fanart_image', meta['backdrop_url'])
            else: liz.setProperty('fanart_image', fanart)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder,totalItems=itemcount)
            return ok


		   
        except:
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
            ok=True
            liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
            liz.setInfo( type="Video", infoLabels={ "Title": name } )
            liz.setProperty('fanart_image', fanart)
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
            return ok
def addDir(name,url,mode,iconimage,itemcount,isFolder=False):
        try:
          if not 'COLOR' in name:
            splitName=name.partition('(')
            simplename=""
            simpleyear=""
            if len(splitName)>0:
                simplename=splitName[0]
                simpleyear=splitName[2].partition(')')
            if len(simpleyear)>0:
                simpleyear=simpleyear[0]
            mg = metahandlers.MetaData()
          
            meta = mg.get_meta('tvshow', name=simplename ,year=simpleyear)
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
            ok=True
            liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
            liz.setInfo( type="Video", infoLabels= meta )
            liz.setProperty("IsPlayable","true")
            contextMenuItems = []
            contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
            liz.addContextMenuItems(contextMenuItems, replaceItems=False)
            if not meta['backdrop_url'] == '': liz.setProperty('fanart_image', meta['backdrop_url'])
            else: liz.setProperty('fanart_image', fanart)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder,totalItems=itemcount)
            return ok


		   
        except:
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
            ok=True
            liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
            liz.setInfo( type="Video", infoLabels={ "Title": name } )
            liz.setProperty('fanart_image', fanart)
            liz.setProperty("IsPlayable","true")
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

elif mode==1: GETINDEX(url,name)
elif mode==3: GETINDEXMOVIES(url,name)
elif mode==4: SEARCH()

elif mode==2: GETSEASONS(url,name,iconimage)
elif mode==6: GETEP(url,name,iconimage)

elif mode==99: GETLINKS(url,name,iconimage)
elif mode==100: PLAYLINK(name,url,iconimage)


xbmcplugin.endOfDirectory(int(sys.argv[1]))


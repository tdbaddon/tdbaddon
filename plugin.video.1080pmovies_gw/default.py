import urllib2, urllib, xbmcgui, xbmcplugin, xbmc, re, sys, os, dandy
import xbmcaddon
from addon.common.addon import Addon
import urlresolver
import requests
#A special thank you - Many of my addons contain code originally written by Mucky Duck
s = requests.session() 
addon_id='plugin.video.1080pmovies_gw'
selfAddon = xbmcaddon.Addon(id=addon_id)
datapath= xbmc.translatePath(selfAddon.getAddonInfo('profile'))
addon = Addon(addon_id, sys.argv)
addon_name = selfAddon.getAddonInfo('name')
ART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/icons/'))
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
BASEURL = 'https://www.filmapik.tv'
enable_shows = addon.get_setting('enable_shows')

def MENU():
    addDir('[B][COLOR white]Box Office[/COLOR][/B]',BASEURL + '/category/box-office',5,ART + 'boxoffice.jpg',FANART,'')
    addDir('[B][COLOR white]Latest Movies[/COLOR][/B]',BASEURL + '/year',5,ART + 'lat_mov.jpg',FANART,'')
    addDir('[B][COLOR white]Latest Uploaded[/COLOR][/B]',BASEURL + '/latest',5,ART + 'latest_up.jpg',FANART,'')
    addDir('[B][COLOR white]Popular[/COLOR][/B]',BASEURL + '/popular',5,ART + 'pop.jpg',FANART,'')
    addDir('[B][COLOR white]IMDB Top Rated Movies[/COLOR][/B]',BASEURL + '/imdb/',5,ART + 'tr_imdb.jpg',FANART,'')
    addDir('[B][COLOR white]IMDB Popular Movies[/COLOR][/B]',BASEURL + '/popularimdb',5,ART + 'pop_imdb.jpg',FANART,'')
    addDir('[B][COLOR white]Genres[/COLOR][/B]',BASEURL,3,ART + 'bygenre.jpg',FANART,'')
    addDir('[B][COLOR white]Release Year[/COLOR][/B]',BASEURL,4,ART + 'by_year.jpg',FANART,'')
    if enable_shows == 'true':
		addDir('[B][COLOR white]TV Shows[/COLOR][/B]',BASEURL + '/tvshows-genre/west-series',5,ART + 'tvshows.jpg',FANART,'')
    addDir('[B][COLOR red]Search[/COLOR][/B]','url',6,ART + 'search.jpg',FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def Get_content(url):
    OPEN = Open_Url(url)
    Regex = re.compile('class="item">.+?href="(.+?)".+?<img src="(.+?)".+?<h2>(.+?)</h2>.+?<span class="ttx">(.+?)<div',re.DOTALL).findall(OPEN)
    for url,icon,name,desc in Regex:
            icon = icon.replace('w185','w300_and_h450_bestv2')
            name = name.replace('&#8217;','\'').replace('#038;','').replace('\\xc3\\xa9','e').replace('&#8211;','-')
            if '/tvshows/' in url:
                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,9,icon,FANART,desc)
            else:
                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url+'/play',100,icon,FANART,desc)
    np = re.compile('<div class="pag_b"><a href="(.+?)"',re.DOTALL).findall(OPEN)
    for url in np:
        addDir('[B][COLOR red]Next Page>>>[/COLOR][/B]',url,5,ART + 'nextpage.jpg',FANART,'')
    setView('movies', 'movie-view')

def Get_Genres(url):
    OPEN = Open_Url(url)
    Regex = re.compile('Kategori</a>(.+?)</ul>',re.DOTALL).findall(OPEN)[0]
    Regex2 = re.compile('<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(str(Regex))
    for url,name in Regex2:
        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,BASEURL+url,5,ART + 'bygenre.jpg',FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def Get_Years(url):
    OPEN = Open_Url(url)
    Regex = re.compile('Tahun</a>(.+?)</ul>',re.DOTALL).findall(OPEN)[1]
    Regex2 = re.compile('href="(.+?)">(.+?)</a></li>',re.DOTALL).findall(str(Regex))
    for url,name in Regex2:
        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,BASEURL+url,5,ART + 'by_year.jpg',FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')


def Get_show_content(name,url):
    OPEN = Open_Url(url)
    show=name
    Regex = re.compile('<div class="numerando">(.+?)</div>.+?<a href="(.+?)"',re.DOTALL).findall(OPEN)
    for epis,url in Regex:
            name = show + '[B][COLOR white] - ' + epis +'[/B][/COLOR]'
            addDir(name,url,100,iconimage,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')


# def Get_links(url):
    # OPEN = Open_Url(url)
    # Regex = re.compile('<iframe src="(.+?)"',re.DOTALL).findall(OPEN)[0]
    # source = Open_Url(Regex)
    # mainlinks = re.compile('"label":"(.+?)".+?"file":"(.+?)"',re.DOTALL).findall(source)
    # for name2,url in mainlinks:
        # if 'Indonesia' not in name2:
            # url = url.replace('\/','/').replace(' ','%20')
            # addDir('[B][COLOR white]Play in %s[/COLOR][/B]' %name2,url,100,iconimage,FANART,name)
    # links = re.compile("Onclick=.+?'(.+?)'",re.DOTALL).findall(source)
    # for url in links:
        # if 'googleapis' not in url:
            # name2 = url.split('//')[1].replace('www.','')
            # name2 = name2.split('/')[0].split('.')[0].title()
            # if urlresolver.HostedMediaFile(url).valid_url():
                # name2 = name2.replace('Oload','Openload')
                # addDir('[B][COLOR white]%s[/COLOR][/B]' %name2,url,100,iconimage,FANART,name)
    # xbmc.executebuiltin('Container.SetViewMode(50)')
    
def Search():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                url = BASEURL + '/?s=' + search
                Get_content(url)


def setView(content, viewType):
    ''' Why recode whats allready written and works well,
    Thanks go to Eldrado for it '''
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if addon.get_setting('auto-view') == 'true':

        print addon.get_setting(viewType)
        if addon.get_setting(viewType) == 'Info':
            VT = '504'
        elif addon.get_setting(viewType) == 'Info2':
            VT = '503'
        elif addon.get_setting(viewType) == 'Info3':
            VT = '515'
        elif addon.get_setting(viewType) == 'Fanart':
            VT = '508'
        elif addon.get_setting(viewType) == 'Poster Wrap':
            VT = '501'
        elif addon.get_setting(viewType) == 'Big List':
            VT = '51'
        elif addon.get_setting(viewType) == 'Low List':
            VT = '724'
        elif addon.get_setting(viewType) == 'List':
            VT = '50'
        elif addon.get_setting(viewType) == 'Default Menu View':
            VT = addon.get_setting('default-view1')
        elif addon.get_setting(viewType) == 'Default TV Shows View':
            VT = addon.get_setting('default-view2')
        elif addon.get_setting(viewType) == 'Default Episodes View':
            VT = addon.get_setting('default-view3')
        elif addon.get_setting(viewType) == 'Default Movies View':
            VT = addon.get_setting('default-view4')
        elif addon.get_setting(viewType) == 'Default Docs View':
            VT = addon.get_setting('default-view5')
        elif addon.get_setting(viewType) == 'Default Cartoons View':
            VT = addon.get_setting('default-view6')
        elif addon.get_setting(viewType) == 'Default Anime View':
            VT = addon.get_setting('default-view7')

        print viewType
        print VT
        
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ( int(VT) ) )

    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )
    
def RESOLVE(url):
    res_quality = []
    stream_url = []
    quality = ''
    OPEN = Open_Url(url)
    Regex = re.compile('<iframe src="(.+?)"',re.DOTALL).findall(OPEN)[0]
    source = Open_Url(Regex)
    match = re.compile('"label":"(.+?)".+?"file":"(.+?)"').findall(source)
    for label,link in match:
            quality = '[B][COLOR white]%s[/COLOR][/B]' %label
            res_quality.append(quality)
            stream_url.append(link)
    if len(match) >1:
            dialog = xbmcgui.Dialog()
            ret = dialog.select('Please Select Quality',res_quality)
            if ret == -1:
                return
            elif ret > -1:
                    url = stream_url[ret]
    else:
        url = re.compile('"file":"(.+?)"').findall(OPEN)[0]
    url = url.replace('\/','/')
    stream=urlresolver.HostedMediaFile(url).resolve()
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={"Title": name})
    liz.setProperty("IsPlayable","true")
    liz.setPath(stream)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)



        
def Open_Url(url):
    headers = {}
    headers['User-Agent'] = User_Agent
    link = s.get(url, headers=headers).text
    link = link.encode('ascii', 'ignore')
    return link
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
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


                
def addDir(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
	liz.setProperty('fanart_image', fanart)
	if mode==100:
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def OPEN_UrlRez():
        xbmcaddon.Addon('script.module.urlresolver').openSettings()

params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None




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
try:
	description=urllib.unquote_plus(params["description"])
except:
	pass

if mode==None or url==None or len(url)<1 : MENU()
elif mode == 3 : Get_Genres(url)
elif mode == 4 : Get_Years(url)
elif mode == 5 : Get_content(url) 
elif mode == 6 : Search()
elif mode == 9 : Get_show_content(name,url)
elif mode == 10 : Get_links(url)
elif mode == 200: OPEN_UrlRez()
elif mode ==100: RESOLVE(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))

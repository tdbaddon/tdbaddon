# -*- coding: utf-8 -*-
import urllib2, urllib, xbmcgui, xbmcplugin, xbmc, re, sys, dandy,xbmcaddon
import requests
from addon.common.addon import Addon
from metahandler import metahandlers
s = requests.session() 
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
addon_id='plugin.video.filmcube'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
addon_name = selfAddon.getAddonInfo('name')
ADDON      = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo('path')
ICON = ADDON.getAddonInfo('icon')
FANART = ADDON.getAddonInfo('fanart')
PATH = 'filmcube'
VERSION = ADDON.getAddonInfo('version')
ART = ADDON_PATH + "/resources/icons/"
BASEURL = 'https://flenix.net'
metaset = selfAddon.getSetting('enable_meta')
metaget = metahandlers.MetaData()


def Main_menu():
    addDir('[B][COLOR white]Trending Movies[/COLOR][/B]',BASEURL+'/movies/trending/',5,ART + 'trend_mov.jpg',FANART,'')
    addDir('[B][COLOR white]New Releases[/COLOR][/B]',BASEURL+'/movies/releases/',5,ART + 'mov_new.jpg',FANART,'')
    addDir('[B][COLOR white]Movies in HD[/COLOR][/B]',BASEURL+'/movies/hd/',5,ART + 'mov_hd.jpg',FANART,'')
    addDir('[B][COLOR white]All Movies[/COLOR][/B]',BASEURL+'/movies/',5,ART + 'allmov.jpg',FANART,'')
    addDir('[B][COLOR white]Genres[/COLOR][/B]',BASEURL,3,ART + 'genres.jpg',FANART,'')
    addDir('[B][COLOR white]Release Year[/COLOR][/B]',BASEURL,4,ART + 'rel_year.jpg',FANART,'')
    # addDir('[B][COLOR white]Trending TV[/COLOR][/B]',BASEURL+'/tv/trending/',5,ART + 'ttv.jpg',FANART,'')
    # addDir('[B][COLOR white]New Releases TV[/COLOR][/B]',BASEURL+'/tv/releases/',5,ART + 'mov_new.jpg',FANART,'')
    # addDir('[B][COLOR white]All TV Shows[/COLOR][/B]',BASEURL+'/tv/',5,ART + 'all_tv.jpg',FANART,'')
    addDir('[B][COLOR white]Search All[/COLOR][/B]','url',6,ART + 'search.jpg',FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

    
def Get_Genres(url):
    OPEN = Open_Url(url)
    Regex = re.compile('<span>Movies</span>.+?<ul class="reset">(.+?)<span>TV Shows</span>',re.DOTALL).findall(OPEN)
    Regex2 = re.compile('href="(.+?)">(.+?)</a>',re.DOTALL).findall(str(Regex))
    for url,name in Regex2:
        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,BASEURL+url,5,ART + 'genres.jpg',FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def Get_Years(url):
    OPEN = Open_Url(url)
    Regex = re.compile('<span>Movies</span>.+?<div>Sort by year:</div>(.+?)</li>',re.DOTALL).findall(OPEN)
    Regex2 = re.compile('href="(.+?)">(.+?)</a>',re.DOTALL).findall(str(Regex))
    for url,name in Regex2:
            addDir('[B][COLOR white]%s[/COLOR][/B]' %name,BASEURL+url,5,ART + 'rel_year.jpg',FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')
	
def Get_content(url):    
    OPEN = Open_Url(url)
    Regex = re.compile('<div class="poster item-flip">.+?src="(.+?)".+?<div class="title">(.+?)</div>.+?<span>(.+?)</span>.+?href="(.+?)"',re.DOTALL).findall(OPEN)
    for icon,title,year,url in Regex:
            items = len(Regex)
            name = title + ' (' + year + ')'
            name = name.replace('amp;','')
            if '/tv/' in  url:
                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,9,icon,FANART,'')
            else:
                if metaset=='true':
                    addDir2('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,items)
                else:
                    addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,FANART,'')
    np = re.compile('<span>[0-9]</span> <a href="(.+?)"',re.DOTALL).findall(OPEN)
    for url in np:
        addDir('[B][COLOR red]Next Page>>>[/COLOR][/B]',url,5,ART + 'next.jpg',FANART,'')
    setView('movies', 'movie-view')

def Get_links(name,url):
    referer = url
    headers = {'Host': 'flenix.net', 'User-Agent': User_Agent, 'Referer': referer}
    links=requests.get(url,headers=headers,allow_redirects=True).content
    Regex = re.compile('file:"(.+?)"',re.DOTALL).findall(links)
    for url in Regex:
        url = 'https:' + url
        name=url
        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,ART + 'rel_year.jpg',FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')
    
def Get_show_content(name,url):
    referer = url
    epis_numb=0
    headers = {'Host': 'flenix.net', 'User-Agent': User_Agent, 'Referer': referer}
    OPEN = Open_Url(url)
    holderpage = re.compile('<iframe id="movie" class="tcontainer" src="(.+?)"').findall(OPEN)[0]
    links=requests.get(holderpage,headers=headers,allow_redirects=True).content
    Regex = re.compile('/video/t/(.+?)"',re.DOTALL).findall(links)
    for url in Regex:
        epis_numb = epis_numb +1
        name2 = epis_numb
        addDir('[B][COLOR white]Episode %s - [/COLOR][/B]' %name2 + name,'https://hdgo.cx/video/t/%s'%url,101,iconimage,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')
    


def Search():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                url = BASEURL + '/index.php?do=search&story=' + search
                Get_content(url)
    

    
def Open_Url(url):
    headers = {}
    headers['User-Agent'] = User_Agent
    link = s.get(url, headers=headers).text
    link = link.encode('ascii', 'ignore')
    return link
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def addDir(name,url,mode,iconimage,fanart,description):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
    liz.setProperty('fanart_image', fanart)
    if mode==100 or mode==101:
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    else:
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addDir2(name,url,mode,iconimage,itemcount):
        name = name.replace('[B][COLOR white]','').replace('[/COLOR][/B]','')
        splitName=name.partition('(')
        simplename=""
        simpleyear=""
        if len(splitName)>0:
            simplename=splitName[0]
            simpleyear=splitName[2].partition(')')
        if len(simpleyear)>0:
            simpleyear=simpleyear[0]
        meta = metaget.get_meta('movie',simplename,simpleyear)
        if meta['cover_url']=='':
            try:
                meta['cover_url']=iconimage
            except:
                meta['cover_url']=iconimage
        name = '[B][COLOR white]' + name + '[/COLOR][/B]'
        meta['title'] = name
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
        liz.setInfo( type="Video", infoLabels= meta )
        contextMenuItems = []
        contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
        if meta['trailer']:
                contextMenuItems.append(('Play Trailer', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 99, 'url':meta['trailer']})))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if not meta['backdrop_url'] == '':
                liz.setProperty('fanart_image', meta['backdrop_url'])
        else: liz.setProperty('fanart_image',FANART)
        if mode==100 or mode==101:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=itemcount)
        else:
             ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
        return ok

def notification(title, message, icon):
        addon.show_small_popup( addon.get_name(), message.title(), 5000, icon)
        return
    
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

def PT(url):
        addon.log('Play Trailer %s' % url)
        notification( addon.get_name(), 'fetching trailer', addon.get_icon())
        xbmc.executebuiltin("PlayMedia(%s)"%url)
    
def resolve(url):
    referer = url
    headers = {'Host': 'flenix.net', 'User-Agent': User_Agent, 'Referer': referer}
    try:
        links=requests.get(url,headers=headers,allow_redirects=True).content
        stream_url = re.compile('file:"(.+?)"',re.DOTALL).findall(links)[0]
        stream_url = 'https:' + stream_url
    except:
        OPEN = Open_Url(url)
        holderpage = re.compile('<iframe id="movie" class="tcontainer" src="(.+?)"').findall(OPEN)[0]
        links=requests.get(holderpage,headers=headers,allow_redirects=True).content
        stream_url = re.compile("url: '(.+?)'",re.DOTALL).findall(links)[-1]
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": description})
    liz.setProperty("IsPlayable","true")
    liz.setPath(stream_url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

# def resolve(url):
    # liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    # liz.setInfo(type="Video", infoLabels={"Title": description})
    # liz.setProperty("IsPlayable","true")
    # liz.setPath(url)
    # xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)


def resolve_tv(url):
    referer = url
    headers = {'Host': 'flenix.net', 'User-Agent': User_Agent, 'Referer': referer}
    links=requests.get(url,headers=headers,allow_redirects=True).content
    # dialog = xbmcgui.Dialog()
    # servers = dialog.yesno('Quality', 'Please Choose your Link', yeslabel='HD', nolabel='SD')
    # if servers:
            # url = re.compile("{url: '(.+?)'",re.DOTALL).findall(links)[-1]

    # else:
            # url = re.compile("{url: '(.+?)'",re.DOTALL).findall(links)[0]
    res_quality = []###removed as middle rezz dont play if HD dont 
    stream_url = []
    quality = ''
    match = re.compile("{url: '(.+?)'").findall(links)
    for link in match:
            if '/1/' in link:
                label = '360p'
            if '/2/' in link:
                label = '480p'
            if '/3/' in link:
                label = '720p'
            if '/4/' in link:
                label = '1080p'                 
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
        url = re.compile("{url: '(.+?)'").findall(OPEN)[0]
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": description})
    liz.setProperty("IsPlayable","true")
    liz.setPath(url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)


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
iconimage=None
mode=None
fanart=None
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
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
        
        
print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
#########################################################
	
if mode == None: Main_menu()
elif mode == 3: Get_Genres(url)
elif mode == 4: Get_Years(url)
elif mode == 5 : Get_content(url)
elif mode == 6 : Search()
elif mode == 9 : Get_show_content(name,url)
elif mode == 10 : Get_links(name,url)
elif mode == 99: PT(url)
elif mode == 100 : resolve(url)
elif mode == 101 : resolve_tv(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))

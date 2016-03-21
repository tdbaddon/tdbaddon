import sys,urllib,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os
import requests
from addon.common.addon import Addon
from metahandler import metahandlers

#M4U Add-on Created By Mucky Duck (3/2016)

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
addon_id='plugin.video.mdm4u'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
metaset = selfAddon.getSetting('enable_meta')
metaget = metahandlers.MetaData()
baseurl = 'http://m4ufree.info'




def CAT():
        addDir('[B][COLOR white]LATEST ADDED[/COLOR][/B]',baseurl+'/newupdate',1,icon,fanart,'')
        addDir('[B][COLOR white]MOST VIEWED[/COLOR][/B]',baseurl+'/top-view',1,icon,fanart,'')
        addDir('[B][COLOR white]HOT MOVIES[/COLOR][/B]',baseurl,1,icon,fanart,'')
        addDir('[B][COLOR white]BEST 100[/COLOR][/B]',baseurl+'/best-100-movies',1,icon,fanart,'')
        addDir('[B][COLOR white]SEARCH[/COLOR][/B]','url',4,icon,fanart,'')
        addDir('[B][COLOR white]GENRE[/COLOR][/B]',baseurl,5,icon,fanart,'')
        addDir('[B][COLOR white]YEAR[/COLOR][/B]',baseurl,6,icon,fanart,'')
        addDir('[B][COLOR white]TV[/COLOR][/B]','url',8,icon,fanart,'')




def TV():
        addDir('[B][COLOR white]LATEST ADDED[/COLOR][/B]',baseurl+'/tvs-newupdate',11,icon,fanart,'')
        addDir('[B][COLOR white]MOST VIEWED[/COLOR][/B]',baseurl+'/top-view-tvshow',11,icon,fanart,'')
        addDir('[B][COLOR white]SEARCH[/COLOR][/B]','url',10,icon,fanart,'')
        addDir('[B][COLOR white]GENRE[/COLOR][/B]',baseurl,9,icon,fanart,'')
        addDir('[B][COLOR white]ALL[/COLOR][/B]',baseurl+'/tvshow',11,icon,fanart,'')




def INDEX(url):
        link = OPEN_URL(url)
        all_videos = regex_get_all(link, '"item"', 'clear:both')
        items = len(all_videos)
        for a in all_videos:
                name = regex_from_to(a, 'cite>', '<')
                name = addon.unescape(name)
                name = name.encode('ascii', 'ignore').decode('ascii')
                qual = regex_from_to(a, 'class="h3-quality".*?>', '<')#.replace('- Quality:','[COLOR gold]- Quality:[/COLOR]')
                url = regex_from_to(a, 'href="', '"')
                thumb = regex_from_to(a, 'src=', 'alt=').replace(' ','')
                epi = regex_from_to(a, '"h4-cat"<a title="Latest episode.*?">', '<')#.replace('Latest episode:','[COLOR gold]Latest episode:[/COLOR]')
                if metaset=='true':
                        if '-tvshow-' in url:
                                addDir3('[B][COLOR white]%s[/COLOR][/B] [I][B][COLOR dodgerblue]%s[/COLOR][/B][/I]' %(name,epi),url,2,thumb,items,'',name)
                        else:
                                addDir2('[B][COLOR white]%s[/COLOR][/B][I][B][COLOR dodgerblue]%s[/COLOR][/B][/I]' %(name,qual),url,3,thumb,items)
                else:
                        if '-tvshow-' in url:
                                addDir('[B][COLOR white]%s[/COLOR][/B][I][B] [COLOR dodgerblue]%s[/COLOR][/B][/I]' %(name,epi),url,2,thumb,fanart,'')
                        else:
                                addDir('[B][COLOR white]%s[/COLOR][/B][I][B][COLOR dodgerblue]%s[/COLOR][/B][/I]' %(name,qual),url,3,thumb,fanart,'')
        try:
                np = re.compile("<a id='right' href='(.*?)'> <img src='next\.png' alt='.*?' width='50'></a>").findall(link)[0]
                addDir('[I][B][COLOR dodgerblue]Go To Next Page>>>[/COLOR][/B][/I]',np,1,art+'next.png',fanart,'')
        except:pass
        setView('movies', 'movie-view')




def INDEX2(url):
        link = OPEN_URL(url)
        all_videos = regex_get_all(link, '"item"', 'clear:both')
        items = len(all_videos)
        for a in all_videos:
                name = regex_from_to(a, 'cite>', '<')
                name = addon.unescape(name)
                name = name.encode('ascii', 'ignore').decode('ascii')
                qual = regex_from_to(a, 'class="h3-quality".*?>', '<')#.replace('- Quality:','[COLOR gold]- Quality:[/COLOR]')
                url = regex_from_to(a, 'href="', '"')
                thumb = regex_from_to(a, 'src=', 'alt=').replace(' ','')
                epi = regex_from_to(a, '"h4-cat"<a title="Latest episode.*?">', '<')#.replace('Latest episode:','[COLOR gold]Latest episode:[/COLOR]')
                if metaset=='true':
                        if '-tvshow-' in url:
                                addDir3('[B][COLOR white]%s[/COLOR][/B] [I][B][COLOR dodgerblue]%s[/COLOR][/B][/I]' %(name,epi),url,2,thumb,items,'',name)
                        else:
                                addDir2('[B][COLOR white]%s[/COLOR][/B][I][B][COLOR dodgerblue]%s[/COLOR][/B][/I]' %(name,qual),url,3,thumb,items)
                else:
                        if '-tvshow-' in url:
                                addDir('[B][COLOR white]%s[/COLOR][/B][I][B] [COLOR dodgerblue]%s[/COLOR][/B][/I]' %(name,epi),url,2,thumb,fanart,'')
                        else:
                                addDir('[B][COLOR white]%s[/COLOR][/B][I][B][COLOR dodgerblue]%s[/COLOR][/B][/I]' %(name,qual),url,3,thumb,fanart,'')
        try:
                np = re.compile("<a id='right' href='(.*?)'> <img src='next\.png' alt='.*?' width='50'></a>").findall(link)[0]
                addDir('[I][B][COLOR dodgerblue]Go To Next Page>>>[/COLOR][/B][/I]',np,1,art+'next.png',fanart,'')
        except:pass
        setView('tvshows', 'show-view')




def EPIS(name,url,iconimage):
        if iconimage == None:
                iconimage = icon
        link = OPEN_URL(url)
        match=re.compile('<a itemprop="target" href="(.*?)"><button type="button"  class="episode" >(.*?)</button></a>').findall(link) 
        items = len(match)
        for url,name2 in match:
                if metaset=='true':
                        addDir3('[I][B][COLOR white]%s[/COLOR][/B][/I]' %name2,url,3,iconimage,items,'',name)
                else:
                        addDir('[I][B][COLOR white]%s[/COLOR][/B][/I]' %name2,url,3,iconimage,fanart,'')
        setView('tvshows', 'show-view')




def LINK(name,url,iconimage):
        if '-tvshow-' not in url:
                url = re.split(r'fo/', url, re.I)[1]
                url = baseurl + '/watch-free-movie/' + url
        link = OPEN_URL(url)
        try:
                url = re.findall(r'type="application/x-shockwave-flash" src="(.*?)"', str(link), re.I|re.DOTALL)[0]
                vid_id = re.split(r'=', url, re.I)[1]
                vid_id = re.split(r'&amp', vid_id, re.I)[0]
                url = 'https://docs.google.com/get_video_info?docid=' + vid_id +'&authuser='
                link = OPEN_URL(url)
                link = urllib.unquote(link)
                link = link.encode('ascii', 'ignore').decode('ascii')
                url = re.findall(r'\|(.*?)\|', str(link), re.I|re.DOTALL)[0]
        except:
                url = re.findall(r'<source type="video/mp4"  src="(.*?)"', str(link), re.I|re.DOTALL)[0]
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)




def SEARCHM():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','-')
                url = baseurl+'/tag/'+search
                INDEX(url)




def SEARCHT():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','-')
                url = baseurl+'/tagtvs/'+search
                INDEX2(url)




def GENRE(url):
        link = OPEN_URL(url)
        match=re.compile('<li> <a href="(.*?)" title="All movies.*?">(.*?)</a></li>').findall(link) 
        for url,name in match:
                if '/movie-' in url:
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,1,icon,fanart,'')




def YEAR(url):
        link = OPEN_URL(url)
        match=re.compile('<li> <a href="(.*?)" title="All movies.*?">(.*?)</a></li>').findall(link) 
        for url,name in match:
                if '/year-' in url:
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,1,icon,fanart,'')




def TVGENRE(url):
        link = OPEN_URL(url)
        match=re.compile('<li> <a href="(.*?)" title="All TVshow.*?">(.*?)</a></li>').findall(link) 
        for url,name in match:
                if '/tvshow-' in url:
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,11,icon,fanart,'')




def regex_from_to(text, from_string, to_string, excluding=True):
        if excluding:
                try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
                except: r = ''
        else:
                try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
                except: r = ''
        return r




def regex_get_all(text, start_with, end_with):
        r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
        return r




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
        name = name.replace('()','')
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
        liz.setProperty('fanart_image', fanart)
        if mode==3:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok




def PT(url):
        addon.log('Play Trailer %s' % url)
        notification( addon.get_name(), 'fetching trailer', addon.get_icon())
        xbmc.executebuiltin("PlayMedia(%s)"%url)




def notification(title, message, icon):
        addon.show_small_popup( addon.get_name(), message.title(), 5000, icon)
        return




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
        if '[I]' in simplename:
                simplename = re.split(r'[I]', simplename, re.I)[0]
                simplename = simplename[:-6]
        meta = metaget.get_meta('movie',simplename,simpleyear)
        if meta['cover_url']=='':
            try:
                meta['cover_url']=iconimage
            except:
                meta['cover_url']=icon
        name = '[B][COLOR white]' + name + '[/COLOR][/B]'
        meta['title'] = name
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
        liz.setInfo( type="Video", infoLabels= meta )
        contextMenuItems = []
        if meta['trailer']:
                contextMenuItems.append(('Play Trailer', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 7, 'url':meta['trailer']})))
        contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if not meta['backdrop_url'] == '':
                liz.setProperty('fanart_image', meta['backdrop_url'])
        else: liz.setProperty('fanart_image', art+'m4u.jpg')
        if mode==3:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=itemcount)
        else:
             ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
        return ok




def addDir3(name,url,mode,iconimage,itemcount,description,show_title):
        show_title = show_title.replace('[B][COLOR white]','').replace('[/COLOR][/B]','')
        try:
                show_title = re.split(r"\(", str(show_title), re.I)[0]
        except: pass
        try:
                show_title = re.split(r" Season ", str(show_title), re.I)[0]
        except: pass
        try:
                show_title = re.split(r"[I]", str(show_title), re.I)[0]
        except: pass
        meta = metaget.get_meta('tvshow',show_title)
        if meta['cover_url']=='':
            try:
                meta['cover_url']=iconimage
            except:
                meta['cover_url']=icon
        meta['title'] = name
        contextMenuItems = []
        contextMenuItems.append(('Show Info', 'XBMC.Action(Info)'))
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&show_title="+urllib.quote_plus(show_title)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
        liz.setInfo( type="Video", infoLabels= meta )
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if not meta['backdrop_url'] == '':
                liz.setProperty('fanart_image', meta['backdrop_url'])
        else:
                liz.setProperty('fanart_image', art+'m4u.jpg')
        if mode==3:
                liz.setProperty("IsPlayable","true")
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=itemcount)
        else:
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
        return ok
        



def addLink(name,url,mode,iconimage,fanart,description=''):
        #u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        #ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok




def OPEN_URL(url):
        headers = {}
        headers['User-Agent'] = User_Agent
        link = requests.get(url, headers=headers, allow_redirects=False).text
        link = link.encode('ascii', 'ignore').decode('ascii')
        return link





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
        elif viewType == 'default-view':
            VT = addon.get_setting(viewType)

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




params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
site=None




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




if mode==None or url==None or len(url)<1:
        CAT()

elif mode==1:
        INDEX(url)

elif mode==2:
        EPIS(name,url,iconimage)

elif mode==3:
        LINK(name,url,iconimage)

elif mode==4:
        SEARCHM()

elif mode==5:
        GENRE(url)

elif mode==6:
        YEAR(url)

elif mode==7:
        PT(url)

elif mode==8:
        TV()

elif mode==9:
        TVGENRE(url)

elif mode==10:
        SEARCHT()

elif mode==11:
        INDEX2(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

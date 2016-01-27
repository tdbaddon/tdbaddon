import urllib,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os
import requests
from addon.common.addon import Addon
from addon.common.net import Net
from metahandler import metahandlers

#PubFilm Add-on Created By Mucky Duck (1/2016)

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
addon_id='plugin.video.mdpubfilm'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
metaset = selfAddon.getSetting('enable_meta')
metaget = metahandlers.MetaData()
baseurl = 'http://tv.pubfilmhd.com/'
baseurl2 = 'http://pubfilm.com'
net = Net()



def CAT():
        addDir('[B][COLOR white]Newley Added[/COLOR][/B]',baseurl2+'/tag/new-added',1,icon,fanart,'')
        addDir('[B][COLOR white]Genre/Year[/COLOR][/B]',baseurl2,5,icon,fanart,'')
        addDir('[B][COLOR white]Search[/COLOR][/B]','url',8,icon,fanart,'')
        addDir('[B][COLOR white]Movies[/COLOR][/B]',baseurl2+'/tag/movies',1,icon,fanart,'')
        addDir('[B][COLOR white]Series[/COLOR][/B]',baseurl2+'/tag/series',2,icon,fanart,'')




def INDEX(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, '<div class="recent-item">', '<p class="post-meta">')
        items = len(all_videos)
        for a in all_videos:
                name = regex_from_to(a, '<h3 class="post-box-title"><a href=".+?" rel="bookmark">', '</a>').replace(' &#8211; Full (HD)','').replace('Seaosn','Season')
                name = addon.unescape(name)
                name = name.encode('ascii', 'ignore').decode('ascii')
                qualep = regex_from_to(a, '<div class="f_tag">', '<')
                url = regex_from_to(a, 'href="', '"')
                thumb = regex_from_to(a, 'src="', '"')
                if metaset=='true':
                        if '/' in qualep:
                                qualep = qualep.replace('/',' of ')
                                addDir2('[B][COLOR white]%s Episode%s[/COLOR][/B]' %(name,qualep),url,3,thumb,items)
                        else:
                                addDir2('[B][COLOR white]%s[/COLOR][/B]' %name,url,3,thumb,items)
                else:
                        addDir('[B][COLOR white]%s(%s)[/COLOR][/B]' %(name,qualep),url,3,thumb,fanart,'')
        try:
                nextp=re.compile('<a href="(.*?)" >\&raquo;</a>').findall(link)[0] 
                addDir('[I][COLOR red]Next Page>>>[/COLOR][/I]',nextp,1,icon,fanart,'')
        except: pass
        setView('movies', 'movie-view')




def INDEX2(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, '<div class="recent-item">', '<p class="post-meta">')
        items = len(all_videos)
        for a in all_videos:
                name = regex_from_to(a, '<h3 class="post-box-title"><a href=".+?" rel="bookmark">', '</a>').replace(' &#8211; Full (HD)','').replace('Seaosn','Season')
                name = addon.unescape(name)
                name = name.encode('ascii', 'ignore').decode('ascii')
                qualep = regex_from_to(a, '<div class="f_tag">', '<')
                url = regex_from_to(a, 'href="', '"')
                thumb = regex_from_to(a, 'src="', '"')
                if metaset=='true':
                        if '/' in qualep:
                                qualep = qualep.replace('/',' of ')
                                addDir2('[B][COLOR white]%s Episodes%s[/COLOR][/B]' %(name,qualep),url,6,thumb,items)
                        else:
                                addDir2('[B][COLOR white]%s[/COLOR][/B]' %name,url,3,thumb,items)
                else:
                        if 'season' in url:
                                addDir('[B][COLOR white]%s(%s)[/COLOR][/B]' %(name,qualep),url,6,thumb,fanart,'')
                        else:
                                addDir('[B][COLOR white]%s(%s)[/COLOR][/B]' %(name,qualep),url,3,thumb,fanart,'')
        try:
                nextp=re.compile('<a href="(.*?)" >\&raquo;</a>').findall(link)[0] 
                addDir('[I][COLOR red]Next Page>>>[/COLOR][/I]',nextp,2,icon,fanart,'')
        except: pass
        setView('movies', 'movie-view')




def EPS(name,url,iconimage):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<a href="(.*?)" target="EZWebPlayer" data-wpel-ignored="true"><input class="abutton orange big" type="button" value="(.*?)" /></a>').findall(link) 
        for url1,name in match:
                name = name.replace('Episode ','').replace('EPISODE ','')
                addDir('[B][COLOR white]Episode [/COLOR][/B][B][COLOR red]%s[/COLOR][/B]' %name,url+url1,4,icon,fanart,'')




def LINK(url):
        link = OPEN_URL(url)
        RequestURL = 'http://player.pubfilm.com/smplayer/plugins/gkphp/plugins/gkpluginsphp.php'
        r = re.compile('<ifram.*?rc="(.*?)".*?>').findall(link)[0]
        r = addon.unescape(r)
        link = re.split(r'&sub=', r, re.I)[0]
        sub = re.split(r'&sub=', r, re.I)[1]
        form_data={'link': link, 'sub': sub}
        headers = {'host': 'player.pubfilm.com', 'referer': url, 'user-agent': User_Agent}
        html = requests.get(r, data=form_data, headers=headers).text
        form_data={'link': re.search(r'link:"(.*?)"',html,re.I).group(1)}
        headers = {'host': 'player.pubfilm.com', 'content-type':'application/x-www-form-urlencoded',
                   'origin':'http://player.pubfilm.com', 'referer': r, 'user-agent': User_Agent}
        html = requests.post(RequestURL, data=form_data, headers=headers)
        url = re.findall(r'"link":"(.*?)"', str(html.text), re.I|re.DOTALL)[-1]
        url = url.replace('\/','/')
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)




def LINK2(url):
        splitLink=url.partition('.html')
        url = ""
        r = ""
        url = splitLink[0]
        url = url + '.html'
        r = splitLink[2]
        r = addon.unescape(r)
        RequestURL = 'http://player.pubfilm.com/smplayer/plugins/gkphp/plugins/gkpluginsphp.php'
        link = re.split(r'&sub=', r, re.I)[0]
        sub = re.split(r'&sub=', r, re.I)[1]
        form_data={'link': link, 'sub': sub}
        headers = {'host': 'player.pubfilm.com', 'referer': url, 'user-agent': User_Agent}
        html = requests.get(r, data=form_data, headers=headers).text
        form_data={'link': re.search(r'link:"(.*?)"',html,re.I).group(1)}
        headers = {'host': 'player.pubfilm.com', 'content-type':'application/x-www-form-urlencoded',
                   'origin':'http://player.pubfilm.com', 'referer': r, 'user-agent': User_Agent}
        html = requests.post(RequestURL, data=form_data, headers=headers)
        url = re.findall(r'"link":"(.*?)"', str(html.text), re.I|re.DOTALL)[-1]
        url = url.replace('\/','/')
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)




def SEARCH():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','%20')
                url = baseurl+'feeds/posts/summary?q='+search+'&max-results=9999&callback=showResult'
                link = OPEN_URL(url)
                link = link.encode('ascii', 'ignore').decode('ascii')
                match = re.compile(".*?link rel='alternate' type='text/html' href='(.*?)' title='(.*?)'").findall(link)[1:]
                items = len(match)
                for url,name in match:
                        name = addon.unescape(name)
                        name = name.replace(' - Full','')
                        if 'Season' in name:
                                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,6,'',fanart,'')
                        else:
                                if metaset=='true':
                                        addDir2('[B][COLOR white]%s[/COLOR][/B]' %name,url,3,'',items)
                                else:
                                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,3,'',fanart,'')
        setView('movies', 'movie-view')




def SEARCH2():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                url = baseurl2+'/?s='+search
                link = OPEN_URL(url)
                link = link.encode('ascii', 'ignore').decode('ascii')
                INDEX2(url)




def GENRE(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<a class="mega-links-head"  href="(.*?)">(.*?)</a></li>').findall(link) 
        for url,name in match:
                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,baseurl2+url,2,icon,fanart,'')




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
        if iconimage=='':
                iconimage=icon
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
        liz.setProperty('fanart_image', fanart)
        if mode==3 or mode==4:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok




def addDir2(name,url,mode,iconimage,itemcount):
        name = name.replace('[B][COLOR white]','').replace('[/COLOR][/B]','')
        if ': Season' not in name:
                year = name[-4:]
                year = year.replace(' ','')
                name = name[:-4]
                meta = metaget.get_meta('movie',name=name,year=year)
                name = '[B][COLOR white]' + name + '[/COLOR][/B]' + '[I][COLOR red]' + '(' + year + ')' + '[/COLOR][/I]'
                meta['title'] = name
        else:
                splitName=name.partition(':')
                name=""
                season=""
                if len(splitName)>0:
                        name=splitName[0]
                        season=splitName[2]
                        year = name[-4:]
                        year = year.replace(' ','')
                        print year
                        name = name[:-5]
                        print name
                print year
                meta = metaget.get_meta('tvshow',name=name,year=year)
                name = '[B][COLOR white]' + name + '[/COLOR][/B]' + ' [I][COLOR red]' + '[' + season + ']' + '[/COLOR][/I]'
                meta['title'] = name
                
        if meta['cover_url']=='':
                try:
                        meta['cover_url']=iconimage
                except:
                        meta['cover_url']=icon
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
        liz.setInfo( type="Video", infoLabels= meta )
        contextMenuItems = []
        contextMenuItems.append(('Movie/Show Information', 'XBMC.Action(Info)')),
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if not meta['backdrop_url'] == '': liz.setProperty('fanart_image', meta['backdrop_url'])
        else: liz.setProperty('fanart_image', fanart)
        if mode==3 or mode==4:
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
    name = ''
    headers['User-Agent'] = User_Agent
    link = requests.get(url, headers=headers).text
    return link




''' Why recode whats allready written and works well,
    Thanks go to Eldrado for it '''

def setView(content, viewType):
        
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
        INDEX2(url)

elif mode==3:
        LINK(url)

elif mode==4:
        LINK2(url)

elif mode==5:
        GENRE(url)

elif mode==6:
        EPS(name,url,iconimage)

elif mode==7:
        SEARCH()

elif mode==8:
        SEARCH2()

xbmcplugin.endOfDirectory(int(sys.argv[1]))

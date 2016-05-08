import sys,urllib,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os
import requests
from addon.common.addon import Addon
from metahandler import metahandlers

#Scene Peeper Add-on Created By Mucky Duck (3/2016)

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
addon_id='plugin.video.mdscenepeeper'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
auto_play = addon.get_setting('autoplay')
def_quality = addon.get_setting('default_quality')
metaset = selfAddon.getSetting('enable_meta')
metaget = metahandlers.MetaData()
baseurl = 'http://layarkaca21.tv' #'http://layarkaca21.com' #'http://www.nonton.mobi/




def CAT():
        addDir('[B][COLOR white]ALL HD[/COLOR][/B]',baseurl+'/latest/?order=desc&genre1=0&genre2=0&country=0&country=0&hdonly=1',1,icon,art+'m4u2.jpg','')
        addDir('[B][COLOR white]NEW TO OLD[/COLOR][/B]',baseurl+'/release/',1,icon,fanart,'')
        addDir('[B][COLOR white]OLD TO NEW[/COLOR][/B]',baseurl+'/release/?order=asc&genre1=0&genre2=0&country=0&tahun=0',1,icon,fanart,'')
        addDir('[B][COLOR white]720p MOVIES[/COLOR][/B]',baseurl+'/size/720/',1,icon,fanart,'')
        addDir('[B][COLOR white]1080p MOVIES[/COLOR][/B]',baseurl+'/size/1080/',1,icon,fanart,'')
        addDir('[B][COLOR white]BLU-RAY MOVIES[/COLOR][/B]',baseurl+'/quality/bluray/',1,icon,fanart,'')
        addDir('[B][COLOR white]NEWLY UPLOADED[/COLOR][/B]',baseurl+'/latest/',1,icon,fanart,'')
        addDir('[B][COLOR white]NOT SO POPULAR[/COLOR][/B]',baseurl+'/populer/?order=asc&genre1=0&genre2=0&country=0&tahun=0',1,icon,fanart,'')
        addDir('[B][COLOR white]MOST POPULAR[/COLOR][/B]',baseurl+'/populer/',1,icon,fanart,'')
        addDir('[B][COLOR white]RANDOM MOVIE[/COLOR][/B]',baseurl+'/mau-nonton-apa/',2,icon,fanart,'')
        addDir('[B][COLOR white]WORST IMDB[/COLOR][/B]',baseurl+'/rating/?order=asc&genre1=0&genre2=0&country=0&tahun=0',1,icon,fanart,'')
        addDir('[B][COLOR white]TOP IMDB[/COLOR][/B]',baseurl+'/rating/',1,icon,fanart,'')
        addDir('[B][COLOR white]COUNTRY[/COLOR][/B]',baseurl,8,icon,fanart,'')
        addDir('[B][COLOR white]SEARCH[/COLOR][/B]','url',4,icon,fanart,'')
        addDir('[B][COLOR white]TOPICS[/COLOR][/B]',baseurl,10,icon,fanart,'')
        addDir('[B][COLOR white]GENRE[/COLOR][/B]',baseurl,5,icon,fanart,'')
        addDir('[B][COLOR white]YEAR[/COLOR][/B]',baseurl,6,icon,fanart,'')
        addDir('[B][COLOR white]A/Z[/COLOR][/B]',baseurl+'/title/?order=asc&genre1=0&genre2=0&country=0&tahun=0',1,icon,fanart,'')
        addDir('[B][COLOR white]Z/A[/COLOR][/B]',baseurl+'/title/',1,icon,fanart,'')




def INDEX(url):
        link = OPEN_URL(url)
        all_videos = regex_get_all(link, '<article', '</article')
        items = len(all_videos)
        for a in all_videos:
                name = regex_from_to(a, 'Nonton</span> ', '<')
                name = addon.unescape(name)
                name = name.encode('ascii', 'ignore').decode('ascii')
                qual = regex_from_to(a, 'Kualitas Film ', '"')
                qual2 = regex_from_to(a, 'Resolusi Maksimum ', '"')
                url = regex_from_to(a, 'href="', '"')
                thumb = regex_from_to(a, 'src=', 'alt=').replace(' ','')
                if metaset == 'true':
                        if name > '':
                                addDir2('[B][COLOR white]%s[/COLOR][/B] [I][B][COLOR darkred]%s-%s[/COLOR][/B][/I]' %(name,qual,qual2),url,3,thumb,items)
                else:
                        if name > '':
                                addDir('[B][COLOR white]%s[/COLOR][/B][I][B][COLOR darkred]%s-%s[/COLOR][/B][/I]' %(name,qual,qual2),url,3,thumb,fanart,'')
        try:
                try:
                        np = re.compile('<a class="next page-numbers" href="(.*?)">').findall(link)[0]
                except:
                        np = re.compile('<link rel="next" href="(.*?)"/>').findall(link)[0]
                addDir('[I][B][COLOR darkred]Next Page>>>[/COLOR][/B][/I]',np,1,art+'next.png',fanart,'')
        except:pass
        try:
                match = re.findall(r"<a class='page-numbers' href='(.*?)'>(.*?)</a>", str(link), re.I|re.DOTALL)
                for url, name in match:
                        addDir('[I][B][COLOR darkred]Page[/COLOR][/B][/I] [I][B][COLOR white]%s[/COLOR][/B][/I]' %name,url,1,icon,fanart,'')
        except:pass
        setView('movies', 'movie-view')




def RANDOM(url):
        link = OPEN_URL(url)
        url = re.compile("script type=\"text/javascript\">var rss_playlist= '(.*?)'").findall(link)[0] 
        link = OPEN_URL(url)
        try:
                url = re.findall(r'<jwplayer:source type="mp4" file="(.*?)"', str(link), re.I|re.DOTALL)[-1]
        except:
                url = re.findall(r'<jwplayer:source type="mp4" file="(.*?)"', str(link), re.I|re.DOTALL)[0]
        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        




def LINK(name,url,iconimage):
        title = url.replace('http://layarkaca21.com/','').replace('http://layarkaca21.tv/','').replace('/','')
        mplay = 'http://layarkaca21.tv/movie/play.php?movie='
        url = url + '0/'
        link = OPEN_URL(url)
        all_links = regex_get_all(link, 'server-list', '<script>')
        res_quality = []
        res_token = []
        qt = re.findall(r'<a href=".*?" class="btn btn-.*? btn-sm">.*? (.*?)</a>', str(all_links), re.I|re.DOTALL)
        if auto_play == 'true':
                global def_quality
                def_quality = def_quality.replace('p','')
                qt[0] = qt[0].lower()
                qt[0] = qt[0].replace('class="fa-play"></i>','').replace('p','').replace('sd','').replace(' ','')
                if '1080' in def_quality:
                        try:
                                url = mplay + str(title) + '&size=' + str(qt[-1]) + '&server=0'
                        except:
                                url = mplay + str(title) + '&size=' + str(qt[0]) + '&server=0'
                elif '720' in def_quality:
                        if '720' in str(qt):
                                url = mplay + str(title) + '&size=' + def_quality + '&server=0'
                        elif '480' in str(qt):
                                url = mplay + str(title) + '&size=480&server=0'
                        else:
                                url = mplay + str(title) + '&size=' + str(qt[0]) + '&server=0'
                elif '480' in def_quality:
                        if '480' in str(qt):
                                url = mplay + str(title) + '&size=' + def_quality + '&server=0'
                        else:
                                url = mplay + str(title) + '&size=' + str(qt[0]) + '&server=0'
                elif '360' in def_quality:
                        url = mplay + str(title) + '&size=' + str(qt[0]) + '&server=0'
        else:
                for qual in qt:  ## I learned this function from studying jas0n_pc's code and works well thank you.
                        qual = qual.lower()
                        qual = qual.replace('class="fa-play"></i>','').replace('p','')
                        qual = qual.replace('sd','').replace('hd','').replace(' ','')
                        if '1080' in qual:
                                quality = '[COLOR blue][B]'+qual+'[/COLOR][/B]'
                        elif '720' in qual:
                                quality = '[COLOR green][B]'+qual+'[/COLOR][/B]'
                        elif '480' in qual:
                                quality = '[COLOR red][B]'+qual+'[/COLOR][/B]'
                        elif '360' in qual:
                                quality = '[COLOR yellow][B]'+qual+'[/COLOR][/B]'
                        res_quality.append(quality)
                        res_token.append(qual)
                if len(qt) >1:
                        dialog = xbmcgui.Dialog()
                        ret = dialog.select('Select Stream Quality',res_quality)
                        if ret == -1:
                                return
                        elif ret > -1:
                                url = mplay + str(title) + '&size=' + res_token[ret] + '&server=0'
        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
                




def SEARCH():
        keyb = xbmc.Keyboard('', 'SEARCH')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                url = baseurl+'/search/'+search+'/'
                link = OPEN_URL(url)
                all_videos = regex_get_all(link, '<article', '</div> </article>')
                items = len(all_videos)
                for a in all_videos:
                        name = regex_from_to(a, 'itemprop="url">', '<')
                        name = addon.unescape(name)
                        name = name.encode('ascii', 'ignore').decode('ascii')
                        qual = regex_from_to(a, 'Kualitas Film ', '"')
                        qual2 = regex_from_to(a, 'Resolusi Maksimum ', '"')
                        url = regex_from_to(a, 'href="', '"')
                        thumb = regex_from_to(a, 'src=', 'alt=').replace(' ','')
                        if metaset == 'true':
                                if name > '':
                                        addDir2('[B][COLOR white]%s[/COLOR][/B] [I][B][COLOR darkred]%s-%s[/COLOR][/B][/I]' %(name,qual,qual2),url,3,thumb,items)
                        else:
                                if name > '':
                                        addDir('[B][COLOR white]%s[/COLOR][/B][I][B][COLOR darkred]%s-%s[/COLOR][/B][/I]' %(name,qual,qual2),url,3,thumb,fanart,'')




def GENRE(url):
        link = OPEN_URL(url)
        match=re.compile('<li><a href="(.*?)">(.*?)</a></li>').findall(link) 
        for url,name in match:
                if '/genre/' in url:
                        nono = ['ACTION', 'ANIME', 'HORROR', 'SCI-FI', 'KOMEDI', 'ROMANCE']
                        if name not in nono:
                                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,baseurl+url,1,icon,fanart,'')




def YEAR(url):
        link = OPEN_URL(url)
        match=re.compile('<li><a href="(.*?)">(.*?)</a></li>').findall(link) 
        for url,name in match:
                if '/year/' in url:
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,baseurl+url,1,icon,fanart,'')




def COUNTRY(url):
        link = OPEN_URL(url)
        match=re.compile("<a href='(.*?)' class='tag-link-.*?' title='.*?topics' style='.*?'>(.*?)</a>").findall(link) 
        for url,name in match:
                if '/country/' in url:
                        nono = ['INDIA', 'JEPANG', 'KOREA', 'THAILAND', 'KOMEDI', 'ROMANCE']
                        if name not in nono:
                                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,1,icon,fanart,'')




def TOPIC(url):
        link = OPEN_URL(url)
        match=re.compile("<a href='(.*?)' class='tag-link-.*?' title='.*?topics' style='.*?'>(.*?)</a>").findall(link) 
        for url,name in match:
                if '/tag/' in url:
                        name = addon.unescape(name)
                        name = name.encode('ascii', 'ignore').decode('ascii')
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,1,icon,fanart,'')




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
        if mode==2 or mode==3:
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
        else: liz.setProperty('fanart_image', fanart)
        if mode==2 or mode==3:
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
    link = requests.get(url, headers=headers).text
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
        elif addon.get_setting(viewType) == 'Low List':
            VT = '724'
        elif addon.get_setting(viewType) == 'Thumbnail':
            VT = '500'
        elif addon.get_setting(viewType) == 'Default View':
            VT = addon.get_setting('default-view')
        #elif viewType == 'default-view':
            #VT = addon.get_setting(viewType)

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
        RANDOM(url)

elif mode==3:
        LINK(name,url,iconimage)

elif mode==4:
        SEARCH()

elif mode==5:
        GENRE(url)

elif mode==6:
        YEAR(url)

elif mode==7:
        PT(url)

elif mode==8:
        COUNTRY(url)

elif mode==9:
        TVGENRE(url)

elif mode==10:
        TOPIC(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

import hashlib,jsunpack,os,random,re,requests,shutil,string,sys,urllib
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs
from metahandler import metahandlers
from addon.common.addon import Addon
from md_request import open_url 

#PMovies Add-on Created By Mucky Duck (10/2016)

User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
addon_id='plugin.video.mdpmovies'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon_name = selfAddon.getAddonInfo('name')
addon = Addon(addon_id, sys.argv)
dialog = xbmcgui.Dialog()
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
metaset = selfAddon.getSetting('enable_meta')
auto_play = addon.get_setting('autoplay')
show_tv = selfAddon.getSetting('enable_shows')
show_mov = selfAddon.getSetting('enable_movies')
metaget = metahandlers.MetaData()
baseurl = 'http://pmovies.to'
s = requests.session()




sort_id = ['rating','latest','view','favorite','imdb']
sort = ['[B][I][COLOR steelblue]Most Rated[/COLOR][/I][/B]', '[B][I][COLOR steelblue]Recently Added[/COLOR][/I][/B]',
        '[B][I][COLOR steelblue]Most Viewed[/COLOR][/I][/B]', '[B][I][COLOR steelblue]Most Favorited[/COLOR][/I][/B]',
        '[B][I][COLOR steelblue]IMDB Rating[/COLOR][/I][/B]']




def CAT():
        if metaset == 'true':
                addDir('[B][I][COLOR steelblue]Meta Settings[/COLOR][/I][/B]','url',16,icon,fanart,'')
        if show_tv == 'true':
                addDir('[B][I][COLOR steelblue]TV SHOWS[/COLOR][/I][/B]','url',7,icon,art+'tvshows.jpg','')
        if show_mov == 'true':
                addDir('[B][I][COLOR steelblue]MOVIES[/COLOR][/I][/B]','url',1,icon,art+'movies.jpg','')
        setView('files', 'menu-view')



def MOVIES():
        addDir('[B][I][COLOR steelblue]Recently Added Movies[/COLOR][/I][/B]',baseurl+'/filter/?sort=latest&type=movie&quality=all&year=all',2,icon,art+'movies.jpg','')
        addDir('[B][I][COLOR steelblue]Most Favorited[/COLOR][/I][/B]',baseurl+'/filter/?sort=favorite&type=movie&quality=all&year=all',2,icon,art+'movies.jpg','')
        addDir('[B][I][COLOR steelblue]Most Viewed[/COLOR][/I][/B]',baseurl+'/filter/?sort=view&type=movie&quality=all&year=all',2,icon,art+'movies.jpg','')
        addDir('[B][I][COLOR steelblue]Most Rated[/COLOR][/I][/B]',baseurl+'/filter/?sort=rating&type=movie&quality=all&year=all',2,icon,art+'movies.jpg','')
        addDir('[B][I][COLOR steelblue]Country[/COLOR][/I][/B]',baseurl + '/filter',4,icon,art+'movies.jpg','')
        addDir('[B][I][COLOR steelblue]Cinema[/COLOR][/I][/B]',baseurl+'/cinema/',2,icon,art+'movies.jpg','')
        addDir('[B][I][COLOR steelblue]Search[/COLOR][/I][/B]','url',6,icon,art+'movies.jpg','')
        addDir('[B][I][COLOR steelblue]Genre[/COLOR][/I][/B]',baseurl + '/filter',3,icon,art+'movies.jpg','')
        addDir('[B][I][COLOR steelblue]IMDB[/COLOR][/I][/B]',baseurl+'/filter/?sort=imdb&type=movie&quality=all&year=all',2,icon,art+'movies.jpg','')
        addDir('[B][I][COLOR steelblue]Year[/COLOR][/I][/B]',baseurl + '/filter',5,icon,art+'movies.jpg','')
        setView('files', 'menu-view')




def MINDEX(url):
        if baseurl not in url:
                url = baseurl + url
        link = open_url(url).content
        all_videos = regex_get_all(link, '"ml-item"', '</div>')
        items = len(all_videos)
        for a in all_videos:
                name = regex_from_to(a, 'title="', '"')
                name = addon.unescape(name)
                name = name.encode('ascii', 'ignore').decode('ascii').replace('\\','')
                url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
                thumb = regex_from_to(a, 'data-original="', '"')
                qual = regex_from_to(a, 'quality\'>', '<')
                eps = regex_from_to(a, 'eps\'>', '</')
                eps = eps.replace('<span>',' ').replace('<i>',' ')
                if eps == '':
                        if metaset=='true':
                                addDir2('[B][COLOR white]%s[/COLOR][COLOR steelblue][I](%s)[/I][/COLOR][/B]' %(name,qual),url+'watch',14,thumb,items,name)
                        else:
                                addDir('[B][COLOR white]%s[/COLOR][COLOR steelblue][I](%s)[/I][/COLOR][/B]' %(name,qual),url+'watch',14,thumb,art+'movies.jpg','')
        try:
                pn = re.findall(r'<li class=".*?"><a href="%s(.*?)" data-ci-pagination-page=".*?" rel="(.*?)">.*?</a></li>' %baseurl, str(link), re.I|re.DOTALL)
                for url,name in pn:
                        url = url.replace('&amp;','&')
                        nono = ['prev', 'next']
                        if name in nono:
                                name = name.replace('next','>>Next Page>>>')
                                name = name.replace('prev','<<<Previous Page<<')
                                addDir('[B][I][COLOR steelblue]%s[/COLOR][/I][/B]' %name,baseurl+url,2,icon,art+'movies.jpg','')
        except:pass
        setView('movies', 'movie-view')




def MGENRE(url):
        ret = dialog.select('Select Sort Method',sort)
        sort_method = sort_id[ret]
        link = open_url(url).content
        match = re.findall(r'<li><label><input class="genre-ids" value="(.*?)" name=".*?" type="checkbox"  >(.*?)</label></li>', str(link), re.I|re.DOTALL)
        for genre_id, name in match:
                url = baseurl + '/filter/?sort=%s&type=movie&quality=all&genres%%5B%%5D=%s&year=all' %(sort_method,genre_id)
                addDir('[B][I][COLOR steelblue]%s[/COLOR][/I][/B]' %name,url,2,icon,art+'movies.jpg','')
        setView('files', 'menu-view')




def MCOUNTRY(url):
        ret = dialog.select('Select Sort Method',sort)
        sort_method = sort_id[ret]
        link = open_url(url).content
        match = re.findall(r'<li><label><input class="country-ids" value="(.*?)" name=".*?" type="checkbox"  >(.*?)</label></li>', str(link), re.I|re.DOTALL)
        for country_id, name in match:
                url = baseurl + '/filter/?sort=%s&type=movie&quality=all&countries%%5B%%5D=%s&year=all' %(sort_method,country_id)
                addDir('[B][I][COLOR steelblue]%s[/COLOR][/I][/B]' %name,url,2,icon,art+'movies.jpg','')
        setView('files', 'menu-view')




def MYEAR(url):
        ret = dialog.select('Select Sort Method',sort)
        sort_method = sort_id[ret]
        link = open_url(url).content
        match = re.findall(r'<input name="year" value=".*?" type="radio"  >(.*?)</label>', str(link), re.I|re.DOTALL)
        for year in match:
                url = baseurl + '/filter/?sort=%s&type=movie&quality=all&year=%s' %(sort_method,year)
                addDir('[B][I][COLOR steelblue]%s[/COLOR][/I][/B]' %year,url,2,icon,art+'movies.jpg','')
        addDir('[B][I][COLOR steelblue]Older[/COLOR][/I][/B]',baseurl + '/filter/?sort=%s&type=movie&quality=all&year=older' %sort_method,2,icon,art+'movies.jpg','')
        setView('files', 'menu-view')




def MSEARCH():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                url = baseurl + '/search/?q=' + search
                MINDEX(url)




def TV():
        addDir('[B][I][COLOR steelblue]Recently Added Shows[/COLOR][/I][/B]',baseurl+'/filter/?sort=latest&type=series&quality=all&year=all',8,icon,art+'tvshows.jpg','')
        addDir('[B][I][COLOR steelblue]Most Favorited[/COLOR][/I][/B]',baseurl+'/filter/?sort=favorite&type=series&quality=all&year=all',8,icon,art+'tvshows.jpg','')
        addDir('[B][I][COLOR steelblue]Most Viewed[/COLOR][/I][/B]',baseurl+'/filter/?sort=view&type=series&quality=all&year=all',8,icon,art+'tvshows.jpg','')
        addDir('[B][I][COLOR steelblue]Most Rated[/COLOR][/I][/B]',baseurl+'/filter/?sort=rating&type=series&quality=all&year=all',8,icon,art+'tvshows.jpg','')
        addDir('[B][I][COLOR steelblue]Country[/COLOR][/I][/B]',baseurl + '/filter',11,icon,art+'tvshows.jpg','')
        addDir('[B][I][COLOR steelblue]Search[/COLOR][/I][/B]','url',13,icon,art+'tvshows.jpg','')
        addDir('[B][I][COLOR steelblue]Genre[/COLOR][/I][/B]',baseurl + '/filter',10,icon,art+'tvshows.jpg','')
        addDir('[B][I][COLOR steelblue]IMDB[/COLOR][/I][/B]',baseurl+'/filter/?sort=imdb&type=series&quality=all&year=all',8,icon,art+'tvshows.jpg','')
        addDir('[B][I][COLOR steelblue]Year[/COLOR][/I][/B]',baseurl + '/filter',12,icon,art+'tvshows.jpg','')
        setView('files', 'menu-view')




def TVINDEX(url):
        if baseurl not in url:
                url = baseurl + url
        link = open_url(url).content
        all_videos = regex_get_all(link, '"ml-item"', '</div>')
        items = len(all_videos)
        for a in all_videos:
                name = regex_from_to(a, 'title="', '"')
                name = addon.unescape(name)
                name = name.encode('ascii', 'ignore').decode('ascii').replace('\\','')
                url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
                thumb = regex_from_to(a, 'data-original="', '"')
                qual = regex_from_to(a, 'quality\'>', '<')
                eps = regex_from_to(a, 'eps\'>', '</')
                eps = eps.replace('<span>',' ').replace('<i>',' ')
                if eps > '':
                        if metaset=='true':
                                addDir3('[B][COLOR white]%s[/COLOR][COLOR steelblue][I](%s)[/I][/COLOR][/B]' %(name,eps),url+'watch',9,thumb,items,'',name)
                        else:
                                addDir('[B][COLOR white]%s[/COLOR][COLOR steelblue][I](%s)[/I][/COLOR][/B]' %(name,eps),url+'watch',9,thumb,art+'tvshows.jpg','')
        try:
                pn = re.findall(r'<li class=".*?"><a href="%s(.*?)" data-ci-pagination-page=".*?" rel="(.*?)">.*?</a></li>' %baseurl, str(link), re.I|re.DOTALL)
                for url,name in pn:
                        url = url.replace('&amp;','&')
                        nono = ['prev', 'next']
                        if name in nono:
                                name = name.replace('next','>>Next Page>>>')
                                name = name.replace('prev','<<<Previous Page<<')
                                addDir('[B][I][COLOR steelblue]%s[/COLOR][/I][/B]' %name,baseurl+url,8,icon,art+'tvshows.jpg','')
        except:pass
        setView('tvshows', 'show-view')




def EPIS(url,iconimage,show_title):
        if baseurl not in url:
                url = baseurl + url
        if iconimage == '' or iconimage == None:
                iconimage = icon
        headers = {'User-Agent':User_Agent}
        link = open_url(url).content
        all_links = regex_get_all(link, 'id="list-eps"', '"clearfix"')
        all_videos = regex_get_all(str(all_links), '<a', 'a>')
        items = len(all_videos)
        for a in all_videos:
                name = regex_from_to(a, 'btn-eps first-ep .*?">', '</')
                name = name.replace('Episode','[COLOR steelblue]Episode[/COLOR]')
                name = addon.unescape(name)
                name = name.encode('ascii', 'ignore').decode('ascii').replace('\\','')
                url = regex_from_to(a, 'href="', '"')
                addon.log(url)
                if '/server-' in url:
                        if metaset=='true':
                                addDir4('[B][I][COLOR white]%s[/COLOR][/I][/B]' %name,url,14,iconimage,items,'',show_title)
                        else:
                                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,14,iconimage,art+'tvshows.jpg','')
        setView('episodes', 'epi-view')




def TVGENRE(url):
        ret = dialog.select('Select Sort Method',sort)
        sort_method = sort_id[ret]
        link = open_url(url).content
        match = re.findall(r'<li><label><input class="genre-ids" value="(.*?)" name=".*?" type="checkbox"  >(.*?)</label></li>', str(link), re.I|re.DOTALL)
        for genre_id, name in match:
                url = baseurl + '/filter/?sort=%s&type=series&quality=all&genres%%5B%%5D=%s&year=all' %(sort_method,genre_id)
                addDir('[B][I][COLOR steelblue]%s[/COLOR][/I][/B]' %name,url,8,icon,art+'tvshows.jpg','')
        setView('files', 'menu-view')




def TVCOUNTRY(url):
        ret = dialog.select('Select Sort Method',sort)
        sort_method = sort_id[ret]
        link = open_url(url).content
        match = re.findall(r'<li><label><input class="country-ids" value="(.*?)" name=".*?" type="checkbox"  >(.*?)</label></li>', str(link), re.I|re.DOTALL)
        for country_id, name in match:
                url = baseurl + '/filter/?sort=%s&type=series&quality=all&countries%%5B%%5D=%s&year=all' %(sort_method,country_id)
                addDir('[B][I][COLOR steelblue]%s[/COLOR][/I][/B]' %name,url,8,icon,art+'tvshows.jpg','')
        setView('files', 'menu-view')




def TVYEAR():
        ret = dialog.select('Select Sort Method',sort)
        sort_method = sort_id[ret]
        link = open_url(url).content
        match = re.findall(r'<input name="year" value=".*?" type="radio"  >(.*?)</label>', str(link), re.I|re.DOTALL)
        for year in match:
                url = baseurl + '/filter/?sort=%s&type=series&quality=all&year=%s' %(sort_method,year)
                addon.log(match)
                addDir('[B][I][COLOR steelblue]%s[/COLOR][/I][/B]' %year,url,2,icon,art+'tvshows.jpg','')
        addDir('[B][I][COLOR steelblue]Older[/COLOR][/I][/B]',baseurl + '/filter/?sort=%s&type=movie&quality=all&year=older' %sort_method,8,icon,art+'tvshows.jpg','')
        setView('files', 'menu-view')




def TVSEARCH():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                url = baseurl+'/search/?q='+search
                TVINDEX(url)



key = '!@#$%^&*('
'''def RESOLVE(name,url,iconimage):
        headers = {'User-Agent':User_Agent}
        link = s.get(url, headers=headers).content
        request_url = re.findall(r'<script src="(.*?)"', str(link), re.I|re.DOTALL)[1]
        link2 = s.get(request_url, headers=headers).content
        
        if jsunpack.detect(link2):
                js_data = jsunpack.unpack(link2)
                match = re.search('"sourcesPlaylist"\s*:\s*"([^"]+)', js_data)

        request_url2 = match.group(1).replace('\\\/','/')
        final = s.get(request_url2, headers=headers).json()
        res_quality = []
        stream_url = []
        quality = ''
        if auto_play == 'true':
                url = final['playlist'][0]['sources'][0]['file']
        else:
                match = final['playlist'][0]['sources']
                for a in match:
                        quality = '[B][I][COLOR steelblue]%s[/COLOR][/I][/B]' %a['label']
                        res_quality.append(quality)
                        stream_url.append(a['file'])
                if len(match) >1:
                        dialog = xbmcgui.Dialog()
                        ret = dialog.select('Select Stream Quality',res_quality)
                        if ret == -1:
                                return
                        elif ret > -1:
                                url = stream_url[ret]
                else:
                        url = final['playlist'][0]['sources'][0]['file']
        if baseurl not in url:
                if 'google' not in url:
                        url = baseurl + url
        url = url.replace('&amp;','&')
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={"Title": name})
        liz.setProperty("IsPlayable","true")
        liz.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)'''




def RESOLVE(name,url,iconimage):

        link = open_url(url).content

        server_select = re.findall(r'<i class="fa fa-server mr5"></i><strong>(.*?)</strong>.*?<a href="(.*?)" .*?>', str(link), re.I|re.DOTALL)
        server_choice = []
        server_url = []
        servers = ''

        for sname, surl in server_select:
                if 'SERVER' in sname:
                        servers = '[B][I][COLOR steelblue]%s[/COLOR][/I][/B]' %sname
                        server_choice.append(servers)
                        server_url.append(surl)

        if auto_play == 'true':
                request_url = server_url[0]

        else:
                if len(server_select) >1:
                        ret = dialog.select('Please Choose A Server',server_choice)
                        if ret == -1:
                                return
                        elif ret > -1:
                                request_url = server_url[ret]

        link2 = open_url(request_url).content
        key_gen = random_generator()
        episode_id = re.findall(r'episode: "(.*?)"', str(link2), re.I|re.DOTALL)[2]
        hash_id = re.findall(r'hash: "(.*?)"', str(link2), re.I|re.DOTALL)[0]
        base_id = baseurl.replace('http://','').replace('https://','')
        #key2 = hash_id[46:58]

        cookie = '%s=%s' %(hashlib.md5(key[::1] + episode_id + key_gen).hexdigest(),
                           hashlib.md5(key_gen + request_url + episode_id).hexdigest())

        request_url2 = 'http://play.%s/grabber-api/episode/%s?token=%s' %(base_id,episode_id,key_gen)
        headers = {'Accept-Encoding':'gzip, deflate, sdch', 'Cookie': cookie, 'Referer': request_url,
                   'Origin':baseurl, 'User-Agent':User_Agent}

        final = open_url(request_url2, headers=headers).json()
        
        res_quality = []
        stream_url = []
        quality = ''

        if auto_play == 'true':
                url = final['playlist'][0]['sources'][0]['file']

        else:
                match = final['playlist'][0]['sources']
                for a in match:
                        quality = '[B][I][COLOR steelblue]%s[/COLOR][/I][/B]' %a['label']
                        res_quality.append(quality)
                        stream_url.append(a['file'])
                if len(match) >1:
                        ret = dialog.select('Select Stream Quality',res_quality)
                        if ret == -1:
                                return
                        elif ret > -1:
                                url = stream_url[ret]
                else:
                        url = final['playlist'][0]['sources'][0]['file']

        if baseurl not in url:
                if 'google' not in url:
                        url = baseurl + url

        url = url.replace('&amp;','&')
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={"Title": name})
        liz.setProperty("IsPlayable","true")
        liz.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)




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




def PT(url):
        addon.log('Play Trailer %s' % url)
        notification( addon.get_name(), 'fetching trailer', addon.get_icon())
        xbmc.executebuiltin("PlayMedia(%s)"%url)




def notification(title, message, icon):
        addon.show_small_popup( addon.get_name(), message.title(), 5000, icon)




def random_generator(size=8, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))




#key = '(*&^%$#@!'




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
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={"Title":name,"Plot":description})
        liz.setProperty('fanart_image', fanart)
        if mode==14 or mode==15:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok




def addDir2(name,url,mode,iconimage,itemcount,movie_title):
        meta = metaget.get_meta('movie',movie_title,'')
        if meta['cover_url']=='':
            try:
                meta['cover_url']=iconimage
            except:
                meta['cover_url']=icon
        meta['title'] = name
        meta['plot'] = '[B][COLOR white]%s[/COLOR][/B]' %meta['plot']
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&movie_title="+urllib.quote_plus(movie_title)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
        liz.setInfo(type="Video", infoLabels=meta)
        contextMenuItems = []
        contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
        if meta['trailer']:
                contextMenuItems.append(('Play Trailer', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 15, 'url':meta['trailer']})))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if not meta['backdrop_url'] == '':
                liz.setProperty('fanart_image', meta['backdrop_url'])
        else: liz.setProperty('fanart_image', art+'movies.jpg')
        if mode==14 or mode==15:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=itemcount)
        else:
             ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
        return ok




def addDir3(name,url,mode,iconimage,itemcount,description,show_title):
        title = show_title.split(' - Season')[0]
        meta = metaget.get_meta('tvshow',title)
        meta['plot'] = '[B][COLOR white]%s[/COLOR][/B]' %meta['plot']
        if meta['cover_url']=='':
            try:
                meta['cover_url']=iconimage
            except:
                meta['cover_url']=icon
        meta['title'] = name
        contextMenuItems = []
        contextMenuItems.append(('Show Info', 'XBMC.Action(Info)'))
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)+"&show_title="+urllib.quote_plus(show_title)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
        liz.setInfo(type="Video", infoLabels=meta)
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if not meta['backdrop_url'] == '':
                liz.setProperty('fanart_image', meta['backdrop_url'])
        else:
                liz.setProperty('fanart_image', art+'tvshows.jpg')
        if mode==14 or mode==15:
                liz.setProperty("IsPlayable","true")
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=itemcount)
        else:
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
        return ok




def addDir4(name,url,mode,iconimage,itemcount,description,show_title):
        season = show_title.replace(' ','')
        try:
                season = season.lower().split('-season')[1].strip()
                if '0' in season[0]:
                        season = season[1]
        except:
                pass
        try:
                episode = name.lower().split('episode[/color]')[1].strip()
                episode = episode.split(':')[0].strip()
                if '0' in episode[0]:
                        episode = episode[1]
        except:
                pass
        show_title = show_title.split('- Season')[0].rstrip()
        try:
                meta = metaget.get_episode_meta(show_title,'',season,episode)
        except:
                meta = metaget.get_meta('tvshow',show_title)
        meta['plot'] = '[B][COLOR white]%s[/COLOR][/B]' %meta['plot']
        if meta['cover_url']=='':
            try:
                meta['cover_url']=iconimage
            except:
                meta['cover_url']=icon
        meta['title'] = name
        contextMenuItems = []
        contextMenuItems.append(('Episode Info', 'XBMC.Action(Info)'))
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)+"&show_title="+urllib.quote_plus(show_title)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
        liz.setInfo(type="Video", infoLabels=meta)
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if not meta['backdrop_url'] == '':
                liz.setProperty('fanart_image', meta['backdrop_url'])
        else:
                liz.setProperty('fanart_image', art+'tvshows.jpg')
        if mode==14 or mode==15:
                liz.setProperty("IsPlayable","true")
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=itemcount)
        else:
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
        return ok




def addLink(name,url,mode,iconimage,fanart,description=''):
        #u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        #ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={"Title": name, 'plot': description})
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok




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
        elif addon.get_setting(viewType) == 'Thumbnail':
            VT = '500'
        elif addon.get_setting(viewType) == 'Default Menu View':
            VT = addon.get_setting('default-view1')
        elif addon.get_setting(viewType) == 'Default TV Shows View':
            VT = addon.get_setting('default-view2')
        elif addon.get_setting(viewType) == 'Default Episodes View':
            VT = addon.get_setting('default-view3')
        elif addon.get_setting(viewType) == 'Default Movies View':
            VT = addon.get_setting('default-view4')

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




try:
        path = xbmc.translatePath( "special://temp" ) 
        filenames = next(os.walk(path))[2]
        for i in filenames:
            if ".fi" in i:
                os.remove(os.path.join(path, i))
except: pass
           


params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
show_title=None
movie_title=None

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

try:
        show_title=urllib.unquote_plus(params["show_title"])
except:
        pass

try:
        show_title=urllib.unquote_plus(params["movie_title"])
except:
        pass
   
        
if mode==None or url==None or len(url)<1:
        CAT()

elif mode==1:
        MOVIES()

elif mode==2:
        MINDEX(url)

elif mode==3:
        MGENRE(url)

elif mode==4:
        MCOUNTRY(url)

elif mode==5:
        MYEAR(url)

elif mode==6:
        MSEARCH()

elif mode==7:
        TV()

elif mode==8:
        TVINDEX(url)

elif mode==9:
        EPIS(url,iconimage,show_title)

elif mode==10:
        TVGENRE(url)

elif mode==11:
        TVCOUNTRY(url)

elif mode==12:
        TVYEAR(url)

elif mode==13:
        TVSEARCH()

elif mode==14:
        RESOLVE(name,url,iconimage)

elif mode==15:
        PT(url)

elif mode==16:
    import metahandler
    metahandler.display_settings()

xbmcplugin.endOfDirectory(int(sys.argv[1]))




























































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































if xbmcvfs.exists(xbmc.translatePath('special://home/userdata/sources.xml')):
        with open(xbmc.translatePath('special://home/userdata/sources.xml'), 'r+') as f:
                my_file = f.read()
                if re.search(r'http://muckys.mediaportal4kodi.ml', my_file):
                        addon.log('===Muckys===Source===Found===in===sources.xml===Not Deleting.===')
                else:
                        line1 = "you have Installed The MDrepo From An"
                        line2 = "Unofficial Source And Will Now Delete Please"
                        line3 = "Install From [COLOR red]http://muckys.mediaportal4kodi.ml[/COLOR]"
                        line4 = "Removed Repo And Addon"
                        line5 = "successfully"
                        xbmcgui.Dialog().ok(addon_name, line1, line2, line3)
                        delete_addon = xbmc.translatePath('special://home/addons/'+addon_id)
                        delete_repo = xbmc.translatePath('special://home/addons/repository.mdrepo')
                        shutil.rmtree(delete_addon, ignore_errors=True)
                        shutil.rmtree(delete_repo, ignore_errors=True)
                        dialog = xbmcgui.Dialog()
                        addon.log('===DELETING===ADDON===+===REPO===')
                        xbmcgui.Dialog().ok(addon_name, line4, line5)



































































































































































































































































































































































































































































































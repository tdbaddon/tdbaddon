import base64,hashlib,os,random,re,requests,shutil,string,sys,urllib
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs
from metahandler import metahandlers
from addon.common.addon import Addon

#Yes Movies Add-on Created By Mucky Duck (10/2016)

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
addon_id='plugin.video.mdyesmovies'
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
baseurl = 'https://yesmovies.to'
s = requests.session()




sort_id = ['rating','latest','view','favorite','imdb_mark']
sort = ['[B][I][COLOR indianred]Most Rated[/COLOR][/I][/B]', '[B][I][COLOR indianred]Recently Added[/COLOR][/I][/B]',
        '[B][I][COLOR indianred]Most Viewed[/COLOR][/I][/B]', '[B][I][COLOR indianred]Most Favorited[/COLOR][/I][/B]',
        '[B][I][COLOR indianred]IMDB Rating[/COLOR][/I][/B]']




def CAT():
        if metaset == 'true':
                addDir('[B][I][COLOR indianred]Meta Settings[/COLOR][/I][/B]','url',17,icon,fanart,'')
        if show_tv == 'true':
                addDir('[B][I][COLOR indianred]TV SHOWS[/COLOR][/I][/B]','url',7,icon,fanart,'')
        if show_mov == 'true':
                addDir('[B][I][COLOR indianred]MOVIES[/COLOR][/I][/B]','url',1,icon,fanart,'')
        setView('files', 'menu-view')



def MOVIES():
        addDir('[B][I][COLOR indianred]Recently Added Movies[/COLOR][/I][/B]',baseurl+'/movie/filter/movie/latest/all/all/all/all/all.html',2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Most Favorited[/COLOR][/I][/B]',baseurl+'/movie/filter/movie/favorite/all/all/all/all/all',2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Most Viewed[/COLOR][/I][/B]',baseurl+'/movie/filter/movie/view/all/all/all/all/all',2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Most Rated[/COLOR][/I][/B]',baseurl+'/movie/filter/movie/rating/all/all/all/all/all',2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Country[/COLOR][/I][/B]','movie',4,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Search[/COLOR][/I][/B]','url',6,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Genre[/COLOR][/I][/B]','movie',3,icon,fanart,'')
        addDir('[B][I][COLOR indianred]IMDB[/COLOR][/I][/B]',baseurl+'/movie/filter/movie/imdb_mark/all/all/all/all/all',2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Year[/COLOR][/I][/B]','url',5,icon,fanart,'')
        setView('files', 'menu-view')




def MINDEX(url):
        if baseurl not in url:
                url = baseurl + url
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, '"ml-item"', '</div>')
        items = len(all_videos)
        for a in all_videos:
                name = regex_from_to(a, 'title="', '"')
                name = addon.unescape(name)
                name = name.encode('ascii', 'ignore').decode('ascii').replace('\\','')
                url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
                thumb = regex_from_to(a, 'data-original="', '"')
                qual = regex_from_to(a, 'quality">', '<')
                eps = regex_from_to(a, 'mli-eps">', '</')
                eps = eps.replace('<span>',' ')
                if eps == '':
                        if metaset=='true':
                                addDir2('[B][COLOR white]%s[/COLOR][COLOR indianred][I](%s)[/I][/COLOR][/B]' %(name,qual),url,14,thumb,items,name)
                        else:
                                addDir('[B][COLOR white]%s[/COLOR][COLOR indianred][I](%s)[/I][/COLOR][/B]' %(name,qual),url,14,thumb,fanart,'')
        try:
                pn = re.findall(r'<li class=".*?"><a href="%s(.*?)" data-ci-pagination-page=".*?" rel="(.*?)">.*?</a></li>' %baseurl, str(link), re.I|re.DOTALL)
                for url,name in pn:
                        url = url.replace('&amp;','&')
                        nono = ['prev', 'next']
                        if name in nono:
                                name = name.replace('next','>>Next Page>>>')
                                name = name.replace('prev','<<<Previous Page<<')
                                addDir('[B][I][COLOR indianred]%s[/COLOR][/I][/B]' %name,baseurl+url,2,icon,fanart,'')
        except:pass
        setView('movies', 'movie-view')




def MGENRE(url):
        ret = dialog.select('Select Sort Method',sort)
        sort_method = sort_id[ret]
        addDir('[B][I][COLOR indianred]Action[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/1/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Adventure[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/2/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Animation[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/120/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Biography[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/125/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Comedy[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/7/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Costume[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/12/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Crime[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/25/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Documentary[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/126/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Drama[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/119/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Family[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/114/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Fantasy[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/124/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]History[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/112/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Horror[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/122/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Kungfu[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/6/all/all/all/all' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Musical[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/27/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Mystery[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/121/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Mythological[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/11/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Mythological[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/9/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Romance[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/4/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Sci-Fi[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/10/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Sitcom[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/118/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Sport[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/123/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Thriller[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/3/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]TV Show[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/23/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]War[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/22/all/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        setView('files', 'menu-view')




def MCOUNTRY(url):
        ret = dialog.select('Select Sort Method',sort)
        sort_method = sort_id[ret]
        addDir('[B][I][COLOR indianred]United Kingdom[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/all/72/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]United States[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/all/7/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]International[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/all/1/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Thailand[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/all/8/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Hongkong[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/all/5/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Europe[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/all/12/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]France[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/all/73/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Taiwan[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/all/4/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Indian[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/all/9/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Japan[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/all/6/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Korea[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/all/3/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]China[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/all/2/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Asia[/COLOR][/I][/B]',baseurl+'/movie/filter/%s/%s/all/10/all/all/all.html' %(url,sort_method),2,icon,fanart,'')
        setView('files', 'menu-view')




def MYEAR():
        ret = dialog.select('Select Sort Method',sort)
        sort_method = sort_id[ret]
        ret_no = dialog.numeric(0, 'Enter Year', '2016')
        MINDEX(baseurl+'/movie/filter/movie/%s/all/all/%s/all/all.html' %(sort_method,ret_no))




def MSEARCH():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                url = baseurl+'/search/'+search
                MINDEX(url)




def TV():
        addDir('[B][I][COLOR indianred]Recently Added Shows[/COLOR][/I][/B]',baseurl+'/movie/filter/series/latest/all/all/all/all/all.html',8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Most Favorited[/COLOR][/I][/B]',baseurl+'/movie/filter/series/favorite/all/all/all/all/all',8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Most Viewed[/COLOR][/I][/B]',baseurl+'/movie/filter/series/view/all/all/all/all/all',8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Most Rated[/COLOR][/I][/B]',baseurl+'/movie/filter/series/rating/all/all/all/all/all',8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Country[/COLOR][/I][/B]','series',11,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Search[/COLOR][/I][/B]','url',13,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Genre[/COLOR][/I][/B]','series',10,icon,fanart,'')
        addDir('[B][I][COLOR indianred]IMDB[/COLOR][/I][/B]',baseurl+'/movie/filter/series/imdb_mark/all/all/all/all/all',8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Year[/COLOR][/I][/B]','url',12,icon,fanart,'')
        setView('files', 'menu-view')




def TVINDEX(url):
        if baseurl not in url:
                url = baseurl + url
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, '"ml-item"', '</div>')
        items = len(all_videos)
        for a in all_videos:
                name = regex_from_to(a, 'title="', '"')
                name = addon.unescape(name)
                name = name.encode('ascii', 'ignore').decode('ascii').replace('\\','')
                url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
                thumb = regex_from_to(a, 'data-original="', '"')
                qual = regex_from_to(a, 'quality">', '<')
                eps = regex_from_to(a, 'mli-eps">', '</')
                eps = eps.replace('<i>',' ')
                if eps > '':
                        if metaset=='true':
                                addDir3('[B][COLOR white]%s[/COLOR][COLOR indianred][I](%s)[/I][/COLOR][/B]' %(name,eps),url,9,thumb,items,'',name)
                        else:
                                addDir('[B][COLOR white]%s[/COLOR][COLOR indianred][I](%s)[/I][/COLOR][/B]' %(name,eps),url,9,thumb,fanart,'')
        try:
                pn = re.findall(r'<li class=".*?"><a href="%s(.*?)" data-ci-pagination-page=".*?" rel="(.*?)">.*?</a></li>' %baseurl, str(link), re.I|re.DOTALL)
                for url,name in pn:
                        url = url.replace('&amp;','&')
                        nono = ['prev', 'next']
                        if name in nono:
                                name = name.replace('next','>>Next Page>>>')
                                name = name.replace('prev','<<<Previous Page<<')
                                addDir('[B][I][COLOR indianred]%s[/COLOR][/I][/B]' %name,baseurl+url,8,icon,fanart,'')
        except:pass
        setView('tvshows', 'show-view')




def EPIS(url,iconimage,show_title):
        if baseurl not in url:
                url = baseurl + url
        if iconimage == '' or iconimage == None:
                iconimage = icon
        headers = {'User-Agent':User_Agent}
        link = s.get(url, headers=headers,verify=False).content
        referer = re.findall(r'<a class="mod-btn mod-btn-watch" href="(.*?)" title="Watch movie">', str(link), re.I|re.DOTALL)[0]
        link2 = s.get(referer, headers=headers,verify=False).content
        i_d = re.findall(r'id: "(.*?)"', str(link2), re.I|re.DOTALL)[0]
        server = re.findall(r'server: "(.*?)"', str(link2), re.I|re.DOTALL)[0]
        type = re.findall(r'type: "(.*?)"', str(link2), re.I|re.DOTALL)[0]
        episode_id = re.findall(r'episode_id: "(.*?)"', str(link2), re.I|re.DOTALL)[0]
        request_url = baseurl + '/ajax/v3_movie_get_episodes/' + i_d + '/' + server + '/' + episode_id + '/' + type + '.html'
        headers.update({'Accept-Encoding':'gzip, deflate, sdch', 'Referer': referer, 'x-requested-with':'XMLHttpRequest'})
        link3 = s.get(request_url, headers=headers,verify=False).text
        all_links = regex_get_all(link3, '"episodes-server-%s"' %server, '</ul>')
        all_videos = regex_get_all(str(all_links), '<li', '</li>')
        items = len(all_videos)
        for a in all_videos:
                name = regex_from_to(a, 'title="', '"')
                name = name.replace('Episode','[COLOR indianred]Episode[/COLOR]')
                name = addon.unescape(name)
                name = name.encode('ascii', 'ignore').decode('ascii').replace('\\','')
                url = regex_from_to(a, '"episode-', '"')
                url = referer + '|' + url
                if metaset=='true':
                        addDir4('[B][I][COLOR white]%s[/COLOR][/I][/B]' %name,url,15,iconimage,items,'',show_title)
                else:
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,15,iconimage,fanart,'')
        setView('episodes', 'epi-view')




def TVGENRE(url):
        ret = dialog.select('Select Sort Method',sort)
        sort_method = sort_id[ret]
        addDir('[B][I][COLOR indianred]Action[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/1/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Adventure[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/2/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Animation[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/120/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Biography[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/125/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Comedy[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/7/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Costume[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/12/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Crime[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/25/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Documentary[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/126/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Drama[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/119/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Family[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/114/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Fantasy[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/124/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]History[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/112/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Horror[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/122/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Kungfu[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/6/all/all/all/all' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Musical[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/27/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Mystery[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/121/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Mythological[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/11/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Mythological[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/9/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Romance[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/4/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Sci-Fi[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/10/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Sitcom[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/118/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Sport[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/123/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Thriller[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/3/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]TV Show[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/23/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]War[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/22/all/all/all/all.html' %sort_method,8,icon,fanart,'')
        setView('files', 'menu-view')




def TVCOUNTRY(url):
        ret = dialog.select('Select Sort Method',sort)
        sort_method = sort_id[ret]
        addDir('[B][I][COLOR indianred]United Kingdom[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/all/72/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]United States[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/all/7/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]International[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/all/1/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Thailand[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/all/8/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Hongkong[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/all/5/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Europe[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/all/12/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]France[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/all/73/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Taiwan[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/all/4/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Indian[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/all/9/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Japan[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/all/6/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Korea[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/all/3/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]China[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/all/2/all/all/all.html' %sort_method,8,icon,fanart,'')
        addDir('[B][I][COLOR indianred]Asia[/COLOR][/I][/B]',baseurl+'/movie/filter/series/%s/all/10/all/all/all.html' %sort_method,8,icon,fanart,'')
        setView('files', 'menu-view')




def TVYEAR():
        ret = dialog.select('Select Sort Method',sort)
        sort_method = sort_id[ret]
        ret_no = dialog.numeric(0, 'Enter Year', '2016')
        TVINDEX(baseurl+'/movie/filter/series/%s/all/all/%s/all/all.html' %(sort_method,ret_no))




def TVSEARCH():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                url = baseurl+'/search/'+search
                TVINDEX(url)




key = 'xwh38if39ucx'
key2 = '8qhfm9oyq1ux'
key3 = 'ctiw4zlrn09tau7kqvc153uo'


def __jav( a):
        b = str(a)
        code = ord(b[0])
        if 0xD800 <= code and code <= 0xDBFF:
            c = code
            if len(b) == 1:
                return code
            d = ord(b[1])
            return ((c - 0xD800) * 0x400) + (d - 0xDC00) + 0x10000

        if 0xDC00 <= code and code <= 0xDFFF:
            return code
        return code

def __uncensored( a, b):
        c = ''
        i = 0
        for i, d in enumerate(a):
            e = b[i % len(b) - 1]
            d = int(__jav(d) + __jav(e))
            c += chr(d)

        return base64.b64encode(c)


def random_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))




def MRESOLVE(name,url,iconimage):
        headers = {'User-Agent':User_Agent}
        link = s.get(url, headers=headers,verify=False).content
        referer = re.findall(r'<a class="mod-btn mod-btn-watch" href="(.*?)" title="Watch movie">', str(link), re.I|re.DOTALL)[0]
        link2 = s.get(referer, headers=headers,verify=False).content
        i_d = re.findall(r'id: "(.*?)"', str(link2), re.I|re.DOTALL)[0]
        server = re.findall(r'server: "(.*?)"', str(link2), re.I|re.DOTALL)[0]
        type = re.findall(r'type: "(.*?)"', str(link2), re.I|re.DOTALL)[0]
        episode_id = re.findall(r'episode_id: "(.*?)"', str(link2), re.I|re.DOTALL)[0]
        key_gen = random_generator()

        getc = re.findall(r'<img title=.*?src="(.*?)"', str(link2), re.I|re.DOTALL)[0]
        headers = {'Accept': 'image/webp,image/*,*/*;q=0.8', 'Accept-Encoding':'gzip, deflate, sdch, br',
                   'Accept-Language': 'en-US,en;q=0.8', 'Referer': referer, 'User-Agent':User_Agent}
        cookie = s.get(getc,headers=headers,verify=False).cookies.get_dict()
        for i in cookie:
                cookie =  i + '=' + cookie[i]
        #coookie = hashlib.md5(key + episode_id + key2).hexdigest() + '=%s' %key_gen
        coookie = key + episode_id + key2 + '=%s' %key_gen
        cookie = '%s; %s' %(cookie,coookie)
        a= episode_id + key3
        b= key_gen
        hash_id = __uncensored(a, b)
        hash_id = urllib.quote(hash_id).encode('utf8')

        request_url2 =  baseurl + '/ajax/v2_get_sources/' + episode_id + '?hash=' + hash_id
        headers = {'Accept-Encoding':'gzip, deflate, sdch', 'Cookie': cookie, 'Referer': referer,
                   'User-Agent':User_Agent,'X-Requested-With':'XMLHttpRequest'}
        #request_url2 = baseurl + '/ajax/v2_get_sources/' + episode_id + '/' + hash_id + '.html'
        try:
                final = s.get(request_url2, headers=headers,verify=False).json()
                res_quality = []
                stream_url = []
                quality = ''
                if auto_play == 'true':
                        url = final['playlist'][0]['sources'][0]['file']
                else:
                        match = final['playlist'][0]['sources']
                        for a in match:
                                quality = '[B][I][COLOR indianred]%s[/COLOR][/I][/B]' %a['label']
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
        except:
                final = s.get(request_url2, headers=headers,verify=False).text
                res_quality = []
                stream_url = []
                quality = ''
                if auto_play == 'true':
                        url = re.compile('"file":"(.*?)"').findall(final)[0]
                else:
                        match = re.compile('"file":"(.*?)","label":"(.*?)"').findall(final)
                        for stream_url, label in match:
                                if '.srt' not in stream_url:
                                        quality = '[B][I][COLOR indianred]%s[/COLOR][/I][/B]' %label
                                        res_quality.append(quality)
                                        stream_url.append(stream_url)
                        if len(match) >1:
                                dialog = xbmcgui.Dialog()
                                ret = dialog.select('Select Stream Quality',res_quality)
                                if ret == -1:
                                        return
                                elif ret > -1:
                                        url = stream_url[ret]
                        else:
                                url = re.compile('"file":"(.*?)"').findall(final)[0]
        url = url.replace('&amp;','&').replace('\/','/')
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={"Title": name})
        liz.setProperty("IsPlayable","true")
        liz.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        




def TVRESOLVE(name,url,iconimage,description):
        headers = {'User-Agent':User_Agent}
        referer = url.split('|')[0]
        episode_id = url.split('|')[1]
        key_gen = random_generator()
        link = s.get(referer, headers=headers,verify=False).content
        getc = re.findall(r'<img title=.*?src="(.*?)"', str(link), re.I|re.DOTALL)[0]
        headers = {'Accept': 'image/webp,image/*,*/*;q=0.8', 'Accept-Encoding':'gzip, deflate, sdch, br',
                   'Accept-Language': 'en-US,en;q=0.8', 'Referer': referer, 'User-Agent':User_Agent}
        cookie = s.get(getc,headers=headers,verify=False).cookies.get_dict()
        for i in cookie:
                cookie =  i + '=' + cookie[i]
        addon.log('#######################################url= '+str(url))
        #coookie = hashlib.md5(episode_id + key).hexdigest() + '=%s' %key_gen
        coookie = key + episode_id + key2 + '=%s' %key_gen
        cookie = '%s; %s' %(cookie,coookie)
        a = episode_id + key3
        b = key_gen
        hash_id = __uncensored(a, b)
        hash_id = urllib.quote(hash_id).encode('utf8')
        addon.log('#######################################cookie= '+str(cookie))
        headers = {'Accept-Encoding':'gzip, deflate, sdch', 'Cookie': cookie, 'Referer': referer,
                   'User-Agent':User_Agent,'X-Requested-With':'XMLHttpRequest'}
        request_url =  baseurl + '/ajax/v2_get_sources/' + episode_id + '?hash=' + urllib.quote(hash_id)
        res_quality = []
        stream_url = []
        quality = ''
        try:
                final = s.get(request_url, headers=headers,verify=False).json()
                res_quality = []
                stream_url = []
                quality = ''
                if auto_play == 'true':
                        url = final['playlist'][0]['sources'][0]['file']
                else:
                        match = final['playlist'][0]['sources']
                        for a in match:
                                quality = '[B][I][COLOR indianred]%s[/COLOR][/I][/B]' %a['label']
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
        except:
                final = s.get(request_url, headers=headers,verify=False).text
                res_quality = []
                stream_url = []
                quality = ''
                if auto_play == 'true':
                        url = re.compile('"file":"(.*?)"').findall(final)[0]
                else:
                        match = re.compile('"file":"(.*?)","label":"(.*?)"').findall(final)
                        for stream_url, label in match:
                                if '.srt' not in stream_url:
                                        quality = '[B][I][COLOR indianred]%s[/COLOR][/I][/B]' %label
                                        res_quality.append(quality)
                                        stream_url.append(stream_url)
                        if len(match) >1:
                                dialog = xbmcgui.Dialog()
                                ret = dialog.select('Select Stream Quality',res_quality)
                                if ret == -1:
                                        return
                                elif ret > -1:
                                        url = stream_url[ret]
                        else:
                                url = re.compile('"file":"(.*?)"').findall(final)[0]
        url = url.replace('&amp;','&').replace('\/','/')
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
                contextMenuItems.append(('Play Trailer', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 16, 'url':meta['trailer']})))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if not meta['backdrop_url'] == '':
                liz.setProperty('fanart_image', meta['backdrop_url'])
        else: liz.setProperty('fanart_image', fanart)
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
                liz.setProperty('fanart_image', fanart)
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
        except:
                pass
        episode = name.lower().split('episode[/color]')[1].strip()
        episode = episode.split(':')[0].strip()
        if '0' in season[0]:
                season = season[1]
        if '0' in episode[0]:
                 episode = episode[1]
        show_title = show_title.split('- Season')[0].rstrip()
        addon.log(episode)
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
        contextMenuItems.append(('Show Info', 'XBMC.Action(Info)'))
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)+"&show_title="+urllib.quote_plus(show_title)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
        liz.setInfo(type="Video", infoLabels=meta)
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if not meta['backdrop_url'] == '':
                liz.setProperty('fanart_image', meta['backdrop_url'])
        else:
                liz.setProperty('fanart_image', fanart)
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




def OPEN_URL(url):
    headers = {'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Referer': url, 'Accept-Encoding': 'gzip, deflate, sdch', 'Accept-Language': 'en-US,en;q=0.8'}
    headers['User-Agent'] = User_Agent
    link = s.get(url, headers=headers,verify=False).text
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
        MYEAR()

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
        TVYEAR()

elif mode==13:
        TVSEARCH()

elif mode==14:
        MRESOLVE(name,url,iconimage)

elif mode==15:
        TVRESOLVE(name,url,iconimage,description)

elif mode==16:
        PT(url)

elif mode==17:
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



































































































































































































































































































































































































































































































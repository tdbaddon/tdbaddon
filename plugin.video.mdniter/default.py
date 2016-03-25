import urllib,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os
import urlresolver
import requests
from addon.common.addon import Addon
from addon.common.net import Net
from metahandler import metahandlers
from resources.libs import jsunpack

#niter Add-on Created By Mucky Duck (12/2015)

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
addon_id='plugin.video.mdniter'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
metaset = selfAddon.getSetting('enable_meta')
metaget = metahandlers.MetaData()
baseurl = 'http://niter.co/'
net = Net()



def CAT():
        link = OPEN_URL(baseurl)
        link = link.encode('ascii', 'ignore')
        addDir('[B][COLOR cyan]Movie Search[/COLOR][/B]','url',4,icon,fanart,'')
        addDir('[B][COLOR cyan]Actor/Director Search[/COLOR][/B]','url',8,icon,fanart,'')
        match=re.compile('<li><a href="(.*?)">(.*?)</a></li>').findall(link) 
        for url,name in match:
                if 'relevance' in url:
                        addDir('[B][COLOR cyan]%s[/COLOR][/B]' %name,url,1,icon,fanart,'')
                if 'actors' in url:
                        addDir('[B][COLOR cyan]%s[/COLOR][/B]' %name,url,2,icon,fanart,'')
                if 'directors' in url:
                        addDir('[B][COLOR cyan]%s[/COLOR][/B]' %name,url,2,icon,fanart,'')
        addDir('[B][COLOR cyan]Rating[/COLOR][/B]',baseurl+'movies?relevance=all&genre=all&yearFrom=1931&yearTo=2015&sortBy=rating&numRows=48&view=0',1,icon,fanart,'')
        addDir('[B][COLOR cyan]Genres[/COLOR][/B]',baseurl,5,icon,fanart,'')
        addDir('[B][COLOR cyan]Year[/COLOR][/B]',baseurl,7,icon,fanart,'')
        addDir('[B][COLOR cyan]A/Z[/COLOR][/B]',baseurl+'movies?relevance=all&genre=all&yearFrom=1931&yearTo=2015&sortBy=A-Z&numRows=48&view=0',1,icon,fanart,'')




def INDEX(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, '<figure class="', '</figure>')
        items = len(all_videos)
        for a in all_videos:
                name = regex_from_to(a, 'data-name="', '"')
                name = addon.unescape(name)
                year = regex_from_to(a, 'data-release="', '"')
                url = regex_from_to(a, 'href="', '"')
                thumb = regex_from_to(a, 'src="', '"')
                dis = regex_from_to(a, 'Synopsis:</b>', '</')
                dis = addon.unescape(dis)
                if metaset=='false':
                        addDir2('[B][COLOR white]%s (%s)[/COLOR][/B]' %(name,year),baseurl+url,3,icon,items)
                else:
                        addDir('[B][COLOR white]%s (%s)[/COLOR][/B]' %(name,year),url,3,thumb,fanart,dis)
        try:
                match=re.compile('<li><a href="(.*?)">(.*?)</a></li>').findall(link) 
                for url,name in match:
                    if '&page' in url:
                            if '&' not in name:
                                addDir('[B][COLOR cyan]Page %s[/COLOR][/B]' %name,url,1,icon,fanart,'')
        except: pass
        setView('movies', 'movie-view')




def PEOPLE(url):
        link = OPEN_URL(url)
        print url
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, '<figure class=', '</figure>')
        for a in all_videos:
                name = regex_from_to(a, 'data-name="', '"')
                name = addon.unescape(name)
                url = regex_from_to(a, 'href="', '"')
                thumb = regex_from_to(a, 'src="', '"')
                age = regex_from_to(a, 'data-age="', '"')
                if age=='':
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,6,thumb,fanart,'')
                else:
                        addDir('[B][COLOR white]%s (%s)[/COLOR][/B]' %(name,age),url,6,thumb,fanart,'')
        try:
                match=re.compile('<li><a href="(.*?)">(.*?)</a></li>').findall(link) 
                for url,name in match:
                    if 'page=' in url:
                            if '&' not in name:
                                addDir('[B][COLOR cyan]Page %s[/COLOR][/B]' %name,url,2,icon,fanart,'')
        except: pass
        setView('movies', 'movie-view')




def PINDEX(url):
        link = OPEN_URL(url)
        match=re.compile('<td class="col-xs-6 col-sm-10">\n<a href="(.*?)">(.*?)</a>\n</td>\n<td class="col-xs-4 col-sm-1">\n(.+?)\n</td>').findall(link) 
        items = len(match)
        for url,name,year in match:
                name = addon.unescape(name)
                print url
                addDir2('[B][COLOR white]%s (%s)[/COLOR][/B]' %(name,year),url,3,icon,items)
        try:
                match=re.compile('<li><a href="(.*?)">(.*?)</a></li>').findall(link) 
                for url,name in match:
                    if 'page=' in url:
                            if '&' not in name:
                                addDir('[B][COLOR cyan]Page %s[/COLOR][/B]' %name,url,6,icon,fanart,'')
        except: pass
        setView('movies', 'movie-view')



def LINK(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        try:
                referer = url
                try:
                    RequestURL = re.search(r'emb=(.*?)&',link,re.I).group(1)
                except:
                    RequestURL = re.search(r'emb2=(.*?)&',link,re.I).group(1)

                headers = {'Host': 'videomega.tv', 'Referer': referer, 'User-Agent': User_Agent}
                link = requests.get(RequestURL, headers=headers).content
                if jsunpack.detect(link): #1 these 3 lines taken from urlresolver
                    js_data = jsunpack.unpack(link) #2
                    match = re.search('"src"\s*,\s*"([^"]+)', js_data) #3
                headers = {'Origin': 'videomega.tv', 'Referer': link, 'User-Agent': User_Agent}
                url = match.group(1) + '|' + urllib.urlencode(headers)
                liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
                liz.setInfo(type='Video', infoLabels={'Title':description})
                liz.setProperty("IsPlayable","true")
                liz.setPath(str(url))
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        except:pass
        try:
                referer = url
                RequestURL = 'http://niter.co/player/pk/pk/plugins/player_p2.php'
                form_data = re.findall(r'ic=.*?&em.*?&(.*?)<', str(link), re.I|re.DOTALL)[0].replace('=','_')
                form_data={'url':form_data}
                headers = {'host': 'niter.co', 'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
                           'origin':'http://niter.co', 'referer': referer,
                           'user-agent': User_Agent,'x-requested-with':'XMLHttpRequest'}
                r = requests.post(RequestURL, data=form_data, headers=headers)
                url = re.findall(r'"url":"(.*?)"', str(r.text), re.I|re.DOTALL)[-1]
                host =  url.replace('http://','').replace('https://','').partition('/')[0]
                headers = {'Host': host, 'Referer': referer, 'User-Agent': User_Agent}
                url = url + '|' + urllib.urlencode(headers)
                liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
                liz.setInfo(type='Video', infoLabels={'Title':description})
                liz.setProperty("IsPlayable","true")
                liz.setPath(str(url))
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        except:pass
        try:
                RequestURL = 'http://niter.co/player/pk/pk/plugins/player_p2.php'
                try:
                        form_data={'url': re.search(r'ic=(.*?)&',link,re.I).group(1)}
                except:
                        form_data={'url': re.search(r'ic=(.*?)<',link,re.I).group(1)}
                headers = {'host': 'niter.co', 'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
                           'origin':'http://niter.co', 'referer': url,
                           'user-agent': User_Agent,'x-requested-with':'XMLHttpRequest'}
                r = requests.post(RequestURL, data=form_data, headers=headers)
                url = re.findall(r'"url":"(.*?)"', str(r.text), re.I|re.DOTALL)[-1]
                url = url.replace('.pdf','.mp4')
                headers = {'Host': host, 'Referer': referer, 'User-Agent': User_Agent}
                url = url + '|' + urllib.urlencode(headers)
                liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
                liz.setInfo(type='Video', infoLabels={'Title':description})
                liz.setProperty("IsPlayable","true")
                liz.setPath(url)
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        except:pass
        try:
                referer = url
                url = re.findall(r'dir=(.*?)&', str(link), re.I|re.DOTALL)[0]
                host =  url.replace('http://','').replace('https://','').partition('/')[0]
                headers = {'Host': host, 'Referer': referer, 'User-Agent': User_Agent}
                url = url + '|' + urllib.urlencode(headers)
                liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
                liz.setInfo(type='Video', infoLabels={'Title':description})
                liz.setProperty("IsPlayable","true")
                liz.setPath(str(url))
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        except: pass
        try:
                try:
                        RequestURL = re.search(r'&emb=(.*?)&',link,re.I).group(1)
                except:
                        RequestURL = re.search(r'&emb=(.*?)<',link,re.I).group(1)
                video_id = re.split(r'ef=', RequestURL, re.I)[1]
                form_data={'ref:': video_id}
                headers = {'host': 'up2stream.com','referer': url, 'user-agent': User_Agent,}
                r = requests.get(RequestURL, data=form_data, headers=headers).text
                try:
                        match = re.compile("\,.*?'(.*?)'\.split\('\|'\)").findall(r)[0]
                        try:
                                url_part = re.compile("15,15,\'(.*?)\|").findall(r)[0]
                        except:
                                url_part = re.compile("16,16,\'(.*?)\|").findall(r)[0]
                        try:
                                hash_id = re.split(r"15,15,", str(match), re.I)[1]
                        except:
                                hash_id = re.split(r"16,16,", str(match), re.I)[1]
                        try:
                                hash_id2 = re.split(r"\|cdn\|http\|src\|video\|attr\|vizplay\|org\|", str(hash_id), re.I)[1]
                        except:
                                hash_id2 = re.split(r"\|cdn\|vizplay\|http\|src\|video\|attr\|org\|v\|hash\|.*?\|", str(hash_id), re.I)[1]
    
                        try:
                                url_part2 = re.split(r"\|hash\|st\|mp4\|v\|", str(hash_id2), re.I)[0]
                        except:
                                url_part2 = re.split(r"\|st\|", str(hash_id2), re.I)[0]
                        try:
                                hash_id3 = re.split(r"\|hash\|st\|mp4\|v\|", str(hash_id2), re.I)[1]
                        except:
                                hash_id3 = re.split(r"\|st\|", str(hash_id2), re.I)[1]
                        url_part3 = re.split(r"\|", str(hash_id3), re.I)[0]
                        try:
                                url_part4 = re.split(r"\|mp4\|", str(hash_id3), re.I)[1]
                        except:
                                url_part4 = re.split(r"\|", str(hash_id3), re.I)[1]
                        url = 'http://'+url_part+'.cdn.vizplay.org/v/'+url_part3+'.mp4?st='+url_part2+'&hash='+url_part4
                        print url
                        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
                        liz.setInfo(type='Video', infoLabels={'Title':description})
                        liz.setProperty("IsPlayable","true")
                        liz.setPath(url)
                        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
                except:pass
        except:pass
        




def MSEARCH():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                url = baseurl+'search?q='+search
                link = OPEN_URL(url)
                all_videos = regex_get_all(link, 'data-filter', '</figure>')
                items = len(all_videos)
                for a in all_videos:
                        name = regex_from_to(a, 'data-name="', '"')
                        name = addon.unescape(name)
                        url = regex_from_to(a, 'href="', '"')
                        thumb = regex_from_to(a, 'src="', '"')
                        if metaset=='true':
                                addDir2('[B][COLOR white]%s[/COLOR][/B]' %name,url,3,thumb,items)
                        else:
                                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,3,thumb,fanart,'')
        setView('movies', 'movie-view')




def ADSEARCH():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                url = baseurl+'search?q='+search
                link = OPEN_URL(url)
                all_videos = regex_get_all(link, 'figure class', '</figure>')
                items = len(all_videos)
                for a in all_videos:
                        name = regex_from_to(a, 'alt="', '"')
                        name = addon.unescape(name)
                        url = regex_from_to(a, 'href="', '"')
                        thumb = regex_from_to(a, 'src="', '"')
                        if 'people' in url:
                                if 'noimage' in thumb:
                                        thumb = icon
                                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,6,thumb,fanart,'')
                                else:
                                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,6,thumb,fanart,'')
        setView('movies', 'movie-view')




def GENRE(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<li><a href="(.*?)">(.*?)</a></li>').findall(link) 
        for url,name in match:
                ok = 'genre'
                if ok in url:
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,1,icon,fanart,'')




def YEAR(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<li><a href="(.*?)">(.*?)</a></li>').findall(link) 
        for url,name in match:
                ok = 'year'
                if ok in url:
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
        if iconimage=='':
                iconimage=icon
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
        liz.setProperty('fanart_image', fanart)
        if mode==3:
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
                meta['cover_url']=icon
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
        liz.setInfo( type="Video", infoLabels= meta )
        contextMenuItems = []
        contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)')),
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if not meta['backdrop_url'] == '': liz.setProperty('fanart_image', meta['backdrop_url'])
        else: liz.setProperty('fanart_image', fanart)
        name = name+'[COLOR white]'+'[/COLOR]'
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
        PEOPLE(url)

elif mode==3:
        LINK(url)

elif mode==4:
        MSEARCH()

elif mode==5:
        GENRE(url)

elif mode==6:
        PINDEX(url)

elif mode==7:
        YEAR(url)

elif mode==8:
        ADSEARCH()

xbmcplugin.endOfDirectory(int(sys.argv[1]))

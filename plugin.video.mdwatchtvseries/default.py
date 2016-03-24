import sys,urllib,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os
import requests
from addon.common.addon import Addon
from addon.common.net import Net

#Watch TV Series Add-on Created By Mucky Duck (1/2016)

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
addon_id='plugin.video.mdwatchtvseries'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
baseurl = 'http://seriestv.us/'  #'http://sermov.com/' #'http://tvserieswatch.net/' #'http://tvwatchtvseries.com/'
net = Net()




def CAT():
        addDir('[B][COLOR red]Click Here For Latest Episodes Added[/COLOR][/B]',baseurl,1,icon,fanart,'')
        url = baseurl+'categoryy'
        link = OPEN_URL(url)
        match=re.compile('<li style="width:50%;"><a href=".*?">(.*?) \(.*?\)</a></li>').findall(link) 
        for name in match:
                if 'Season' not in name:
                        name = addon.unescape(name)
                        name = name.encode('ascii', 'ignore').decode('ascii')
                        name = name.replace('&nbsp;','').replace('&#8216;','\'').replace('&#8217;','\'').replace('&#8220;','"').replace('&#8221;','"')
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,4,icon,fanart,'')
        




def INDEX(url):
        link = OPEN_URL(url)
        all_videos = regex_get_all(link, '<li class="border-radius-5 box-shadow">', '</li>')
        for a in all_videos:
                        name = regex_from_to(a, 'href=.*?>', '<').replace(' Watch Online Free','').replace(' Watch Online','').replace('<span>','')
                        name = name.replace('&nbsp;','').replace('&#8216;','\'').replace('&#8217;','\'').replace('&#8220;','"').replace('&#8221;','"').replace('Free Full','')
                        name = addon.unescape(name)
                        name = name.encode('ascii', 'ignore').decode('ascii')
                        name = name.replace('Season','[COLOR red]Season[/COLOR]').replace('Episode','[COLOR red]Episode[/COLOR]')
                        url = regex_from_to(a, 'href="', '"')
                        thumb = regex_from_to(a, 'title=.*?src.*?="', '"')
                        print thumb
                        #dis = regex_from_to(a, '<P>', '<').replace('&nbsp;','').replace('&#8216;','\'').replace('&#8217;','\'').replace('&#8220;','"').replace('&#8221;','"')
                        addDir('[I][B][COLOR white] %s[/COLOR][/B][/I]' %name,url,3,thumb,fanart,'')
        
        try:
                pagen = re.compile('<div class="pagination"><ul><li><span>(.*?)</span>').findall(link)[0]
                addLink('[I][B][COLOR red]%s[/COLOR][/B][/I]' %pagen,'url','',fanart,'')
        except: pass
                        
        try:
                nextp=re.compile('<li><a href="(.*?)">Next &rsaquo;</a></li>').findall(link)[0]
                addDir('[I][B][COLOR red]Next Page >>>[/COLOR][/B][/I]',nextp,1,'',fanart,'')
        except: pass
        
        try:
                pages=re.compile('<li><a href=\'(.*?)\' class="inactive">(.*?)</a>').findall(link)
                for url, name in pages: 
                        addDir('[I][B][COLOR red]Page %s >>>[/COLOR][/B][/I]' %name,url,1,'',fanart,'')
        except: pass
        setView('movies', 'tv-view')




def EPIS(url):
        link = OPEN_URL(url)
        all_videos = regex_get_all(link, '<li class="border-radius-5 box-shadow">', '</li>')
        for a in all_videos:
                        name = regex_from_to(a, 'href=.*?>', '<').replace(' Watch Online Free','').replace(' Watch Online','').replace('<span>','')
                        name = name.replace('&nbsp;','').replace('&#8216;','\'').replace('&#8217;','\'').replace('&#8220;','"').replace('&#8221;','"').replace('Free Full','')
                        name = addon.unescape(name)
                        name = name.encode('ascii', 'ignore').decode('ascii')
                        name = name.replace('Season','[COLOR red]Season[/COLOR]').replace('Episode','[COLOR red]Episode[/COLOR]')
                        url = regex_from_to(a, 'href="', '"')
                        thumb = regex_from_to(a, 'title=.*?src.*?="', '"')
                        print thumb
                        #dis = regex_from_to(a, '<P>', '<').replace('&nbsp;','').replace('&#8216;','\'').replace('&#8217;','\'').replace('&#8220;','"').replace('&#8221;','"')
                        addDir('[I][B][COLOR white] %s[/COLOR][/B][/I]' %name,url,3,thumb,fanart,'')
        try:
                pagen = re.compile('<div class="pagination"><ul><li><span>(.*?)</span>').findall(link)[0]
                addLink('[I][B][COLOR red]%s[/COLOR][/B][/I]' %pagen,'url','',fanart,'')
        except:pass
        try:
                nextp=re.compile('<li><a href="(.*?)">Next &rsaquo;</a></li>').findall(link)[0]
                addDir('[I][B][COLOR red]Next Page >>>[/COLOR][/B][/I]',nextp,2,'',fanart,'')
        except: pass
        
        try:
                pages=re.compile('<li><a href=\'(.*?)\' class="inactive">(.*?)</a>').findall(link)
                for url, name in pages: 
                        addDir('[I][B][COLOR red]Page %s >>>[/COLOR][/B][/I]' %name,url,2,'',fanart,'')
        except: pass
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_TITLE )
        setView('movies', 'tv-view')




def SEAS(url,name):
        link = OPEN_URL(url)
        name = name.replace('[B][COLOR white]','').replace('[/COLOR][/B]','')
        match=re.compile('<li style="width:50%;"><a href="(.*?)">(.*?) \(.*?\)</a></li>').findall(link) 
        for url,season in match:
                season = addon.unescape(season)
                season = season.encode('ascii', 'ignore').decode('ascii')
                season = season.replace('&nbsp;','').replace('&#8216;','\'').replace('&#8217;','\'').replace('&#8220;','"').replace('&#8221;','"')
                if name in season:
                        if 'season' in url: 
                                addDir('[B][COLOR white]%s[/COLOR][/B]' %season,url,2,icon,fanart,'')




def LINK(url):
        link = OPEN_URL(url)
        try:
                RequestURL = re.findall(r'lazy-src="(.*?)"', str(link), re.I|re.DOTALL)[0]
                if '724moviehd.com' in RequestURL:
                        headers = {'host': '724moviehd.com', 'referer': url, 'user-agent': User_Agent}
                elif 'moviecav.com' in RequestURL:
                        headers = {'host': 'moviecav.com', 'referer': url, 'user-agent': User_Agent}
                else:
                        headers = {'host': 'sermov.com', 'referer': url, 'user-agent': User_Agent}
                link = requests.get(RequestURL, headers=headers).text
                if 'sermovold' in RequestURL:
                        url = re.compile('"file":"(.*?)"').findall(link)[0]
                else:
                        try:
                                url = re.compile('"file":"(.*?);').findall(link)[-1]
                        except:
                                url = re.compile('"file":"(.*?);').findall(link)[0]
        except: pass
        try:
                try:
                        RequestURL = re.findall(r'<if.*?rc="(.*?)" .*?>', str(link), re.I|re.DOTALL)[-1]
                except:
                        RequestURL = re.findall(r'<if.*?rc="(.*?)" .*?>', str(link), re.I|re.DOTALL)[0]
                if '724moviehd.com' in RequestURL:
                        headers = {'host': '724moviehd.com', 'referer': url, 'user-agent': User_Agent}
                elif 'moviecav.com' in RequestURL:
                        headers = {'host': 'moviecav.com', 'referer': url, 'user-agent': User_Agent}
                else:
                        headers = {'host': 'sermov.com', 'referer': url, 'user-agent': User_Agent}
                link = requests.get(RequestURL, headers=headers).text
                if 'sermovold' in RequestURL:
                        url = re.compile('"file":"(.*?)"').findall(link)[0]
                else:
                        try:
                                url = re.compile('"file":"(.*?);').findall(link)[-1]
                        except:
                                url = re.compile('"file":"(.*?);').findall(link)[0]
        except: pass
        try:
                form_data={'link': re.search(r'link:"(.*?)"',link,re.I).group(1)}
                headers = {'host' : 'seriestv.us', 'origin' : 'http://seriestv.us', 'referer' : url, 'user-agent' : User_Agent}
                link = requests.post(baseurl+'plugins/gkpluginsphp.php', data=form_data, headers=headers).text
                try:
                        url = re.compile('link":"(.*?)"').findall(link)[-1].replace('\/','/')
                except:
                        url = re.compile('link":"(.*?)"').findall(link)[0].replace('\/','/')
        except:pass
        url = url+'|User-Agent=%s' %User_Agent
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(str(url))
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
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
        liz.setProperty('fanart_image', fanart)
        if mode==3:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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
        EPIS(url)

elif mode==3:
        LINK(url)

elif mode==4:
        SEAS(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

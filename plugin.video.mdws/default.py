import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os
import urlresolver
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net


#Watchseries - By Mucky Duck (03/2015)

addon_id='plugin.video.mdws'
addon = Addon(addon_id, sys.argv)
baseurl = 'http://watchseries.vc'
net = Net()
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))

def CATEGORIES():
        addDir('[B][COLOR yellow]A-Z[/COLOR][/B]',baseurl+'/series',7,art+'mdws.png',fanart)
        addDir('[B][COLOR yellow]Genres[/COLOR][/B]',baseurl,8,art+'mdws.png',fanart)
        addDir('[B][COLOR yellow]TV Schedule[/COLOR][/B]',baseurl+'/tvschedule/-4',11,art+'mdws.png',fanart)
        addDir('[B][COLOR yellow]Popular Episodes Added This Week[/COLOR][/B]',baseurl+'/new',10,art+'mdws.png',fanart)
        addDir('[B][COLOR yellow]Newest Episodes Added This Week[/COLOR][/B]',baseurl+'/latest',9,art+'mdws.png',fanart)
        addDir('[B][COLOR yellow]Search[/COLOR][/B]',baseurl,12,art+'mdws.png',fanart)
         

def ATOZ(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(link)
        for url,name in match:
                ok = ['#','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
                if name in ok:
                        name = name.replace('#','0-9')
                        addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,baseurl+url,1,art+'mdws.png',fanart)

def GENRES(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('title=".+?" href="(.+?)">(.+?)</a></li>\n').findall(link)
        for url,name in match:
                ok = '/genres/'
                if ok in url:
                        addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,baseurl+url,1,art+'mdws.png',fanart)

def SCHEDULE(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)".+?>(.+?)</a></li>').findall(link)
        for url,name in match:
                ok = '/tvschedule/'
                if ok in url:
                        addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,baseurl+url,10,art+'mdws.png',fanart)


def NEW(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('href="(.+?)"><span class=".+?" style="font-weight: bold; float: .+?;"></span>(.+?)</a>').findall(link)
        for url,name in match:
                addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,baseurl+url,4,art+'mdws.png',fanart)

def POPULAR(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('title=".+?" href="(.+?)"><span class=".+?" style=".+?"></span>(.+?)</a></li>').findall(link)
        for url,name in match:
                addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,baseurl+url,4,art+'mdws.png',fanart)


def SEARCH(url):
        keyb = xbmc.Keyboard('', 'Search WatchSeries')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)
                print encode
                url = baseurl+'/search/'+encode
                print url
                match=re.compile('<a title=".+?" href="(.+?)"><b>(.+?)</b></a>').findall(net.http_GET(url).content) 
                for url,name in match:
                        addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,baseurl+url,2,art+'mdws.png',fanart)


def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<li><a title="(.+?)" href="(.+?)">.+?<span class="epnum">').findall(link)
        for name,url in match:
                addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,baseurl+url,2,art+'mdws.png',fanart)

def SEASONS(name,url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<h2 class="lists"><a class="null" href="(.+?)">(.+?)</a></h2>').findall(link)
        for url,name in match:
                 addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,baseurl+url,3,art+'mdws.png',fanart)
        
                


def EPISODES(url):
        link = net.http_GET(url).content
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, '<li>', '</a></li>')
        for a in all_videos:
                name = regex_from_to(a, 'class="" .*?>', '<').replace("&amp;","&").replace('&nbsp;',' ')
                date = regex_from_to(a, 'class="epnum">', '<')
                url = regex_from_to(a, 'href="', '"')
                try:
                        addDir('[COLOR yellow]%s (%s)[/COLOR]' %(name,date),baseurl+url,4,art+'mdws.png',fanart)
                except:
                        addDir('[COLOR yellow]%s[/COLOR]' %name,baseurl+url,4,art+'mdws.png',fanart)




def VIDEOHOSTESTV(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<span style=".+?">(.+?)</span></td><td > <a target="_blank" href="(.+?)".+?</a>').findall(link)
        for name,url in match:
                 addDir('[B][COLOR yellow]%s[/COLOR][/B]' %name,baseurl+url,5,art+'mdws.png',fanart)




def VIDEOLINKSTV(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()

        try:
                match=re.compile('<a class="myButton p2" href="(.+?)">Click Here to Play</a>').findall(net.http_GET(url).content)
                for url in match:
                        RESOLVE(name,url)
                        
        except:
                match=re.compile('<iframe .*?src="(.+?)" .*?>').findall(net.http_GET(url).content)
                for url in match:
                        RESOLVE(name,url)
        
                





def RESOLVE(name,url):
        try:
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                streamlink = urlresolver.resolve(urllib2.urlopen(req).url)
                print streamlink
                url = streamlink
                ok=True
                liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
                xbmc.Player().play(streamlink,liz,False)
        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY LINK DOWN[/B][/COLOR],[COLOR gold][B]PLEASE TRY ANOTHER ONE[/B][/COLOR],7000,"")")
                

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




def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok


def addDir(name,url,mode,iconimage,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        if mode==6:
                liz.setProperty("IsPlayable","true")
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
        
params=get_params()
url=None
name=None
mode=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        types=urllib.unquote_plus(params["types"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)

elif mode==2:
        print ""+url
        SEASONS(name,url)

elif mode==3:
        print ""+url
        EPISODES(url)

elif mode==4:
        print ""+url
        VIDEOHOSTESTV(url)

elif mode==5:
        print ""+url
        VIDEOLINKSTV(url)

elif mode==6:
        print ""+url
        RESOLVE(name,url)

elif mode==7:
        print ""+url
        ATOZ(url)

elif mode==8:
        print ""+url
        GENRES(url)

elif mode==9:
        print ""+url
        NEW(url)

elif mode==10:
        print ""+url
        POPULAR(url)

elif mode==11:
        print ""+url
        SCHEDULE(url)

elif mode==12:
        print ""+url
        SEARCH(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

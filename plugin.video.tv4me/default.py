'''
kinkin
'''

import urllib,urllib2,re,xbmcplugin,xbmcgui,os
import settings
import time,datetime
from datetime import date
from threading import Timer
from helpers import clean_file_name
import shutil
import glob
from threading import Thread
import cookielib
from t0mm0.common.net import Net
from helpers import clean_file_name
import requests
import urlresolver
from metahandler import metahandlers
metainfo = metahandlers.MetaData()
net = Net()


ADDON = settings.addon()
ENABLE_SUBS = settings.enable_subscriptions()
ENABLE_META = settings.enable_meta()
TV_PATH = settings.tv_directory()
AUTOPLAY = settings.autoplay()
FAV = settings.favourites_file()
SUB = settings.subscription_file()
cookie_jar = settings.cookie_jar()
addon_path = os.path.join(xbmc.translatePath('special://home/addons'), '')
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tv4me',  'fanart.jpg'))
iconart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tv4me', 'icon.png'))
base_url = 'http://www.watch-tvseries.net/'
trans_table = ''.join( [chr(i) for i in range(128)] + [' '] * 128 )

def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev>(KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev>')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def CATEGORIES(name):
    addDir("All Shows", base_url + 'play/menulist',7,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tv4me', 'art', 'alltvshows.jpg')), '','')
    addDir("Top Shows", base_url,2,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tv4me', 'art', 'hittvshows.jpg')), '','')
    addDir("New Episodes", base_url,1,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tv4me', 'art', 'newepisodes.jpg')), '','')
    addDir("A-Z", 'url',8,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tv4me', 'art', 'a-z.jpg')), '','')
    addDir("My Favourites", 'url',12,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tv4me', 'art', 'myfavourites.jpg')), '','')
    if ENABLE_SUBS:
        addDir("My Subscriptions", 'url',16,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tv4me', 'art', 'mysubscriptions.jpg')), '','')
    else:
        addDir("[COLOR orange] My Subscriptions (ENABLE IN SETTINGS)[/COLOR]", 'url',16,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tv4me', 'art', 'mysubscriptions.jpg')), '','')
    addDir("Search", 'url',6,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tv4me', 'art', 'search.jpg')), '','')

			
def a_to_z(url):
    alphabet =  ['#', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U','V', 'W', 'X', 'Y', 'Z']
    for a in alphabet:
        addDir(a,  base_url + 'play/menulist',9,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tv4me', 'art', a.lower().replace('#','hash') + '.jpg')), '','menu')
		
def favourites():
    if os.path.isfile(FAV):
        s = read_from_file(FAV)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('QQ')
                title = list1[0]
                title = title.replace('->-', ' & ')
                url = list1[1]
                thumb = list1[2]
                if ENABLE_META:
                    infoLabels = get_meta(title,'tvshow',year=None,season=None,episode=None,imdb=None)
                    if infoLabels['title']=='':
                        title=title
                    else:
                        title=infoLabels['title']
                    if infoLabels['cover_url']=='':
                        iconimage=thumb
                    else:
                        iconimage=infoLabels['cover_url']
                else:
                    infoLabels =None
                    iconimage=thumb
                addDir(title, url,3,thumb, list,'sh',infoLabels=infoLabels)
				
def subscriptions():
    if os.path.isfile(SUB):
        s = read_from_file(SUB)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('QQ')
                title = list1[0]
                title = title.replace('->-', ' & ')
                url = list1[1]
                thumb = list1[2]
                addDir(title, url,3,thumb, list,'sh')
				
def search():
    keyboard = xbmc.Keyboard('', 'Search TV Show', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            search_show(query)
			
def search_show(query):
    header_dict = {}
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; rv:24.0) Gecko/20100101 Firefox/24.0'
    net.set_cookies(cookie_jar)
    link = net.http_GET(base_url + 'play/menulist', headers=header_dict).content.encode("utf-8").rstrip()
    match = re.compile("<li><a href='(.+?)'>(.+?)</a></li>").findall(link)
    for url, title in match:
        if query.lower() in title.lower():
            if not 'http://www.watch-tvseries.net' in url:
                url='http://www.watch-tvseries.net' + url
            if ENABLE_META:
                infoLabels = get_meta(title,'tvshow',year=None,season=None,episode=None,imdb=None)
                if infoLabels['title']=='':
                    title=title
                else:
                    title=infoLabels['title']
                if infoLabels['cover_url']=='':
                    iconimage=iconart
                else:
                    iconimage=infoLabels['cover_url']
            else:
                infoLabels =None
                iconimage=iconart
            list_data = "%sQQ%sQQ%s" % (title, url, iconimage)
            addDir(title, url,3,iconimage, list_data,'sh',infoLabels=infoLabels)
    setView('episodes', 'show')
		
	
def shows(url):
    header_dict = {}
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; rv:24.0) Gecko/20100101 Firefox/24.0'
    net.set_cookies(cookie_jar)
    link = net.http_GET(url, headers=header_dict).content.encode("utf-8").rstrip()
    all_shows = regex_from_to(link,'Top TV Shows', '</div></div></div><div id=')
    match = re.compile('<a href="(.+?)">(.+?)</a>').findall(all_shows)
    for url, title in match:
        if not 'http://www.watch-tvseries.net' in url:
            url='http://www.watch-tvseries.net' + url
        if ENABLE_META:
            infoLabels = get_meta(title,'tvshow',year=None,season=None,episode=None,imdb=None)
            if infoLabels['title']=='':
                name=title
            else:
                name=infoLabels['title']
            if infoLabels['cover_url']=='':
                iconimage=iconart
            else:
                iconimage=infoLabels['cover_url']
        else:
            infoLabels =None
            iconimage=iconart
        list_data = "%sQQ%sQQ%s" % (title, url, iconimage)
        addDir(title, url,3,iconimage, list_data,'sh',infoLabels=infoLabels)
    setView('episodes', 'show')

def a_z_shows(name, url):
    name = str(name)
    header_dict = {}
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; rv:24.0) Gecko/20100101 Firefox/24.0'
    net.set_cookies(cookie_jar)
    link = net.http_GET(url, headers=header_dict).content.encode("utf-8").rstrip()
    match = re.compile("<li><a href='(.+?)'>(.+?)</a></li>").findall(link)
    for url, title in match:
        if not 'http://www.watch-tvseries.net' in url:
            url='http://www.watch-tvseries.net' + url
        tnum = title[:1].replace('9','#').replace('8','#').replace('7','#').replace('6','#').replace('5','#').replace('4','#').replace('3','#').replace('2','#').replace('1','#').replace('0','#')
        if title[:1] == name or tnum == name:
            if ENABLE_META:
                infoLabels = get_meta(title,'tvshow',year=None,season=None,episode=None,imdb=None)
                if infoLabels['title']=='':
                    title=title
                else:
                    title=infoLabels['title']
                if infoLabels['cover_url']=='':
                    iconimage=iconart
                else:
                    iconimage=infoLabels['cover_url']
            else:
                infoLabels =None
                iconimage=iconart
            list_data = "%sQQ%sQQ%s" % (title, url, iconimage)
            addDir(title, url,3,iconimage, list_data,'sh',infoLabels=infoLabels)
    setView('episodes', 'show')
	
def latest_episodes(url):
    header_dict = {}
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; rv:24.0) Gecko/20100101 Firefox/24.0'
    net.set_cookies(cookie_jar)
    link = net.http_GET(url, headers=header_dict).content.encode("utf-8").rstrip()#
    all_episodes = regex_from_to(link,'Latest Episodes', '</div> </div></div>')
    episodes = re.compile('<a href="(.+?)">(.+?)data-original="(.+?)"(.+?)<a href="(.+?)">(.+?)</a> </div> <div class="midestv"> (.+?) </div> <div class="ddestv"> (.+?)</div> </div> </div>').findall(all_episodes)
    for url,a,thumb,b,url2,title,desc,aired in episodes:
        name = "%s - %s" % (title, aired)
        addDirPlayable(name,url,5,thumb, "")
    setView('episodes', 'episodes-view')
	
def grouped_shows(url):
    header_dict = {}
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; rv:24.0) Gecko/20100101 Firefox/24.0'
    net.set_cookies(cookie_jar)
    link = net.http_GET(url, headers=header_dict).content.encode("utf-8").rstrip()
    match = re.compile("<li><a href='(.+?)'>(.+?)</a></li>").findall(link)
    for url, title in match:
        if not 'http://www.watch-tvseries.net' in url:
            url='http://www.watch-tvseries.net' + url
        if ENABLE_META:
            infoLabels = get_meta(title,'tvshow',year=None,season=None,episode=None,imdb=None)
            if infoLabels['title']=='':
                name=title
            else:
                name=infoLabels['title']
            if infoLabels['cover_url']=='':
                iconimage=iconart
            else:
                iconimage=infoLabels['cover_url']
        else:
            infoLabels =None
            iconimage=iconart
        list_data = "%sQQ%sQQ%s" % (title, url, iconimage)
        addDir(title, url,3,iconimage, list_data,'sh',infoLabels=infoLabels)
    setView('episodes', 'show')

def tv_show(name, url, iconimage):
    episodes = []
    if 'tvseries.net' in url:
        site = "ZZnetYY"
    else:
        site = "ZZmeYY"
    net.set_cookies(cookie_jar)
    #url='http://www.watch-tvseries.net' + url
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)
    seasonlist = regex_get_all(link.replace('&', 'and'), '<div class="csseason', '</div> </div> <div class=')
    for s in seasonlist:
        sname = regex_from_to(s, '">', '</div>')
        if sname.startswith('Season 0'):
            sn = sname.replace('Season 0', '')
        else:
            sn = sname.replace('Season ', '')
        eplist = regex_get_all(str(s), '<a', '</a>')
        if ENABLE_META:
            infoLabels=get_meta(name,'tvshow',year=None,season=sn,episode=None)
            if infoLabels['title']=='':
                name=name
            else:
                name=infoLabels['title']
            if infoLabels['cover_url']=='':
                iconimage=iconart
            else:
                iconimage=infoLabels['cover_url']
        else:
            infoLabels =None
            iconimage=iconart
        addDir(sname, 'url',4,iconimage, eplist,site + name,infoLabels=infoLabels)
    setView('episodes', 'seasons-view')
		
def tv_show_episodes(name, list, iconimage, showname):
    list = str(list)
    site = regex_from_to(showname,'ZZ', 'YY')
    splitshnm = showname.split('YY')
    showname = splitshnm[1]
    episodes = re.compile('<a title="(.+?)" href="(.+?)"> <div class="(.+?)data-original="(.+?)"(.+?)nseasnumep"> (.+?) <br(.+?)>(.+?) </div> </div> </a>').findall(list)
    for epname, url, a, thumb, b, snum, c, epnum in episodes:
        url = 'http://www.watch-tvseries.' + site + url
        epnum = epnum.replace('episode ', 'E')
        snum = snum.replace('season ', 'S')
        sn = snum.replace('S0','')
        if epnum.startswith('E0'):
            en = epnum.replace('E0', '')
        else:
            en = epnum.replace('E', '')
        name = "%s%s - %s" % (snum, epnum, clean_file_name(epname))
        if ENABLE_META:
            infoLabels=get_meta(showname,'episode',year=None,season=sn,episode=en)
            if infoLabels['title']=='':
                name = name
            else:
                name = "%s%s %s" % (snum, epnum, infoLabels['title'])
            if infoLabels['cover_url']=='':
                iconimage=thumb
            else:
                iconimage=infoLabels['cover_url']
        else:
            infoLabels =None
            iconimage=iconart
        if AUTOPLAY:
            addDirPlayable(name,url,5,iconimage, showname,infoLabels=infoLabels)
        else:
            addDir(name,url,20,iconimage, showname, showname,infoLabels=infoLabels)
    setView('episodes', 'episodes-view')
		
def play(name, url, iconimage, showname):
    hosturl = url
    site = regex_from_to(hosturl,'www.watch-tvseries.', '/series')
    host = 'www.watch-tvseries.' + site
    vidlinks = "found"
    dp = xbmcgui.DialogProgress()
    dp.create("Opening",showname + ' - ' + name)
    dp.update(0)
    header_dict = {}
    header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    header_dict['Host'] = host
    header_dict['Connection'] = 'keep-alive'
    header_dict['Cache-Control'] = 'max-age=0'
    header_dict['Referer'] = hosturl
    header_dict['User-Agent'] = 'AppleWebKit/<WebKit Rev>'
    link = net.http_GET(url, headers=header_dict).content.replace("'", '"')#.content.encode("utf-8").translate(trans_table)
    net.save_cookies(cookie_jar)
    url1=[]
    if site == 'net':
        key = re.compile('get[(]"http://www.watch-tvseries.net/"[+]updv[+]"(.+?)"').findall(link)
    else:
        key = re.compile('get[(]"http://www.watch-tvseries.me/"[+]updv[+]"(.+?)"').findall(link)
    for url in key:
        url1.append('http://www.watch-tvseries.%s/play/plvids%s' % (site, url))
    match=re.compile('morurlvid[(]"(.+?)"').findall(link)
    nItem=len(match)
    count=0
    for kl in match:
        count+=1
        url = 'http://www.watch-tvseries.net/play/mvideo_' + kl
        response = requests.get(url, allow_redirects=False)
        url1.append(response.headers['location'])
    nItm=len(url1)
    count=0
    for u in url1:
        u=urllib.unquote(u.replace('https://p.wplay.me/red.php?u=',''))
        try:
            title = regex_from_to(u, 'http://', '/')
        except:
            try:
                title = regex_from_to(u, 'https://', '/')
            except:
                title = u
        title = title.replace('embed.','').replace('api.','').replace('www.','')
        count+=1
        titlelist = str(count) + ' of ' + str(nItem) + ': ' + title
        progress = float(count) / float(nItem) * 100  
        dp.update(int(progress), 'Adding link',"")
        if dp.iscanceled():
            return
        if not 'watch-tvseries' in titlelist:
            if AUTOPLAY:
                try:
                    dp = xbmcgui.DialogProgress()
                    dp.create("TV4ME: Trying Links",titlelist)
                    play_videos(name,u,iconimage,showname)
                    return
                except:
                    pass
            else:
                addDirPlayable(title,u,19,iconimage,name+'<>'+showname)
	
def play_videos(name, url, iconimage, showname):
    if '<>' in showname:
        name=showname.split('<>')[0]
        showname=showname.split('<>')[1]
    hosturl = url
    header_dict = {}
    header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    header_dict['Host'] = 'vk.com'
    header_dict['Referer'] = str(hosturl)
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; rv:24.0) Gecko/20100101 Firefox/24.0'
    if 'plvids' in url:
        linkvk = net.http_GET(url).content.encode("utf-8").rstrip()
        if 'mail.ru' in linkvk:
            url = regex_from_to(linkvk, 'src="', '"')
            url = url.replace('.html','.json?ver=0.2.60').replace('embed/','')
            max=0
            link = requests.get(url).content
            cookielink = requests.get(url)
            setcookie = cookielink.headers['Set-Cookie']
            match=re.compile('"key":"(.+?)","url":"(.+?)"').findall(link)
            for q,url in match:
                quality=int(q.replace('p',''))
                if quality > max:
                    max=quality
                    playlink="%s|Cookie=%s" % (url,urllib.quote(setcookie))	
        elif 'http://vk.com/video_ext.php?oid' in linkvk:
            url = regex_from_to(linkvk, 'src="', '"').replace('https://p.wplay.me/red.php?u=','').replace('&amp;', '&') + '&hd=1'
            net.set_cookies(cookie_jar)
            link = net.http_GET(url, headers=header_dict).content.encode("utf-8").rstrip()
            net.save_cookies(cookie_jar)
            if 'url720":"' in link:
                vidlinks = re.compile('url720":"(.+?)"').findall(link)
            elif 'url480":"' in link:
                vidlinks = re.compile('url480":"(.+?)"').findall(link)
            elif 'url360":"' in link:
                vidlinks = re.compile('url360":"(.+?)"').findall(link)
            elif 'url240":"' in link:
                vidlinks = re.compile('url240":"(.+?)"').findall(link)
            else: 
                vidlinks = "removed"
            for playlink in vidlinks:
                playlink = playlink.replace('\/', '/')
        elif 'http://www.youtube.com' in linkvk:
            vidlink = regex_from_to(linkvk, 'src="http://www.youtube.com/embed/', 'wmode').replace('?', '')
            vidlinks = "found"
            playlink = ('plugin://plugin.video.youtube/?action=play_video&videoid=%s' % vidlink)
    else:			
        if 'gorillavid.in' in url:
            link = requests.get(url).text
            playlink = regex_from_to(link, 'file: "', '"')
        elif 'nowvideo' in url:
            headers = {'Referer': hosturl, 'Host': 'embed.nowvideo.sx'}
            link = requests.get(url, headers=headers).text
            key = regex_from_to(link, 'var fkzd="', '"').replace('.', '%2E').replace('-', '%2D')
            file = regex_from_to(link, 'flashvars.file="', '"')
            linkurl = 'http://www.nowvideo.sx/api/player.api.php?cid=1&cid3=undefined&key=%s&user=undefined&file=%s&numOfErrors=0&pass=undefined&cid2=undefined' % (key, file)
            link = open_url(linkurl)
            playlink = regex_from_to(link, 'url=', '&title')
        elif 'ishared' in url:
            link = open_url(url).strip().replace('\n', '').replace('\t', '')
            try:
                playlink = regex_from_to(link, 'var zzzz = "', '"')
            except:
                findfile = regex_from_to(link, 'playlist:', 'type')
                key = regex_from_to(findfile, 'file: ', ',')
                playlink = regex_from_to(link, 'var ' + key + ' = "', '"')
        elif 'vk.com' in url:
            url = url.replace('https://p.wplay.me/red.php?u=','').replace('&amp;', '&') + '&hd=1'
            net.set_cookies(cookie_jar)
            link = net.http_GET(url, headers=header_dict).content.encode("utf-8").rstrip()
            net.save_cookies(cookie_jar)
            if 'url720":"' in link:
                vidlinks = re.compile('url720":"(.+?)"').findall(link)
            elif 'url480":"' in link:
                vidlinks = re.compile('url480":"(.+?)"').findall(link)
            elif 'url360":"' in link:
                vidlinks = re.compile('url360":"(.+?)"').findall(link)
            elif 'url240":"' in link:
                vidlinks = re.compile('url240":"(.+?)"').findall(link)
            else: 
                vidlinks = "removed"
            for playlink in vidlinks:
                playlink = playlink.replace('\/', '/')
        else:
            validresolver = urlresolver.HostedMediaFile(url)
            if validresolver:
                playlink = urlresolver.resolve(url)
            

    
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    listitem = xbmcgui.ListItem(showname + ' ' + name, iconImage=iconimage, thumbnailImage=iconimage)
    playlist.add(playlink,listitem)
    xbmcPlayer = xbmc.Player()
	
    handle = str(sys.argv[1])    
    if handle != "-1":
        listitem.setProperty("IsPlayable", "true")
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    else:
        xbmcPlayer.play(playlist)


	
def add_favourite(name, url, iconimage, dir, text):
    list_data = iconimage.replace('hhhh', 'http:')
    splitdata = list_data.split('QQ')
    name = splitdata[0]
    name = name.replace('->-', ' & ')
    thumb = splitdata[2]
    add_to_list(list_data, dir)
    notification(name, "[COLOR lime]" + text + "[/COLOR]", '5000', thumb)
	
def remove_from_favourites(name, url, iconimage, dir, text):
    list_data = iconimage.replace('hhhh', 'http:')
    splitdata = list_data.split('QQ')
    name = splitdata[0]
    name = name.replace('->-', ' & ')
    thumb = splitdata[2]
    remove_from_list(list_data, dir)
    notification(name, "[COLOR orange]" + text + "[/COLOR]", '5000', thumb)
	
def create_tv_show_strm_files(name, url, iconimage, ntf):
    dialog = xbmcgui.Dialog()
    n = name
    u = url
    l = iconimage
    list_data = iconimage.replace('hhhh', 'http:')
    splitdata = iconimage.split('QQ')
    name = splitdata[0]
    name = name.replace('->-', ' & ')
    thumbmain = splitdata[2]
    tv_show_path = create_directory(TV_PATH, name)
    net.set_cookies(cookie_jar)
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)
    seasonlist = regex_get_all(link.replace('&', 'and'), '<div class="csseason', '</div> </div> <div class=')
    for s in seasonlist:
        sname = regex_from_to(s, '">', '</div>')
        if sname.startswith('Season 0'):
            snum = sname.replace('Season 0', '')
        else:
            snum = sname.replace('Season ', '')
        season_path = create_directory(tv_show_path, str(snum))
        eplist = regex_get_all(str(s), '<a', '</a>')
        for e in eplist:
            episodes = re.compile('<a title="(.+?)" href="(.+?)"> <div class="(.+?)data-original="(.+?)"(.+?)nseasnumep"> (.+?) <br(.+?)>(.+?) </div> </div> </a>').findall(e)
            for epname, url, a, thumb, b, snum, c, epnum in episodes:
                url = 'http://www.watch-tvseries.net' + url
                epnum = epnum.replace('episode ', 'E')
                snum = snum.replace('season ', 'S')
                sn = snum.replace('S0','')
                if epnum.startswith('E0'):
                    en = epnum.replace('E0', '')
                else:
                    en = epnum.replace('E', '')
                ep = "%sx%s" % (sn, en)
                display = "%s %s" % (ep, epname)
                create_strm_file(display, url, "5", season_path, thumbmain, name)
    if ntf == "true" and ENABLE_SUBS:
        if dialog.yesno("Subscribe?", 'Do you want TV[COLOR lime]4[/COLOR]ME to automatically add new', '[COLOR gold]' + name + '[/COLOR]' + ' episodes when available?'):
            add_favourite(n, u, l, SUB, "Added to Library/Subscribed")
        else:
            notification(name, "[COLOR lime]Added to Library[/COLOR]", '5000', thumb)
    if xbmc.getCondVisibility('Library.IsScanningVideo') == False:           
        xbmc.executebuiltin('UpdateLibrary(video)')


def remove_tv_show_strm_files(name, url, iconimage, dir_path):
    dialog = xbmcgui.Dialog()
    splitname = iconimage.split('QQ')
    rname = splitname[0]
    rname = rname.replace('->-', ' & ')
    try:
        path = os.path.join(dir_path, str(rname))
        shutil.rmtree(path)
        remove_from_favourites(name, url, iconimage, SUB, "Removed from Library/Unsubscribed")
        if xbmc.getCondVisibility('Library.IsScanningVideo') == False:
            if dialog.yesno("Clean Library?", '', 'Do you want clean the library now?'):		
                xbmc.executebuiltin('CleanLibrary(video)')		
    except:
        xbmc.log("[TV4ME] Was unable to remove TV show: %s" % (name)) 

		
def create_directory(dir_path, dir_name=None):
    if dir_name:
        dir_path = os.path.join(dir_path, dir_name)
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def create_file(dir_path, file_name=None):
    if file_name:
        file_path = os.path.join(dir_path, file_name)
    file_path = file_path.strip()
    if not os.path.exists(file_path):
        f = open(file_path, 'w')
        f.write('')
        f.close()
    return file_path
	
def create_strm_file(name, url, mode, dir_path, iconimage, showname):
    try:
        strm_string = create_url(name, mode, url=url, iconimage=iconimage, showname=showname)
        filename = clean_file_name("%s.strm" % name)
        path = os.path.join(dir_path, filename)
        if not os.path.exists(path):
            stream_file = open(path, 'w')
            stream_file.write(strm_string)
            stream_file.close()
    except:
        xbmc.log("[TV4ME] Error while creating strm file for : " + name)
		
def create_url(name, mode, url, iconimage, showname):
    name = urllib.quote(str(name))
    data = urllib.quote(str(url))
    iconimage = urllib.quote(str(iconimage))
    showname = urllib.quote(str(showname))
    mode = str(mode)
    url = sys.argv[0] + '?name=%s&url=%s&mode=%s&iconimage=%s&showname=%s' % (name, data, mode, iconimage, showname)
    return url
	
def get_subscriptions():
    try:
        if os.path.isfile(SUB):
            s = read_from_file(SUB)
            search_list = s.split('\n')
            for list in search_list:
                if list != '':
                    list1 = list.split('QQ')
                    title = list1[0]
                    url = list1[1]
                    thumb = list1[2]
                    create_tv_show_strm_files(title, url, list, "false")
    except:
        xbmc.log("[TV4ME] Failed to fetch subscription")

def regex_from_to(text, from_string, to_string, excluding=True):
    if excluding:
        r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
    else:
        r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
    return r

def regex_get_all(text, start_with, end_with):
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r

def strip_text(r, f, t, excluding=True):
    r = re.search("(?i)" + f + "([\S\s]+?)" + t, r).group(1)
    return r


def find_list(query, search_file):
    try:
        content = read_from_file(search_file) 
        lines = content.split('\n')
        index = lines.index(query)
        return index
    except:
        return -1
		
def add_to_list(list, file):
    if find_list(list, file) >= 0:
        return

    if os.path.isfile(file):
        content = read_from_file(file)
    else:
        content = ""

    lines = content.split('\n')
    s = '%s\n' % list
    for line in lines:
        if len(line) > 0:
            s = s + line + '\n'
    write_to_file(file, s)
    xbmc.executebuiltin("Container.Refresh")
    
def remove_from_list(list, file):
    index = find_list(list, file)
    if index >= 0:
        content = read_from_file(file)
        lines = content.split('\n')
        lines.pop(index)
        s = ''
        for line in lines:
            if len(line) > 0:
                s = s + line + '\n'
        write_to_file(file, s)
        xbmc.executebuiltin("Container.Refresh")
		
def write_to_file(path, content, append=False, silent=False):
    try:
        if append:
            f = open(path, 'a')
        else:
            f = open(path, 'w')
        f.write(content)
        f.close()
        return True
    except:
        if not silent:
            print("Could not write to " + path)
        return False

def read_from_file(path, silent=False):
    try:
        f = open(path, 'r')
        r = f.read()
        f.close()
        return str(r)
    except:
        if not silent:
            print("Could not read from " + path)
        return None

def wait_dl_only(time_to_wait, title):
    print 'Waiting ' + str(time_to_wait) + ' secs'    

    progress = xbmcgui.DialogProgress()
    progress.create(title)
    
    secs = 0
    percent = 0
    
    cancelled = False
    while secs < time_to_wait:
        secs = secs + 1
        percent = int((100 * secs) / time_to_wait)
        secs_left = str((time_to_wait - secs))
        remaining_display = ' waiting ' + secs_left + ' seconds for download to start...'
        progress.update(percent, remaining_display)
        xbmc.sleep(1000)
        if (progress.iscanceled()):
            cancelled = True
            break
    if cancelled == True:     
        print 'wait cancelled'
        return False
    else:
        print 'Done waiting'
        return True

		
def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")
	
def get_meta(name,types=None,year=None,season=None,episode=None,imdb=None,episode_title=None):
    if 'tvshow' in types:
        meta = metainfo.get_meta('tvshow',name,'','','')
    if 'episode' in types:
        meta = metainfo.get_episode_meta(name, '', season, episode)
    infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],'fanart': meta['backdrop_url'],'Episode': meta['episode'],'Aired': meta['premiered']}
        
    return infoLabels 
	
def remove_list_duplicates(list_to_check): 
    temp_set = {} 
    map(temp_set.__setitem__, list_to_check, []) 
    return temp_set.keys()
	
def setView(content, viewType):
	if content:
		xbmcplugin.setContent(int(sys.argv[1]), content)
   

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


def addDir(name,url,mode,iconimage,list,description,infoLabels=None):
        suffix = ""
        suffix2 = ""
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+str(iconimage)+"&list="+str(list)+"&description="+str(description)
        ok=True
        contextMenuItems = []
        if name == "My Subscriptions":
            contextMenuItems.append(("[COLOR cyan]Refresh Subscriptions[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=17&list=%s)'%(sys.argv[0], name, url, str(list).replace('http:','hhhh'))))
        if description == "sh":
            if find_list(list, FAV) < 0:
                suffix = ""
                contextMenuItems.append(("[COLOR lime]Add to TV4ME Favourites[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=11&list=%s)'%(sys.argv[0], name, url, str(list).replace('http:','hhhh'))))
            else:
                suffix = ' [COLOR lime]+[/COLOR]'
                contextMenuItems.append(("[COLOR orange]Remove from TV4ME Favourites[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=13&list=%s)'%(sys.argv[0], name, url, str(list).replace('http:','hhhh'))))
            if find_list(list, SUB) < 0:
                suffix2 = ""
                contextMenuItems.append(("[COLOR lime]Add to XBMC Library/Subscribe[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=14&list=%s)'%(sys.argv[0], name, url, str(list).replace('http:','hhhh'))))
            else:
                suffix2 = ' [COLOR cyan][s][/COLOR]'
                contextMenuItems.append(("[COLOR orange]Remove from XBMC Library[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=15&list=%s)'%(sys.argv[0], name, url, str(list).replace('http:','hhhh'))))
        liz=xbmcgui.ListItem(name + suffix + suffix2, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels=infoLabels)
        try:
            liz.setProperty( "fanart_image", infoLabels['fanart'] )
        except:
            liz.setProperty('fanart_image', fanart )
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDirPlayable(name,url,mode,iconimage,showname,infoLabels=None):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&showname="+urllib.quote_plus(showname)
        ok=True
        #contextMenuItems = []
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels=infoLabels)
        try:
            liz.setProperty( "fanart_image", infoLabels['fanart'] )
        except:
            liz.setProperty('fanart_image', fanart )
        #contextMenuItems.append(("[COLOR red]Report an error[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=10&showname=%s)'%(sys.argv[0],name, url, showname)))
        #liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        
              
params=get_params()

url=None
name=None
mode=None
iconimage=None



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
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        start=urllib.unquote_plus(params["start"])
except:
        pass
try:
        list=urllib.unquote_plus(params["list"])
except:
        pass
try:
        showname=urllib.unquote_plus(params["showname"])
except:
        pass
try:
        description=urllib.unquote_plus(params["description"])
except:
        pass


if mode==None or url==None or len(url)<1:
        CATEGORIES(name)

elif mode == 1:
        latest_episodes(url)        
       
elif mode==2:
        shows(url)
		
elif mode==3:
        tv_show(name, url, iconimage)
		
elif mode==4:
        tv_show_episodes(name, list, iconimage, description)
		
elif mode==5:
        play(name, url, iconimage.replace('hhhh', 'http:'), showname)
		
elif mode==6:
        search()
		
elif mode==7:
        grouped_shows(url)
		
elif mode == 8:
        a_to_z(url)
		
elif mode == 9:
        a_z_shows(name,url)
		
elif mode == 11:
        add_favourite(name, url, list, FAV, "Added to Favourites")
		
elif mode == 12:
        favourites()
		
elif mode == 13:
        remove_from_favourites(name, url, list, FAV, "Removed from Favourites")
		
elif mode == 14:
        create_tv_show_strm_files(name, url, list, "true")
		
elif mode == 15:
        remove_tv_show_strm_files(name, url, list, TV_PATH)
		
elif mode == 16:
        subscriptions()
		
elif mode == 17:
        get_subscriptions()
		
elif mode == 18:
        search_show(name)
		
elif mode==19:
        play_videos(name, url, iconimage.replace('hhhh', 'http:'), showname)
		
elif mode==20:
        play(name, url, iconimage.replace('hhhh', 'http:'), list)
		
xbmcplugin.endOfDirectory(int(sys.argv[1]))



import urllib,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os
import requests
from addon.common.addon import Addon
from addon.common.net import Net

#By Mucky Duck (12/2015)

addon_id='plugin.video.md123movies'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
show_tv = selfAddon.getSetting('enable_shows')
baseurl = 'http://123movies.to'
net = Net()

def CAT():
	addDir('[B][COLOR white]Most Favorite[/COLOR][/B]',baseurl+'/movie/filter/movie/favorite/all/all/all/all/all',1,icon,fanart,'')
	addDir('[B][COLOR white]Most Ratings[/COLOR][/B]',baseurl+'/movie/filter/movie/rating/all/all/all/all/all',1,icon,fanart,'')
	addDir('[B][COLOR white]Most Viewed[/COLOR][/B]',baseurl+'/movie/filter/movie/view/all/all/all/all/all',1,icon,fanart,'')
	addDir('[B][COLOR white]Top IMDB[/COLOR][/B]',baseurl+'/movie/filter/movie/imdb_mark/all/all/all/all/all',1,icon,fanart,'')
	addDir('[B][COLOR white]Country[/COLOR][/B]',baseurl+'/movie/filter/all',10,icon,fanart,'')
	addDir('[B][COLOR white]Search[/COLOR][/B]','url',8,icon,fanart,'')
	addDir('[B][COLOR white]Latest[/COLOR][/B]',baseurl+'/movie/filter/movie/latest/all/all/all/all/all',1,icon,fanart,'')
	addDir('[B][COLOR white]Genre[/COLOR][/B]',baseurl+'/movie/filter/all',9,icon,fanart,'')
	addDir('[B][COLOR white]Year[/COLOR][/B]',baseurl+'/movie/filter/all',11,icon,fanart,'')
        if show_tv == 'true':
                addDir('[B][COLOR white]TV[/COLOR][/B]','url',4,icon,fanart,'')

def TV():
        addDir('[B][COLOR white]Most Favorite[/COLOR][/B]',baseurl+'/movie/filter/series/favorite/all/all/all/all/all',2,icon,fanart,'')
        addDir('[B][COLOR white]Most Ratings[/COLOR][/B]',baseurl+'/movie/filter/series/rating/all/all/all/all/all',2,icon,fanart,'')
        addDir('[B][COLOR white]Most Viewed[/COLOR][/B]',baseurl+'/movie/filter/series/view/all/all/all/all/all',2,icon,fanart,'')
        addDir('[B][COLOR white]Top IMDB[/COLOR][/B]',baseurl+'/movie/filter/series/imdb_mark/all/all/all/all/all',2,icon,fanart,'')
        addDir('[B][COLOR white]Country[/COLOR][/B]',baseurl+'/movie/filter/series',10,icon,fanart,'')
        addDir('[B][COLOR white]Search[/COLOR][/B]','url',8,icon,fanart,'')
        addDir('[B][COLOR white]Latest[/COLOR][/B]',baseurl+'/movie/filter/series/latest/all/all/all/all/all',2,icon,fanart,'')
        addDir('[B][COLOR white]Genre[/COLOR][/B]',baseurl+'/movie/filter/series',9,icon,fanart,'')
        addDir('[B][COLOR white]Year[/COLOR][/B]',baseurl+'/movie/filter/series',11,icon,fanart,'')

def GENRE(url):
        link = OPEN_URL(url)
	link = link.encode('ascii', 'ignore')
	match=re.compile('<input class="genre-ids" value="(.*?)" name=".*?"\n.*?type="checkbox" >(.*?)</label>').findall(link) 
	for url2,name in match:
                name = name.replace(' ','')
                if '/series' in url:
                        url2 = baseurl + '/movie/filter/series/latest/'+url2+'/all/all/all/all'
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url2,2,icon,fanart,'')
                else:
                        url2 = baseurl + '/movie/filter/movie/latest/'+url2+'/all/all/all/all'
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url2,1,icon,fanart,'')

def COUNTRY(url):
        link = OPEN_URL(url)
	link = link.encode('ascii', 'ignore')
	match=re.compile('<input class="country-ids" value="(.*?)" name=".*?"\n.*?type="checkbox" >(.*?)</label>').findall(link) 
	for url2,name in match:
                name = name.replace(' ','')
                if '/series' in url:
                        url2 = baseurl + '/movie/filter/series/latest/all/'+url2+'/all/all/all'
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url2,2,icon,fanart,'')
                else:
                        url2 = baseurl + '/movie/filter/movie/latest/all/'+url2+'/all/all/all'
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url2,1,icon,fanart,'')

def YEAR(url):
        link = OPEN_URL(url)
	link = link.encode('ascii', 'ignore')
	match=re.compile('value="(.*?)" name="year"\n.*?>(.*?)</label>').findall(link) 
	for url2,name in match:
                name = name.replace(' ','')
                if '/series' in url:
                        url2 = baseurl + '/movie/filter/series/latest/all/all/'+url2+'/all/all'
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url2,2,icon,fanart,'')
                        
                else:
                        url2 = baseurl + '/movie/filter/movie/latest/all/all/'+url2+'/all/all'
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url2,1,icon,fanart,'')
                        
        if '/series' in url:
                addDir('[B][COLOR white]Older[/COLOR][/B]',baseurl+'/movie/filter/series/latest/all/all/older-2012/all/all',2,icon,fanart,'')
        else:
                addDir('[B][COLOR white]Older[/COLOR][/B]',baseurl+'/movie/filter/movie/latest/all/all/older-2012/all/all',1,icon,fanart,'')

def INDEX(url):
	link = OPEN_URL(url)
	link = link.encode('ascii', 'ignore').decode('ascii')
	all_videos = regex_get_all(link, '<div class="ml-item">', '</h2></span>')
	for a in all_videos:
		name = regex_from_to(a, 'title="', '"').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'")
		url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
		icon = regex_from_to(a, 'original="', '"')
		#dis = regex_from_to(a, 'data-url="', '"')[0].replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'")
		if 'Season' not in name:
			addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url+'watching.html',3,icon,fanart,'')
	try:
		nextp=re.compile('<li class="next"><a href="(.*?)" data-ci-pagination-page=".*?" rel="next">').findall(link)[0]
		addDir('[B][COLOR red]Next Page>>>[/COLOR][/B]',nextp,1,icon,fanart,'')
	except: pass
	setView('movies', 'show-view')

def INDEX2(url):
	link = OPEN_URL(url)
	link = link.encode('ascii', 'ignore').decode('ascii')
	all_videos = regex_get_all(link, '<div class="ml-item">', '</h2></span>')
	for a in all_videos:
		name = regex_from_to(a, 'title="', '"').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'")
		url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
		icon = regex_from_to(a, 'original="', '"')
		#dis = regex_from_to(a, '<p>', '</p>').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'")
		if 'Season' in name:
			addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url+'watching.html',6,icon,fanart,'')
	try:
		nextp=re.compile('<li class="next"><a href="(.*?)" data-ci-pagination-page=".*?" rel="next">').findall(link)[0]
		addDir('[B][COLOR red]Next Page>>>[/COLOR][/B]',nextp,2,icon,fanart,'')
	except: pass
	setView('movies', 'show-view')

def EPIS(url):
        link = OPEN_URL(url)
	token = re.compile('token="(.*?)"').findall(link)[0]
	video_id = re.compile('-id="(.*?)"').findall(link)[0]
	request_url =  'http://123movies.to/ajax/get_episodes/'+video_id+'/'+token
	link = OPEN_URL(request_url)
	all_videos = regex_get_all(link, '<a', '</a>')
	for a in all_videos:
		name = regex_from_to(a, 'title="', '"').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'")
		hash_id = regex_from_to(a, 'hash="', '"')
		episode_id = regex_from_to(a, 'episode-id="', '"')
		url =  'http://123movies.to/ajax/load_episode/'+episode_id+'/'+hash_id
		addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,7,icon,fanart,'')
	setView('movies', 'show-view')

def LINKS(url):
	link = OPEN_URL(url)
	token = re.compile('token="(.*?)"').findall(link)[0]
	video_id = re.compile('-id="(.*?)"').findall(link)[0]
	request_url =  'http://123movies.to/ajax/get_episodes/'+video_id+'/'+token
	
        
	
	try:
                link = OPEN_URL(request_url)
                all_videos = regex_get_all(link, '"server-9"', '"clearfix"')
                for a in all_videos:
                        print
                        hash_id = regex_from_to(a, 'hash="', '"')
                        episode_id = regex_from_to(a, 'episode-id="', '"')


                        
                        #hash_id = re.compile(r'hash="(.*?)"').findall(link)[0]
                        #episode_id = re.compile(r'episode-id="(.*?)"').findall(link)[0]
                        request_url =  'http://123movies.to/ajax/load_episode/'+episode_id+'/'+hash_id
                        headers = {'host': '123movies.to', 'referer': url,
                                   'user-agent':User_Agent,'x-requested-with':'XMLHttpRequest'}
                        link = OPEN_URL(request_url)
                        url = re.compile('file="(.*?)"').findall(link)[-1]
                        if 'http://sub.' in url:
                                url = re.compile('file="(.*?)"').findall(link)[-2]
                                if 'http://sub.' in url:
                                        url = re.compile('file="(.*?)"').findall(link)[-3]
                                        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
                                        liz.setInfo(type='Video', infoLabels={'Title':description})
                                        liz.setProperty("IsPlayable","true")
                                        liz.setPath(url)
                                        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
                                else:
                                        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
                                        liz.setInfo(type='Video', infoLabels={'Title':description})
                                        liz.setProperty("IsPlayable","true")
                                        liz.setPath(url)
                                        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
                        else:
                                liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
                                liz.setInfo(type='Video', infoLabels={'Title':description})
                                liz.setProperty("IsPlayable","true")
                                liz.setPath(url)
                                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	except:
		url = re.compile('file="(.*?)"').findall(link)[0]
		liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
		liz.setInfo(type='Video', infoLabels={'Title':description})
		liz.setProperty("IsPlayable","true")
		liz.setPath(url)
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

def LINKS2(url):
	headers = {'host': '123movies.to', 'referer': url,
                   'user-agent':User_Agent,'x-requested-with':'XMLHttpRequest'}
        link = requests.get(url, headers=headers, allow_redirects=False).text
	try:
                url = re.compile('file="(.*?)"').findall(link)[-1]
                if 'http://sub' in url:
                        url = re.compile('file="(.*?)"').findall(link)[-2]
                        if 'http://sub.' in url:
                                url = re.compile('file="(.*?)"').findall(link)[--3]
                                liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
                                liz.setInfo(type='Video', infoLabels={'Title':description})
                                liz.setProperty("IsPlayable","true")
                                liz.setPath(url)
                                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
                        else:
                                liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
                                liz.setInfo(type='Video', infoLabels={'Title':description})
                                liz.setProperty("IsPlayable","true")
                                liz.setPath(url)
                                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
                else:
			liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
			liz.setInfo(type='Video', infoLabels={'Title':description})
			liz.setProperty("IsPlayable","true")
			liz.setPath(url)
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        except:
                url = re.compile('file="(.*?)"').findall(link)[0]
                liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
                liz.setInfo(type='Video', infoLabels={'Title':description})
                liz.setProperty("IsPlayable","true")
                liz.setPath(url)
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz) 
	

def SEARCH(query,type):
	if query:
		search = query.replace(' ','+')
	else:
		keyb = xbmc.Keyboard('', 'Type in Query')
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText().replace(' ','+')
			if search == '':
				xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]EMPTY QUERY[/B][/COLOR],Aborting search,7000,"+icon+")")
				return
			else: pass
	url = baseurl+'/movie/search/'+search
	print url
	link = OPEN_URL(url)
	link = link.encode('ascii', 'ignore').decode('ascii')
	all_videos = regex_get_all(link, '<div class="ml-item">', '</h2></span>')
	for a in all_videos:
		name = regex_from_to(a, 'title="', '"').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'")
		url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
		icon = regex_from_to(a, 'original="', '"')
		#dis = regex_from_to(a, '<p>', '</p>').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'")
		if 'Season' in name:
			if type != 'tv':
				addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url+'watching.html',6,icon,fanart,'')
		else:
			if type != 'movie':
				addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url+'watching.html',3,icon,fanart,'')
# OpenELEQ: query & type-parameter (edited 27 lines above)

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
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
	liz.setProperty('fanart_image', fanart)
	if mode==3 or mode==7:
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
	link = link.encode('ascii', 'ignore')
	return link

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
query=None
type=None
# OpenELEQ: query & type-parameter (added 2 lines above)

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
	query=urllib.unquote_plus(params["query"])
except:
	pass
try:
	type=urllib.unquote_plus(params["type"])
except:
	pass
# OpenELEQ: query & type-parameter (added 8 lines above)

if mode==None or url==None or len(url)<1:
	CAT()

elif mode==1:
	INDEX(url)

elif mode==2:
	INDEX2(url)

elif mode==3:
	LINKS(url)

elif mode==4:
	TV()

elif mode==6:
	EPIS(url)

elif mode==7:
	LINKS2(url)

elif mode==8:
	SEARCH(query,type)
# OpenELEQ: query & type-parameter (added to line above)

elif mode==9:
	GENRE(url)

elif mode==10:
	COUNTRY(url)

elif mode==11:
	YEAR(url)





xbmcplugin.endOfDirectory(int(sys.argv[1]))

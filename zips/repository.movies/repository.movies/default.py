import base64,hashlib,os,random,re,requests,shutil,string,sys,urllib
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs
from addon.common.addon import Addon
from addon.common.net import Net

#This is muckyducks code i have just borrowed the goognes, this is all his hard work.

addon_id='repository.movies'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
addon_name = selfAddon.getAddonInfo('name')
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
show_tv = selfAddon.getSetting('enable_shows')
baseurl = selfAddon.getSetting('base_url')
s = requests.session()
net = Net()



def CAT():
	addDir('[B][COLOR lime]Search[/COLOR][/B]','url',8,icon,fanart,'')
	addDir('[B][COLOR lime]Latest[/COLOR][/B]',baseurl+'/movie/filter/movie/latest/all/all/all/all/all',1,icon,fanart,'')
	addDir('[B][COLOR lime]Genre[/COLOR][/B]',baseurl+'/movie/filter/all',9,icon,fanart,'')
	addDir('[B][COLOR lime]Year[/COLOR][/B]',baseurl+'/movie/filter/all',11,icon,fanart,'')
	if show_tv == 'true':addDir('[B][COLOR lime]TV[/COLOR][/B]','url',4,icon,fanart,'')


def TV():
        addDir('[B][COLOR lime]Most Favorite[/COLOR][/B]',baseurl+'/movie/filter/series/favorite/all/all/all/all/all',2,icon,fanart,'')
        addDir('[B][COLOR lime]Most Ratings[/COLOR][/B]',baseurl+'/movie/filter/series/rating/all/all/all/all/all',2,icon,fanart,'')
        addDir('[B][COLOR lime]Most Viewed[/COLOR][/B]',baseurl+'/movie/filter/series/view/all/all/all/all/all',2,icon,fanart,'')
        addDir('[B][COLOR lime]Top IMDB[/COLOR][/B]',baseurl+'/movie/filter/series/imdb_mark/all/all/all/all/all',2,icon,fanart,'')
        addDir('[B][COLOR lime]Country[/COLOR][/B]',baseurl+'/movie/filter/series',10,icon,fanart,'')
        addDir('[B][COLOR lime]Search[/COLOR][/B]','url',8,icon,fanart,'')
        addDir('[B][COLOR lime]Latest[/COLOR][/B]',baseurl+'/movie/filter/series/latest/all/all/all/all/all',2,icon,fanart,'')
        addDir('[B][COLOR lime]Genre[/COLOR][/B]',baseurl+'/movie/filter/series',9,icon,fanart,'')
        addDir('[B][COLOR lime]Year[/COLOR][/B]',baseurl+'/movie/filter/series',11,icon,fanart,'')


def GENRE(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<input class="genre-ids" value="(.*?)" name=".*?"\n.*?type="checkbox" >(.*?)</label>').findall(link)
        for url2,name in match:
                name = name.replace(' ','')
                if '/series' in url:
                        url2 = baseurl + '/movie/filter/series/latest/'+url2+'/all/all/all/all'
                        addDir('[B][COLOR lime]%s[/COLOR][/B]' %name,url2,2,icon,fanart,'')
                else:
                        url2 = baseurl + '/movie/filter/movie/latest/'+url2+'/all/all/all/all'
                        addDir('[B][COLOR lime]%s[/COLOR][/B]' %name,url2,1,icon,fanart,'')


def COUNTRY(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<input class="country-ids" value="(.*?)" name=".*?"\n.*?type="checkbox" >(.*?)</label>').findall(link)
        for url2,name in match:
                name = name.replace(' ','')
                if '/series' in url:
                        url2 = baseurl + '/movie/filter/series/latest/all/'+url2+'/all/all/all'
                        addDir('[B][COLOR lime]%s[/COLOR][/B]' %name,url2,2,icon,fanart,'')
                else:
                        url2 = baseurl + '/movie/filter/movie/latest/all/'+url2+'/all/all/all'
                        addDir('[B][COLOR lime]%s[/COLOR][/B]' %name,url2,1,icon,fanart,'')


def YEAR(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('value="(.*?)" name="year"\n.*?>(.*?)</label>').findall(link)
        for url2,name in match:
                name = name.replace(' ','')
                if '/series' in url:
                        url2 = baseurl + '/movie/filter/series/latest/all/all/'+url2+'/all/all'
                        addDir('[B][COLOR lime]%s[/COLOR][/B]' %name,url2,2,icon,fanart,'')
                        
                else:
                        url2 = baseurl + '/movie/filter/movie/latest/all/all/'+url2+'/all/all'
                        addDir('[B][COLOR lime]%s[/COLOR][/B]' %name,url2,1,icon,fanart,'')
                        
        if '/series' in url:
                addDir('[B][COLOR lime]Older[/COLOR][/B]',baseurl+'/movie/filter/series/latest/all/all/older-2012/all/all',2,icon,fanart,'')
        else:
                addDir('[B][COLOR lime]Older[/COLOR][/B]',baseurl+'/movie/filter/movie/latest/all/all/older-2012/all/all',1,icon,fanart,'')

def INDEX(url):
	link = OPEN_URL(url)
	link = link.encode('ascii', 'ignore').decode('ascii')
	addon.log('#######################link = '+str(link))
	all_videos = regex_get_all(link, 'class="ml-item">', '</h2></span>')
	for a in all_videos:
		name = regex_from_to(a, 'title="', '"').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'")
		url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
		icon = regex_from_to(a, 'original="', '"')
		qual = regex_from_to(a, 'mli-quality">', '<')
		if 'Season' not in name:
			addDir('[B][COLOR lime]%s[/COLOR][/B][B][I][COLOR orange](%s)[/COLOR][/I][/B]' %(name,qual),url+'watching.html',3,icon,fanart,'')
	try:
		nextp=re.compile('<li class="next"><a href="(.*?)" data-ci-pagination-page=".*?" rel="next">').findall(link)[0]
		addDir('[B][COLOR orange]Next Page>>>[/COLOR][/B]',nextp,1,icon,fanart,'')
	except: pass
	setView('movies', 'show-view')


def INDEX2(url):
	link = OPEN_URL(url)
	link = link.encode('ascii', 'ignore').decode('ascii')
	all_videos = regex_get_all(link, 'class="ml-item">', '</h2></span>')
	for a in all_videos:
		name = regex_from_to(a, 'title="', '"').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'")
		url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
		icon = regex_from_to(a, 'original="', '"')
		#dis = regex_from_to(a, '<p>', '</p>').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'")
		if 'Season' in name:
			addDir('[B][COLOR lime]%s[/COLOR][/B]' %name,url+'watching.html',6,icon,fanart,'')
	try:
		nextp=re.compile('<li class="next"><a href="(.*?)" data-ci-pagination-page=".*?" rel="next">').findall(link)[0]
		addDir('[B][COLOR orange]Next Page>>>[/COLOR][/B]',nextp,2,icon,fanart,'')
	except: pass
	setView('tvshows', 'show-view')


key = '87wwxtp3dqii'
key2 = '7bcq9826avrbi6m49vd7shxkn985mhod'


def EPIS(url):
        link = OPEN_URL(url)
        referer = url
        video_id = re.compile('id: "(.*?)"').findall(link)[0]
        request_url =  baseurl + '/ajax/v2_get_episodes/'+video_id#+'/'+token
        link2 = OPEN_URL(request_url)
        all_links = regex_get_all(link2, '"server-10"', '"clearfix"')
        all_videos = regex_get_all(str(all_links), '<a', '</a>')
        for a in all_videos:
                name = regex_from_to(a, 'title="', '"').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'")
                key_gen = random_generator()
                episode_id = regex_from_to(a, 'episode-id="', '"')

                coookie = hashlib.md5(episode_id + key).hexdigest() + '=%s' %key_gen
                getc = re.findall(r'<img title=.*?src="(.*?)"', str(link), re.I|re.DOTALL)[0]
                headers = {'Accept': 'image/webp,image/*,*/*;q=0.8', 'Accept-Encoding':'gzip, deflate, sdch, br',
                           'Accept-Language': 'en-US,en;q=0.8', 'Referer': referer, 'User-Agent':User_Agent}
                cookie = s.get(getc,headers=headers,verify=False).cookies.get_dict()
                for i in cookie:
                        cookie =  i + '=' + cookie[i]
                a= episode_id + key2
                b= key_gen
                hash_id = __uncensored(a, b)
                cookie = '%s; %s' %(cookie,coookie)

                a= episode_id + key2
                b= key_gen
                hash_id = __uncensored(a, b)
                headers = referer + '\+' + cookie
                url =  baseurl + '/ajax/v2_get_sources/' + episode_id + '?hash=' + urllib.quote(hash_id).encode('utf8')
                addDir('[B][COLOR lime]%s[/COLOR][/B]' %name,url,7,icon,fanart,headers)
        setView('tvshows', 'show-view')


def LINKS(url):
        link = OPEN_URL(url)
        referer = url
        video_id = re.compile('id: "(.*?)"').findall(link)[0]
        request_url =  baseurl + '/ajax/v2_get_episodes/'+video_id
        getc = re.findall(r'<img title=.*?src="(.*?)"', str(link), re.I|re.DOTALL)[0]
        headers = {'Accept': 'image/webp,image/*,*/*;q=0.8', 'Accept-Encoding':'gzip, deflate, sdch, br',
                   'Accept-Language': 'en-US,en;q=0.8', 'Referer': referer, 'User-Agent':User_Agent}
        cookie = s.get(getc,headers=headers,verify=False).cookies.get_dict()
        for i in cookie:
                cookie =  i + '=' + cookie[i]
        link = OPEN_URL(request_url)
        try:
                all_videos = regex_get_all(link, '"server-10"', '"clearfix"')
                for a in all_videos:
                        episode_id = regex_from_to(a, 'episode-id="', '"')
                        key_gen = random_generator()
                        coookie = hashlib.md5(episode_id + key).hexdigest() + '=%s' %key_gen
                        cookie = '%s; %s' %(cookie,coookie)
                        a= episode_id + key2
                        b= key_gen
                        hash_id = __uncensored(a, b)
                        request_url2 =  baseurl + '/ajax/v2_get_sources/' + episode_id + '?hash=' + urllib.quote(hash_id).encode('utf8')
                        headers = {'Accept-Encoding':'gzip, deflate, sdch', 'Cookie':cookie, 'Referer': referer,
                                   'User-Agent':User_Agent,'x-requested-with':'XMLHttpRequest','Accept':'application/json, text/javascript, */*; q=0.01'}
                        link = s.get(request_url2, headers=headers).text
                        url = re.compile('"file":"(.*?)"').findall(link)[0]
                        url = url.replace('&amp;','&').replace('\/','/')
                        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
                        liz.setInfo(type='Video', infoLabels={"Title": name})
                        liz.setProperty("IsPlayable","true")
                        liz.setPath(url)
                        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        except:
                all_videos = regex_get_all(link, '"server-8"', '"clearfix"')
                for a in all_videos:
                        episode_id = regex_from_to(a, 'episode-id="', '"')
                        key_gen = random_generator()
                        coookie = hashlib.md5(episode_id + key).hexdigest() + '=%s' %key_gen
                        cookie = '%s; %s' %(cookie,coookie)
                        a= episode_id + key2
                        b= key_gen
                        hash_id = __uncensored(a, b)
                        request_url2 =  baseurl + '/ajax/v2_get_sources/' + episode_id + '?hash=' + urllib.quote(hash_id).encode('utf8')
                        headers = {'Accept-Encoding':'gzip, deflate, sdch', 'Cookie':cookie, 'Referer': referer,
                                   'User-Agent':User_Agent,'x-requested-with':'XMLHttpRequest','Accept':'application/json, text/javascript, */*; q=0.01'}
                        link = s.get(request_url2, headers=headers).text
                        url = re.compile('"file":"(.*?)"').findall(link)[0]
                        url = url.replace('&amp;','&').replace('\/','/')
                        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
                        liz.setInfo(type='Video', infoLabels={"Title": name})
                        liz.setProperty("IsPlayable","true")
                        liz.setPath(url)
                        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        '''except:
                url = re.compile('"file":"(.*?)"').findall(link)[0]
                url = url.replace('&amp;','&').replace('\/','/')
                liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
                liz.setInfo(type='Video', infoLabels={"Title": name})
                liz.setProperty("IsPlayable","true")
                liz.setPath(url)
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)'''


def LINKS2(url,description):
        split_head = re.split(r"\+", str(description), re.I)
        referer = split_head[0]
        coookie = split_head[1]
        headers = {'Referer': referer, 'Cookie': coookie, 'user-agent':User_Agent,'x-requested-with':'XMLHttpRequest'}
        link = requests.get(url, headers=headers, allow_redirects=False).text
        url = re.compile('"file":"(.*?)"').findall(link)[0]
        url = url.replace('&amp;','&').replace('\/','/')
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={"Title": name})
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
	all_videos = regex_get_all(link, 'ml-item">', '</h2></span>')
	for a in all_videos:
		name = regex_from_to(a, 'title="', '"').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'")
		url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
		icon = regex_from_to(a, 'original="', '"')
		#dis = regex_from_to(a, '<p>', '</p>').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'")
		if 'Season' in name:
			if type != 'tv':
				addDir('[B][COLOR lime]%s[/COLOR][/B]' %name,url+'watching.html',6,icon,fanart,'')
		else:
			if type != 'movie':
				addDir('[B][COLOR lime]%s[/COLOR][/B]' %name,url+'watching.html',3,icon,fanart,'')
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



def random_generator(size=16, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


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
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
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
	link = s.get(url, headers=headers, verify=False).text
	link = link.encode('ascii', 'ignore')
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
        elif addon.get_setting(viewType) == 'Default View':
            VT = addon.get_setting('default-view')

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
	LINKS2(url,description)

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
























































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































                        

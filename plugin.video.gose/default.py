# -*- coding: utf-8 -*-

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,json,time
import base64,hashlib,random,string
from resources.lib.i4a_request import open_url
from resources.lib.common import Addon
from resources.lib.i4a_tools import i4a
import re,sys,urllib

# THIS ADDON IS A 123MOVIES REBUILD AND NOW RUNS FROM THE GOMOVIES WEBSITE : BY INSIDE4NDROID 

# REMOVED MOVIES AND FIXED HOW THE EPISODES LOAD

#MUCKY DUCK IS THE ORIGINAL CODE CREATOR I JUST MODIFIED IT TO WORK SO MASSIVE THANKS AND CREDIT TO HIM.

#THE REASON I MADE THIS ADDON WORK AND IMPLEMENTED THE MODIFIED CODE BY ME WAS BECAUSE MUCKY DUCK HAS VANISHED AND I PERSONALLY LOVED 123MOVIES 

#INSIDE4NDROID 07:10AM 1/05/2017

addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon = Addon(addon_id, sys.argv)
addon_name = addon.get_name()
addon_path = addon.get_path()
i4a = i4a(addon_id, sys.argv)
auto_play = 'true'
metaset = addon.get_setting('tv_show_meta')
show_add_set = 'true'
art = i4a.get_art()
icon = addon.get_icon()
fanart = addon.get_fanart()
sort_method = xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE_IGNORE_THE)
baseurl = 'https://gomovies.to'
reload(sys)
sys.setdefaultencoding("utf-8")

def MAIN():
	filt = 'series'
	filter_url = baseurl+'/movie/filter/%s/%s/all/all/all/all/all'
	i4a.addDir({'mode': 'search', 'name':'[B][COLOR yellow]Search[/COLOR][/B]', 'url':'url', 'content':'tvshows'})
	i4a.addDir({'mode': '2', 'name':'[B][COLOR yellow]Top Rated (by users)[/COLOR][/B]', 'url':filter_url %(filt,'rating'), 'content':'tvshows'})
	i4a.addDir({'mode': '2', 'name':'[B][COLOR yellow]Top Rated (imdb)[/COLOR][/B]', 'url':filter_url %(filt,'imdb_mark'), 'content':'tvshows'})
	i4a.addDir({'mode': '2', 'name':'[B][COLOR yellow]Most Viewed[/COLOR][/B]', 'url':filter_url %(filt,'view'), 'content':'tvshows'})
	i4a.addDir({'mode': '2', 'name':'[B][COLOR yellow]Recently Added[/COLOR][/B]', 'url':filter_url %(filt,'latest'), 'content':'tvshows'})
	i4a.addDir({'mode': '4', 'name':'[B][COLOR yellow]Genres[/COLOR][/B]', 'url':baseurl+'/movie/filter', 'content':'tvshows'})
	i4a.addDir({'mode': '5', 'name':'[B][COLOR yellow]Years[/COLOR][/B]', 'url':baseurl+'/series/filter', 'content':'tvshows'})
	i4a.addDir({'mode':'addon_settings', 'name':'[COLOR yellow][B]Settings[/B][/COLOR]', 'url':'url'}, is_folder=False, is_playable=False)
	i4a.addDir({'mode':'addon_support', 'name':'[COLOR yellow][B]Support[/B][/COLOR]', 'url':'url'}, is_folder=False, is_playable=False)
	if metaset=='true':
		setView('movies', 'MAIN')
	else: xbmc.executebuiltin('Container.SetViewMode(50)')




def INDEX(url,content):
	link = open_url(url).content
	all_videos = i4a.regex_get_all(link, 'class="ml-item">', '</h2></span>')
	items = len(all_videos)
	for a in all_videos:
		name = i4a.regex_from_to(a, 'title="', '"')
		url = i4a.regex_from_to(a, 'href="', '"')
		thumb = i4a.regex_from_to(a, 'original="', '"')
		qual = i4a.regex_from_to(a, 'mli-quality">', '<')
		eps = i4a.regex_from_to(a, '"mli-eps">', '</')
		eps = eps.replace('<span>',' ').replace('<i>',' ')
		if eps:
			data = name.split('- Season')
			sorttitle = data[0].strip()
			try:
				season = data[1].strip()
			except:
				season = ''
			i4a.addDir({'mode': '3', 'name':'[B][COLOR white]%s[/COLOR] [I][COLOR yellow](%s)[/COLOR][/I][/B]' %(name,eps),'title':sorttitle, 'url':url+'watching.html', 'iconimage':thumb, 'content':'tvshows', 'season':season},{'sorttitle':sorttitle}, fan_art={'icon':thumb}, item_count=items)
	try:
		nextp = re.compile('<li class="next"><a href="(.*?)" data-ci-pagination-page=".*?" rel="next">').findall(link)[0]
		i4a.addDir({'mode': '2', 'name':'[B][COLOR red]Next Page>>>[/COLOR][/B]', 'url':nextp, 'content':'tvshows'})
	except: pass
	if metaset=='true':
		setView('movies', 'MAIN')
	else: xbmc.executebuiltin('Container.SetViewMode(50)')
	addon.end_of_directory()

def EPIS(title, url, iconimage, content, season):
	link = open_url(url).content
	referer = url
	media_id = re.compile('id: "([^"]+)"').findall(link)[0]
	request_url = '%s/ajax/movie_episodes/%s' %(baseurl,media_id)
	headers = {'Accept-Encoding':'gzip, deflate, sdch, br', 'Referer':referer, 'User-Agent':i4a.User_Agent()}
	link2 = open_url(request_url, headers=headers, verify=False).json()
	try:
		all_links = i4a.regex_get_all(link2['html'], '>Server 8<', '"clearfix"')
		all_videos = i4a.regex_get_all(str(all_links), '<a', '</a>')
		items = len(all_videos)
	except:
		all_links = i4a.regex_get_all(link2['html'], '>Server 10<', '"clearfix"')
		all_videos = i4a.regex_get_all(str(all_links), '<a', '</a>')
		items = len(all_videos)
		
	for a in all_videos:
		name = i4a.regex_from_to(a, 'title="', '"')
		episode_id = i4a.regex_from_to(a, 'data-id="', '"')
		headers = referer + '\|' + episode_id + '\|' + media_id
		url =  '%s/ajax/movie_sources/%s' %(baseurl,episode_id)
		try:
			episode = name.split('Episode')[1].strip()[:2]
		except:pass
		fan_art = {'icon':iconimage}
		i4a.addDir({'mode': '7', 'name':'[B][COLOR white]%s[/COLOR][/B]' %name,'url':url, 'iconimage':iconimage, 'content':'episodes', 'query':headers},{'sorttitle':title, 'season':season, 'episode':episode},fan_art, is_folder=False, item_count=items)
	if metaset=='true':
		setView('movies', 'MAIN')
	else: xbmc.executebuiltin('Container.SetViewMode(50)')
	addon.end_of_directory()

def GENRE(url, content):
	link = open_url(url).content
	match = re.compile('<input class="genre-ids" value="(.*?)" name=".*?"\n.*?type="checkbox" >(.*?)</label>').findall(link)
	for genre,name in match:
		name = name.replace(' ','')
		url = '%s/movie/filter/series/%s/%s/all/all/all/all' %(baseurl,sort_method,genre)
		i4a.addDir({'mode': '2', 'name':'[B][COLOR yellow]%s[/COLOR][/B]' %name, 'url':url, 'content':'tvshows'})
	if metaset=='true':
		setView('movies', 'MAIN')
	else: xbmc.executebuiltin('Container.SetViewMode(50)')
	addon.end_of_directory()

def YEAR(url, content):
	content = 'tvshows'
	ret_no = i4a.numeric_select('Enter Year', '2017')
	INDEX('%s/movie/filter/series/%s/all/all/%s/all/all' %(baseurl,sort_method,ret_no), content)
	if metaset=='true':
		setView('movies', 'MAIN')
	else: xbmc.executebuiltin('Container.SetViewMode(50)')
	addon.end_of_directory()

def SUPPORT():
	xbmcgui.Dialog().ok('[B][COLOR blue]GO [/COLOR][COLOR gold]MOVIES [/COLOR][/B]','Thanks for using GO SERIES. If you require support or want to report non working films or errors please contact me via the following ways >>> \nEMAIL: inside4ndroid.techsup@gmail.com \nTWITTER: @Inside_4ndroid \nThank You')
	return

def SEARCH(content, query):
        content = 'tvshows'
        try:
                if query:
                        search = query.replace(' ','+')
                else:
                        search = i4a.search()
                        if search == '':
                                i4a.notification('[COLOR gold][B]EMPTY QUERY[/B][/COLOR],Aborting search',icon)
                                return
                        else:
                                pass
                url = '%s/movie/search/%s' %(baseurl,search)
                INDEX(url,content)
        except:
                i4a.notification('[COLOR gold][B]Sorry No Results[/B][/COLOR]',icon)

def LINKS(url,name,iconimage,content,infolabels,query):

	split_head = re.split(r'\|', str(query), re.I)
	referer = split_head[0].replace('\\','')
	episode_id = split_head[1].replace('\\','')
	media_id = split_head[2].replace('\\','')

	time_now = int(time.time() * 10000)
	slug = '%s/ajax/movie_token' %baseurl
	params = {'eid':episode_id, 'mid':media_id, '_':time_now}
	headers = {'Accept':'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01','Accept-Encoding':'gzip, deflate, sdch, br', 'Accept-Language':'en-US,en;q=0.8','Referer':referer, 'User-Agent':i4a.User_Agent(), 'X-Requested-With':'XMLHttpRequest'}
        
	data = open_url(slug, params=params, headers=headers, verify=False).content
	xx = re.compile("_x='([^']+)'").findall(data)[0]
	xy = re.compile("_y='([^']+)'").findall(data)[0]
	request_url2 = '%s/ajax/movie_sources/%s' %(baseurl,episode_id)
	hash_params = {'x':xx, 'y':xy}
	headers = {'Accept':'application/json, text/javascript, */*; q=0.01','Accept-Encoding':'gzip, deflate, sdch, br', 'Accept-Language':'en-US,en;q=0.8','Referer':referer, 'User-Agent':i4a.User_Agent(), 'X-Requested-With':'XMLHttpRequest'}
	final = open_url(request_url2, params=hash_params, headers=headers, verify=False).json()

	res_quality = []
	stream_url = []
	quality = ''

	if auto_play == 'true':
		url = max(final['playlist'][0]['sources'], key=lambda lab: int(re.sub('\D', '', lab['label'])))
		url = url['file']
	else:
		match = final['playlist'][0]['sources']
		url = final['playlist'][0]['sources'][0]['file']
		
	url = url.replace('&amp;','&').replace('\/','/')
	liz = xbmcgui.ListItem('', iconImage=iconimage, thumbnailImage=iconimage)
	liz.setInfo(type='Video', infoLabels=infolabels)
	liz.setProperty("IsPlayable","true")
	liz.setPath(url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

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

def setView(content, viewType):
    ''' Why recode whats allready written and works well,
    Thanks go to Eldrado for it '''
    VT = '50'
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
        
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ( int(VT) ) )

    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )


mode = i4a.args['mode']
url = i4a.args.get('url', None)
name = i4a.args.get('name', None)
query = i4a.args.get('query', None)
title = i4a.args.get('title', None)
season = i4a.args.get('season', None)
episode = i4a.args.get('episode' ,None)
infolabels = i4a.args.get('infolabels', None)
content = i4a.args.get('content', None)
mode_id = i4a.args.get('mode_id', None)
iconimage = i4a.args.get('iconimage', None)
fan_art = i4a.args.get('fan_art', None)
is_folder = i4a.args.get('is_folder', True)



if mode is None or url is None or len(url)<1:
	MAIN()

elif mode == '2':
	INDEX(url,content)

elif mode == '3':
	EPIS(title, url, iconimage, content, season)

elif mode == '4':
	GENRE(url, content)

elif mode == '5':
	YEAR(url, content)

elif mode == '7':
	LINKS(url,name,iconimage,content,infolabels,query)

elif mode == 'search':
	SEARCH(content,query)

elif mode == 'addon_settings':
	addon.show_settings()

elif mode == 'addon_support':
	SUPPORT()

xbmcplugin.endOfDirectory(int(sys.argv[1]))

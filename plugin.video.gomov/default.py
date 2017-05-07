# -*- coding: utf-8 -*-

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,json,time
import base64,hashlib,random,string
from resources.lib.i4a_request import open_url
from resources.lib.common import Addon
from resources.lib.i4a_tools import i4a
import re,sys,urllib

# THIS ADDON IS A 123MOVIES REBUILD AND NOW RUNS FROM THE GOMOVIES WEBSITE BY INSIDE4NDROID 

# REMOVED TV SHOWS AND FIXED HOW THE MOVIES LOAD

#MUCKY DUCK IS THE ORIGINAL CODE CREATOR I JUST MODIFIED IT TO WORK SO MASSIVE THANKS AND CREDIT TO HIM.

#THE REASON I MADE THIS ADDON WORK AND IMPLEMENTED THE MODIFIED CODE BY ME WAS BECAUSE MUCKY DUCK HAS VANISHED AND I PERSONALLY LOVED 123MOVIES 

#INSIDE4NDROID 07:10AM 1/05/2017

addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon = Addon(addon_id, sys.argv)
addon_name = addon.get_name()
addon_path = addon.get_path()
i4a = i4a(addon_id, sys.argv)
auto_play = 'true'
metaset = addon.get_setting('enable_meta')
show_add_set = 'true'
art = i4a.get_art()
icon = addon.get_icon()
fanart = addon.get_fanart()
sort_method = xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE_IGNORE_THE)
baseurl = 'https://gomovies.to'
reload(sys)
sys.setdefaultencoding("utf-8")
content = 'movies'

def MAIN():
	filt = 'movie'
	filter_url = baseurl+'/movie/filter/%s/%s/all/all/all/all/all'
	i4a.addDir({'mode': 'search', 'name':'[B][COLOR yellow]Search[/COLOR][/B]', 'url':'url', 'content':'movies'})
	i4a.addDir({'mode': '2', 'name':'[B][COLOR yellow]Top Rated (by users)[/COLOR][/B]', 'url':filter_url %(filt,'rating'), 'content':'movies'})
	i4a.addDir({'mode': '2', 'name':'[B][COLOR yellow]Top Rated (imdb)[/COLOR][/B]', 'url':filter_url %(filt,'imdb_mark'), 'content':'movies'})
	i4a.addDir({'mode': '2', 'name':'[B][COLOR yellow]Most Viewed[/COLOR][/B]', 'url':filter_url %(filt,'view'), 'content':'movies'})
	i4a.addDir({'mode': '2', 'name':'[B][COLOR yellow]Recently Added[/COLOR][/B]', 'url':filter_url %(filt,'latest'), 'content':'movies'})
	i4a.addDir({'mode': '4', 'name':'[B][COLOR yellow]Genres[/COLOR][/B]', 'url':baseurl+'/movie/filter', 'content':'movies'})
	i4a.addDir({'mode': '5', 'name':'[B][COLOR yellow]Years[/COLOR][/B]', 'url':baseurl+'/movie/filter', 'content':'movies'})
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
		i4a.addDir({'mode': '7', 'name':'[B][COLOR white]%s[/COLOR][I][COLOR gold] (%s)[/COLOR][/I][/B]' %(name,qual),'url':url+'watching.html', 'iconimage':thumb, 'content':'movies'}, {'sorttitle':name},fan_art={'icon':thumb}, is_folder=False, item_count=items)
	try:
		nextp = re.compile('<li class="next"><a href="(.*?)" data-ci-pagination-page=".*?" rel="next">').findall(link)[0]
		i4a.addDir({'mode': '2', 'name':'[B][COLOR red]Next Page>>>[/COLOR][/B]', 'url':nextp, 'content':'movies'})
	except: pass
	if metaset=='true':
		setView('movies', 'MAIN')
	else: xbmc.executebuiltin('Container.SetViewMode(50)')
	addon.end_of_directory()

def GENRE(url, content):
	link = open_url(url).content
	match = re.compile('<input class="genre-ids" value="(.*?)" name=".*?"\n.*?type="checkbox" >(.*?)</label>').findall(link)
	for genre,name in match:
		name = name.replace(' ','')
		url = '%s/movie/filter/movie/%s/%s/all/all/all/all' %(baseurl,'latest',genre)
		i4a.addDir({'mode': '2', 'name':'[B][COLOR yellow]%s[/COLOR][/B]' %name, 'url':url, 'content':'movies'})
	if metaset=='true':
		setView('movies', 'MAIN')
	else: xbmc.executebuiltin('Container.SetViewMode(50)')
	addon.end_of_directory()

def YEAR(url, content):
        ret_no = i4a.numeric_select('Enter Year', '2017')
	if content == 'tvshows':
		INDEX('%s/movie/filter/series/%s/all/all/%s/all/all' %(baseurl,sort_method,ret_no), content)
	elif content == 'movies':
		INDEX('%s/movie/filter/movie/%s/all/all/%s/all/all' %(baseurl,sort_method,ret_no), content)
	if metaset=='true':
		setView('movies', 'MAIN')
	else: xbmc.executebuiltin('Container.SetViewMode(50)')
	addon.end_of_directory()

def SUPPORT():
	xbmcgui.Dialog().ok('[B][COLOR blue]GO [/COLOR][COLOR gold]MOVIES [/COLOR][/B]','Thanks for using GO MOVIES. If you require support or want to report non working films or errors please contact me via the following ways >>> \nEMAIL: inside4ndroid.techsup@gmail.com \nTWITTER: @Inside_4ndroid \nThank You')
	return


def COUNTRY(url, content):
        ret = i4a.dialog_select('Select Sort Method',sort)
        sort_method = sort_id[ret]
	link = open_url(url).content
	match=re.compile('<input class="country-ids" value="(.*?)" name=".*?"\n.*?type="checkbox" >(.*?)</label>').findall(link)
	for country,name in match:
		name = name.replace(' ','')
		if content == 'tvshows':
			url = '%s/movie/filter/series/%s/all/%s/all/all/all' %(baseurl,sort_method,country)
			i4a.addDir({'mode': '2', 'name':'[B][COLOR white]%s[/COLOR][/B]' %name, 'url':url, 'content':'movies'})
		elif content == 'movies':
			url = '%s/movie/filter/movie/%s/all/%s/all/all/all' %(baseurl,sort_method,country)
			i4a.addDir({'mode': '2', 'name':'[B][COLOR white]%s[/COLOR][/B]' %name, 'url':url, 'content':'movies'})
	if metaset=='true':
		setView('movies', 'MAIN')
	else: xbmc.executebuiltin('Container.SetViewMode(50)')
	addon.end_of_directory()




def SEARCH(content, query):
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




key = '87wwxtp3dqii'
key2 = '7bcq9826avrbi6m49vd7shxkn985mhod'

def LINKS(url,iconimage,content,infolabels,title):

	try:
		link = open_url(url).text
		referer = url
		video_id = re.compile('id: "(.*?)"').findall(link)[0]
		request_url =  baseurl + '/ajax/movie_episodes/'+video_id
		open  = open_url(request_url).text
		js = json.loads(open)
		js = js['html']
		server   = i4a.regex_from_to(js,'<strong>Server 10</strong>','></div>')
		eid      = i4a.regex_from_to(server,'id="ep-','"')
		url    = baseurl+'/ajax/movie_token?eid=%s&mid=%s&_=%s'%(eid,video_id,time.time())
		open   = open_url(url).text
		x      = i4a.regex_from_to(open,"x='","'")
		y      = i4a.regex_from_to(open,"y='","'")
		url    = baseurl+'/ajax/movie_sources/%s?x=%s&y=%s'%(eid,x,y)
	except:
		link = open_url(url).text
		referer = url
		video_id = re.compile('id: "(.*?)"').findall(link)[0]
		request_url =  baseurl + '/ajax/movie_episodes/'+video_id
		open  = open_url(request_url).text
		js = json.loads(open)
		js = js['html']
		server   = i4a.regex_from_to(js,'<strong>Server 8</strong>','></div>')
		eid      = i4a.regex_from_to(server,'id="ep-','"')
		url    = baseurl+'/ajax/movie_token?eid=%s&mid=%s&_=%s'%(eid,video_id,time.time())
		open   = open_url(url).text
		x      = i4a.regex_from_to(open,"x='","'")
		y      = i4a.regex_from_to(open,"y='","'")
		url    = baseurl+'/ajax/movie_sources/%s?x=%s&y=%s'%(eid,x,y)
						
	final  = open_url(url).text
	res_quality = []
	stream_url  = []
	quality     = ''

	if auto_play == 'true':
		url = i4a.regex_from_to(final,'file":"','"')
	else:
		if 'googlevideo' in final:
			match = i4a.regex_get_all(final,'file"','}')
			for a in match:
				quality = '[B][I][COLOR red]%s[/COLOR][/I][/B]' %i4a.regex_from_to(a,'label":"','"')
				url     =  i4a.regex_from_to(a,':"','"')
			if not '.srt' in url:
				res_quality.append(quality)
				stream_url.append(url)
			if len(match) >1:
				ret = i4a.dialog_select('Select Stream Quality',res_quality)
			if ret == -1:
				return
			elif ret > -1:
				url = stream_url[ret]
			else:
				url = i4a.regex_from_to(final,'file":"','"')
		else:
			url = i4a.regex_from_to(final,'file":"','"')
		
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

elif mode == '4':
	GENRE(url, content)

elif mode == '5':
	YEAR(url, content)

elif mode == '6':
	COUNTRY(url, content)

elif mode == '7':
	LINKS(url,iconimage,content,infolabels,title)

elif mode == 'search':
	SEARCH(content,query)

elif mode == 'addon_settings':
	addon.show_settings()

elif mode == 'addon_support':
	SUPPORT()

xbmcplugin.endOfDirectory(int(sys.argv[1]))

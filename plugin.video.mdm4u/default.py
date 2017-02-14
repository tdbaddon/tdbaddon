# -*- coding: utf-8 -*-


import xbmc,xbmcaddon,xbmcgui,xbmcplugin
from md_request import open_url
from md_view import setView
from common import Addon
from md_tools import md
import re,sys,urllib


#M4U Add-on Created By Mucky Duck (3/2016)


addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon = Addon(addon_id, sys.argv)
addon_name = addon.get_name()
addon_path = addon.get_path()
md = md(addon_id, sys.argv)

metaset = addon.get_setting('enable_meta')
show_tv = addon.get_setting('enable_shows')
show_mov = addon.get_setting('enable_movies')
show_fav = addon.get_setting('enable_favs')
show_add_set = addon.get_setting('add_set')
show_meta_set = addon.get_setting('enable_meta_set')

art = md.get_art()
icon = addon.get_icon()
fanart = addon.get_fanart()


baseurl = addon.get_setting('base_url')


reload(sys)
sys.setdefaultencoding("utf-8")




def MAIN():

	if show_tv == 'true':
		md.addDir({'mode': '2', 'name':'[COLOR white][B]TV[/B][/COLOR]', 'url':'url'})
	if show_mov == 'true':
		md.addDir({'mode': '1', 'name':'[COLOR white][B]MOVIES[/B][/COLOR]', 'url':'url'})
	if show_fav == 'true':
		md.addDir({'mode': 'fetch_favs', 'name':'[COLOR white][B]MY FAVOURITES[/B][/COLOR]', 'url':'url'})
	if metaset == 'true':
		if show_meta_set == 'true':
			md.addDir({'mode':'meta_settings', 'name':'[COLOR white][B]META SETTINGS[/B][/COLOR]', 'url':'url'}, is_folder=False, is_playable=False)
	if show_add_set == 'true':
		md.addDir({'mode':'addon_settings', 'name':'[COLOR white][B]ADDON SETTINGS[/B][/COLOR]', 'url':'url'}, is_folder=False, is_playable=False)
	

	setView(addon_id, 'files', 'menu-view')
	addon.end_of_directory()




def MOVIES():

	if show_fav == 'true':
		md.addDir({'mode': 'fetch_favs', 'name':'[COLOR white][B]MY FAVOURITES[/B][/COLOR]', 'url':'url'})
	md.addDir({'mode': '3', 'name':'[COLOR white][B]LATEST ADDED[/B][/COLOR]', 'url':baseurl+'/newadd', 'content':'movies'})
	md.addDir({'mode': '3', 'name':'[COLOR white][B]MOST VIEWED[/B][/COLOR]', 'url':baseurl+'/top-view', 'content':'movies'})
	md.addDir({'mode': '3', 'name':'[COLOR white][B]HOT MOVIES[/B][/COLOR]', 'url':baseurl, 'content':'movies'})
	md.addDir({'mode': 'search', 'name':'[COLOR white][B]SEARCH[/B][/COLOR]', 'url':'url', 'content':'movies'})
	md.addDir({'mode': '4', 'name':'[COLOR white][B]GENRE[/B][/COLOR]', 'url':baseurl, 'content':'movies'})
	md.addDir({'mode': '5', 'name':'[COLOR white][B]YEAR[/B][/COLOR]', 'url':baseurl, 'content':'movies'})
	
	setView(addon_id, 'files', 'menu-view')
	addon.end_of_directory()




def TV():

	if show_fav == 'true':
		md.addDir({'mode': 'fetch_favs', 'name':'[COLOR white][B]MY FAVOURITES[/B][/COLOR]', 'url':'url'})
	md.addDir({'mode': '3', 'name':'[COLOR white][B]LATEST ADDED[/B][/COLOR]', 'url':baseurl+'/latest-tvshow', 'content':'tvshows'})
	md.addDir({'mode': '3', 'name':'[COLOR white][B]MOST VIEWED[/B][/COLOR]', 'url':baseurl+'/top-view-tvshow', 'content':'tvshows'})
	md.addDir({'mode': 'search', 'name':'[COLOR white][B]SEARCH[/B][/COLOR]', 'url':baseurl, 'content':'tvshows'})
	md.addDir({'mode': '4', 'name':'[COLOR white][B]GENRE[/B][/COLOR]', 'url':baseurl+'/tvshow', 'content':'tvshows'})
	md.addDir({'mode': '3', 'name':'[COLOR white][B]ALL[/B][/COLOR]', 'url':baseurl+'/tvshow', 'content':'tvshows'})

	setView(addon_id, 'files', 'menu-view')
	addon.end_of_directory()




def INDEX(url,content):

	link = open_url(url).text
	all_videos = md.regex_get_all(link, '"item"', 'clear:both')
	items = len(all_videos)

	for a in all_videos:
		
		if content == 'movies':
			name = md.regex_from_to(a, 'cite>', '<')

		elif content == 'tvshows':
			name = md.regex_from_to(a, 'href=.*?>', '<')
			
		name = addon.unescape(name)
		name = name.encode('ascii', 'ignore').decode('ascii')
		qual = md.regex_from_to(a, 'class="h3-quality".*?>', '<')
		url = md.regex_from_to(a, 'href="', '"')
		thumb = md.regex_from_to(a, 'src=', 'alt=').replace(' ','')
		epi = md.regex_from_to(a, '"h4-cat".*?>', '<')
		fan_art = {'icon':thumb, 'fanart':art+'m4u.jpg'}
		if '-tvshow-' in url:
			md.addDir({'mode': '6', 'name':'[B][COLOR white]%s[/COLOR] [I][COLOR dodgerblue]%s[/COLOR][/I][/B]' %(name,epi), 'title':name,
				   'url':url, 'iconimage':thumb ,'content':'tvshows'}, {'sorttitle':name}, fan_art, item_count=items)
		else:
			md.addDir({'mode': '7', 'name':'[B][COLOR white]%s[/COLOR] [I][COLOR dodgerblue]%s[/COLOR][/I][/B]' %(name,qual),
				   'url':url, 'iconimage':thumb, 'content':'movies'}, {'sorttitle':name}, fan_art, is_folder=False, item_count=items)

	np_fan_art = {'icon':art+'next.png', 'fanart':art+'m4u.jpg'}
	try:
		fan_art = {'icon':thumb, 'fanart':art+'m4u.jpg'}
		np = re.compile("<a id='right' href='(.*?)'> <img src='next\.png' alt='.*?' width='50'></a>").findall(link)[0]
		md.addDir({'mode': '3', 'name':'[I][B][COLOR dodgerblue]Go To Next Page>>>[/COLOR][/B][/I]',
			   'url':np, 'content':content}, fan_art=np_fan_art)
	except:pass

	try:

		np = re.compile('<a class="btnpg btnpg-alt btnpg-flat waves-button waves-effect" href="(.*?)">(.*?)</a>.*?').findall(link)
		for url, name in np:
			md.addDir({'mode': '3', 'name':'[I][B][COLOR dodgerblue]Page %s >>>[/COLOR][/B][/I]' %name,
				   'url':url, 'content':content}, np_fan_art)
	except:pass

	if content == 'movies':
		setView(addon_id, 'movies', 'movie-view')
	elif content == 'tvshows':
		setView(addon_id, 'tvshows', 'show-view')
	addon.end_of_directory()




def EPIS(title,url,iconimage,content):
	
	if iconimage == None:
		iconimage = icon

	link = open_url(url).text

	match=re.compile('<a itemprop="target" href="(.*?)"><.*?class="episode".*?>(.*?)</button></a>').findall(link) 
	items = len(match)

	for url,name in match:

		data = name.split('-')
		season = data[0].replace('S','').replace('s','')
		episode = data[1].replace('E','').replace('e','')
		
		try:
			episode = episode.split(',')[0]
		except:
			pass

		fan_art = {'icon':iconimage, 'fanart':art+'m4u.jpg'}

		md.addDir({'mode': '7', 'name':'[I][B][COLOR dodgerblue]%s[/COLOR][/B][/I]' %name,
			   'url':url, 'iconimage':iconimage, 'content':'episodes'},
			  {'sorttitle':title, 'season':season, 'episode':episode},
			  fan_art, is_folder=False, item_count=items)

	setView(addon_id,'episodes', 'epi-view')
	addon.end_of_directory()




def GENRE(url,content):

	link = open_url(url).text
	if content == 'movies':
		match=re.compile('<li> <a href="(.*?)" title="All movies.*?">(.*?)</a></li>').findall(link) 
		for url,name in match:
			if '/movie-' in url:
				md.addDir({'mode': '3', 'name':'[B][COLOR white]%s[/COLOR][/B]' %name, 'url':url,
					   'content':'movies'})
				

	elif content == 'tvshows':
		match=re.compile('<li> <a href="(.*?)" title="All TVshow.*?">(.*?)</a></li>').findall(link)
		for url,name in match:
			if '/tvshow-' in url:
				md.addDir({'mode': '3', 'name':'[B][COLOR white]%s[/COLOR][/B]' %name, 'url':url,
					   'content':'tvshows'})

	setView(addon_id, 'files', 'menu-view')
	addon.end_of_directory()




def YEAR(url,content):

	link = open_url(url).text
	match=re.compile('<li> <a href="(.*?)" title="All movies.*?">(.*?)</a></li>').findall(link) 

	for url,name in match:
		if '/year-' in url:
			md.addDir({'mode': '3', 'name':'[B][COLOR white]%s[/COLOR][/B]' %name, 'url':url,
					   'content':'movies'})

	setView(addon_id, 'files', 'menu-view')
	addon.end_of_directory()




def SEARCH(content, query):
	try:
		if query:
			search = query.replace(' ','-')
		else:
			search = md.search('-')
			if search == '':
				md.notification('[COLOR gold][B]EMPTY QUERY[/B][/COLOR],Aborting search',icon)
				return
			else:
				pass

		if content == 'movies':
			url = '%s/tag/%s' %(baseurl,search)
		elif content == 'tvshows':
			url = '%s/tagtvs/%s' %(baseurl,search)
		INDEX(url,content)

	except:
		md.notification('[COLOR gold][B]Sorry No Results[/B][/COLOR]',icon)




def RESOLVE(url,name,content,fan_art,infolabels):

        link = open_url(url).content

	if content == 'movies':
                request_url = re.findall(r'<a  href="([^"]+)">Watch <b>', str(link), re.I|re.DOTALL)[0]
		link = open_url(request_url).content
		
	value = []
	max_url = []
	final_url= ''

	match = re.findall(r'"file":"([^"]+)".*?"label":"([^"]+)"', str(link), re.I|re.DOTALL)
	for url,label in match:
		value.append(int(re.sub('\D', '', label)))
		max_url.append(url)

	try:
		final_url =  max_url[md.get_max_value_index(value)[0]]
	except:
		pass

	if not final_url:
		request_url = '%s/demo.php' %baseurl
		try:
			params = {'v':re.findall(r'link="([^"]+)".*?>Server 0</span>', str(link), re.I|re.DOTALL)[0]}
		except:
			try:
				params = {'v':re.findall(r'link="([^"]+)" >Server 1</span>', str(link), re.I|re.DOTALL)[0]}
			except:
				params = {'v':re.findall(r'link="([^"]+)" >Server 2</span>', str(link), re.I|re.DOTALL)[0]}
		
		link2 = open_url(request_url, params=params).content

		try:
			final_url = re.findall(r'source.*?src="([^"]+)"', str(link2), re.I|re.DOTALL)[0]
		except:
			match = re.findall(r'"file":"([^"]+)".*?"label":"([^"]+)"', str(link2), re.I|re.DOTALL)
			for url,label in match:
				value.append(int(re.sub('\D', '', label)))
				max_url.append(url)

			try:
				final_url =  max_url[md.get_max_value_index(value)[0]]
			except:
				pass

	if 'google' in final_url:
		final_url = final_url
	else:
		if baseurl not in final_url:
			final_url = '%s/%s' %(baseurl,final_url)

	final_url = final_url.replace('../view.php?','view.php?')
	final_url = final_url.replace('./view.php?','view.php?')
		
	md.resolved(final_url, name, fan_art, infolabels)
	addon.end_of_directory()




mode = md.args['mode']
url = md.args.get('url', None)
name = md.args.get('name', None)
query = md.args.get('query', None)
title = md.args.get('title', None)
season = md.args.get('season', None)
episode = md.args.get('episode' ,None)
infolabels = md.args.get('infolabel', None)
content = md.args.get('content', None)
mode_id = md.args.get('mode_id', None)
iconimage = md.args.get('iconimage', None)
fan_art = md.args.get('fan_art', None)
is_folder = md.args.get('is_folder', True)




if mode is None or url is None or len(url)<1:
	MAIN()

elif mode == '1':
	MOVIES()

elif mode == '2':
	TV()

elif mode == '3':
	INDEX(url,content)

elif mode == '4':
	GENRE(url,content)

elif mode == '5':
	YEAR(url,content)

elif mode == '6':
	EPIS(title,url,iconimage,content)

elif mode == '7':
	RESOLVE(url,name,content,fan_art,infolabels)

elif mode == 'search':
	SEARCH(content,query)

elif mode == 'addon_search':
	md.addon_search(content,query,fan_art,infolabels)

elif mode == 'add_remove_fav':
	md.add_remove_fav(name, url, infolabels, fan_art,
			  content, mode_id, is_folder)
elif mode == 'fetch_favs':
	md.fetch_favs(baseurl)

elif mode == 'addon_settings':
	addon.show_settings()

elif mode == 'meta_settings':
	import metahandler
	metahandler.display_settings()

md.check_source()
addon.end_of_directory()

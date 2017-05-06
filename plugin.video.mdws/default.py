# -*- coding: utf-8 -*-


import xbmc,xbmcaddon,xbmcgui,xbmcplugin
import itertools,re,sys,urlresolver
from md_request import open_url
from md_view import setView
from common import Addon
from md_tools import md


#Watchseries - By Mucky Duck (03/2015)


addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon = Addon(addon_id, sys.argv)
addon_name = addon.get_name()
addon_path = addon.get_path()
md = md(addon_id, sys.argv)


metaset = addon.get_setting('enable_meta')
show_fav = addon.get_setting('enable_favs')
show_add_set = addon.get_setting('add_set')
show_meta_set = addon.get_setting('enable_meta_set')
show_resolver_set = addon.get_setting('enable_resolver_set')


art = md.get_art()
icon = addon.get_icon()
fanart = addon.get_fanart()


baseurl =  addon.get_setting('base_url') #original source 'http://watchseries.vc'


reload(sys)
sys.setdefaultencoding("utf-8")


def MAIN():

	md.addDir({'mode':'4', 'name':'[B][COLOR yellow]A-Z[/COLOR][/B]', 'url':baseurl+'/letters/A'}, fan_art={'icon':art+'mdws.png'})
	md.addDir({'mode':'search', 'name':'[B][COLOR yellow]Search[/COLOR][/B]', 'url':'url'}, fan_art={'icon':art+'mdws.png'})
	md.addDir({'mode':'6', 'name':'[B][COLOR yellow]TV Schedule[/COLOR][/B]', 'url':baseurl+'/tvschedule'}, fan_art={'icon':art+'mdws.png'})
	if show_fav == 'true':
		md.addDir({'mode': 'fetch_favs', 'name':'[COLOR yellow][B]My Favourites[/B][/COLOR]', 'url':'url'})
	md.addDir({'mode':'7', 'name':'[B][COLOR yellow]TV Shows Years[/COLOR][/B]', 'url':baseurl+'/years/2017'}, fan_art={'icon':art+'mdws.png'})
	md.addDir({'mode':'5', 'name':'[B][COLOR yellow]TV Shows Genres[/COLOR][/B]', 'url':baseurl+'/genres/action'}, fan_art={'icon':art+'mdws.png'})
	md.addDir({'mode':'1', 'name':'[B][COLOR yellow]Newest Episodes Added[/COLOR][/B]', 'url':baseurl+'/latest', 'content':'episodes'}, fan_art={'icon':art+'mdws.png'})
	md.addDir({'mode':'1', 'name':'[B][COLOR yellow]This Week\'s Popular Episodes[/COLOR][/B]', 'url':baseurl+'/new', 'content':'episodes'}, fan_art={'icon':art+'mdws.png'})
	if show_resolver_set == 'true':
		md.addDir({'mode':'urlresolver_settings', 'name':'[COLOR yellow][B]UrlResolver Settings[/B][/COLOR]', 'url':'url'}, is_folder=False, is_playable=False)
        if show_add_set == 'true':
		md.addDir({'mode':'addon_settings', 'name':'[COLOR yellow][B]Add-on Settings[/B][/COLOR]', 'url':'url'}, is_folder=False, is_playable=False)
	if metaset == 'true':
		if show_meta_set == 'true':
			md.addDir({'mode':'meta_settings', 'name':'[COLOR yellow][B]Meta Settings[/B][/COLOR]', 'url':'url'}, is_folder=False, is_playable=False)
	setView(addon_id, 'files', 'menu-view')
	addon.end_of_directory()




def INDEX(url,title,mode_id,content):

	link = open_url(url).content

	if mode_id == '6':
		link = md.regex_get_all(link, title, '<ul class="tabs">')

	all_links = md.regex_get_all(str(link), '"listings">', '</ul>')
	all_videos = md.regex_get_all(str(all_links), '<li', '</li')
	items = len(all_videos) 

	for a in all_videos:

		name = md.regex_from_to(a, 'title="', '"').replace("\\'","'")
		name = addon.unescape(name)
		url = md.regex_from_to(a, 'href="', '"')
		thumb = md.regex_from_to(a, 'src="', '"')

                if not thumb:
                        thumb = art+'mdws.png'

		if baseurl not in url:
			url = baseurl + url

		if content == 'episodes':

			info = name.split('- Season')
			title = info[0].strip()
			
			try:
                                sep = md.regex_from_to(a, '<br/>', '<br/>')
                                episode = sep.split('Episode')[1]
                                season = sep.split('Episode')[0]

                        except:
                                season = info[1].split('Episode')[0]
                                episode = info[1].split('Episode')[1].split('-')[0]

                        md.remove_punctuation(title)

                        md.addDir({'mode':'8','name':'[B][COLOR white]%s[/COLOR][COLOR yellow][I] - Season %s[/I][/COLOR][/B]' %(title,info[1]),
				   'url':url, 'content':content, 'title':title, 'season':season, 'iconimage':thumb,
                                   'episode':episode}, {'sorttitle':title, 'season':season, 'episode':episode},
                                  fan_art={'icon':thumb}, item_count=items)

		else:
			if mode_id == '4':
				infolabels = {}
			else:
				infolabels = {'sorttitle':name}

			md.remove_punctuation(name)

			md.addDir({'mode':'2', 'name':'[B][COLOR white]%s[/COLOR][/B]' %name, 'url':url,
				   'title':title, 'iconimage':thumb, 'content':content},
				  infolabels, fan_art={'icon':thumb}, item_count=items)

	try:

                np = re.compile('<li ><a href="([^"]+)">Next Page</a></li>').findall(link)[0]
                md.addDir({'mode':'1','name':'[COLOR yellow][B][I]>>Next Page>>>[/I][/B][/COLOR]', 'url':np,
			   'title':title, 'content':content, 'mode_id':mode_id}, fan_art={'icon':art+'mdws.png'})

        except:pass

	if content == 'tvshows':
		setView(addon_id, 'tvshows', 'show-view')
	elif content == 'episodes':
		setView(addon_id,'episodes', 'epi-view')
	addon.end_of_directory()




def SEASONS(url,title):

	link = open_url(url).content
	match = re.compile('<a href="([^"]+)" itemprop="url"><span itemprop="name">([^<>]*)</span>').findall(link)
	items = len(match)

	try:
		thumb = re.compile('<meta property="og:image" content="([^"]+)" />').findall(link)[0]
	except:
		thumb = art+'mdws.png'

	try:
		year = re.compile('href=.*?/years/.*?>([^<>]*)</a></span>').findall(link)[0]
	except:
		year = ''

	md.remove_punctuation(title)

	for url,name in match:
		md.addDir({'mode':'3','name':'[COLOR yellow][B][I]%s[/I][/B][/COLOR]' %name, 'url':url,
			   'title':title, 'iconimage':thumb, 'content':'tvshows', 'season':name},
			  {'sorttitle':title, 'year':year}, fan_art={'icon':thumb}, item_count=items)

	setView(addon_id, 'tvshows', 'show-view')
	addon.end_of_directory()




def EPISODES(url,iconimage,title,season,infolabels):

	if iconimage is None:
		fan_art = {'icon':art+'mdws.png'}
	else:
		fan_art = {'icon':iconimage}

	try:
		code = re.compile("'imdb_id': u'([^']+)'").findall(infolabels)[0]
	except:
		code = ''

	link = open_url(url).content
	all_videos = md.regex_get_all(link, '<li id="episode_', '</li>')
	items = len(all_videos)

	for a in all_videos:

		name = md.regex_from_to(a, '"name">', '<')
		name = addon.unescape(name)
		date = md.regex_from_to(a, '"datepublished">', '<')
		links = md.regex_from_to(a, '<b>', '<')
		url = md.regex_from_to(a, 'href="', '"')
		episode = name.split('&')[0]
		name = name.replace("&amp;","&").replace('&nbsp;',' ')
		
		md.addDir({'mode':'8', 'name':'[B][COLOR white]%s[/COLOR][/B][B][I][COLOR yellow]%s%s[/COLOR][/I][/B]' %(name,links,date),
			   'url':url, 'iconimage':iconimage, 'content':'episodes'},
			  {'sorttitle':title, 'code':code, 'season':season, 'episode':episode},
			  fan_art, item_count=items)

	setView(addon_id,'episodes', 'epi-view')
	addon.end_of_directory()




def ATOZ(url):

	link = open_url(url).content
	all_links = md.regex_get_all(link, '"pagination">', '</ul>')
	all_videos = md.regex_get_all(str(all_links), '<li', '</li')
	items = len(all_videos) 

	for a in all_videos:

		name = md.regex_from_to(a, 'href=.*?>', '<')
		url = md.regex_from_to(a, 'href="', '"')

		if baseurl not in url:
			url = baseurl + url

		if 'NEW' not in name:
			md.addDir({'mode':'1','name':'[COLOR yellow][B][I]%s[/I][/B][/COLOR]' %name,
				   'url':url, 'mode_id':'4', 'content':'tvshows'},
				  fan_art={'icon':art+'mdws.png'}, item_count=items)

	setView(addon_id, 'files', 'menu-view')
	addon.end_of_directory()




def GENRES(url):

	link = open_url(url).content
	all_links = md.regex_get_all(link, '"pagination" style', '</ul>')
	all_videos = md.regex_get_all(str(all_links), '<li', '</li')
	items = len(all_videos) 

	for a in all_videos:

		name = md.regex_from_to(a, 'href=.*?>', '<')
		url = md.regex_from_to(a, 'href="', '"')
		url = url + '/1/0/0'

		if baseurl not in url:
			url = baseurl + url

		md.addDir({'mode':'1','name':'[COLOR yellow][B][I]%s[/I][/B][/COLOR]' %name,
                           'url':url, 'content':'tvshows'}, fan_art={'icon':art+'mdws.png'}, item_count=items)

	setView(addon_id, 'files', 'menu-view')
	addon.end_of_directory()




def YEARS(url):

        year = []
        year_url = []

        link = open_url(url).content
	all_links = md.regex_get_all(link, '"pagination" style', '</ul>')
	all_videos = md.regex_get_all(str(all_links), '<li', '</li')
        
	for a in all_videos:

		name = md.regex_from_to(a, 'href=.*?>', '<')
		url = md.regex_from_to(a, 'href="', '"')

		if baseurl not in url:
			url = baseurl + url

		year.append(name)
		year_url.append(url)

	match = re.compile('value="([^"]+)".*?>([^<>]*)</option>').findall(link)
	for url2,name2 in match:
                if '/years/' in url2:
                        year.append(name2)
                        year_url.append(url2)
                
        items = len(year)

        for final_name,final_url in itertools.izip_longest(year,year_url):
                md.addDir({'mode':'1','name':'[COLOR yellow][B][I]%s[/I][/B][/COLOR]' %final_name,
                           'url':final_url, 'content':'tvshows'}, fan_art={'icon':art+'mdws.png'}, item_count=items)

	setView(addon_id, 'files', 'menu-view')
	addon.end_of_directory()




def SCHEDULE(url):

	link = open_url(url).content
	match = re.compile('<div style="width: 153px;">([^<>]*)<').findall(link)
	items = len(match)
	for name in match:
		md.addDir({'mode':'1','name':'[COLOR yellow][B][I]%s[/I][/B][/COLOR]' %name,
			   'url':url, 'mode_id':'6', 'content':'episodes', 'title':name},
			  fan_art={'icon':art+'mdws.png'}, item_count=items)

	setView(addon_id, 'files', 'menu-view')
	addon.end_of_directory()




def SEARCH(content, query):

        if content is None:
                content = 'tvshows'
	try:

		if query:
			search = query.replace(' ', '%20')
		else:
			search = md.search('%20')
			if search == '':
				md.notification('[COLOR gold][B]EMPTY QUERY[/B][/COLOR],Aborting search',icon)
				return
			else:
				pass

		url = '%s/search/%s' %(baseurl,search)
                link = open_url(url).content
                all_videos = md.regex_get_all(link, 'ih-item', 'Add Link')
                items = len(all_videos) 

                for a in all_videos:

                        name = md.regex_from_to(a, '<strong>', '</').replace("\\'","'")
                        name = addon.unescape(name)
                        url = md.regex_get_all(a, 'href="', '"', excluding=True)[2]
                        thumb = md.regex_from_to(a, 'src="', '"')

                        if not thumb:
                                thumb = art+'mdws.png'

                        if baseurl not in url:
                                url = baseurl + url

                        md.remove_punctuation(name)

                        md.addDir({'mode':'2', 'name':'[B][COLOR white]%s[/COLOR][/B]' %name, 'url':url,
                                   'title':name, 'iconimage':thumb, 'content':content},
                                  {'sorttitle':name}, fan_art={'icon':thumb}, item_count=items)

                setView(addon_id, 'tvshows', 'show-view')
                addon.end_of_directory()

        except:
		md.notification('[COLOR gold][B]Sorry No Results[/B][/COLOR]',icon)

        

		



def FILEHOSTS(url,iconimage,title,season,episode,infolabels):
	
	if iconimage is None or iconimage == '':
		fanart = {'icon':art+'mdws.png'}
	else:
		fanart = {'icon':iconimage}
		
	link = open_url(url).content
	match = re.compile('cale\.html\?r=(.*?)" class="buttonlink" title="([^"]+)"').findall(link)
	items = len(match)
	for url,name in match:
		url = url.decode('base64')
		if urlresolver.HostedMediaFile(url):
			md.addDir({'mode':'9','name':'[COLOR yellow][B][I]%s[/I][/B][/COLOR]' %name, 'url':url},
				  fan_art=fanart, is_folder=False, item_count=items)

	setView(addon_id, 'files', 'menu-view')
	addon.end_of_directory()




def RESOLVE(url,name,fan_art,infolabels):

	try:

		final_url = urlresolver.resolve(url)
		md.resolved(final_url, name, fan_art, infolabels)

	except:

		md.notification('[COLOR gold][B]SORRY LINK DOWN PLEASE TRY ANOTHER ONE[/B][/COLOR]', icon)

	addon.end_of_directory()




mode = md.args['mode']
url = md.args.get('url', None)
name = md.args.get('name', None)
query = md.args.get('query', None)
title = md.args.get('title', None)
year = md.args.get('year', None)
season = md.args.get('season', None)
episode = md.args.get('episode' ,None)
infolabels = md.args.get('infolabels', None)
content = md.args.get('content', None)
mode_id = md.args.get('mode_id', None)
iconimage = md.args.get('iconimage', None)
fan_art = md.args.get('fan_art', None)
is_folder = md.args.get('is_folder', True)




if mode is None or url is None or len(url)<1:
	MAIN()
       
elif mode == '1':
	INDEX(url,title,mode_id,content)

elif mode == '2':
	SEASONS(url,title)

elif mode == '3':
	EPISODES(url,iconimage,title,season,infolabels)

elif mode == '4':
	ATOZ(url)

elif mode == '5':
	GENRES(url)

elif mode == '6':
	SCHEDULE(url)

elif mode == '7':
	YEARS(url)

elif mode == '8':
	FILEHOSTS(url,iconimage,title,season,episode,infolabels)

elif mode == '9':
	RESOLVE(url,name,fan_art,infolabels)

elif mode == 'search':
	SEARCH(content, query)

elif mode == 'addon_search':
	md.addon_search(content,query,fan_art,infolabels)

elif mode == 'add_remove_fav':
	md.add_remove_fav(name,url,infolabels,fan_art,
			  content,mode_id,is_folder)
elif mode == 'fetch_favs':
	md.fetch_favs(baseurl)

elif mode == 'addon_settings':
	addon.show_settings()

elif mode == 'meta_settings':
	import metahandler
	metahandler.display_settings()

elif mode == 'urlresolver_settings':
	urlresolver.display_settings()

addon.end_of_directory()

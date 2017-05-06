# -*- coding: utf-8 -*-

import xbmc,xbmcaddon,xbmcgui,xbmcplugin
from md_request import open_url
from md_view import setView
from common import Addon
from md_tools import md
import re,sys,time,urllib


#123Movies By Mucky Duck (12/2015)


addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon = Addon(addon_id, sys.argv)
addon_name = addon.get_name()
addon_path = addon.get_path()
md = md(addon_id, sys.argv)

auto_play = addon.get_setting('autoplay')
metaset = addon.get_setting('enable_meta')
show_tv = addon.get_setting('enable_shows')
show_mov = addon.get_setting('enable_movies')
show_fav = addon.get_setting('enable_favs')
show_proxy = addon.get_setting('enable_proxy')
show_add_set = addon.get_setting('add_set')
show_meta_set = addon.get_setting('enable_meta_set')

art = md.get_art()
icon = addon.get_icon()
fanart = addon.get_fanart()


baseurl = addon.get_setting('base_url')


reload(sys)
sys.setdefaultencoding("utf-8")


sort_id = ['rating','latest','view','favorite','imdb_mark']
sort = ['[B][I][COLOR red]Most Rated[/COLOR][/I][/B]', '[B][I][COLOR red]Recently Added[/COLOR][/I][/B]',
	'[B][I][COLOR red]Most Viewed[/COLOR][/I][/B]', '[B][I][COLOR red]Most Favourited[/COLOR][/I][/B]',
	'[B][I][COLOR red]IMDB Rating[/COLOR][/I][/B]']




def MAIN():

	if show_mov == 'true':
		md.addDir({'mode': '1', 'name':'[COLOR white][B]MOVIES[/B][/COLOR]', 'url':'url', 'content':'movies'})
	if show_tv == 'true':
		md.addDir({'mode': '1', 'name':'[COLOR white][B]TV SHOWS[/B][/COLOR]', 'url':'url', 'content':'tvshows'})
	if show_fav == 'true':
		md.addDir({'mode': 'fetch_favs', 'name':'[COLOR white][B]MY FAVOURITES[/B][/COLOR]', 'url':'url'})
	if metaset == 'true':
                if show_meta_set == 'true':
                        md.addDir({'mode':'meta_settings', 'name':'[COLOR white][B]META SETTINGS[/B][/COLOR]', 'url':'url'}, is_folder=False, is_playable=False)
	if show_add_set == 'true':
		md.addDir({'mode':'addon_settings', 'name':'[COLOR white][B]ADDON SETTINGS[/B][/COLOR]', 'url':'url'}, is_folder=False, is_playable=False)
	#if show_proxy == 'true':
		#md.addDir({'mode': 'get_proxy', 'name':'[COLOR white][B]GET PROXY ADDRESS[/B][/COLOR]', 'url':'http://123movies-proxy.com'}, is_folder=False, is_playable=False)
	

	setView(addon_id, 'files', 'menu-view')
	addon.end_of_directory()




def CATS(content):

	if show_fav == 'true':
		md.addDir({'mode': 'fetch_favs', 'name':'[COLOR white][B]MY ADD-ON FAVOURITES[/B][/COLOR]', 'url':'url'})
		
	if content == 'movies':
		filt = 'movie'

	elif content == 'tvshows':
		filt = 'series'

	filter_url = baseurl+'/movie/filter/%s/%s/all/all/all/all/all'

	md.addDir({'mode': '2', 'name':'[B][COLOR white]MOST RECENTLY ADDED[/COLOR][/B]', 'url':filter_url %(filt,'latest'), 'content':content})
	md.addDir({'mode': '2', 'name':'[B][COLOR white]MOST FAVOURITED[/COLOR][/B]', 'url':filter_url %(filt,'favorite'), 'content':content})
	md.addDir({'mode': '2', 'name':'[B][COLOR white]MOST RATINGS[/COLOR][/B]', 'url':filter_url %(filt,'rating'), 'content':content})
	md.addDir({'mode': '2', 'name':'[B][COLOR white]MOST VIEWED[/COLOR][/B]', 'url':filter_url %(filt,'view'), 'content':content})
	md.addDir({'mode': '2', 'name':'[B][COLOR white]TOP IMDB[/COLOR][/B]', 'url':filter_url %(filt,'imdb_mark'), 'content':content})
	md.addDir({'mode': '6', 'name':'[B][COLOR white]COUNTRY[/COLOR][/B]', 'url':baseurl+'/movie/filter', 'content':content})
	md.addDir({'mode': 'search', 'name':'[B][COLOR white]SEARCH[/COLOR][/B]', 'url':'url', 'content':content})
	md.addDir({'mode': '4', 'name':'[B][COLOR white]GENRE[/COLOR][/B]', 'url':baseurl+'/movie/filter', 'content':content})
	md.addDir({'mode': '5', 'name':'[B][COLOR white]YEAR[/COLOR][/B]', 'url':baseurl+'/movie/filter', 'content':content})

	setView(addon_id, 'files', 'menu-view')
        addon.end_of_directory()




def INDEX(url,content):

	link = open_url(url,verify=False).content
	all_videos = md.regex_get_all(link, 'class="ml-item">', '</h2></span>')
	items = len(all_videos)

	for a in all_videos:

		name = md.regex_from_to(a, 'title="', '"')
		url = md.regex_from_to(a, 'href="', '"')
		thumb = md.regex_from_to(a, 'original="', '"')
		qual = md.regex_from_to(a, 'mli-quality">', '<')
		eps = md.regex_from_to(a, '"mli-eps">', '</')
		eps = eps.replace('<span>',' ').replace('<i>',' ')

		if content == 'movies':
                        if qual:
                                md.addDir({'mode': '7', 'name':'[B][COLOR white]%s[/COLOR][I][COLOR red](%s)[/COLOR][/I][/B]' %(name,qual),
                                           'url':url+'watching.html', 'iconimage':thumb, 'content':content}, {'sorttitle':name},
                                          fan_art={'icon':thumb}, is_folder=False, item_count=items)

		elif content == 'tvshows':
                        if eps:
                                data = name.split('- Season')
                                sorttitle = data[0].strip()
                                try:
                                        season = data[1].strip()
                                except:
                                        season = ''
                                md.addDir({'mode': '3', 'name':'[B][COLOR white]%s[/COLOR] [I][COLOR red]%s[/COLOR][/I][/B]' %(name,eps),
                                           'title':sorttitle, 'url':url+'watching.html', 'iconimage':thumb, 'content':content, 'season':season},
                                          {'sorttitle':sorttitle}, fan_art={'icon':thumb}, item_count=items)

	try:
		nextp = re.compile('<li class="next"><a href="(.*?)" data-ci-pagination-page=".*?" rel="next">').findall(link)[0]
		md.addDir({'mode': '2', 'name':'[B][COLOR red]Next Page>>>[/COLOR][/B]', 'url':nextp, 'content':content})
	except: pass

	if content == 'movies':
		setView(addon_id, 'movies', 'movie-view')
	elif content == 'tvshows':
		setView(addon_id, 'tvshows', 'show-view')
	addon.end_of_directory()




def EPIS(title, url, iconimage, content, season):

        link = open_url(url,verify=False).content
	referer = url
	media_id = re.compile('id: "([^"]+)"').findall(link)[0]
	request_url = '%s/ajax/movie_episodes/%s' %(baseurl,media_id)
        headers = {'Accept-Encoding':'gzip, deflate, sdch, br', 'Referer':referer, 'User-Agent':md.User_Agent()}
        link2 = open_url(request_url, headers=headers, verify=False).json()
        all_links = md.regex_get_all(link2['html'], '>Server 10<', '"clearfix"')
	all_videos = md.regex_get_all(str(all_links), '<a', '</a>')
	items = len(all_videos)

	for a in all_videos:

		name = md.regex_from_to(a, 'title="', '"')
		episode_id = md.regex_from_to(a, 'data-id="', '"')

		headers = referer + '\|' + episode_id + '\|' + media_id
		url =  '%s/ajax/movie_sources/%s' %(baseurl,episode_id)

		try:
                        episode = name.split('Episode')[1].strip()[:2]
                except:pass
                
		fan_art = {'icon':iconimage}

                md.addDir({'mode': '7', 'name':'[B][COLOR white]%s[/COLOR][/B]' %name,
                           'url':url, 'iconimage':iconimage, 'content':'episodes', 'query':headers},
                          {'sorttitle':title, 'season':season, 'episode':episode},
                          fan_art, is_folder=False, item_count=items)

	setView(addon_id,'episodes', 'epi-view')
        addon.end_of_directory()




def GENRE(url, content):

        ret = md.dialog_select('Select Sort Method',sort)
        sort_method = sort_id[ret]
	link = open_url(url,verify=False).content
	match = re.compile('<input class="genre-ids" value="(.*?)" name=".*?"\n.*?type="checkbox" >(.*?)</label>').findall(link)
	for genre,name in match:
		name = name.replace(' ','')
		if content == 'tvshows':
			url = '%s/movie/filter/series/%s/%s/all/all/all/all' %(baseurl,sort_method,genre)
			md.addDir({'mode': '2', 'name':'[B][COLOR white]%s[/COLOR][/B]' %name, 'url':url, 'content':content})
		elif content == 'movies':
			url = '%s/movie/filter/movie/%s/%s/all/all/all/all' %(baseurl,sort_method,genre)
			md.addDir({'mode': '2', 'name':'[B][COLOR white]%s[/COLOR][/B]' %name, 'url':url, 'content':content})

	setView(addon_id, 'files', 'menu-view')
	addon.end_of_directory()




def YEAR(url, content):

        ret = md.dialog_select('Select Sort Method',sort)
        sort_method = sort_id[ret]
        ret_no = md.numeric_select('Enter Year', '2017')

	if content == 'tvshows':
		INDEX('%s/movie/filter/series/%s/all/all/%s/all/all' %(baseurl,sort_method,ret_no), content)
	elif content == 'movies':
		INDEX('%s/movie/filter/movie/%s/all/all/%s/all/all' %(baseurl,sort_method,ret_no), content)

	setView(addon_id, 'files', 'menu-view')
	addon.end_of_directory()




def COUNTRY(url, content):

        ret = md.dialog_select('Select Sort Method',sort)
        sort_method = sort_id[ret]
	link = open_url(url,verify=False).content

	match=re.compile('<input class="country-ids" value="(.*?)" name=".*?"\n.*?type="checkbox" >(.*?)</label>').findall(link)
	for country,name in match:
		name = name.replace(' ','')
		if content == 'tvshows':
			url = '%s/movie/filter/series/%s/all/%s/all/all/all' %(baseurl,sort_method,country)
			md.addDir({'mode': '2', 'name':'[B][COLOR white]%s[/COLOR][/B]' %name, 'url':url, 'content':content})
		elif content == 'movies':
			url = '%s/movie/filter/movie/%s/all/%s/all/all/all' %(baseurl,sort_method,country)
			md.addDir({'mode': '2', 'name':'[B][COLOR white]%s[/COLOR][/B]' %name, 'url':url, 'content':content})


	setView(addon_id, 'files', 'menu-view')
	addon.end_of_directory()




def SEARCH(content, query):
        try:
                if query:
                        search = query.replace(' ','+')
                else:
                        search = md.search()
                        if search == '':
                                md.notification('[COLOR gold][B]EMPTY QUERY[/B][/COLOR],Aborting search',icon)
                                return
                        else:
                                pass
                url = '%s/movie/search/%s' %(baseurl,search)
                INDEX(url,content)
        except:
                md.notification('[COLOR gold][B]Sorry No Results[/B][/COLOR]',icon)




def LINKS(url,name,iconimage,content,infolabels,query):

	if content == 'movies':

                link = open_url(url,verify=False).content
                referer = url

                headers = {'User-Agent':md.User_Agent()}
                link = open_url(url, headers=headers).content
                media_id = re.compile('id: "([^"]+)"').findall(link)[0]

                request_url = '%s/ajax/movie_episodes/%s' %(baseurl,media_id)
                headers = {'Accept-Encoding':'gzip, deflate, sdch, br', 'Referer':referer, 'User-Agent':md.User_Agent()}
                link2 = open_url(request_url, headers=headers, verify=False).json()
                episode_id = re.compile('data-id="([^"]+)"').findall(link2['html'])[1]

        else:
                split_head = re.split(r'\|', str(query), re.I)
                referer = split_head[0].replace('\\','')
                episode_id = split_head[1].replace('\\','')
                media_id = split_head[2].replace('\\','')

        time_now = int(time.time() * 10000)
        slug = '%s/ajax/movie_token' %baseurl
        params = {'eid':episode_id, 'mid':media_id, '_':time_now}
        headers = {'Accept':'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
                   'Accept-Encoding':'gzip, deflate, sdch, br', 'Accept-Language':'en-US,en;q=0.8',
                   'Referer':referer, 'User-Agent':md.User_Agent(), 'X-Requested-With':'XMLHttpRequest'}
        
        data = open_url(slug, params=params, headers=headers, verify=False).content
        xx = re.compile("_x='([^']+)'").findall(data)[0]
        xy = re.compile("_y='([^']+)'").findall(data)[0]
        request_url2 = '%s/ajax/movie_sources/%s' %(baseurl,episode_id)
        hash_params = {'x':xx, 'y':xy}
        headers = {'Accept':'application/json, text/javascript, */*; q=0.01',
                   'Accept-Encoding':'gzip, deflate, sdch, br', 'Accept-Language':'en-US,en;q=0.8',
                   'Referer':referer, 'User-Agent':md.User_Agent(), 'X-Requested-With':'XMLHttpRequest'}
        final = open_url(request_url2, params=hash_params, headers=headers, verify=False).json()

        res_quality = []
        stream_url = []
        quality = ''
        if auto_play == 'true':
                url = max(final['playlist'][0]['sources'], key=lambda lab: int(re.sub('\D', '', lab['label'])))
                url = url['file']
        else:
                match = final['playlist'][0]['sources']
                for a in match:
                        quality = '[B][I][COLOR red]%s[/COLOR][/I][/B]' %a['label']
                        res_quality.append(quality)
                        stream_url.append(a['file'])
                if len(match) >1:
                        ret = md.dialog_select('Select Stream Quality',res_quality)
                        if ret == -1:
                                return
                        elif ret > -1:
                                url = stream_url[ret]
                else:
                        url = final['playlist'][0]['sources'][0]['file']
        md.resolved(url, name, fan_art, infolabels)
	addon.end_of_directory()




def PROXY_GET(url):

        proxy_menu = []
	proxy_path = []

        link = open_url(url).content
        all_videos = md.regex_get_all(link, 'pl-item', '</tr>')
        for a in all_videos:

                name = md.regex_from_to(a, 'title="', '"')
                url = md.regex_from_to(a, 'href="', '"')
                proxy_menu.append('[COLOR white][B]%s[/B][/COLOR]' %name)
		proxy_path.append(url)

	if len(all_videos) >1:
                ret = md.dialog_select('Select Proxy Address', proxy_menu)
		if ret == -1:
			return
		elif ret > -1:
                        url = proxy_path[ret]
		else:
                        url = proxy_path[0]

        headers = open_url(url, redirects=False).headers

        if 'location' in headers:
                url = headers['location']
        
        if url[-1] == '/':
                url = url[:-1]

        addon.set_setting('base_url', url)

        md.notification('url added to settings successfully',icon)

	return




mode = md.args['mode']
url = md.args.get('url', None)
name = md.args.get('name', None)
query = md.args.get('query', None)
title = md.args.get('title', None)
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
	CATS(content)

elif mode == '2':
	INDEX(url,content)

elif mode == '3':
	EPIS(title, url, iconimage, content, season)

elif mode == '4':
	GENRE(url, content)

elif mode == '5':
	YEAR(url, content)

elif mode == '6':
	COUNTRY(url, content)

elif mode == '7':
	LINKS(url,name,iconimage,content,infolabels,query)

elif mode == 'search':
	SEARCH(content,query)

elif mode == 'addon_search':
	md.addon_search(content,query,fan_art,infolabels)

elif mode == 'get_proxy':
	PROXY_GET(url)

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
xbmcplugin.endOfDirectory(int(sys.argv[1]))

# -*- coding: utf-8 -*-

'''
Copyright (C) 2014                                                     

This program is free software: you can redistribute it and/or modify   
it under the terms of the GNU General Public License as published by   
the Free Software Foundation, either version 3 of the License, or      
(at your option) any later version.                                    

This program is distributed in the hope that it will be useful,        
but WITHOUT ANY WARRANTY; without even the implied warranty of         
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          
GNU General Public License for more details.                           

You should have received a copy of the GNU General Public License      
along with this program. If not, see <http://www.gnu.org/licenses/>  
'''                                                                           

import urllib, urllib2, re, os, sys
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

mysettings = xbmcaddon.Addon(id = 'plugin.video.AznKodiAdult')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
logos = xbmc.translatePath(os.path.join(home, 'resources', 'logos\\'))
homemenu = xbmc.translatePath(os.path.join(home, 'resources', 'playlists', 'xxx_playlist.m3u'))
vietsextv = 'rtmpe://64.62.143.5/live/do%20not%20steal%20my-Stream2'
hdporn = 'http://pornhdhdporn.com'
playvid = 'http://www.playvid.com'
redtube = 'http://www.redtube.com'
xvideos = 'http://www.xvideos.com'
youjizz = 'http://www.youjizz.com'
youporn = 'http://www.youporn.com'
tube8 = 'http://www.tube8.com'
porncom = 'http://www.porn.com'
flyflv = 'http://www.flyflv.com'
vikiporn = 'http://www.vikiporn.com'
xhamster = 'http://xhamster.com'
tnaflix = 'https://www.tnaflix.com/'
lubetube = 'http://lubetube.com/'
erotik = 'http://www.ero-tik.com/'
v_erotik = 'http://videomega.tv/'
yesxxx = 'http://www.yes.xxx/'
pornxs = 'http://pornxs.com/'
zbporn = 'http://zbporn.com/'
pornhd = 'http://www.pornhd.com/'

def menulist():
	try:
		mainmenu = open(homemenu, 'r')  
		content = mainmenu.read()
		mainmenu.close()
		match = re.compile('#.+,(.+?)\n(.+?)\n').findall(content)
		return match
	except:
		pass	

def make_request(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
		response = urllib2.urlopen(req, timeout = 60)
		link = response.read()
		response.close()  
		return link
	except urllib2.URLError, e:
		print 'We failed to open "%s".' % url
		if hasattr(e, 'code'):
			print 'We failed with error code - %s.' % e.code	
		elif hasattr(e, 'reason'):
			print 'We failed to reach a server.'
			print 'Reason: ', e.reason

def home():
	add_dir('[COLOR cyan]. .[COLOR red]  ^  [COLOR cyan]. .[COLOR yellow]  Home  [COLOR cyan]. .[COLOR red]  ^  [COLOR cyan]. .[/COLOR]', '', None, icon, fanart)
			
def main():
	
	add_dir('[COLOR orange]FlyFLV [COLOR red] Adult Videos[/COLOR]', flyflv, 2, logos + 'flyflv.png', fanart) 
	add_dir('[COLOR yellow]LubeTube [COLOR red] Adult Videos[/COLOR]', lubetube, 2, logos + 'lubetube.png', fanart) 
	add_dir('[COLOR violet]PlayVid [COLOR red] Adult Videos[/COLOR]', playvid, 2, logos + 'playvid.png', fanart) 	
	add_dir('[COLOR blue]PornXS [COLOR red] Adult Videos[/COLOR]', pornxs + 'browse/', 2, logos + 'pornxs.png', fanart)		
	add_dir('[COLOR silver]ViKiPorn [COLOR red] Adult Videos[/COLOR]', vikiporn, 2, logos + 'vikiporn.png', fanart) 
	
def porn4u():
	home()
	for name, url in menulist(): 
		add_link(name, url, 4, logos + 'porn4u.png', fanart)

def HD():
	home()
	add_dir('[COLOR yellow]HD [COLOR red] Adult Videos[COLOR cyan] - [COLOR lime]Tube8[/COLOR]', tube8 + '/cat/hd/22/', 5, logos + 'hdadult.png', fanart)  
	add_dir('[COLOR lime]HD [COLOR red] Adult Videos[COLOR cyan] - [COLOR yellow]YouJizz[/COLOR]', youjizz + '/search/highdefinition-1.html', 6, logos + 'hdadult.png', fanart)    
  
def search():
	try:
		keyb = xbmc.Keyboard('', '[COLOR yellow]Enter search text[/COLOR]')
		keyb.doModal()
		if (keyb.isConfirmed()):
			searchText = urllib.quote_plus(keyb.getText())
		if 'HD - YouJizz' in name:
			url = youjizz + '/srch.php?q=' + searchText     	  
			youjizz_HD(url)
		elif 'redtube.com' in name:
			url = redtube + '/?search=' + searchText      	  
			media_list(url) 
		elif 'youjizz.com' in name:  
			url = youjizz + '/srch.php?q=' + searchText     	  
			media_list(url)			
		elif 'xvideos.com' in name:
			url = xvideos + '/?k=' + searchText      	  
			media_list(url)
		elif 'tube8.com' in name:
			url = tube8 + '/searches.html?q=' + searchText      	  
			category(url)
		elif 'HD - Tube 8' in name:
			url = tube8 + '/cat/hd/22/?q=' + searchText      	  
			tube8_HD(url)
		elif 'youporn.com' in name:
			url = youporn + '/search/?query=' + searchText      	  
			media_list(url)
		elif 'playvid.com' in name:
			url = playvid + '/search?q=' + searchText      	  
			media_list(url) 
		elif '.porn.com' in name:
			url = porncom + '/search?q=' + searchText      	  
			media_list(url) 
		elif 'flyflv.com' in name:
			url = flyflv + '/?q=' + searchText      	  
			media_list(url)
		elif 'vikiporn.com' in name:
			url = vikiporn + '/search/?q=' + searchText      	  
			media_list(url)	
		elif 'xhamster.com' in name:
			url = xhamster + '/search.php?q=' + searchText +'&qcat=video'     	  
			media_list(url)	
		elif 'tnaflix.com' in name:
			url = tnaflix + 'search.php?what=' + searchText  	  
			media_list(url)	
		elif 'lubetube.com' in name:
			url = lubetube + 'search/title/' + searchText.replace('+', '_') + '/'	  
			media_list(url)	
		elif 'ero-tik.com' in name:
			url = erotik + 'search.php?keywords=' + searchText	  
			media_list(url)	
		elif 'yes.xxx' in name:
			url = yesxxx + '?s=search&search=' + searchText	  
			media_list(url)		
		elif 'pornxs.com' in name:
			url = pornxs + 'search.php?s=' + searchText	  
			search_result(url)
		elif 'zbporn' in name:
			url = zbporn + 'search/?q=' + searchText	  
			media_list(url)	
		elif 'pornhd.com' in name:
			url = pornhd + 'search?search=' + searchText	  
			media_list(url)				
	except:
		pass	

def search_result(url):
	home()
	content = make_request(url)
	if 'pornxs' in url:
		match = re.compile('href="/(.+?)">\s*<div class.+?>\s*<div class.+?>\s*<div class.+?>\s*<img src="(.+?)" alt="(.+?)"').findall(content)
		for url, thumb, name in match:
			add_link(name, pornxs + url, 4, thumb, fanart)			
		match = re.compile('href="(.+?)">(\d+)<').findall(content)
		for url, name in match:
			add_dir('[COLOR yellow]Page ' + name + '[/COLOR]', url.replace('&amp;', '&'), 30, logos + 'pornxs.png', fanart)
	xbmc.executebuiltin('Container.SetViewMode(500)')
	
def category(url): 
	home()
	if 'youjizz' in url:
		content = make_request(url)
		add_dir('[COLOR yellow]youjizz.com   [COLOR lime]>[COLOR cyan]>[COLOR orange]>[COLOR magenta]>   [COLOR red]Adult Movie Search[/COLOR]', youjizz, 1, logos + 'youjizz.png', fanart)
		add_dir('[COLOR lime]HD[/COLOR]', youjizz + '/search/highdefinition-1.html', 3, logos + 'youjizz.png', fanart)
		match = re.compile("<a href=\"(.+?)\" ><span>(.+?)<\/span><\/a>").findall(content)
		for url, name in match:
			add_dir('[COLOR cyan]' + name + '[/COLOR]', youjizz + url, 3, logos + 'youjizz.png', fanart)  
		match = re.compile("<a href=\"([^\"]*)\"><span>(.+?)<\/span><\/a>").findall(content)[1:-1]
		for url, name in match:
			add_dir('[COLOR cyan]' + name + '[/COLOR]', youjizz + url, 3, logos + 'youjizz.png', fanart)
	elif 'xvideos' in url:
		content = make_request(url)
		add_dir('[COLOR lightgreen]xvideos.com   [COLOR lime]>[COLOR cyan]>[COLOR orange]>[COLOR magenta]>   [COLOR red]Adult Movie Search[/COLOR]', xvideos, 1, logos + 'xvideos.png', fanart)
		match = re.compile('<img src="(.+?)" id=".+?" onload=".+?" onerror=".+?"  /></a>\s*</div>\s*<p><a href="(.+?)" title="(.+?)">').findall(content)
		for thumb, url, name in match:
			add_link('[COLOR yellow]' + name + '[/COLOR]', xvideos + url, 4, thumb, fanart)
		match = re.compile("href=\"([^\"]*)\">1<").findall(content)	
		add_dir('[COLOR lime]New Videos[/COLOR]', xvideos + match[-1], 3, logos + 'xvideos.png', fanart)
		match = re.compile("href=\"([^\"]+)\">Best Videos<").findall(content)  
		add_dir('[COLOR orange]Best Videos[/COLOR]', xvideos + match[0], 3, logos + 'xvideos.png', fanart)  
		content = make_request(xvideos)
		match = re.compile("<li><a href=\"\/c\/(.+?)\">(.+?)<\/a>").findall(content) 
		for url, name in match:
			add_dir('[COLOR cyan]' + name + '[/COLOR]', xvideos + '/c/' + url, 3, logos + 'xvideos.png', fanart)
		xbmc.executebuiltin('Container.SetViewMode(500)')
	elif 'tube8' in url:
		content = make_request(url)
		add_dir('[COLOR lime]tube8.com   [COLOR lime]>[COLOR cyan]>[COLOR orange]>[COLOR magenta]>   [COLOR red]Adult Movie Search[/COLOR]', tube8, 1, logos + 'tube8.png', fanart)
		match = re.compile('href="(.+?)" class="video-thumb-link">\s*<img class="videoThumbs"\s*id=".+?"\s*category=".+?"\s*src="(.+?)"\s*alt="(.+?)"').findall(content)
		for url, thumb, name in match:
			if 'HD' in name:
				add_link('[COLOR yellow]' + name + '[/COLOR]', url, 4, thumb, fanart)
		match = re.compile('href="(.+?)" class="video-thumb-link">\s*<img class="videoThumbs"\s*id=".+?"\s*category=".+?"\s*src="(.+?)"\s*alt="(.+?)"').findall(content)
		for url, thumb, name in match:	  
			if 'HD' in name:
				pass
			else:  
				add_link('[COLOR cyan]' + name + '[/COLOR]', url, 4, thumb, fanart)	
		match = re.compile("href=\"(.+?)\">(\d+)<").findall(content) 
		for url, name in match:  
			add_dir('[COLOR lime]Page ' + name + '[COLOR orange] >>>>[/COLOR]', url, 2, logos + 'tube8.png', fanart)
		xbmc.executebuiltin('Container.SetViewMode(500)')
	elif 'youporn' in url:
		content = make_request(url)
		add_dir('[COLOR lime]youporn.com   [COLOR lime]>[COLOR cyan]>[COLOR orange]>[COLOR magenta]>   [COLOR red]Adult Movie Search[/COLOR]', youporn, 1, logos + 'youporn.png', fanart)
		match = re.compile("onclick=\".+?\" href=\"([^\"]*)\">(.+?)<").findall(content)[1:7]
		for url, name in match:
			add_dir('[COLOR yellow]' + name + '[/COLOR]', youporn + url, 3, logos + 'youporn.png', fanart)
		add_dir('[COLOR yellow]Most Discussed[/COLOR]', youporn + '/most_discussed/', 3, logos + 'youporn.png', fanart)	
		match = re.compile("href=\"\/category(.+?)\">(.+?)<").findall(content)
		for url, name in match:
			add_dir('[COLOR cyan]' + name + '[/COLOR]', youporn + '/category' + url, 3, logos + 'youporn.png', fanart)	
		match = re.compile("href=\"\/country(.+?)\">(.+?)<").findall(content)
		for url, name in match:
			add_dir('[COLOR lime]' + name + '[/COLOR]', youporn + '/country' + url, 3, logos + 'youporn.png', fanart)
	elif 'playvid' in url:
		content = make_request(url)
		add_dir('[COLOR lime]playvid.com   [COLOR lime]>[COLOR cyan]>[COLOR orange]>[COLOR magenta]>   [COLOR red]Adult Movie Search[/COLOR]', playvid, 1, logos + 'playvid.png', fanart)
		match = re.compile('class="ajax" href="(.+?)" title="(.+?)"').findall(content)
		for url, name in match:
			name = name.replace('HD', 'HD [COLOR magenta]- [COLOR cyan]HD quality for registered members only.')
			add_dir('[COLOR yellow]' + name + '[/COLOR]', playvid + url, 3, logos + 'playvid.png', fanart)      
		match = re.compile('class="ajax" href="(.+?)" >(.+?)<').findall(content)
		for url,name in match:  
			add_dir('[COLOR yellow]' + name + '[/COLOR]', playvid + url, 9, logos + 'playvid.png', fanart)
	elif 'redtube' in url:
		content = make_request(url)
		add_dir('[COLOR lime]redtube.com   [COLOR lime]>[COLOR cyan]>[COLOR orange]>[COLOR magenta]>   [COLOR red]Adult Movie Search[/COLOR]', redtube, 1, logos + 'redtube.png', fanart)
		add_dir('[COLOR magenta]Channels[/COLOR]', redtube + '/channel', 10, logos + 'redtube.png', fanart) 
		content = make_request(redtube)
		match = re.compile('href="([^"]*)" onclick="return([^"]*)">\s*(.+?)\s*<').findall(content)
		for url, dummy, name in match:
			if 'Channels' in name or 'Subscriptions' in name:
				pass
			else:
				add_dir('[COLOR yellow]' + name + '[/COLOR]', redtube + url, 3, logos + 'redtube.png', fanart)      
		match = re.compile('href="([^"]+)" title="([^"]*)".+?\s*<img src="(.+?)"').findall(content)
		for url, name, thumb in match:  
			add_dir('[COLOR cyan]' + name + '[/COLOR]', redtube + url, 3, thumb, fanart)
	elif '.porn.com' in url:
		content = make_request(url)
		add_dir('[COLOR lightblue].porn.com   [COLOR lime]>[COLOR cyan]>[COLOR orange]>[COLOR magenta]>   [COLOR red]Adult Movie Search[/COLOR]', porncom, 1, logos + 'porncom.png', fanart)	
		match = re.compile('href="/videos/(.+?)" title="(.+?)"').findall(content)[31:200]
		for url, name in match:
			add_dir(name, porncom + '/videos/' + url,  3, logos + 'porncom.png', fanart)
	elif 'flyflv' in url:
		content = make_request(url)
		add_dir('[COLOR orange]flyflv.com   [COLOR lime]>[COLOR cyan]>[COLOR orange]>[COLOR magenta]>   [COLOR red]Adult Movie Search[/COLOR]', flyflv, 1, logos + 'flyflv.png', fanart)	
		match = re.compile('href="/category/(.+?)">(.+?)<').findall(content)[:23]
		for url, name in match:
			add_dir(name, flyflv + '/category/' + url,  3, logos + 'flyflv.png', fanart)
	elif 'vikiporn' in url:
		content = make_request(url)
		add_dir('[COLOR silver]vikiporn.com   [COLOR lime]>[COLOR cyan]>[COLOR orange]>[COLOR magenta]>   [COLOR red]Adult Movie Search[/COLOR]', vikiporn, 1, logos + 'vikiporn.png', fanart)	
		match = re.compile('href="(.+?)">(.+?)<span>(\(\d+\))<').findall(content)[42:]
		for url, name, inum in match:
			inum = inum.replace(')', ' videos)')
			add_dir(name + '[COLOR lime] ' + inum + '[/COLOR]', url,  3, logos + 'vikiporn.png', fanart)
	elif 'xhamster' in url:
		content = make_request(url)
		add_dir('[COLOR blue]xhamster.com   [COLOR lime]>[COLOR cyan]>[COLOR orange]>[COLOR magenta]>   [COLOR red]Adult Movie Search[/COLOR]', xhamster, 1, logos + 'xhamster.png', fanart)	
		match = re.compile("href='/channels(.+?)'>(.+?)</a>").findall(content)
		for url, name in match:
			name = name.split('>')[-1]
			add_dir(name, xhamster + '/channels' + url,  3, logos + 'xhamster.png', fanart)
	elif 'tnaflix' in url:
		content = make_request(url)
		add_dir('[COLOR green]tnaflix.com   [COLOR lime]>[COLOR cyan]>[COLOR orange]>[COLOR magenta]>   [COLOR red]Adult Movie Search[/COLOR]', tnaflix, 1, logos + 'tnaflix.png', fanart)	
		match = re.compile('href="/([^"]*)" title=".+?">(?!Sign In)(.+?)<').findall(content)
		for url, name in match:
			name = name.replace('&amp;', '&')
			add_dir(name, tnaflix + url,  3, logos + 'tnaflix.png', fanart)
	elif 'lubetube' in url:
		content = make_request(url)
		add_dir('[COLOR white]lubetube.com   [COLOR lime]>[COLOR cyan]>[COLOR orange]>[COLOR magenta]>   [COLOR red]Adult Movie Search[/COLOR]', lubetube, 1, logos + 'lubetube.png', fanart)	
		match = re.compile('href="http://lubetube.com/search/adddate/cat/([^"]*)">(.+?)<').findall(content)
		for url, name in match:
			add_dir(name, lubetube + 'search/adddate/cat/' + url,  3, logos + 'lubetube.png', fanart)
		next_content =	make_request(lubetube + 'pornstars/')
		match = re.compile('href="/pornstars/(\w)">(.+?)<').findall(next_content)
		for url, name in match:
			add_dir(name, lubetube + 'pornstars/' + url,  12, logos + 'lubetube.png', fanart)
	elif 'ero-tik' in url:
		content = make_request(url)
		add_dir('[COLOR cyan]ero-tik.com   [COLOR lime]>[COLOR cyan]>[COLOR orange]>[COLOR magenta]>   [COLOR red]Adult Movie Search[/COLOR]', erotik, 1, logos + 'erotik.png', fanart)
		match = re.compile('href="(.+?)" class="wide-nav-link">(.+?)<').findall(content)[1:6]
		for url, name in match:
			add_dir(name, url,  3, logos + 'erotik.png', fanart)		
		match = re.compile('href="http://www.ero-tik.com/browse-(.+?)" class="">(.+?)<').findall(content)[:24]
		for url, name in match:
			add_dir(name, erotik + 'browse-' + url,  3, logos + 'erotik.png', fanart)	
	elif 'yes.xxx' in url:
		content = make_request(url)
		match = re.compile('href="/(.+?)" title="(.+?)"><img src="(.+?)" /><b>.+?</b></a>(.+?)</div>').findall(content)
		for url, name, thumb, vidnum in match:
			add_dir(name + '[COLOR lime]' + vidnum + '[/COLOR]', yesxxx + url,  3, thumb, fanart)		
		match = re.compile('href="/(.+?)">(\d+)<').findall(content)
		for url, name in match:
			add_dir('[COLOR cyan]Page ' + name + '[/COLOR]', yesxxx + url,  2, logos + 'yes.png', fanart)
	elif 'pornxs' in url:
		content = make_request(url)
		add_dir('[COLOR blue]pornxs.com   [COLOR lime]>[COLOR cyan]>[COLOR orange]>[COLOR magenta]>   [COLOR red]Adult Movie Search[/COLOR]', pornxs, 1, logos + 'pornxs.png', fanart)
		links = re.compile('<div class=title>categories</div>((?s).+?)<div class=clear></div>').findall(content)	# ((?s).+?) scrape multiline
		match = re.compile('href="/(.+?)">(.+?)<').findall(str(links))
		for url, name in match:
			add_dir(name, pornxs + url,  3, logos + 'pornxs.png', fanart)
	elif 'zbporn' in url:
		content = make_request(url)
		if 'categories' in url:
			match = re.compile('href="(.+?)"><span>(.+?)</span> (\d+)<').findall(content)
			for url, name, VidNum in match:
				add_dir(name + ' [COLOR lime](' + VidNum + ' videos)[/COLOR]', url,  3, logos + 'zbporn.png', fanart)
		elif 'performers' in url:
			match = re.compile('href="(.+?)"><img src="(.+?)" alt="(.+?)"><span class="info">(.+?) <').findall(content)
			for url, thumb, name, VidNum in match:
				add_dir(name + ' [COLOR lime](' + VidNum + ')[/COLOR]', url,  3, thumb, fanart)
			match = re.compile('data-page="\d+" href="(.+?)">(\d+)<').findall(content)
			for url, name in match:
				add_dir('[COLOR cyan]Page ' + name + '[/COLOR]', zbporn + url,  2, logos + 'zbporn.png', fanart)		
	elif 'pornhd' in url:
		add_dir('[COLOR lime]pornhd.com   [COLOR lime]>[COLOR cyan]>[COLOR orange]>[COLOR magenta]>   [COLOR red]Adult Movie Search[/COLOR]', pornhd, 1, logos + 'pornhd.png', fanart)	
		url1 = url + 'category'
		content = make_request(url1)
		new_content = ''.join(content.splitlines()).replace('\t', '')	
		match = re.compile('img width="\d+" height="\d+" src="(.+?)".+?href="/(.+?)">(.+?)<').findall(new_content)
		for thumb, href, name in match:
			add_dir(name.replace('&amp;', '&'), pornhd + href,  3, thumb, fanart)
		url2 = url + 'pornstars'	
		content = make_request(url2)
		new_content = ''.join(content.splitlines()).replace('\t', '')	
		match = re.compile('href="/([^<]*)">([A-Z])<').findall(new_content)
		for href, name in match:
			add_dir(name, pornhd + href,  3, logos + 'pornhd.png', fanart)

def porn_hd(url):
	home()
	content = make_request(url)
	new_content = ''.join(content.splitlines()).replace('\t', '')
	match = re.compile('img src="(.+?)".+?<time>(.+?)</time>.+?href="/(.+?)">(.+?)<').findall(new_content)
	for thumb, duration, url, name in match:
		add_link(name + ' [COLOR orange](' + duration + ')[/COLOR]', pornhd + url, 4, thumb, fanart)
	match = re.compile('class="" rel="" href="/(.+?)">(\d+)<').findall(new_content)
	for url, name in match:
		add_dir('[COLOR cyan]Page ' + name + '[/COLOR]', pornhd + url, 50, logos + 'pornhd.png', fanart)		
	xbmc.executebuiltin('Container.SetViewMode(500)')
	
def zb_porn():
	home()
	add_dir('[COLOR green]zbporn.com   [COLOR lime]>[COLOR cyan]>[COLOR orange]>[COLOR magenta]>   [COLOR red]Adult Movie Search[/COLOR]', zbporn, 1, logos + 'zbporn.png', fanart)	
	add_dir('Latest Updates', zbporn + 'latest-updates/', 3, logos + 'zbporn.png', fanart) 
	add_dir('Models', zbporn + 'performers/', 2, logos + 'zbporn.png', fanart) 
	add_dir('Categories', zbporn + 'categories/', 2, logos + 'zbporn.png', fanart) 
		
def lubtetube_pornstars(url):
	home()
	content = make_request(url)
	match = re.compile('class="frame" href="/(.+?)"><img src="(.+?)" alt="(.+?)"').findall(content)
	for url, thumb, name in match:
		add_dir(name, lubetube + url,  3, thumb, fanart)
	match = re.compile('href="/pornstars/(.+?)">(\d+)<').findall(content)
	for url, name in match:
		add_dir('[COLOR yellow]Page ' + name + '[/COLOR]', lubetube + 'pornstars/' + url,  12, logos + 'lubetube.png', fanart)
			
def play_vid(url):
	home()
	content = make_request(url)
	if 'categories' in url:
		match = re.compile('data-url="(.+?)"\s*data-title="(.+?)videos"\s*data-image="(.+?)"').findall(content)
		for url, name, thumb in match:
			name = name.replace('Adult', '')
			add_dir('[COLOR lightblue]' + name + '[/COLOR]', url, 3,thumb, fanart)
	else:    
		match = re.compile('img src="(.+?)".+?\s.+\s*\s.+\s.+href="(.+?)">(.+?)</a>').findall(content)
		for thumb, url, name in match:
			thumb = thumb.replace('/images/thumbs/default-ava-channel-250.jpg', '//www.playvid.com/images/thumbs/default-ava-channel-250.jpg')
			add_dir('[COLOR lightgreen]' + name + '[/COLOR]', playvid + url, 3, 'http:' + thumb, fanart)

def yess_xxx():
	home()
	add_dir('[COLOR cyan]yes.xxx  [COLOR lime]>[COLOR cyan]>[COLOR orange]>[COLOR magenta]>   [COLOR red]Adult Movie Search[/COLOR]', yesxxx, 1, logos + 'yes.png', fanart)	
	add_dir('Most recent', yesxxx + '?s=recent', 3, logos + 'yes.png', fanart) 
	add_dir('Most view', yesxxx + '?s=viewed', 3, logos + 'yes.png', fanart)
	add_dir('Categories', yesxxx + '?s=tags', 2, logos + 'yes.png', fanart)
	add_dir('Channels', yesxxx + '?s=channels', 2, logos + 'yes.png', fanart)	
	
def tube8_HD(url):
	home()
	content = make_request(url)
	add_dir('[COLOR cyan]HD - Tube 8   [COLOR lime]>[COLOR cyan]>[COLOR orange]>[COLOR magenta]>   [COLOR red]Adult Movie Search[/COLOR]', tube8 + '/cat/hd/22/', 1, logos + 'hdadult.png', fanart)  
	match = re.compile('href="(.+?)" class="video-thumb-link">\s*<span class="(.+?)Icon"><\/span>\s*<img class="videoThumbs"\s*id=".+?"\s*category=".+?"\s*src="(.+?)"\s*alt="(.+?)"').findall(content)
	for url, hdcat, thumb, name in match:
		add_link('[COLOR yellow]' + name + ' [COLOR lime][UPPERCASE][' + hdcat + '][/UPPERCASE][/COLOR] ', url, 4, thumb, fanart)
	match = re.compile("href=\"http:\/\/www.tube8.com(.+?)\">(\d+)<").findall(content) 
	for url, name in match:  
		add_dir('[COLOR magenta]Page ' + name + '[COLOR orange] >>>>[/COLOR]', tube8 + url, 5, logos + 'hdadult.png', fanart) 
	xbmc.executebuiltin('Container.SetViewMode(500)')
	
def youjizz_HD(url):
	home()
	content = make_request(url)
	match = re.compile("href='([^']*)'.+?\s*\s*<img class=.+?data-original=\"([^\"]*)\">\s*<\/span>\s*<span id=\"title1\">\s*(.+?)<\/span>").findall(content)
	for url, thumb, name in match:
		if '-1280-720-' in thumb:  # SD contents '-640-480-' in thumbnail
			add_link('[COLOR yellow]' + name + ' [COLOR lime][HD - 720][/COLOR] ', youjizz + url, 4, thumb, fanart)	
		elif '-1280-960-' in thumb or '-1920-1080-' in thumb:
			add_link('[COLOR yellow]' + name + ' [COLOR cyan][HD - 1080][/COLOR] ', youjizz + url, 4, thumb, fanart)	
	match = re.compile("href=\"\/search(.+?)\">(\d+)<").findall(content) 
	for url, name in match:  
		add_dir('[COLOR lime]Page ' + name + '[COLOR orange] >>>>[/COLOR]', youjizz + '/search' + url, 6, logos + 'hdadult.png', fanart) 
	match = re.compile('href=\'\/search(.+?)\'>(\d+)<').findall(content) 
	for url, name in match:  
		add_dir('[COLOR red]Page ' + name + '[COLOR yellow] >>>>[/COLOR]', youjizz + '/search' + url, 6, logos + 'hdadult.png', fanart)        
	xbmc.executebuiltin('Container.SetViewMode(500)')
	
def redtube_channels_cat(url): 
	home()
	content = make_request(url)
	match = re.compile('href="/channel/(.+?)" title="(.+?)">').findall(content)
	for url, name in match:
		add_dir('[COLOR orange]' + name + '[/COLOR]', redtube + '/channel/' + url, 11, logos + 'redtube.png', fanart)  
	match = re.compile('href="(.+?)">([A-Z])<').findall(content)
	for url, name in match:
		add_dir('[COLOR violet]' + name + '[/COLOR]', redtube + url, 11, logos + 'redtube.png', fanart)

def redtube_channels_list(url):
	home()
	content = make_request(url)
	match = re.compile('href="(.+?)" class="channels-list-img">\s*<img src="(.+?)" alt="(.+?)">').findall(content)
	for url, thumb, name in match:
		add_dir('[COLOR lightgreen]' + name + '[/COLOR]', redtube + url, 3, thumb, fanart)
	match = re.compile('<a  href	= "(.+?)" title	= ".+?" ><b>(\d+)</b></a>').findall(content)
	for url, name in match:
		add_dir('[COLOR yellow]Page ' + name + '[/COLOR]', redtube + url, 11, logos + 'redtube.png', fanart)
   
def media_list(url):
	home()
	content = make_request(url)
	if 'youjizz' in url:	  
		if 'random' in url or 'srch.php' in url:
			match = re.compile("<a class=\"frame\" href='(.+?)'.+?><\/a>\s*<img class.+?data-original=\"(.+?)\"").findall(content)		
			for url, thumb in match:
				name = url.replace('/videos/', '').replace('-', ' ').replace('.html', '') 
				name = re.sub('\s\d+$', '', name) # Get rid of numbers at the end of string 
				add_link('[COLOR yellow][UPPERCASE]' + name + '[/UPPERCASE][/COLOR]', youjizz + url, 4, thumb, fanart)
		elif 'highdefinition' in url:
			match = re.compile("href='([^']*)'.+?\s*\s*<img class=.+?data-original=\"([^\"]*)\">\s*<\/span>\s*<span id=\"title1\">\s*(.+?)<\/span>").findall(content)
			for url, thumb, name in match: # SD contents '-640-480-' in thumbnail
				if '-1280-720-' in thumb:  
					add_link('[COLOR yellow]' + name + ' [COLOR lime][HD - 720][/COLOR] ', youjizz + url, 4, thumb, fanart)	
				elif '-1280-960-' in thumb or '-1920-1080-' in thumb:
					add_link('[COLOR yellow]' + name + ' [COLOR cyan][HD - 1080][/COLOR] ', youjizz + url, 4, thumb, fanart)	
			match = re.compile("href=\"\/search(.+?)\">(\d+)<").findall(content) 
			for url, name in match:  
				add_dir('[COLOR lime]Page ' + name + '[COLOR orange] >>>>[/COLOR]', youjizz + '/search' + url, 3, logos + 'hdadult.png', fanart) 
			match = re.compile('href=\'\/search(.+?)\'>(\d+)<').findall(content) 
			for url, name in match:  
				add_dir('[COLOR red]Page ' + name + '[COLOR yellow] >>>>[/COLOR]', youjizz + '/search' + url, 3, logos + 'hdadult.png', fanart) 
		else:
			match = re.compile("<a class=\"frame\" href='(.+?)'.+?><\/a>\s*<img class.+?data-original=\"(.+?)\">\s*<\/span>\s*<span id=\"title1\">(.+?)<\/span>\s*<span id=\"title2\">\s*<span class='thumbtime'><span>(.+?)<\/span>").findall(content)		
			for url, thumb, name, duration in match:
				add_link('[COLOR yellow]' + name + ' [COLOR lime](' + duration + ')[/COLOR]', youjizz + url, 4, thumb, fanart)
			match = re.compile("<a href=\"(.+?).html\">(\d+)<\/a>").findall(content)
			for url, name in match:	
				add_dir('[COLOR orange]Page ' + name + '[COLOR cyan]  >>>>[/COLOR]', youjizz + url + '.html', 3, logos + 'youjizz.png', fanart)
			match = re.compile("<a href='([^>]*)'>(\d+)<\/a>").findall(content)
			for url, name in match:	
				add_dir('[COLOR red]Page ' + name + '[COLOR magenta]  >>>>[/COLOR]', youjizz + url, 3, logos + 'youjizz.png', fanart)
	elif 'xvideos' in url:
		match = re.compile("<a href=\"(.+?)\"><img src=\"(.+?)\"").findall(content)
		for url, thumb in match:
			name = re.sub('/video[0-9]+/', '', url).replace('_', ' ').replace('-', ' ').replace('.', ' ')
			add_link('[COLOR yellow]' + name + '[/COLOR]', xvideos + url, 4, thumb, fanart)
		match = re.compile("class=\"nP\" href=\"(.+?)\">Next<").findall(content)  
		add_dir('[COLOR lime]Next[COLOR orange]  Page[COLOR red]  >>>>[/COLOR]', xvideos + match[0], 3, logos + 'xvideos.png', fanart)
	elif 'youporn' in url:
		match = re.compile("href=\"(.+?)\">\s*<span class=\"hdIcon\"><\/span>	<img src=\"(.+?)\" alt=\"(.+?)\"").findall(content)
		for url, thumb, name in match:
			add_link('[COLOR yellow]' + name.replace("&#39;", "'") + '[/COLOR]', youporn + url, 4, thumb, fanart)
		match = re.compile("href=\"(.+?)\">\s*<img src=\"(.+?)\" alt=\"(.+?)\"").findall(content)
		for url, thumb, name in match:
			add_link('[COLOR yellow]' + name + '[/COLOR]', youporn + url, 4, thumb, fanart)	
		match = re.compile("link rel=\"next\" href=\"(.+?)\"").findall(content) 
		for url in match:  
			add_dir('[COLOR lime]Next[COLOR orange]  Page[COLOR red]  >>>>[/COLOR]', url, 3, logos + 'youporn.png', fanart)
	elif 'playvid' in url:
		match = re.compile('title="([^"]*)">\s\s*\s.+\s.+href="([^"]+)".+?src="([^"]*)".+?\s*\s.+\s.+"duration">(.+?)<').findall(content)
		for name, url, thumb, duration in match:
			add_link('[COLOR cyan]' + name + ' [COLOR orange][' + duration + '][/COLOR]', playvid + url, 4, thumb, fanart)
		match = re.compile('class="ajax" href="(.+?)">(\d+)<').findall(content)
		for url, name in match:
			add_dir('[COLOR lime]Page ' + name + '[/COLOR]', playvid + url, 3, logos + 'playvid.png', fanart)
	elif 'redtube' in url:
		match = re.compile('href="([^"]*)" title="(.+?)" class.+?>\s*<span.+?>([^>]*)</span>\s*<img.+?data-src="([^"]+)"').findall(content)
		for url, name, duration, thumb in match:
			name = name.replace('&#039;', '\'').replace('&amp;', '&')
			add_link('[COLOR cyan]' + name + ' [COLOR orange][' + duration + '][/COLOR]', redtube + url, 4, thumb, fanart)
		match = re.compile('<a  href	= "(.+?)" title	= ".+?" onclick	= ".+?" ><b>(\d+)</b>').findall(content)
		for url, name in match:
			add_dir('[COLOR lime]Page ' + name + '[/COLOR]', redtube + url, 3, logos + 'redtube.png', fanart)
	elif '.porn.com' in url:
		match = re.compile('href="([^"]*)" class="thumb"><img src="(.+?)".+?class=".+?".+?"duration">(.+?)<.+?title="(.+?)"').findall(content)
		for url, thumb, duration, name in match:
			add_link(name + ' [COLOR lime]('+ duration + ')[/COLOR]', porncom + url, 4, thumb, fanart)
		match = re.compile('href="([^"]*)">(\d+)</a>&nbsp;').findall(content)
		for url, name in match:
			add_dir('[COLOR yellow]Page ' + name + '[/COLOR]', porncom + url.replace('&amp;', '&') , 3, logos + 'porncom.png', fanart)			
	elif 'flyflv' in url:
		match = re.compile('class="imageLink" href="(.+?)"><img.+?bestThumb.+?src="(.+?)" alt="(.+?)"').findall(content)
		for url, thumb, name in match:
			add_link(name, flyflv + url, 4, thumb, fanart)
		match = re.compile('href="(.+?)">(\d+)<').findall(content)
		for url, name in match:
			add_dir('[COLOR yellow]Page ' + name + '[/COLOR]', flyflv + url, 3, logos + 'flyflv.png', fanart)			
	elif 'vikiporn' in url:
		match = re.compile('href="(.+?)">\s*.+\s*<img.+?original="(.+?)" alt="(.+?)".+?\(this\)">\s*.+"time-info">(.+?)<').findall(content)
		for url, thumb, name, duration in match:
			add_link(name + '[COLOR lime] (' + duration + ')[/COLOR]', url, 4, thumb, fanart)
		match = re.compile('href="(.+?)" title="Page (\d+)"').findall(content)
		for url, name in match:
			add_dir('[COLOR yellow]Page ' + name + '[/COLOR]', vikiporn + url, 3, logos + 'vikiporn.png', fanart)			
	elif 'xhamster' in url:
		match = re.compile("href='(.+?)'  class.*?><img src='(.+?)'.+?class='thumb' alt=\"(.+?)\"").findall(content)
		for url, thumb, name in match:
			add_link(name, url, 4, thumb, fanart)
		match = re.compile("href='([^']*)'>(\d+)<").findall(content)
		for url, name in match:
			url = url.replace('search.php?q=', '/search.php?q=')
			add_dir('[COLOR yellow]Page ' + name + '[/COLOR]', xhamster + url, 3, logos + 'xhamster.png', fanart)						
	elif 'tnaflix' in url:
		match = re.compile('href="/(.+?)" class.+?title="">\s*.+><h2>(.+?)</h2>\s*.+"duringTime">(.+?)</span>\s*.+\s*<img src="(.+?)"').findall(content)
		for url, name, duration, thumb in match:
			add_link(name + '[COLOR lime] (' + duration + ')[/COLOR]', tnaflix + url, 4, 'http:' + thumb, fanart)
		match = re.compile('href="([^"]*)">(\d+)<').findall(content)
		for url, name in match:
			url = url.replace('search.php', tnaflix + 'search.php')
			add_dir('[COLOR yellow]Page ' + name + '[/COLOR]', url, 3, logos + 'tnaflix.png', fanart)	
	elif 'lubetube' in url:
		match = re.compile('href="(.+?)" title="(.+?)"><img src="(.+?)".+?Length: (.+?)<').findall(content)
		for url, name, thumb, duration in match:
			add_link(name + '[COLOR lime] (' + duration + ')[/COLOR]', url, 4, thumb, fanart)
		match = re.compile('href="/([^"]*)">(\d+)<').findall(content)
		for url, name in match:
			add_dir('[COLOR yellow]Page ' + name + '[/COLOR]', lubetube + url, 3, logos + 'lubetube.png', fanart)	
	elif 'ero-tik' in url:
		match = re.compile('href="(.+?)" class=".+?"><span class=".+?"><img src="(.+?)" alt="(.+?)"').findall(content)
		for url, thumb, name in match:
			add_link(name, url, 4, thumb, fanart)
		match = re.compile('<a href="(.+?)">&raquo;</a>').findall(content)
		for url in match:
			if 'http://www.ero-tik.com/' not in url:
				add_dir('[COLOR lime]Next page[/COLOR]', erotik + url.replace(' ', '%20'), 3, logos + 'erotik.png', fanart)
			else:
				add_dir('[COLOR lime]Next page[/COLOR]', url, 3, logos + 'erotik.png', fanart)
	elif 'yes.xxx' in url:
		match = re.compile('href="/(.+?)" title="(.+?)"><img src="(.+?)".+?"dur">(.+?)<').findall(content)
		for url, name, thumb, duration in match:
			add_link(name + ' (' + duration + ')', yesxxx + url, 4, thumb, fanart)
		match = re.compile('href="/(.+?)">(\d+)<').findall(content)
		for url, name in match:
			add_dir(name, yesxxx + url,  3, logos + 'yes.png', fanart)	
	elif 'pornxs' in url:
		match = re.compile('href="/(.+?)"><.+?class=video>\s*<img src="(.+?)" alt="(.+?)"').findall(content)
		for url, thumb, name in match:
			add_link(name, pornxs + url, 4, thumb, fanart)
		match = re.compile('href="/(.+?)"><.+?video-container-box>\s*<div class=video><img src="(.+?)" alt="(.+?)"').findall(content)
		for url, thumb, name in match:
			add_link(name, pornxs + url, 4, thumb, fanart)			
		match = re.compile('href="/(.+?)">(\d+)<').findall(content)
		for url, name in match:
			add_dir('[COLOR yellow]Page ' + name + '[/COLOR]', pornxs + url, 3, logos + 'pornxs.png', fanart)	
	elif 'zbporn' in url:
		match = re.compile('href="(.+?)".*?><img src="(.+?)" alt="(.+?)"').findall(content)
		for url, thumb, name in match:
			add_link(name , url, 4, thumb, fanart)
		match = re.compile('data-page="\d+" href="(.+?)">(\d+)<').findall(content)
		for url, name in match:
			add_dir('[COLOR cyan]Page ' + name + '[/COLOR]', zbporn + url,  3, logos + 'zbporn.png', fanart)
	elif 'pornhd' in url:
		if ('category' in url) or ('search' in url):
			new_content = ''.join(content.splitlines()).replace('\t', '')
			match = re.compile('img src="(.+?)".+?<time>(.+?)</time>.+?href="/(.+?)">(.+?)<').findall(new_content)
			for thumb, duration, url, name in match:
				add_link(name + ' [COLOR orange](' + duration + ')[/COLOR]', pornhd + url, 4, thumb, fanart)
		elif 'pornstars' in url:
			new_content = ''.join(content.splitlines()).replace('\t', '')
			match = re.compile('img src="(.+?)" alt.+?href="/(.+?)">(.+?)</a><div class="video-count">(.+?)</div>').findall(new_content)
			for thumb, url, name, VidNum in match:
				add_dir(name + ' [COLOR lime](' + VidNum + ')[/COLOR]', pornhd + url, 50, thumb, fanart)
		match = re.compile('class="" rel="" href="/(.+?)">(\d+)<').findall(new_content)
		for url, name in match:
			add_dir('[COLOR cyan]Page ' + name + '[/COLOR]', pornhd + url, 3, logos + 'pornhd.png', fanart)								
	xbmc.executebuiltin('Container.SetViewMode(500)')
	
def resolve_url(url):
	content = make_request(url)
	if 'youjizz' in url:
		media_url = re.compile("<a href=\"(.+?)\" style=\".+?\" >Download This Video<\/a>").findall(content)[0]
	elif 'xvideos' in url:
		media_url = urllib.unquote(re.compile("flv_url=(.+?)&amp").findall(content)[-1]) 
	elif 'tube8' in url:
		media_url = re.compile('videoUrlJS = "(.+?)"').findall(content)[0]
	elif 'youporn' in url:
		media_url = re.compile("video id=\"player-html5\" src=\"(.+?)\"").findall(content)[0].replace('&amp;', '&') 
		#media_url = re.compile("<span>&nbsp;<\/span><a href=\"(.+?)\"").findall(content)[0].replace('&amp;', '&')#MPG	
	elif 'playvid' in url:
		try:
			video_url = re.compile("video_urls.+?480p.+?=(.+?)&amp;video_vars").findall(content)[0]   #480p
		except:
			video_url = re.compile("video_urls.+?360p.+?=(.+?)&amp;video_vars").findall(content)[0]   #360p
		media_url = urllib.unquote_plus(video_url)
	elif 'redtube' in url: 
		try:
			video_url = re.compile('quality_720p=(.+?)=').findall(content)[0]   #720p
		except:
			video_url = re.compile('value="quality_.+?=(.+?)=').findall(content)[0]   #240p
		media_url = urllib.unquote_plus(video_url)
	elif '.porn.com' in url:
		media_url = re.compile('file:"(.+?)"').findall(content)[0]
	elif 'flyflv' in url:
		media_url = re.compile('fileUrl="(.+?)"').findall(content)[0]	
	elif 'vikiporn' in url:
		media_url = re.compile("video_url: '(.+?)'").findall(content)[0]
	elif 'xhamster' in url:
		media_url = re.compile('file="(.+?)"').findall(content)[0]
	elif 'tnaflix' in url:
		media_url = 'http:' + re.compile('href="([^"]*)" class="downloadButton">MP4 for Mobile<').findall(content)[0]	
	elif 'lubetube' in url: 
		media_url = re.compile('id="video-.+?" href="(.+?)"').findall(content)[0] 	
	elif 'ero-tik' in url:
		match = re.compile('src="http://videomega.tv/validatehash.php\?hashkey=(.+?)"').findall(content)[0]			
		req = urllib2.Request(v_erotik + 'cdn.php?ref=' + match)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
		req.add_header('Referer', v_erotik + '?ref=' + match)
		response = urllib2.urlopen(req)
		content = response.read()	
		response.close()        
		media_url = re.compile('<source src="(.+?)" type="video').findall(content)[0]
	elif 'yes.xxx' in url: 
		media_url = re.compile('<source type="video/mp4" src="(.+?)">').findall(content)[0]		
	elif 'pornxs' in url: 
		media_url = re.compile('config-final-url="(.+?)"').findall(content)[0]	
	elif 'zbporn' in url: 
		media_url = re.compile("video_url: '(.+?)'").findall(content)[0]	
	elif 'pornhd' in url: 
		try:
			media_url = re.compile("'480p'  : '(.+?)'").findall(content)[0]	
		except:
			media_url = re.compile("'240p'  : '(.+?)'").findall(content)[0]			
	else:
		media_url = url
	item = xbmcgui.ListItem(name, path = media_url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)	  
	return

def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring)>= 2:
		params = sys.argv[2]
		cleanedparams = params.replace('?', '')
		if (params[len(params)-1] == '/'):
			params = params[0:len(params)-2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0]] = splitparams[1]
	return param

def add_dir(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
	return ok

def add_link(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)	
	liz = xbmcgui.ListItem(name, iconImage = "DefaultVideo.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	liz.setProperty('IsPlayable', 'true')  
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz)  
	  
params = get_params()
url = None
name = None
mode = None
iconimage = None

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	name = urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode = int(params["mode"])
except:
	pass
try:
	iconimage = urllib.unquote_plus(params["iconimage"])
except:
	pass  

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)
print "iconimage: " + str(iconimage)

if mode == None or url == None or len(url) < 1:
	main()

elif mode == 1:
	search()

elif mode == 2:
	category(url)
  
elif mode == 3:
	media_list(url)
  
elif mode == 4:
	resolve_url(url) 

elif mode == 5:
	tube8_HD(url)

elif mode == 6:
	youjizz_HD(url)  
  
elif mode == 7:
	HD() 

elif mode == 8:
	porn4u() 

elif mode == 9:
	play_vid(url) 
  
elif mode == 10:
	redtube_channels_cat(url)

elif mode == 11:  
	redtube_channels_list(url)  

elif mode == 12:
	lubtetube_pornstars(url)
	
elif mode == 20:
	yess_xxx()

elif mode == 30:	
	search_result(url)

elif mode == 40:	
	zb_porn()

elif mode == 50:	
	porn_hd(url)
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
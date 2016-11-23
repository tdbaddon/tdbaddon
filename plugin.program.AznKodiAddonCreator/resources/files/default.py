# -*- coding: utf-8 -*-

"""
Copyright (C) 2015

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
"""

import urllib, urllib2, sys, re, os, unicodedata
import xbmc, xbmcgui, xbmcplugin, xbmcaddon

plugin_handle = int(sys.argv[1])

mysettings = xbmcaddon.Addon(id = 'plugin.video.MyNewlyCreatedAddon')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))

online_m3u = mysettings.getSetting('online_m3u')
local_m3u = mysettings.getSetting('local_m3u')
online_xml = mysettings.getSetting('online_xml')
local_xml = mysettings.getSetting('local_xml')

xml_regex = '<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>'
m3u_thumb_regex = 'tvg-logo=[\'"](.*?)[\'"]'
m3u_regex = '#(.+?),(.+)\s*(.+)\s*'

u_tube = 'http://www.youtube.com'

def removeAccents(s):
	return ''.join((c for c in unicodedata.normalize('NFD', s.decode('utf-8')) if unicodedata.category(c) != 'Mn'))
					
def read_file(file):
    try:
        f = open(file, 'r')
        content = f.read()
        f.close()
        return content
    except:
        pass

def make_request(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
		response = urllib2.urlopen(req)	  
		link = response.read()
		response.close()  
		return link
	except urllib2.URLError, e:
		print 'We failed to open "%s".' % url
		if hasattr(e, 'code'):
			print 'We failed with error code - %s.' % e.code	
		if hasattr(e, 'reason'):
			print 'We failed to reach a server.'
			print 'Reason: ', e.reason
			
def main():
	add_dir('[B]<<<  SEARCH  >>>[/B]', 'searchlink', 99, icon, fanart)
	if len(online_m3u) > 0:	
		add_dir('[COLOR yellow][B]>> ONLINE M3U <<[/B][/COLOR]', u_tube, 2, icon, fanart)
	if len(local_m3u) > 0:	
		add_dir('[COLOR magenta][B]>> LOCAL M3U <<[/B][/COLOR]', u_tube, 3, icon, fanart)
	if len(online_xml) > 0:	
		add_dir('[COLOR cyan][B]>> ONLINE XML <<[/B][/COLOR]', u_tube, 4, icon, fanart)
	if len(local_xml) > 0:	
		add_dir('[COLOR lime][B]>> LOCAL XML <<[/B][/COLOR]', u_tube, 5, icon, fanart)		
	if (len(online_m3u) < 1 and len(local_m3u) < 1 and len(online_xml) < 1 and len(local_xml) < 1 ):		
		mysettings.openSettings()
		xbmc.executebuiltin("Container.Refresh")		

def search(): 	
	try:
		keyb = xbmc.Keyboard('', 'Enter search text')
		keyb.doModal()
		if (keyb.isConfirmed()):
			searchText = urllib.quote_plus(keyb.getText()).replace('+', ' ')
		if len(online_m3u) > 0:		
			content = make_request(online_m3u)
			match = re.compile(m3u_regex).findall(content)
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
		if len(local_m3u) > 0:		
			content = read_file(local_m3u)
			match = re.compile(m3u_regex).findall(content)		
			for thumb, name, url in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					m3u_playlist(name, url, thumb)	
		if len(online_xml) > 0:					
			content = make_request(online_xml)
			match = re.compile(xml_regex).findall(content)	
			for name, url, thumb in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					xml_playlist(name, url, thumb)	
		if len(local_xml) > 0:		
			content = read_file(local_xml)
			match = re.compile(xml_regex).findall(content)		
			for name, url, thumb in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					xml_playlist(name, url, thumb)	
	except:
		pass
		
def m3u_online():		
	content = make_request(online_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass
			
def xml_online():			
	content = make_request(online_xml)
	match = re.compile(xml_regex).findall(content)
	for name, url, thumb in match:
		try:
			xml_playlist(name, url, thumb)
		except:
			pass
			
def m3u_local():
	content = read_file(local_m3u)
	match = re.compile(m3u_regex).findall(content)
	for thumb, name, url in match:	
		try:
			m3u_playlist(name, url, thumb)
		except:
			pass

def xml_local():		
	content = read_file(local_xml)
	match = re.compile(xml_regex).findall(content)
	for name, url, thumb in match:	
		try:
			xml_playlist(name, url, thumb)
		except:
			pass
				
def m3u_playlist(name, url, thumb):	
	name = re.sub('\s+', ' ', name).strip()			
	url = url.replace('"', ' ').replace('&amp;', '&').strip()
	if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
		if 'tvg-logo' in thumb:
			thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')			
			add_dir(name, url, '', thumb, thumb)			
		else:	
			add_dir(name, url, '', icon, fanart)
	else:
		if 'youtube.com/watch?v=' in url:
			url = 'plugin://plugin.video.youtube/play/?video_id=%s' % (url.split('=')[-1])
		elif 'dailymotion.com/video/' in url:
			url = url.split('/')[-1].split('_')[0]
			url = 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=%s' % url	
		else:			
			url = url
		if 'tvg-logo' in thumb:				
			thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
			add_link(name, url, 1, thumb, thumb)			
		else:				
			add_link(name, url, 1, icon, fanart)	
					
def xml_playlist(name, url, thumb):
	name = re.sub('\s+', ' ', name).strip()			
	url = url.replace('"', ' ').replace('&amp;', '&').strip()
	if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
		if len(thumb) > 0:	
			add_dir(name, url, '', thumb, thumb)			
		else:	
			add_dir(name, url, '', icon, fanart)
	else:
		if 'youtube.com/watch?v=' in url:
			url = 'plugin://plugin.video.youtube/play/?video_id=%s' % (url.split('=')[-1])
		elif 'dailymotion.com/video/' in url:
			url = url.split('/')[-1].split('_')[0]
			url = 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=%s' % url	
		else:			
			url = url
		if len(thumb) > 0:		
			add_link(name, url, 1, thumb, thumb)			
		else:			
			add_link(name, url, 1, icon, fanart)	
	
def play_video(url):
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
	if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
		u = 'plugin://plugin.video.youtube/%s/%s/' % (url.split( '/' )[-2], url.split( '/' )[-1])
		ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
		return ok		
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
	play_video(url)

elif mode == 2:
	m3u_online()
	
elif mode == 3:
	m3u_local()
	
elif mode == 4:
	xml_online()
	
elif mode == 5:
	xml_local()	

elif mode == 99:
	search()
	
xbmcplugin.endOfDirectory(plugin_handle)
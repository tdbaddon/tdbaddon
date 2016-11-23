# -*- coding: utf-8 -*-

'''
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
'''                                                                           

import urllib, urllib2, re, os, sys, shutil, zipfile
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

mysettings = xbmcaddon.Addon(id = 'plugin.program.AznKodiAddonCreator')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
logos = xbmc.translatePath(os.path.join(home, 'resources/logos/'))

addon_old_place = xbmc.translatePath(os.path.join(home, 'resources/files/addon.xml'))
default_old_place = xbmc.translatePath(os.path.join(home, 'resources/files/default.py'))
settings_old_place = xbmc.translatePath(os.path.join(home, 'resources/files/settings.xml'))
sample_m3u = xbmc.translatePath(os.path.join(home, 'resources/files/sample m3u.m3u'))
sample_xml = xbmc.translatePath(os.path.join(home, 'resources/files/sample xml.xml'))
license_txt = xbmc.translatePath(os.path.join(home, 'LICENSE.txt'))

name_of_plugin_folder = mysettings.getSetting('name_of_plugin_folder')
my_first_addon = xbmc.translatePath('special://home/addons/plugin.video.' + name_of_plugin_folder)
addon_new_place = xbmc.translatePath(os.path.join(my_first_addon, 'addon.xml'))
default_new_place = xbmc.translatePath(os.path.join(my_first_addon, 'default.py'))
settings_new_place = xbmc.translatePath(os.path.join(my_first_addon, 'resources/settings.xml'))
name_of_addon = mysettings.getSetting('name_of_addon')
addon_version_number = mysettings.getSetting('addon_version_number')
provider_name = mysettings.getSetting('provider-name')
addon_icon = mysettings.getSetting('addon_icon')
addon_fanart = mysettings.getSetting('addon_fanart')
sum_mary = mysettings.getSetting('sum_mary')
description = mysettings.getSetting('desc')
destination = mysettings.getSetting('dst')
online_m3u = mysettings.getSetting('online_m3u')
online_xml = mysettings.getSetting('online_xml')

target_zipfile = xbmc.translatePath('special://home/addons/packages/plugin.video.' + name_of_plugin_folder + '-' + addon_version_number + '.zip')
	
def read_file(file):
	try:
		f = open(file, 'r')
		content = f.read()
		f.close()
		return content	
	except:
		pass 
		
def home():
	add_dir(
				'Create add-on for [COLOR magenta]m3u/xml playlists[/COLOR] **[COLOR red][B] NO REGEX[/B][/COLOR] **', 
				'AddonCreator', 1, logos + 'kodi_xbmc.png', fanart
			)

def check_settings(): 
	if (	
			len(name_of_plugin_folder) > 0 and len(name_of_addon) > 0 and len(addon_version_number) > 0 and len(provider_name) > 0 and
			len(addon_icon) > 0 and len(addon_fanart) > 0 and len(sum_mary) > 0 and len(description) > 0
		):
			create_addon()
	else:	
		mysettings.openSettings()

def create_addon():
	try:
		# Delete the same old plug-in folder if exists and create new empty one.
		try:
			shutil.rmtree(my_first_addon)
		except:
			pass				
		os.makedirs(my_first_addon + '/resources')	
		
		# Copy default.py and replace the target string.
		shutil.copy(default_old_place, my_first_addon)
		default_py = None	
		default_py = read_file(default_new_place)
		default_py = default_py.replace('MyNewlyCreatedAddon', name_of_plugin_folder)	
		f = open(default_new_place, 'w')
		f.write(default_py)
		f.close()
		
		# Copy addon.xml and replace the target strings.		
		shutil.copy(addon_old_place, my_first_addon)
		addon_xml = None	
		addon_xml = read_file(addon_new_place)
		addon_xml = addon_xml.replace(
										'<addon id="" name="" version="" provider-name="">',
										'<addon id="plugin.video.' + name_of_plugin_folder + '" name="' + name_of_addon +
										'" version="' + addon_version_number + '" provider-name="' + provider_name + '">'
										).replace('<summary></summary>', '<summary>' + sum_mary + '</summary>'
										).replace('<description></description>', '<description>' + description + '</description>'
										).replace('\[', '[').replace('\]', ']'
									 )	
		f = open(addon_new_place, 'w')
		f.write(addon_xml)
		f.close()
		
		# Copy settings.xml and replace the target strings.	
		shutil.copy(settings_old_place, my_first_addon + '/resources')
		try:
			settings_xml = None	
			settings_xml = read_file(settings_new_place)
			if len(online_m3u) > 0 and len(online_xml) < 1:
				settings_xml = settings_xml.replace('id="online_m3u" default="" />', 'id="online_m3u" default="' + online_m3u + '" />')
			if len(online_xml) > 0 and len(online_m3u) < 1:	
				settings_xml = settings_xml.replace('id="online_xml" default="" />', 'id="online_xml" default="' + online_xml + '" />')
			if len(online_m3u) > 0 and len(online_xml) > 0:	
				settings_xml = settings_xml.replace(	
														'id="online_m3u" default="" />', 'id="online_m3u" default="' + online_m3u + '" />'
														).replace('id="online_xml" default="" />', 'id="online_xml" default="' + online_xml + '" />'
													)				
			f = open(settings_new_place, 'w')
			f.write(settings_xml)
			f.close()		
		except:
			pass
			
		# Create changelog.txt
		f = open(my_first_addon + '/changelog.txt', 'w')
		f.write('Version ' + addon_version_number)
		f.close()
		
		# Copy license.txt, sample links, icon.png, and fanart.jpg		
		shutil.copy(license_txt, my_first_addon)
		shutil.copy(sample_m3u, my_first_addon)
		shutil.copy(sample_xml, my_first_addon)		
		shutil.copy(addon_icon, my_first_addon)
		shutil.copy(addon_fanart, my_first_addon)	
		
		# make zipfile
		try:
			create_zipfile() 
		except:
			pass
			
		xbmcgui.Dialog().ok(
								'Add-on Creator', 
								'[COLOR red][B]Please manually reboot XBMC - KODI.[/B][/COLOR]', 
								'Look for new add-on in [B]VIDEOS > Add-ons.[/B]', 
								'[COLOR red][B]Next, check for zipfile if selected.[/B][/COLOR]'
							)
			
		# Delete same old zipfile in destination if exist AND then copy zipfile to chosen destination if selected
		if len(destination) > 0:
			try:
				os.remove(xbmc.translatePath(os.path.join(destination, 'plugin.video.' + name_of_plugin_folder + '.zip')))
			except:
				pass
			try:
				shutil.copy(target_zipfile, destination) 
				xbmcgui.Dialog().ok(
										'Add-on Creator', 
										'[COLOR red][B]Go to the chosen destination for addon zipfile.[/B][/COLOR]',
										'',
										'[B]Well Done. Enjoy![/B]', 
									)					
			except:
				xbmcgui.Dialog().ok(
										'Add-on Creator', 
										'[COLOR red][B]Oops! Unable to save addon zipfile.[/B][/COLOR]', 
										'', 
										'[B]Choose different destination. Get zipfile again.[/B]'
									)			
								
	except:	
		xbmcgui.Dialog().ok(
								'Add-on Creator', 
								'[COLOR red][B]Oops! Something has gone terribly wrong.[/B][/COLOR]', 
								'[B]Double check [COLOR red]ALL[/COLOR] settings.[/B]', 
								'Then try again.'
							)

def create_zipfile():
	os.chdir(xbmc.translatePath('special://home/addons'))
	src_dir = 'plugin.video.' + name_of_plugin_folder	
	#target_zipfile
	zf = zipfile.ZipFile(target_zipfile, 'w')
	for dirname, subdirs, files in os.walk(src_dir):
		zf.write(dirname)
		for filename in files:
			zf.write(os.path.join(dirname, filename))
	zf.close()	

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
	u = (	
			sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + 
			"&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
		)	
	ok = True
	liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
	return ok

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

if mode == None or url == None or len(url)<1:
	home()

elif mode == 1:
	check_settings()
	sys.exit(0)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
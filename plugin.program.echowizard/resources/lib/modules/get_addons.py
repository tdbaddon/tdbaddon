"""
    Copyright (C) 2016 ECHO Wizard

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys,xbmcvfs
import shutil
import base64
import re
import shutil
import time
from resources.lib.modules import common as Common
from resources.lib.modules import downloader
import zipfile
import urllib,urllib2

dialog           = xbmcgui.Dialog()
dp               =  xbmcgui.DialogProgress()
AddonTitle       ="[COLOR yellowgreen]ECHO[/COLOR] [COLOR white]Wizard[/COLOR]"
addon_id         = 'plugin.program.echowizard'
FANART           = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'fanart.jpg'))
ICON             = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/installer.png'))
XXX_ICON         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/installer.png'))
VIDEO_ICON       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/installer.png'))
TOP_ICON         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/installer.png'))
SUPPORT_ICON     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/installer.png'))
PROGRAM_ICON     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/installer.png'))
PICTURE_ICON     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/installer.png'))
PC_ICON          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/installer.png'))
PAID_ICON        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/installer.png'))
PACKS_ICON       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/installer.png'))
MUSIC_ICON       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/installer.png'))
DEP_ICON         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/installer.png'))
ALL_ICON         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/installer.png'))
UPDATE_ICON      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/installer.png'))
REPO_ICON        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/installer.png'))
ADDON_DATA       = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id, 'packs/'))
PARENTAL_FILE    = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id , 'controls.txt'))
PARENTAL_FOLDER  = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id))
BASEURL          = base64.b64decode(b'aHR0cDovL2VjaG9jb2Rlci5jb20v')
ADDON_LIST       = BASEURL + base64.b64decode(b'YWRkb25zL2FkZG9uX2xpc3RfbmV3LnhtbA==')
ADDON_LIST_PAID  = BASEURL + base64.b64decode(b'YWRkb25zL2FkZG9uX2xpc3RfcGFpZC54bWw=')
DEPENDENCIES     = BASEURL + base64.b64decode(b'YWRkb25zL2RlcGVuZGVuY2llc19saXN0LnhtbA==')
REPO_LIST        = BASEURL + base64.b64decode(b'YWRkb25zL3JlcG9zLnhtbA==')
PASSWD           = BASEURL + base64.b64decode(b'b3RoZXIvYWR1bHRwYXNzLnR4dA==')
PACKS_LIST       = BASEURL + base64.b64decode(b'YWRkb25zL2FkZG9uX3BhY2tzLnhtbA==')
SOURCES_URL      = BASEURL + base64.b64decode(b'YWRkb25zL3NvdXJjZXMueG1s')
DEP_LIST         = BASEURL + base64.b64decode(b'YWRkb25zL2RlcHMueG1s')
PAID_DESC        = BASEURL + base64.b64decode(b'YWRkb25zL3BhaWRfZGVzY3JpcHRpb25zLw==')
DESC             = BASEURL + base64.b64decode(b'YWRkb25zL2Rlc2NyaXB0aW9ucy8=')
USER_AGENT       = base64.b64decode(b'VGhlV2l6YXJkSXNIZXJl')

def MENU():

	xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
	version=float(xbmc_version[:4])
	codename = "Decline"

	total = ""
	total_count = Common.count_addons_week(total)
	Common.addDir("[COLOR white][B]" + str(total_count) + " [/COLOR][COLOR yellowgreen]Addons Downloaded This Week[/B][/COLOR]",BASEURL,121,ALL_ICON,FANART,description='all')
	Common.addDir("[COLOR yellowgreen][B]############################################################################[/B][/COLOR]",BASEURL,121,ALL_ICON,FANART,description='all')
	
	Common.addDir("[COLOR dodgerblue][B]UPDATE INSTALLED ADDONS[/B][/COLOR]",BASEURL,174,ALL_ICON,FANART,'')
	Common.addDir("[COLOR white][B]ENTER THE ECHO ADDON INSTALLER[/B][/COLOR]",BASEURL,175,ALL_ICON,FANART,'')

def MENU_MAIN():

	if os.path.exists(PARENTAL_FILE):
		vq = Common._get_keyboard( heading="Please Enter Your Password" )
		if ( not vq ): 
			dialog.ok(AddonTitle,"Sorry, no password was entered.")
			quit()
		pass_one = vq

		vers = open(PARENTAL_FILE, "r")
		regex = re.compile(r'<password>(.+?)</password>')
		for line in vers:
			file = regex.findall(line)
			for current_pin in file:
				password = base64.b64decode(current_pin)
				if not password == pass_one:
					dialog.ok(AddonTitle,"Sorry, the password you entered was incorrect.")
					quit()

	total = ""
	total_count = Common.count_addons_week(total)
	Common.addDir("[COLOR yellowgreen][B]" + str(total_count) + " Addons Downloaded This Week[/B][/COLOR]",BASEURL,121,ALL_ICON,FANART,description='all')
	Common.addDir("[COLOR yellowgreen][B]############################################################################[/B][/COLOR]",BASEURL,121,ALL_ICON,FANART,description='all')
	Common.addDir("[COLOR white][B]All Addons[/B][/COLOR]",BASEURL,150,ALL_ICON,FANART,description='all')
	Common.addDir("[COLOR white][B]Repositories[/B][/COLOR]",BASEURL,150,REPO_ICON,FANART,description='repos')
	Common.addDir("[COLOR white][B]File Manager Sources[/B][/COLOR]",BASEURL,177,REPO_ICON,FANART,description='')
	Common.addDir("[COLOR white][B]Top 14 downloaded addons this week[/B][/COLOR]",BASEURL,150,TOP_ICON,FANART,description='top')
	Common.addDir("[COLOR white][B]APK Addons[/B][/COLOR]",BASEURL,170,XXX_ICON,FANART,description='Null')
	Common.addDir("[COLOR white][B]Video Addons[/B][/COLOR]",BASEURL,150,VIDEO_ICON,FANART,description='video')
	Common.addDir("[COLOR white][B]Program Addons[/B][/COLOR]",BASEURL,150,PROGRAM_ICON,FANART,description='program')
	Common.addDir("[COLOR white][B]Music Addons[/B][/COLOR]",BASEURL,150,MUSIC_ICON,FANART,description='audio')
	Common.addDir("[COLOR white][B]Picture Addons[/B][/COLOR]",BASEURL,150,PICTURE_ICON,FANART,description='image')
	Common.addDir("[COLOR white][B]Adult (XXX) Addons[/B][/COLOR]",BASEURL,150,XXX_ICON,FANART,description='xxx')
	Common.addDir("[COLOR yellowgreen][B][I]Subscription Based Services (e.g IPTV,VPN,TV GUIDES).[/I][/B][/COLOR]",BASEURL,150,PAID_ICON,FANART,description='paid')
	Common.addDir("[COLOR dodgerblue][B]Report A Broken Addon[/B][/COLOR]",BASEURL,152,SUPPORT_ICON,FANART,'')
	Common.addDir("[COLOR dodgerblue][B]How To Get an Addon Added[/B][/COLOR]",BASEURL,153,SUPPORT_ICON,FANART,'')

	if not os.path.exists(PARENTAL_FILE):
		Common.addDir("[COLOR orangered][B]PARENTAL CONTROLS - [COLOR red]OFF[/COLOR][/B][/COLOR]","url",159,PC_ICON,FANART,'')
	else:
		Common.addDir("[COLOR orangered][B]PARENTAL CONTROLS - [COLOR yellowgreen]ON[/COLOR][/B][/COLOR]","url",159,PC_ICON,FANART,'')

	kodi_name = Common.GET_KODI_VERSION()

	if kodi_name == "Jarvis":
		xbmc.executebuiltin("Container.SetViewMode(50)")
	elif kodi_name == "Krypton":
		xbmc.executebuiltin("Container.SetViewMode(55)")
	else: xbmc.executebuiltin("Container.SetViewMode(50)")

def GET_LIST(description):

	matcher = description
	
	SOURCES     =  xbmc.translatePath(os.path.join('special://home/userdata','sources.xml'))
	i = 0
	a = 0
	b = 0
	if not os.path.isfile(SOURCES):
		f = open(SOURCES,'w')
		f.write('<sources>\n    <files>\n        <default pathversion="1"></default>\n    </files>\n</sources>')
		f.close()

	dp.create(AddonTitle,"[COLOR blue]We are getting the addons from our server.[/COLOR]",'','')	

	if matcher == "repos":
		namelist=[]
		countlist=[]
		iconlist=[]
		fanartlist=[]
		repolist=[]
		url = REPO_LIST
		link = open_url(url)
		dp.update(0)
		match= re.compile('<item>(.+?)</item>').findall(link)
		dis_links = len(match)
		for item in sorted(match):
			links=re.compile('<link>(.+?)</link>').findall(item)
			i = i + 1
			dis_count = str(i)
			progress = 100 * int(i)/int(dis_links)
			name=re.compile('<title>(.+?)</title>').findall(item)[0]
			repo_path=re.compile('<repo_path>(.+?)</repo_path>').findall(item)[0]
			iconimage=re.compile('<iconimage>(.+?)</iconimage>').findall(item)[0]
			fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]     
			dp.update(progress,"Filtering repositories " + str(dis_count) + " of " + str(dis_links),"[COLOR grey][B]Found " + name + "[/B][/COLOR]")
			namelist.append(name)
			countlist.append(str(Common.count_addons_week(name)))
			iconlist.append(iconimage)
			fanartlist.append(fanart)
			repolist.append(repo_path)
			combinedlists = list(zip(countlist,namelist,iconlist,fanartlist,repolist))
		tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
		for count,name,iconimage,fanart,repo_path in tup:
			REPO   =  xbmc.translatePath(os.path.join('special://home/addons',repo_path))
			url2 = repo_path + "," + name  + "," + url
			try:
				bname = " | [COLOR white] This Week:[/COLOR][COLOR lightskyblue][B] " + count + "[/B][/COLOR]"
			except:
				bname = "Unknown"
			if not os.path.exists(REPO):
				Common.addDir("[COLOR white][B]" + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
			else:
				Common.addDir("[COLOR lightskyblue][B]" + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')

	elif matcher == "top":
		namelist=[]
		countlist=[]
		iconlist=[]
		fanartlist=[]
		addonlist=[]
		repolist=[]
		found_one = 0
		url = ADDON_LIST
		url2 = ADDON_LIST
		link = open_url(url)
		dp.update(0)
		match= re.compile('<item>(.+?)</item>').findall(link)
		dis_links = len(match)	
		for item in sorted(match):
			if '<link>' in item:
				links=re.compile('<link>(.+?)</link>').findall(item)
				i = i + 1
				dis_count = str(i)
				progress = 100 * int(i)/int(dis_links)
				if len(links)>1:
					name=re.compile('<title>(.+?)</title>').findall(item)[0]
					dp.update(progress,"Filtering addon " + str(dis_count) + " of " + str(dis_links),"[COLOR grey][B]Found " + name + "[/B][/COLOR]")
					addon_path=re.compile('<addon_path>(.+?)</addon_path>').findall(item)[0]
					repo_path=re.compile('<repo_path>(.+?)</repo_path>').findall(item)[0]
					iconimage=re.compile('<iconimage>(.+?)</iconimage>').findall(item)[0]
					fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]     
					namelist.append(name)
					countlist.append(str(Common.count_addons_week(name)))
					iconlist.append(iconimage)
					fanartlist.append(fanart)
					addonlist.append(addon_path)
					repolist.append(repo_path)
					combinedlists = list(zip(countlist,namelist,iconlist,fanartlist,addonlist,repolist))
		tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
		check = 1
		for count,name,iconimage,fanart,addon_path,repo_path in tup:
			ADDON  =  xbmc.translatePath(os.path.join('special://home/addons',addon_path))
			REPO   =  xbmc.translatePath(os.path.join('special://home/addons',repo_path))
			url2 = addon_path + "," + repo_path + "," + name  + "," + url
			if check < 14:
				if check == 1:
					bname = " | [COLOR gold][B] This Week:[/COLOR][COLOR gold] " + count + "[/B][/COLOR]"
					if not os.path.exists(ADDON):
						Common.addDir("[COLOR gold][B]1st - " + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
					else:
						Common.addDir("[COLOR gold][B]1st - " + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
				elif check == 2:
					bname = " | [COLOR ghostwhite][B] This Week:[/COLOR][COLOR ghostwhite] " + count + "[/B][/COLOR]"
					if not os.path.exists(ADDON):
						Common.addDir("[COLOR ghostwhite][B]2nd - " + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
					else:
						Common.addDir("[COLOR ghostwhite][B]2nd - " + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
				elif check == 3:
					bname = " | [COLOR orange][B] This Week:[/COLOR][COLOR gold] " + count + "[/B][/COLOR]"
					if not os.path.exists(ADDON):
						Common.addDir("[COLOR orange][B]3rd - " + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
						Common.addItem("[COLOR grey]----------------------------------[/COLOR]",url2,999,iconimage,fanart,'')
					else:
						Common.addDir("[COLOR orange][B]3rd - " + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
						Common.addItem("[COLOR grey]----------------------------------[/COLOR]",url2,999,iconimage,fanart,'')
				else:
					bname = " | [COLOR grey] This Week:[/COLOR][COLOR lightskyblue][B] " + count + "[/B][/COLOR]"
					if not os.path.exists(ADDON):
						Common.addDir("[COLOR grey][B]" + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
					else:
						Common.addDir("[COLOR lightskyblue][B]" + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
			check = check + 1
	elif matcher == "paid":
		namelist=[]
		countlist=[]
		iconlist=[]
		fanartlist=[]
		addonlist=[]
		repolist=[]
		url = ADDON_LIST_PAID
		url2 = ADDON_LIST_PAID
		link = open_url(url)
		dp.update(0)
		match= re.compile('<item>(.+?)</item>').findall(link)
		dis_links = len(match)	
		for item in sorted(match):
			if '<link>' in item:
				links=re.compile('<link>(.+?)</link>').findall(item)
				i = i + 1
				dis_count = str(i)
				progress = 100 * int(i)/int(dis_links)
				if len(links)>1:
					name=re.compile('<title>(.+?)</title>').findall(item)[0]
					dp.update(progress,"Filtering addon " + str(dis_count) + " of " + str(dis_links),"[COLOR grey][B]Found " + name + "[/B][/COLOR]")
					addon_path=re.compile('<addon_path>(.+?)</addon_path>').findall(item)[0]
					repo_path=re.compile('<repo_path>(.+?)</repo_path>').findall(item)[0]
					iconimage=re.compile('<iconimage>(.+?)</iconimage>').findall(item)[0]
					fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]     
					namelist.append(name)
					countlist.append(str(Common.count_addons_week(name)))
					iconlist.append(iconimage)
					fanartlist.append(fanart)
					addonlist.append(addon_path)
					repolist.append(repo_path)
					combinedlists = list(zip(countlist,namelist,iconlist,fanartlist,addonlist,repolist))
		tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
		for count,name,iconimage,fanart,addon_path,repo_path in tup:
			ADDON  =  xbmc.translatePath(os.path.join('special://home/addons',addon_path))
			REPO   =  xbmc.translatePath(os.path.join('special://home/addons',repo_path))
			url2 = addon_path + "," + repo_path + "," + name  + "," + url
			try:
				bname = " | [COLOR white] This Week:[/COLOR][COLOR lightskyblue][B] " + count + "[/B][/COLOR]"
			except:
				bname = "Unknown"
			if not os.path.exists(ADDON):
				Common.addDir("[COLOR white][B]" + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2+",paid",176,iconimage,fanart,'')
			else:
				Common.addDir("[COLOR lightskyblue][B]" + name + " - INSTALLED[/B][/COLOR]" + bname,url2+",paid",176,iconimage,fanart,'')
	else:
		url = ADDON_LIST
		url2 = ADDON_LIST
		link = open_url(url)
		dp.update(0)
		match= re.compile('<item>(.+?)</item>').findall(link)
		dis_links = len(match)
		namelist=[]
		countlist=[]
		iconlist=[]
		fanartlist=[]
		addonlist=[]
		repolist=[]
		for item in match:
			if '<link>' in item:
				links=re.compile('<link>(.+?)</link>').findall(item)
				i = i + 1
				dis_count = str(i)
				progress = 100 * int(i)/int(dis_links)
				if len(links)>1:
					name=re.compile('<title>(.+?)</title>').findall(item)[0]
					dp.update(progress,"Filtering addon " + str(dis_count) + " of " + str(dis_links),"[COLOR grey][B]Found " + name + "[/B][/COLOR]")
					addon_path=re.compile('<addon_path>(.+?)</addon_path>').findall(item)[0]
					repo_path=re.compile('<repo_path>(.+?)</repo_path>').findall(item)[0]
					iconimage=re.compile('<iconimage>(.+?)</iconimage>').findall(item)[0]
					fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]     
					namelist.append(name)
					countlist.append(str(Common.count_addons_week(name)))
					iconlist.append(iconimage)
					fanartlist.append(fanart)
					addonlist.append(addon_path)
					repolist.append(repo_path)
					combinedlists = list(zip(countlist,namelist,iconlist,fanartlist,addonlist,repolist))
		tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
		for count,name,iconimage,fanart,addon_path,repo_path in tup:
			ADDON  =  xbmc.translatePath(os.path.join('special://home/addons',addon_path))
			REPO   =  xbmc.translatePath(os.path.join('special://home/addons',repo_path))
			url2 = addon_path + "," + repo_path + "," + name  + "," + url
			base_name = name
			try:
				bname = " | [COLOR white] This Week:[/COLOR][COLOR lightskyblue][B] " + count + "[/B][/COLOR]"
			except:
				bname = "Unknown"
			if matcher == "xxx":
				if matcher in name.lower():
					if not os.path.exists(ADDON):
						Common.addDir("[COLOR white][B]" + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
					else:
						Common.addDir("[COLOR lightskyblue][B]" + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')

			elif matcher != "all":
				if matcher in addon_path:
					if not os.path.exists(ADDON):
							Common.addDir("[COLOR white][B]" + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
					else:
							Common.addDir("[COLOR lightskyblue][B]" + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
			else:
				if not os.path.exists(ADDON):
					Common.addDir("[COLOR white][B]" + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
				else:
					Common.addDir("[COLOR lightskyblue][B]" + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')

	kodi_name = Common.GET_KODI_VERSION()

	if kodi_name == "Jarvis":
		xbmc.executebuiltin("Container.SetViewMode(50)")
	elif kodi_name == "Krypton":
		xbmc.executebuiltin("Container.SetViewMode(55)")
	else: xbmc.executebuiltin("Container.SetViewMode(50)")

def ADDON_DECIDE(name,url):

	urla  = url
	paid_mark = "null"
	try:
		addon_path,repo_path,base_name,url,paid_mark   = urla.split(',')
	except:
		try:
			addon_path,repo_path,base_name,url   = urla.split(',')
		except: repo_path,base_name,url   = urla.split(',')
	
	try:
		ADDON  =  xbmc.translatePath(os.path.join('special://home/addons',addon_path))
		if not os.path.exists(ADDON):
			Common.addItem("[COLOR white][B]Install Addon[/B][/COLOR]",urla+",install_me",151,ICON,FANART,'')
		else:
			Common.addItem("[COLOR white][B]Uninstall Addon[/B][/COLOR]",urla+",uninstall_me",151,ICON,FANART,'')
		if paid_mark == "paid":
			Common.addItem("[COLOR white][B]Addon Information[/B][/COLOR]",urla+",paid_info",151,ICON,FANART,'')
		else:
			Common.addItem("[COLOR white][B]Addon Information[/B][/COLOR]",urla+",info_me",151,ICON,FANART,'')
		Common.addDir("[COLOR white][B]Read Addon Reviews[/B][/COLOR]",urla+",readreview_me",151,ICON,FANART,'')
		Common.addItem("[COLOR white][B]Leave Review[/B][/COLOR]",urla+",leavereview_me",151,ICON,FANART,'')
	except:
		ADDON  =  xbmc.translatePath(os.path.join('special://home/addons',repo_path))
		if not os.path.exists(ADDON):
			Common.addItem("[COLOR white][B]Install Repository[/B][/COLOR]",urla+",install_me",164,ICON,FANART,'')
		else:
			Common.addItem("[COLOR white][B]Uninstall Repository[/B][/COLOR]",urla+",uninstall_me",164,ICON,FANART,'')
		Common.addItem("[COLOR white][B]Repository Information[/B][/COLOR]",urla+",info_me",164,ICON,FANART,'')
		Common.addDir("[COLOR white][B]Read Repository Reviews[/B][/COLOR]",urla+",readreview_me",164,ICON,FANART,'')
		Common.addItem("[COLOR white][B]Leave Review[/B][/COLOR]",urla+",leavereview_me",164,ICON,FANART,'')

def GET_MULTI(name,url):
	
	kodi_name = Common.GET_KODI_VERSION()
	urla  = url
	try:
		addon_path,repo_path,base_name,url,marker   = urla.split(',')
	except: addon_path,repo_path,base_name,url,disre,marker   = urla.split(',')
	get_url = url
	service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9hZGRvbl9yZXZpZXcucGhwP2FjdGlvbj1jb3VudCZidWlsZD0=') + base64.b64encode(addon_path)
	body = urllib2.urlopen(service_url).read()

	ADDON  =  xbmc.translatePath(os.path.join('special://home/addons',addon_path))

	if marker == "info_me":
		url = DESC + addon_path + ".txt"
		content = open_url_desc(url)
		string = str(content)
		if string == "None":
			dialog.ok(AddonTitle,"Sorry, there was an error getting the requested information.")
		TextBoxes("%s" % string)
	elif marker == "paid_info":
		url = PAID_DESC + addon_path + ".txt"
		content = open_url_desc(url)
		string = str(content)
		if string == "None":
			dialog.ok(AddonTitle,"Sorry, there was an error getting the requested information.")
		TextBoxes("%s" % string)
	elif marker == "readreview_me":
		Common.List_Addon_Review(addon_path)
	elif marker == "leavereview_me":
		Common.Write_Addon_Review(addon_path)
	elif marker == "uninstall_me":
		dp.create(AddonTitle,"[COLOR blue]Removing addon....[/COLOR]",'[COLOR yellow]Please Wait...[/COLOR]',' ')	
		dp.update(0,'','',' ')
		try:
			shutil.rmtree(ADDON)
			shutil.rmtree(REPO)
		except: pass
		if kodi_name == "Krypton":
			DISABLE_DATABASE_ADDON(addon_path)
		time.sleep(2)
		xbmc.executebuiltin("UpdateLocalAddons")
		time.sleep(2)
		xbmc.executebuiltin("UpdateAddonRepos")
		time.sleep(2)
		dp.close()
		dialog.ok(AddonTitle,"[COLOR white]" + base_name + " has been successfully removed from your system![/COLOR]")
		xbmc.executebuiltin("Container.Refresh")
	elif marker == "install_me":
		get_dep = 1
		get_addon = 1
		if get_dep == 1:
			try:
				streamurl=[]
				streamname=[]
				streamicon=[]
				link=open_url(DEPENDENCIES)
				urls=re.compile('<title>'+re.escape("Dependencies")+'</title>(.+?)</item>',re.DOTALL).findall(link)[0]
				iconimage=re.compile('<iconimage>(.+?)</iconimage>').findall(urls)[0]
				links=re.compile('<link>(.+?)</link>').findall(urls)
				i=1
				for sturl in links:
					sturl2=sturl
					if '(' in sturl:
						sturl=sturl.split('(')[0]
						caption=str(sturl2.split('(')[1].replace(')',''))
						streamurl.append(sturl)
						streamname.append(caption)
						ADDON  =  xbmc.translatePath(os.path.join('special://home/addons/',str(caption)))
						if not os.path.exists(ADDON):
							url = str(sturl)
							install_name = str("[COLOR lightskyblue][B]" + caption + "[/B][/COLOR]")
							INSTALL(install_name,url)
							if kodi_name == "Krypton":
								ADD_DATABASE_ADDON(caption,"")
						i=i+1
			except: pass
		if get_addon == 1:
			streamurl=[]
			streamname=[]
			streamicon=[]
			link=open_url(get_url)
			urls=re.compile('<title>'+re.escape(base_name)+'</title>(.+?)</item>',re.DOTALL).findall(link)[0]
			links=re.compile('<link>(.+?)</link>').findall(urls)
			iconimage=re.compile('<iconimage>(.+?)</iconimage>').findall(urls)[0]
			i=1
			for sturl in links:
				try:
					sturl2=sturl
					if '(' in sturl:
						sturl=sturl.split('(')[0]
						caption=str(sturl2.split('(')[1].replace(')',''))
						streamurl.append(sturl)
						streamname.append(caption)
						ADDON2  =  xbmc.translatePath(os.path.join('special://home/addons/',str(caption)))
						if not "http" in caption:
							if not os.path.exists(ADDON2):
								url = str(sturl)
								install_name = str("[COLOR lightskyblue][B]" + caption + "[/B][/COLOR]")
								INSTALL(install_name,url)
								if kodi_name == "Krypton":
									if "repo" in caption.lower():
										ADD_DATABASE_ADDON(repo_path,"")
										ADD_DATABASE_REPO(repo_path)
									else:
										ADD_DATABASE_ADDON(str(caption),repo_path)
								i=i+1
				except:
					try:
						shutil.rmtree(ADDON)
						shutil.rmtree(REPO)
					except: pass
					time.sleep(2)
					xbmc.executebuiltin("UpdateLocalAddons")
					time.sleep(2)
					xbmc.executebuiltin("UpdateAddonRepos")
					time.sleep(2)
					dialog.ok(AddonTitle,"There was an error installing " + install_name + " please report this to @EchoCoder on Twitter")
					xbmc.executebuiltin("Container.Refresh")
					quit()	
		dp.create(AddonTitle,"[COLOR blue]Adding the download to the counters[/COLOR]",'[COLOR yellow]Please Wait...[/COLOR]',' ')	
		dp.update(0,'','',' ')
		add_download = Common.add_one_addons_week(base_name)
		dp.update(50,'Refreshing kodi addons to finish the installation process.','',' ')
		time.sleep(2)
		xbmc.executebuiltin("UpdateLocalAddons")
		time.sleep(2)
		xbmc.executebuiltin("UpdateAddonRepos")
		time.sleep(2)
		xbmc.executebuiltin("Container.Refresh")
		dp.close

		xbmcgui.Dialog().ok(AddonTitle, "[COLOR white]" + base_name + " successfully installed![/COLOR]")

def GET_REPO(name,url):
	
	kodi_name = Common.GET_KODI_VERSION()

	urla  = url
	repo_path,base_name,url,marker   = urla.split(',')
	get_url = url

	service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9hZGRvbl9yZXZpZXcucGhwP2FjdGlvbj1jb3VudCZidWlsZD0=') + base64.b64encode(repo_path)
	body = urllib2.urlopen(service_url).read()

	REPO  =  xbmc.translatePath(os.path.join('special://home/addons',repo_path))

	if marker == "info_me":
		url = DESC + repo_path + ".txt"
		content = open_url_desc(url)
		string = str(content)
		if string == "None":
			dialog.ok(AddonTitle,"Sorry, there was an error getting the requested information.")
			quit()
		TextBoxes("%s" % string)
	elif marker == "readreview_me":
		Common.List_Addon_Review(repo_path)
	elif marker == "leavereview_me":
		Common.Write_Addon_Review(repo_path)
	elif marker == "uninstall_me":
		dp.create(AddonTitle,"[COLOR blue]Removing addon....[/COLOR]",'[COLOR yellow]Please Wait...[/COLOR]',' ')	
		dp.update(0,'','',' ')
		try:
			shutil.rmtree(REPO)
		except: pass
		if kodi_name == "Krypton":
			DISABLE_DATABASE_ADDON(repo_path)
		time.sleep(2)
		xbmc.executebuiltin("UpdateLocalAddons")
		time.sleep(2)
		xbmc.executebuiltin("UpdateAddonRepos")
		time.sleep(2)
		dp.close()
		dialog.ok(AddonTitle,"[COLOR white]" + base_name + " has been successfully removed from your system![/COLOR]")
		xbmc.executebuiltin("Container.Refresh")

	elif marker == "install_me":
		streamurl=[]
		streamname=[]
		streamicon=[]
		link=open_url(get_url)
		urls=re.compile('<title>'+re.escape(base_name)+'</title>(.+?)</item>',re.DOTALL).findall(link)[0]
		links=re.compile('<link>(.+?)</link>').findall(urls)
		iconimage=re.compile('<iconimage>(.+?)</iconimage>').findall(urls)[0]
		i=1
		for sturl in links:
			try:
				sturl2=sturl
				if '(' in sturl:
					sturl=sturl.split('(')[0]
					caption=str(sturl2.split('(')[1].replace(')',''))
					streamurl.append(sturl)
					streamname.append(caption)
					REPO  =  xbmc.translatePath(os.path.join('special://home/addons/',str(caption)))
					if not "http" in caption:
						if not os.path.exists(REPO):
							url = str(sturl)
							install_name = str("[COLOR lightskyblue][B]" + caption + "[/B][/COLOR]")
							INSTALL(install_name,url)
							if kodi_name == "Krypton":
								ADD_DATABASE_ADDON(repo_path,"")
								ADD_DATABASE_REPO(repo_path)
					i=i+1
			except:
				time.sleep(2)
				xbmc.executebuiltin("UpdateLocalAddons")
				time.sleep(2)
				xbmc.executebuiltin("UpdateAddonRepos")
				time.sleep(2)
				dialog.ok(AddonTitle,"There was an error installing " + install_name + " please report this to @EchoCoder on Twitter")
				xbmc.executebuiltin("Container.Refresh")
				quit()	
		dp.create(AddonTitle,"[COLOR blue]Adding the download to the counters[/COLOR]",'[COLOR yellow]Please Wait...[/COLOR]',' ')	
		dp.update(0,'','',' ')
		add_download = Common.add_one_addons_week(base_name)

		time.sleep(2)
		xbmc.executebuiltin("UpdateLocalAddons")
		time.sleep(2)
		xbmc.executebuiltin("UpdateAddonRepos")
		time.sleep(2)
		xbmc.executebuiltin("Container.Refresh")

		dp.close()

		xbmcgui.Dialog().ok(AddonTitle, "[COLOR white]" + base_name + " successfully installed![/COLOR]")

def FILE_MANAGER_SOURCES(name,url,description):
	
	SOURCES     =  xbmc.translatePath(os.path.join('special://home/userdata','sources.xml'))

	if not os.path.isfile(SOURCES):
		f = open(SOURCES,'w')
		f.write('<sources>\n    <files>\n        <default pathversion="1"></default>\n    </files>\n</sources>')
		f.close()
	i=0
	link = open_url(SOURCES_URL)
	match= re.compile('<item>(.+?)</item>').findall(link)
	for item in match:

		title=re.compile('<title>(.+?)</title>').findall(item)[0]
		source=re.compile('<source>(.+?)</source>').findall(item)[0]
		
		if str(source) not in open(SOURCES).read():
			url = title + '|SPLIT|' + source
			Common.addItem('[COLOR white]' + title + 's Source[/COLOR]',url,178,ICON,FANART,"")
			i = i + 1
	
	if i == 0:
		Common.addItem('[COLOR white]All of the sources we have are already in your File Manager.[/COLOR]','url',999,ICON,FANART,"")

def WRITE_SOURCE_TO_FILE_MANAGER(name,url):

	SOURCES     =  xbmc.translatePath(os.path.join('special://home/userdata','sources.xml'))

	name,source = url.split('|SPLIT|')

	choice = xbmcgui.Dialog().yesno(AddonTitle, "[COLOR white]Write the following to your File Manager?[/COLOR]","[COLOR white]Name:[/COLOR][COLOR dodgerblue][B]" + name + "[/B][/COLOR]","[COLOR white]Source:[/COLOR][COLOR dodgerblue][B]" + source + "[/B][/COLOR]", yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
	if choice == 1:
		try:
			OLD = '<files>\n		<default pathversion="1"></default>'
			NEW = '<files>\n		<default pathversion="1"></default>\n		<source>\n			<name>'+name+'</name>\n			<path pathversion="1">'+source+'</path>\n			<allowsharing>true</allowsharing>\n		</source>'
			a=open(SOURCES).read()
			b=a.replace(OLD, NEW)
			f= open((SOURCES), mode='w')
			f.write(str(b))
			f.close()
		except:	
			dialog.ok(AddonTitle, '[COLOR white]Sorry, there was an error writing the source to the file manager.[/COLOR]')
			quit()
	else:
		quit()

	if not source in open(SOURCES).read():
		try:
			OLD = '<files>\n        <default pathversion="1"></default>'
			NEW = '<files>\n        <default pathversion="1"></default>\n		<source>\n			<name>'+name+'</name>\n			<path pathversion="1">'+source+'</path>\n			<allowsharing>true</allowsharing>\n		</source>'
			a=open(SOURCES).read()
			b=a.replace(OLD, NEW)
			f= open((SOURCES), mode='w')
			f.write(str(b))
			f.close()
		except:	
			dialog.ok(AddonTitle, '[COLOR white]Sorry, there was an error writing the source to the file manager.[/COLOR]')
			quit()
			
	if not source in open(SOURCES).read():
		dialog.ok(AddonTitle, '[COLOR white]Sorry, there was an error writing the source to the file manager.[/COLOR]')
		quit()
	
	xbmc.executebuiltin("RereshSources")

	dialog.ok(AddonTitle, '[COLOR white]The ' + name + ' source has been written to your File Manager.', '[COLOR red][B]The Source will NOT SHOW in the File Manager until Kodi has been restarted. [/B][/COLOR]', 'Thank you for using ECHO Wizard.[/COLOR]')

	xbmc.executebuiltin("Container.Refresh") 

def ADD_DATABASE_ADDON(name,url):

	Enabled = 1
	AddonID = name
	Origen = url

	import datetime
	installDate = str(datetime.datetime.now())[:-7]
 
	import sqlite3
	DB_Path = xbmc.translatePath(os.path.join('special://home/userdata/', 'Database/Addons26.db'))
 
	conn = sqlite3.connect(DB_Path)
	cursor = conn.cursor()
 
	try:
		q = """ INSERT INTO installed(addonID,enabled, installDate, origin) VALUES(?, ?, ?, ?) """
		cursor.execute(q, (str(AddonID), str(Enabled), str(installDate), str(Origen)))
		conn.commit()
	except:
		q = """ UPDATE installed SET enabled= ? WHERE addonID = ? """
		cursor.execute(q, (str(Enabled), str(AddonID)))
		conn.commit()
		pass
	
def ADD_DATABASE_REPO(name):

	try:
		Repo_Path = xbmc.translatePath(os.path.join('special://home/addons/', name + '/addon.xml'))
		a=open(Repo_Path).read()
		b=a.replace('\n',' ').replace('\r',' ')
		match=re.compile('version="(.+?)".+?<checksum>(.+?)</checksum>').findall(str(b))
		for version,checksum in match:
			checksum_id = open_url(checksum)
			AddonID = name
			version_id = version

		import datetime
		installDate = str(datetime.datetime.now())[:-7]
	
		import sqlite3
		DB_Path = xbmc.translatePath(os.path.join('special://home/userdata/', 'Database/Addons26.db'))
	 
		conn = sqlite3.connect(DB_Path)
		cursor = conn.cursor()
	 
		q = """ INSERT INTO repo(addonID,checksum, lastcheck, version) VALUES(?, ?, ?, ?) """
		cursor.execute(q, (str(AddonID), str(checksum_id), str(installDate), str(version_id)))
		conn.commit()
	except: pass
	
def DISABLE_DATABASE_ADDON(name):

	Enabled = 0
	AddonID = name

	import sqlite3
	DB_Path = xbmc.translatePath(os.path.join('special://home/userdata/', 'Database/Addons26.db'))
 
	conn = sqlite3.connect(DB_Path)
	cursor = conn.cursor()
 
	try:
		q = """ UPDATE installed SET enabled= ? WHERE addonID = ? """
		cursor.execute(q, (str(Enabled), str(AddonID)))
		conn.commit()
	except: pass

def INSTALL(name, url):

	#Check is the packages folder exists, if not create it.
	path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
	if not os.path.exists(path):
		os.makedirs(path)
	dp = xbmcgui.DialogProgress()
	if "repository" in url:
		dp.create(AddonTitle,"","Installing " + name,' ')
	else:
		dp.create(AddonTitle,"","Installing " + name,' ')

	lib=os.path.join(path, 'addon.zip')
	
	try:
		os.remove(lib)
	except:
		pass

	dialog = xbmcgui.Dialog()
	try:
		downloader.download(url, lib, dp)
	except:
		downloader.download(url, lib, dp)
	addonfolder = xbmc.translatePath(os.path.join('special://home','addons'))
	time.sleep(2)
	dp.update(0,"","Extracting Zip Please Wait"," ")
	unzip(lib,addonfolder,dp)
	time.sleep(1)
	try:
		os.remove(lib)
	except:
		pass

def unzip(_in, _out, dp):
	__in = zipfile.ZipFile(_in,  'r')
	
	nofiles = float(len(__in.infolist()))
	count   = 0
	
	try:
		for item in __in.infolist():
			count += 1
			update = (count / nofiles) * 100
			
			if dp.iscanceled():
				dialog = xbmcgui.Dialog()
				dialog.ok(AddonTitle, 'Extraction was cancelled.')
				
				sys.exit()
				dp.close()
			
			try:
				dp.update(int(update),'','','[COLOR dodgerblue][B]' + str(item.filename) + '[/B][/COLOR]')
				__in.extract(item, _out)
			
			except Exception, e:
				print str(e)

	except Exception, e:
		print str(e)
		return False
		
	return True 

def open_url(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', USER_AGENT)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		link=link.replace('\n','').replace('\r','').replace('<title></title>','<title>x</title>').replace('<link></link>','<link>x</link>').replace('<fanart></fanart>','<fanart>x</fanart>').replace('<thumbnail></thumbnail>','<thumbnail>x</thumbnail>').replace('<utube>','<link>https://www.youtube.com/watch?v=').replace('</utube>','</link>')#.replace('></','>x</')
		return link
	except: pass
	
def open_url_desc(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', USER_AGENT)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link
	except: pass

def PARENTAL_CONTROLS():

	found = 0
	if not os.path.exists(PARENTAL_FILE):
		found = 1
		Common.addDir("[COLOR blue][B]PARENTAL CONTROLS - [/COLOR][COLOR red]OFF[/B][/COLOR]","url",999,ICON,FANART,'')
		Common.addDir("[COLOR yellow][B]Setup Parental Password[/B][/COLOR]","url",160,ICON,FANART,'')
	else:
		vers = open(PARENTAL_FILE, "r")
		regex = re.compile(r'<password>(.+?)</password>')
		for line in vers:
			file = regex.findall(line)
			for current_pin in file:
				password = base64.b64decode(current_pin)
				found = 1
				Common.addDir("[COLOR blue][B]PARENTAL CONTROLS - [/COLOR][COLOR yellowgreen]ON[/B][/COLOR]","url",999,ICON,FANART,'')
				Common.addDir("[COLOR yellow][B]Current Password - [/COLOR][COLOR orangered]" + str(password) + "[/B][/COLOR]","url",999,ICON,FANART,'')
				Common.addDir("[COLOR yellowgreen][B]Change Password[/B][/COLOR]","url",160,ICON,FANART,'')
				Common.addDir("[COLOR red][B]Disable Password[/B][/COLOR]","url",161,ICON,FANART,'')

	if found == 0:
		Common.addDir("[COLOR blue][B]PARENTAL CONTROLS - [/COLOR][COLOR red]OFF[/B][/COLOR]","url",999,ICON,FANART,'')
		Common.addDir("[COLOR yellow][B]Setup Parental Password[/B][/COLOR]","url",160,ICON,FANART,'')

def PARENTAL_CONTROLS_PIN():

	vq = Common._get_keyboard( heading="Please Set Password" )
	if ( not vq ):
		dialog.ok(AddonTitle,"Sorry, no password was entered.")
		quit()
	pass_one = vq

	vq = Common._get_keyboard( heading="Please Confirm Your Password" )
	if ( not vq ):
		dialog.ok(AddonTitle,"Sorry, no password was entered.")
		quit()
	pass_two = vq
		
	if not os.path.exists(PARENTAL_FILE):
		if not os.path.exists(PARENTAL_FOLDER):
			os.makedirs(PARENTAL_FOLDER)
		open(PARENTAL_FILE, 'w')

		if pass_one == pass_two:
			writeme = base64.b64encode(pass_one)
			f = open(PARENTAL_FILE,'w')
			f.write('<password>'+str(writeme)+'</password>')
			f.close()
			dialog.ok(AddonTitle,'Your password has been set and parental controls have been enabled.')
			xbmc.executebuiltin("Container.Refresh")
		else:
			dialog.ok(AddonTitle,'The passwords do not match, please try again.')
			quit()
	else:
		os.remove(PARENTAL_FILE)
		
		if pass_one == pass_two:
			writeme = base64.b64encode(pass_one)
			f = open(PARENTAL_FILE,'w')
			f.write('<password>'+str(writeme)+'</password>')
			f.close()
			dialog.ok(AddonTitle,'Your password has been set and parental controls have been enabled.')
			xbmc.executebuiltin("Container.Refresh")
		else:
			dialog.ok(AddonTitle,'The passwords do not match, please try again.')
			quit()

def PARENTAL_CONTROLS_OFF():

	try:
		os.remove(PARENTAL_FILE)
		dialog.ok(AddonTitle,'Parental controls have been disabled.')
		xbmc.executebuiltin("Container.Refresh")
	except:
		dialog.ok(AddonTitle,'There was an error disabling the parental controls.')
		xbmc.executebuiltin("Container.Refresh")

def TextBoxes(announce):
	class TextBox():
		WINDOW=10147
		CONTROL_LABEL=1
		CONTROL_TEXTBOX=5
		def __init__(self,*args,**kwargs):
			xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
			self.win=xbmcgui.Window(self.WINDOW) # get window
			xbmc.sleep(500) # give window time to initialize
			self.setControls()
		def setControls(self):
			self.win.getControl(self.CONTROL_LABEL).setLabel('Information') # set heading
			try: f=open(announce); text=f.read()
			except: text=announce
			self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
			return
	TextBox()
	while xbmc.getCondVisibility('Window.IsVisible(10147)'):
		time.sleep(.5)
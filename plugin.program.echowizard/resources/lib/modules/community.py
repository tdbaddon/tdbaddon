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
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys
import urllib2,urllib
from resources.lib.modules import extract
from resources.lib.modules import downloader
import requests
from resources.lib.modules import protected_wizards
import re
from resources.lib.modules import plugintools
from resources.lib.modules import common as Common
from resources.lib.modules import installer

AddonData = xbmc.translatePath('special://userdata/addon_data')
addon_id = 'plugin.program.echowizard'
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
ADDON = xbmcaddon.Addon(id=addon_id)
dp               =  xbmcgui.DialogProgress()
AddonTitle="[COLOR yellowgreen]ECHO[/COLOR] [COLOR white]Wizard[/COLOR]"
MaintTitle="[COLOR yellowgreen]ECHO[/COLOR] [COLOR white]Maintenance Tools[/COLOR]"
BASEURL = base64.b64decode(b'aHR0cDovL2VjaG9jb2Rlci5jb20v')
key = base64.b64encode(plugintools.get_setting("beta"))
COMMUNITY_ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/community.png'))
Community_List = BASEURL + base64.b64decode(b"Y29tbXVuaXR5L3dpemFyZHMudHh0")
Protected_List = BASEURL + base64.b64decode(b"Y29tbXVuaXR5L3Byb3RlY3RlZC9wYWdl")
COM_NOTICE = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/community_notice.txt'))
SEARCH_ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/search.png'))
page_number = 1
dialog = xbmcgui.Dialog()

#######################################################################
#######################################################################
#						Community Builds
#######################################################################

def COMMUNITY():
	i=0
	dp.create(AddonTitle,"[COLOR blue]We are getting the list of developers from our server.[/COLOR]",'[COLOR yellow]Please Wait...[/COLOR]','')	
	dp.update(0)
	namelist=[]
	urllist=[]
	hiddenlist=[]
	countlist=[]
	deslist=[]
	iconlist=[]
	fanartlist=[]
	link = Common.OPEN_URL(Community_List).replace('\n','').replace('\r','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?rotected="(.+?)".+?mg="(.+?)".+?anart="(.+?)"').findall(link)
	dis_links = len(match)
	for name,url,hidden,iconimage,fanart in match:
		i = i + 1
		dis_count = str(i)
		progress = 100 * int(i)/int(dis_links)
		dp.update(progress,"Getting details of developer " + str(dis_count) + " of " + str(dis_links),'',"[COLOR white][B]FOUND - [/B] " + name + "[/COLOR]")
		developer = str(name.replace('[COLOR white][B]','').replace('[/B][/COLOR]','').replace('[/B][/COLOR]','').replace(' BUILDS',''))
		description = str(developer + "," + hidden)
		namelist.append(name)
		urllist.append(url)
		hiddenlist.append(hidden)
		countlist.append(str(Common.community_dev_week(developer)))   
		deslist.append(description)		
		iconlist.append(iconimage)
		fanartlist.append(fanart)
		combinedlists = list(zip(countlist,namelist,urllist,hiddenlist,deslist,iconlist,fanartlist))
	tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
	dp.close()
	rank = 1
	for count,name,url,hidden,description,iconimage,fanart in tup:
		developer = str(name.replace('[COLOR white][B]','').replace('[/B][/COLOR]','').replace('[/B][/COLOR]','').replace(' BUILDS',''))
		if hidden != "false":
			url = hidden + "," + url
			if rank == 1:
				bname = " | [COLOR gold] This Week:[/COLOR][COLOR gold] " + count + " - [COLOR red][PASSWORD PROTECTED][/COLOR][/B][/COLOR]"
				Common.addDir("[B][COLOR gold]1st - " + developer + "[/COLOR]"  + bname,url,93,iconimage,fanart,description)
				rank = rank + 1
			elif rank == 2:
				bname = " | [COLOR ghostwhite] This Week:[/COLOR][COLOR ghostwhite] " + count + " - [COLOR red][PASSWORD PROTECTED][/COLOR][/B][/COLOR]"
				Common.addDir("[B][COLOR ghostwhite]2nd - " + developer + "[/COLOR]"  + bname,url,93,iconimage,fanart,description)
				rank = rank + 1
			elif rank == 3:
				bname = " | [COLOR orange] This Week:[/COLOR][COLOR orange] " + count + " - [COLOR red][PASSWORD PROTECTED][/COLOR][/B][/COLOR]"
				Common.addDir("[B][COLOR orange]3rd - " + developer + "[/COLOR]"  + bname,url,93,iconimage,fanart,description)
				rank = rank + 1
				Common.addItem("[COLOR grey]-----------------------------------------------[/COLOR]",url,17,iconimage,fanart,description)
			else:
				bname = " | [COLOR grey] This Week:[/COLOR][COLOR grey][B] " + count + " - [COLOR red][PASSWORD PROTECTED][/COLOR][/B][/COLOR]"
				Common.addDir("[COLOR grey]" + developer + "[/COLOR]"  + bname,url,93,iconimage,fanart,description)
		else:
			if rank == 1:
				bname = " | [COLOR gold] This Week:[/COLOR][COLOR gold] " + count + "[/B][/COLOR]"
				Common.addDir("[B][COLOR gold]1st - " + developer + "[/COLOR]"  + bname,url,93,iconimage,fanart,description)
				rank = rank + 1
			elif rank == 2:
				bname = " | [COLOR ghostwhite] This Week:[/COLOR][COLOR ghostwhite] " + count + "[/B][/COLOR]"
				Common.addDir("[B][COLOR ghostwhite]2nd - " + developer + "[/COLOR]"  + bname,url,93,iconimage,fanart,description)
				rank = rank + 1
			elif rank == 3:
				bname = " | [COLOR orange] This Week:[/COLOR][COLOR orange] " + count + "[/B][/COLOR]"
				Common.addDir("[B][COLOR orange]3rd - " + developer + "[/COLOR]"  + bname,url,93,iconimage,fanart,description)
				rank = rank + 1
				Common.addItem("[COLOR grey]-----------------------------------------------[/COLOR]",url,17,iconimage,fanart,description)
			else:
				bname = " | [COLOR grey] This Week:[/COLOR][COLOR grey][B] " + count + "[/B][/COLOR]"
				Common.addDir("[COLOR grey]" + developer + "[/COLOR]"  + bname,url,93,iconimage,fanart,description)
	
	Common.addItem('[B][COLOR lightskyblue]HOW TO ADD YOUR BUILDS TO THE LIST[/COLOR][/B]',BASEURL,17,COMMUNITY_ICON,FANART,'')

def SHOWCOMMUNITYBUILDS(name, url, description):

	if "," in url:
		passed = 0

		hidden,url = url.split(",")
		
		vq = Common._get_keyboard( heading="Please Enter Your Password" )
		if ( not vq ): return False, 0
		title = vq

		if title==hidden:
			passed = 1

		if passed == 0:
			dialog.ok(AddonTitle, "Sorry the password entered was not found.",'[COLOR smokewhite]Thank you for using ECHO Wizard[/COLOR]')
			sys.exit(0)

	xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
	version=float(xbmc_version[:4])
	codename = "Decline"

	i=0
	dp.create(AddonTitle,"[COLOR blue]We are getting the list of builds from our server.[/COLOR]",'[COLOR yellow]Please Wait...[/COLOR]','')	
	dp.update(0)

	if version >= 16.0 and version < 17.0:
		codename = 'Jarvis'
	if version >= 17.0 and version < 18.0:
		codename = 'Krypton'

	if 'endlessflix' in url:
		protected_wizards.Endless_Install()


	if 'CALL_THE_BEAST' in url:
		protected_wizards.Beast_Install()
		url = url.replace('CALL_THE_BEAST','')

	i=0
	dp.create(AddonTitle,"[COLOR blue]We are getting the list of developers from our server.[/COLOR]",'[COLOR yellow]Please Wait...[/COLOR]','')	
	dp.update(0)
	namelist=[]
	urllist=[]
	countlist=[]
	deslist=[]
	iconlist=[]
	fanartlist=[]
	desca = description
	developer = desca.split(',')[0]
	hidden = desca.split(',')[1]
	a = 0
	b = 0

	if "beast" in url:
		link = Common.OPEN_URL_BEAST(url).replace('\n','').replace('\r','')
	else: link = Common.OPEN_URL_NORMAL(url).replace('\n','').replace('\r','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)"').findall(link)
	dis_links = len(match)
	for name,url,iconimage,fanart in match:
		i = i + 1
		dis_count = str(i)
		progress = 100 * int(i)/int(dis_links)
		dp.update(progress,"Getting details for developer " + str(dis_count) + " of " + str(dis_links),'',"[COLOR white][B]FOUND - [/B] " + name + "[/COLOR]")
		found = 1
		description = "null" + "," + developer
		name = "[COLOR ghostwhite][B]" + name + "[/B][/COLOR]"
		namelist.append(name)
		urllist.append(url)
		countlist.append(str(Common.count_community(name)))   
		deslist.append(description)
		iconlist.append(iconimage)
		fanartlist.append(fanart)
		combinedlists = list(zip(countlist,namelist,urllist,deslist,iconlist,fanartlist))
	tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
	for count,name,url,description,iconimage,fanart in tup:
		if codename == "Jarvis":
			if not "krypton" in name.lower():
				b = b + 1
				if "skip" in name.lower():
					name=name.replace('skip','')
					Common.addItem(name,url,999,iconimage,fanart,description)
				else:
					bname = "- [COLOR white]Downloads:[/COLOR] [COLOR lightskyblue][B]" + count + "[/B][/COLOR]"
					Common.addDir(name + bname,url,97,iconimage,fanart,description)
		if codename == "Krypton":
			if "krypton" in name.lower():
				a = a + 1
				if "skip" in name.lower():
					name=name.replace('skip','')
					Common.addItem(name,url,999,iconimage,fanart,description)
				else:
					bname = "- [COLOR white]Downloads:[/COLOR] [COLOR lightskyblue][B]" + count + "[/B][/COLOR]"
					Common.addDir(name + bname,url,97,iconimage,fanart,description)
	
	if codename == "Krypton":
		if a == 0:
			dialog.ok(AddonTitle, "[COLOR white]Sorry, no Krypton builds were found![/COLOR]")
			sys,exit(1)

	if codename == "Jarvis":
		if b == 0:
			dialog.ok(AddonTitle, "[COLOR white]Sorry, no Jarvis builds were found![/COLOR]")
			sys,exit(1)

	try:
		f = open(COM_NOTICE,mode='r'); msg = f.read(); f.close()
		Common.TextBoxesPlain("%s" % msg)
	except: pass

def SHOWPROTECTEDBUILDS(name, url, description):

	desca = description
	developer = desca.split(',')[0]
	hidden = desca.split(',')[1]
	
	try:
		link = Common.OPEN_URL(url).replace('\n','').replace('\r','')
		match = re.compile('notice="(.+?)"').findall(link)
		for notice in match:
			dialog.ok(AddonTitle, '[COLOR red][B]' + notice + '[/B][/COLOR]')
	except: pass

	vq = Common._get_keyboard( heading="Please Enter Your Password" )
	if ( not vq ): return False, 0
	title = vq

	if "http" not in hidden:
		AUTH = BASEURL + "community/protected/" + hidden + '.txt'
	else:
		AUTH = hidden
	passed = 0
	link = Common.OPEN_URL(AUTH).replace('\n','').replace('\r','')
	match = re.compile('passkey="(.+?)"').findall(link)
	for passkey in match:
		if title==passkey:
			passed = 1

	if passed == 0:
		dialog.ok(AddonTitle, "Sorry the password entered was not found.",'[COLOR smokewhite]Thank you for using ECHO Wizard[/COLOR]')
		sys.exit(0)

	link = Common.OPEN_URL(url).replace('\n','').replace('\r','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)"').findall(link)
	for name,url,iconimage,fanart in match:
		description = "null" + "," + developer
		name = "[COLOR ghostwhite][B]" + name + "[/B][/COLOR]"
		bname = "- [COLOR white]Downloads:[/COLOR] [COLOR lightskyblue][B]" + str(Common.count_community(name)) + "[/B][/COLOR]"
		Common.addDir(name + bname,url,97,iconimage,fanart,description)

	try:
		f = open(COM_NOTICE,mode='r'); msg = f.read(); f.close()
		Common.TextBoxesPlain("%s" % msg)
	except: pass

#######################################################################
#                       Community
#######################################################################
def CommunityBuilds():
    
    dialog = xbmcgui.Dialog()
    dialog.ok(AddonTitle, "[COLOR white]If you would like your build to be hosted by[/COLOR]", "[COLOR ghostwhite]ECHO[/COLOR] [COLOR lightsteelblue]WIZARD[/COLOR]  [COLOR white]please visit:[/COLOR]", "[COLOR smokewhite]http://www.echocoder.com/forum [/COLOR]")

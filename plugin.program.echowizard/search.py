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
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import urllib2,urllib
import re
import common as Common
import youtube as YOU

addon_id = 'plugin.program.echowizard'
ADDON = xbmcaddon.Addon(id=addon_id)
AddonTitle="[COLOR lime]ECHO[/COLOR] [COLOR white]Wizard[/COLOR]"
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
YOUTUBE_ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/youtube.png'))
#URLS
BASEURL = base64.b64decode(b"aHR0cDovL2VjaG9jb2Rlci5jb20v")
JARVIS_LIST = BASEURL + base64.b64decode(b"YnVpbGRzL3NlYXJjaF9qYXJ2aXMudHh0")
KRYPTON_LIST = BASEURL + base64.b64decode(b"YnVpbGRzL3NlYXJjaF9rcnlwdG9uLnR4dA==")
COM_NOTICE = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/community_notice.txt'))
COM_LIST = BASEURL + base64.b64decode(b"Y29tbXVuaXR5L3NlYXJjaC50eHQ=")
AdvancedSettings = BASEURL + base64.b64decode(b"YWR2YW5jZWRzZXR0aW5ncy93aXphcmRfcmVsLnR4dA==")
LIB = BASEURL + base64.b64decode(b"bGliL2xpYmxpc3QudHh0")
TOOLS = BASEURL + base64.b64decode(b"a29kaS90b29scy9saXN0LnR4dA==")
CHANNELS = BASEURL + base64.b64decode(b'eW91dHViZS9jaGFubmVscy50eHQ=')
youtubelink = base64.b64decode(b"cGx1Z2luOi8vcGx1Z2luLnZpZGVvLnlvdXR1YmUvP2FjdGlvbj1wbGF5X3ZpZGVvJnZpZGVvaWQ9")
#Wizard ICONS
BUILD_ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/build.png'))
ADVANCED_SETTINGS_ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/advanced_settings.png'))
APK_ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/apk.png'))
BACKUP_ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/backup.png'))
COMMUNITY_ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/community.png'))
SETTINGS_ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/settings.png'))
SPEEDTEST_ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/speed_test.png'))
SPMC_ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/SPMC.png'))
SUPPORT_ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/support.png'))
SYSTEM_INFO_ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/system_info.png'))
TMP_ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/TMP_FILES.png'))
TOOLS_ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/tools.png'))
VIP_ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/VIP.png'))
LIB_ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/lib.png'))
YOUTUBE_ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/youtube.png'))

#######################################################################
#						Search Function
#######################################################################

def YOUTUBE():

	vq = Common._get_keyboard( heading="What would you like to search for?" )
	if ( not vq ): return False, 0
	title = vq
	url = title

	YOU.LOADITEM(title, url)

def BUILDS():

	vq = Common._get_keyboard( heading="What would you like to search for?" )
	if ( not vq ): return False, 0
	title = vq

	xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
	version=float(xbmc_version[:4])
	codename = "Decline"
	
	if version >= 16.0 and version <= 16.9:
		codename = 'Jarvis'
	if version >= 17.0 and version <= 17.9:
		codename = 'Krypton'
	
	Common.addItem("[COLOR lightskyblue][B]You Searched For: [/B][/COLOR][COLOR white][I]" + title + "[/COLOR][/I]",BASEURL,22,ICON,FANART,'')
	matchbuild = 0
	#Check for Jarvis builds.
	if codename == "Jarvis":
		link = Common.OPEN_URL(JARVIS_LIST).replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)"').findall(link)
		for url in match:	
			link = Common.OPEN_URL(url).replace('\n','').replace('\r','')
			match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)".+?escription="(.+?)".+?resh="(.+?)".+?ash="(.+?)".+?outube="(.+?)".+?kin="(.+?)"').findall(link)
			for name,url,iconimage,fanart,version,desc,fresh,hash,youtube,skin in match:
				if title.lower() in name.lower():
					matchbuild = 1
					id=youtubelink+youtube
					description = str(desc + "," + hash + "," + fresh + "," + id + "," + skin)
					Common.addDir(name,url,83,iconimage,fanart,description)
	if codename == "Krypton":
		link = Common.OPEN_URL(KRYPTON_LIST).replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)"').findall(link)
		for url in match:	
			link = Common.OPEN_URL(url).replace('\n','').replace('\r','')
			match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)".+?escription="(.+?)".+?resh="(.+?)".+?ash="(.+?)".+?outube="(.+?)".+?kin="(.+?)"').findall(link)
			for name,url,iconimage,fanart,version,desc,fresh,hash,youtube,skin in match:
				if title.lower() in name.lower():
					matchbuild = 1
					id=youtubelink+youtube
					description = str(desc + "," + hash + "," + fresh + "," + id + "," + skin)
					Common.addDir(name,url,83,iconimage,fanart,description)
	if matchbuild == 0:
		Common.addItem("[I]No Results Found[/I]",BASEURL,22,ICON,FANART,'')
		
def COMMUNITY():

	choice = xbmcgui.Dialog().yesno(AddonTitle,'This search will scan all of our community builds. Depending on how many builds there are and the speed of your internet this search may take a minute or two. ','[COLOR dodgerblue][B]Do you wish to continue?[/B][/COLOR]', yeslabel='[B][COLOR lime]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
	if choice == 0: 
		sys.exit(0)

	vq = Common._get_keyboard( heading="What would you like to search for?" )
	if ( not vq ): return False, 0
	title = vq
	matchcomm = 0
	found = 0
	Common.addItem("[COLOR lightskyblue][B]You Searched For: [/B][/COLOR][COLOR white][I]" + title + "[/COLOR][/I]",BASEURL,22,ICON,FANART,'')
	link = Common.OPEN_URL(COM_LIST)
	match = re.compile('url="(.+?)"').findall(link)
	for url in match:	
		try:
			link = Common.OPEN_URL(url)
			match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?kin="(.+?)"').findall(link)
			for name,url,iconimage,fanart,skin in match:
				if title.lower() in name.lower():
					found = 1
					matchcomm = 1
					description = skin + "," + ""
					name = "[COLOR ghostwhite][B]" + name + "[/B][/COLOR]"
					Common.addDir(name,url,97,iconimage,fanart,description)
			if found == 0:
				link = Common.OPEN_URL(url).replace('\n','').replace('\r','')
				match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)"').findall(link)
				for name,url,iconimage,fanart in match:
					if title.lower() in name.lower():
						found = 1
						matchcomm = 1
						description = "null" + "," + ""
						name = "[COLOR ghostwhite][B]" + name + "[/B][/COLOR]"
						Common.addDir(name,url,97,iconimage,fanart,description)
		except: pass

	if matchcomm == 0:
		Common.addItem("[I]No Results Found[/I]",BASEURL,22,ICON,FANART,'')
	else:
		try:
			f = open(COM_NOTICE,mode='r'); msg = f.read(); f.close()
			Common.TextBoxesPlain("%s" % msg)
		except: pass

def ALL():

	#Keyboard.

	vq = Common._get_keyboard( heading="What would you like to search for?" )
	if ( not vq ): return False, 0
	title = vq

	#Check Kodi Version

	xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
	version=float(xbmc_version[:4])
	codename = "Decline"
	if version >= 16.0 and version <= 16.9:
		codename = 'Jarvis'
	if version >= 17.0 and version <= 17.9:
		codename = 'Krypton'

	Common.addItem("[COLOR lightskyblue][B]You Searched For: [/B][/COLOR][COLOR white][I]" + title + "[/COLOR][/I]",BASEURL,22,ICON,FANART,'')
	#Check for Jarvis builds.
	matchbuild = 0
	Common.addItem("[COLOR smokewhite][B]TEAM TDB BUILD RESULTS[/B][/COLOR]",BASEURL,22,BUILD_ICON,FANART,'')
	if codename == "Jarvis":
		link = Common.OPEN_URL(JARVIS_LIST).replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)"').findall(link)
		for url in match:	
			link = Common.OPEN_URL(url).replace('\n','').replace('\r','')
			match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)".+?escription="(.+?)".+?resh="(.+?)".+?ash="(.+?)".+?outube="(.+?)".+?kin="(.+?)"').findall(link)
			for name,url,iconimage,fanart,version,desc,fresh,hash,youtube,skin in match:
				if title.lower() in name.lower():
					matchbuild = 1
					id=youtubelink+youtube
					description = str(desc + "," + hash + "," + fresh + "," + id + "," + skin)
					Common.addDir(name,url,83,iconimage,fanart,description)
	
	#Check for Krypton builds.
	if codename == "Krypton":
		link = Common.OPEN_URL(KRYPTON_LIST).replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)"').findall(link)
		for url in match:	
			link = Common.OPEN_URL(url).replace('\n','').replace('\r','')
			match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)".+?escription="(.+?)".+?resh="(.+?)".+?ash="(.+?)".+?outube="(.+?)".+?kin="(.+?)"').findall(link)
			for name,url,iconimage,fanart,version,desc,fresh,hash,youtube,skin in match:
				if title.lower() in name.lower():
					matchbuild = 1
					id=youtubelink+youtube
					description = str(desc + "," + hash + "," + fresh + "," + id + "," + skin)
					Common.addDir(name,url,83,iconimage,fanart,description)
	if matchbuild == 0:
		Common.addItem("[I]No Results Found[/I]",BASEURL,22,ICON,FANART,'')
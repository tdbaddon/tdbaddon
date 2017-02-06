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
#######################################################################
#						GET ALL DEPENDANCIES NEEDED
#######################################################################

import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
from urllib import FancyURLopener
import platform
import shutil
import urllib2,urllib
import re
import glob
import time
import errno
import socket
import json

#######################################################################
#		REQUIRES script.module.requests AS A DEPENDANCY.
#######################################################################

import requests

#######################################################################
#					LOCAL .PY DEPENDANCIES
#######################################################################
from resources.lib.modules import get_addons
from resources.lib.modules import uploadlog
from resources.lib.modules import runner
from resources.lib.modules import community
from resources.lib.modules import installer
from resources.lib.modules import update
from resources.lib.modules import parameters
from resources.lib.modules import maintenance
from resources.lib.modules import plugintools
from resources.lib.modules import backuprestore
from resources.lib.modules import speedtest
from resources.lib.modules import common as Common
from resources.lib.modules import wipe
from resources.lib.modules import versioncheck
from resources.lib.modules import extras
from resources.lib.modules import security
from resources.lib.modules import cache_dir

#######################################################################
#					VERIABLES NEEDED
#######################################################################

AddonTitle          ="[COLOR yellowgreen]ECHO[/COLOR] [COLOR white]Wizard[/COLOR]"
AddonData           = xbmc.translatePath('special://userdata/addon_data')
USERDATA            =  xbmc.translatePath(os.path.join('special://home/userdata',''))
addon_id            = 'plugin.program.echowizard'
ADDON               = xbmcaddon.Addon(id=addon_id)
CHANGELOG           =  xbmc.translatePath(os.path.join('special://home/addons/' + addon_id,'changelog.txt'))
WIZARD_VERSION      =  xbmc.translatePath(os.path.join('special://home/addons/' + addon_id,'version.txt'))
RESOURCES           =  xbmc.translatePath(os.path.join('special://home/addons/' + addon_id,'resources'))
NOTICE              =  xbmc.translatePath(os.path.join('special://home/addons/' + addon_id,'resources/NOTICE.txt'))
GET_VERSION         =  xbmc.translatePath('special://home/addons/' + addon_id + '/addon.xml')
DEFAULT_SETTINGS    =  xbmc.translatePath(os.path.join('special://home/addons/' + addon_id,'resources/settings_default.xml'))
ADDON_DATA          =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id))
ECHO_SETTINGS       =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id,'settings.xml'))
TEMP_FOLDER         =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id,'temp'))
TEMP_FILE           =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id,'temp/temp.xml'))
TEMP_ADDONS         =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id,'temp/temp_installer.xml'))
COMMUNITY_BUILD		=  xbmc.translatePath(os.path.join('special://home/userdata/','community_build.txt'))
COMMUNITY_OTA		=  xbmc.translatePath(os.path.join('special://home/userdata/','echo_community_ota.txt'))
KEYBOARD_FILE       =  xbmc.translatePath(os.path.join('special://home/userdata/keymaps/','keyboard.xml'))
ADVANCED_SET_FILE   =  xbmc.translatePath(os.path.join('special://home/userdata/','advancedsettings.xml'))
dp                  =  xbmcgui.DialogProgress()
skin                =  xbmc.getSkinDir()
string              = ""
dialog              = xbmcgui.Dialog()
THE_TIME 			= time.strftime("%H:%M %p")
THE_DATE 			= time.strftime("%A %B %d %Y")

#######################################################################
#					ADDON SETTINGS
#######################################################################

check               = plugintools.get_setting("checkupdates")
check_addon         = plugintools.get_setting("checkaddonupdates")
auto                = plugintools.get_setting("autoupdates")

#######################################################################
#					URLS NEEDED
#######################################################################

BASEURL             = base64.b64decode(b'aHR0cDovL2VjaG9jb2Rlci5jb20v')
SpeedTest           = BASEURL + base64.b64decode(b'c3BlZWR0ZXN0L3NwZWVkdGVzdC50eHQ=')
AdvancedSettings    = BASEURL + base64.b64decode(b'YWR2YW5jZWRzZXR0aW5ncy93aXphcmRfcmVsLnR4dA==')
KeymapsURL          = BASEURL + base64.b64decode(b'a2V5bWFwcy93aXphcmRfcmVsLnR4dA==')
APKS                = BASEURL + base64.b64decode(b'a29kaS9hcGtzL2Fwa2xpc3QudHh0')
APKS_INSTALLER      = BASEURL + base64.b64decode(b'YWRkb25zL2Fwa3MudHh0')
AND_APKS            = BASEURL + base64.b64decode(b'YW5kcm9pZC9hcGtzL2xpc3QudHh0')
WINDOWS             = BASEURL + base64.b64decode(b'a29kaS93aW5kb3dzL2xpc3QudHh0')
OSX                 = BASEURL + base64.b64decode(b'a29kaS9vc3gvbGlzdC50eHQ=')
IOS                 = BASEURL + base64.b64decode(b'a29kaS9pb3MvbGlzdC50eHQ=')
APKSLIB             = BASEURL + base64.b64decode(b'YXBrcy9hcGtsaWJsaXN0LnR4dA==')
LIB                 = BASEURL + base64.b64decode(b'bGliL2xpYmxpc3QudHh0')
TOOLS               = BASEURL + base64.b64decode(b'a29kaS90b29scy9saXN0LnR4dA==')
CONTACTS            = BASEURL + base64.b64decode(b'b3RoZXIvY29udGFjdGxpc3QudHh0')
SUPPORT             = BASEURL + base64.b64decode(b'b3RoZXIvc3VwcG9ydC50eHQ=')
CREDITS             = BASEURL + base64.b64decode(b'Y3JlZGl0cy93aXphcmQudHh0')
NEWS                = BASEURL + base64.b64decode(b'b3RoZXIvbmV3cy50eHQ=')
DONATIONS_URL       = BASEURL + base64.b64decode(b'b3RoZXIvZG9uYXRpb25zLnR4dA==')
SERVER_CHECKER      = BASEURL + base64.b64decode(b'ZG93bi50eHQ=')
SERVER_CHECK        = BASEURL + base64.b64decode(b'Y2hlY2tlci50eHQ=')
ADD_COMMUNITY       = BASEURL + base64.b64decode(b'b3RoZXIvYWRkX2NvbW11bml0eS50eHQ=')
ADDONS_API          = BASEURL + base64.b64decode(b'YXBpL2FwaS5waHA/c2VydmljZT1hZGRvbnMmYWN0aW9uPWNvdW50')
ECHO_API            = BASEURL + base64.b64decode(b"YXBpL2FwaS5waHA/c2VydmljZT1idWlsZHMmYWN0aW9uPWNvdW50")
ECHO_CHANNEL        = base64.b64decode(b"aHR0cDovL2VjaG9jb2Rlci5jb20veW91dHViZS95b3V0dWJlLnBocD9pZD1VQ29ZVkVRd3psU3VFLU4yQ3VLdlFKNHc=")
JARVIS_URL          = BASEURL + base64.b64decode(b"YnVpbGRzL3dpemFyZF9yZWxfamFydmlzLnR4dA==")
KRYPTON_URL         = BASEURL + base64.b64decode(b"YnVpbGRzL3dpemFyZF9yZWxfa3J5cHRvbi50eHQ=")
youtubelink         = base64.b64decode(b"cGx1Z2luOi8vcGx1Z2luLnZpZGVvLnlvdXR1YmUvcGxheS8/dmlkZW9faWQ9")
FANRIFFIC_URL_NEW   = base64.b64decode(b'aHR0cDovL2ZhbnJpZmZpYy5jb20vd2l6d2l6L3Bob29leXRoZW1lcy50eHQ=')
FANRIFFIC_URL_OLD   = base64.b64decode(b'aHR0cDovL2ZhbnJpZmZpYy5jb20vd2l6d2l6L3Bob29leXRoZW1lc29sZC50eHQ=')
FANRIFFIC_KRYPTON   = base64.b64decode(b'aHR0cDovL2ZhbnJpZmZpYy5jb20vd2l6d2l6L2tyeXB0b250aGVtZXMudHh0')

#######################################################################
#					ECHO WIZARD ICONS
#######################################################################

FANART              = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON                = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
ART                 = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
ECHOICON            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
WIZARDICON          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
ADVANCED_SET_ICON   = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
APK_ICON            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
BACKUP_ICON         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
COMMUNITY_ICON      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
SETTINGS_ICON       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
SPEEDTEST_ICON      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
SPMC_ICON           = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
SUPPORT_ICON        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
SYSTEM_INFO_ICON    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
TMP_ICON            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
TOOLS_ICON          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
VIP_ICON            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
LIB_ICON            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
YOUTUBE_ICON        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
SEARCH_ICON         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
GUEST_ICON          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
SERVER_ICON         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
BUILD_ICON          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
KODI_ICON           = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
KODI_FANART         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
SPMC_ICON           = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
SPMC_FANART         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
UPDATE_ICON         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
EXTRAS_ICON         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
SPORTS_ICON         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
ERROR_ICON          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
STATS_ICON          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
TWITTER_ICON        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
KEYMAPS_ICON        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))

#######################################################################
#				CONTACT THE RUNNER
#######################################################################

runner.check()

#######################################################################
#					ECHO VERSION CHECKERS
#######################################################################

ECHO_VERSION        =  os.path.join(USERDATA,'echo_build.txt')

#######################################################################
#					CUSTOM HEADER FOR SECURITY
#######################################################################

class MyOpener(FancyURLopener):
	version = base64.b64decode(b'VGhlV2l6YXJkSXNIZXJl')

#######################################################################
#			REDIRECT URLLIB COMMANDS TO MYOPENER
#######################################################################

myopener = MyOpener()
urlopen = MyOpener().open

#######################################################################
#			CHECK FOR ARCHIVE_CACHE IN KODI 17
#######################################################################

cache_dir.check()

#######################################################################
#			CREATE SETTINGS XML IF IT DOES NOT EXIST
#######################################################################

if not os.path.isfile(ECHO_SETTINGS):
	if not os.path.exists(ADDON_DATA):
		os.makedirs(ADDON_DATA)
	shutil.copyfile(DEFAULT_SETTINGS, ECHO_SETTINGS)

#######################################################################
#						CREATE PATH FOR BACKUPS
#######################################################################

backuprestore.check_path()

#######################################################################
#						CHECK FOR NOTICE
#######################################################################

if os.path.isfile(NOTICE):
	f = open(NOTICE,mode='r'); msg = f.read(); f.close()
	Common.TextBoxesPlain("%s" % msg)
	os.remove(NOTICE)

#######################################################################
#			CREATE FILES AND FOLDERS FOR ECHO API
#######################################################################

if not os.path.exists(TEMP_FOLDER):
	os.makedirs(TEMP_FOLDER)
if not os.path.isfile(TEMP_FILE):
	open(TEMP_FILE, 'w')
if not os.path.isfile(TEMP_ADDONS):
	open(TEMP_ADDONS, 'w')

#######################################################################
#						ECHO WIZARD ROOT MENU
#######################################################################

def INDEX():

	#######################################################################
	#	VERIABLES NEEDED IN THE LIST MENU
	#######################################################################

	pleasecheck 		= 0
	BUILD_CHECK_ERROR   = 0
	CURRENT_BUILD = "[COLOR yellowgreen]ERROR[/COLOR]"
	CURRENT_VERSION_CODE = "[COLOR yellowgreen]ERROR[/COLOR]"
	LATEST_VERSION = "[COLOR yellowgreen]ERROR[/COLOR]"

	#######################################################################
	#					FIND ADDON VERSION
	#######################################################################
	
	a=open(GET_VERSION).read()
	b=a.replace('\n',' ').replace('\r',' ')
	match=re.compile('name=".+?".+?version="(.+?)".+?provider-name=".+?">').findall(str(b))
	for item in match:
		addon_version = float(item)
	
	#######################################################################
	#					FIND BUILD INFORMATION
	#######################################################################

	try:
		U_A = 'TheWizardIsHere'
		if os.path.exists(ECHO_VERSION):
			VERSIONCHECK = ECHO_VERSION
			FIND_URL = BASEURL + base64.b64decode(b'YnVpbGRzL3VwZGF0ZV93aXoudHh0')
			checkurl = BASEURL + base64.b64decode(b'YnVpbGRzL3ZlcnNpb25fY2hlY2sudHh0')
			pleasecheck = 1
		if os.path.exists(COMMUNITY_OTA):
			VERSIONCHECK = COMMUNITY_OTA
			a=open(VERSIONCHECK).read()
			FIND_URL = re.compile('<update_url>(.+?)</update_url>').findall(a)[0]
			checkurl = re.compile('<version_check>(.+?)</version_check>').findall(a)[0]
			try:
				U_A = re.compile('<user_agent>(.+?)</user_agent>').findall(a)[0]
			except: pass
			pleasecheck = 1
	except:
		pass

	#######################################################################
	#					CHECK FOR BUILD UPDATES
	#######################################################################

	try:
		if pleasecheck == 1:
			a=open(VERSIONCHECK).read()
			CURRENT_BUILD = re.compile('<build>(.+?)</build>').findall(a)[0]
			CURRENT_VERSION = re.compile('<version>(.+?)</version>').findall(a)[0]
			req = urllib2.Request(checkurl)
			req.add_header('User-Agent',U_A)
			response = urllib2.urlopen(req)
			link=response.read()
			response.close()
			match = re.compile('<build>'+CURRENT_BUILD+'</build><version>(.+?)</version><fresh>(.+?)</fresh>').findall(link)
			for newversion,fresh in match:
				LATEST_VERSION = newversion
				if CURRENT_VERSION < LATEST_VERSION:
					CURRENT_VERSION_CODE = '[COLOR yellowgreen]' + CURRENT_VERSION + '[/COLOR]'
				else:
					CURRENT_VERSION_CODE = '[COLOR yellowgreen]' + CURRENT_VERSION + '[/COLOR]'
	except:
		CURRENT_BUILD = "[COLOR yellowgreen]ERROR[/COLOR]"
		CURRENT_VERSION_CODE = "[COLOR yellowgreen]ERROR[/COLOR]"
		LATEST_VERSION = "[COLOR yellowgreen]ERROR[/COLOR]"

	#######################################################################
	#					FIND OUT VERSION OF KODI
	#######################################################################

	kodi_name = Common.GET_KODI_VERSION()

	#######################################################################
	#					GET API INFORMATION
	#######################################################################

	api_interval = plugintools.get_setting("api_interval")

	if api_interval == "0":
		mark = "60"
	elif api_interval == "1":
		mark = "50"
	elif api_interval == "2":
		mark = "40"
	elif api_interval == "3":
		mark = "30"
	elif api_interval == "4":
		mark = "20"
	elif api_interval == "5":
		mark = "10"
	elif api_interval == "6":
		mark = "5"
	else: mark = "60"

	#######################################################################
	#					GET COUNTS FROM THE ECHO API
	#######################################################################

	GET_COUNTS()
	
	#######################################################################
	#					START MAIN MENU
	#######################################################################

	Common.addItem("[COLOR white][B]ECHO WIZARD VERSION:[/COLOR] [COLOR yellowgreen]" + str(addon_version) + "[/B][/COLOR]",'url',999,ICON,FANART,'')
	total_addons_week = Common.count("TOTAL_ADDONS_WEEK",TEMP_ADDONS)
	total_builds_week = Common.count("TOTAL_BUILDS_WEEK",TEMP_FILE)
	Common.addDir("[COLOR white][B]ADDONS DOWNLOADED THIS WEEK - [/COLOR][COLOR yellowgreen]" + str(total_addons_week) + "[/B][/COLOR]",BASEURL,121,ICON,FANART,'')
	Common.addDir("[COLOR white][B]BUILDS DOWNLOADED THIS WEEK - [/COLOR][COLOR yellowgreen]" + str(total_builds_week) + "[/B][/COLOR]",BASEURL,121,ICON,FANART,'')
	#Common.addDir('[COLOR ghostwhite][B]ALL OFFICIAL ECHO YOUTUBE VIDEOS[/B][/COLOR]',BASEURL,60,YOUTUBE_ICON,FANART,'')
	if pleasecheck == 1:
		Common.addItem("[COLOR yellowgreen][B]--------------------------[/B][/COLOR]",BASEURL,79,ICON,FANART,'')
		Common.addItem('[COLOR ghostwhite][B]CURRENT BUILD: [/B][/COLOR][COLOR yellowgreen][B]' + CURRENT_BUILD + '[/B][/COLOR]',BASEURL,4,BUILD_ICON,FANART,'')
		Common.addItem('[COLOR ghostwhite][B]YOUR VERSION: [/B][/COLOR][B]' + CURRENT_VERSION_CODE + '[/B]',BASEURL,4,BUILD_ICON,FANART,'')
		Common.addItem('[COLOR ghostwhite][B]LATEST VERSION: [/B][/COLOR][COLOR yellowgreen][B]' + LATEST_VERSION + '[/B][/COLOR]',BASEURL,4,BUILD_ICON,FANART,'')
		try:
			if LATEST_VERSION > CURRENT_VERSION:
				if "ERROR" not in CURRENT_VERSION_CODE:
					Common.addItem('[COLOR ghostwhite][B]CLICK TO UPDATE ' + CURRENT_BUILD.upper() + ' NOW![/B][/COLOR]',BASEURL,33,UPDATE_ICON,FANART,'')
			else:
				Common.addItem('[COLOR yellowgreen][B]' + CURRENT_BUILD.upper() + ' IS UP TO DATE![/B][/COLOR]',BASEURL,4,UPDATE_ICON,FANART,'')
		except:
			Common.addItem('[COLOR ghostwhite][B]ERROR RETRIEVING INFORMATION[/B][/COLOR]',BASEURL,4,UPDATE_ICON,FANART,'')
	else:
		if os.path.isfile(COMMUNITY_BUILD):
			Common.addDir('[COLOR slategrey][B]CURRENT BUILD: [/COLOR][COLOR yellowgreen][B]COMMUNITY BUILD INSTALLED[/COLOR][/B]',BASEURL,88,BUILD_ICON,FANART,'')
	Common.addItem("[COLOR yellowgreen][B]--------------------------[/B][/COLOR]",BASEURL,79,ICON,FANART,'')
	Common.addDir('[COLOR ghostwhite][B]OFFICIAL ECHO BUILDS[/B][/COLOR]',BASEURL,50,BUILD_ICON,FANART,'')
	Common.addDir('[COLOR ghostwhite][B]COMMUNITY BUILDS[/B][/COLOR]',BASEURL,87,COMMUNITY_ICON,FANART,'')
	Common.addDir('[COLOR ghostwhite][B]ECHO ADDON INSTALLER[/B][/COLOR]',BASEURL,121,ICON,FANART,'')
	Common.addDir('[COLOR ghostwhite][B]FANRIFFIC THEMES[/B][/COLOR]',BASEURL,144,ICON,FANART,'')
	Common.addItem("[COLOR yellowgreen][B]--------------------------[/B][/COLOR]",BASEURL,79,ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite][B]RUN THE ECHO SECURITY CHECK[/COLOR][/B]',BASEURL,181,TOOLS_ICON,FANART,'')
	Common.addDir('[COLOR ghostwhite][B]BACKUP [COLOR white]|[/COLOR] RESTORE[/B][/COLOR]',BASEURL,8,BACKUP_ICON,FANART,'')
	Common.addDir('[COLOR ghostwhite][B]MAINTENANCE TOOLS[/COLOR][/B]',BASEURL,5,TOOLS_ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite][B]VIEW ALL ERRORS IN LOG FILE[/B][/COLOR]',BASEURL,155,ERROR_ICON,FANART,'')
	Common.addDir('[COLOR ghostwhite][B]SPEED TEST[/B][/COLOR]',BASEURL,16,SPEEDTEST_ICON,FANART,'')
	Common.addItem("[COLOR yellowgreen][B]--------------------------[/B][/COLOR]",BASEURL,79,ICON,FANART,'')
	Common.addDir('[COLOR ghostwhite][B]EXTRAS - FIXES, TWEAKS ETC[/B][/COLOR]',BASEURL,74,EXTRAS_ICON,FANART,'')
	Common.addDir('[COLOR ghostwhite][B]ADVANCED SETTINGS[/B][/COLOR]',BASEURL,30,ADVANCED_SET_ICON,FANART,'')	
	Common.addDir('[COLOR ghostwhite][B]CUSTOM KEYMAPS[/B][/COLOR]',BASEURL,129,KEYMAPS_ICON,FANART,'')	
	#Common.addDir('[COLOR ghostwhite][B]ANDROID APKS[/B][/COLOR]',BASEURL,149,TOOLS_ICON,FANART,'')
	Common.addDir('[COLOR ghostwhite][B]MUST HAVE KODI PROGRAMS & TOOLS[/B][/COLOR]',BASEURL,46,TOOLS_ICON,FANART,'')
	Common.addDir('[COLOR ghostwhite][B]KODI/SPMC INSTALLATION FILES[/B][/COLOR]',BASEURL,28,APK_ICON,FANART,'')
	Common.addDir('[COLOR ghostwhite][B]KODI/SPMC LIBRTMP FILES[/B][/COLOR]',BASEURL,29,LIB_ICON,FANART,'')
	Common.addItem("[COLOR yellowgreen][B]--------------------------[/B][/COLOR]",BASEURL,79,ICON,FANART,'')
	Common.addDir('[COLOR ghostwhite][B]ESSENTIAL DEVELOPER TWITTER DETAILS[/B][/COLOR]',BASEURL,84,TWITTER_ICON,FANART,'')
	Common.addDir('[COLOR ghostwhite][B]THE DAYS SPORT LISTINGS[/B][/COLOR]',BASEURL,47,SPORTS_ICON,FANART,'')
	Common.addDir('[COLOR ghostwhite][B]SYSTEM INFORMATION[/B][/COLOR]',BASEURL,163,SYSTEM_INFO_ICON,FANART,'')
	Common.addItem("[COLOR yellowgreen][B]--------------------------[/B][/COLOR]",BASEURL,79,ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite][B]THE ECHO API REFRESHES EVERY ' + '[COLOR yellowgreen]'+str(mark)+' [/COLOR]MINUTES[/B][/COLOR]',BASEURL,9,SETTINGS_ICON,FANART,'')
	#Common.addItem('[COLOR ghostwhite][B]CLEAR DOWNLOAD COUNTERS[/B][/COLOR]',BASEURL,180,SETTINGS_ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite][B]REGENERATE DOWNLOAD COUNTERS[/B][/COLOR]',BASEURL,179,SETTINGS_ICON,FANART,'')
	Common.addItem("[COLOR yellowgreen][B]--------------------------[/B][/COLOR]",BASEURL,79,ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite][B]LATEST NEWS[/B][/COLOR]',BASEURL,106,ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite][B]DONATIONS: [COLOR yellowgreen]paypal.me/echocoder[/COLOR][/B][/COLOR]',BASEURL,172,ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite][B]TWITTER: [/B][/COLOR][COLOR yellowgreen][B]@ECHOCODER[/B][/COLOR]',BASEURL,4,BUILD_ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite][B]HOW TO GET SUPPORT[/B][/COLOR]',BASEURL,79,SUPPORT_ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite][B]VIEW WIZARD CHANGELOG[/B][/COLOR]',BASEURL,80,SEARCH_ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite][B]VIEW EHCO WIZARD CREDITS[/B][/COLOR]',BASEURL,81,SETTINGS_ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite][B]ECHO WIZARD SETTINGS[/B][/COLOR]',BASEURL,9,SETTINGS_ICON,FANART,'')

	kodi_name = Common.GET_KODI_VERSION()

	if kodi_name == "Jarvis":
		xbmc.executebuiltin("Container.SetViewMode(50)")
	elif kodi_name == "Krypton":
		xbmc.executebuiltin("Container.SetViewMode(55)")
	else: xbmc.executebuiltin("Container.SetViewMode(50)")

#######################################################################
#					TDB WIZARD BUILD MENU
#######################################################################

def BUILDMENU():

	xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
	version=float(xbmc_version[:4])
	codename = "Decline"

	i=0
	dp.create(AddonTitle,"[COLOR blue]We are getting the list of builds from our server.[/COLOR]",'[COLOR yellow]Please Wait...[/COLOR]','')	
	dp.update(0)

	if version >= 16.0 and version <= 16.9:
		codename = 'Jarvis'
	elif version >= 17.0 and version <= 17.9:
		codename = 'Krypton'
	else: codename = "Decline"
	
	if codename == "Decline":
		dialog.ok(AddonTitle, "Sorry we are unable to process your request","[COLOR yellowgreen][I][B]Error: ECHO does not support this version of Kodi.[/COLOR][/I][/B]")
		return

	if codename == "Jarvis":
		namelist=[]
		urllist=[]
		deslist=[]
		countlist=[]
		totallist=[]
		iconlist=[]
		fanartlist=[]
		link = Common.OPEN_URL(JARVIS_URL).replace('\n','').replace('\r','')
		match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)".+?escription="(.+?)".+?resh="(.+?)".+?ash="(.+?)".+?outube="(.+?)"').findall(link)
		dis_links = len(match)
		for name,url,iconimage,fanart,version,desc,fresh,hash,youtube in match:
			skin = 'null'
			i = i + 1
			dis_count = str(i)
			progress = 100 * int(i)/int(dis_links)
			dp.update(progress,"Getting details from build " + str(dis_count) + " of " + str(dis_links),"[COLOR white][B]FOUND - [/B] " + name + "[/COLOR]")
			id=youtubelink+youtube
			description = str(desc + "," + hash + "," + fresh + "," + id + "," + skin)
			namelist.append(name)
			urllist.append(url)
			deslist.append(description)
			countlist.append(str(Common.count(name,TEMP_FILE)))  
			totallist.append(str(Common.count(name+"TOTAL_COUNT",TEMP_FILE)))     
			iconlist.append(iconimage)
			fanartlist.append(fanart)
			combinedlists = list(zip(countlist,totallist,namelist,urllist,deslist,iconlist,fanartlist))
		tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
		dp.close()
		for count,total,name,url,description,iconimage,fanart in tup:
			url = name + "," + url
			bname = " | [COLOR white] This Week:[/COLOR][COLOR yellowgreen][B] " + count + "[/B][/COLOR][COLOR white] - Total:[/COLOR][COLOR yellowgreen][B] " + total + "[/B][/COLOR]"
			title = "[COLOR dodgerblue][B]" + name + "[/B][/COLOR]" + bname
			Common.addDir(title,url,83,iconimage,fanart,description)

	if codename == "Krypton":
		namelist=[]
		urllist=[]
		deslist=[]
		countlist=[]
		totalcount=[]
		iconlist=[]
		fanartlist=[]
		link = Common.OPEN_URL(KRYPTON_URL).replace('\n','').replace('\r','')
		match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)".+?escription="(.+?)".+?resh="(.+?)".+?ash="(.+?)".+?outube="(.+?)"').findall(link)
		dis_links = len(match)
		for name,url,iconimage,fanart,version,desc,fresh,hash,youtube in match:
			skin = 'null'
			i = i + 1
			dis_count = str(i)
			progress = 100 * int(i)/int(dis_links)
			dp.update(progress,"Getting details from build " + str(dis_count) + " of " + str(dis_links),"[COLOR white][B]FOUND - [/B] " + name + "[/COLOR]")
			id=youtubelink+youtube
			description = str(desc + "," + hash + "," + fresh + "," + id + "," + skin)
			namelist.append(name)
			urllist.append(url)
			deslist.append(description)
			countlist.append(str(Common.count(name,TEMP_FILE)))  
			totalcount.append(str(Common.count(name+"TOTAL_COUNT",TEMP_FILE)))     			
			iconlist.append(iconimage)
			fanartlist.append(fanart)
			combinedlists = list(zip(countlist,totalcount,namelist,urllist,deslist,iconlist,fanartlist))
		tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
		dp.close()
		for count,total,name,url,description,iconimage,fanart in tup:
			url = name + "," + url
			bname = " | [COLOR white] This Week:[/COLOR][COLOR yellowgreen][B] " + count + "[/B][/COLOR][COLOR white] - Total:[/COLOR][COLOR yellowgreen][B] " + total + "[/B][/COLOR]"
			title = "[COLOR dodgerblue][B]" + name + "[/B][/COLOR]" + bname
			Common.addDir(title,url,83,iconimage,fanart,description)

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#						MAINTENANCE MENU
#######################################################################

def MAINTENANCE_MENU():

	check_folders = plugintools.get_setting("maint_check_folders")
	check_log     = plugintools.get_setting("maint_check_log")

	HOME          =  xbmc.translatePath('special://home/')
	PACKAGES      =  xbmc.translatePath(os.path.join('special://home/addons','packages'))
	THUMBS        =  xbmc.translatePath(os.path.join('special://home/userdata','Thumbnails'))
	CACHE_FOLDER  =  xbmc.translatePath(os.path.join('special://home','cache'))
	TEMP_FOLDER   =  xbmc.translatePath(os.path.join('special://','temp'))
	CACHE         =  "NULL"

	if check_folders == "true":
		if os.path.exists(CACHE_FOLDER):
			CACHE = CACHE_FOLDER

		if os.path.exists(TEMP_FOLDER):
			CACHE = TEMP_FOLDER

		if not os.path.exists(PACKAGES):
			os.makedirs(PACKAGES)

		if CACHE == "NULL":
			try:
				PACKAGES_SIZE_BYTE = maintenance.get_size(PACKAGES)
				THUMB_SIZE_BYTE    = maintenance.get_size(THUMBS)
			except: pass
		else:
			try:
				CACHE_SIZE_BYTE    = maintenance.get_size(CACHE)
				PACKAGES_SIZE_BYTE = maintenance.get_size(PACKAGES)
				THUMB_SIZE_BYTE    = maintenance.get_size(THUMBS)
			except: pass
		
		if CACHE == "NULL":
			try:
				PACKAGES_SIZE = maintenance.convertSize(PACKAGES_SIZE_BYTE)
				THUMB_SIZE    = maintenance.convertSize(THUMB_SIZE_BYTE)
			except: pass
		else:
			try:
				CACHE_SIZE    = maintenance.convertSize(CACHE_SIZE_BYTE)
				PACKAGES_SIZE = maintenance.convertSize(PACKAGES_SIZE_BYTE)
				THUMB_SIZE    = maintenance.convertSize(THUMB_SIZE_BYTE)
			except: pass
		
		if CACHE == "NULL":
			CACHE_SIZE    =  "[COLOR red][B]ERROR READING CACHE[/B][/COLOR]"

	startup_clean = plugintools.get_setting("acstartup")
	weekly_clean = plugintools.get_setting("clearday")
	sizecheck_clean = plugintools.get_setting("startupsize")

	if startup_clean == "false":
		startup_onoff = "[COLOR red][B]OFF[/COLOR][/B]"
	else:
		startup_onoff = "[COLOR yellowgreen][B]ON[/COLOR][/B]"
	if weekly_clean == "0":
		weekly_onoff = "[COLOR red][B]OFF[/COLOR][/B]"
	else:
		weekly_onoff = "[COLOR yellowgreen][B]ON[/COLOR][/B]"
	if sizecheck_clean == "false":
		sizecheck_onoff = "[COLOR red][B]OFF[/COLOR][/B]"
	else:
		sizecheck_onoff = "[COLOR yellowgreen][B]ON[/COLOR][/B]"

	if check_log == "true":

		curr = maintenance.grab_Log(True, False)
		old = maintenance.grab_Log(True, True)
		errors1 = []; errors2 = []
		if not curr == False: errors1 = maintenance.errorList(curr)
		if not old == False: errors2 = maintenance.errorList(old)
		i = len(errors1) + len(errors2)
        
		if i == 0:
			ERRORS_IN_LOG = "[COLOR yellowgreen][B]0 ERRORS FOUND IN LOG[/B][/COLOR]"
		else:
			ERRORS_IN_LOG = "[COLOR red][B]" + str(i) + " ERRORS FOUND IN LOG[/B][/COLOR]"

	Common.addDir('[COLOR yellowgreen][B]CLICK FOR SYSTEM INFORMATION (ADDONS, IP, ETC)[/B][/COLOR]',BASEURL,163,SYSTEM_INFO_ICON,FANART,'')
	if check_folders == "true":
		try:
			Common.addItem("[COLOR white][B]CACHE SIZE IS [/B][/COLOR]" + str(CACHE_SIZE),BASEURL,79,ICON,FANART,'')
		except: 		
			Common.addItem("[COLOR white][B]ERROR GETTING CACHE SIZE[/B][/COLOR]",BASEURL,79,ICON,FANART,'')
		try:
			Common.addItem("[COLOR white][B]PACKAGES SIZE IS [/B][/COLOR]" + str(PACKAGES_SIZE),BASEURL,79,ICON,FANART,'')
		except:
			Common.addItem("[COLOR white][B]ERROR GETTING PACKAGES SIZE[/B][/COLOR]",BASEURL,79,ICON,FANART,'')
		try:
			Common.addItem("[COLOR white][B]THUMBNAIL SIZE IS [/B][/COLOR]" + str(THUMB_SIZE),BASEURL,79,ICON,FANART,'')
		except:
			Common.addItem("[COLOR white][B]ERROR GETTING THUMBNAIL SIZE[/B][/COLOR]",BASEURL,79,ICON,FANART,'')
	Common.addItem("[COLOR white][B]--------------------------[/B][/COLOR]",BASEURL,79,ICON,FANART,'')
	Common.addItem('[COLOR white][B]WEEKLY AUTO CLEAN - [/B][/COLOR]' + weekly_onoff,BASEURL,113,TOOLS_ICON,FANART,'')
	Common.addItem('[COLOR white][B]AUTO CLEAN ON KODI LAUNCH - [/B][/COLOR]' + startup_onoff,BASEURL,112,TOOLS_ICON,FANART,'')
	Common.addItem("[COLOR white][B]SETUP AUTO CLEAR AT SPECIFIC MB - [/B][/COLOR]" + sizecheck_onoff,BASEURL,9,ICON,FANART,'')
	Common.addItem("[COLOR white][B]--------------------------[/B][/COLOR]",BASEURL,79,ICON,FANART,'')
	if check_log == "true":
		Common.addItem(ERRORS_IN_LOG,BASEURL,155,ERROR_ICON,FANART,'')
	Common.addItem('[COLOR white][B]VIEW LOG FILE[/B][/COLOR]',BASEURL,82,ERROR_ICON,FANART,'')
	Common.addItem('[COLOR white][B]VIEW THE LAST ERROR IN LOG FILE[/B][/COLOR]',BASEURL,154,ERROR_ICON,FANART,'')
	if check_log == "true":
		Common.addItem('[COLOR white][B]VIEW ALL ' + str(i) + ' ERROR IN LOG FILE[/B][/COLOR]',BASEURL,155,ERROR_ICON,FANART,'')
	Common.addItem('[COLOR white][B]UPLOAD LOG FILE[/B][/COLOR]','url',36,TOOLS_ICON,FANART,'')
	Common.addItem("[COLOR white][B]--------------------------[/B][/COLOR]",BASEURL,79,ICON,FANART,'')
	Common.addItem('[COLOR white]Auto Clean Device[/COLOR]','url',31,TOOLS_ICON,FANART,'')
	Common.addItem('[COLOR white]Clear Cache[/COLOR]','url',1,TOOLS_ICON,FANART,'')
	Common.addItem('[COLOR white]Delete Crash Logs[/COLOR]','url',25,TOOLS_ICON,FANART,'')
	Common.addItem('[COLOR white]Delete Thumbnails[/COLOR]','url',2,TOOLS_ICON,FANART,'')
	Common.addItem('[COLOR white]Purge Packages[/COLOR]','url',3,TOOLS_ICON,FANART,'')
	Common.addItem('[COLOR white]Check for Broken Repositories[/COLOR]','url',147,TOOLS_ICON,FANART,'')
	Common.addItem('[COLOR white]Check for Broken Sources in sources.xml[/COLOR]','url',148,TOOLS_ICON,FANART,'')
	Common.addItem('[COLOR white]Reload Skin[/COLOR]','url',124,TOOLS_ICON,FANART,'')
	Common.addItem('[COLOR white]Update Addons and Repositories[/COLOR]','url',125,TOOLS_ICON,FANART,'')
	Common.addItem('[COLOR white]Ruya Empty List Fix[/COLOR]','url',109,TOOLS_ICON,FANART,'')
	Common.addItem('[COLOR white]Fix Addon Update Errors (Remove Addon Database)[/COLOR]','url',10,TOOLS_ICON,FANART,'')
	Common.addItem('[COLOR white]Convert Physical Paths To Special[/COLOR]','url',13,TOOLS_ICON,FANART,'')
	Common.addItem('[COLOR white]Hide All Passwords[/COLOR]','url',26,TOOLS_ICON,FANART,'')
	Common.addItem('[COLOR white]Unhide All Passwords[/COLOR]','url',37,TOOLS_ICON,FANART,'')
	Common.addItem('[COLOR white]Base64 - Encode | Decode[/COLOR]','url',117,TOOLS_ICON,FANART,'')
	Common.addItem('[COLOR white]Turn Debugging On/Off[/COLOR]','url',127,TOOLS_ICON,FANART,'')
	Common.addItem('[COLOR white]Open Addon Settings (Exodus, SALTS, Specto)[/COLOR]','url',126,TOOLS_ICON,FANART,'')
	Common.addItem('[COLOR white]Force Close Kodi[/COLOR]','url',86,TOOLS_ICON,FANART,'')
	Common.addDir('[B][COLOR red]SYSTEM RESET(CAUTION)[/COLOR][/B]','url',6,TOOLS_ICON,FANART,'')

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)
	
#######################################################################
#		KEYMAPS MENU for keymap.xml FILES
#######################################################################

def KEYMAPS():

	namelist=[]
	urllist=[]
	countlist=[]
	totallist=[]
	iconlist=[]
	fanartlist=[]
	link = Common.OPEN_URL(KeymapsURL).replace('\n','').replace('\r','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)".+?ash="(.+?)"').findall(link)
	if os.path.isfile(KEYBOARD_FILE):
		Common.addItem('[COLOR white][B]Remove Current Keymap Configuration[/B][/COLOR]',BASEURL,128,ICON,FANART,'')
	for name,url,iconimage,fanart,version,description in match:
		name2 = name
		url = name2 + "|SPLIT|" + url
		name = "[COLOR white][B]" + name + "[/B][/COLOR]"
		namelist.append(name)
		urllist.append(url)
		countlist.append(str(Common.count(name2,TEMP_FILE)))
		totallist.append(str(Common.count(name2+"TOTAL_COUNT",TEMP_FILE)))
		iconlist.append(iconimage)
		fanartlist.append(fanart)
		combinedlists = list(zip(countlist,totallist,namelist,urllist,iconlist,fanartlist))
	tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
	for count,total,name,url,iconimage,fanart in tup:
		bname = " | [COLOR white] This Week:[/COLOR][COLOR yellowgreen][B] " + count + "[/B][/COLOR][COLOR white] - Total:[/COLOR][COLOR yellowgreen][B] " + total + "[/B][/COLOR]"
		Common.addItem(name + bname,url,130,ADVANCED_SET_ICON,FANART,description)

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#		ADVANCED SETTINGS MENU for advancedsettings.xml FILES
#######################################################################

def ADVANCEDSETTINGS():

	kodi_name = Common.GET_KODI_VERSION()

	namelist=[]
	urllist=[]
	countlist=[]
	totallist=[]
	iconlist=[]
	fanartlist=[]
	link = Common.OPEN_URL(AdvancedSettings).replace('\n','').replace('\r','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)".+?ash="(.+?)"').findall(link)
	if os.path.isfile(ADVANCED_SET_FILE):
		Common.addItem('[COLOR white][B]Remove Current Advanced Settings Configuration[/B][/COLOR]',BASEURL,131,ICON,FANART,'')
	for name,url,iconimage,fanart,version,description in match:
		name2 = name
		url = name2 + "|SPLIT|" + url
		name = "[COLOR white][B]" + name + "[/B][/COLOR]"
		namelist.append(name)
		urllist.append(url)
		countlist.append(str(Common.count(name2,TEMP_FILE)))
		totallist.append(str(Common.count(name2+"TOTAL_COUNT",TEMP_FILE)))
		iconlist.append(iconimage)
		fanartlist.append(fanart)
		combinedlists = list(zip(countlist,totallist,namelist,urllist,iconlist,fanartlist))
	tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
	for count,total,name,url,iconimage,fanart in tup:
	
		if not kodi_name == "Krypton":
			if not "kodi 17" in name.lower():
				name = name.replace(' - Kodi 16','')
				bname = " | [COLOR white] This Week:[/COLOR][COLOR yellowgreen][B] " + count + "[/B][/COLOR][COLOR white] - Total:[/COLOR][COLOR yellowgreen][B] " + total + "[/B][/COLOR]"
				Common.addItem(name + bname,url,98,ADVANCED_SET_ICON,FANART,description)
		else:
			if "kodi 17" in name.lower():
				name = name.replace(' - Kodi 17','')
				bname = " | [COLOR white] This Week:[/COLOR][COLOR yellowgreen][B] " + count + "[/B][/COLOR][COLOR white] - Total:[/COLOR][COLOR yellowgreen][B] " + total + "[/B][/COLOR]"
				Common.addItem(name + bname,url,98,ADVANCED_SET_ICON,FANART,description)

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#				GET FANRIFFIC THEMES SKINS
#######################################################################

def FANRIFFIC_THEMES():

	xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
	version=float(xbmc_version[:4])
	codename = "Decline"

	if version >= 16.0 and version <= 16.9:
		codename = 'Jarvis'
	if version >= 17.0 and version <= 17.9:
		codename = 'Krypton'
	
	if codename == "Jarvis":
		i=0
		dp.create(AddonTitle,"[COLOR blue]We are getting the list of themes from the fanriffic server.[/COLOR]",'[COLOR yellow]Please Wait...[/COLOR]','')	
		dp.update(0)
		namelist=[]
		urllist=[]
		countlist=[]
		totallist=[]
		iconlist=[]
		fanartlist=[]
		link = Common.OPEN_URL(FANRIFFIC_URL_NEW).replace('\n','').replace('\r','')
		link2 = Common.OPEN_URL(FANRIFFIC_URL_OLD).replace('\n','').replace('\r','')
		match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
		match2 = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link2)
		dis_links1 = len(match)
		dis_links2 = len(match2)
		dis_links  = dis_links1 + dis_links2
		for name,url,iconimage,fanart,description in match:
			name2 = name
			url = name2 + "|SPLIT|" + url
			name = "[COLOR white][B]" + name + "[/B][/COLOR]"
			i = i + 1
			dis_count = str(i)
			progress = 100 * int(i)/int(dis_links)
			dp.update(progress,"Getting details from theme " + str(dis_count) + " of " + str(dis_links),"[COLOR white][B]FOUND - [/B] " + name + "[/COLOR]")
			namelist.append(name)
			urllist.append(url)
			countlist.append(str(Common.count(name2,TEMP_FILE)))    
			totallist.append(str(Common.count(name2+"TOTAL_COUNT",TEMP_FILE)))    			
			iconlist.append(iconimage)
			fanartlist.append(fanart)
			combinedlists = list(zip(countlist,totallist,namelist,urllist,iconlist,fanartlist))
		for name,url,iconimage,fanart,description in match2:
			name2 = name
			url = name2 + "|SPLIT|" + url
			name = "[COLOR white][B]" + name + "[/B][/COLOR]"
			i = i + 1
			dis_count = str(i)
			progress = 100 * int(i)/int(dis_links)
			dp.update(progress,"Getting details from theme " + str(dis_count) + " of " + str(dis_links),"[COLOR white][B]FOUND - [/B] " + name + "[/COLOR]")
			namelist.append(name)
			urllist.append(url)
			countlist.append(str(Common.count(name2,TEMP_FILE)))   
			totallist.append(str(Common.count(name2+"TOTAL_COUNT",TEMP_FILE)))    			
			iconlist.append(iconimage)
			fanartlist.append(fanart)
			combinedlists = list(zip(countlist,totallist,namelist,urllist,iconlist,fanartlist))
		tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
		dp.close()
		for count,total,name,url,iconimage,fanart in tup:
			bname = " | [COLOR white] This Week:[/COLOR][COLOR yellowgreen][B] " + count + "[/B][/COLOR][COLOR white] - Total:[/COLOR][COLOR yellowgreen][B] " + total + "[/B][/COLOR]"
			Common.addItem(name + bname,url,145,iconimage,iconimage,description="")

	elif codename == "Krypton":
		i=0
		dp.create(AddonTitle,"[COLOR blue]We are getting the list of themes from the fanriffic server.[/COLOR]",'[COLOR yellow]Please Wait...[/COLOR]','')	
		dp.update(0)
		namelist=[]
		urllist=[]
		countlist=[]
		totallist=[]
		iconlist=[]
		fanartlist=[]
		link = Common.OPEN_URL(FANRIFFIC_KRYPTON).replace('\n','').replace('\r','')
		match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
		dis_links = len(match)
		for name,url,iconimage,fanart,description in match:
			name2 = name
			url = name2 + "|SPLIT|" + url
			name = "[COLOR white][B]" + name + "[/B][/COLOR]"
			i = i + 1
			dis_count = str(i)
			progress = 100 * int(i)/int(dis_links)
			dp.update(progress,"Getting details from theme " + str(dis_count) + " of " + str(dis_links),"[COLOR white][B]FOUND - [/B] " + name + "[/COLOR]")
			namelist.append(name)
			urllist.append(url)
			countlist.append(str(Common.count(name2,TEMP_FILE)))    
			totallist.append(str(Common.count(name2+"TOTAL_COUNT",TEMP_FILE)))    
			iconlist.append(iconimage)
			fanartlist.append(fanart)
			combinedlists = list(zip(countlist,totallist,namelist,urllist,iconlist,fanartlist))
		tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
		dp.close()
		for count,total,name,url,iconimage,fanart in tup:
			bname = " | [COLOR white] This Week:[/COLOR][COLOR yellowgreen][B] " + count + "[/B][/COLOR][COLOR white] - Total:[/COLOR][COLOR yellowgreen][B] " + total + "[/B][/COLOR]"
			Common.addItem(name + bname,url,145,iconimage,iconimage,description="")

	#if codename == "Decline":
	#	dialog.ok(AddonTitle,'[COLOR white]Sorry there are no supported themes for your version of Kodi.')
    #   quit()

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#						SPEEDTEST LIST
#######################################################################

def SPEEDTEST():

	link = Common.OPEN_URL('http://pastebin.com/raw/VECYSGBL').replace('\n','').replace('\r','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
	for name,url,iconimage,fanart,description in match:
		Common.addItem('[COLOR ghostwhite]' + name + " | " + description + '[/COLOR]',url,15,SPEEDTEST_ICON,ART+'speedfanart.jpg','')

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

def GET_COUNTS():
	
	api_interval = plugintools.get_setting("api_interval")

	if api_interval == "0":
		mark = 60
	elif api_interval == "1":
		mark = 50
	elif api_interval == "2":
		mark = 40
	elif api_interval == "3":
		mark = 30
	elif api_interval == "4":
		mark = 20
	elif api_interval == "5":
		mark = 10
	elif api_interval == "6":
		mark = 5
	else: mark = 60
	
	fileCreation = os.path.getmtime(TEMP_FILE)
	fileCreation2 = os.path.getmtime(TEMP_ADDONS)

	now = time.time()

	check = now - 60*mark
	
	text_file = open(TEMP_FILE)
	compfile = text_file.read()  
	text_file = open(TEMP_ADDONS)
	compfile2 = text_file.read()  
	
	if len(compfile) == 0:
		counts=Common.OPEN_URL_NORMAL(ECHO_API)

		text_file = open(TEMP_FILE, "w")
		text_file.write(counts)
		text_file.close()

	elif fileCreation < check:

		counts=Common.OPEN_URL_NORMAL(ECHO_API)

		text_file = open(TEMP_FILE, "w")
		text_file.write(counts)
		text_file.close()

	if len(compfile2) == 0:
		counts=Common.OPEN_URL_NORMAL(ADDONS_API)

		text_file = open(TEMP_ADDONS, "w")
		text_file.write(counts)
		text_file.close()

	elif fileCreation2 < check:

		counts=Common.OPEN_URL_NORMAL(ADDONS_API)
		text_file = open(TEMP_ADDONS, "w")
		text_file.write(counts)
		text_file.close()
		

#######################################################################
#						BACKUP MENU MENU
#######################################################################
	
def BACKUPMENU():

	Common.addItem('[COLOR yellowgreen][B]BACKUP OPTIONS[/B][/COLOR]','url',22,BACKUP_ICON,FANART,'')	
	Common.addItem('[COLOR white]Full Backup (All Files and Folders Included)[/COLOR]','url',69,BACKUP_ICON,FANART,'')	
	Common.addItem('[COLOR white]Backup for Builds (Exc: Thumbnails, Databases)[/COLOR]','url',70,BACKUP_ICON,FANART,'')
	Common.addItem('[COLOR white]Backup Addon Data[/COLOR]','url',108,BACKUP_ICON,FANART,'')
	Common.addItem('[COLOR white]Backup RD & Trakt Settings[/COLOR]','url',103,BACKUP_ICON,FANART,'')
	Common.addItem('[COLOR white]Backup ECHO TV Guide Settings[/COLOR]','url',107,BACKUP_ICON,FANART,'')
	Common.addItem('[COLOR yellowgreen][B]RESTORE OPTIONS[/B][/COLOR]','url',22,BACKUP_ICON,FANART,'')	
	Common.addDir('[COLOR white]Restore A Backup - (Full/Builds)[/COLOR]','url',71,BACKUP_ICON,FANART,'')
	Common.addDir('[COLOR white]Restore Addon Data[/COLOR]','url',71,BACKUP_ICON,FANART,'')
	Common.addDir('[COLOR white]Restore RD & Trakt Settings[/COLOR]','url',104,BACKUP_ICON,FANART,'')
	Common.addDir('[COLOR white]Restore ECHO TV Guide Settings[/COLOR]','url',71,BACKUP_ICON,FANART,'')
	Common.addItem('[COLOR yellowgreen][B]OTHER OPTIONS[/B][/COLOR]','url',22,BACKUP_ICON,FANART,'')	
	Common.addDir('[COLOR white]Delete A Backup[/COLOR]','url',72,BACKUP_ICON,FANART,'')
	Common.addItem('[COLOR white]Delete All Backups[/COLOR]','url',73,BACKUP_ICON,FANART,'')
	Common.addItem('[COLOR white]Select Backup Location[/COLOR]','url',9,BACKUP_ICON,FANART,'')

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#					LATEST SPORTS LISTINGS
#######################################################################

def SPORT_LISTINGS():

	url = base64.b64decode(b'aHR0cDovL3d3dy53aGVyZXN0aGVtYXRjaC5jb20vdHYvaG9tZS5hc3A=')
	r = Common.OPEN_URL_NORMAL(url).replace('\r','').replace('\n','').replace('\t','')
	match = re.compile('href="http://www.wheresthematch.com/fixtures/(.+?).asp.+?class="">(.+?)</em> <em class="">v</em> <em class="">(.+?)</em>.+?time-channel ">(.+?)</span>').findall(r)
	for game,name1,name2,gametime in match:
		a,b = gametime.split(" on ")
		Common.addItem('[COLOR white]'+name1+' vs '+name2+' - '+a+' [/COLOR]','','',ICON,FANART,'')
		Common.addItem('[COLOR yellowgreen][B]Watch on '+b+'[/B][/COLOR]','','',ICON,FANART,'')
		Common.addItem('------------------------------------------','','',ICON,FANART,'')

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#		DISPLAYS USER INFO LIKE IP ADDRESS ETC
#######################################################################

def ACCOUNT():

	#######################################################################
	#			FIND WHAT VERSION OF KODI IS RUNNING
	#######################################################################

	xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
	version=float(xbmc_version[:4])

	if version >= 11.0 and version <= 11.9:
		codename = 'Eden'
	if version >= 12.0 and version <= 12.9:
		codename = 'Frodo'
	if version >= 13.0 and version <= 13.9:
		codename = 'Gotham'
	if version >= 14.0 and version <= 14.9:
		codename = 'Helix'
	if version >= 15.0 and version <= 15.9:
		codename = 'Isengard'
	if version >= 16.0 and version <= 16.9:
		codename = 'Jarvis'
	if version >= 17.0 and version <= 17.9:
		codename = 'Krypton'

	f = urllib.urlopen("http://www.canyouseeme.org/")
	html_doc = f.read()
	f.close()
	m = re.search('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',html_doc)
	
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))

	if check=="true":
		a = "[COLOR yellowgreen]Yes[/COLOR]"
	else:
		a = "[COLOR yellowgreen]No[/COLOR]"

	Common.addItem('[COLOR ghostwhite]Version: [/COLOR][COLOR yellowgreen]%s' % version + " " + codename + "[/COLOR]",BASEURL,200,SYSTEM_INFO_ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite]Check For Updates: [/COLOR]' + a,BASEURL,200,SYSTEM_INFO_ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite]Local IP: [/COLOR][COLOR white]' + s.getsockname()[0] + '[/COLOR]',BASEURL,200,SYSTEM_INFO_ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite]External IP: [/COLOR][COLOR white]' + m.group(0) + '[/COLOR]',BASEURL,200,SYSTEM_INFO_ICON,FANART,'')

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#		MUST HAVE KODI PROGRAMS AND TOOLS MENU
#######################################################################

def KODI_TOOLS():

	link = Common.OPEN_URL(TOOLS).replace('\n','').replace('\r','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
	for name,url,iconimage,fanart,description in match:
		Common.addItem(name,url,89,KODI_ICON,KODI_FANART,description)

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#		LIST OF LATEST KODI INSTALLATION FILES
#######################################################################

def LATEST_LIST():

	if xbmc.getCondVisibility('system.platform.windows'):
		LATEST_WINDOWS()

	elif xbmc.getCondVisibility('system.platform.osx'):
		LATEST_OSX()

	elif xbmc.getCondVisibility('system.platform.darwin'):
		LATEST_OSX()

	elif xbmc.getCondVisibility('system.platform.ios'):
		LATEST_IOS()

	elif xbmc.getCondVisibility('system.platform.android'):
		LATEST_ANDROID()
	else:
	
		if xbmc.getCondVisibility('system.platform.linux'):
			platform_name = "Linux"
		elif xbmc.getCondVisibility('system.platform.linuxraspberrypi'):
			platform_name = "Raspberry Pi"
		elif xbmc.getCondVisibility('system.platform.darwin'):
			platform_name = "Linux"
		elif xbmc.getCondVisibility('system.platform.atv2'):
			platform_name = "Apple TV 2"
		elif xbmc.getCondVisibility('system.platform.atv4'):
			platform_name = "Apple TV 4"
		else: platform_name = "Unknown"
		
		Common.addItem('[COLOR white][B]Detected Platform: [/B][/COLOR][COLOR yellowgreen]' + platform_name + '[/COLOR]',url,999,ICON,FANART,'')
		Common.addItem('No installation files found for this platform.',url,999,ICON,FANART,'')

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#					GETS THE WINDOWS LIST
#######################################################################

def LATEST_WINDOWS():

	if not xbmc.getCondVisibility('system.platform.windows'):
		dialog = xbmcgui.Dialog()
		dialog.ok(AddonTitle + " - Windows", "[B][COLOR white]Sorry, this function is only available for Windows devices[/COLOR][/B]",'[COLOR white]Thank you for using ECHO Wizard[/COLOR]')
		sys.exit(1)
	else:
		link = Common.OPEN_URL(WINDOWS).replace('\n','').replace('\r','')
		match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
		Common.addItem('[COLOR yellowgreen][B]EXE Will Be Donwloaded to [COLOR yellowgreen]special://Downloads[/COLOR] You Will Need To Manually Install From There[/B][/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		Common.addItem('[COLOR white]-----------------------------------------------------------[/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		for name,url,iconimage,fanart,description in match:
			Common.addItem(name,url,89,KODI_ICON,KODI_FANART,description)

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#					GETS THE OSX LIST
#######################################################################
			
def LATEST_OSX():

	if not xbmc.getCondVisibility('system.platform.osx'):
		dialog = xbmcgui.Dialog()
		dialog.ok(AddonTitle + " - OSX", "[B][COLOR white]Sorry, this function is only available for OSX devices[/COLOR][/B]",'[COLOR white]Thank you for using ECHO Wizard[/COLOR]')
		sys.exit(1)
	else:
		link = Common.OPEN_URL(OSX).replace('\n','').replace('\r','')
		match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
		Common.addItem('[COLOR yellowgreen][B].dmg Will Be Donwloaded to [COLOR yellowgreen]special://Downloads[/COLOR] You Will Need To Manually Install From There[/B][/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		Common.addItem('[COLOR white]-----------------------------------------------------------[/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		for name,url,iconimage,fanart,description in match:
			Common.addItem(name,url,89,KODI_ICON,KODI_FANART,description)

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)
	
#######################################################################
#					GETS THE IOS LIST
#######################################################################

def LATEST_IOS():

	if not xbmc.getCondVisibility('system.platform.ios'):
		dialog = xbmcgui.Dialog()
		dialog.ok(AddonTitle + " - iOS", "[B][COLOR white]Sorry, this function is only available for iOS devices[/COLOR][/B]",'[COLOR white]Thank you for using ECHO Wizard[/COLOR]')
		sys.exit(1)
	else:
		link = Common.OPEN_URL(IOS).replace('\n','').replace('\r','')
		match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
		Common.addItem('[COLOR yellowgreen][B].deb Will Be Donwloaded to [COLOR yellowgreen]special://Downloads[/COLOR] You Will Need To Manually Install From There[/B][/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		Common.addItem('[COLOR white]-----------------------------------------------------------[/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		for name,url,iconimage,fanart,description in match:
			Common.addItem(name,url,89,KODI_ICON,KODI_FANART,description)

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#					GETS THE ANDROID LIST
#######################################################################

def LATEST_ANDROID():

	if not xbmc.getCondVisibility('system.platform.android'):
		dialog = xbmcgui.Dialog()
		dialog.ok(AddonTitle + " - Android", "[B][COLOR white]Sorry, this function is only available for Android devices[/COLOR][/B]",'[COLOR white]Thank you for using ECHO Wizard[/COLOR]')
		sys.exit(1)
	else:
		link = Common.OPEN_URL(APKS).replace('\n','').replace('\r','')
		match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
		Common.addItem('[COLOR yellowgreen][B]APKS Will Be Donwloaded to [COLOR yellowgreen]/sdcard/Downloads[/COLOR] You Will Need To Manually Install From There[/B][/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		Common.addItem('[COLOR white]-----------------------------------------------------------[/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		Common.addDir('[COLOR yellowgreen]CLICK FOR THE LATEST SIGNED KODI/SPMC APKS WITH UP TO DATE LIB FILE INCLUDED IN APK[/COLOR]',BASEURL,32,APK_ICON,FANART,'')
		for name,url,iconimage,fanart,description in match:
			Common.addItem(name,url,91,iconimage,fanart,description)

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#					INSTALLER LIST
#######################################################################

def INSTALLER_APKS():

	#FOR ADDON INSTALLER
	if not xbmc.getCondVisibility('system.platform.android'):
		dialog = xbmcgui.Dialog()
		dialog.ok(AddonTitle + " - Android", "[B][COLOR white]Sorry, this function is only available for Android devices[/COLOR][/B]",'[COLOR white]Thank you for using ECHO Wizard[/COLOR]')
		sys.exit(1)
	else:
		dp.create(AddonTitle,"[COLOR blue]We are getting the addons from our server.[/COLOR]",'','')	
		i=0
		namelist=[]
		countlist=[]
		iconlist=[]
		fanartlist=[]
		urllist=[]
		link = Common.OPEN_URL(APKS_INSTALLER).replace('\n','').replace('\r','')
		dp.update(0)
		match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)"').findall(link)
		dis_links = len(match)
		for name,url,iconimage,fanart in match:
			i = i + 1
			dis_count = str(i)
			progress = 100 * int(i)/int(dis_links)
			dp.update(progress,"Filtering pack " + str(dis_count) + " of " + str(dis_links),"[COLOR grey][B]Found " + name + "[/B][/COLOR]")
			namelist.append(name)
			countlist.append(str(Common.count_addons_week(name)))
			iconlist.append(iconimage)
			fanartlist.append(fanart)
			urllist.append(url)
			combinedlists = list(zip(countlist,namelist,iconlist,fanartlist,urllist))
		tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
		for count,name,iconimage,fanart,url in tup:
			url2 = name + "#!" + url
			bname = " | [COLOR white] This Week:[/COLOR][COLOR yellowgreen][B] " + count + "[/B][/COLOR]"
			Common.addItem("[COLOR white][B]" + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,171,iconimage,fanart,description="None")

		view_mode = SET_VIEW("list")
		xbmc.executebuiltin(view_mode)
	
#######################################################################
#					GETS THE LATEST SIGNED APKS LIST
#######################################################################

def LATESTAPKSWITHLIB():

	link = Common.OPEN_URL(APKSLIB).replace('\n','').replace('\r','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
	Common.addItem('[COLOR yellowgreen][B]APKS Will Be Donwloaded to [COLOR yellowgreen]/sdcard/Downloads[/COLOR] You Will Need To Manually Install From There[/B][/COLOR]',BASEURL,79,APK_ICON,FANART,'')
	Common.addItem('[COLOR white]-----------------------------------------------------------[/COLOR]',BASEURL,79,APK_ICON,FANART,'')
	for name,url,iconimage,fanart,description in match:
		Common.addDir(name,url,91,iconimage,fanart,description)

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#					GETS THE LIBRTMP FILES LIST
#######################################################################

def DOWNLOADLIB():

	link = Common.OPEN_URL(LIB).replace('\n','').replace('\r','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
	Common.addItem('[COLOR yellowgreen][B]Lib Files Will Be Donwloaded to [COLOR yellowgreen]the Kodi special directory[/COLOR] You Will Need To Manually Install From There. The Windows Lib File will Auto Install[/B][/COLOR]',BASEURL,79,LIB_ICON,FANART,'')
	Common.addItem('[COLOR white]-----------------------------------------------------------[/COLOR]',BASEURL,79,LIB_ICON,FANART,'')
	for name,url,iconimage,fanart,description in match:
		Common.addDir(name,url,94,LIB_ICON,fanart,description)

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#					ANDROID APKS
#######################################################################

def ANDROID_APKS():

	if not xbmc.getCondVisibility('system.platform.android'):
		dialog = xbmcgui.Dialog()
		dialog.ok(AddonTitle + " - Android", "[B][COLOR white]Sorry, this function is only available for Android devices[/COLOR][/B]",'[COLOR white]Thank you for using ECHO Wizard[/COLOR]')
		sys.exit(1)
	else:
		link = Common.OPEN_URL(AND_APKS).replace('\n','').replace('\r','')
		match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)"').findall(link)
		Common.addItem('[COLOR yellowgreen][B]APKS Will Be Donwloaded to [COLOR yellowgreen]/sdcard/Downloads[/COLOR][/B][/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		Common.addItem('[COLOR dodgerblue][B]THIS LIST IS MAINTAINED BY @VULCAN_TDB [/B][/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		Common.addItem('[COLOR dodgerblue][B]CONTACT HIM ON TWITTER WITH REQUESTS[/B][/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		Common.addItem('[COLOR white]-----------------------------------------------------------[/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		for name,url,iconimage,fanart in match:
			Common.addItem(name,url,91,iconimage,fanart,'')

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#					ESSENTIAL CONTACTS LIST
#######################################################################

def KODI_CONTACTS():

	link = Common.OPEN_URL(CONTACTS)
	patron = "<video>(.*?)</video>"
	videos = re.findall(patron,link,re.DOTALL)
	items = []
	for video in videos:
		item = {}
		item["name"] = Common.find_single_match(video,"<name>([^<]+)</name>")
		item["url"] = Common.find_single_match(video,"<url>([^<]+)</url>")
		item["description"] = Common.find_single_match(video,"<description>([^<]+)</description>")

		if "NULL" in item["description"]:
			Common.addItem(item["name"] + '[COLOR white]@[/COLOR][COLOR white]' + item["url"] + '[/COLOR]',BASEURL,666,ICON,FANART,'')
		else:
			Common.addDir(item["name"] + '[COLOR white]@[/COLOR][COLOR white]' + item["url"] + '[/COLOR]',BASEURL,102,ICON,FANART,item["description"])

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#					SET VIEW
#######################################################################

def SET_VIEW(name):

	kodi_name = Common.GET_KODI_VERSION()

	if name == "list":
		if kodi_name == "Jarvis":
			command = '"Container.SetViewMode(50)"'
		elif kodi_name == "Krypton":
			command = '"Container.SetViewMode(55)"'
		else: command = '"Container.SetViewMode(50)"'
	elif name == "thumbs":
		if kodi_name == "Jarvis":
			command = '"Container.SetViewMode(500)"'
		elif kodi_name == "Krypton":
			command = '"Container.SetViewMode(52)"'
		else: command = '"Container.SetViewMode(500)"'
	else:
		if kodi_name == "Jarvis":
			command = '"Container.SetViewMode(50)"'
		elif kodi_name == "Krypton":
			command = '"Container.SetViewMode(55)"'
		else: command = '"Container.SetViewMode(50)"'
		
	return command

#######################################################################
#					VIEW CHANGELOG
#######################################################################

def VIEW_CHANGELOG():

	f = open(CHANGELOG,mode='r'); msg = f.read(); f.close()
	Common.TextBoxesPlain("%s" % msg)

#######################################################################
#					HOW TO GET SUPPORT
#######################################################################

def GET_SUPPORT():

	f = requests.get(SUPPORT)
	Common.TextBoxesPlain("%s" % f.text)

#######################################################################
#					ADD TO COMMUNITY BUILDS
#######################################################################

def ADD_COMMUNITY_BUILD():

	f = requests.get(ADD_COMMUNITY)
	Common.TextBoxesPlain("%s" % f.text)

#######################################################################
#					LATEST ECHO NEWS
#######################################################################

def LATEST_NEWS():

	f = requests.get(NEWS)
	Common.TextBoxesPlain("%s" % f.text)

#######################################################################
#					ECHO DONATIONS
#######################################################################

def DONATIONS_LINK():

	f = requests.get(DONATIONS_URL)
	Common.TextBoxesPlain("%s" % f.text)

#######################################################################
#					ECHO WIZARD CREDITS
#######################################################################

def VIEW_CREDITS():

	f = requests.get(CREDITS)
	Common.TextBoxesPlain("%s" % f.text)

#######################################################################
#					REMOVE KEYBOARD.XML FILE
#######################################################################

def REMOVE_KEYBOARD_FILE():

	try:
		os.remove(KEYBOARD_FILE)
	except:
		dialog.ok(AddonTitle, "[B][COLOR white]Sorry, ECHO Wizard encountered an error[/COLOR][/B]",'[COLOR white]We were unable to remove the keyboard.xml file.[/COLOR]')
		sys.exit(0)
		
	dialog.ok(AddonTitle, "[B][COLOR white]Success, we have removed the keyboards.xml file.[/COLOR][/B]",'[COLOR white]Thank you for using ECHO Wizard[/COLOR]')
	xbmc.executebuiltin("Container.Refresh")

#######################################################################
#					REMOVE ADVANCEDSETTINGS.XML FILE
#######################################################################

def REMOVE_ADVANCED_FILE():

	try:
		os.remove(ADVANCED_SET_FILE)
	except:
		dialog.ok(AddonTitle, "[B][COLOR white]Sorry, ECHO Wizard encountered an error[/COLOR][/B]",'[COLOR white]We were unable to remove the keyboard.xml file.[/COLOR]')
		sys.exit(0)
		
	dialog.ok(AddonTitle, "[B][COLOR white]Success, we have removed the advancedsettings.xml file.[/COLOR][/B]",'[COLOR white]Thank you for using ECHO Wizard[/COLOR]')
	xbmc.executebuiltin("Container.Refresh")

#######################################################################
#			AUTO UPDATER
#######################################################################

def AUTO_UPDATER(name):

	GET_VERSION         =  xbmc.translatePath('special://home/addons/' + addon_id + '/addon.xml')
	GET_REPO_VERSION    =  xbmc.translatePath('special://home/addons/repository.echo/addon.xml')
	BASE_UPDATE         = base64.b64decode(b'aHR0cHM6Ly9naXRodWIuY29tL2VjaG9jb2RlcmtvZGkvcmVwb3NpdG9yeS5lY2hvL3Jhdy9tYXN0ZXIvemlwcy9wbHVnaW4ucHJvZ3JhbS5lY2hvd2l6YXJkL3BsdWdpbi5wcm9ncmFtLmVjaG93aXphcmQt')
	BASE_REPO_UPDATE    = base64.b64decode(b'aHR0cHM6Ly9naXRodWIuY29tL2VjaG9jb2RlcmtvZGkvcmVwb3NpdG9yeS5lY2hvL3Jhdy9tYXN0ZXIvemlwcy9yZXBvc2l0b3J5LmVjaG8vcmVwb3NpdG9yeS5lY2hvLQ==')
	BASE_XXX_UPDATE     = base64.b64decode(b'aHR0cHM6Ly9naXRodWIuY29tL2VjaG9jb2RlcmtvZGkvcmVwb3NpdG9yeS54eHhlY2hvL3Jhdy9tYXN0ZXIvemlwcy9yZXBvc2l0b3J5Lnh4eGVjaG8vcmVwb3NpdG9yeS54eHhlY2hvLQ==')
	XXX_REPO            = xbmc.translatePath('special://home/addons/repository.xxxecho')
	GET_XXX_VERSION     =  xbmc.translatePath('special://home/addons/repository.xxxecho/addon.xml')
	found = 0

	try:
		Common.OPEN_URL_NORMAL("http://www.google.com")
	except:
		dialog.ok(AddonTitle,'[COLOR red][B]Error: It appears you do not currently have an active internet connection. This will cause false positives in the test. Please try again with an active internet connection.[/B][/COLOR]')
		sys.exit(0)

	try:
		dp.create(AddonTitle,"Checking for repository updates",'', 'Please Wait...')	
		dp.update(0)
		a=open(GET_REPO_VERSION).read()
		b=a.replace('\n',' ').replace('\r',' ')
		match=re.compile('name=".+?".+?version="(.+?)".+?provider-name=".+?">').findall(str(b))
		for item in match:
			dp.update(25)
			new_version = float(item) + 0.01
			url = BASE_REPO_UPDATE + str(new_version) + '.zip'
			result = requests.get(url)
			if "Not Found" not in result.content:
				found = 1
				dp.update(75)
				path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
				if not os.path.exists(path):
					os.makedirs(path)
				lib=os.path.join(path, 'repoupdate.zip')
				try: os.remove(lib)
				except: pass
				dp.update(100)
				dp.update(0,"","Downloading Update Please Wait","")
				import downloader
				downloader.download(url, lib, dp)
				addonfolder = xbmc.translatePath(os.path.join('special://','home/addons'))
				dp.update(0,"","Extracting Update Please Wait","")
				import extract
				extract.all(lib,addonfolder,dp)
				try: os.remove(lib)
				except: pass
				xbmc.executebuiltin("UpdateLocalAddons")
				xbmc.executebuiltin("UpdateAddonRepos")
				dialog.ok(AddonTitle,"ECHO repository was updated to " + str(new_version) + ', you may need to restart the addon for changes to take effect')

		if os.path.exists(XXX_REPO):
			dp.update(50,"Checking for XXX repository updates")
			a=open(GET_XXX_VERSION).read()
			b=a.replace('\n',' ').replace('\r',' ')
			match=re.compile('name=".+?".+?version="(.+?)".+?provider-name=".+?">').findall(str(b))
			for item in match:
				new_version = float(item) + 0.01
				url = BASE_XXX_UPDATE + str(new_version) + '.zip'
				result = requests.get(url)
				if "Not Found" not in result.content:
					found = 1
					dp.update(75)
					path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
					if not os.path.exists(path):
						os.makedirs(path)
					lib=os.path.join(path, 'repoupdate.zip')
					try: os.remove(lib)
					except: pass
					dp.update(100)
					dp.update(0,"","Downloading Update Please Wait","")
					import downloader
					downloader.download(url, lib, dp)
					addonfolder = xbmc.translatePath(os.path.join('special://','home/addons'))
					dp.update(0,"","Extracting Update Please Wait","")
					import extract
					extract.all(lib,addonfolder,dp)
					try: os.remove(lib)
					except: pass
					xbmc.executebuiltin("UpdateLocalAddons")
					xbmc.executebuiltin("UpdateAddonRepos")
					dialog.ok(AddonTitle,"ECHO XXX repository was updated to " + str(new_version) + ', you may need to restart the addon for changes to take effect')

		dp.update(75,"Checking for addon updates")
		a=open(GET_VERSION).read()
		b=a.replace('\n',' ').replace('\r',' ')
		match=re.compile('name=".+?".+?version="(.+?)".+?provider-name=".+?">').findall(str(b))
		for item in match:
			new_version = float(item) + 0.01
			url = BASE_UPDATE + str(new_version) + '.zip'
			result = requests.get(url)
			if "Not Found" not in result.content:
				found = 1
				dp.update(75)
				path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
				if not os.path.exists(path):
					os.makedirs(path)
				lib=os.path.join(path, 'wizupdate.zip')
				try: os.remove(lib)
				except: pass
				dp.update(100)
				dp.update(0,"","Downloading Update Please Wait","")
				import downloader
				downloader.download(url, lib, dp)
				addonfolder = xbmc.translatePath(os.path.join('special://','home/addons'))
				dp.update(0,"","Extracting Update Please Wait","")
				import extract
				extract.all(lib,addonfolder,dp)
				try: os.remove(lib)
				except: pass
				xbmc.executebuiltin("UpdateLocalAddons")
				xbmc.executebuiltin("UpdateAddonRepos")
				dp.update(100)
				dp.close
				dialog.ok(AddonTitle,"ECHO Wizard was updated to " + str(new_version) + ', you may need to restart the addon for changes to take effect')
	except:
		dialog.ok(AddonTitle,'Sorry! We encountered an error whilst checking for updates. You can make Kodi force check the repository for updates as an alternative if you wish.')
		quit()

	if dp.iscanceled():
		dp.close()
	else:
		if found == 0:
			if not name == "no dialog":
				dialog.ok(AddonTitle,"There are no updates at this time.")
				quit()

#######################################################################
#					PLAY VIDEO FUNCTION
#######################################################################

def PLAYVIDEO(url):
	xbmc.Player().play(url)
	
def GETTEMP():

	TEMP_FOLDER   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id,'temp'))
	TEMP_BUILDS   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id,'temp/temp.xml'))
	TEMP_ADDONS   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id,'temp/temp_installer.xml'))
	BASEURL       =  base64.b64decode(b'aHR0cDovL2VjaG9jb2Rlci5jb20v')
	BUILDS_API    =  BASEURL + base64.b64decode(b'YXBpL2FwaS5waHA/c2VydmljZT1idWlsZHMmYWN0aW9uPWNvdW50')
	ADDONS_API    =  BASEURL + base64.b64decode(b'YXBpL2FwaS5waHA/c2VydmljZT1hZGRvbnMmYWN0aW9uPWNvdW50')
	dialog        =  xbmcgui.Dialog()
	passed        =  0

	dp.create(AddonTitle, "[COLOR yellowgreen][B]Connecting to the ECHO Wizard API....[/B][/COLOR]")
	dp.update(0)

	if os.path.exists(TEMP_FOLDER):
		
		try:
			shutil.rmtree(TEMP_FOLDER)
		except: pass

	try:
		if not os.path.exists(TEMP_FOLDER):
			os.makedirs(TEMP_FOLDER)

		if not os.path.isfile(TEMP_BUILDS):
			open(TEMP_BUILDS, 'w')
		if not os.path.isfile(TEMP_ADDONS):
			open(TEMP_ADDONS, 'w')
	except: pass
		
	try:
		dp.update(50, '[COLOR yellowgreen][B]Connected![/B][/COLOR]','[COLOR white]Getting build information from the API.[/COLOR]')
		req = urllib2.Request(BUILDS_API)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36')
		response = urllib2.urlopen(req)
		counts=response.read()
		response.close()
		text_file = open(TEMP_BUILDS, "w")
		text_file.write(counts)
		text_file.close()

		dp.update(75, '','[COLOR white]Getting addon installer information from the API.[/COLOR]')
		req = urllib2.Request(ADDONS_API)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36')
		response = urllib2.urlopen(req)
		counts=response.read()
		response.close()
		text_file = open(TEMP_ADDONS, "w")
		text_file.write(counts)
		text_file.close()

		dp.update(100, '','[COLOR dodgerblue]Finishing up.[/COLOR]')
		dp.close()
		dialog.ok(AddonTitle, "We have successfully genenerated the ECHO download counters.")
		passed = 1
		quit()
	except: pass
		
	if passed == 0:
		dp.close()
		dialog.ok(AddonTitle, "There was an error generating the download counters. Please try again later.")
		quit()

def CLEARTEMP():

	dp.create(AddonTitle, "[COLOR yellowgreen]Removing ECHO Wizard temp files.[/COLOR]")
	
	TEMP_FOLDER      =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id,'temp'))

	if os.path.exists(TEMP_FOLDER):
		
		try:
			shutil.rmtree(TEMP_FOLDER)
		except:
			dp.close()
			dialog.ok(AddonTitle, "There was an error removing the ECHO temp files.")
			quit()
		dp.close()
		dialog.ok(AddonTitle, "We have succesfully removed the ECHO temp files.")
		quit()

	else:
		dp.close()
		dialog.ok(AddonTitle, "No temp files could be found.")
		quit()

#######################################################################
#					OPEN THE SETTINGS DIALOG
#######################################################################

def OPEN_SETTINGS(params):
    plugintools.open_settings_dialog()

##############################    END    #########################################

##################################################################################
#						Which mode to select
#######################################################################

params=parameters.get_params()

url=None
name=None
mode=None
iconimage=None
fanart=None
description=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass

if mode==None or url==None or len(url)<1:
        INDEX()
		
elif mode==1:
		maintenance.clearCache()
        
elif mode==2:
		maintenance.deleteThumbnails()

elif mode==3:
		maintenance.purgePackages()

elif mode==4:
		ACCOUNT()
		
elif mode==5:
        MAINTENANCE_MENU()

elif mode==6:        
		wipe.FRESHSTART()
		
elif mode==7:
        COMINGSOON()

elif mode==8:
        BACKUPMENU()
		
elif mode==9:
        OPEN_SETTINGS(params)
		
elif mode==10:
        maintenance.deleteAddonDB()

elif mode==11:
        update.updateaddons()
		
elif mode==12:
        xbmc.executebuiltin("RunAddon(plugin.program.echowizard)")
		
elif mode==13:
        maintenance.Fix_Special(url)

elif mode==14:
        versioncheck.XBMC_Version()
		
elif mode==15:
        speedtest.runtest(url)
		
elif mode==16:
        SPEEDTEST()

elif mode==17:
       ADD_COMMUNITY_BUILD()

elif mode==18:
       community.CommunityUpdateNotice()

elif mode==22:
        GET_SUPPORT()

elif mode==25:
		maintenance.DeleteCrashLogs()
		
elif mode==26:
		maintenance.HidePasswords()

elif mode==27:
		maintenance.lib()

elif mode==28:
		LATEST_LIST()
	
elif mode==29:
		DOWNLOADLIB()
		
elif mode==30:
		ADVANCEDSETTINGS()
		
elif mode==31:
		maintenance.autocleanask()
		
elif mode==32:
		LATESTAPKSWITHLIB()
		
elif mode==33:
        update.check()

elif mode==35:
        maintenance.viewLogFile()
		
elif mode==36:
        uploadlog.main(argv=None)

elif mode==37:
		maintenance.UnhidePasswords()
		
elif mode==40:
		LATEST_WINDOWS()
		
elif mode==41:
		LATEST_ANDROID()
		
elif mode==42:
		LATEST_IOS()
		
elif mode==43:
		LATEST_OSX()

elif mode==44:
        versioncheck.BUILD_Version()

elif mode==46:
        KODI_TOOLS()

elif mode==47:
        SPORT_LISTINGS()
		
elif mode==49:
		dialog.ok(AddonTitle, url )

elif mode==50:
        BUILDMENU()

elif mode==58:
	Common.WriteReview(url)

elif mode==59:
	Common.ListReview(url)

elif mode==60:
        youtube.MAINMENU()
		
elif mode==61:
        youtube.LOADLIST(name,url)
		
elif mode==62:
        youtube.LOADITEM(name,url)
		
elif mode==63:
        youtube.OTHER_CHANNELS(url)
		
elif mode==64:
        search.YOUTUBE()
		
elif mode==65:
        search.COMMUNITY()
		
elif mode==66:
        search.BUILDS()
		
elif mode==67:
        search.ALL()

elif mode==69:
        backuprestore.FullBackup()

elif mode==70:
        backuprestore.Backup()
		
elif mode==71:
        backuprestore.Restore()
	
elif mode==72:
        backuprestore.ListBackDel()
		
elif mode==73:
        backuprestore.DeleteAllBackups()
		
elif mode==74:
        extras.EXTRAS_MENU()
		
elif mode==75:
        extras.HORUS_INTRO()
		
elif mode==76:
        extras.ENABLE_HORUS_INTRO()

elif mode==77:
        extras.SPMC_MINIMIZE()

elif mode==79:
        GET_SUPPORT()
		
elif mode==80:
        VIEW_CHANGELOG()
		
elif mode==81:
        VIEW_CREDITS()

elif mode==82:
        maintenance.viewLogFile()

elif mode==83:
        Common.BUILDER(name,url,iconimage,fanart,description)

elif mode==84:
        KODI_CONTACTS()

elif mode==85:
        print "############   ATTEMPT TO KILL XBMC/KODI   #################"
        Common.killxbmc()

elif mode==86:
        print "############   ATTEMPT TO KILL XBMC/KODI   #################"
        Common.KillKodi()

elif mode==87:
       community.COMMUNITY()

elif mode==88:
        BUILDMENU()
	
elif mode==89:
        installer.INSTALLEXE(name,url,description)

elif mode==90:
        installer.INSTALL(name,url,description)
		
elif mode==91:
        installer.INSTALLAPK(name,url,description)

elif mode==92:
        status.Check()
		
elif mode==93:
       community.SHOWCOMMUNITYBUILDS(name, url, description)
	 
elif mode==94:
        installer.INSTALLLIB(name,url,description)

elif mode==95:
        PLAYVIDEO(url)
		
elif mode==96:
        installer.INSTALL_COMMUNITY(name,url,description)
	 
elif mode==97:
        Common.BUILDER_COMMUNITY(name,url,iconimage,fanart,description)

elif mode==98:
        installer.INSTALL_ADVANCED(name,url,description)

elif mode==99:
		installer.INSTALL(name,url,description)

elif mode==100:
		backuprestore.READ_ZIP(url)
	
elif mode==101:
		backuprestore.DeleteBackup(url)

elif mode==102:
        xbmc.executebuiltin(description)
        sys.exit(0)

elif mode==103:
		backuprestore.BACKUP_RD_TRAKT()

elif mode==104:
		backuprestore.RESTORE_RD_TRAKT()

elif mode==105:
		backuprestore.READ_ZIP_TRAKT(url)

elif mode==106:
		LATEST_NEWS()

elif mode==107:
		backuprestore.TV_GUIDE_BACKUP()
		
elif mode==108:
		backuprestore.ADDON_DATA_BACKUP()
		
elif mode==109:
		maintenance.RUYA_FIX()

elif mode==110:
		extras.PLAYERCORE_ANDROID()

elif mode==111:
		dialog.ok(AddonTitle, '[COLOR yellowgreen][B]Current Time: [/B][/COLOR][COLOR white]' + THE_TIME + '[/COLOR]', '[COLOR yellowgreen][B]Current Date: [/B][/COLOR][COLOR white]' + THE_DATE + '[/COLOR]')

elif mode==112:
		maintenance.AUTO_CLEAN_ON_OFF()

elif mode==113:
		maintenance.AUTO_WEEKLY_CLEAN_ON_OFF()

elif mode==114:
		xbmc.executebuiltin("Container.Refresh")

elif mode==115:
		extras.PLAYERCORE_WINDOWS()

elif mode==116:
		Common.SHOW_PICTURE(fanart)

elif mode==117:
		maintenance.BASE64_ENCODE_DECODE()

elif mode==118:
		Common.WriteTicket()

elif mode==119:
		Common.ListTickets()

elif mode==120:
		dialog.ok(AddonTitle, url )
		xbmc.executebuiltin("Container.Refresh")

elif mode==121:
		get_addons.MENU_MAIN()

elif mode==122:
		get_addons.GET_SINGLE(name,url)
		
elif mode==123:
		get_addons.GET_MULTI(name,url)

elif mode==124:
		xbmc.executebuiltin("ReloadSkin()")

elif mode==125:
		xbmc.executebuiltin("ActivateWindow(busydialog)")
		xbmc.executebuiltin("UpdateAddonRepos")
		xbmc.executebuiltin("UpdateLocalAddons")
		xbmc.executebuiltin("Dialog.Close(busydialog)")
		
elif mode==126:
		maintenance.OPEN_EXTERNAL_SETTINGS()

elif mode==127:
		xbmc.executebuiltin("ToggleDebug")

elif mode==128:
		REMOVE_KEYBOARD_FILE()

elif mode==129:
		KEYMAPS()

elif mode==130:
        installer.INSTALL_KEYMAP(name,url,description)

elif mode==131:
		REMOVE_ADVANCED_FILE()

elif mode==132:
		extras.YOUTUBE_REMOVE()
		
elif mode==140:
		community.NEXT_PAGE_COMMUNITY(description)
		
elif mode==141:
		community.PROTECTED_FOLDER()
		
elif mode==142:
		community.NEXT_PAGE_PROTECTED(description)
		
elif mode==143:
		community.SHOWPROTECTEDBUILDS(name,url,description)

elif mode==144:
		FANRIFFIC_THEMES()

elif mode==145:
        installer.INSTALL_FANRIFFIC(name,url,description)

elif mode==146:
		extras.SPORTS_DEVIL_FIX()
		
elif mode==147:
		maintenance.CHECK_BROKEN_REPOS()

elif mode==148:
		maintenance.CHECK_BROKEN_SOURCES()

elif mode==149:
		ANDROID_APKS()

elif mode==150:
		get_addons.GET_LIST(description)

elif mode==151:
		get_addons.GET_MULTI(name,url)

elif mode==152:
		dialog = xbmcgui.Dialog()
		dialog.ok(AddonTitle, '[COLOR white][B]Please contact ECHO on Twitter: [/B][/COLOR]','[COLOR dodgerblue][B]@echo_coding[/B][/COLOR]')

elif mode==153:
		dialog = xbmcgui.Dialog()
		dialog.ok(AddonTitle, '[COLOR white][B]To get an addon added to the installer we must have permission from the developer. If you would like to add an addon please ask them for permission and if granted contact ECHO on twitter @echo_coding to let us know. We will get the addon added ASAP. Thank you![/B][/COLOR]')

elif mode==154:
		maintenance.view_LastError()

elif mode==155:
		maintenance.view_Errors()

elif mode==156:
		get_addons.GET_PAID(name,url)

elif mode==157:
		dialog = xbmcgui.Dialog()
		dialog.ok(AddonTitle, '[COLOR white][B]COMING SOON! Please contact ECHO on Twitter for more information: [/B][/COLOR]','[COLOR dodgerblue][B]@echo_coding[/B][/COLOR]')

elif mode==158:
		extras.REMOVE_GUIDE()

elif mode==159:
		get_addons.PARENTAL_CONTROLS()

elif mode==160:
		get_addons.PARENTAL_CONTROLS_PIN()

elif mode==161:
		get_addons.PARENTAL_CONTROLS_OFF()

elif mode==162:
		AUTO_UPDATER(name)

elif mode==163:
		maintenance.GET_ADDON_STATS()

elif mode==164:
		get_addons.GET_REPO(name,url)

elif mode==165:
		AUTO_UPDATER("dialog")

elif mode==170:
		INSTALLER_APKS()

elif mode==171:
        installer.INSTALLAPK_INSTALLER(name,url,description)

elif mode==172:
		DONATIONS_LINK()

elif mode==173:
		get_addons.FINISH()

elif mode==174:
		dp.create(AddonTitle)
		dp.update(0, "Updating installed addons, please wait.")
		xbmc.executebuiltin("UpdateAddonRepos")
		xbmc.executebuiltin("UpdateLocalAddons")
		time.sleep(5)
		dp.close()
		dialog.ok(AddonTitle, "All local addons have been updated. Thank you for using ECHO Wizard!")
		sys.exit(0)

elif mode==175:
		get_addons.MENU_MAIN()
	
elif mode==176:
		get_addons.ADDON_DECIDE(name,url,iconimage,fanart)
		
elif mode==177:
		get_addons.FILE_MANAGER_SOURCES(name,url,description)

elif mode==178:
		get_addons.WRITE_SOURCE_TO_FILE_MANAGER(name,url)

elif mode==179:
		GETTEMP()
		
elif mode==180:
		CLEARTEMP()

elif mode==181:
		security.check()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
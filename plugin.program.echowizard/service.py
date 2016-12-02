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
import shutil
import zipfile
import extract
import downloader
import maintenance
import installer
import re
import backuprestore
import time
import common as Common
import wipe
import runner
import plugintools
from random import randint
from datetime import date
import calendar
import acdays

my_date = date.today()
today = calendar.day_name[my_date.weekday()]
addon_id = 'plugin.program.echowizard'
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
SOURCES     =  xbmc.translatePath(os.path.join('special://home/userdata','sources.xml'))
ADDON     =  xbmc.translatePath(os.path.join('special://home/addons/plugin.program.echowizard',''))
my_addon = xbmcaddon.Addon()
dp = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()
AddonTitle="[COLOR lime]ECHO[/COLOR] [COLOR white]Wizard[/COLOR]"
GoogleOne = "http://www.google.com"
GoogleTwo = "http://www.google.co.uk"
check = plugintools.get_setting("checkupdates")
addonupdate = plugintools.get_setting("updaterepos")
autoclean = plugintools.get_setting("acstartup")
size_check = plugintools.get_setting("startupsize")
CLEAR_CACHE_SIZE = plugintools.get_setting("cachemb")
CLEAR_PACKAGES_SIZE = plugintools.get_setting("packagesmb")
CLEAR_THUMBS_SIZE = plugintools.get_setting("thumbsmb")
BASEURL = base64.b64decode(b"aHR0cDovL2VjaG9jb2Rlci5jb20v")
nointernet = 0

#Update Information
ECHO_VERSION  =  os.path.join(USERDATA,'echo_build.txt')
HOME         =  xbmc.translatePath('special://home/')
TMP_TRAKT     =  xbmc.translatePath(os.path.join(HOME,'tmp_trakt'))
TRAKT_MARKER =  xbmc.translatePath(os.path.join(TMP_TRAKT,'marker.xml'))
backup_zip = xbmc.translatePath(os.path.join(TMP_TRAKT,'Restore_RD_Trakt_Settings.zip'))

try:
    response = Common.OPEN_URL_NORMAL(GoogleOne)
except:
    try:
        response = Common.OPEN_URL_NORMAL(GoogleTwo)
    except:
        nointernet = 1
        pass

#######################################################################
#						Check for Team ECHO Updates
#######################################################################

pleasecheck = 0

#Information for ECHO Wizard OTA updates.
if os.path.exists(ECHO_VERSION):
	VERSIONCHECK = ECHO_VERSION
	FIND_URL = BASEURL + base64.b64decode(b'YnVpbGRzL3dpemFyZC91cGRhdGVfd2l6LnR4dA==')
	checkurl = BASEURL + base64.b64decode(b'YnVpbGRzL3dpemFyZC92ZXJzaW9uX2NoZWNrLnR4dA==')
	pleasecheck = 1

if nointernet == 0 and pleasecheck == 1:
	if check == 'true':
		if os.path.exists(VERSIONCHECK):
			vers = open(VERSIONCHECK, "r")
			regex = re.compile(r'<build>(.+?)</build><version>(.+?)</version>')
			for line in vers:
				currversion = regex.findall(line)
				for build,vernumber in currversion:
					if vernumber > 0:
						req = urllib2.Request(checkurl)
						req.add_header('User-Agent',base64.b64decode(b'VGhlV2l6YXJkSXNIZXJl'))
						try:
							response = urllib2.urlopen(req)
						except:
							dialog.ok(AddonTitle,'Sorry we are unable to check for updates!','The update host appears to be down.','Please check for updates later via the wizard.')							   
							sys.exit(1)
							
						link=response.read()
						response.close()
						match = re.compile('<build>'+build+'</build><version>(.+?)</version><fresh>(.+?)</fresh>').findall(link)
						for newversion,fresh in match:
							if newversion > vernumber:
								if fresh =='false': # TRUE
									choice = xbmcgui.Dialog().yesno("NEW UPDATE AVAILABLE", 'Found a new update for the Build', build + " ver: "+newversion, 'Do you want to install it now?', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR lightskyblue]NO[/COLOR][/B]')
									if choice == 1: 
										updateurl = FIND_URL
										req = urllib2.Request(updateurl)
										req.add_header('User-Agent',base64.b64decode(b'VGhlV2l6YXJkSXNIZXJl'))
										try:
											response = urllib2.urlopen(req)
										except:
											dialog.ok(AddonTitle,'Sorry we were unable to download the update!','The update host appears to be down.','Please check for updates later via the wizard.')
											sys.exit(1)
										link=response.read()
										response.close()
										match = re.compile('<build>'+build+'</build><url>(.+?)</url>').findall(link)
										for url in match:				
											path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
											name = "build"
											dp = xbmcgui.DialogProgress()
	
											dp.create(AddonTitle,"Downloading ",'', 'Please Wait')
											lib=os.path.join(path, name+'.zip')
											try:
												os.remove(lib)
											except:
												pass
										
											downloader.download(url, lib, dp)
											addonfolder = xbmc.translatePath(os.path.join('special://','home'))
											time.sleep(2)
											dp.update(0,"", "Extracting Zip Please Wait")
											installer.unzip(lib,addonfolder,dp)
											dialog = xbmcgui.Dialog()
											dialog.ok(AddonTitle, "Your build has succesfully been updated to the latest version.","Kodi must now force close to complete the update.")							
											Common.KillKodi()
									else:
										sys.exit(1)
								else:
									choice = xbmcgui.Dialog().yesno( build + " " + newversion + " update available", 'Found a new update for the Build', build + " ver: "+newversion, 'Do you want to install it now?', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR lightskyblue]NO[/COLOR][/B]')
									if choice == 1: 
										dialog.ok('[COLOR lightskyblue]A WIPE is required for the update[/COLOR]','[COLOR white]Once you wipe the system you will need to go to ECHO Wizard and download the [/COLOR]' + build + '[COLOR white] build.[/COLOR]','[COLOR smokewhite]Kodi will return to the default state after the wipe is performed![/COLOR]')
										wipe.FRESHSTART()
									else:
										sys.exit(1)

# Sleeper added before the maintenance functions due to the updating of addons.

if autoclean == "true":
	maintenance.Auto_Startup()

CACHE      =  xbmc.translatePath(os.path.join('special://home/cache',''))
PACKAGES   =  xbmc.translatePath(os.path.join('special://home/addons','packages'))
THUMBS     =  xbmc.translatePath(os.path.join('special://home/userdata','Thumbnails'))

if not os.path.exists(CACHE):
	CACHE     =  xbmc.translatePath(os.path.join('special://home/temp',''))
if not os.path.exists(PACKAGES):
	os.makedirs(PACKAGES)
	
if not CLEAR_CACHE_SIZE == "0":
	if CLEAR_CACHE_SIZE == "1":
		CACHE_TO_CLEAR = 25000000
	if CLEAR_CACHE_SIZE == "2":
		CACHE_TO_CLEAR = 50000000
	if CLEAR_CACHE_SIZE == "3":
		CACHE_TO_CLEAR = 75000000
	if CLEAR_CACHE_SIZE == "4":
		CACHE_TO_CLEAR = 100000000

	CACHE_SIZE_BYTE    = Common.get_size(CACHE)
	
	if  CACHE_SIZE_BYTE > CACHE_TO_CLEAR:
		maintenance.AUTO_CLEAR_CACHE_MB()

if not CLEAR_PACKAGES_SIZE == "0":
	if CLEAR_PACKAGES_SIZE == "1":
		PACKAGES_TO_CLEAR = 25000000
	if CLEAR_PACKAGES_SIZE == "2":
		PACKAGES_TO_CLEAR = 50000000
	if CLEAR_PACKAGES_SIZE == "3":
		PACKAGES_TO_CLEAR = 75000000
	if CLEAR_PACKAGES_SIZE == "4":
		PACKAGES_TO_CLEAR = 100000000

	PACKAGES_SIZE_BYTE    = Common.get_size(PACKAGES)
	
	if PACKAGES_SIZE_BYTE > PACKAGES_TO_CLEAR:
		if not xbmc.getCondVisibility("Window.isVisible(ProgressDialog)"):
			maintenance.AUTO_CLEAR_PACKAGES_MB()

if not CLEAR_THUMBS_SIZE == "0":
	if CLEAR_THUMBS_SIZE == "1":
		THUMBS_TO_CLEAR = 25000000
	if CLEAR_THUMBS_SIZE == "2":
		THUMBS_TO_CLEAR = 50000000
	if CLEAR_THUMBS_SIZE == "3":
		THUMBS_TO_CLEAR = 75000000
	if CLEAR_THUMBS_SIZE == "4":
		THUMBS_TO_CLEAR = 100000000

	THUMBS_SIZE_BYTE    = Common.get_size(THUMBS)

	if  THUMBS_SIZE_BYTE > THUMBS_TO_CLEAR:
			maintenance.AUTO_CLEAR_THUMBS_MB()

if size_check == "true":

	CACHE_SIZE_BYTE    = Common.get_size(CACHE)
	PACKAGES_SIZE_BYTE    = Common.get_size(PACKAGES)
	THUMBS_SIZE_BYTE    = Common.get_size(THUMBS)
	
	if CACHE_SIZE_BYTE >= 100000000:
		choice = xbmcgui.Dialog().yesno(AddonTitle, '[COLOR smokewhite]Your Cache is now over 100 MB[/COLOR]','This is high and we recommend you clear it now.','[COLOR lightskyblue][B]WOULD YOU LIKE TO CLEAR THE CACHE NOW?[/COLOR][/B]', yeslabel='[COLOR green][B]YES[/B][/COLOR]',nolabel='[COLOR lightskyblue][B]NO[/B][/COLOR]')
		if choice == 1: 
			xbmc.executebuiltin( "ActivateWindow(busydialog)" )
			maintenance.AUTO_CLEAR_CACHE_MB()
			xbmc.executebuiltin( "Dialog.Close(busydialog)" )
			dialog = xbmcgui.Dialog()
			dialog.ok(AddonTitle, "Your cache has been successfully cleared.","Thank you for using ECHO Wizard")							

	if PACKAGES_SIZE_BYTE >= 1000000000:
		if not xbmc.getCondVisibility("Window.isVisible(ProgressDialog)"):
			choice = xbmcgui.Dialog().yesno(AddonTitle, '[COLOR smokewhite]Your Packages folder is now over 1 GB[/COLOR]','This is high and we recommend you clear it now.','[COLOR lightskyblue][B]WOULD YOU LIKE TO PURGE THE PACKAGES NOW?[/COLOR][/B]', yeslabel='[COLOR green][B]YES[/B][/COLOR]',nolabel='[COLOR lightskyblue][B]NO[/B][/COLOR]')
			if choice == 1:
				xbmc.executebuiltin( "ActivateWindow(busydialog)" )
				maintenance.AUTO_CLEAR_PACKAGES_MB()
				xbmc.executebuiltin( "Dialog.Close(busydialog)" )
				dialog = xbmcgui.Dialog()
				dialog.ok(AddonTitle, "Your packages have been successfully purged.","Thank you for using ECHO Wizard")							

	if THUMBS_SIZE_BYTE >= 300000000:
		choice = xbmcgui.Dialog().yesno(AddonTitle, '[COLOR smokewhite]Your Thumbnails are now over 300 MB[/COLOR]','This is high and we recommend you clear it now.','[COLOR lightskyblue][B]WOULD YOU LIKE TO CLEAR THE THUMBNAILS NOW?[/COLOR][/B]', yeslabel='[COLOR green][B]YES[/B][/COLOR]',nolabel='[COLOR lightskyblue][B]NO[/B][/COLOR]')
		if choice == 1: 
			xbmc.executebuiltin( "ActivateWindow(busydialog)" )
			maintenance.AUTO_CLEAR_THUMBS_MB()
			xbmc.executebuiltin( "Dialog.Close(busydialog)" )
			dialog = xbmcgui.Dialog()
			dialog.ok(AddonTitle, "Your thumbnails have been successfully cleared.","Thank you for using ECHO Wizard")							
	
#Call the daily auto cleaner script.
acdays.Checker()
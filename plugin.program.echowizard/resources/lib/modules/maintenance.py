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
import shutil
import urllib2,urllib
import re
import glob
import requests
from resources.lib.modules import common as Common
from resources.lib.modules import downloader
from resources.lib.modules import extract
import time
import os
from resources.lib.modules import installer
from resources.lib.modules import plugintools

AddonTitle="[COLOR yellowgreen]ECHO[/COLOR] [COLOR white]Wizard[/COLOR]"
addon_id = 'plugin.program.echowizard'
thumbnailPath = xbmc.translatePath('special://userdata/Thumbnails');
cachePath = os.path.join(xbmc.translatePath('special://home'), 'cache')
tempPath = os.path.join(xbmc.translatePath('special://home'), 'temp')
addonPath = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.program.echowizard')
mediaPath = os.path.join(addonPath, 'resources/art')
ADDONS = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'))
FANART              = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
databasePath = xbmc.translatePath('special://userdata/Database')
ICON    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
USERDATA = xbmc.translatePath('special://userdata/')
AddonData = xbmc.translatePath('special://userdata/addon_data')
MaintTitle="[COLOR yellowgreen]ECHO[/COLOR] [COLOR white]Maintenance Tools[/COLOR]"
EXCLUDES     = ['plugin.program.echowizard','repository.echocoder','script.module.requests','temp','kodi.log','kodi.log.old','spmc.log','spmc.log.old','dbmc.log','dbmc.log.old']
dp = xbmcgui.DialogProgress()
Windows = xbmc.translatePath('special://home')
WindowsCache = xbmc.translatePath('special://home')
OtherCache = os.path.join(xbmc.translatePath('special://home'), 'temp')
dialog = xbmcgui.Dialog()
BASEURL = base64.b64decode(b'aHR0cDovL3RkYnJlcG8uY29tLw==')

#######################################################################
#						Cache Functions
#######################################################################

class Gui(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)
        self.header = kwargs.get("header")
        self.content = kwargs.get("content")

    def onInit(self):
        self.getControl(1).setLabel(self.header)
        self.getControl(5).setText(self.content)

path   = xbmcaddon.Addon().getAddonInfo('path').decode("utf-8")

class cacheEntry:
    def __init__(self, namei, pathi):
        self.name = namei
        self.path = pathi	

#######################################################################
#						Maintenance Functions
#######################################################################
def setupCacheEntries():
    entries = 5 #make sure this refelcts the amount of entries you have
    dialogName = ["WTF", "4oD", "BBC iPlayer", "Simple Downloader", "ITV"]
    pathName = ["special://profile/addon_data/plugin.video.whatthefurk/cache", "special://profile/addon_data/plugin.video.4od/cache",
					"special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache","special://profile/addon_data/script.module.simple.downloader",
                    "special://profile/addon_data/plugin.video.itv/Images"]
                    
    cacheEntries = []
    
    for x in range(entries):
        cacheEntries.append(cacheEntry(dialogName[x],pathName[x]))
    
    return cacheEntries

#######################################################################
#						Clear Cache
#######################################################################

def clearCache():
    
    if os.path.exists(cachePath)==True:    
        for root, dirs, files in os.walk(cachePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Kodi Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        try:
							if (f.endswith(".log")): continue
							os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if os.path.exists(tempPath)==True:    
        for root, dirs, files in os.walk(tempPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Kodi Temp Files", str(file_count) + " files found", "Do you want to delete them?"):
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'Other'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'LocalAndRental'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass    
                
    cacheEntries = setupCacheEntries()
                                         
    for entry in cacheEntries:
        clear_cache_path = xbmc.translatePath(entry.path)
        if os.path.exists(clear_cache_path)==True:    
            for root, dirs, files in os.walk(clear_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:

                    dialog = xbmcgui.Dialog()
                    if dialog.yesno(MaintTitle,str(file_count) + "%s cache files found"%(entry.name), "Do you want to delete them?"):
                        for f in files:
                            os.unlink(os.path.join(root, f))
                        for d in dirs:
                            shutil.rmtree(os.path.join(root, d))
                            
                else:
                    pass
                

    dialog = xbmcgui.Dialog()
    dialog.ok(MaintTitle, "Done Clearing Cache files")
    xbmc.executebuiltin("Container.Refresh")

#######################################################################
#						Delete Thumbnails
#######################################################################
    
def deleteAddonDB():

	dialog = xbmcgui.Dialog()
	xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
	version=float(xbmc_version[:4])

	if version >= 17.0 and version <= 17.9:
		codename = 'Krypton'
	else:
		codename = 'Pass'
	
	if codename == "Pass":
		try:
			for root, dirs, files in os.walk(databasePath,topdown=True):
				dirs[:] = [d for d in dirs]
				for name in files:
					if "addons" in name.lower():
						try:
							os.remove(os.path.join(root,name))
							dialog.ok(MaintTitle,str(name)+  "removed!",'','[COLOR smokewhite]Thank you for using ECHO Wizard[/COLOR]')
						except: 
							dialog.ok(MaintTitle,'Error Removing ' + str(name),'','[COLOR smokewhite]Thank you for using ECHO Wizard[/COLOR]')
							pass
					else:
						continue
		except:
			pass
	else:
		dialog.ok(MaintTitle,'This feature is not available in Kodi 17 Krypton','','[COLOR smokewhite]Thank you for using ECHO Wizard[/COLOR]')

#######################################################################
#						Delete Thumbnails
#######################################################################
    
def deleteThumbnails():
    
    if os.path.exists(thumbnailPath)==True:  
            dialog = xbmcgui.Dialog()
            if dialog.yesno("Delete Thumbnails", "This option deletes all thumbnails", "Are you sure you want to do this?"):
                for root, dirs, files in os.walk(thumbnailPath):
                    file_count = 0
                    file_count += len(files)
                    if file_count > 0:                
                        for f in files:
                            try:
                                os.unlink(os.path.join(root, f))
                            except:
								pass
    else:
        pass
    
    text13 = os.path.join(databasePath,"Textures13.db")
    try:
		os.unlink(text13)
    except OSError:
        pass

	dialog.ok(MaintTitle, 'Thumbnails have been deleted.','Thank you for using ECHO Wizard')
	xbmc.executebuiltin("Container.Refresh")

def GET_ADDON_STATS():

	dp.create(AddonTitle,'Counting total addons installed')
	dp.update(0)
	i=0
	for item in os.listdir(ADDONS):
		i=i+1
	Common.addItem('[COLOR white]Total Addons = [/COLOR][COLOR yellowgreen]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')

	dp.update(10,'[COLOR white]Counting the installed video addons.[/COLOR]')
	i=0
	for item in os.listdir(ADDONS):
		if "video" in item.lower():
			i=i+1
	Common.addItem('[COLOR white]Video Addons = [/COLOR][COLOR yellowgreen]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')

	dp.update(20,'[COLOR white]Counting the installed program addons.[/COLOR]')
	i=0
	for item in os.listdir(ADDONS):
		if "program" in item.lower():
			i=i+1
	Common.addItem('[COLOR white]Program Addons = [/COLOR][COLOR yellowgreen]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')

	dp.update(30,'[COLOR white]Counting the installed music addons.[/COLOR]')
	i=0
	for item in os.listdir(ADDONS):
		if "music" in item.lower():
			i=i+1
	Common.addItem('[COLOR white]Music Addons = [/COLOR][COLOR yellowgreen]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')

	dp.update(40,'[COLOR white]Counting the installed image addons.[/COLOR]')
	i=0
	for item in os.listdir(ADDONS):

		if "image" in item.lower():
			i=i+1
	Common.addItem('[COLOR white]Picture Addons = [/COLOR][COLOR yellowgreen]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')

	dp.update(50,'[COLOR white]Counting the installed scripts.[/COLOR]')
	i=0
	for item in os.listdir(ADDONS):
		if "script" in item.lower():
			i=i+1
	Common.addItem('[COLOR white]Scripts = [/COLOR][COLOR yellowgreen]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')

	dp.update(55,'[COLOR white]Counting the installed skins.[/COLOR]')
	i=0
	for item in os.listdir(ADDONS):
		if "skin" in item.lower():
			i=i+1
	Common.addItem('[COLOR white]Skins = [/COLOR][COLOR yellowgreen]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')


	dp.update(60,'[COLOR white]Counting the installed repositories.[/COLOR]')
	i=0
	for root, dirs, files in os.walk(ADDONS,topdown=True):
		dirs[:] = [d for d in dirs]
		for name in dirs:
			if "repo" in name.lower():
				i=i+1
	Common.addItem('[COLOR white]Repositories = [/COLOR][COLOR yellowgreen]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')

	xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
	version=float(xbmc_version[:4])
	dp.update(70,'[COLOR white]Finding which version of Kodi is installed.[/COLOR]')
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

	dp.update(80,'[COLOR white]Getting your IP address.[/COLOR]')
	f = urllib.urlopen("http://www.canyouseeme.org/")
	html_doc = f.read()
	f.close()
	m = re.search('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',html_doc)
	import socket
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	check = plugintools.get_setting("checkaddonupdates")
	check_build = plugintools.get_setting("checkupdates")

	dp.update(90,'[COLOR white]Getting your update preferences.[/COLOR]')
	if check=="true":
		a = "[COLOR yellowgreen]Yes[/COLOR]"
	else:
		a = "[COLOR lightskyblue]No[/COLOR]"
	if check_build=="true":
		b = "[COLOR yellowgreen]Yes[/COLOR]"
	else:
		b = "[COLOR lightskyblue]No[/COLOR]"
	Common.addItem('[COLOR ghostwhite]Version: [/COLOR][COLOR yellowgreen]%s' % version + " " + codename + "[/COLOR]",BASEURL,200,ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite]Check For Updates on Start: [/COLOR]' + a,BASEURL,200,ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite]Check For Build Updates on Kodi launch: [/COLOR]' + b,BASEURL,200,ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite]Local IP: [/COLOR][COLOR yellowgreen]' + s.getsockname()[0] + '[/COLOR]',BASEURL,200,ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite]External IP: [/COLOR][COLOR yellowgreen]' + m.group(0) + '[/COLOR]',BASEURL,200,ICON,FANART,'')

	dp.update(100)
	dp.close()
	xbmc.executebuiltin('Container.SetViewMode(50)')

def CHECK_BROKEN_SOURCES():

	dialog = xbmcgui.Dialog()
	SOURCES_FILE =  xbmc.translatePath('special://home/userdata/sources.xml')

	if not os.path.isfile(SOURCES_FILE):
		dialog.ok(AddonTitle,'[COLOR red][B]Error: It appears you do not currently have a sources.xml file on your system. We are unable to perform this test.[/B][/COLOR]')
		sys.exit(0)

	dp.create(AddonTitle,"Testing Internet Connection...",'', 'Please Wait...')	

	try:
		Common.OPEN_URL_NORMAL("http://www.google.com")
	except:
		dialog.ok(AddonTitle,'[COLOR red][B]Error: It appears you do not currently have an active internet connection. This will cause false positives in the test. Please try again with an active internet connection.[/B][/COLOR]')
		sys.exit(0)
	found = 0
	passed = 0
	dp.update(0,"Checking Sources...",'', 'Please Wait...')	
	a=open(SOURCES_FILE).read()	
	b=a.replace('\n','U').replace('\r','F')
	match=re.compile('<source>(.+?)</source>').findall(str(b))
	counter = 0
	for item in match:
		name=re.compile('<name>(.+?)</name>').findall(item)[0]
		checker=re.compile('<path pathversion="1">(.+?)</path>').findall(item)[0]
		if "http" in str(checker):
			dp.update(0,"","[COLOR yellowgreen][B]Checking: " + name + "[/B][/COLOR]", "")
			try:
				checkme = requests.get(checker)
			except:
				checkme = "null"
				pass
			try:
				error_out = 0
				if not "this does not matter its just a test" in ("%s" % checkme.text):
					error_out = 0
			except:
				error_out = 1

			if error_out == 0:
				if not ".zip" in ("%s" % checkme.text):		
					if not "repo" in ("%s" % checkme.text):
						if not "<title>Index of /</title>" in ("%s" % checkme.text):
							choice = dialog.select("[COLOR red][B]Error connecting to " + name + " (" + checker + ")[/B][/COLOR]", ['[COLOR lightskyblue][B]Edit the source URL.[/B][/COLOR]','[COLOR lightskyblue][B]Remove the source.[/B][/COLOR]','[COLOR lightskyblue][B]Do Nothing (Leave the source)[/B][/COLOR]'])
							if choice == 0:
								found = 1
								counter = counter + 1
								string =''
								keyboard = xbmc.Keyboard(string, 'Enter New Source URL')
								keyboard.doModal()
								if keyboard.isConfirmed():
									string = keyboard.getText().replace(' ','')
								if len(string)>1:
									if not "http://" in string:
										if not "htts://" in string:
											string = "http://" + string
									h=open(SOURCES_FILE).read()
									i=h.replace('\n','U').replace('\r','F')
									j=i.replace(str(checker), str(string))
									k=j.replace('U','\n').replace('F','\r')
									f= open(SOURCES_FILE, mode='w')
									f.write(k)
									f.close()
								else: quit()
							elif choice == 1:
								found = 1
								counter = counter + 1
								h=open(SOURCES_FILE).read()
								i=h.replace('\n','U').replace('\r','F')
								j=i.replace(str(item), '')
								k=j.replace('U','\n').replace('F','\r')
								l=k.replace('<source></source>','').replace('        \n','')
								f= open(SOURCES_FILE, mode='w')
								f.write(l)
								f.close()
							else:
								found = 1
								counter = counter + 1
						else:
							passed = passed + 1
					else:
						passed = passed + 1
				else:
					passed = passed + 1
			else:
				choice = dialog.select("[COLOR red][B]Error connecting to " + name + " (" + checker + ")[/B][/COLOR]", ['[COLOR lightskyblue][B]Edit the source URL.[/B][/COLOR]','[COLOR lightskyblue][B]Remove the source.[/B][/COLOR]','[COLOR lightskyblue][B]Do Nothing (Leave the source)[/B][/COLOR]'])
				if choice == 0:
					found = 1
					counter = counter + 1
					string =''
					keyboard = xbmc.Keyboard(string, 'Enter New Source URL')
					keyboard.doModal()
					if keyboard.isConfirmed():
						string = keyboard.getText().replace(' ','')
					if len(string)>1:
						if not "http://" in string:
							if not "htts://" in string:
								string = "http://" + string
						h=open(SOURCES_FILE).read()
						i=h.replace('\n','U').replace('\r','F')
						j=i.replace(str(checker), str(string))
						k=j.replace('U','\n').replace('F','\r')
						f= open(SOURCES_FILE, mode='w')
						f.write(k)
						f.close()
					else: quit()
				elif choice == 1:
					found = 1
					counter = counter + 1
					h=open(SOURCES_FILE).read()
					i=h.replace('\n','U').replace('\r','F')
					j=i.replace(str(item), '')
					k=j.replace('U','\n').replace('F','\r')
					l=k.replace('<source></source>','').replace('        \n','')
					f= open(SOURCES_FILE, mode='w')
					f.write(l)
					f.close()
				else:
					found = 1
					counter = counter + 1

			if dp.iscanceled():
				dialog = xbmcgui.Dialog()
				dialog.ok(AddonTitle, 'The source check was cancelled')
				dp.close()
				sys.exit()

			dp.update(0,"","","[COLOR yellowgreen][B]Alive: " + str(passed) + "[/B][/COLOR][COLOR red][B]        Dead: " + str(counter) + "[/B][/COLOR]")

	dialog.ok(AddonTitle,'[COLOR white]We have checked your sources and found:[/COLOR]', '[COLOR yellowgreen][B]WORKING SOURCES: ' + str(passed) + ' [/B][/COLOR]','[COLOR red][B]DEAD SOURCES: ' + str(counter) + ' [/B][/COLOR]')

def CHECK_BROKEN_REPOS():

	dialog = xbmcgui.Dialog()

	dp.create(AddonTitle,"Testing Internet Connection...",'', 'Please Wait...')	

	try:
		Common.OPEN_URL_NORMAL("http://www.google.com")
	except:
		dialog.ok(AddonTitle,'[COLOR red][B]Error: It appears you do not currently have an active internet connection. This will cause false positives in the test. Please try again with an active internet connection.[/B][/COLOR]')
		sys.exit(0)
	passed = 0
	failed = 0
	HOME =  xbmc.translatePath('special://home/addons/')
	dp.update(0,"[COLOR yellowgreen][B]We are currently checking:[/B][/COLOR]",'',"[COLOR yellowgreen][B]Alive: 0[/B][/COLOR][COLOR red][B]        Dead: 0[/B][/COLOR]")
	url = HOME
	for root, dirs, files in os.walk(url):
		for file in files:
			if file == "addon.xml":
				a=open((os.path.join(root, file))).read()	
				if "info compressed=" in str(a):
					match = re.compile('<info compressed="false">(.+?)</info>').findall(a)
					for checker in match:
						dp.update(0,"","[COLOR yellowgreen][B]" + checker + "[/B][/COLOR]", "")
						try:
							Common.OPEN_URL_NORMAL(checker)
							passed = passed + 1
						except:
							try:
								checkme = requests.get(checker)
							except:
								pass
						
							try:
								error_out = 0
								if not "this does not matter its just a test" in ("%s" % checkme.text):
									error_out = 0
							except:
								error_out = 1

							if error_out == 0:
								if not "addon id=" in ("%s" % checkme.text):	
									failed = failed + 1
									match = re.compile('<addon id="(.+?)".+?ame="(.+?)" version').findall(a)
									for repo_id,repo_name in match:
										dialog = xbmcgui.Dialog()
										default_path = xbmc.translatePath("special://home/addons/")
										file_path = xbmc.translatePath(file)
										full_path = default_path + repo_id
										choice = xbmcgui.Dialog().yesno(AddonTitle,"[COLOR white]The [/COLOR][COLOR yellowgreen]" + repo_name + "[/COLOR] [COLOR white] appears to be broken. We attempted to connect to the repo but it was unsuccessful.[/COLOR]",'[COLOR red]To remove this repository please click YES[/COLOR]',yeslabel='[B][COLOR yellowgreen]YES[/COLOR][/B]',nolabel='[B][COLOR lightskyblue]NO[/COLOR][/B]')
										if choice == 1:
											try:
												shutil.rmtree(full_path)
											except:
												dialog.ok(AddonTitle,"[COLOR white]Sorry we were unable to remove " + repo_name + "[/COLOR]")
								else:
									passed = passed + 1
							else:
								failed = failed + 1
								match = re.compile('<addon id="(.+?)".+?ame="(.+?)" version').findall(a)
								for repo_id,repo_name in match:
									dialog = xbmcgui.Dialog()
									default_path = xbmc.translatePath("special://home/addons/")
									file_path = xbmc.translatePath(file)
									full_path = default_path + repo_id
									choice = xbmcgui.Dialog().yesno(AddonTitle,"[COLOR white]The [/COLOR][COLOR yellowgreen]" + repo_name + "[/COLOR] [COLOR white] appears to be broken. We attempted to connect to the repo but it was unsuccessful.[/COLOR]",'[COLOR red]To remove this repository please click YES[/COLOR]',yeslabel='[B][COLOR yellowgreen]YES[/COLOR][/B]',nolabel='[B][COLOR lightskyblue]NO[/COLOR][/B]')
									if choice == 1:
										try:
											shutil.rmtree(full_path)
										except:
											dialog.ok(AddonTitle,"[COLOR white]Sorry we were unable to remove " + repo_name + "[/COLOR]")
			
						if dp.iscanceled():
							dialog = xbmcgui.Dialog()
							dialog.ok(AddonTitle, 'The repository check was cancelled')
							dp.close()
							sys.exit()
						dp.update(0,"","","[COLOR yellowgreen][B]Alive: " + str(passed) + "[/B][/COLOR][COLOR red][B]        Dead: " + str(failed) + "[/B][/COLOR]")
						
	dialog.ok(AddonTitle,'[COLOR white]We have checked your repositories and found:[/COLOR]', '[COLOR yellowgreen][B]WORKING SOURCES: ' + str(passed) + ' [/B][/COLOR]','[COLOR red][B]DEAD SOURCES: ' + str(failed) + ' [/B][/COLOR]')

#######################################################################
#						Delete Packages
#######################################################################

def purgePackages():
    
    purgePath = xbmc.translatePath('special://home/addons/packages')
    dialog = xbmcgui.Dialog()
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
    if dialog.yesno("Delete Package Cache Files", "%d packages found."%file_count, "Delete Them?"):  
        for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:            
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
                dialog = xbmcgui.Dialog()
                dialog.ok(MaintTitle, "Deleting Packages all done")
            else:
                dialog = xbmcgui.Dialog()
                dialog.ok(MaintTitle, "No Packages to Purge")

    xbmc.executebuiltin("Container.Refresh")

#######################################################################
#						Convert physical to special
#######################################################################	

def Fix_Special(url):

    HOME =  xbmc.translatePath('special://home')
    dialog = xbmcgui.Dialog()
    dp.create(AddonTitle,"Renaming paths...",'', '')
    url = xbmc.translatePath('special://userdata')
    for root, dirs, files in os.walk(url):
        for file in files:
            if file.endswith(".xml"):
                 dp.update(0,"Fixing","[COLOR yellowgreen]" + file + "[/COLOR]", "Please wait.....")
                 a=open((os.path.join(root, file))).read()
                 b=a.replace(HOME, 'special://home/')
                 f= open((os.path.join(root, file)), mode='w')
                 f.write(str(b))
                 f.close()

    dialog.ok(MaintTitle, "All physical paths have been converted to special","To complete this process you must force close Kodi now!")
    Common.KillKodi()

#######################################################################
#						Autoclean Function
#######################################################################
def setupCacheEntries():
    entries = 5 #make sure this refelcts the amount of entries you have
    dialogName = ["WTF", "4oD", "BBC iPlayer", "Simple Downloader", "ITV"]
    pathName = ["special://profile/addon_data/plugin.video.whatthefurk/cache", "special://profile/addon_data/plugin.video.4od/cache",
					"special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache","special://profile/addon_data/script.module.simple.downloader",
                    "special://profile/addon_data/plugin.video.itv/Images"]
                    
    cacheEntries = []
    
    for x in range(entries):
        cacheEntries.append(cacheEntry(dialogName[x],pathName[x]))
    
    return cacheEntries

#######################################################################
#						Delete Crash Log Function
#######################################################################

def DeleteCrashLogs():  

	HomeDir = xbmc.translatePath('special://home')
	WindowsCache = os.path.join(xbmc.translatePath('special://home'), 'cache')
	OtherCache = xbmc.translatePath('special://temp')
	
	if os.path.exists(HomeDir)==True:   
		dialog = xbmcgui.Dialog()
		if dialog.yesno(MaintTitle, '', "Do you want to delete old crash logs?"):
			path=Windows
			import glob
			for infile in glob.glob(os.path.join(path, '*.dmp')):
				File=infile
				print infile
				os.remove(infile)
				
			for infile in glob.glob(os.path.join(path, '*.txt')):
				File=infile
				print infile
				os.remove(infile)
				
		if os.path.exists(WindowsCache)==True:   
			path=WindowsCache
			import glob
			for infile in glob.glob(os.path.join(path, '*.dmp')):
				File=infile
				print infile
				os.remove(infile)
				
			for infile in glob.glob(os.path.join(path, '*.txt')):
				File=infile
				print infile
				os.remove(infile)

		if os.path.exists(OtherCache)==True:   
			path=OtherCache
			import glob
			for infile in glob.glob(os.path.join(path, '*.dmp')):
				File=infile
				print infile
				os.remove(infile)
				
			for infile in glob.glob(os.path.join(path, '*.txt')):
				File=infile
				print infile
				os.remove(infile)
		
		dialog = xbmcgui.Dialog()
		dialog.ok(MaintTitle, "Crash logs deleted", "[COLOR smokewhite]Thank you for using ECHO Wizard[/COLOR]")
	else:
		dialog = xbmcgui.Dialog()
		dialog.ok(MaintTitle, "An error occured", "[COLOR smokewhite]Please report this to ECHO Wizard[/COLOR]")

def HidePasswords():

    dialog = xbmcgui.Dialog()
    HOME         =  xbmc.translatePath('special://home')
    if dialog.yesno(MaintTitle, "Are You Sure You Want To Hide Passwords?", ""):
        dialog = xbmcgui.Dialog()
        dp.create(MaintTitle,"Renaming paths...",'', 'Please Wait')
        for root, dirs, files in os.walk(HOME):
            for f in files:
                if f == "settings.xml":
                    FILE=open(os.path.join(root, f)).read()
                    match=re.compile('<setting id=(.+?)>').findall (FILE)
                    for LINE in match:
                        if 'pass' in LINE:
                            if not 'option="hidden"' in LINE:
                                try:
                                    CHANGEME=LINE.replace('/',' option="hidden"/') 
                                    f = open(os.path.join(root, f), mode='w')
                                    f.write(str(FILE).replace(LINE,CHANGEME))
                                    f.close()
                                except:pass
			
        dialog.ok(MaintTitle, "All Passowrds are now hidden!", "[COLOR smokewhite]Thank you for using ECHO Wizard[/COLOR]") 
		
                                            
def UnhidePasswords():

    dialog = xbmcgui.Dialog()
    HOME         =  xbmc.translatePath('special://home')
    if dialog.yesno(MaintTitle, "Are You Sure You Want To Make All Passwords Visable?", ""):
        dialog = xbmcgui.Dialog()
        dp.create(MaintTitle,"Renaming paths...",'', 'Please Wait')
        for root, dirs, files in os.walk(HOME):
            for f in files:
                if f == "settings.xml":
                    FILE=open(os.path.join(root, f)).read()
                    match=re.compile('<setting id=(.+?)>').findall (FILE)
                    for LINE in match:
                        if 'pass' in LINE:
                            if 'option="hidden"' in LINE:
                                try:
                                    CHANGEME=LINE.replace('option="hidden"','') 
                                    f = open(os.path.join(root, f), mode='w')
                                    f.write(str(FILE).replace(LINE,CHANGEME))
                                    f.close()
                                except:pass
			
        dialog.ok(MaintTitle, "All Passowrds are now visable!", "[COLOR smokewhite]Thank you for using ECHO Wizard[/COLOR]") 

		
def view_LastError():

	cachePath = os.path.join(xbmc.translatePath('special://home'), 'cache')
	tempPath = os.path.join(xbmc.translatePath('special://home'), 'temp')
	WindowsCache = xbmc.translatePath('special://home')
	found = 0
	get_log = 0

	if os.path.exists(tempPath):
		for root, dirs, files in os.walk(tempPath,topdown=True):
			dirs[:] = [d for d in dirs]
			for name in files:
				if ".old.log" not in name.lower():
					if ".log" in name.lower():
						got_log = 1
						a=open((os.path.join(root, name))).read()	
						b=a.replace('\n','NEW_L').replace('\r','NEW_R')
						match = re.compile('EXCEPTION Thrown(.+?)End of Python script error report').findall(b)
						for checker in match:
							found = 1
							THE_ERROR = "[B][COLOR red]THE LAST ERROR YOU ENCOUNTERED WAS:[/B][/COLOR]\n\n" + checker + '\n'
						if found == 0:
							dialog.ok(MaintTitle,'Great news! We did not find any errors in your log.')
						else:
							c=THE_ERROR.replace('NEW_L','\n').replace('NEW_R','\r')
							Common.TextBoxesPlain("%s" % c)
							sys.exit(0)

	if os.path.exists(WindowsCache):
		for root, dirs, files in os.walk(WindowsCache,topdown=True):
			dirs[:] = [d for d in dirs]
			for name in files:
				if ".old.log" not in name.lower():
					if ".log" in name.lower():
						got_log = 1
						a=open((os.path.join(root, name))).read()	
						b=a.replace('\n','NEW_L').replace('\r','NEW_R')
						match = re.compile('EXCEPTION Thrown(.+?)End of Python script error report').findall(b)
						for checker in match:
							found = 1
							THE_ERROR = "[B][COLOR red]THE LAST ERROR YOU ENCOUNTERED WAS:[/B][/COLOR]\n\n" + checker + '\n'
						if found == 0:
							dialog.ok(MaintTitle,'Great news! We did not find any errors in your log.')
						else:
							c=THE_ERROR.replace('NEW_L','\n').replace('NEW_R','\r')
							Common.TextBoxesPlain("%s" % c)
							sys.exit(0)
	if got_log == 0:
		dialog.ok(MaintTitle,'Sorry we could not find a log file on your system')

def viewErrors():

	cachePath = os.path.join(xbmc.translatePath('special://home'), 'cache')
	tempPath = os.path.join(xbmc.translatePath('special://home'), 'temp')
	WindowsCache = xbmc.translatePath('special://home')
	found = 0
	get_log = 0
	i = 0
	String = " "

	if os.path.exists(tempPath):
		for root, dirs, files in os.walk(tempPath,topdown=True):
			dirs[:] = [d for d in dirs]
			for name in files:
				if ".old.log" not in name.lower():
					if ".log" in name.lower():
						got_log = 1
						a=open((os.path.join(root, name))).read()	
						b=a.replace('\n','NEW_L').replace('\r','NEW_R')
						match = re.compile('EXCEPTION Thrown(.+?)End of Python script error report').findall(b)
						for checker in match:
							found = 1
							i = i + 1
							if i == 1:
								String = "[B][COLOR red]ERROR NUMBER " + str(i) + "[/B][/COLOR]\n\n" + checker + '\n'
							else:
								String = String + "[B][COLOR red]ERROR NUMBER: " + str(i) + "[/B][/COLOR]\n\n" + checker + '\n'

						if found == 0:
							dialog.ok(MaintTitle,'Great news! We did not find any errors in your log.')
						else:
							c=String.replace('NEW_L','\n').replace('NEW_R','\r')
							Common.TextBoxesPlain("%s" % c)
							sys.exit(0)

	if os.path.exists(WindowsCache):
		for root, dirs, files in os.walk(WindowsCache,topdown=True):
			dirs[:] = [d for d in dirs]
			for name in files:
				if ".old.log" not in name.lower():
					if ".log" in name.lower():
						got_log = 1
						a=open((os.path.join(root, name))).read()	
						b=a.replace('\n','NEW_L').replace('\r','NEW_R')
						match = re.compile('EXCEPTION Thrown(.+?)End of Python script error report').findall(b)
						for checker in match:
							found = 1
							i = i + 1
							if i == 1:
								String = "[B][COLOR red]ERROR NUMBER " + str(i) + "[/B][/COLOR]\n\n" + checker + '\n'
							else:
								String = String + "[B][COLOR red]ERROR NUMBER " + str(i) + "[/B][/COLOR]\n\n" + checker + '\n'

						if found == 0:
							dialog.ok(MaintTitle,'Great news! We did not find any errors in your log.')
						else:
							c=String.replace('NEW_L','\n').replace('NEW_R','\r')
							Common.TextBoxesPlain("%s" % c)
							sys.exit(0)
	if got_log == 0:
		dialog.ok(MaintTitle,'Sorry we could not find a log file on your system')

def viewLogFile():
	kodilog = xbmc.translatePath('special://logpath/kodi.log')
	spmclog = xbmc.translatePath('special://logpath/spmc.log')
	dbmclog = xbmc.translatePath('special://logpath/dbmc.log')
	kodiold = xbmc.translatePath('special://logpath/kodi.old.log')
	spmcold = xbmc.translatePath('special://logpath/spmc.old.log')
	dbmcold = xbmc.translatePath('special://logpath/dbmc.old.log')

	if os.path.exists(dbmclog):
		if os.path.exists(dbmclog) and os.path.exists(dbmcold):
			choice = xbmcgui.Dialog().yesno(MaintTitle,"Current & Old Log Detected on your system.","Which log would you like to view?","", yeslabel='[B]OLD[/B]',nolabel='[B]CURRENT[/B]')
			if choice == 0:
				f = open(dbmclog,mode='r'); msg = f.read(); f.close()
				Common.TextBoxes("%s - dbmc.log" % "[COLOR white]" + msg + "[/COLOR]")
			else:
				f = open(dbmcold,mode='r'); msg = f.read(); f.close()
				Common.TextBoxes("%s - dbmc.old.log" % "[COLOR white]" + msg + "[/COLOR]")
		else:
			f = open(dbmclog,mode='r'); msg = f.read(); f.close()
			Common.TextBoxes("%s - dbmc.log" % "[COLOR white]" + msg + "[/COLOR]")

	if os.path.exists(spmclog):
		if os.path.exists(spmclog) and os.path.exists(spmcold):
			choice = xbmcgui.Dialog().yesno(MaintTitle,"Current & Old Log Detected on your system.","Which log would you like to view?","", yeslabel='[B]OLD[/B]',nolabel='[B]CURRENT[/B]')
			if choice == 0:
				f = open(spmclog,mode='r'); msg = f.read(); f.close()
				Common.TextBoxes("%s - spmc.log" % "[COLOR white]" + msg + "[/COLOR]")
			else:
				f = open(spmcold,mode='r'); msg = f.read(); f.close()
				Common.TextBoxes("%s - spmc.old.log" % "[COLOR white]" + msg + "[/COLOR]")
		else:
			f = open(spmclog,mode='r'); msg = f.read(); f.close()
			Common.TextBoxes("%s - spmc.log" % "[COLOR white]" + msg + "[/COLOR]")
			
	if os.path.exists(kodilog):
		if os.path.exists(kodilog) and os.path.exists(kodiold):
			choice = xbmcgui.Dialog().yesno(MaintTitle,"Current & Old Log Detected on your system.","Which log would you like to view?","", yeslabel='[B]OLD[/B]',nolabel='[B]CURRENT[/B]')
			if choice == 0:
				f = open(kodilog,mode='r'); msg = f.read(); f.close()
				Common.TextBoxes("%s - kodi.log" % "[COLOR white]" + msg + "[/COLOR]")
			else:
				f = open(kodiold,mode='r'); msg = f.read(); f.close()
				Common.TextBoxes("%s - kodi.old.log" % "[COLOR white]" + msg + "[/COLOR]")
		else:
			f = open(kodilog,mode='r'); msg = f.read(); f.close()
			Common.TextBoxes("%s - kodi.log" % "[COLOR white]" + msg + "[/COLOR]")

	if os.path.isfile(kodilog) or os.path.isfile(spmclog) or os.path.isfile(dbmclog):
		return True
	else:
		dialog.ok(MaintTitle,'Sorry, No log file was found.','','[COLOR smokewhite]Thank you for using ECHO Wizard[/COLOR]')

def autocleanask():
    
	choice = xbmcgui.Dialog().yesno(MaintTitle, 'Selecting [COLOR green]YES[/COLOR] will delete your cache, thumbnails and packages.','[I][COLOR lightsteelblue]Do you wish to continue?[/I][/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR lightskyblue]NO[/COLOR][/B]')
	if choice == 1:
		autocleannow()
	
def autocleannow():

    HomeDir = xbmc.translatePath('special://home')
    WindowsCache = os.path.join(xbmc.translatePath('special://home'), 'cache')
    OtherCache = os.path.join(xbmc.translatePath('special://home'), 'temp')
	
    if os.path.exists(HomeDir)==True:   
        path=Windows
        import glob
        for infile in glob.glob(os.path.join(path, '*.dmp')):
            File=infile
            print infile
            os.remove(infile)
			
        for infile in glob.glob(os.path.join(path, '*.txt')):
            File=infile
            print infile
            os.remove(infile)
				
        if os.path.exists(WindowsCache)==True:   
            path=WindowsCache
            import glob
            for infile in glob.glob(os.path.join(path, '*.dmp')):
                File=infile
                print infile
                os.remove(infile)
				
            for infile in glob.glob(os.path.join(path, '*.txt')):
                File=infile
                print infile
                os.remove(infile)

        if os.path.exists(OtherCache)==True:   
            path=OtherCache
            import glob
            for infile in glob.glob(os.path.join(path, '*.dmp')):
                File=infile
                print infile
                os.remove(infile)
				
            for infile in glob.glob(os.path.join(path, '*.txt')):
                File=infile
                print infile
                os.remove(infile)

    if os.path.exists(cachePath)==True:    
        for root, dirs, files in os.walk(cachePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
							if (f.endswith(".log")): continue
							os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
				
    if os.path.exists(tempPath)==True:    
        for root, dirs, files in os.walk(tempPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass    
                
    cacheEntries = setupCacheEntries()
                                         
    for entry in cacheEntries:
        clear_cache_path = xbmc.translatePath(entry.path)
        if os.path.exists(clear_cache_path)==True:    
            for root, dirs, files in os.walk(clear_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:
                        for f in files:
                            os.unlink(os.path.join(root, f))
                        for d in dirs:
                            shutil.rmtree(os.path.join(root, d))
                            
                else:
                    pass
        
    if os.path.exists(thumbnailPath)==True:  
                for root, dirs, files in os.walk(thumbnailPath):
                    file_count = 0
                    file_count += len(files)
                    if file_count > 0:                
                        for f in files:
                            try:
                                os.unlink(os.path.join(root, f))
                            except:
								pass
    else:
        pass
    
    text13 = os.path.join(databasePath,"Textures13.db")
    try:
		os.unlink(text13)
    except OSError:
        pass
		
    purgePath = xbmc.translatePath('special://home/addons/packages')
    dialog = xbmcgui.Dialog()
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:            
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))

    xbmc.executebuiltin("Container.Refresh")

    xbmcgui.Dialog().ok(MaintTitle,"Auto clean finished.","Your cache, thumbnails and packages have all been deleted")

def AUTO_CLEAR_CACHE_MB():

    HomeDir = xbmc.translatePath('special://home')
    WindowsCache = os.path.join(xbmc.translatePath('special://home'), 'cache')
    OtherCache = os.path.join(xbmc.translatePath('special://home'), 'temp')

    if os.path.exists(cachePath)==True:    
        for root, dirs, files in os.walk(cachePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
							if (f.endswith(".log")): continue
							os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
				
    if os.path.exists(tempPath)==True:    
        for root, dirs, files in os.walk(tempPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass    
                
    cacheEntries = setupCacheEntries()
                                         
    for entry in cacheEntries:
        clear_cache_path = xbmc.translatePath(entry.path)
        if os.path.exists(clear_cache_path)==True:    
            for root, dirs, files in os.walk(clear_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:
                        for f in files:
                            os.unlink(os.path.join(root, f))
                        for d in dirs:
                            shutil.rmtree(os.path.join(root, d))
                            
                else:
                    pass

    xbmc.executebuiltin("Container.Refresh")

def AUTO_CLEAR_PACKAGES_MB():

    time.sleep(60)

    purgePath = xbmc.translatePath('special://home/addons/packages')
    dialog = xbmcgui.Dialog()
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:            
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))

def AUTO_CLEAR_THUMBS_MB():

    if os.path.exists(thumbnailPath)==True:  
                for root, dirs, files in os.walk(thumbnailPath):
                    file_count = 0
                    file_count += len(files)
                    if file_count > 0:                
                        for f in files:
                            try:
                                os.unlink(os.path.join(root, f))
                            except:
								pass
    else:
        pass
    
    text13 = os.path.join(databasePath,"Textures13.db")
    try:
		os.unlink(text13)
    except OSError:
        pass

def Auto_Startup():

    AutoThumbs()
    AutoCache()
    time.sleep(60)
    AutoPackages()

def AutoCache():

    if os.path.exists(cachePath)==True:    
        for root, dirs, files in os.walk(cachePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
							if (f.endswith(".log")): continue
							os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
				
    if os.path.exists(tempPath)==True:    
        for root, dirs, files in os.walk(tempPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass    
                
    cacheEntries = setupCacheEntries()
                                         
    for entry in cacheEntries:
        clear_cache_path = xbmc.translatePath(entry.path)
        if os.path.exists(clear_cache_path)==True:    
            for root, dirs, files in os.walk(clear_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:
                        for f in files:
                            os.unlink(os.path.join(root, f))
                        for d in dirs:
                            shutil.rmtree(os.path.join(root, d))
                            
                else:
                    pass

def AutoThumbs():

    if os.path.exists(thumbnailPath)==True:  
                for root, dirs, files in os.walk(thumbnailPath):
                    file_count = 0
                    file_count += len(files)
                    if file_count > 0:                
                        for f in files:
                            try:
                                os.unlink(os.path.join(root, f))
                            except: pass
    else: pass
    
    text13 = os.path.join(databasePath,"Textures13.db")
    try:
        os.unlink(text13)
    except: pass

def AutoPackages():

    time.sleep(60)
    purgePath = xbmc.translatePath('special://home/addons/packages')
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:            
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))

def AutoCrash():  

	HomeDir = xbmc.translatePath('special://home')
	WindowsCache = os.path.join(xbmc.translatePath('special://home'), 'cache')
	OtherCache = os.path.join(xbmc.translatePath('special://home'), 'temp')
	
	if os.path.exists(HomeDir)==True:   
		path=Windows
		import glob
		for infile in glob.glob(os.path.join(path, '*.dmp')):
			File=infile
			print infile
			os.remove(infile)
				
		for infile in glob.glob(os.path.join(path, '*.txt')):
			File=infile
			print infile
			os.remove(infile)
				
	if os.path.exists(WindowsCache)==True:   
		path=WindowsCache
		import glob
		for infile in glob.glob(os.path.join(path, '*.dmp')):
			File=infile
			print infile
			os.remove(infile)
				
		for infile in glob.glob(os.path.join(path, '*.txt')):
			File=infile
			print infile
			os.remove(infile)

	if os.path.exists(OtherCache)==True:   
		path=OtherCache
		import glob
		for infile in glob.glob(os.path.join(path, '*.dmp')):
			File=infile
			print infile
			os.remove(infile)
				
		for infile in glob.glob(os.path.join(path, '*.txt')):
			File=infile
			print infile
			os.remove(infile)
			
def OPEN_EXTERNAL_SETTINGS():

	SALTS  = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.salts')
	EXODUS = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.exodus')
	SPECTO = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.specto')
	
	if os.path.exists(SALTS):
		SALTS_SELECT = '[COLOR white][B]Open SALTS Settings[/B][/COLOR]'
	else:
		SALTS_SELECT = '[COLOR gray][B]SALTS (Not Installed)[/B][/COLOR]'

	if os.path.exists(EXODUS):
		EXODUS_SELECT = '[COLOR white][B]Open Exodus Settings[/B][/COLOR]'
	else:
		EXODUS_SELECT = '[COLOR gray][B]Exodus (Not Installed)[/B][/COLOR]'

	if os.path.exists(SPECTO):
		SPECTO_SELECT = '[COLOR white][B]Open Specto Settings[/B][/COLOR]'
	else:
		SPECTO_SELECT = '[COLOR gray][B]Specto (Not Installed)[/B][/COLOR]'

	choice = dialog.select(AddonTitle, [SALTS_SELECT,EXODUS_SELECT,SPECTO_SELECT])
	if choice == 0:
		if os.path.exists(SALTS):
			xbmc.executebuiltin("Addon.OpenSettings(plugin.video.salts)")
		else:
			dialog.ok(AddonTitle,"[COLOR white]Sorry, SALTS is not installed on this system so we cannot oepn the settings.[/COLOR]")
	if choice == 1:
		if os.path.exists(EXODUS):
			xbmc.executebuiltin("Addon.OpenSettings(plugin.video.exodus)")
		else:
			dialog.ok(AddonTitle,"[COLOR white]Sorry, Exodus is not installed on this system so we cannot oepn the settings.[/COLOR]")
	if choice == 2:
		if os.path.exists(SPECTO):
			xbmc.executebuiltin("Addon.OpenSettings(plugin.video.specto)")
		else:
			dialog.ok(AddonTitle,"[COLOR white]Sorry, Specto is not installed on this system so we cannot oepn the settings.[/COLOR]")


def RUYA_FIX():

	name = "[COLOR white][B]Ruya Fix[/B][/COLOR]"
	url = BASEURL + base64.b64decode(b'bWFpbnRlbmFuY2UvcnV5YV9maXguemlw')
	description = "NULL"
	#Check is the packages folder exists, if not create it.
	path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
	if not os.path.exists(path):
		os.makedirs(path)
	buildname = name
	dp = xbmcgui.DialogProgress()
	dp.create(AddonTitle,"","","Build: " + buildname)
	buildname = "build"
	lib=os.path.join(path, buildname+'.zip')
	
	try:
		os.remove(lib)
	except:
		pass

	dialog = xbmcgui.Dialog()
	downloader.download(url, lib, dp)
	addonfolder = xbmc.translatePath(os.path.join('special://home','userdata'))
	time.sleep(2)
	dp.update(0,"","Extracting Zip Please Wait","")
	installer.unzip(lib,addonfolder,dp)
	time.sleep(1)
	try:
		os.remove(lib)
	except:
		pass

	HomeDir = xbmc.translatePath('special://home')
	WindowsCache = os.path.join(xbmc.translatePath('special://home'), 'cache')
	OtherCache = xbmc.translatePath('special://temp')

	if os.path.exists(WindowsCache)==True:   
		path=WindowsCache
		import glob
		for infile in glob.glob(os.path.join(path, '*.fi')):
			File=infile
			print infile
			os.remove(infile)

	if os.path.exists(OtherCache)==True:   
		path=OtherCache
		import glob
		for infile in glob.glob(os.path.join(path, '*.fi')):
			File=infile
			print infile
			os.remove(infile)

	dialog.ok(AddonTitle, "[COLOR white]RUYA Fix installed![/COLOR]",'',"[COLOR white]Thank you for using ECHO Wizard![/COLOR]")

def BASE64_ENCODE_DECODE():

	dialog = xbmcgui.Dialog()
	choice = dialog.select(AddonTitle, ['Encode A String','Decode A String'])
	if choice == 0:
		vq = Common._get_keyboard( heading="Enter String to Encode" )
		if ( not vq ): return False, 0
		input = str(vq)
		output = base64.b64encode(input)
		dialog.ok(AddonTitle, '[COLOR lightskyblue]Orignal String: [/COLOR]' + input, '[COLOR lightskyblue]Encrypted String: [/COLOR]' + output)
	else:
		vq = Common._get_keyboard( heading="Enter String to Decode" )
		if ( not vq ): return False, 0
		input = str(vq)
		output = base64.b64decode(vq)
		dialog.ok(AddonTitle, '[COLOR lightskyblue]Encrypted String: [/COLOR]' + input, '[COLOR lightskyblue]Original String: [/COLOR]' + output)

#######################################################################
#				TURN AUTO CLEAN ON|OFF
#######################################################################	

def AUTO_CLEAN_ON_OFF():

    startup_clean = plugintools.get_setting("acstartup")

    if startup_clean == 'true':
        CURRENT = '    <setting id="acstartup" value="true" />'
        NEW     = '    <setting id="acstartup" value="false" />'
    else:
        CURRENT = '    <setting id="acstartup" value="false" />'
        NEW 	= '    <setting id="acstartup" value="true" />'

    HOME         =  xbmc.translatePath('special://userdata/addon_data/plugin.program.echowizard')
    for root, dirs, files in os.walk(HOME):  #Search all xml files and replace physical with special
        for file in files:
            if file == "settings.xml":
                 a=open((os.path.join(root, file))).read()
                 b=a.replace(CURRENT, NEW)
                 f = open((os.path.join(root, file)), mode='w')
                 f.write(str(b))
                 f.close()

    xbmc.executebuiltin("Container.Refresh")

#######################################################################
#				TURN WEEKLY AUTO CLEAN ON|OFF
#######################################################################	

def AUTO_WEEKLY_CLEAN_ON_OFF():

    startup_clean = plugintools.get_setting("clearday")

    if startup_clean == '1':
        CURRENT = '    <setting id="clearday" value="1" />'
        NEW     = '    <setting id="clearday" value="0" />'
    if startup_clean == '2':
        CURRENT = '    <setting id="clearday" value="2" />'
        NEW     = '    <setting id="clearday" value="0" />'
    if startup_clean == '3':
        CURRENT = '    <setting id="clearday" value="3" />'
        NEW     = '    <setting id="clearday" value="0" />'
    if startup_clean == '4':
        CURRENT = '    <setting id="clearday" value="4" />'
        NEW     = '    <setting id="clearday" value="0" />'
    if startup_clean == '5':
        CURRENT = '    <setting id="clearday" value="5" />'
        NEW     = '    <setting id="clearday" value="0" />'
    if startup_clean == '6':
        CURRENT = '    <setting id="clearday" value="6" />'
        NEW     = '    <setting id="clearday" value="0" />'
    if startup_clean == '7':
        CURRENT = '    <setting id="clearday" value="7" />'
        NEW     = '    <setting id="clearday" value="0" />'
    if startup_clean == '0':
        CURRENT = '    <setting id="clearday" value="0" />'
        NEW     = '    <setting id="clearday" value="1" />'


    HOME         =  xbmc.translatePath('special://userdata/addon_data/plugin.program.echowizard')
    for root, dirs, files in os.walk(HOME):  #Search all xml files and replace physical with special
        for file in files:
            if file == "settings.xml":
                 a=open((os.path.join(root, file))).read()
                 b=a.replace(CURRENT, NEW)
                 f = open((os.path.join(root, file)), mode='w')
                 f.write(str(b))
                 f.close()

    xbmc.executebuiltin("Container.Refresh")
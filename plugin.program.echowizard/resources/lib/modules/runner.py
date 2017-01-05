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
import urllib, urllib2
import time
import downloader
import re
import zipfile
from resources.lib.modules import common as Common

BASEURL = base64.b64decode(b"aHR0cDovL2VjaG9jb2Rlci5jb20v")
CURRENT_VERSION =  BASEURL + base64.b64decode(b"b3RoZXIvcmVwb192ZXJzaW9uLnR4dA==")
SOURCES     =  xbmc.translatePath(os.path.join('special://home/userdata','sources.xml'))
ADDON     =  xbmc.translatePath(os.path.join('special://home/addons/plugin.program.echowizard',''))
REPO     =  xbmc.translatePath(os.path.join('special://home/addons','repository.echo'))
WIZARD     =  xbmc.translatePath(os.path.join('special://home/addons','plugin.program.echowizard'))
GUIDE     =  xbmc.translatePath(os.path.join('special://home/addons','plugin.program.echotvguide'))
dialog = xbmcgui.Dialog()
AddonTitle="[COLOR yellowgreen]ECHO[/COLOR] [COLOR white]Wizard[/COLOR]"

def check():

	if not os.path.exists(REPO):
		choice = xbmcgui.Dialog().yesno(AddonTitle, 'The ECHO Repository is not installed','It is a requirement of the ECHO Wizard to have the repo installed.','[COLOR dodgerblue][B]Do you want to install the ECHO repo now?[/B][/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
		if choice == 1:
			INSTALL()
		else:
			sys.exit(0)

def INSTALL():

	req = urllib2.Request(CURRENT_VERSION)
	req.add_header('User-Agent',base64.b64decode(b'VGhlV2l6YXJkSXNIZXJl'))
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match = re.compile('<version>(.+?)</version>').findall(link)
	for latver in match:
		VERSION_NUMBER = latver
	url = base64.b64decode(b'aHR0cHM6Ly9naXRodWIuY29tL2VjaG9jb2RlcmtvZGkvcmVwb3NpdG9yeS5lY2hvL3Jhdy9tYXN0ZXIvemlwcy9yZXBvc2l0b3J5LmVjaG8vcmVwb3NpdG9yeS5lY2hvLQ==') + VERSION_NUMBER + ".zip"

	#Check is the packages folder exists, if not create it.
	path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
	if not os.path.exists(path):
		os.makedirs(path)

	dp = xbmcgui.DialogProgress()
	dp.create(AddonTitle,"","","Installing Repository")
	lib=os.path.join(path, 'repo.zip')
		
	try:
		os.remove(lib)
	except:
		pass
	
	dialog = xbmcgui.Dialog()
	downloader.download(url, lib, dp)
	addonfolder = xbmc.translatePath(os.path.join('special://home','addons'))
	time.sleep(2)
	dp.update(0,"","Extracting Zip Please Wait","")
	unzip(lib,addonfolder,dp)
	time.sleep(1)
	try:
		os.remove(lib)
	except:
		pass


	dialog.ok(AddonTitle, "ECHO Repository successfully installed")
	
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
				dp.update(int(update))
				__in.extract(item, _out)
			
			except Exception, e:
				print str(e)

	except Exception, e:
		print str(e)
		return False
		
	return True
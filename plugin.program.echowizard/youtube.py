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
import search

AddonTitle="[COLOR lime]ECHO[/COLOR] [COLOR white]Wizard[/COLOR]"
addon_id = 'plugin.program.echowizard'
ADDON = xbmcaddon.Addon(id=addon_id)
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'resources/art/youtube.jpg'))
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
SEARCH_ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/search.png'))
YOUTUBE_ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/youtube.png'))
BASEURL = base64.b64decode(b"aHR0cDovL2VjaG9jb2Rlci5jb20v")
ECHO_CHANNEL = BASEURL + base64.b64decode(b"eW91dHViZS95b3V0dWJlLnBocD9pZD1VQ29ZVkVRd3psU3VFLU4yQ3VLdlFKNHc=")
TEAMPASS = BASEURL + base64.b64decode(b"eW91dHViZS90ZWFtdGRicGFzc3dvcmQudHh0")
YOUTUBELIST = BASEURL + base64.b64decode(b"eW91dHViZS9tYWlubGlzdC50eHQ=")
CHANNELS = BASEURL + base64.b64decode(b"eW91dHViZS9jaGFubmVscy50eHQ=")

#######################################################################
#						YOUTUBE SECTION
#######################################################################

def MAINMENU():

    link = Common.OPEN_URL(ECHO_CHANNEL)
    patron = "<video>(.*?)</video>"
    videos = re.findall(patron,link,re.DOTALL)

    items = []
    for video in videos:
        item = {}
        item["name"] = Common.find_single_match(video,"<name>([^<]+)</name>")
        item["url"] = base64.b64decode(b"cGx1Z2luOi8vcGx1Z2luLnZpZGVvLnlvdXR1YmUvP2FjdGlvbj1wbGF5X3ZpZGVvJnZpZGVvaWQ9")+Common.find_single_match(video,"<id>([^<]+)</id>")
        item["author"] = Common.find_single_match(video,"<author>([^<]+)</author>")
        item["iconimage"] = Common.find_single_match(video,"<iconimage>([^<]+)</iconimage>")
        item["date"] = Common.find_single_match(video,"<date>([^<]+)</date>")
		
        Common.addItem('[COLOR white]' + item["name"] + ' - on ' + item["date"] + '[/COLOR]',item["url"],95,item["iconimage"],FANART,'')

def OTHER_CHANNELS(url):

	link = Common.OPEN_URL(url).replace('\n','').replace('\r','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)"').findall(link)
	for name,url,icon,fanart in match:
		Common.addDir("[COLOR smokewhite]" + name + " [/COLOR]",url,61,icon,FANART,'')

def LOADITEM(name,url):

	tag = url
	list = Common.OPEN_URL(CHANNELS).replace('\n','').replace('\r','')
	match = re.compile('url="(.+?)"').findall(list)
	for url in match:
		link = Common.OPEN_URL(url)
		patron = "<video>(.*?)</video>"
		videos = re.findall(patron,link,re.DOTALL)
		items = []
		for video in videos:
			item = {}
			item["name"] = Common.find_single_match(video,"<name>([^<]+)</name>")
			item["url"] = base64.b64decode(b"cGx1Z2luOi8vcGx1Z2luLnZpZGVvLnlvdXR1YmUvP2FjdGlvbj1wbGF5X3ZpZGVvJnZpZGVvaWQ9")+Common.find_single_match(video,"<id>([^<]+)</id>")
			item["author"] = Common.find_single_match(video,"<author>([^<]+)</author>")
			item["iconimage"] = Common.find_single_match(video,"<iconimage>([^<]+)</iconimage>")
			item["date"] = Common.find_single_match(video,"<date>([^<]+)</date>")		
			if str(tag.lower()) in item["name"].lower():
				Common.addItem('[COLOR white]' + item["name"] + ' - ' + '[COLOR orangered] Published by ' + item["author"] + ' on ' + item["date"] + '[/COLOR]',item["url"],95,item["iconimage"],FANART,'')

def LOADLIST(name,url):

    if "search" in name.lower():
        search.YOUTUBE()
    else:
         link = Common.OPEN_URL(url)
    patron = "<video>(.*?)</video>"
    videos = re.findall(patron,link,re.DOTALL)

    items = []
    for video in videos:
        item = {}
        item["name"] = Common.find_single_match(video,"<name>([^<]+)</name>")
        item["url"] = base64.b64decode(b"cGx1Z2luOi8vcGx1Z2luLnZpZGVvLnlvdXR1YmUvP2FjdGlvbj1wbGF5X3ZpZGVvJnZpZGVvaWQ9")+Common.find_single_match(video,"<id>([^<]+)</id>")
        item["author"] = Common.find_single_match(video,"<author>([^<]+)</author>")
        item["iconimage"] = Common.find_single_match(video,"<iconimage>([^<]+)</iconimage>")
        item["date"] = Common.find_single_match(video,"<date>([^<]+)</date>")
		
        Common.addItem('[COLOR white]' + item["name"] + ' - ' + '[COLOR orangered] Published by ' + item["author"] + ' on ' + item["date"] + '[/COLOR]',item["url"],95,item["iconimage"],FANART,'')
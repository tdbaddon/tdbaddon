'''
    Ultimate Whitecream
    Copyright (C) 2016 mortael, hdgdl
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
'''

import urllib2
import os
import sys
import random
import sqlite3
import json

import xbmc
import xbmcplugin
import xbmcgui
from resources.lib import utils



#elif mode == 475: camsoda.Main()
    #elif mode == 476: camsoda.List(url)
    #elif mode == 478: camsoda.Playvid(url, name)
    #elif mode == 479: camsoda.clean_database(True)

def Main():
	utils.addDir('[COLOR red]Refresh Camsoda images[/COLOR]','',479,'',Folder=False)
	List('http://www.camsoda.com/api/v1/browse/online')
	xbmcplugin.endOfDirectory(utils.addon_handle)


def List(url):
    if utils.addon.getSetting("chaturbate") == "true":
        clean_database()
    response = urllib2.urlopen(url)
    data = json.load(response)
    for camgirl in data['results']:
        name = camgirl['slug'] + " [" + camgirl['status'] + "]"
        videourl = "https://www.camsoda.com/api/v1/video/vtoken/" + camgirl['slug'] + "?username=guest_" + str(random.randrange(100, 55555))
        img = "https:" + camgirl['thumb']
        utils.addDownLink(name, videourl, 478, img, '', noDownload=True)
    xbmcplugin.endOfDirectory(utils.addon_handle)

def clean_database(showdialog=False):
    conn = sqlite3.connect(xbmc.translatePath("special://database/Textures13.db"))
    try:
        with conn:
            list = conn.execute("SELECT id, cachedurl FROM texture WHERE url LIKE '%%%s%%';" % "m.camsoda.com")
            for row in list:
                conn.execute("DELETE FROM sizes WHERE idtexture LIKE '%s';" % row[0])
                try: os.remove(xbmc.translatePath("special://thumbnails/" + row[1]))
                except: pass
            conn.execute("DELETE FROM texture WHERE url LIKE '%%%s%%';" % "m.camsoda.com")
            if showdialog:
                utils.notify('Finished','Camsoda images cleared')
    except:
        pass


def Playvid(url, name):
    response = urllib2.urlopen(url)
    data = json.load(response)
    if "camhouse" in data['stream_name']:
       videourl = "https://camhouse.camsoda.com/" + data['app'] + "/mp4:" + data['stream_name'] + "_mjpeg/playlist.m3u8?token=" + data['token']
    else:
       videourl = "https://" + data['edge_servers'][1] + "/" + data['app'] + "/mp4:" + data['stream_name'] + "_mjpeg/playlist.m3u8?token=" + data['token']
    iconimage = xbmc.getInfoImage("ListItem.Thumb")
    listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
    listitem.setProperty("IsPlayable","true")
    if int(sys.argv[1]) == -1:
       pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
       pl.clear()
       pl.add(videourl, listitem)
       xbmc.Player().play(pl)
    else:
       listitem.setPath(str(videourl))
       xbmcplugin.setResolvedUrl(utils.addon_handle, True, listitem)


'''
    Ultimate Whitecream
    Copyright (C) 2015 mortael

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

import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon, sqlite3

import utils

from chaturbate import clean_database as cleanchat
from cam4 import clean_database as cleancam4

dialog = utils.dialog
favoritesdb = utils.favoritesdb



conn = sqlite3.connect(favoritesdb)
c = conn.cursor()
try:
    c.executescript("CREATE TABLE IF NOT EXISTS favorites (name, url, mode, image);")
    c.executescript("CREATE TABLE IF NOT EXISTS keywords (keyword);")
except:
    pass
conn.close()


def List():
    if utils.addon.getSetting("chaturbate") == "true":
        cleanchat()
        cleancam4()
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM favorites")
        for (name, url, mode, img) in c.fetchall():
            utils.addDownLink(name, url, int(mode), img, '', '', 'del')
        conn.close()
        xbmcplugin.endOfDirectory(utils.addon_handle)
    except:
        conn.close()
        utils.notify('No Favorites','No Favorites found')
        return


def Favorites(fav,mode,name,url,img):
    if fav == "add":
        delFav(url)
        addFav(mode, name, url, img)
        utils.notify('Favorite added','Video added to the favorites')
    elif fav == "del":
        delFav(url)
        utils.notify('Favorite deleted','Video removed from the list')
        xbmc.executebuiltin('Container.Refresh')


def addFav(mode,name,url,img):
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    c.execute("INSERT INTO favorites VALUES (?,?,?,?)", (name, url, mode, img))
    conn.commit()
    conn.close()


def delFav(url):
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    c.execute("DELETE FROM favorites WHERE url = '%s'" % url)
    conn.commit()
    conn.close()



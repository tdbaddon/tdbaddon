# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

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


import os
import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui
import xbmcvfs


lang = xbmcaddon.Addon().getLocalizedString

setting = xbmcaddon.Addon().getSetting

addon = xbmcaddon.Addon

addItem = xbmcplugin.addDirectoryItem

item = xbmcgui.ListItem

directory = xbmcplugin.endOfDirectory

content = xbmcplugin.setContent

addonInfo = xbmcaddon.Addon().getAddonInfo

infoLabel = xbmc.getInfoLabel

condVisibility = xbmc.getCondVisibility

window = xbmcgui.Window(10000)

dialog = xbmcgui.Dialog()

windowDialog = xbmcgui.WindowDialog()

image = xbmcgui.ControlImage

keyboard = xbmc.Keyboard

sleep = xbmc.sleep

execute = xbmc.executebuiltin

skin = xbmc.getSkinDir()

player = xbmc.Player()

playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)

resolve = xbmcplugin.setResolvedUrl

openFile = xbmcvfs.File

makeFile = xbmcvfs.mkdir

deleteFile = xbmcvfs.delete

skinPath = xbmc.translatePath('special://skin/')

addonPath = xbmc.translatePath(addonInfo('path'))

dataPath = xbmc.translatePath(addonInfo('profile')).decode('utf-8')

databaseFile = os.path.join(dataPath, 'settings.db')

cachesourcesFile = os.path.join(dataPath, 'sources.db')

cachemetaFile = os.path.join(dataPath, 'metacache.db')

cacheFile = os.path.join(dataPath, 'cache.db')


def addonIcon():
    appearance = setting('appearance').lower()
    if appearance == '-': return addonInfo('icon')
    elif appearance == '': return addonInfo('icon')
    else: return os.path.join(addonPath, 'resources', 'art', appearance, 'icon.png')


def addonThumb():
    appearance = setting('appearance').lower()
    if appearance == '-': return 'DefaultFolder.png'
    elif appearance == '': return addonInfo('icon')
    else: return os.path.join(addonPath, 'resources', 'art', appearance, 'icon.png')


def addonFanart():
    appearance = setting('appearance').lower()
    if appearance == '-': return None
    elif appearance == '': return addonInfo('fanart')
    else: return os.path.join(addonPath, 'resources', 'art', appearance, 'fanart.jpg')


def artPath():
    appearance = setting('appearance').lower()
    if appearance == '-': return None
    elif appearance == '': return None
    else: return os.path.join(addonPath, 'resources', 'art', appearance)


def infoDialog(message, heading=addonInfo('name'), icon=addonIcon(), time=3000):
    try: dialog.notification(heading, message, icon, time, sound=False)
    except: execute("Notification(%s,%s, %s, %s)" % (heading, message, time, icon))


def yesnoDialog(line1, line2, line3, heading=addonInfo('name'), nolabel='', yeslabel=''):
    return dialog.yesno(heading, line1, line2, line3, nolabel, yeslabel)


def selectDialog(list, heading=addonInfo('name')):
    return dialog.select(heading, list)


def refresh():
    return execute('Container.Refresh')


def queueItem():
    return execute('Action(Queue)')


def openPlaylist():
    return execute('ActivateWindow(VideoPlaylist)')


def openSettings(id=addonInfo('id'), c=None, f=None):
    try:
        execute('Addon.OpenSettings(%s)' % id)
        if c == None or  f == None: raise Exception()
        execute('SetFocus(%i)' % (int(c) + 100))
        execute('SetFocus(%i)' % (int(f) + 200))
    except:
        return


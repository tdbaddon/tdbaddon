# -*- coding: utf-8 -*-

'''
    gClone Add-on
    Copyright (C) 2015 NVTTeam

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

addonInfo = xbmcaddon.Addon().getAddonInfo

infoLabel = xbmc.getInfoLabel

resolve = xbmcplugin.setResolvedUrl

window = xbmcgui.Window(10000)

dialog = xbmcgui.Dialog()

windowDialog = xbmcgui.WindowDialog()

image = xbmcgui.ControlImage

keyboard = xbmc.Keyboard

execute = xbmc.executebuiltin

player = xbmc.Player()

openFile = xbmcvfs.File

deleteFile = xbmcvfs.delete

addonPath = xbmc.translatePath(addonInfo('path'))

dataPath = xbmc.translatePath(addonInfo('profile')).decode('utf-8')

databaseFile = os.path.join(dataPath, 'settings.db')

cachesourcesFile = os.path.join(dataPath, 'sources.db')

cacheFile = os.path.join(dataPath, 'cache.db')


def addonFanart():
    appearance = setting('appearance').lower()
    if not appearance == '-': return os.path.join(addonPath, 'resources', 'art', appearance, 'fanart.jpg')
    return None


def infoDialog(message, heading=addonInfo('name'), time=3000):
    try: dialog.notification(heading, message, addonInfo('icon'), time, sound=False)
    except: execute("Notification(%s,%s, %s, %s)" % (heading, message, time, addonInfo('icon')))


def yesnoDialog(line1, line2, heading=addonInfo('name'), nolabel='', yeslabel=''):
    return dialog.yesno(heading, line1, line2, '', nolabel, yeslabel)


def selectDialog(list, heading=addonInfo('name')):
    return dialog.select(heading, list)


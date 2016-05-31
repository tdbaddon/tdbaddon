# -*- coding: utf-8 -*-

'''
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


import os,xbmc,xbmcaddon,xbmcplugin,xbmcgui,xbmcvfs


lang = xbmcaddon.Addon().getLocalizedString

setting = xbmcaddon.Addon().getSetting

addon = xbmcaddon.Addon

addItem = xbmcplugin.addDirectoryItem

item = xbmcgui.ListItem

directory = xbmcplugin.endOfDirectory

content = xbmcplugin.setContent

property = xbmcplugin.setProperty

addonInfo = xbmcaddon.Addon().getAddonInfo

infoLabel = xbmc.getInfoLabel

condVisibility = xbmc.getCondVisibility

jsonrpc = xbmc.executeJSONRPC

window = xbmcgui.Window(10000)

dialog = xbmcgui.Dialog()

progressDialog = xbmcgui.DialogProgress()

windowDialog = xbmcgui.WindowDialog()

button = xbmcgui.ControlButton

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

listDir = xbmcvfs.listdir

transPath = xbmc.translatePath

skinPath = xbmc.translatePath('special://skin/')

addonPath = xbmc.translatePath(addonInfo('path'))

dataPath = xbmc.translatePath(addonInfo('profile')).decode('utf-8')

settingsFile = os.path.join(dataPath, 'settings.xml')

databaseFile = os.path.join(dataPath, 'settings.db')

favouritesFile = os.path.join(dataPath, 'favourites.db')

sourcescacheFile = os.path.join(dataPath, 'sources.db')

cachemetaFile = os.path.join(dataPath, 'metacache.db')

libcacheFile = os.path.join(dataPath, 'library.db')

metacacheFile = os.path.join(dataPath, 'meta.db')

cacheFile = os.path.join(dataPath, 'cache.db')

# List          xbmc.executebuiltin('Container.SetViewMode(502)')
# Big List      xbmc.executebuiltin('Container.SetViewMode(51)')
# Thumbnails    xbmc.executebuiltin('Container.SetViewMode(500)')
# Poster Wrap   xbmc.executebuiltin('Container.SetViewMode(501)')
# Fanart        xbmc.executebuiltin('Container.SetViewMode(508)')
# Media info    xbmc.executebuiltin('Container.SetViewMode(504)')
# Media info 2  xbmc.executebuiltin('Container.SetViewMode(503)')
# Media info 3  xbmc.executebuiltin('Container.SetViewMode(515)')
viewMode = {'list':502, 'biglist':51, 'thumbnails':500, 'posterwrap':501, 'fanart':508, 'mediainfo1':504,'mediainfo2':503, 'mediainfo3':515}

def addonIcon():
    #appearance = setting('appearance').lower()
    #if appearance in ['-', '']: return addonInfo('icon')
    #else:
    return os.path.join(addonPath, 'resources', 'media', 'icon.png')

def addonPoster():
    #appearance = setting('appearance').lower()
    #if appearance in ['-', '']: return 'DefaultVideo.png'
    #else:
    return os.path.join(addonPath, 'resources', 'media', 'poster.png')

def addonBanner():
    #appearance = setting('appearance').lower()
    #if appearance in ['-', '']: return 'DefaultVideo.png'
    #else:
    return os.path.join(addonPath, 'resources', 'media', 'banner.png')

def addonThumb():
    #appearance = setting('appearance').lower()
    #if appearance == '-': return 'DefaultFolder.png'
    #elif appearance == '': return addonInfo('icon')
    #else:
    #return os.path.join(addonPath, 'resources', 'media', appearance, 'icon.png')
    return os.path.join(addonPath, 'resources', 'media', 'icon.png')

def addonFanart():
    #appearance = setting('appearance').lower()
    #if appearance == '-': return None
    #elif appearance == '': return addonInfo('fanart')
    #else:
    return os.path.join(addonPath, 'resources', 'media', 'fanart.png')

def addonNext():
    appearance = setting('appearance').lower()
    #if appearance in ['-', '']: return 'DefaultFolderBack.png'
    #else:
    return os.path.join(addonPath, 'resources', 'media', 'next.png')

def artPath():
    return os.path.join(addonPath, 'resources', 'media')

def infoDialog(message, heading=addonInfo('name'), icon=addonIcon(), time=3000):
    try: dialog.notification(heading, message, icon, time, sound=False)
    except: execute("Notification(%s,%s, %s, %s)" % (heading, message, time, icon))

def yesnoDialog(line1, line2, line3, heading=addonInfo('name'), nolabel='', yeslabel=''):
    return dialog.yesno(heading, line1, line2, line3, nolabel, yeslabel)

def selectDialog(list, heading=addonInfo('name')):
    return dialog.select(heading, list)

def version():
    num = ''
    try: version = addon('xbmc.addon').getAddonInfo('version')
    except: version = '999'
    for i in version:
        if i.isdigit(): num += i
        else: break
    return int(num)

def refresh():
    return execute('Container.Refresh')

def idle():
    return execute('Dialog.Close(busydialog)')

def queueItem():
    return execute('Action(Queue)')

def openPlaylist():
    return execute('ActivateWindow(VideoPlaylist)')

def openSettings(query=None, id=addonInfo('id')):
    try:
        idle()
        execute('Addon.OpenSettings(%s)' % id)
        if query == None: raise Exception()
        c, f = query.split('.')
        execute('SetFocus(%i)' % (int(c) + 100))
        execute('SetFocus(%i)' % (int(f) + 200))
    except:
        return
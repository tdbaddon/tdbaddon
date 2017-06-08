# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2017 Aftershockpy

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

import urlparse,os,sys
import xbmc,xbmcaddon,xbmcplugin,xbmcgui,xbmcvfs


lang = xbmcaddon.Addon().getLocalizedString

setting = xbmcaddon.Addon().getSetting

setSetting = xbmcaddon.Addon().setSetting

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

sourcescacheFile = os.path.join(dataPath, 'sources.db')

libcacheFile = os.path.join(dataPath, 'library.db')

metacacheFile = os.path.join(dataPath, 'meta.db')

cacheFile = os.path.join(dataPath, 'cache.db')

def artwork():
    execute('RunPlugin(plugin://script.aftershock.artwork)')

def appearance():
    appearance = setting('appearance').lower() if condVisibility('System.HasAddon(script.aftershock.artwork)') else setting('appearance.alt').lower()
    return appearance

def addonIcon():
    theme = appearance() ; art = artPath()
    if not (art == None and theme in ['-', '']): return os.path.join(art, 'icon.png')
    return addonInfo('icon')


def addonThumb():
    theme = appearance() ; art = artPath()
    if not (art == None and theme in ['-', '']): return os.path.join(art, 'poster.png')
    elif theme == '-': return 'DefaultFolder.png'
    return addonInfo('icon')

def addonPoster():
    theme = appearance() ; art = artPath()
    if not (art == None and theme in ['-', '']): return os.path.join(art, 'poster.png')
    return 'DefaultVideo.png'

def addonBanner():
    theme = appearance() ; art = artPath()
    if not (art == None and theme in ['-', '']): return os.path.join(art, 'banner.png')
    return 'DefaultVideo.png'

def addonFanart():
    theme = appearance() ; art = artPath()
    if not (art == None and theme in ['-', '']): return os.path.join(art, 'fanart.png')
    return addonInfo('fanart')

def addonNext():
    theme = appearance() ; art = artPath()
    if not (art == None and theme in ['-', '']): return os.path.join(art, 'next.png')
    return 'DefaultVideo.png'

def artPath():
    theme = appearance()
    if theme in ['-', '']: return
    elif condVisibility('System.HasAddon(script.aftershock.artwork)'):
        return os.path.join(xbmcaddon.Addon('script.aftershock.artwork').getAddonInfo('path'), 'resources', 'media', theme)

def logoPath():
    if condVisibility('System.HasAddon(script.aftershock.artwork)'):
        return os.path.join(xbmcaddon.Addon('script.aftershock.artwork').getAddonInfo('path'), 'resources', 'media', 'logos')

def infoDialog(message, heading=addonInfo('name'), icon=addonIcon(), time=3000):
    try: dialog.notification(heading, message, icon, time, sound=False)
    except: execute("Notification(%s,%s, %s, %s)" % (heading, message, time, icon))

def yesnoDialog(line1, line2, line3, heading=addonInfo('name'), nolabel='', yeslabel=''):
    return dialog.yesno(heading, line1, line2, line3, nolabel, yeslabel)

def okDialog(line1, line2=None, line3=None, heading=addonInfo('name')):
    return dialog.ok(heading, line1, line2, line3)

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

def moderator():
    netloc = [urlparse.urlparse(sys.argv[0]).netloc, '']

    if not infoLabel('Container.PluginName') in netloc: sys.exit()

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

def delete(fileName):
    try :
        filePath = os.path.join(dataPath, fileName)
        if xbmcvfs.exists(filePath):
            xbmcvfs.delete(filePath)
        return '1'
    except:
        return '1'

def deleteAll(extn):
    try :
        dirs, files = xbmcvfs.listdir(dataPath)
        for file in files:
            if extn in file:
                filePath = os.path.join(dataPath, file)
                xbmcvfs.delete(filePath)
        return '1'
    except:
        return '1'

def resetSettings(forceReset, version):
    try :
        if xbmcvfs.exists(settingsFile):
            xbmcvfs.delete(settingsFile)
        return '1'
    except:
        return '1'

# estuary View Modes :
## List          xbmc.executebuiltin('Container.SetViewMode(50)')
## Poster        xbmc.executebuiltin('Container.SetViewMode(51)')
## Shift         xbmc.executebuiltin('Container.SetViewMode(53)')
## InfoWall      xbmc.executebuiltin('Container.SetViewMode(54)')
## WideList      xbmc.executebuiltin('Container.SetViewMode(55)')
## Wall          xbmc.executebuiltin('Container.SetViewMode(500)')
## FanArt        xbmc.executebuiltin('Container.SetViewMode(502)')

# Confluence
# List          xbmc.executebuiltin('Container.SetViewMode(502)')
# Big List      xbmc.executebuiltin('Container.SetViewMode(51)')
# Thumbnails    xbmc.executebuiltin('Container.SetViewMode(500)')
# Poster Wrap   xbmc.executebuiltin('Container.SetViewMode(501)')
# Fanart        xbmc.executebuiltin('Container.SetViewMode(508)')
# Media info    xbmc.executebuiltin('Container.SetViewMode(504)')
# Media info 2  xbmc.executebuiltin('Container.SetViewMode(503)')
# Media info 3  xbmc.executebuiltin('Container.SetViewMode(515)')

viewMode = {
            'confluence':{'list':'502', 'biglist':'51', 'thumbnails':'500', 'posterwrap':'501', 'fanart':'508', 'mediainfo1':'504','mediainfo2':'503', 'mediainfo3':'515'},
            'esturary':{'list':'50', 'poster':'51', 'shift':'53', 'infowall':'54', 'widelist':'55', 'wall':'500', 'fanart':'502'}
            }

#confluence :
#estouchy : 50, 500, 550
#esturary : 50,51,52,53,54,55,500,501,502
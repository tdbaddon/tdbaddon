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


import os,xbmc,xbmcaddon,xbmcvfs

addon = xbmcaddon.Addon(id='script.aftershocknow.guide')

setting = addon.getSetting

setSetting = addon.setSetting

addonInfo = addon.getAddonInfo

jsonrpc = xbmc.executeJSONRPC

execute = xbmc.executebuiltin

makeFile = xbmcvfs.mkdir

skinPath = xbmc.translatePath('special://skin/')

addonPath = xbmc.translatePath(addonInfo('path'))

dataPath = xbmc.translatePath(addonInfo('profile')).decode('utf-8')

def artwork():
    execute('RunPlugin(plugin://script.aftershock.artwork)')

def logoPath():
    return os.path.join(xbmcaddon.Addon('script.aftershock.artwork').getAddonInfo('path'), 'resources', 'media', 'logos')

def version():
    num = ''
    try: version = addon('xbmc.addon').getAddonInfo('version')
    except: version = '999'
    for i in version:
        if i.isdigit(): num += i
        else: break
    return int(num)
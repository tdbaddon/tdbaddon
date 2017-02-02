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

import os
import sys
import urlparse

from resources.lib.modules import control
from resources.lib.modules import logger
from resources.lib.modules import views
from resources.lib.modules import analytics

sysaddon = sys.argv[0] ; syshandle = int(sys.argv[1])

artPath = control.artPath() ; addonFanart = control.addonFanart()

try: action = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))['action']
except: action = None

imdbMode = False if control.setting('imdb_user') == '' else True

class navigator:
    def __init__(self):
        self.index_provider = control.setting('idx_provider')

    def root(self):

        self.addDirectoryItem(30860, 'movieLangNavigator', 'movies.png','DefaultMovies.png')
        self.addDirectoryItem(90114, 'desiLiveNavigator', 'tv-live.png','DefaultMovies.png')
        self.addDirectoryItem(90115, 'liveEPGNavigator', 'tv-epg.png','DefaultMovies.png')
        self.addDirectoryItem(30861, 'desiTVNavigator', 'tv-vod.png','DefaultMovies.png')

        self.addDirectoryItem(90116, 'openSettings&query=0.0', 'settings.png', 'DefaultMovies.png')
        self.addDirectoryItem(90117, 'clearCache', 'clearcache.png', 'DefaultMovies.png')
        self.addDirectoryItem(30864, 'changelog', 'changelog.png', 'DefaultMovies.png')

        from resources.lib.modules import cache
        from resources.lib.modules import changelog
        cache.get(changelog.get, 600000000, control.addonInfo('version'), table='changelog')
        cache.get(self.donation, 600000000, control.addonInfo('version'), table='changelog')
        #cache.get(control.resetSettings, 600000000, 'true', control.addonInfo('version'), table='changelog')
        cache.get(analytics.sendAnalytics, 600000000, ("Installed-%s" % control.addonInfo('version')), table='changelog')

        self.endDirectory()

    def donation(self, version):
        control.okDialog("Donations for this addon [Aftershock v%s] gracefully accepted at" % version, "", "http://paypal.me/aftershockpy/10USD")
        return 1

    def clearCache(self, url=None):
        if url == None:
            self.addDirectoryItem(90124, 'clearCache&url=main', 'clearcache.png','DefaultMovies.png')
            self.addDirectoryItem(90125, 'clearCache&url=providers', 'clearcache.png','DefaultMovies.png')
            self.addDirectoryItem(90126, 'clearCache&url=live', 'clearcache.png','DefaultMovies.png')
            self.addDirectoryItem(90127, 'clearCache&url=meta', 'clearcache.png','DefaultMovies.png')

            self.endDirectory(confViewMode='list')
        elif url == 'main':
            from resources.lib.modules import cache
            cache.clear()
        elif url == 'providers':
            from resources.lib.modules import cache
            cache.clear(['rel_src', 'rel_url'], control.sourcescacheFile)
        elif url == 'live' :
            from resources.lib.modules import cache
            control.deleteAll('.json')
            control.delete('user.db')
            cache.clear(['rel_live', 'rel_logo', 'live_meta'], control.sourcescacheFile)
            cache.clear(['live_cache'])
        elif url == 'meta':
            from resources.lib.modules import cache
            cache.clear(['meta', 'meta_imdb'], control.metacacheFile)

    def desiLiveTV(self, url=None):
        from resources.lib.indexers import livetv
        if url == None :
            genres = livetv.sources().getLiveGenre()
            self.addDirectoryItem('ALL', 'desiLiveNavigator&url=all', 'tv-live.png','DefaultMovies.png')
            for genre in genres:
                self.addDirectoryItem(genre.upper(), 'desiLiveNavigator&url=%s' % genre, 'tv-live.png','DefaultMovies.png')
            self.addDirectoryItem('OTHERS', 'desiLiveNavigator&url=others', 'tv-live.png','DefaultMovies.png')
            self.endDirectory(confViewMode='list')
        else:
            livetv.channels().get(url)

    def desiTV(self):
        listItems = []

        provider = control.setting('tvshow.provider')

        if not provider == None:
            try:
                call = __import__('resources.lib.sources.%s' % provider, globals(), locals(), ['source'], -1).source()
                listItems = call.networks()
            except Exception as e:
                logger.error(e)
                pass
        else:
            from resources.lib.sources import desirulez
            listItems = desirulez.source().networks()

        listItems.sort()

        for item in listItems:
            self.addDirectoryItem(item['name'], '%s&provider=%s&url=%s' % (item['action'],item['provider'], item['url']), os.path.join(
                control.logoPath(), item['image']), 'DefaultMovies.png')

        self.endDirectory()

    def search(self):
        self.addDirectoryItem(30151, 'movieSearch', 'search.jpg', 'DefaultMovies.png')
        self.addDirectoryItem(30152, 'tvSearch', 'search.jpg', 'DefaultTVShows.png')
        self.addDirectoryItem(30153, 'moviePerson', 'moviePerson.jpg', 'DefaultMovies.png')
        self.addDirectoryItem(30154, 'tvPerson', 'tvPerson.jpg', 'DefaultTVShows.png')

        self.endDirectory()

    def addDirectoryItem(self, name, query, thumb, icon, context=None, isAction=True, isFolder=True):
        try: name = control.lang(name).encode('utf-8')
        except: pass
        url = '%s?action=%s&name=%s' % (sysaddon, query, name) if isAction == True else query

        if not 'http' in thumb :
            thumb = os.path.join(artPath, thumb) if not artPath == None else icon

        cm = []

        if not context == None: cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name, iconImage=thumb, thumbnailImage=thumb)
        item.addContextMenuItems(cm)
        if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

    def endDirectory(self, cacheToDisc=False, estViewMode='biglist', confViewMode='thumbnails'):
        control.content(syshandle, 'addons')
        views.setView('addons', {'skin.confluence': control.viewMode['confluence'][confViewMode], 'skin.estuary':
            control.viewMode['esturary'][estViewMode]})
        control.directory(syshandle, cacheToDisc=cacheToDisc)
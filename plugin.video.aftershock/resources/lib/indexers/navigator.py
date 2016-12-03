# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2015 IDev

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


import os,sys,urlparse

from resources.lib.libraries import control
from resources.lib.libraries import views
from resources.lib.libraries import logger
from resources.lib.libraries import analytics

artPath = control.artPath() ; addonFanart = control.addonFanart()

try: action = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))['action']
except: action = None

imdbMode = False if control.setting('imdb_user') == '' else True

sysaddon = sys.argv[0]

class navigator:
    def __init__(self):
        self.index_provider = control.setting('idx_provider')
        self.langProviderMap = {'hindi':self.index_provider,
                                'tamil':self.index_provider,
                                'telugu':self.index_provider,
                                'marathi':'ibollytv',
                                'punjabi':'ibollytv',
                                'bengali':'ibollytv',
                                'gujarati':'ibollytv',
                                'malayalam':'ibollytv',
                                'kannada':'ibollytv'}

    def root(self):

        self.addDirectoryItem(30860, 'movieLangNavigator', 'movies.png','DefaultMovies.png')
        self.addDirectoryItem(90114, 'desiLiveNavigator', 'tv-live.png','DefaultMovies.png')
        self.addDirectoryItem(90115, 'liveEPGNavigator', 'tv-epg.png','DefaultMovies.png')
        self.addDirectoryItem(30861, 'desiTVNavigator', 'tv-vod.png','DefaultMovies.png')

        self.addDirectoryItem(90116, 'openSettings&query=0.0', 'settings.png', 'DefaultMovies.png')
        self.addDirectoryItem(90117, 'clearCache', 'clearcache.png', 'DefaultMovies.png')

        self.endDirectory()


        from resources.lib.libraries import cache
        from resources.lib.libraries import changelog
        cache.get(changelog.get, 600000000, control.addonInfo('version'), table='changelog')
        #cache.get(control.resetSettings, 600000000, 'true', control.addonInfo('version'), table='changelog')
        cache.get(analytics.sendAnalytics, 600000000, ("Installed-%s" % control.addonInfo('version')), table='changelog')

    def clearCache(self, url=None):
        if url == None:
            self.addDirectoryItem(90124, 'clearCache&url=main', 'clearcache.png','DefaultMovies.png')
            self.addDirectoryItem(90125, 'clearCache&url=providers', 'clearcache.png','DefaultMovies.png')
            self.addDirectoryItem(90126, 'clearCache&url=live', 'clearcache.png','DefaultMovies.png')
            self.addDirectoryItem(90127, 'clearCache&url=meta', 'clearcache.png','DefaultMovies.png')

            self.endDirectory(viewMode='list')
        elif url == 'main':
            from resources.lib.libraries import cache
            cache.clear()
        elif url == 'providers':
            from resources.lib.libraries import cache
            cache.clear(['rel_src', 'rel_url'], control.sourcescacheFile)
        elif url == 'live' :
            from resources.lib.libraries import cache
            control.delete('static.json')
            control.delete('ditto.json')
            control.delete('cinefun.json')
            control.delete('dynns.json')
            control.delete('swift.json')
            cache.clear(['rel_live','rel_logo'], control.sourcescacheFile)
        elif url == 'meta':
            from resources.lib.libraries import cache
            cache.clear(['meta', 'meta_imdb'], control.metacacheFile)

    def desiLangMovies(self):
        self.addDirectoryItem(30201, 'movieSearch', 'search.png', 'DefaultMovies.png')
        self.addDirectoryItem(90105, 'movieNavigator&lang=%s' % 'hindi', 'language.png', 'DefaultMovies.png')
        self.addDirectoryItem(90106, 'movieNavigator&lang=%s' % 'tamil', 'language.png', 'DefaultMovies.png')
        self.addDirectoryItem(90107, 'movieNavigator&lang=%s' % 'telugu', 'language.png', 'DefaultMovies.png')
        self.addDirectoryItem(90118, 'movieNavigator&lang=%s' % 'marathi', 'language.png', 'DefaultMovies.png')
        self.addDirectoryItem(90119, 'movieNavigator&lang=%s' % 'punjabi', 'language.png', 'DefaultMovies.png')
        self.addDirectoryItem(90120, 'movieNavigator&lang=%s' % 'bengali', 'language.png', 'DefaultMovies.png')
        self.addDirectoryItem(90121, 'movieNavigator&lang=%s' % 'gujarati', 'language.png', 'DefaultMovies.png')
        self.addDirectoryItem(90122, 'movieNavigator&lang=%s' % 'malayalam', 'language.png', 'DefaultMovies.png')
        self.addDirectoryItem(90123, 'movieNavigator&lang=%s' % 'kannada', 'language.png', 'DefaultMovies.png')
        self.endDirectory()

    def desiMovies(self, lang):
        index_provider = self.langProviderMap[lang]
        if lang in 'hindi, tamil, telugu':
            self.addDirectoryItem(90109, 'movieGenres&provider=%s_mv&lang=%s' % (index_provider, lang), 'genre.png', 'DefaultMovies.png')
            self.addDirectoryItem(90110, 'movieYears&provider=%s_mv&lang=%s' % (index_provider, lang), 'year.png', 'DefaultMovies.png')
        self.addDirectoryItem(90103, 'movies&url=theaters&provider=%s_mv&lang=%s' % (index_provider, lang), 'new.png', 'DefaultMovies.png')
        self.addDirectoryItem(90104, 'movies&url=added&provider=%s_mv&lang=%s' % (index_provider, lang), 'latest.png', 'DefaultMovies.png')
        if lang in 'hindi, tamil, telugu':
            index_provider = 'hdbuffer'
            self.addDirectoryItem(90108, 'movies&url=HD&provider=%s_mv&lang=%s' % (index_provider, lang), 'dvd2hd.png', 'DefaultMovies.png')
        self.endDirectory()

    def desiLiveTV(self):
        from resources.lib.indexers import livetv
        livetv.channels.get()

    def desiTV(self):
        listItems = []
        logoBaseURL=control.logoPath() + "\\"

        provider = control.setting('tvshow.provider')

        if not provider == None:
            for i in ('_mv_tv', '_tv'):
                try:
                    tProvider = provider + i
                    call = __import__('resources.lib.sources.%s' % tProvider, globals(), locals(), ['source'], -1).source()
                    listItems = call.get_networks(logoBaseURL)
                    if len(listItems) > 0 :
                        break
                except Exception as e:
                    logger.error(e)
                    pass
        else:
            from resources.lib.sources import desirulez_mv_tv
            listItems = desirulez_mv_tv.source().get_networks(logoBaseURL)
        listItems.sort()

        for item in listItems:
            self.addDirectoryItem(item['name'], '%s&provider=%s&url=%s' % (item['action'],item['provider'], item['url']), item['image'], 'DefaultMovies.png')

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
        item.addContextMenuItems(cm, replaceItems=False)
        if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=isFolder)

    def endDirectory(self, cacheToDisc=True, viewMode='thumbnails'):
        views.setView('movies', {'skin.confluence': control.viewMode[viewMode]})
        control.directory(int(sys.argv[1]), cacheToDisc=cacheToDisc)
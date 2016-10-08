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
        logoBaseURL='http://www.lyngsat-logo.com/logo/tv'
        provider = 'desirulez_tv'
        listItems.append({'provider':provider, 'name':90200, 'image': logoBaseURL+'/ss/star_plus.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=42'})
        listItems.append({'provider':provider, 'name':90201, 'image': logoBaseURL+'/zz/zee_tv.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=73'})
        listItems.append({'provider':provider, 'name':90203, 'image': logoBaseURL+'/ss/set_in.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=63'})
        listItems.append({'provider':provider, 'name':90205, 'image': logoBaseURL+'/ll/life_ok_in.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=1375'})
        listItems.append({'provider':provider, 'name':90206, 'image': logoBaseURL+'/ss/sahara_one.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=134'})
        listItems.append({'provider':provider, 'name':90207, 'image': logoBaseURL+'/ss/star_jalsha.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=667'})
        listItems.append({'provider':provider, 'name':90208, 'image': logoBaseURL+'/cc/colors_in.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=176'})
        listItems.append({'provider':provider, 'name':90209, 'image': logoBaseURL+'/ss/sony_sab_tv.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=254'})
        listItems.append({'provider':provider, 'name':90210, 'image': logoBaseURL+'/ss/star_pravah.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=1138'})
        listItems.append({'provider':provider, 'name':90212, 'image': logoBaseURL+'/mm/mtv_india.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=339'})
        listItems.append({'provider':provider, 'name':90213, 'image': logoBaseURL+'/cc/channel_v_in.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=633'})
        listItems.append({'provider':provider, 'name':90214, 'image': logoBaseURL+'/uu/utv_bindass.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=504'})
        listItems.append({'provider':provider, 'name':90215, 'image': logoBaseURL+'/uu/utv_stars.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=1274'})
        listItems.append({'provider':provider, 'name':90218, 'image': logoBaseURL+'/hh/hungama.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=472'})
        listItems.append({'provider':provider, 'name':90219, 'image': logoBaseURL+'/cc/cartoon_network_in.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=509'})
        listItems.append({'provider':provider, 'name':90220, 'image': logoBaseURL+'/aa/and_tv_in.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=3138'})
        listItems.append({'provider':provider, 'name':90222, 'image': logoBaseURL+'/cc/colors_in_bangla.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=2117'})
        listItems.append({'provider':provider, 'name':90223, 'image': logoBaseURL+'/zz/zee_zindagi_in.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=2679'})
        listItems.append({'provider':provider, 'name':90224, 'image': logoBaseURL+'/bb/big_magic_in.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=1887'})
        listItems.append({'provider':provider, 'name':90225, 'image': logoBaseURL+'/cc/colors_in_marathi.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=2369'})
        listItems.append({'provider':provider, 'name':90226, 'image': logoBaseURL+'/mm/maa_tv.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=3165'})
        listItems.append({'provider':provider, 'name':90227, 'image': logoBaseURL+'/zz/zee_marathi.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=1299'})
        listItems.append({'provider':provider, 'name':90228, 'image': logoBaseURL+'/zz/zee_bangla.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=676'})
        listItems.append({'provider':provider, 'name':90229, 'image': logoBaseURL+'/zz/zoom_tv_in.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=1876'})
        listItems.append({'provider':provider, 'name':90230, 'image': logoBaseURL+'/ss/star_vijay_in.png', 'action': 'tvshows', 'url':'forumdisplay.php?f=1609'})
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

    def endDirectory(self, cacheToDisc=True):
        views.setView('movies', {'skin.confluence': control.viewMode['thumbnails']})
        control.directory(int(sys.argv[1]), cacheToDisc=cacheToDisc)
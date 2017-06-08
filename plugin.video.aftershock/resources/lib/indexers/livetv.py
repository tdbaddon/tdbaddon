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

import json
import os
import sys
import urllib

from ashock.modules import control
from ashock.modules import views
from resources.lib.sources import sources
from ashock.modules import logger

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

sysaddon = sys.argv[0] ; syshandle = int(sys.argv[1])

class channels:
    def __init__(self):
        self.list = []

    def getGenre(self):
        return sources().getLiveGenre()

    def get(self, url=None):
        try :

            if url == None:
                self.list = self.getGenre()
            else :
                name=None
                title=None
                year=None
                imdb=None
                tvdb=None
                season=None
                episode=None
                tvshowtitle=None
                date=None
                meta={'genre':url}

                sourceList = sources().getSources(name, title, year, imdb, tvdb, season, episode, tvshowtitle, date, meta)

                sourceList = dict((item['name'],item) for item in sourceList).values()

                self.list.extend(sourceList)
                self.list = sorted(self.list, key=lambda k: k['name'])

                if not url == None :
                    self.channelDirectory(self.list)
                else:
                    self.channelDirectory(self.list, action='desiLiveNavigator')
        except Exception as e:
            logger.error(e, __name__)
            pass

    def channelDirectory(self, items, action='play'):
        if items == None or len(items) == 0: return

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart = control.addonFanart()
        artPath = control.logoPath()

        for i in items:
            try:
                label = "%s" % (i['name'])
                sysname = urllib.quote_plus(i['name'])

                meta = json.loads(i['meta'])
                poster, banner, direct = meta['poster'], meta['poster'], i['direct']
                try :provider=i['provider']
                except:provider=None

                if poster.startswith('http'):
                    pass
                elif not artPath == None and not poster == "": poster = os.path.join(artPath, poster)
                else: poster = addonPoster

                url = i['url']
                if not direct:
                    content = 'live'
                    meta = {"poster":poster, "iconImage":poster}
                    source = {"provider":provider,
                              "url":url,
                              "quality":'HD',
                              "label":'Resolving %s' % label,
                              "source":provider, "meta":json.dumps(meta)}
                    syssource = urllib.quote_plus(json.dumps([source]))

                    url = 'action=%s&content=%s&name=%s' % (action, content, sysname)
                    url = '%s?%s' % (sysaddon, url)

                item = control.item(label=label, iconImage=poster, thumbnailImage=poster)

                try: item.setArt({'poster': poster, 'banner': banner})
                except: pass

                if not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)

                item.setProperty('Video', 'true')
                item.setProperty("IsPlayable", "true")
                item.addContextMenuItems([])
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=False)
            except Exception as e:
                logger.error(e, __name__)
                pass

        #control.content(syshandle, 'video')
        #viewMode = 'list'
        #views.setView('movies', {'skin.confluence': control.viewMode['confluence'][viewMode], 'skin.estuary':
        #    control.viewMode['esturary'][viewMode]})
        control.directory(syshandle, cacheToDisc=False)

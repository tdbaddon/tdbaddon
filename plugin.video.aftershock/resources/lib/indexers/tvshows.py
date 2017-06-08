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

import base64
import datetime
import json
import os
import re
import sys
import urllib
import urlparse

try: action = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))['action']
except: action = None


from ashock.modules import control
from ashock.modules import cleantitle
from ashock.modules import client
from ashock.modules import cache
from ashock.modules import metacache
from ashock.modules import workers
from ashock.modules import views
from ashock.modules import logger

sysaddon = sys.argv[0] ; syshandle = int(sys.argv[1])

class tvshows:
    def __init__(self):
        self.list = []

        self.tmdb_key = base64.urlsafe_b64decode('MTdmMjI3YmVjNTdkOTQ4OGJiYzgyNzYyZmMxNDQ0NmM=')
        self.tvdb_key = base64.urlsafe_b64decode('OUZDQkM2MjlEQzgyRjA4Qw==')
        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        self.info_lang = control.setting('infoLang') or 'en'

        self.tvdb_info_link = 'http://thetvdb.com/api/%s/series/%s/%s.xml' % (self.tvdb_key, '%s', re.sub('bg', 'en', self.info_lang))
        self.tvdb_search_link = 'http://thetvdb.com/api/GetSeries.php?seriesname=%s'
        self.tvdb_by_imdb = 'http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=%s'
        self.imdb_by_query = 'http://www.omdbapi.com/?t=%s&y=%s'
        self.imdb_by_title = 'http://www.omdbapi.com/?t=%s'
        self.tvdb_image = 'http://thetvdb.com/banners/'

        self.burp_search_link = 'http://tv.burrp.com/search.html?q=%s'

    def get(self, url, idx=True, provider=None,network=None):
        try:
            self.list = cache.get(self.shows, 168, url, provider, network, table='rel_shows')
            self.list = sorted(self.list, key=lambda k: k['name'])
            if idx == True: self.tvshowDirectory(self.list)
            return self.list
        except Exception as e:
            logger.error(e, __name__)
            pass

    def shows(self, url, provider=None, network=None):
        try:

            # change the implementation to get shows from all providers as save to DB
            if not provider == None:
                call = __import__('resources.lib.sources.%s' % provider, globals(), locals(), ['source'], -1).source()
                self.list = call.tvshows(network, url)
                self.worker()
            return self.list
        except Exception as e:
            logger.error(e, __name__)
            pass

    def worker(self):
        self.meta = []
        total = len(self.list)

        for i in range(0, total): self.list[i].update({'metacache': False})
        self.list = metacache.fetch(self.list, self.info_lang)

        for r in range(0, total, 25):
            threads = []
            for i in range(r, r+25):
                if i < total: threads.append(workers.Thread(self.super_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

        if len(self.meta) > 0: metacache.insert(self.meta)

    def super_info(self, i):
        try :
            if self.list[i]['metacache'] == True: raise Exception()
            try: imdb = self.list[i]['imdb']
            except: imdb = '0'
            try: tvdb = self.list[i]['tvdb']
            except: tvdb = '0'

            self.list[i].update({"imdb":imdb, "tvdb":tvdb})

            title = self.list[i]['title']
            if 'season' in title.lower():
                title = title[:title.index('Season')-1]
            else:
                # strip end #'s
                title = title.replace(' 10', '')

            url = self.burp_search_link % urllib.quote_plus(title)

            result = client.request(url)
            result = result.decode('iso-8859-1').encode('utf-8')

            result = result.replace('\n','').replace('\t','')

            result = client.parseDOM(result, name="table", attrs={"class": "result"})[0]

            result = client.parseDOM(result, name="td", attrs={"class": "resultTitle"})
            showUrl = None
            for item in result:
                showTitle = client.parseDOM(item, name="a", attrs={"class": "title"})[0]
                showTitle = client.parseDOM(showTitle, name="strong")[0]
                if cleantitle.tv(showTitle) == cleantitle.tv(title):
                    showUrl = client.parseDOM(item, name="a", attrs={"class": "title"}, ret="href")[0]
                if showUrl != None:
                    break
            if showUrl == None:
                raise Exception()
            result = client.request(showUrl)

            if 'No information available!' in result:
                raise Exception()

            result = result.decode('iso-8859-1').encode('utf-8')
            #result = result.replace('\n','').replace('\t','')

            right = client.parseDOM(result, "div", attrs={"class": "Right"})[0]
            showDetails = client.parseDOM(result, "td", attrs={"class": "showDetails"})[0]
            try:
                genre = client.parseDOM(showDetails, "tr")
                for item in genre:
                    if "genre" in item.lower():
                        genre = client.parseDOM(item, "td")[0]
                        genre = genre.replace(',', ' / ').strip()
                    elif "show type" in item.lower():
                        genre = client.parseDOM(item, "td")[0]
                        genre = genre.replace(',', ' / ').strip()
            except Exception as e:
                logger.error(e)
                genre = ''

            if genre == '': genre = '0'
            genre = client.replaceHTMLCodes(genre)
            genre = genre.encode('utf-8')
            if not genre == '0': self.list[i].update({'genre': genre})

            try :
                poster = client.parseDOM(result, "td", attrs={"class": "showPics"})[0]
                poster = client.parseDOM(poster, "img", ret="src")[0]
            except:
                poster = ''

            if poster == '' or poster == None: poster = '0'
            poster = client.replaceHTMLCodes(poster)
            poster = poster.encode('utf-8')
            if not poster == '0': self.list[i].update({'poster': poster})

            try:
                plot = client.parseDOM(right, "div", attrs={"class": "synopsis"})[0].strip()
                try :
                    plot += client.parseDOM(right, "span", attrs={"id": "morecontent"})[0].strip()
                except:pass
            except: plot = ''
            if plot == '': plot = '0'
            plot = client.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')
            if not plot == '0': self.list[i].update({'plot': plot})

            try : metaHTML = client.parseDOM(right, "table", attrs={"class": "meta"})[0]
            except : metaHTML = None

            if metaHTML:
                items = client.parseDOM(metaHTML, "tr")
                premiered = cast = None
                for item in items :
                    if "release date" in item.lower():
                        premiered = client.parseDOM(item, "span", attrs={"itemprop": "name"})[0]
                        premiered = premiered.encode('utf-8')
                    elif "Actor" in item:
                        cast = client.parseDOM(item, "span", attrs={"itemprop": "name"})[0]
                        cast = cast.split(',')

                if premiered != None:
                    try: year = re.compile('(\d{4})').findall(premiered)[0]
                    except: year = ''
                    if year == '': year = '0'
                    year = year.encode('utf-8')
                    self.list[i].update({'year': year})
                    self.list[i].update({'premiered': premiered})
                if cast != None and len(cast) > 0: self.list[i].update({'cast': cast})

            imdb = cleantitle.tv(title)
            tvdb = banner = fanart = studio = duration = rating = votes = mpaa = '0'
            self.meta.append({'year': year, 'imdb': imdb, 'tvdb': tvdb, 'lang': self.info_lang, 'item': {'code': imdb, 'imdb': imdb, 'tvdb': tvdb, 'poster': poster, 'banner': banner, 'fanart': fanart, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'cast': cast, 'plot': plot}})
        except Exception as e:
            logger.error(e, __name__)
            pass

    def tvshowDirectory(self, items, confViewMode='list', estViewMode='widelist'):
        if items == None or len(items) == 0: return

        isFolder = True if control.setting('host_select') == '1' else False

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')

        for i in items:
            try:
                label = i['name']
                systitle = sysname = urllib.quote_plus(i['title'])
                sysimage = urllib.quote_plus(i['poster'])
                imdb, tvdb, year = i['imdb'], i['tvdb'], i['year']
                try :sysurl, sysprovider = urllib.quote_plus(i['url']), i['provider']
                except:pass

                poster, banner, fanart = i['poster'], i['banner'], i['fanart']
                if poster == '0': poster = addonPoster
                if banner == '0' and poster == '0': banner = addonBanner
                elif banner == '0': banner = poster

                meta = dict((k,v) for k, v in i.iteritems() if not v == '0')
                meta.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, sysname)})
                if i['duration'] == '0': meta.update({'duration': '60'})
                try: meta.update({'duration': str(int(meta['duration']) * 60)})
                except: pass
                sysmeta = urllib.quote_plus(json.dumps(meta))

                action = 'episodes'
                url = '%s?action=%s&provider=%s&url=%s&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s' % (sysaddon, action, sysprovider, sysurl, systitle, year, imdb, tvdb)

                cm = []

                if isFolder == False:
                    cm.append((control.lang(30232).encode('utf-8'), 'RunPlugin(%s?action=queueItem)' % sysaddon))

                cm.append((control.lang(30233).encode('utf-8'), 'Action(Info)'))

                cm.append((control.lang(30234).encode('utf-8'), 'RunPlugin(%s?action=tvPlaycount&name=%s&year=%s&imdb=%s&tvdb=%s&query=7)' % (sysaddon, systitle, year, imdb, tvdb)))
                cm.append((control.lang(30235).encode('utf-8'), 'RunPlugin(%s?action=tvPlaycount&name=%s&year=%s&imdb=%s&tvdb=%s&query=6)' % (sysaddon, systitle, year, imdb, tvdb)))

                cm.append((control.lang(30240).encode('utf-8'), 'RunPlugin(%s?action=addView&content=tvshows)' % sysaddon))

                item = control.item(label=label, iconImage=poster, thumbnailImage=poster)

                logger.debug('poster %s banner %s fanart %s' % (poster, banner, fanart))

                try: item.setArt({'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})
                except: pass

                if settingFanart == 'true' and not fanart == '0':
                    item.setProperty('Fanart_Image', fanart)
                elif not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)

                item.setInfo(type='Video', infoLabels = meta)
                item.setProperty('Video', 'true')
                item.addContextMenuItems(cm)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except Exception as e:
                logger.error(e, __name__)
                pass

        content = 'tvshows'
        control.content(syshandle, content)
        control.directory(syshandle, cacheToDisc=True)
        views.setView(content, {'skin.confluence': control.viewMode['confluence'][confViewMode], 'skin.estuary':
            control.viewMode['esturary'][estViewMode]})

    def getTVShowPosterFromGoogle(self, showName, retry):
        if retry == 0:
            return ''
        #baseURL = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q={query}'

        keyBing = 'btcCcvQ4Sfo9P2Q7u62eOREA1NfLEQPezqCNb+2LVhY'        # get Bing key from: https://datamarket.azure.com/account/keys
        credentialBing = 'Basic ' + (':%s' % keyBing).encode('base64')[:-1] # the "-1" is to remove the trailing "\n" which encode adds

        headers = {}
        headers['Authorization'] = credentialBing

        baseURL = 'https://api.datamarket.azure.com/Bing/Search/v1/Image?Query=%27{query}%27&$format=json'

        query = showName.lower() + ' poster'
        url = baseURL.format(query=urllib.quote_plus(query))
        try:
            result = client.request(url, headers=headers)

            results = json.loads(result)['d']['results']

            for image_info in results:
                iconImage = image_info['MediaUrl']
                break
            if iconImage is not None:
                return iconImage
            else:
                return '0'
        except :
            return self.getTVShowPosterFromGoogle(showName, retry-1)
        return ''

    def addDirectory(self, items):
        if items == None or len(items) == 0: return

        addonFanart = control.addonFanart()
        addonThumb = control.addonThumb()
        artPath = control.artPath()

        for i in items:
            try:
                try: name = control.lang(i['name']).encode('utf-8')
                except: name = i['name']

                if i['image'].startswith('http://'): thumb = i['image']
                elif not artPath == None: thumb = os.path.join(artPath, i['image'])
                else: thumb = addonThumb

                url = '%s?action=%s' % (sysaddon, i['action'])
                try: url += '&url=%s' % urllib.quote_plus(i['url'])
                except: pass

                cm = []

                item = control.item(label=name, iconImage=thumb, thumbnailImage=thumb)
                item.addContextMenuItems(cm)
                if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except Exception as e:
                logger.error(e, __name__)
                pass

        viewMode = 'mediainfo1'
        views.setView('tvshows', {'skin.confluence': control.viewMode['confluence'][viewMode], 'skin.estuary':
            control.viewMode['esturary'][viewMode]})
        control.directory(syshandle, cacheToDisc=True)
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


import sys,pkgutil,re,json,urllib,urlparse,datetime,time, random

try: import xbmc
except: pass

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

from resources.lib.libraries import control
from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import workers
from resources.lib.libraries import debrid
from resources.lib.libraries import alterepisode
from resources.lib.libraries import cache
from resources.lib import resolvers
from resources.lib.libraries import logger

class sources:
    def __init__(self):
        self.resolverList = self.getResolverList()
        self.hostDict = self.getHostDict()
        self.sources = []
        self.debridDict = debrid.debridDict()
        self.itemProperty = "%s.itemProperty" % control.addonInfo('name')
        self.metaProperty = "%s.itemMeta" % control.addonInfo('name')

    def addItem(self, title, content):
        try:
            control.playlist.clear()

            items = control.window.getProperty(self.itemProperty)
            items = json.loads(items)

            if items == []: raise Exception()

            meta = control.window.getProperty(self.metaProperty)
            meta = json.loads(meta)

            infoMenu = control.lang(30502).encode('utf-8')

            downloads = True if control.setting('downloads') == 'true' and not control.setting('movie.download.path') == '' else False
            sysaddon = sys.argv[0]
            syshandle = int(sys.argv[1])

            if 'tvshowtitle' in meta and 'season' in meta and 'episode' in meta:
                name = '%s S%02dE%02d' % (title, int(meta['season']), int(meta['episode']))
            elif 'year' in meta:
                name = '%s (%s)' % (title, meta['year'])
            else:
                name = title

            systitle = urllib.quote_plus(title.encode('utf-8'))

            sysname = urllib.quote_plus(name.encode('utf-8'))

            poster = meta['poster'] if 'poster' in meta else '0'
            banner = meta['banner'] if 'banner' in meta else '0'
            thumb = meta['thumb'] if 'thumb' in meta else poster
            fanart = meta['fanart'] if 'fanart' in meta else '0'

            if poster == '0': poster = control.addonPoster()
            if banner == '0' and poster == '0': banner = control.addonBanner()
            elif banner == '0': banner = poster
            if thumb == '0' and fanart == '0': thumb = control.addonFanart()
            elif thumb == '0': thumb = fanart
            if control.setting('fanart') == 'true' and not fanart == '0': pass
            else: fanart = control.addonFanart()

            sysimage = urllib.quote_plus(poster.encode('utf-8'))

            for i in range(len(items)):
                try :
                    parts = int(items[i]['parts'])
                    logger.debug('Download : %s, Parts : %s, Label : %s' % (downloads, parts, label), __name__)
                except:
                    parts = 1

                label = items[i]['label']

                syssource = urllib.quote_plus(json.dumps([items[i]]))

                sysurl = '%s?action=playItem&title=%s&source=%s&content=%s' % (sysaddon, systitle, syssource, content)

                item = control.item(label=label)

                cm = []
                cm.append((control.lang(30504).encode('utf-8'), 'RunPlugin(%s?action=queueItem)' % sysaddon))
                if (downloads == True and parts <= 1):
                    cm.append((control.lang(30505).encode('utf-8'), 'RunPlugin(%s?action=download&name=%s&image=%s&source=%s)' % (sysaddon, systitle, sysimage, syssource)))
                #cm.append((infoMenu, 'Action(Info)'))
                #cm.append((control.lang(30506).encode('utf-8'), 'RunPlugin(%s?action=refresh)' % sysaddon))
                #cm.append((control.lang(30507).encode('utf-8'), 'RunPlugin(%s?action=openSettings)' % sysaddon))
                #cm.append((control.lang(30508).encode('utf-8'), 'RunPlugin(%s?action=openPlaylist)' % sysaddon))
                item.setArt({'icon': thumb, 'thumb': thumb, 'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})

                if not fanart == None: item.setProperty('Fanart_Image', fanart)

                item.addContextMenuItems(cm)
                item.setInfo(type='Video', infoLabels = meta)

                control.addItem(handle=syshandle, url=sysurl, listitem=item, isFolder=False)

            control.directory(int(sys.argv[1]), cacheToDisc=True)
        except Exception as e:
            logger.error(e.message)
            control.infoDialog(control.lang(30501).encode('utf-8'))

    def play(self, name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta, url, select=None):
        try:
            if not control.infoLabel('Container.FolderPath').startswith('plugin://'):
                control.playlist.clear()

            control.resolve(int(sys.argv[1]), True, control.item(path=''))
            control.execute('Dialog.Close(okdialog)')

            if imdb == '0': imdb = '0000000'
            imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))

            if title == None and tvshowtitle == None :
                content = 'live'
            else :
                content = 'movie' if tvshowtitle == None else 'episode'

            self.sources = self.getSources(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta)

            select = control.setting('host_select') if select == None else select

            try :
                if content == 'live':
                    select = '2'
                    title = name
                    meta = self.sources[0]['meta']
                    logger.debug('Content is live hence setting Auto-Play')
            except Exception as e:
                logger.error(e.message)
                pass

            items = self.sourcesFilter()
            if len(items) > 0:

                if select == '1' and 'plugin' in control.infoLabel('Container.PluginName'):
                    control.window.clearProperty(self.itemProperty)
                    control.window.setProperty(self.itemProperty, json.dumps(items))

                    control.window.clearProperty(self.metaProperty)
                    control.window.setProperty(self.metaProperty, meta)

                    control.sleep(200)

                    return control.execute('Container.Update(%s?action=addItem&title=%s&content=%s)' % (sys.argv[0], urllib.quote_plus(title.encode('utf-8')), content))

                elif select == '0' or select == '1':
                    url = self.sourcesDialog(items)

                else:
                    url = self.sourcesDirect(items)

            if url == None: raise Exception()
            if url == 'close://': return

            if control.setting('playback_info') == 'true':
                control.infoDialog(self.selectedSource, heading=name)

            control.sleep(200)

            from resources.lib.libraries.player import player
            player().run(content, name, url, year, imdb, tvdb, meta)

            return url
        except Exception as e:
            logger.error(e.message)
            control.infoDialog(control.lang(30501).encode('utf-8'))

    def playItem(self, content, title, source):
        try:
            control.resolve(int(sys.argv[1]), True, control.item(path=''))
            control.execute('Dialog.Close(okdialog)')

            next = [] ; prev = [] ; total = []
            meta = control.window.getProperty(self.metaProperty)
            meta = json.loads(meta)

            year = meta['year'] if 'year' in meta else None
            imdb = meta['imdb'] if 'imdb' in meta else None
            tvdb = meta['tvdb'] if 'tvdb' in meta else None


            for i in range(1,10000):
                try:
                    u = control.infoLabel('ListItem(%s).FolderPath' % str(i))

                    if u in total: raise Exception()
                    total.append(u)
                    u = dict(urlparse.parse_qsl(u.replace('?','')))
                    if 'meta' in u: meta = u['meta']
                    u = json.loads(u['source'])[0]
                    next.append(u)
                except:
                    break
            for i in range(-10000,0)[::-1]:
                try:
                    u = control.infoLabel('ListItem(%s).FolderPath' % str(i))
                    if u in total: raise Exception()
                    total.append(u)
                    u = dict(urlparse.parse_qsl(u.replace('?','')))
                    if 'meta' in u: meta = u['meta']
                    u = json.loads(u['source'])[0]
                    prev.append(u)
                except:
                    break

            items = json.loads(source)
            items = [i for i in items+next+prev][:40]

            self.progressDialog = control.progressDialog
            self.progressDialog.create(control.addonInfo('name'), '')
            self.progressDialog.update(0)

            block = None

            for i in range(len(items)):
                try:
                    self.progressDialog.update(int((100 / float(len(items))) * i), str(items[i]['label']), str(' '))

                    if items[i]['source'] == block: raise Exception()

                    w = workers.Thread(self.sourcesResolve, items[i])
                    w.start()

                    m = ''

                    for x in range(3600):
                        if self.progressDialog.iscanceled(): return self.progressDialog.close()
                        if xbmc.abortRequested == True: return sys.exit()
                        k = control.condVisibility('Window.IsActive(virtualkeyboard)')
                        if k: m += '1'; m = m[-1]
                        if (w.is_alive() == False or x > 30) and not k: break
                        time.sleep(1.0)

                    for x in range(3600):
                        if m == '': break
                        if self.progressDialog.iscanceled(): return self.progressDialog.close()
                        if xbmc.abortRequested == True: return sys.exit()
                        if w.is_alive() == False: break
                        time.sleep(1.0)


                    if w.is_alive() == True: block = items[i]['source']

                    if self.url == None: raise Exception()

                    try: self.progressDialog.close()
                    except: pass

                    control.sleep(200)

                    if control.setting('playback_info') == 'true':
                        control.infoDialog(items[i]['label'])

                    from resources.lib.libraries.player import player
                    player().run(content, title, self.url, year, imdb, tvdb, meta)

                    return self.url
                except:
                    client.printException('')
                    pass

            try: self.progressDialog.close()
            except: pass

            raise Exception()

        except Exception as e:
            logger.error(e.message)
            control.infoDialog(control.lang(30501).encode('utf-8'))
            pass

    def getSources(self, name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta=None):
        sourceDict = []
        channelName = name
        for package, name, is_pkg in pkgutil.walk_packages(__path__): sourceDict.append((name, is_pkg))
        sourceDict = [i[0] for i in sourceDict if i[1] == False]

        if tvshowtitle == None and title == None:
            content = 'live'
        else:
            content = 'movie' if tvshowtitle == None else 'episode'

        if content == 'movie':
            sourceDict = [i for i in sourceDict if i.endswith(('_mv', '_mv_tv'))]
            try: sourceDict = [(i, control.setting(re.sub('_mv_tv$|_mv$|_tv$', '', i))) for i in sourceDict]
            except: sourceDict = [(i, 'true') for i in sourceDict]
        elif content == 'episode':
            sourceDict = [i for i in sourceDict if i.endswith(('_tv', '_mv_tv'))]
            try: sourceDict = [(i, control.setting(re.sub('_mv_tv$|_mv$|_tv$', '', i))) for i in sourceDict]
            except: sourceDict = [(i, 'true') for i in sourceDict]
        elif content == 'live':
            sourceDict = [i for i in sourceDict if i.endswith('_live')]
            try: sourceDict = [(i, control.setting(re.sub('_live$', '', i))) for i in sourceDict]
            except: sourceDict = [(i, 'true') for i in sourceDict]

        threads = []

        control.makeFile(control.dataPath)
        self.sourceFile = control.sourcescacheFile

        sourceDict = [i[0] for i in sourceDict if i[1] == 'true']

        logger.debug('Content [%s] Source Dict : %s' % (content, sourceDict), __name__)

        if content == 'movie':
            title = cleantitle.normalize(title)
            for source in sourceDict: threads.append(workers.Thread(self.getMovieSource, title, year, imdb, re.sub('_mv_tv$|_mv$|_tv$', '', source), __import__(source, globals(), locals(), [], -1).source()))
        elif content == 'episode':
            tvshowtitle = cleantitle.normalize(tvshowtitle)
            season, episode = alterepisode.alterepisode().get(imdb, tmdb, tvdb, tvrage, season, episode, alter, title, date)

            for source in sourceDict: threads.append(workers.Thread(self.getEpisodeSource, title, year, imdb, tvdb, season, episode, tvshowtitle, date, re.sub('_mv_tv$|_mv$|_tv$', '', source), __import__(source, globals(), locals(), [], -1).source(), meta))
        elif content == 'live':
            for source in sourceDict:threads.append(workers.Thread(self.getLiveSource,channelName, re.sub('_live$', '', source), __import__(source, globals(), locals(), [], -1).source()))


        try: timeout = int(control.setting('sources_timeout_40'))
        except: timeout = 40

        [i.start() for i in threads]

        control.idle()

        sourceLabel = [re.sub('_mv_tv$|_mv$|_tv$|_live$', '', i) for i in sourceDict]
        sourceLabel = [re.sub('v\d+$', '', i).upper() for i in sourceLabel]


        self.progressDialog = control.progressDialog
        self.progressDialog.create(control.addonInfo('name'), '')
        self.progressDialog.update(0)

        string1 = control.lang(30512).encode('utf-8')
        string2 = control.lang(30513).encode('utf-8')
        string3 = control.lang(30514).encode('utf-8')

        for i in range(0, timeout * 2):
            try:
                if xbmc.abortRequested == True: return sys.exit()

                try: info = [sourceLabel[int(re.sub('[^0-9]', '', str(x.getName()))) - 1] for x in threads if x.is_alive() == True]
                except: info = []

                if len(info) > 5: info = len(info)

                self.progressDialog.update(int((100 / float(len(threads))) * len([x for x in threads if x.is_alive() == False])), str('%s: %s %s' % (string1, int(i * 0.5), string2)), str('%s: %s' % (string3, str(info).translate(None, "[]'"))))

                if self.progressDialog.iscanceled(): break

                is_alive = [x.is_alive() for x in threads]
                if all(x == False for x in is_alive): break
                time.sleep(0.5)
            except:
                pass

        self.progressDialog.close()

        for i in range(0, len(self.sources)): self.sources[i].update({'content': content})

        return self.sources

    def getMovieSource(self, title, year, imdb, source, call):
        try:
            dbcon = database.connect(self.sourceFile)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS rel_url (""source TEXT, ""imdb_id TEXT, ""season TEXT, ""episode TEXT, ""rel_url TEXT, ""UNIQUE(source, imdb_id, season, episode)"");")
            dbcur.execute("CREATE TABLE IF NOT EXISTS rel_src (""source TEXT, ""imdb_id TEXT, ""season TEXT, ""episode TEXT, ""hosts TEXT, ""added TEXT, ""UNIQUE(source, imdb_id, season, episode)"");")
        except:
            pass

        try:
            sources = []
            dbcur.execute("SELECT * FROM rel_src WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, '', ''))
            match = dbcur.fetchone()
            t1 = int(re.sub('[^0-9]', '', str(match[5])))
            t2 = int(datetime.datetime.now().strftime("%Y%m%d%H%M"))
            update = abs(t2 - t1) > 60
            if update == False:
                sources = json.loads(match[4])
                return self.sources.extend(sources)
        except:
            pass

        try:
            url = None
            dbcur.execute("SELECT * FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, '', ''))
            url = dbcur.fetchone()
            url = url[4]
        except:
            pass

        try:
            if url == None: url = call.get_movie(imdb, title, year)
            if url == None: raise Exception()
            dbcur.execute("DELETE FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, '', ''))
            dbcur.execute("INSERT INTO rel_url Values (?, ?, ?, ?, ?)", (source, imdb, '', '', url))
            dbcon.commit()
        except:
            pass

        try:
            sources = []
            sources = call.get_sources(url)
            if sources == None:
                raise Exception()
                sources = []
            self.sources.extend(sources)
            dbcur.execute("DELETE FROM rel_src WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, '', ''))
            dbcur.execute("INSERT INTO rel_src Values (?, ?, ?, ?, ?, ?)", (source, imdb, '', '', json.dumps(sources), datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
            dbcon.commit()
        except Exception as e:
            logger.error(e)
            import traceback
            pass

    def getEpisodeSource(self, title, year, imdb, tvdb, season, episode, tvshowtitle, date, source, call, meta=None):
        meta = json.loads(meta)

        try :
            if season == '0' and episode == '0':
                imdb = meta['tvshowtitle']
                episode = meta['title']
            try:
                dbcon = database.connect(self.sourceFile)
                dbcur = dbcon.cursor()
                dbcur.execute("CREATE TABLE IF NOT EXISTS rel_url (""source TEXT, ""imdb_id TEXT, ""season TEXT, ""episode TEXT, ""rel_url TEXT, ""UNIQUE(source, imdb_id, season, episode)"");")
                dbcur.execute("CREATE TABLE IF NOT EXISTS rel_src (""source TEXT, ""imdb_id TEXT, ""season TEXT, ""episode TEXT, ""hosts TEXT, ""added TEXT, ""UNIQUE(source, imdb_id, season, episode)"");")
            except:
                pass

            try:
                sources = []
                dbcur.execute("SELECT * FROM rel_src WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, season, episode))
                match = dbcur.fetchone()
                t1 = int(re.sub('[^0-9]', '', str(match[5])))
                t2 = int(datetime.datetime.now().strftime("%Y%m%d%H%M"))
                update = abs(t2 - t1) > 60
                if update == False:
                    sources = json.loads(match[4])
                    return self.sources.extend(sources)
            except:
                pass

            try:
                url = None
                dbcur.execute("SELECT * FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, '', ''))
                url = dbcur.fetchone()
                url = url[4]
            except:
                pass

            try:
                if url == None:
                    tvshowurl = meta['tvshowurl']
                    url = call.get_show(tvshowurl, imdb, tvdb, tvshowtitle, year)
                if url == None: raise Exception()
                dbcur.execute("DELETE FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, '', ''))
                dbcur.execute("INSERT INTO rel_url Values (?, ?, ?, ?, ?)", (source, imdb, '', '', url))
                dbcon.commit()
            except:
                pass

            try:
                ep_url = None
                dbcur.execute("SELECT * FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, season, episode))
                ep_url = dbcur.fetchone()
                ep_url = ep_url[4]
            except:
                pass


            try:
                if url == None: raise Exception()
                if ep_url == None:
                    ep_url = call.get_episode(url, meta['url'], imdb, tvdb, title, date, season, episode)
                if ep_url == None: raise Exception()
                dbcur.execute("DELETE FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, season, episode))
                dbcur.execute("INSERT INTO rel_url Values (?, ?, ?, ?, ?)", (source, imdb, season, episode, ep_url))
                dbcon.commit()
            except:
                pass

            try:
                sources = []
                sources = call.get_sources(ep_url)
                if sources == None: sources = []
                self.sources.extend(sources)
                dbcur.execute("DELETE FROM rel_src WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, season, episode))
                dbcur.execute("INSERT INTO rel_src Values (?, ?, ?, ?, ?, ?)", (source, imdb, season, episode, json.dumps(sources), datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
                dbcon.commit()
            except:
                pass
        except:
            client.printException('sources.getEpisodeSource')
            pass


    def getLiveSource(self, name, source, call):
        try:
            dbcon = database.connect(self.sourceFile)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS rel_live (""source TEXT, ""imdb_id TEXT, ""season TEXT, ""episode TEXT, ""hosts TEXT, ""added TEXT, ""UNIQUE(source, imdb_id, season, episode, hosts)"");")
        except:
            pass

        retValue, sources = call.getLiveSource()

        if retValue == 1:
            try:
                logger.debug('Updated file download from internet', __name__)
                dbcur.execute("DELETE FROM rel_live WHERE source = '%s' AND season = '%s'" % (source, 'live'))
                dbcon.commit()

                idx = 0
                for item in sources:
                    item['name'] = cleantitle.live(item['name'])
                    poster = self.getLivePoster(item['name'])
                    if not poster == None :
                        item['poster'] = poster

                    dbcur.execute("INSERT INTO rel_live Values (?, ?, ?, ?, ?, ?)", (source, item['name'], 'live', str(idx), json.dumps(item), datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
                    idx = idx + 1
                    dbcon.commit()
            except Exception as e:
                logger.error(e.message)
                pass
        elif retValue == 0:
            try:
                sources = []
                dbcur.execute("SELECT * FROM rel_live WHERE source = '%s' AND imdb_id = '%s' AND season = '%s'" % (source, name, 'live'))
                for row in dbcur:
                    match = row
                    logger.debug('Fetched sources from cache for [%s]'% name, call.__class__)
                    sources = json.loads(match[4])
                    sources['content'] = 'live'
                    poster = sources['poster']
                    meta = {"poster":poster, "iconImage":poster, 'thumb': poster}
                    sources['meta'] = json.dumps(meta)
                    self.sources.append(sources)
                    return self.sources
            except:
                logger.debug('Source from cache not found for [%s]'% name, call.__class__)
                pass

        try:
            sources = []
            if name == None or name == '' :
                dbcur.execute("SELECT * FROM rel_live WHERE source = '%s' AND season = '%s'" % (source, 'live'))
                for row in dbcur:
                    match = row[4]
                    self.sources.append(json.loads(match))
                logger.debug('Fetched Live sources : %s' % len(self.sources), call.__class__)
            else :
                dbcur.execute("SELECT * FROM rel_live WHERE source = '%s' AND imdb_id = '%s' AND season = '%s'" % (source, name, 'live'))
                for row in dbcur:
                    match = row
                    sources = json.loads(match[4])
                    sources['content'] = 'live'
                    self.sources.append(sources)
            return self.sources
        except Exception as e:
            logger.error('(%s) Exception Live sources : %s' % (call.__class__, e.args))
            pass
    def getLivePoster(self, source):
        try:
            dbcon = database.connect(self.sourceFile)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS rel_logo (""source TEXT, ""poster_url TEXT, ""added TEXT, ""UNIQUE(source, poster_url)"");")
        except:
            pass

        try:
            logo = []
            try:
                # check if the source site needs to be refreshed
                dbcur.execute("SELECT * FROM rel_logo WHERE source = '%s'" % (source))
                match = dbcur.fetchone()
                poster_url = match[1]
                t1 = int(re.sub('[^0-9]', '', str(match[2])))
                t2 = int(datetime.datetime.now().strftime("%Y%m%d%H%M"))
                update = abs(t2 - t1) > 1000
            except:
                update = True

            if update == True:
                from resources.lib.sources import live_logo

                postersList = cache.get(live_logo.source().getLivePosters, 200)
                try :
                    poster_url = postersList[source]
                except:
                    poster_url = None
                if not poster_url == None:
                    try :
                        dbcur.execute("DELETE FROM rel_logo WHERE source = '%s'" % (source))
                        dbcur.execute("INSERT INTO rel_logo Values (?, ?, ?)", (source, poster_url, datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
                        dbcon.commit()
                    except:
                        pass

            return poster_url

        except:
            pass

    def sourcesDialog(self, items):
        try:

            labels = [i['label'] for i in items]

            select = control.selectDialog(labels)
            if select == -1: return 'close://'

            next = [y for x,y in enumerate(items) if x >= select]
            prev = [y for x,y in enumerate(items) if x < select][::-1]

            items = [items[select]]
            items = [i for i in items+next+prev][:40]

            header = control.addonInfo('name')
            header2 = header.upper()

            progressDialog = control.progressDialog
            progressDialog.create(control.addonInfo('name'), '')
            progressDialog.update(0)

            block = None

            for i in range(len(items)):
                try:
                    if items[i]['source'] == block: raise Exception()

                    w = workers.Thread(self.sourcesResolve, items[i])
                    w.start()

                    try:
                        if progressDialog.iscanceled(): break
                        progressDialog.update(int((100 / float(len(items))) * i), str(items[i]['label']), str(' '))
                    except:
                        progressDialog.update(int((100 / float(len(items))) * i), str(header2), str(items[i]['label']))

                    m = ''

                    for x in range(3600):
                        try:
                            if xbmc.abortRequested == True: return sys.exit()
                            if progressDialog.iscanceled(): return progressDialog.close()
                        except:
                            pass

                        k = control.condVisibility('Window.IsActive(virtualkeyboard)')
                        if k: m += '1'; m = m[-1]
                        if (w.is_alive() == False or x > 30) and not k: break
                        k = control.condVisibility('Window.IsActive(yesnoDialog)')
                        if k: m += '1'; m = m[-1]
                        if (w.is_alive() == False or x > 30) and not k: break
                        time.sleep(0.5)


                    for x in range(30):
                        try:
                            if xbmc.abortRequested == True: return sys.exit()
                            if progressDialog.iscanceled(): return progressDialog.close()
                        except:
                            pass

                        if m == '': break
                        if w.is_alive() == False: break
                        time.sleep(0.5)


                    if w.is_alive() == True: block = items[i]['source']

                    if self.url == None: raise Exception()

                    self.selectedSource = items[i]['label']

                    try: progressDialog.close()
                    except: pass

                    control.execute('Dialog.Close(virtualkeyboard)')
                    control.execute('Dialog.Close(yesnoDialog)')
                    return self.url
                except:
                    pass

            try: progressDialog.close()
            except: pass

        except Exception as e:
            logger.error(e.message)
            try: progressDialog.close()
            except: pass

    def sourcesDirect(self, items):

        u = None

        self.progressDialog = control.progressDialog
        self.progressDialog.create(control.addonInfo('name'), '')
        self.progressDialog.update(0)

        for i in range(len(items)):
            try:
                if self.progressDialog.iscanceled(): break

                self.progressDialog.update(int((100 / float(len(items))) * i), str(items[i]['label']), str(' '))

                if xbmc.abortRequested == True: return sys.exit()

                url = self.sourcesResolve(items[i])
                if url == None: raise Exception()
                if u == None: u = url

                self.selectedSource = items[i]['label']
                self.progressDialog.close()

                return url
            except:
                pass

        try: self.progressDialog.close()
        except: pass

        return u

    def alterSources(self, url, meta):
        try:
            if control.setting('host_select') == '2': url += '&select=1'
            else: url += '&select=2'
            control.execute('RunPlugin(%s)' % url)
        except:
            pass

    def sourcesFilter(self):
        logger.debug('Calling sources.filter()', __name__)
        for i in range(len(self.sources)): self.sources[i]['source'] = self.sources[i]['source'].lower()
        self.sources = sorted(self.sources, key=lambda k: k['source'])

        random.shuffle(self.sources)

        quality = control.setting('playback_quality')
        if quality == '': quality = '0'

        filter = []
        filter += [i for i in self.sources if i['direct'] == True]
        filter += [i for i in self.sources if i['direct'] == False]

        self.sources = filter

        filter = []
        for d in self.debridDict: filter += [dict(i.items() + [('debrid', d)]) for i in self.sources if i['source'].lower() in self.debridDict[d]]
        for host in self.hostDict : filter += [i for i in self.sources if i['direct'] == False and i['source'] in host and 'debridonly' not in i and not i['content'] == 'live']
        filter += [i for i in self.sources if i['direct'] == True and not i['content'] == 'live']
        try:filter += [i for i in self.sources if i['content'] == 'live']
        except:pass
        self.sources = filter

        filter = []
        if quality == '0': filter += [i for i in self.sources if i['quality'] == '1080p' and 'debrid' in i]
        if quality == '0': filter += [i for i in self.sources if i['quality'] == '1080p' and not 'debrid' in i]
        if quality == '0' or quality == '1': filter += [i for i in self.sources if i['quality'] == 'HD' and 'debrid' in i]
        if quality == '0' or quality == '1': filter += [i for i in self.sources if i['quality'] == 'HD' and not 'debrid' in i]
        filter += [i for i in self.sources if i['quality'] == 'SD' and not 'debrid' in i]
        if len(filter) < 25: filter += [i for i in self.sources if i['quality'] == 'SCR']
        if len(filter) < 25:filter += [i for i in self.sources if i['quality'] == 'CAM']
        if len(filter) < 25:filter += [i for i in self.sources if i['quality'] == '']
        self.sources = filter

        for i in range(len(self.sources)):

            s = self.sources[i]['source'].lower()
            p = self.sources[i]['provider']
            p = re.sub('v\d*$', '', p)

            q = self.sources[i]['quality']

            try: f = (' | '.join(['[I]%s [/I]' % info.strip() for info in self.sources[i]['info'].split('|')]))
            except: f = ''

            try: d = self.sources[i]['debrid']
            except: d = self.sources[i]['debrid'] = ''

            if not d == '': label = '%02d | [B]%s[/B] | ' % (int(i+1), d)
            else: label = '%02d | [B]%s[/B] | ' % (int(i+1), p)

            if q in ['1080p', 'HD']: label += '%s | %s | [B][I]%s [/I][/B]' % (s.rsplit('.', 1)[0], f, q)
            #elif q == 'SD': label += '%s | %s' % (s.rsplit('.', 1)[0], f)
            else: label += '%s | %s | [I]%s [/I]' % (s.rsplit('.', 1)[0], f, q)
            label = label.replace('| 0 |', '|').replace(' | [I]0 [/I]', '')
            label = label.replace('[I]HEVC [/I]', 'HEVC')
            label = re.sub('\[I\]\s+\[/I\]', ' ', label)
            label = re.sub('\|\s+\|', '|', label)
            label = re.sub('\|(?:\s+|)$', '', label)

            pts = None
            try : pts = self.sources[i]['parts']
            except:pass

            if not pts == None and int(pts) > 1:
                label += ' [%s]' % pts

            self.sources[i]['label'] = label.upper()
        return self.sources

    def sourcesResolve(self, item):
        try:
            logger.debug('selected url : %s' % item['url'])
            u = url = item['url']
            provider = item['provider'].lower()

            d = item['debrid'] ; direct = item['direct']

            if not provider.endswith(('_mv', '_tv', '_mv_tv')):
                sourceDict = []
                for package, name, is_pkg in pkgutil.walk_packages(__path__): sourceDict.append((name, is_pkg))
                provider = [i[0] for i in sourceDict if i[1] == False and i[0].startswith(provider + '_')][0]

            source = __import__(provider, globals(), locals(), [], -1).source()
            u = url = source.resolve(url, self.resolverList)
            if url == False: raise Exception()

            if not d == '':
                if type(url) is list:
                    url = []
                    for tUrl in url:
                        tUrl = debrid.resolver(url, d)
                        url.append(tUrl)
                else:
                    url = debrid.resolver(url, d)
            try :
                ext = url.split('?')[0].split('&')[0].split('|')[0].rsplit('.')[-1].replace('/', '').lower()
            except :
                ext = None
            if ext == 'rar': raise Exception()

            try: headers = url.rsplit('|', 1)[1]
            except: headers = ''
            headers = urllib.quote_plus(headers).replace('%3D', '=') if ' ' in headers else headers
            headers = dict(urlparse.parse_qsl(headers))

            if not type(url) is list:
                if url.startswith('http') and '.m3u8' in url:
                    result = client.request(url.split('|')[0], headers=headers, output='geturl', timeout='20')
                    if result == None: raise Exception()

                elif url.startswith('http'):
                    result = client.request(url.split('|')[0], headers=headers, output='chunk', timeout='20')
                    if result == None: raise Exception()
            self.url = url
            return url
        except Exception as e:
            logger.error(e.message)
            return

    def getResolverList(self):
        try:
            import urlresolver
            resolverList = []
            try: resolverList = urlresolver.relevant_resolvers(order_matters=True)
            except: resolverList = urlresolver.plugnplay.man.implementors(urlresolver.UrlResolver)
            resolverList = [i for i in resolverList if not '*' in i.domains]
        except:
            resolverList = []
        return resolverList

    def getHostDict(self):
        try:
            hostDict = [i.domains for i in self.resolverList]
            hostDict = [i.lower() for i in reduce(lambda x, y: x+y, hostDict)]
            hostDict = [x for y,x in enumerate(hostDict) if x not in hostDict[:y]]

            customHostDict = [x['host'] for x in resolvers.info()]
            customHostDict = [i.lower() for i in reduce(lambda x, y: x+y, customHostDict)]
            customHostDict = [x for y,x in enumerate(customHostDict) if x not in customHostDict[:y]]
            hostDict += customHostDict
            hostDict = list(set(hostDict))
        except:
            hostDict = []
        return hostDict

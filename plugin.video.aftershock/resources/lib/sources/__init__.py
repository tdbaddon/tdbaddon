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
from resources.lib.resolvers import realdebrid
from resources.lib.resolvers import premiumize
from resources.lib.libraries import alterepisode
from resources.lib import resolvers
from resources.lib.libraries import logger

class sources:
    def __init__(self):
        self.resolverList = self.getResolverList()
        self.hostDict = self.getHostDict()
        self.sources = []

    def addItem(self, name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta):
        try:
            if imdb == '0': imdb = '0000000'
            imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))

            content = 'movie' if tvshowtitle == None else 'episode'

            self.sources = self.getSources(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta)
            if self.sources == []: raise Exception()

            self.progressDialog = control.progressDialog
            self.progressDialog.create(control.addonInfo('name'), '')
            self.progressDialog.update(0, control.lang(30515).encode('utf-8'), str(' '))

            self.sources = self.sourcesFilter()
            if self.sources == []: raise Exception()

            infoMenu = control.lang(30502).encode('utf-8') if content == 'movie' else control.lang(30503).encode('utf-8')

            downloads = True if control.setting('downloads') == 'true' and not control.setting('movie.download.path') == '' else False

            logger.debug('Downloads : %s' % downloads)

            sysmeta = urllib.quote_plus(meta)
            sysaddon = sys.argv[0]

            meta = json.loads(meta)

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

            for i in range(len(self.sources)):
                try:
                    if self.progressDialog.iscanceled(): break

                    self.progressDialog.update(int((100 / float(len(self.sources))) * i))

                    url, label, provider = self.sources[i]['url'], self.sources[i]['label'], self.sources[i]['provider']

                    try :
                        parts = int(self.sources[i]['parts'])
                        logger.debug('Download : %s, Parts : %s, Label : %s' % (downloads, parts, label))
                    except:
                        parts = 2

                    logger.debug('Downloads : %s Parts : %s' % (downloads, parts))

                    systitle = urllib.quote_plus('%s (%s)' % (title, year) if tvshowtitle == None or season == None or episode == None else '%s S%02dE%02d' % (tvshowtitle, int(season), int(episode)))
                    sysname, sysurl, sysimage, sysprovider = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(poster), urllib.quote_plus(provider)

                    syssource = urllib.quote_plus(json.dumps([self.sources[i]]))

                    if i == 0:
                        query = 'action=playItem&content=%s&name=%s&year=%s&imdb=%s&tvdb=%s&source=%s&meta=%s' % (content, sysname, year, imdb, tvdb, syssource, sysmeta)
                    else:
                        query = 'action=playItem&content=%s&name=%s&year=%s&imdb=%s&tvdb=%s&source=%s' % (content, sysname, year, imdb, tvdb, syssource)

                    cm = []
                    cm.append((control.lang(30504).encode('utf-8'), 'RunPlugin(%s?action=queueItem)' % sysaddon))
                    if (downloads == True and parts <= 1):
                        cm.append((control.lang(30505).encode('utf-8'), 'RunPlugin(%s?action=download&name=%s&image=%s&source=%s)' % (sysaddon, systitle, sysimage, syssource)))
                    cm.append((infoMenu, 'Action(Info)'))
                    cm.append((control.lang(30506).encode('utf-8'), 'RunPlugin(%s?action=refresh)' % sysaddon))
                    cm.append((control.lang(30507).encode('utf-8'), 'RunPlugin(%s?action=openSettings)' % sysaddon))
                    cm.append((control.lang(30508).encode('utf-8'), 'RunPlugin(%s?action=openPlaylist)' % sysaddon))

                    item = control.item(label=label, iconImage='DefaultVideo.png', thumbnailImage=thumb)
                    try: item.setArt({'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})
                    except: pass
                    item.setInfo(type='Video', infoLabels = meta)
                    if not fanart == None: item.setProperty('Fanart_Image', fanart)
                    item.setProperty('Video', 'true')
                    #item.setProperty('IsPlayable', 'true')
                    item.addContextMenuItems(cm, replaceItems=True)
                    control.addItem(handle=int(sys.argv[1]), url='%s?%s' % (sysaddon, query), listitem=item, isFolder=False)
                except:
                    pass

            control.directory(int(sys.argv[1]), cacheToDisc=True)
            try: self.progressDialog.close()
            except: pass
        except:
            control.infoDialog(control.lang(30501).encode('utf-8'))
            try: self.progressDialog.close()
            except: pass

    def play(self, name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta, url):
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

            try :
                if content == 'live':
                    meta = self.sources[0]['meta']
            except:
                pass

            self.sources = self.sourcesFilter()

            if url == 'dialog://':
                url = self.sourcesDialog()

            elif url == 'direct://':
                url = self.sourcesDirect()

            elif not control.infoLabel('Container.FolderPath').startswith('plugin://') and control.setting('autoplay_library') == 'false':
                url = self.sourcesDialog()

            elif control.infoLabel('Container.FolderPath').startswith('plugin://') and control.setting('autoplay') == 'false':
                url = self.sourcesDialog()

            else:
                url = self.sourcesDirect()

            if url == None: raise Exception()
            if url == 'close://': return

            if control.setting('playback_info') == 'true':
                control.infoDialog(self.selectedSource, heading=name)

            control.sleep(200)

            from resources.lib.libraries.player import player
            player().run(content, name, url, year, imdb, tvdb, meta)

            return url
        except:
            control.infoDialog(control.lang(30501).encode('utf-8'))

    def playItem(self, content, name, year, imdb, tvdb, source):
        try:
            control.resolve(int(sys.argv[1]), True, control.item(path=''))
            control.execute('Dialog.Close(okdialog)')

            next = [] ; prev = [] ; total = []
            meta = None

            if content == 'live':
                items = json.loads(source)
                source, quality = items[0]['source'], items[0]['quality']
                meta = items[0]['meta']
            else :

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
                source, quality = items[0]['source'], items[0]['quality']
                items = [i for i in items+next+prev if i['quality'] == quality and i['source'] == source][:10]
                items += [i for i in next+prev if i['quality'] == quality and not i['source'] == source][:10]

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
                        control.infoDialog(items[i]['label'], heading=name)

                    from resources.lib.libraries.player import player
                    player().run(content, name, self.url, year, imdb, tvdb, meta)

                    return self.url
                except:
                    client.printException('')
                    pass

            try: self.progressDialog.close()
            except: pass

            raise Exception()

        except:
            control.infoDialog(control.lang(30501).encode('utf-8'))
            client.printException('sources.playItem(content=[%s], name=[%s], year=[%s], imdb=[%s], tvdb=[%s], source=[%s])' % (content, name, year, imdb, tvdb, source))
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
            #try: sourceDict = [(i, control.setting(re.sub('_mv_tv$|_mv$|_tv$', '', i) + '_tv')) for i in sourceDict]
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
        except:
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
            dbcur.execute("CREATE TABLE IF NOT EXISTS rel_src (""source TEXT, ""imdb_id TEXT, ""season TEXT, ""episode TEXT, ""hosts TEXT, ""added TEXT, ""UNIQUE(source, imdb_id, season, episode, hosts)"");")
        except:
            pass

        try:
            sources = []
            dbcur.execute("SELECT * FROM rel_src WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, name, 'live', ''))
            for row in dbcur:
                match = row
                t1 = int(re.sub('[^0-9]', '', str(match[5])))
                t2 = int(datetime.datetime.now().strftime("%Y%m%d%H%M"))
                update = abs(t2 - t1) > 300
                if update == False:
                    logger.debug('Fetched sources from cache for [%s]: %s'% (name, source))
                    sources = json.loads(match[4])
                    sources['content'] = 'live'
                    poster = sources['poster']
                    meta = {"poster":poster, "iconImage":poster, 'thumb': poster}
                    sources['meta'] = json.dumps(meta)
                    self.sources.append(sources)
                else:
                    raise Exception()
            if update == False:
                return self.sources
        except:
            logger.debug('Source from cache not found for [%s]: %s'% (name, source))
            pass
        try:
            sources = []
            try:
                # check if the source site needs to be refreshed
                dbcur.execute("SELECT * FROM rel_src WHERE source = '%s' AND season = '%s' AND episode = '%s'" % (source, 'live', ''))
                match = dbcur.fetchone()
                t1 = int(re.sub('[^0-9]', '', str(match[5])))
                t2 = int(datetime.datetime.now().strftime("%Y%m%d%H%M"))
                update = abs(t2 - t1) > 300
            except:
                update = True
            if update == False:
                sources == None
                logger.debug('No Update required for : %s' % source)
            else :
               logger.debug('Fetching Live source : %s' % source)
               sources = call.getLiveSource()
               dbcur.execute("DELETE FROM rel_src WHERE source = '%s' AND season = '%s' AND episode = '%s'" % (source, 'live', ''))
               dbcon.commit()

            if sources == None:
                raise Exception()
                sources = []

            for item in sources:
                item['name'] = cleantitle.live(item['name'])
                dbcur.execute("INSERT INTO rel_src Values (?, ?, ?, ?, ?, ?)", (source, item['name'], 'live', '', json.dumps(item), datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
                dbcon.commit()

            try:
                sources = []
                if name == None or name == '' :
                    dbcur.execute("SELECT * FROM rel_src WHERE source = '%s' AND season = '%s' AND episode = '%s'" % (source, 'live', ''))
                    for row in dbcur:
                        match = row[4]
                        self.sources.append(json.loads(match))
                else :
                    dbcur.execute("SELECT * FROM rel_src WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, name, 'live', ''))
                    for row in dbcur:
                        match = row
                        sources = json.loads(match[4])
                        sources['content'] = 'live'
                        self.sources.append(sources)
                return self.sources
            except:
                pass
        except:
            pass

    def sourcesDialog(self):
        try:
            sources = [{'label': '00 | [B]%s[/B]' % control.lang(30509).encode('utf-8').upper()}] + self.sources

            labels = [i['label'] for i in sources]

            select = control.selectDialog(labels)
            if select == 0: return self.sourcesDirect()
            if select == -1: return 'close://'

            items = [self.sources[select-1]]

            next = [y for x,y in enumerate(self.sources) if x >= select]
            prev = [y for x,y in enumerate(self.sources) if x < select][::-1]

            source, quality = items[0]['source'], items[0]['quality']
            items = [i for i in items+next+prev if i['quality'] == quality and i['source'] == source][:10]
            items += [i for i in next+prev if i['quality'] == quality and not i['source'] == source][:10]

            self.progressDialog = control.progressDialog
            self.progressDialog.create(control.addonInfo('name'), '')
            self.progressDialog.update(0)

            block = None

            for i in range(len(items)):
                try:
                    if self.progressDialog.iscanceled(): break

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
                        time.sleep(0.5)

                    for x in range(30):
                        if m == '': break
                        if self.progressDialog.iscanceled(): return self.progressDialog.close()
                        if xbmc.abortRequested == True: return sys.exit()
                        if w.is_alive() == False: break
                        time.sleep(0.5)


                    if w.is_alive() == True: block = items[i]['source']

                    if self.url == None: raise Exception()

                    self.selectedSource = items[i]['label']
                    self.progressDialog.close()

                    return self.url
                except:
                    pass

            try: self.progressDialog.close()
            except: pass

        except:
            try: self.progressDialog.close()
            except: pass

    def sourcesDirect(self):

        u = None

        self.progressDialog = control.progressDialog
        self.progressDialog.create(control.addonInfo('name'), '')
        self.progressDialog.update(0)

        for i in range(len(self.sources)):
            try:
                if self.progressDialog.iscanceled(): break

                self.progressDialog.update(int((100 / float(len(self.sources))) * i), str(self.sources[i]['label']), str(' '))

                if xbmc.abortRequested == True: return sys.exit()

                url = self.sourcesResolve(self.sources[i])
                if url == None: raise Exception()
                if u == None: u = url

                self.selectedSource = self.sources[i]['label']
                self.progressDialog.close()

                return url
            except:
                pass

        try: self.progressDialog.close()
        except: pass

        return u

    def alterSources(self, url, meta):
        try:
            setting = control.setting('autoplay')
            if setting == 'false': url += '&url=direct://'
            else: url += '&url=dialog://'

            control.execute('RunPlugin(%s)' % url)
        except:
            pass

    def clearSources(self):
        try:
            control.idle()

            yes = control.yesnoDialog(control.lang(30510).encode('utf-8'), '', '')
            if not yes: return

            control.makeFile(control.dataPath)
            dbcon = database.connect(control.sourcescacheFile)
            dbcur = dbcon.cursor()
            dbcur.execute("DROP TABLE IF EXISTS rel_src")
            dbcur.execute("VACUUM")
            dbcon.commit()

            control.infoDialog(control.lang(30511).encode('utf-8'))
        except:
            pass

    def sourcesFilter(self):
        for i in range(len(self.sources)): self.sources[i]['source'] = self.sources[i]['source'].lower()
        self.sources = sorted(self.sources, key=lambda k: k['source'])

        random.shuffle(self.sources)

        filter = []
        filter += [i for i in self.sources if i['direct'] == True]
        try:filter += [i for i in self.sources if i['content'] == 'live']
        except:pass
        for host in self.hostDict : filter += [i for i in self.sources if i['direct'] == False and i['source'] in host]
        self.sources = filter

        filter = []
        filter += [i for i in self.sources if i['quality'] == '1080p']
        filter += [i for i in self.sources if i['quality'] == 'HD']
        filter += [i for i in self.sources if i['quality'] == 'SD']
        if len(filter) < 15: filter += [i for i in self.sources if i['quality'] == 'SCR']
        if len(filter) < 15:filter += [i for i in self.sources if i['quality'] == 'CAM']
        if len(filter) < 15:filter += [i for i in self.sources if i['quality'] == '']
        self.sources = filter

        for i in range(len(self.sources)):
            s = self.sources[i]['source'].lower()
            p = self.sources[i]['provider']
            p = re.sub('v\d*$', '', p)


            q = self.sources[i]['quality']

            try: d = self.sources[i]['info']
            except: d = ''
            if not d == '': d = ' | [I]%s [/I]' % d

            label = '%02d | [B]%s[/B] | ' % (int(i+1), p)

            if q in ['1080p', 'HD']: label += '%s%s | [B][I]%s [/I][/B]' % (s.rsplit('.', 1)[0], d, q)
            elif q == '' : label += '%s%s' % (s.rsplit('.', 1)[0], d)
            else: label += '%s%s | [I]%s [/I]' % (s.rsplit('.', 1)[0], d, q)

            pts = None
            try : pts = self.sources[i]['parts']
            except:pass

            if not pts == None and int(pts) > 1:
                label += ' [%s]' % pts

            self.sources[i]['label'] = label.upper()
        return self.sources

    def sourcesResolve(self, item):
        try:
            u = url = item['url']
            provider = item['provider'].lower()

            if not provider.endswith(('_mv', '_tv', '_mv_tv')):
                sourceDict = []
                for package, name, is_pkg in pkgutil.walk_packages(__path__): sourceDict.append((name, is_pkg))
                provider = [i[0] for i in sourceDict if i[1] == False and i[0].startswith(provider + '_')][0]

            source = __import__(provider, globals(), locals(), [], -1).source()
            url = source.resolve(url, self.resolverList)

            if url == False: raise Exception()

            try: headers = dict(urlparse.parse_qsl(url.rsplit('|', 1)[1]))
            except: headers = dict('')

            if type(url) is list :
                self.url = url
                return url
            self.url = url
            return url
        except:
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

# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 Exodus

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


import sys,pkgutil,re,json,urllib,urlparse,random,datetime,time

from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import workers

try: from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database

try: import urlresolver
except: pass

try: import xbmc
except: pass



class sources:
    def __init__(self):
        self.getConstants()
        self.sources = []


    def play(self, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, url):
        try:
            if not control.addonInfo('id').lower() == control.infoLabel('Container.PluginName').lower():
                progress = True if control.setting('progress.dialog') == '1' else False
            else:
                control.resolve(int(sys.argv[1]), True, control.item(path=''))
                control.execute('Dialog.Close(okdialog)')
                progress = True

            if 'super.fav' in control.infoLabel('Container.PluginName'):
                return control.dialog.ok('Exodus', control.lang(30518).encode('utf-8'), '', '')

            items = self.getSources(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, progress=progress)

            if control.window.getProperty('PseudoTVRunning') == 'True':
                return control.resolve(int(sys.argv[1]), True, control.item(path=str(self.sourcesDirect(items, progress=progress))))

            if items == []: raise Exception()

            if url == 'direct://': url = self.sourcesDirect(items, progress=progress)
            elif url == 'dialog://': url = self.sourcesDialog(items, progress=progress)
            elif control.setting('autoplay') == 'false': url = self.sourcesDialog(items, progress=progress)
            else: url = self.sourcesDirect(items, progress=progress)

            if url == None: raise Exception()
            if url == 'close://': return

            control.sleep(200)

            if not tvshowtitle == None: title = tvshowtitle

            from resources.lib.modules.player import player
            player().run(title, year, season, episode, imdb, tvdb, meta, url)

            return url
        except:
            control.infoDialog(control.lang(30501).encode('utf-8'))


    def addItem(self, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta):
        try:
            if 'super.fav' in control.infoLabel('Container.PluginName'):
                return control.dialog.ok('Exodus', control.lang(30518).encode('utf-8'), '', '')

            self.sources = self.getSources(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered)
            if self.sources == []: raise Exception()

            self.progressDialog = control.progressDialog
            self.progressDialog.create(control.addonInfo('name'), '')
            self.progressDialog.update(0, control.lang(30515).encode('utf-8'), str(' '))

            content = 'movies' if tvshowtitle == None else 'episodes'

            trailerMenu = control.lang(30516).encode('utf-8') if tvshowtitle == None else control.lang(30517).encode('utf-8')

            infoMenu = control.lang(30502).encode('utf-8') if tvshowtitle == None else control.lang(30503).encode('utf-8')

            downloads = True if control.setting('downloads') == 'true' and not (control.setting('movie.download.path') == '' or control.setting('tv.download.path') == '') else False

            meta = json.loads(meta)

            try: del meta['duration']
            except: pass

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

            systitle = urllib.quote_plus('%s (%s)' % (title, year) if tvshowtitle == None or season == None or episode == None else '%s S%02dE%02d' % (tvshowtitle, int(season), int(episode)))
            sysname = urllib.quote_plus('%s (%s)' % (title, year) if tvshowtitle == None or season == None or episode == None else tvshowtitle)
            sysimage, sysaddon = urllib.quote_plus(poster), sys.argv[0]

            for i in range(len(self.sources)):
                try:
                    #if self.progressDialog.iscanceled(): break

                    self.progressDialog.update(int((100 / float(len(self.sources))) * i))

                    label = self.sources[i]['label']

                    syssource = urllib.quote_plus(json.dumps([self.sources[i]]))

                    url = '%s?action=playItem&source=%s' % (sysaddon, syssource)

                    cm = []
                    cm.append((control.lang(30504).encode('utf-8'), 'RunPlugin(%s?action=queueItem)' % sysaddon))

                    if downloads == True:
                        cm.append((control.lang(30505).encode('utf-8'), 'RunPlugin(%s?action=download&name=%s&image=%s&source=%s)' % (sysaddon, systitle, sysimage, syssource)))

                    cm.append((trailerMenu, 'RunPlugin(%s?action=trailer&name=%s)' % (sysaddon, sysname)))
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
                    item.addContextMenuItems(cm, replaceItems=True)
                    control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)
                except:
                    pass


            control.content(int(sys.argv[1]), content)
            control.directory(int(sys.argv[1]), cacheToDisc=True)
            try: self.progressDialog.close()
            except: pass
        except:
            control.infoDialog(control.lang(30501).encode('utf-8'))
            try: self.progressDialog.close()
            except: pass


    def playItem(self, source):
        try:
            f = dict(urlparse.parse_qsl(control.infoLabel('Container.FolderPath').replace('?','')))

            meta = f['meta'] if 'meta' in f else None
            title = f['title'] if 'title' in f else None
            title = f['tvshowtitle'] if 'tvshowtitle' in f else title
            year = f['year'] if 'year' in f else None
            season = f['season'] if 'season' in f else None
            episode = f['episode'] if 'episode' in f else None
            imdb = f['imdb'] if 'imdb' in f else None
            tvdb = f['tvdb'] if 'tvdb' in f else None

            next = [] ; prev = [] ; total = []

            for i in range(1,1000):
                try:
                    u = control.infoLabel('ListItem(%s).FolderPath' % str(i))
                    if u in total: raise Exception()
                    total.append(u)
                    u = dict(urlparse.parse_qsl(u.replace('?','')))
                    u = json.loads(u['source'])[0]
                    next.append(u)
                except:
                    break
            for i in range(-1000,0)[::-1]:
                try:
                    u = control.infoLabel('ListItem(%s).FolderPath' % str(i))
                    if u in total: raise Exception()
                    total.append(u)
                    u = dict(urlparse.parse_qsl(u.replace('?','')))
                    u = json.loads(u['source'])[0]
                    prev.append(u)
                except:
                    break

            items = json.loads(source)
            items = [i for i in items+next+prev][:20]

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
                        time.sleep(0.5)

                    for x in range(30):
                        if m == '': break
                        if self.progressDialog.iscanceled(): return self.progressDialog.close()
                        if xbmc.abortRequested == True: return sys.exit()
                        if w.is_alive() == False: break
                        time.sleep(0.5)


                    if w.is_alive() == True: block = items[i]['source']

                    if self.url == None: raise Exception()

                    try: self.progressDialog.close()
                    except: pass

                    control.sleep(200)

                    from resources.lib.modules.player import player
                    player().run(title, year, season, episode, imdb, tvdb, meta, self.url)

                    return self.url
                except:
                    pass

            try: self.progressDialog.close()
            except: pass

            raise Exception()

        except:
            control.infoDialog(control.lang(30501).encode('utf-8'))
            pass


    def getSources(self, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, presetDict=[], timeout=30, progress=True):
        sourceDict = []
        for package, name, is_pkg in pkgutil.walk_packages(__path__): sourceDict.append((name, is_pkg))
        sourceDict = [i[0] for i in sourceDict if i[1] == False]

        if not presetDict == []: sourceDict = [i for i in presetDict if i in sourceDict]

        content = 'movie' if tvshowtitle == None else 'episode'

        if content == 'movie':
            sourceDict = [i for i in sourceDict if i.endswith(('_mv', '_mv_tv'))]
        else:
            sourceDict = [i for i in sourceDict if i.endswith(('_tv', '_mv_tv'))]

        try: sourceDict = [(i, control.setting('provider.' + re.sub('_mv_tv$|_mv$|_tv$', '', i))) for i in sourceDict]
        except: sourceDict = [(i, 'true') for i in sourceDict]

        sourceDict = [i[0] for i in sourceDict if not i[1] == 'false']

        threads = []

        control.makeFile(control.dataPath)
        self.sourceFile = control.providercacheFile


        if content == 'movie':
            title = cleantitle.normalize(title)
            for source in sourceDict: threads.append(workers.Thread(self.getMovieSource, title, year, imdb, re.sub('_mv_tv$|_mv$|_tv$', '', source), __import__(source, globals(), locals(), [], -1).source()))
        else:
            tvshowtitle = cleantitle.normalize(tvshowtitle)
            for source in sourceDict: threads.append(workers.Thread(self.getEpisodeSource, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, re.sub('_mv_tv$|_mv$|_tv$', '', source), __import__(source, globals(), locals(), [], -1).source()))


        try: timeout = int(control.setting('scrapers.timeout.1'))
        except: pass

        [i.start() for i in threads]

        control.idle()

        sourceLabel = [re.sub('_mv_tv$|_mv$|_tv$', '', i) for i in sourceDict]
        sourceLabel = [re.sub('v\d+$', '', i).upper() for i in sourceLabel]

        if progress == True:
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

                if progress == True:
                    self.progressDialog.update(int((100 / float(len(threads))) * len([x for x in threads if x.is_alive() == False])), str('%s: %s %s' % (string1, int(i * 0.5), string2)), str('%s: %s' % (string3, str(info).translate(None, "[]'"))))
                    if self.progressDialog.iscanceled(): break

                is_alive = [x.is_alive() for x in threads]
                if all(x == False for x in is_alive): break
                time.sleep(0.5)
            except:
                pass

        try: self.progressDialog.close()
        except: pass

        self.sourcesFilter()

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
            if url == None: url = call.movie(imdb, title, year)
            if url == None: raise Exception()
            dbcur.execute("DELETE FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, '', ''))
            dbcur.execute("INSERT INTO rel_url Values (?, ?, ?, ?, ?)", (source, imdb, '', '', url))
            dbcon.commit()
        except:
            pass

        try:
            sources = []
            sources = call.sources(url, self.hostDict, self.hostprDict)
            if sources == None: sources = []
            self.sources.extend(sources)
            dbcur.execute("DELETE FROM rel_src WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, '', ''))
            dbcur.execute("INSERT INTO rel_src Values (?, ?, ?, ?, ?, ?)", (source, imdb, '', '', json.dumps(sources), datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
            dbcon.commit()
        except:
            pass


    def getEpisodeSource(self, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, source, call):
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
            if url == None: url = call.tvshow(imdb, tvdb, tvshowtitle, year)
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
            if ep_url == None: ep_url = call.episode(url, imdb, tvdb, title, premiered, season, episode)
            if ep_url == None: raise Exception()
            dbcur.execute("DELETE FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, season, episode))
            dbcur.execute("INSERT INTO rel_url Values (?, ?, ?, ?, ?)", (source, imdb, season, episode, ep_url))
            dbcon.commit()
        except:
            pass

        try:
            sources = []
            sources = call.sources(ep_url, self.hostDict, self.hostprDict)
            if sources == None: sources = []
            self.sources.extend(sources)
            dbcur.execute("DELETE FROM rel_src WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, season, episode))
            dbcur.execute("INSERT INTO rel_src Values (?, ?, ?, ?, ?, ?)", (source, imdb, season, episode, json.dumps(sources), datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
            dbcon.commit()
        except:
            pass


    def getURISource(self, url):
        try:
            sourceDict = []
            for package, name, is_pkg in pkgutil.walk_packages(__path__): sourceDict.append((name, is_pkg))
            sourceDict = [i[0] for i in sourceDict if i[1] == False]
            sourceDict = [(i, __import__(i, globals(), locals(), [], -1).source()) for i in sourceDict]

            domain = (urlparse.urlparse(url).netloc).lower()

            domains = [(i[0], i[1].domains) for i in sourceDict]
            domains = [i[0] for i in domains if any(x in domain for x in i[1])]

            if len(domains) == 0: return False

            call = [i[1] for i in sourceDict if i[0] == domains[0]][0]

            self.sources = call.sources(url, self.hostDict, self.hostprDict)
            self.sources = self.sourcesFilter()
            return self.sources
        except:
            pass


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
            dbcon = database.connect(control.providercacheFile)
            dbcur = dbcon.cursor()
            dbcur.execute("DROP TABLE IF EXISTS rel_src")
            dbcur.execute("VACUUM")
            dbcon.commit()

            control.infoDialog(control.lang(30511).encode('utf-8'))
        except:
            pass


    def sourcesFilter(self):
        provider = control.setting('hosts.sort.provider')

        quality = control.setting('hosts.quality')
        if quality == '': quality = '0'

        captcha = control.setting('hosts.captcha')


        random.shuffle(self.sources)

        if provider == 'true':
            self.sources = sorted(self.sources, key=lambda k: k['provider'])

        local = [i for i in self.sources if 'local' in i and i['local'] == True]
        self.sources = [i for i in self.sources if not i in local]

        filter = []
        filter += [i for i in self.sources if i['direct'] == True]
        filter += [i for i in self.sources if i['direct'] == False]
        self.sources = filter

        filter = []
        for d in self.debridDict: filter += [dict(i.items() + [('debrid', d)]) for i in self.sources if i['source'].lower() in self.debridDict[d]]
        filter += [i for i in self.sources if not i['source'].lower() in self.hostprDict and i['debridonly'] == False]
        self.sources = filter

        filter = []
        filter += local
        if quality == '0': filter += [i for i in self.sources if i['quality'] == '1080p' and 'debrid' in i]
        if quality == '0' or quality == '1': filter += [i for i in self.sources if i['quality'] == 'HD' and 'debrid' in i]
        if quality == '0': filter += [i for i in self.sources if i['quality'] == '1080p' and not 'debrid' in i and 'memberonly' in i]
        if quality == '0' or quality == '1': filter += [i for i in self.sources if i['quality'] == 'HD' and not 'debrid' in i and 'memberonly' in i]
        if quality == '0': filter += [i for i in self.sources if i['quality'] == '1080p' and not 'debrid' in i and not 'memberonly' in i]
        if quality == '0' or quality == '1': filter += [i for i in self.sources if i['quality'] == 'HD' and not 'debrid' in i and not 'memberonly' in i]
        filter += [i for i in self.sources if i['quality'] == 'SD']
        if len(filter) < 10: filter += [i for i in self.sources if i['quality'] == 'SCR']
        if len(filter) < 10: filter += [i for i in self.sources if i['quality'] == 'CAM']
        self.sources = filter

        if not captcha == 'true':
            filter = [i for i in self.sources if i['source'].lower() in self.hostcapDict and not 'debrid' in i]
            self.sources = [i for i in self.sources if not i in filter]

        self.sources = self.sources[:2000]

        for i in range(len(self.sources)):
            u = self.sources[i]['url']
            s = self.sources[i]['source'].lower()
            p = self.sources[i]['provider']
            p = re.sub('v\d*$', '', p)

            q = self.sources[i]['quality']

            try: f = (' | ' + ' | '.join(['[I]%s [/I]' % info.strip() for info in self.sources[i]['info'].split('|')])).replace('[I]HEVC [/I]', 'HEVC')
            except: f = ''

            try: d = self.sources[i]['debrid']
            except: d = self.sources[i]['debrid'] = ''

            if not d == '': label = '%02d | [B]%s[/B] | ' % (int(i+1), d)
            #if not d == '': label = '%02d | [B]%s[/B] | [B]%s[/B] | ' % (int(i+1), p, d)
            else: label = '%02d | [B]%s[/B] | ' % (int(i+1), p)

            if q in ['1080p', 'HD']: label += '%s%s | [B][I]%s [/I][/B]' % (s.rsplit('.', 1)[0], f, q)
            else: label += '%s%s | [I]%s [/I]' % (s.rsplit('.', 1)[0], f, q)
            label = label.replace('| 0 |', '|').replace(' | [I]0 [/I]', '')

            self.sources[i]['label'] = label.upper()

        return self.sources


    def sourcesResolve(self, item):
        try:
            self.url = None

            u = url = item['url']

            d = item['debrid'] ; direct = item['direct']

            provider = item['provider'].lower()

            if not provider.endswith(('_mv', '_tv', '_mv_tv')):
                sourceDict = []
                for package, name, is_pkg in pkgutil.walk_packages(__path__): sourceDict.append((name, is_pkg))
                provider = [i[0] for i in sourceDict if i[1] == False and i[0].startswith(provider + '_')][0]

            source = __import__(provider, globals(), locals(), [], -1).source()
            u = url = source.resolve(url)

            if url == None: raise Exception()

            if not d == '':
                self.url = url = debrid.resolver(url, d)
                if url == None: raise Exception()
                ext = url.split('?')[0].split('&')[0].split('|')[0].rsplit('.')[-1].replace('/', '').lower()
                if ext == 'rar': raise Exception()
                return url

            elif not direct == True:
                try:
                    hmf = urlresolver.HostedMediaFile(url=u, include_disabled=True, include_universal=False)
                    if hmf.valid_url() == True: url = hmf.resolve()
                except:
                    pass
                try:
                    hmf = urlresolver.plugnplay.man.implementors(urlresolver.UrlResolver)
                    hmf = [i for i in hmf if not '*' in i.domains]
                    hmf = [(i, i.get_host_and_id(u)) for i in hmf]
                    hmf = [i for i in hmf if not i[1] == False]
                    hmf = [(i[0], i[0].valid_url(u, i[1][0]), i[1][0], i[1][1]) for i in hmf]
                    hmf = [i for i in hmf if not i[1] == False][0]
                    url = hmf[0].get_media_url(hmf[2], hmf[3])
                except:
                    pass

            if url == False or url == None: raise Exception()

            try: headers = url.rsplit('|', 1)[1]
            except: headers = ''
            headers = urllib.quote_plus(headers).replace('%3D', '=') if ' ' in headers else headers
            headers = dict(urlparse.parse_qsl(headers))


            if url.startswith('http') and '.m3u8' in url:
                result = client.request(url.split('|')[0], headers=headers, output='geturl', timeout='20')
                if result == None: raise Exception()

            elif url.startswith('http'):
                result = client.request(url.split('|')[0], headers=headers, output='chunk', timeout='20')
                if result == None: raise Exception()

            self.url = url
            return url
        except:
            return


    def sourcesDialog(self, items, progress=True):
        try:
            sources = [{'label': '00 | [B]%s[/B]' % control.lang(30509).encode('utf-8').upper()}] + items

            labels = [i['label'] for i in sources]

            select = control.selectDialog(labels)
            if select == 0: return self.sourcesDirect(items, progress=progress)
            if select == -1: return 'close://'

            next = [y for x,y in enumerate(items) if x >= select]
            prev = [y for x,y in enumerate(items) if x < select][::-1]

            items = [items[select-1]]
            items = [i for i in items+next+prev][:20]

            if progress == True:
                self.progressDialog = control.progressDialog
                self.progressDialog.create(control.addonInfo('name'), '')
                self.progressDialog.update(0)

            block = None

            for i in range(len(items)):
                try:
                    if progress == True:
                        if self.progressDialog.iscanceled(): break
                        self.progressDialog.update(int((100 / float(len(items))) * i), str(items[i]['label']), str(' '))

                    if items[i]['source'] == block: raise Exception()

                    w = workers.Thread(self.sourcesResolve, items[i])
                    w.start()

                    m = ''

                    for x in range(3600):
                        if progress == True:
                            if self.progressDialog.iscanceled(): return self.progressDialog.close()
                        if xbmc.abortRequested == True: return sys.exit()
                        k = control.condVisibility('Window.IsActive(virtualkeyboard)')
                        if k: m += '1'; m = m[-1]
                        if (w.is_alive() == False or x > 30) and not k: break
                        time.sleep(0.5)

                    for x in range(30):
                        if m == '': break
                        if progress == True:
                            if self.progressDialog.iscanceled(): return self.progressDialog.close()
                        if xbmc.abortRequested == True: return sys.exit()
                        if w.is_alive() == False: break
                        time.sleep(0.5)


                    if w.is_alive() == True: block = items[i]['source']

                    if self.url == None: raise Exception()

                    self.selectedSource = items[i]['label']

                    try: self.progressDialog.close()
                    except: pass

                    return self.url
                except:
                    pass

            try: self.progressDialog.close()
            except: pass

        except:
            try: self.progressDialog.close()
            except: pass


    def sourcesDirect(self, items, progress=True):
        filter = [i for i in items if i['source'].lower() in self.hostcapDict and i['debrid'] == '']
        items = [i for i in items if not i in filter]

        items = [i for i in items if ('autoplay' in i and i['autoplay'] == True) or not 'autoplay' in i]

        if control.setting('autoplay.sd') == 'true':
            items = [i for i in items if not i['quality'] in ['1080p', 'HD']]

        u = None

        try:
            if not progress == True: raise Exception()
            control.sleep(1000)
            self.progressDialog = control.progressDialog
            self.progressDialog.create(control.addonInfo('name'), '')
            self.progressDialog.update(0)
        except:
            pass

        for i in range(len(items)):
            try:
                if not progress == True: raise Exception()
                self.progressDialog.update(int((100 / float(len(items))) * i), str(items[i]['label']), str(' '))
                if self.progressDialog.iscanceled(): break
            except:
                pass

            try:
                if xbmc.abortRequested == True: return sys.exit()

                url = self.sourcesResolve(items[i])
                if u == None: u = url
                if not url == None: break
            except:
                pass

        try: self.progressDialog.close()
        except: pass

        return u


    def getConstants(self):
        try:
            try: self.hostDict = urlresolver.relevant_resolvers(order_matters=True)
            except: self.hostDict = urlresolver.plugnplay.man.implementors(urlresolver.UrlResolver)
            self.hostDict = [i.domains for i in self.hostDict if not '*' in i.domains]
            self.hostDict = [i.lower() for i in reduce(lambda x, y: x+y, self.hostDict)]
            self.hostDict = [x for y,x in enumerate(self.hostDict) if x not in self.hostDict[:y]]
        except:
            self.hostDict = []

        self.hostprDict = ['oboom.com', 'rapidgator.net', 'rg.to', 'uploaded.net', 'uploaded.to', 'ul.to', 'filefactory.com', 'nitroflare.com', 'turbobit.net']

        self.hostcapDict = ['hugefiles.net', 'kingfiles.net']

        self.debridDict = debrid.debridDict()



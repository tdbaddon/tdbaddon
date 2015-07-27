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


try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

import re
import sys
import urllib
import urlparse
import json
import datetime
import time
import pkgutil
import threading
from modules.libraries import control
from modules.libraries import cleantitle
from modules.libraries import client
from modules.libraries import ep_redirect
from modules.resolvers import realdebrid
from modules.resolvers import premiumize
from modules import resolvers



class sources:
    def __init__(self):
        self.sources = [] ; self.sourcesDictionary()


    def play(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, url):
        try:
            if show == None: content = 'movie'
            else: content = 'episode'

            self.sources = self.getSources(name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre)
            if self.sources == []: raise Exception()
            self.sources = self.sourcesFilter()


            if control.window.getProperty('PseudoTVRunning') == 'True':
                url = self.sourcesDirect()

            elif url == 'dialog://':
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

            from modules.libraries.player import player
            player().run(content, name, url, imdb, tvdb)

            return url
        except:
            control.infoDialog(control.lang(30308).encode('utf-8'))
            pass


    def addPlayableItem(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, meta):
        try:
            if tvdb == None: tvdb = '0'

            if show == None: content = 'movie'
            else: content = 'episode'

            self.sources = self.getSources(name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre)
            if self.sources == []: raise Exception()
            self.sources = self.sourcesFilter()

            meta = json.loads(meta)

            try: poster, banner, thumb, fanart = meta['poster'], meta['banner'], meta['thumb'], meta['fanart']
            except: poster, banner, thumb, fanart = meta['poster'], meta['poster'], meta['poster'], meta['fanart']

            if control.setting('fanart') == 'true' and not fanart == '0': pass
            else: fanart = control.addonFanart()

            sysaddon = sys.argv[0]

            for i in self.sources:
                try:
                    url, source, provider = i['url'], i['label'], i['provider']

                    sysname, sysimdb, systvdb, sysurl, sysimage, syssource, sysprovider = urllib.quote_plus(name), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(url), urllib.quote_plus(poster), urllib.quote_plus(source), urllib.quote_plus(provider)

                    query = 'action=playItem&content=%s&name=%s&imdb=%s&tvdb=%s&url=%s&source=%s&provider=%s' % (content, sysname, sysimdb, systvdb, sysurl, syssource, sysprovider)

                    cm = []
                    cm.append((control.lang(30401).encode('utf-8'), 'RunPlugin(%s?action=queueItem)' % (sysaddon)))
                    cm.append((control.lang(30402).encode('utf-8'), 'RunPlugin(%s?action=addDownload&name=%s&url=%s&image=%s&provider=%s)' % (sysaddon, sysname, sysurl, sysimage, sysprovider)))
                    cm.append((control.lang(30412).encode('utf-8'), 'Action(Info)'))
                    cm.append((control.lang(30427).encode('utf-8'), 'RunPlugin(%s?action=refresh)' % (sysaddon)))
                    cm.append((control.lang(30410).encode('utf-8'), 'RunPlugin(%s?action=openSettings)' % (sysaddon)))
                    cm.append((control.lang(30411).encode('utf-8'), 'RunPlugin(%s?action=openPlaylist)' % (sysaddon)))

                    item = control.item(source, iconImage='DefaultVideo.png', thumbnailImage=thumb)
                    try: item.setArt({'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})
                    except: pass
                    item.setInfo(type='Video', infoLabels = meta)
                    if not fanart == None: item.setProperty('Fanart_Image', fanart)
                    item.setProperty('Video', 'true')
                    item.setProperty('IsPlayable', 'true')
                    item.addContextMenuItems(cm, replaceItems=True)
                    control.addItem(handle=int(sys.argv[1]),url='%s?%s' % (sysaddon, query),listitem=item,isFolder=False)
                except:
                    pass

            control.directory(int(sys.argv[1]), cacheToDisc=True)
        except:
            control.infoDialog(control.lang(30308).encode('utf-8'))
            pass


    def playItem(self, content, name, imdb, tvdb, url, source, provider):
        try:
            url = self.sourcesResolve(url, provider)
            if url == None: raise Exception()

            if control.setting('playback_info') == 'true':
                control.infoDialog(source, heading=name)

            from modules.libraries.player import player
            player().run(content, name, url, imdb, tvdb)

            return url
        except:
            control.infoDialog(control.lang(30308).encode('utf-8'))
            pass


    def getSources(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre):
        sourceDict = []
        for package, name, is_pkg in pkgutil.walk_packages(__path__): sourceDict.append((name, is_pkg))
        sourceDict = [i[0] for i in sourceDict if i[1] == False]

        if show == None: content = 'movie'
        else: content = 'episode'


        if content == 'movie':
            sourceDict = [i for i in sourceDict if i.endswith(('_mv', '_mv_tv'))]
            try: sourceDict = [(i, control.setting(re.sub('_mv_tv$|_mv$|_tv$', '', i))) for i in sourceDict]
            except: sourceDict = [(i, 'true') for i in sourceDict]
        else:
            sourceDict = [i for i in sourceDict if i.endswith(('_tv', '_mv_tv'))]
            try: sourceDict = [(i, control.setting(re.sub('_mv_tv$|_mv$|_tv$', '', i) + '_tv')) for i in sourceDict]
            except: sourceDict = [(i, 'true') for i in sourceDict]


        global global_sources
        global_sources = []

        threads = []

        control.makeFile(control.dataPath)
        self.sourceFile = control.cachesourcesFile

        sourceDict = [i[0] for i in sourceDict if i[1] == 'true']

        if content == 'movie':
            title = cleantitle.normalize(title)
            for source in sourceDict: threads.append(Thread(self.getMovieSource, title, year, imdb, re.sub('_mv_tv$|_mv$|_tv$', '', source), __import__(source, globals(), locals(), [], -1).source()))
        else:
            show, show_alt = cleantitle.normalize(show), cleantitle.normalize(show_alt)
            season, episode = ep_redirect.get(title, year, imdb, tvdb, season, episode, show, date, genre)
            for source in sourceDict: threads.append(Thread(self.getEpisodeSource, title, year, imdb, tvdb, date, season, episode, show, show_alt, re.sub('_mv_tv$|_mv$|_tv$', '', source), __import__(source, globals(), locals(), [], -1).source()))


        try: timeout = int(control.setting('sources_timeout_beta'))
        except: timeout = 10


        [i.start() for i in threads]
        #[i.join() for i in threads] ; self.sources = global_sources ; return self.sources


        for i in range(0, timeout * 2):
            is_alive = [x.is_alive() for x in threads]
            if all(x == False for x in is_alive): break
            time.sleep(0.5)

        for i in range(0, 5 * 2):
            is_alive = len([i for i in threads if i.is_alive() == True])
            if is_alive < 10: break
            time.sleep(0.5)


        self.sources = global_sources

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
            dbcur.execute("SELECT * FROM rel_src WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, 'tt' + imdb, '', ''))
            match = dbcur.fetchone()
            t1 = int(re.sub('[^0-9]', '', str(match[5])))
            t2 = int(datetime.datetime.now().strftime("%Y%m%d%H%M"))
            update = abs(t2 - t1) > 60
            if update == False:
                sources = json.loads(match[4])
                return global_sources.extend(sources)
        except:
            pass

        try:
            url = None
            dbcur.execute("SELECT * FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, 'tt' + imdb, '', ''))
            url = dbcur.fetchone()
            url = url[4]
        except:
            pass

        try:
            if url == None: url = call.get_movie(imdb, title, year)
            if url == None: raise Exception()
            dbcur.execute("DELETE FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, 'tt' + imdb, '', ''))
            dbcur.execute("INSERT INTO rel_url Values (?, ?, ?, ?, ?)", (source, 'tt' + imdb, '', '', url))
            dbcon.commit()
        except:
            pass

        try:
            sources = []
            sources = call.get_sources(url, self.hosthdfullDict, self.hostsdfullDict, self.hostlocDict)
            if sources == None: sources = []
            global_sources.extend(sources)
            dbcur.execute("DELETE FROM rel_src WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, 'tt' + imdb, '', ''))
            dbcur.execute("INSERT INTO rel_src Values (?, ?, ?, ?, ?, ?)", (source, 'tt' + imdb, '', '', json.dumps(sources), datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
            dbcon.commit()
        except:
            pass


    def getEpisodeSource(self, title, year, imdb, tvdb, date, season, episode, show, show_alt, source, call):
        try:
            dbcon = database.connect(self.sourceFile)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS rel_url (""source TEXT, ""imdb_id TEXT, ""season TEXT, ""episode TEXT, ""rel_url TEXT, ""UNIQUE(source, imdb_id, season, episode)"");")
            dbcur.execute("CREATE TABLE IF NOT EXISTS rel_src (""source TEXT, ""imdb_id TEXT, ""season TEXT, ""episode TEXT, ""hosts TEXT, ""added TEXT, ""UNIQUE(source, imdb_id, season, episode)"");")
        except:
            pass

        try:
            sources = []
            dbcur.execute("SELECT * FROM rel_src WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, 'tt' + imdb, season, episode))
            match = dbcur.fetchone()
            t1 = int(re.sub('[^0-9]', '', str(match[5])))
            t2 = int(datetime.datetime.now().strftime("%Y%m%d%H%M"))
            update = abs(t2 - t1) > 60
            if update == False:
                sources = json.loads(match[4])
                return global_sources.extend(sources)
        except:
            pass

        try:
            url = None
            dbcur.execute("SELECT * FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, 'tt' + imdb, '', ''))
            url = dbcur.fetchone()
            url = url[4]
        except:
            pass

        try:
            if url == None: url = call.get_show(imdb, tvdb, show, show_alt, year)
            if url == None: raise Exception()
            dbcur.execute("DELETE FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, 'tt' + imdb, '', ''))
            dbcur.execute("INSERT INTO rel_url Values (?, ?, ?, ?, ?)", (source, 'tt' + imdb, '', '', url))
            dbcon.commit()
        except:
            pass

        try:
            ep_url = None
            dbcur.execute("SELECT * FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, 'tt' + imdb, season, episode))
            ep_url = dbcur.fetchone()
            ep_url = ep_url[4]
        except:
            pass

        try:
            if url == None: raise Exception()
            if ep_url == None: ep_url = call.get_episode(url, imdb, tvdb, title, date, season, episode)
            if ep_url == None: raise Exception()
            dbcur.execute("DELETE FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, 'tt' + imdb, season, episode))
            dbcur.execute("INSERT INTO rel_url Values (?, ?, ?, ?, ?)", (source, 'tt' + imdb, season, episode, ep_url))
            dbcon.commit()
        except:
            pass

        try:
            sources = []
            sources = call.get_sources(ep_url, self.hosthdfullDict, self.hostsdfullDict, self.hostlocDict)
            if sources == None: sources = []
            global_sources.extend(sources)
            dbcur.execute("DELETE FROM rel_src WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, 'tt' + imdb, season, episode))
            dbcur.execute("INSERT INTO rel_src Values (?, ?, ?, ?, ?, ?)", (source, 'tt' + imdb, season, episode, json.dumps(sources), datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
            dbcon.commit()
        except:
            pass


    def clearSources(self):
        try:
            yes = control.yesnoDialog('Are you sure?', '', '')
            if not yes: return

            control.makeFile(control.dataPath)
            dbcon = database.connect(control.cachesourcesFile)
            dbcur = dbcon.cursor()
            dbcur.execute("DROP TABLE IF EXISTS rel_src")
            dbcur.execute("VACUUM")
            dbcon.commit()

            control.infoDialog('Process Complete')
        except:
            pass


    def sourcesFilter(self):
        try: customhdDict = [control.setting("hosthd1"), control.setting("hosthd2"), control.setting("hosthd3"), control.setting("hosthd4"), control.setting("hosthd5"), control.setting("hosthd6"), control.setting("hosthd7"), control.setting("hosthd8"), control.setting("hosthd9"), control.setting("hosthd10"), control.setting("hosthd11"), control.setting("hosthd12"), control.setting("hosthd13"), control.setting("hosthd14"), control.setting("hosthd15"), control.setting("hosthd16"), control.setting("hosthd17"), control.setting("hosthd18"), control.setting("hosthd19"), control.setting("hosthd20")]
        except: customhdDict = []
        try: customsdDict = [control.setting("host1"), control.setting("host2"), control.setting("host3"), control.setting("host4"), control.setting("host5"), control.setting("host6"), control.setting("host7"), control.setting("host8"), control.setting("host9"), control.setting("host10"), control.setting("host11"), control.setting("host12"), control.setting("host13"), control.setting("host14"), control.setting("host15"), control.setting("host16"), control.setting("host17"), control.setting("host18"), control.setting("host19"), control.setting("host20")]
        except: customsdDict = []

        hd_rank = []
        hd_rank += [i for i in self.rdDict if i in self.hostprDict + self.hosthdDict]
        hd_rank += [i for i in self.pzDict if i in self.hostprDict + self.hosthdDict]
        hd_rank += customhdDict
        hd_rank += [i['source'] for i in self.sources if i['quality'] in ['1080p', 'HD'] and not i['source'] in customhdDict + self.hostprDict + self.hosthdDict]
        hd_rank += self.hosthdDict
        hd_rank = [i.lower() for i in hd_rank]
        hd_rank = [x for y,x in enumerate(hd_rank) if x not in hd_rank[:y]]

        sd_rank = []
        sd_rank += [i for i in self.rdDict if i in self.hostprDict + self.hosthqDict]
        sd_rank += [i for i in self.pzDict if i in self.hostprDict + self.hosthqDict]
        sd_rank += customsdDict
        sd_rank += [i['source'] for i in self.sources if i['quality'] == 'SD' and not i['source'] in customsdDict + self.hostprDict + self.hosthqDict + self.hostmqDict + self.hostlqDict]
        sd_rank += self.hosthqDict + self.hostmqDict + self.hostlqDict
        sd_rank = [i.lower() for i in sd_rank]
        sd_rank = [x for y,x in enumerate(sd_rank) if x not in sd_rank[:y]]

        for i in range(len(self.sources)): self.sources[i]['source'] = self.sources[i]['source'].lower()
        self.sources = sorted(self.sources, key=lambda k: k['source'])

        filter = []
        for host in hd_rank: filter += [i for i in self.sources if i['quality'] == '1080p' and i['source'] == host]
        for host in hd_rank: filter += [i for i in self.sources if i['quality'] == 'HD' and i['source'] == host]
        for host in sd_rank: filter += [i for i in self.sources if i['quality'] == 'SD' and i['source'] == host]
        if len(filter) < 10: filter += [i for i in self.sources if i['quality'] == 'SCR']
        if len(filter) < 10: filter += [i for i in self.sources if i['quality'] == 'CAM']
        self.sources = filter

        try: playback_quality = control.setting("playback_quality")
        except: playback_quality = '0'

        if playback_quality == '1':
            self.sources = [i for i in self.sources if not i['quality'] == '1080p']
        elif playback_quality == '2':
            self.sources = [i for i in self.sources if not i['quality'] in ['1080p', 'HD']]
        elif playback_quality == '3':
            self.sources = [i for i in self.sources if not i['quality'] in ['1080p', 'HD'] and i['source'] in self.hostmqDict + self.hostlqDict]
        elif playback_quality == '4':
            self.sources = [i for i in self.sources if not i['quality'] in ['1080p', 'HD'] and i['source'] in self.hostlqDict]

        try: playback_captcha = control.setting("playback_captcha")
        except: playback_captcha = 'false'

        try: playback_1080p_hosts = control.setting("playback_1080p_hosts")
        except: playback_1080p_hosts = 'true'

        try: playback_720p_hosts = control.setting("playback_720p_hosts")
        except: playback_720p_hosts = 'true'

        if playback_captcha == 'false':
            self.sources = [i for i in self.sources if not i['source'] in self.hostcapDict]

        if playback_1080p_hosts == 'false':
            self.sources = [i for i in self.sources if not (i['quality'] == '1080p' and i['source'] in self.hosthdDict and not i['source'] in self.rdDict + self.pzDict)]

        if playback_720p_hosts == 'false':
            self.sources = [i for i in self.sources if not (i['quality'] == 'HD' and i['source'] in self.hosthdDict and not i['source'] in self.rdDict + self.pzDict)]

        for i in range(len(self.sources)):
            s = self.sources[i]['source'].lower()
            p = self.sources[i]['provider']

            q = self.sources[i]['quality']
            if q == 'SD' and s in self.hostmqDict: q = 'MQ'
            elif q == 'SD' and s in self.hostlqDict: q = 'LQ'
            elif q == 'SD': q = 'HQ'

            try: d = self.sources[i]['info']
            except: d = ''
            if not d == '': d = ' | [I]%s [/I]' % d

            if s in self.rdDict: label = '%02d | [B]realdebrid[/B] | ' % int(i+1)
            elif s in self.pzDict: label = '%02d | [B]premiumize[/B] | ' % int(i+1)
            else: label = '%02d | [B]%s[/B] | ' % (int(i+1), p)

            if q in ['1080p', 'HD']: label += '%s%s | [B][I]%s [/I][/B]' % (s, d, q)
            else: label += '%s%s | [I]%s [/I]' % (s, d, q)

            self.sources[i]['label'] = label.upper()

        return self.sources


    def sourcesResolve(self, url, provider):
        try:
            provider = provider.lower()

            if not provider.endswith(('_mv', '_tv', '_mv_tv')):
                sourceDict = []
                for package, name, is_pkg in pkgutil.walk_packages(__path__): sourceDict.append((name, is_pkg))
                provider = [i[0] for i in sourceDict if i[1] == False and i[0].startswith(provider + '_')][0]

            source = __import__(provider, globals(), locals(), [], -1).source()
            url = source.resolve(url)

            try: headers = dict(urlparse.parse_qsl(url.rsplit('|', 1)[1]))
            except: headers = dict('')

            result = client.request(url.split('|')[0], headers=headers, output='chunk', timeout='30')
            if result == None: raise Exception()
            return url
        except:
            return


    def sourcesDialog(self):
        try:
            l = '00 | [B]%s[/B]' % control.lang(30408).encode('utf-8').upper()
            sourceList = [l] ; urlList = [''] ; providerList = ['']

            for i in self.sources:
                sourceList.append(i['label']) ; urlList.append(i['url']) ; providerList.append(i['provider'])

            select = control.selectDialog(sourceList)
            if select == 0: return self.sourcesDirect()
            if select == -1: return 'close://'

            url = self.sourcesResolve(urlList[select], providerList[select])
            self.selectedSource = self.sources[select-1]['label']
            return url
        except:
            return


    def sourcesDirect(self):
        self.sources = [i for i in self.sources if not i['source'] in self.hostcapDict]

        self.sources = [i for i in self.sources if not (i['quality'] in ['1080p', 'HD'] and i['source'] in self.hosthdDict and not i['source'] in self.rdDict + self.pzDict)]

        self.sources = [i for i in self.sources if not i['source'] in ['furk']]

        if control.setting("playback_auto_sd") == 'true':
            self.sources = [i for i in self.sources if not i['quality'] in ['1080p', 'HD']]

        u = None

        for i in self.sources:
            try:
                url = self.sourcesResolve(i['url'], i['provider'])
                if url == None: raise Exception()
                if u == None: u = url

                self.selectedSource = i['label']
                return url
            except:
                pass

        return u


    def sourcesDictionary(self):
        hosts = resolvers.info()
        hosts = [i for i in hosts if 'host' in i]

        self.rdDict = realdebrid.getHosts()
        self.pzDict = premiumize.getHosts()

        self.hostlocDict = [i['netloc'] for i in hosts if i['quality'] == 'High' and i['captcha'] == False]
        try: self.hostlocDict = [i.lower() for i in reduce(lambda x, y: x+y, self.hostlocDict)]
        except: pass
        self.hostlocDict = [x for y,x in enumerate(self.hostlocDict) if x not in self.hostlocDict[:y]]

        self.hostprDict = [i['host'] for i in hosts if i['a/c'] == True]
        try: self.hostprDict = [i.lower() for i in reduce(lambda x, y: x+y, self.hostprDict)]
        except: pass
        self.hostprDict = [x for y,x in enumerate(self.hostprDict) if x not in self.hostprDict[:y]]

        self.hostcapDict = [i['host'] for i in hosts if i['captcha'] == True]
        try: self.hostcapDict = [i.lower() for i in reduce(lambda x, y: x+y, self.hostcapDict)]
        except: pass
        self.hostcapDict = [i for i in self.hostcapDict if not i in self.rdDict + self.pzDict]

        self.hosthdDict = [i['host'] for i in hosts if i['quality'] == 'High' and i['a/c'] == False and i['captcha'] == False]
        self.hosthdDict += [i['host'] for i in hosts if i['quality'] == 'High' and i['a/c'] == False and i['captcha'] == True]
        try: self.hosthdDict = [i.lower() for i in reduce(lambda x, y: x+y, self.hosthdDict)]
        except: pass

        self.hosthqDict = [i['host'] for i in hosts if i['quality'] == 'High' and i['a/c'] == False and i['captcha'] == False]
        try: self.hosthqDict = [i.lower() for i in reduce(lambda x, y: x+y, self.hosthqDict)]
        except: pass

        self.hostmqDict = [i['host'] for i in hosts if i['quality'] == 'Medium' and i['a/c'] == False and i['captcha'] == False]
        try: self.hostmqDict = [i.lower() for i in reduce(lambda x, y: x+y, self.hostmqDict)]
        except: pass

        self.hostlqDict = [i['host'] for i in hosts if i['quality'] == 'Low' and i['a/c'] == False and i['captcha'] == False]
        try: self.hostlqDict = [i.lower() for i in reduce(lambda x, y: x+y, self.hostlqDict)]
        except: pass

        self.hostsdfullDict = self.hostprDict + self.hosthqDict + self.hostmqDict + self.hostlqDict

        self.hosthdfullDict = self.hostprDict + self.hosthdDict



class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)


# -*- coding: utf-8 -*-

'''
    gClone Add-on
    Copyright (C) 2015 NVTTeam

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

import urllib,urllib2,urlparse,re,os,sys,threading,datetime,time,base64,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
from operator import itemgetter
import commonsources

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database
try:
    import CommonFunctions as common
except:
    import commonfunctionsdummy as common
try:
    import json
except:
    import simplejson as json


action              = None
getSetting          = xbmcaddon.Addon().getSetting
language            = xbmcaddon.Addon().getLocalizedString
addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
addonDesc           = language(30450).encode("utf-8")
dataPath            = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile")).decode("utf-8")
movieLibrary        = os.path.join(xbmc.translatePath(getSetting("movie_library")),'')
tvLibrary           = os.path.join(xbmc.translatePath(getSetting("tv_library")),'')
PseudoTV            = xbmcgui.Window(10000).getProperty('PseudoTVRunning')
addonLogos          = os.path.join(addonPath,'resources/logos')
addonSettings       = os.path.join(dataPath,'settings.db')
addonSources        = os.path.join(dataPath,'sources.db')
addonCache          = os.path.join(dataPath,'cache.db')


class main:
    def __init__(self):
        global action
        index().container_data()
        params = {}
        splitparams = sys.argv[2][sys.argv[2].find('?') + 1:].split('&')
        for param in splitparams:
            if (len(param) > 0):
                splitparam = param.split('=')
                key = splitparam[0]
                try:    value = splitparam[1].encode("utf-8")
                except: value = splitparam[1]
                params[key] = value

        try:        action = urllib.unquote_plus(params["action"])
        except:     action = None
        try:        name = urllib.unquote_plus(params["name"])
        except:     name = None
        try:        title = urllib.unquote_plus(params["title"])
        except:     title = None
        try:        year = urllib.unquote_plus(params["year"])
        except:     year = None
        try:        imdb = urllib.unquote_plus(params["imdb"])
        except:     imdb = None
        try:        tvdb = urllib.unquote_plus(params["tvdb"])
        except:     tvdb = None
        try:        season = urllib.unquote_plus(params["season"])
        except:     season = None
        try:        episode = urllib.unquote_plus(params["episode"])
        except:     episode = None
        try:        show = urllib.unquote_plus(params["show"])
        except:     show = None
        try:        show_alt = urllib.unquote_plus(params["show_alt"])
        except:     show_alt = None
        try:        date = urllib.unquote_plus(params["date"])
        except:     date = None
        try:        genre = urllib.unquote_plus(params["genre"])
        except:     genre = None
        try:        url = urllib.unquote_plus(params["url"])
        except:     url = None
        try:        image = urllib.unquote_plus(params["image"])
        except:     image = None
        try:        meta = urllib.unquote_plus(params["meta"])
        except:     meta = None
        try:        query = urllib.unquote_plus(params["query"])
        except:     query = None
        try:        source = urllib.unquote_plus(params["source"])
        except:     source = None
        try:        provider = urllib.unquote_plus(params["provider"])
        except:     provider = None

        if action == None:                            root().get()
        elif action == 'root_movies':                 root().movies()
        elif action == 'root_shows':                  root().shows()
        elif action == 'root_calendar':               root().calendar()
        elif action == 'root_genesis':                root().gClone()
        elif action == 'root_tools':                  root().tools()
        elif action == 'root_search':                 root().search()
        elif action == 'root_library':                root().library()
        elif action == 'cache_clear_list':            index().cache_clear_list()
        elif action == 'cache_clear_src':             index().cache_clear_src()
        elif action == 'container_refresh':           index().container_refresh()
        elif action == 'item_queue':                  contextMenu().item_queue()
        elif action == 'view_movies':                 contextMenu().view('movies')
        elif action == 'view_tvshows':                contextMenu().view('tvshows')
        elif action == 'view_seasons':                contextMenu().view('seasons')
        elif action == 'view_episodes':               contextMenu().view('episodes')
        elif action == 'playlist_open':               contextMenu().playlist_open()
        elif action == 'settings_open':               contextMenu().settings_open()
        elif action == 'settings_general':            contextMenu().settings_open(cat=0.0)
        elif action == 'settings_playback':           contextMenu().settings_open(cat=1.0)
        elif action == 'settings_movies':             contextMenu().settings_open(cat=2.0)
        elif action == 'settings_tv':                 contextMenu().settings_open(cat=3.0)
        elif action == 'settings_hostshd':            contextMenu().settings_open(cat=4.0)
        elif action == 'settings_hostssd':            contextMenu().settings_open(cat=5.0)
        elif action == 'settings_accounts':           contextMenu().settings_open(cat=6.1)
        elif action == 'settings_library':            contextMenu().settings_open(cat=7.0)
        elif action == 'settings_downloads':          contextMenu().settings_open(cat=8.0)
        elif action == 'settings_subtitles':          contextMenu().settings_open(cat=9.0)
        elif action == 'favourite_movie_add':         contextMenu().favourite_add('Movie', imdb, name, year, image, refresh=True)
        elif action == 'favourite_movie_from_search': contextMenu().favourite_add('Movie', imdb, name, year, image)
        elif action == 'favourite_tv_add':            contextMenu().favourite_add('TV Show', imdb, name, year, image, refresh=True)
        elif action == 'favourite_tv_from_search':    contextMenu().favourite_add('TV Show', imdb, name, year, image)
        elif action == 'favourite_delete':            contextMenu().favourite_delete(imdb)
        elif action == 'trakt_manager':               contextMenu().trakt_manager('movie', name, imdb)
        elif action == 'trakt_tv_manager':            contextMenu().trakt_manager('show', name, tvdb)
        elif action == 'watched_movies':              contextMenu().playcount_movies(title, year, imdb, 7)
        elif action == 'unwatched_movies':            contextMenu().playcount_movies(title, year, imdb, 6)
        elif action == 'watched_episodes':            contextMenu().playcount_episodes(imdb, tvdb, season, episode, 7)
        elif action == 'unwatched_episodes':          contextMenu().playcount_episodes(imdb, tvdb, season, episode, 6)
        elif action == 'watched_shows':               contextMenu().playcount_shows(name, year, imdb, tvdb, '', 7)
        elif action == 'unwatched_shows':             contextMenu().playcount_shows(name, year, imdb, tvdb, '', 6)
        elif action == 'watched_seasons':             contextMenu().playcount_shows(name, year, imdb, tvdb, season, 7)
        elif action == 'unwatched_seasons':           contextMenu().playcount_shows(name, year, imdb, tvdb, season, 6)
        elif action == 'library_movie_add':           contextMenu().library_movie_add(name, title, year, imdb, url)
        elif action == 'library_movie_list':          contextMenu().library_movie_list(url)
        elif action == 'library_tv_add':              contextMenu().library_tv_add(name, year, imdb, tvdb)
        elif action == 'library_tv_list':             contextMenu().library_tv_list(url)
        elif action == 'library_update_tool':         contextMenu().library_update_tool()
        elif action == 'library_update':              contextMenu().library_update('true')
        elif action == 'library_trakt_collection':    contextMenu().library_movie_tool('trakt_collection')
        elif action == 'library_trakt_watchlist':     contextMenu().library_movie_tool('trakt_watchlist')
        elif action == 'library_imdb_watchlist':      contextMenu().library_movie_tool('imdb_watchlist')
        elif action == 'library_tv_trakt_collection': contextMenu().library_tv_tool('trakt_tv_collection')
        elif action == 'library_tv_trakt_watchlist':  contextMenu().library_tv_tool('trakt_tv_watchlist')
        elif action == 'library_tv_imdb_watchlist':   contextMenu().library_tv_tool('imdb_tv_watchlist')
        elif action == 'toggle_movie_playback':       contextMenu().toggle_playback('movie', name, title, year, imdb, '', '', '', '', '', '', '')
        elif action == 'toggle_episode_playback':     contextMenu().toggle_playback('episode', name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre)
        elif action == 'download':                    contextMenu().download(name, url, provider)
        elif action == 'service':                     contextMenu().service()
        elif action == 'trailer':                     trailer().play(name, url)
        elif action == 'movies':                      movies().get(url)
        elif action == 'movies_userlist':             movies().get(url)
        elif action == 'movies_popular':              movies().popular()
        elif action == 'movies_boxoffice':            movies().boxoffice()
        elif action == 'movies_views':                movies().views()
        elif action == 'movies_oscars':               movies().oscars()
        elif action == 'movies_added_hd':             movies().added_hd()
        elif action == 'movies_added':                movies().added()
        elif action == 'movies_theaters':             movies().theaters()
        elif action == 'movies_trending':             movies().trending()
        elif action == 'movies_featured':             movies().featured()
        elif action == 'movies_trakt_collection':     movies().trakt_collection()
        elif action == 'movies_trakt_watchlist':      movies().trakt_watchlist()
        elif action == 'movies_imdb_watchlist':       movies().imdb_watchlist()
        elif action == 'movies_search':               movies().search(query)
        elif action == 'movies_favourites':           movies().favourites()
        elif action == 'shows':                       shows().get(url)
        elif action == 'shows_userlist':              shows().get(url)
        elif action == 'shows_popular':               shows().popular()
        elif action == 'shows_rating':                shows().rating()
        elif action == 'shows_views':                 shows().views()
        elif action == 'shows_active':                shows().active()
        elif action == 'shows_trending':              shows().trending()
        elif action == 'shows_season_premieres':      shows().season_premieres()
        elif action == 'shows_premieres':             shows().premieres()
        elif action == 'shows_trakt_collection':      shows().trakt_collection()
        elif action == 'shows_trakt_watchlist':       shows().trakt_watchlist()
        elif action == 'shows_imdb_watchlist':        shows().imdb_watchlist()
        elif action == 'shows_search':                shows().search(query)
        elif action == 'shows_favourites':            shows().favourites()
        elif action == 'seasons':                     seasons().get(show, year, imdb, tvdb)
        elif action == 'episodes':                    episodes().get(show, year, imdb, tvdb, season)
        elif action == 'episodes2':                   episodes().get2(show, year, imdb, tvdb, season, episode)
        elif action == 'episodes_calendar_1':         episodes().calendar(1)
        elif action == 'episodes_calendar_2':         episodes().calendar(2)
        elif action == 'episodes_calendar_3':         episodes().calendar(3)
        elif action == 'episodes_calendar_4':         episodes().calendar(4)
        elif action == 'episodes_trakt_progress':     episodes().trakt_progress()
        elif action == 'episodes_trakt':              episodes().trakt_added()
        elif action == 'episodes_added':              episodes().added()
        elif action == 'people_movies':               people().movies(query)
        elif action == 'people_shows':                people().shows(query)
        elif action == 'genres_movies':               genres().movies()
        elif action == 'genres_shows':                genres().shows()
        elif action == 'certificates_movies':         certificates().movies()
        elif action == 'certificates_shows':          certificates().shows()
        elif action == 'languages_movies':            languages().movies()
        elif action == 'years_movies':                years().movies()
        elif action == 'channels_movies':             channels().movies()
        elif action == 'userlists_movies':            userlists().movies()
        elif action == 'userlists_shows':             userlists().shows()
        elif action == 'get_host':                    resolver().get_host(name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, url, meta)
        elif action == 'play_moviehost':              resolver().play_host('movie', name, imdb, tvdb, url, source, provider)
        elif action == 'play_tvhost':                 resolver().play_host('episode', name, imdb, tvdb, url, source, provider)
        elif action == 'play':                        resolver().run(name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, url)

class getUrl(object):
    def __init__(self, url, close=True, proxy=None, post=None, headers=None, mobile=False, referer=None, cookie=None, output='', timeout='10'):
        handlers = []
        if not proxy == None:
            handlers += [urllib2.ProxyHandler({'http':'%s' % (proxy)}), urllib2.HTTPHandler]
            opener = urllib2.build_opener(*handlers)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookies = cookielib.LWPCookieJar()
            handlers += [urllib2.HTTPHandler(), urllib2.HTTPSHandler(), urllib2.HTTPCookieProcessor(cookies)]
            opener = urllib2.build_opener(*handlers)
            opener = urllib2.install_opener(opener)
        try:
            if sys.version_info < (2, 7, 9): raise Exception()
            import ssl; ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            handlers += [urllib2.HTTPSHandler(context=ssl_context)]
            opener = urllib2.build_opener(*handlers)
            opener = urllib2.install_opener(opener)
        except:
            pass
        try: headers.update(headers)
        except: headers = {}
        if 'User-Agent' in headers:
            pass
        elif not mobile == True:
            headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20100101 Firefox/34.0'
        else:
            headers['User-Agent'] = 'Apple-iPhone/701.341'
        if 'referer' in headers:
            pass
        elif referer == None:
            headers['referer'] = url
        else:
            headers['referer'] = referer
        if not 'Accept-Language' in headers:
            headers['Accept-Language'] = 'en-US'
        if 'cookie' in headers:
            pass
        elif not cookie == None:
            headers['cookie'] = cookie
        request = urllib2.Request(url, data=post, headers=headers)
        response = urllib2.urlopen(request, timeout=int(timeout))
        if output == 'cookie':
            result = []
            for c in cookies: result.append('%s=%s' % (c.name, c.value))
            result = "; ".join(result)
        elif output == 'geturl':
            result = response.geturl()
        else:
            result = response.read()
        if close == True:
            response.close()
        self.result = result

class getTrakt:
    def result(self, url, post=None):
        try:
            trakt_key = base64.urlsafe_b64decode(link().trakt_key)
            headers = {'Content-Type': 'application/json', 'trakt-api-key': trakt_key, 'trakt-api-version': '2'}
            if not post == None: post = json.dumps(post)
            if (link().trakt_user == '' or link().trakt_password == ''): pass
            else:
                token = index().cache(self.auth, 24, link().trakt_user, link().trakt_password)
                headers.update({'trakt-user-login': link().trakt_user, 'trakt-user-token': token})
            request = urllib2.Request(url, data=post, headers=headers)
            response = urllib2.urlopen(request, timeout=30)
            result = response.read()
            response.close()
            return result
        except:
            return

    def auth(self, trakt_user, trakt_password):
        try:
            trakt_key = base64.urlsafe_b64decode(link().trakt_key)
            headers = {'Content-Type': 'application/json', 'trakt-api-key': trakt_key, 'trakt-api-version': '2'}
            post = json.dumps({'login': trakt_user, 'password': trakt_password})
            request = urllib2.Request('http://api-v2launch.trakt.tv/auth/login', data=post, headers=headers)
            response = urllib2.urlopen(request, timeout=10)
            result = response.read()
            result = json.loads(result)
            auth = result['token']
            response.close()
            return auth
        except:
            return

    def sync(self, content=''):
        try:
            if content == 'shows': raise Exception()

            url = link().trakt_watched % link().trakt_user
            result = self.result(url)
            r = json.loads(result)
            updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            record = ('movies', link().trakt_user, repr(result), updated)

            dbcon = database.connect(addonCache)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS rel_trakt (""info TEXT, ""user TEXT, ""result TEXT, ""updated TEXT, ""UNIQUE(info, user)"");")
            dbcur.execute("DELETE FROM rel_trakt WHERE info = '%s' AND user = '%s'" % (record[0], record[1]))
            dbcur.execute("INSERT INTO rel_trakt Values (?, ?, ?, ?)", record)
            dbcon.commit()
        except:
            pass

        try:
            if content == 'movies': raise Exception()

            url = link().trakt_tv_watched % link().trakt_user
            url += '?extended=full'
            result = self.result(url)
            r = json.loads(result)
            updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            record = ('shows', link().trakt_user, repr(result), updated)

            dbcon = database.connect(addonCache)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS rel_trakt (""info TEXT, ""user TEXT, ""result TEXT, ""updated TEXT, ""UNIQUE(info, user)"");")
            dbcur.execute("DELETE FROM rel_trakt WHERE info = '%s' AND user = '%s'" % (record[0], record[1]))
            dbcur.execute("INSERT INTO rel_trakt Values (?, ?, ?, ?)", record)
            dbcon.commit()
        except:
            pass

class uniqueList(object):
    def __init__(self, list):
        uniqueSet = set()
        uniqueList = []
        for n in list:
            if n not in uniqueSet:
                uniqueSet.add(n)
                uniqueList.append(n)
        self.list = uniqueList

class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)

class player(xbmc.Player):
    def __init__ (self):
        self.folderPath = xbmc.getInfoLabel('Container.FolderPath')
        self.loadingStarting = time.time()
        xbmc.Player.__init__(self)

    def run(self, content, name, url, imdb, tvdb):
        self.video_info(content, name, imdb, tvdb)
        self.resume_info()

        if self.folderPath.startswith(sys.argv[0]) or PseudoTV == 'True':
            item = xbmcgui.ListItem(path=url)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        else:
            try:
                if self.content == 'movie':
                    meta = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties" : ["title", "originaltitle", "year", "genre", "studio", "country", "runtime", "rating", "votes", "mpaa", "director", "writer", "plot", "plotoutline", "tagline", "thumbnail", "file"]}, "id": 1}' % (self.year, str(int(self.year)+1), str(int(self.year)-1)))
                    meta = unicode(meta, 'utf-8', errors='ignore')
                    meta = json.loads(meta)['result']['movies']
                    self.meta = [i for i in meta if i['file'].endswith(self.file)][0]

                    meta = {'title': self.meta['title'], 'originaltitle': self.meta['originaltitle'], 'year': self.meta['year'], 'genre': str(" / ".join(self.meta['genre'])), 'studio' : str(" / ".join(self.meta['studio'])), 'country' : str(" / ".join(self.meta['country'])), 'duration' : self.meta['runtime'], 'rating': self.meta['rating'], 'votes': self.meta['votes'], 'mpaa': self.meta['mpaa'], 'director': str(" / ".join(self.meta['director'])), 'writer': str(" / ".join(self.meta['writer'])), 'plot': self.meta['plot'], 'plotoutline': self.meta['plotoutline'], 'tagline': self.meta['tagline']}

                    thumb = self.meta['thumbnail']
                    poster = thumb

                elif self.content == 'episode':
                    meta = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "season", "operator": "is", "value": "%s"}, {"field": "episode", "operator": "is", "value": "%s"}]}, "properties": ["title", "season", "episode", "showtitle", "firstaired", "runtime", "rating", "director", "writer", "plot", "thumbnail", "file"]}, "id": 1}' % (self.season, self.episode))
                    meta = unicode(meta, 'utf-8', errors='ignore')
                    meta = json.loads(meta)['result']['episodes']
                    self.meta = [i for i in meta if i['file'].endswith(self.file)][0]

                    meta = {'title': self.meta['title'], 'season' : self.meta['season'], 'episode': self.meta['episode'], 'tvshowtitle': self.meta['showtitle'], 'premiered' : self.meta['firstaired'], 'duration' : self.meta['runtime'], 'rating': self.meta['rating'], 'director': str(" / ".join(self.meta['director'])), 'writer': str(" / ".join(self.meta['writer'])), 'plot': self.meta['plot']}

                    thumb = self.meta['thumbnail']

                    poster = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"filter": {"field": "title", "operator": "is", "value": "%s"}, "properties": ["thumbnail"]}, "id": 1}' % self.meta['showtitle'])
                    poster = unicode(poster, 'utf-8', errors='ignore')
                    poster = json.loads(poster)['result']['tvshows'][0]['thumbnail']

            except:
                poster, thumb, meta = '', '', {'title': self.name}

            item = xbmcgui.ListItem(path=url, iconImage="DefaultVideo.png", thumbnailImage=thumb)
            try: item.setArt({'poster': poster, 'tvshow.poster': poster, 'season.poster': poster})
            except: pass
            item.setInfo(type="Video", infoLabels = meta)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


        for i in range(0, 240):
            if self.isPlayingVideo(): break
            xbmc.sleep(1000)
        while self.isPlayingVideo():
            try: self.totalTime = self.getTotalTime()
            except: pass
            try: self.currentTime = self.getTime()
            except: pass
            xbmc.sleep(1000)
        xbmcgui.Window(10000).clearProperty('script.trakt.ids')
        time.sleep(5)

    def video_info(self, content, name, imdb, tvdb):
        try:
            self.name = name
            self.content = content
            self.totalTime = 0
            self.currentTime = 0
            self.file = self.name + '.strm'
            self.file = self.file.translate(None, '\/:*?"<>|').strip('.')
            self.imdb = re.sub('[^0-9]', '', imdb)
            if tvdb == None: tvdb = '0'
            self.tvdb = tvdb

            if self.content == 'movie':
                self.title, self.year = re.compile('(.+?) [(](\d{4})[)]$').findall(self.name)[0]
                xbmcgui.Window(10000).setProperty('script.trakt.ids', json.dumps({'imdb': 'tt' + self.imdb}))

            elif self.content == 'episode':
                self.show, self.season, self.episode = re.compile('(.+?) S(\d*)E(\d*)$').findall(self.name)[0]
                self.season, self.episode = '%01d' % int(self.season), '%01d' % int(self.episode)
                xbmcgui.Window(10000).setProperty('script.trakt.ids', json.dumps({'tvdb': self.tvdb}))
        except:
            pass

    def resume_info(self):
        try:
            self.offset = '0'
            if PseudoTV == 'True' or not getSetting("resume_playback") == 'true': return

            import hashlib
            n = (hashlib.md5())
            n.update(str(self.name))
            n = str(n.hexdigest())
            i = 'tt' + self.imdb
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM points WHERE name = '%s' AND imdb_id = '%s'" % (n, i))
            match = dbcur.fetchone()
            self.offset = str(match[2])
            dbcon.commit()
        except:
            pass

        try:
            if self.offset == '0': return

            minutes, seconds = divmod(float(self.offset), 60)
            hours, minutes = divmod(minutes, 60)
            offset_time = '%02d:%02d:%02d' % (hours, minutes, seconds)

            yes = index().yesnoDialog('%s %s' % (language(30342).encode("utf-8"), offset_time), '', self.name, language(30343).encode("utf-8"), language(30344).encode("utf-8"))
            if not yes: self.offset = '0'
        except:
            pass

    def change_watched(self):
        if self.content == 'movie':
            try:
                if self.folderPath.startswith(sys.argv[0]): raise Exception()
                xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid" : %s, "playcount" : 1 }, "id": 1 }' % str(self.meta['movieid']))
                index().container_refresh()
            except:
                pass

            try:
                if not self.folderPath.startswith(sys.argv[0]): raise Exception()
                from metahandler import metahandlers
                metaget = metahandlers.MetaData(preparezip=False)
                metaget.get_meta('movie', self.title ,year=self.year)
                metaget.change_watched(self.content, '', self.imdb, season='', episode='', year='', watched=7)
            except:
                pass

            try:
                try: trakt_script_scrobble = xbmcaddon.Addon('script.trakt').getSetting("scrobble_movie")
                except: trakt_script_scrobble = ''
                try: trakt_script_http = xbmcaddon.Addon('script.trakt').getSetting("ExcludeHTTP")
                except: trakt_script_http = ''
                try: trakt_script_auth = xbmcaddon.Addon('script.trakt').getSetting("authorization")
                except: trakt_script_auth = ''

                if trakt_script_scrobble == 'true' and trakt_script_http == 'false' and not trakt_script_auth == '': raise Exception()

                imdb = self.imdb
                if not imdb.startswith('tt'): imdb = 'tt' + imdb
                if (link().trakt_user == '' or link().trakt_password == ''): raise Exception()
                getTrakt().result(link().trakt_history, post={"movies": [{"ids": {"imdb": imdb}}]})
            except:
                pass

            try:
                if (link().trakt_user == '' or link().trakt_password == ''): raise Exception()
                getTrakt().sync('movies')
            except:
                pass

        elif self.content == 'episode':
            try:
                if self.folderPath.startswith(sys.argv[0]): raise Exception()
                xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid" : %s, "playcount" : 1 }, "id": 1 }' % str(self.meta['episodeid']))
                index().container_refresh()
            except:
                pass

            try:
                if not self.folderPath.startswith(sys.argv[0]): raise Exception()
                from metahandler import metahandlers
                metaget = metahandlers.MetaData(preparezip=False)
                metaget.get_meta('tvshow', self.show, imdb_id=self.imdb)
                metaget.get_episode_meta(self.show, self.imdb, self.season, self.episode)
                metaget.change_watched(self.content, '', self.imdb, season=self.season, episode=self.episode, year='', watched=7)
            except:
                pass

            try:
                try: trakt_script_scrobble = xbmcaddon.Addon('script.trakt').getSetting("scrobble_episode")
                except: trakt_script_scrobble = ''
                try: trakt_script_http = xbmcaddon.Addon('script.trakt').getSetting("ExcludeHTTP")
                except: trakt_script_http = ''
                try: trakt_script_auth = xbmcaddon.Addon('script.trakt').getSetting("authorization")
                except: trakt_script_auth = ''

                if trakt_script_scrobble == 'true' and trakt_script_http == 'false' and not trakt_script_auth == '': raise Exception()

                season, episode = int('%01d' % int(self.season)), int('%01d' % int(self.episode))
                if (link().trakt_user == '' or link().trakt_password == ''): raise Exception()
                getTrakt().result(link().trakt_history, post={"shows": [{"seasons": [{"episodes": [{"number": episode}], "number": season}], "ids": {"tvdb": self.tvdb}}]})
            except:
                pass

            try:
                if (link().trakt_user == '' or link().trakt_password == ''): raise Exception()
                getTrakt().sync('shows')
            except:
                pass

    def onPlayBackStarted(self):
        try:
			if self.offset == '0': raise Exception()
			seekTime = float(self.offset)
			self.seekTime(seekTime)
        except:
			pass

        try:
            if self.getSubtitles(): raise Exception()
            try: path = self.getPlayingFile()
            except: path = ''
            if self.content == 'movie':
                self.subtitle = subtitles().get(self.name, path, self.imdb, '', '')
            elif self.content == 'episode':
                self.subtitle = subtitles().get(self.name, path, self.imdb, self.season, self.episode)
            self.setSubtitles(self.subtitle)
        except:
			pass

        if getSetting("playback_info") == 'true' and not PseudoTV == 'True':
            elapsedTime = '%s %s seconds' % (language(30309).encode("utf-8"), int((time.time() - self.loadingStarting)))     
            index().infoDialog(elapsedTime, header=self.name)

    def onPlayBackStopped(self):
        if PseudoTV == 'True': return

        try:
            import hashlib
            n = (hashlib.md5())
            n.update(str(self.name))
            n = str(n.hexdigest())
            i = 'tt' + self.imdb
            r = str(self.currentTime)
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS points (""name TEXT, ""imdb_id TEXT, ""resume_point TEXT, ""UNIQUE(name, imdb_id)"");")
            dbcur.execute("DELETE FROM points WHERE name = '%s' AND imdb_id = '%s'" % (n, i))
            ok = int(self.currentTime) > 180 and (self.currentTime / self.totalTime) <= .92
            if ok: dbcur.execute("INSERT INTO points Values (?, ?, ?)", (n, i, r))
            dbcon.commit()
        except:
            pass

        try:
            ok = self.currentTime / self.totalTime >= .9
            if ok: self.change_watched()
        except:
            pass

    def onPlayBackEnded(self):
        if PseudoTV == 'True': return

        try:
            import hashlib
            n = (hashlib.md5())
            n.update(str(self.name))
            n = str(n.hexdigest())
            i = 'tt' + self.imdb
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS points (""name TEXT, ""imdb_id TEXT, ""resume_point TEXT, ""UNIQUE(name, imdb_id)"");")
            dbcur.execute("DELETE FROM points WHERE name = '%s' AND imdb_id = '%s'" % (n, i))
            dbcon.commit()
        except:
            pass

        try:
            self.change_watched()
        except:
            pass

class subtitles:
    def get(self, name, path, imdb, season, episode):
        if not getSetting("subtitles") == 'true': return
        moviequality = []
        quality = ['bluray', 'hdrip', 'brrip', 'bdrip', 'dvdrip', 'webrip', 'hdtv']
        langDict = {'Afrikaans': 'afr', 'Albanian': 'alb', 'Arabic': 'ara', 'Armenian': 'arm', 'Basque': 'baq', 'Bengali': 'ben', 'Bosnian': 'bos', 'Breton': 'bre', 'Bulgarian': 'bul', 'Burmese': 'bur', 'Catalan': 'cat', 'Chinese': 'chi', 'Croatian': 'hrv', 'Czech': 'cze', 'Danish': 'dan', 'Dutch': 'dut', 'English': 'eng', 'Esperanto': 'epo', 'Estonian': 'est', 'Finnish': 'fin', 'French': 'fre', 'Galician': 'glg', 'Georgian': 'geo', 'German': 'ger', 'Greek': 'ell', 'Hebrew': 'heb', 'Hindi': 'hin', 'Hungarian': 'hun', 'Icelandic': 'ice', 'Indonesian': 'ind', 'Italian': 'ita', 'Japanese': 'jpn', 'Kazakh': 'kaz', 'Khmer': 'khm', 'Korean': 'kor', 'Latvian': 'lav', 'Lithuanian': 'lit', 'Luxembourgish': 'ltz', 'Macedonian': 'mac', 'Malay': 'may', 'Malayalam': 'mal', 'Manipuri': 'mni', 'Mongolian': 'mon', 'Montenegrin': 'mne', 'Norwegian': 'nor', 'Occitan': 'oci', 'Persian': 'per', 'Polish': 'pol', 'Portuguese': 'por,pob', 'Portuguese(Brazil)': 'pob,por', 'Romanian': 'rum', 'Russian': 'rus', 'Serbian': 'scc', 'Sinhalese': 'sin', 'Slovak': 'slo', 'Slovenian': 'slv', 'Spanish': 'spa', 'Swahili': 'swa', 'Swedish': 'swe', 'Syriac': 'syr', 'Tagalog': 'tgl', 'Tamil': 'tam', 'Telugu': 'tel', 'Thai': 'tha', 'Turkish': 'tur', 'Ukrainian': 'ukr', 'Urdu': 'urd'}
        for q in quality: 
            if q in path.lower():
				try: moviequality.append(q)
				except: pass

        langs = []
        try: langs.append(langDict[getSetting("sublang1")])
        except: pass
        try: langs.append(langDict[getSetting("sublang2")])
        except: pass
        langs = ','.join(langs)

        try:
            import xmlrpclib
            server = xmlrpclib.Server('http://api.opensubtitles.org/xml-rpc', verbose=0)
            token = server.LogIn('', '', 'en', 'XBMC_Subtitles_v1')['token']
            if not (season == '' or episode == ''): result = server.SearchSubtitles(token, [{'sublanguageid': langs, 'imdbid': imdb, 'season': season, 'episode': episode}])['data']
            else: result = server.SearchSubtitles(token, [{'sublanguageid': langs, 'imdbid': imdb}])['data']
            result = [i for i in result if i['SubSumCD'] == '1']
        except: return

        subtitles = []
        if moviequality <> []:
            for lang in langs.split(','):
                filter = [i for i in result if lang == i['SubLanguageID']]
                if filter == []: continue
                for q in moviequality: subtitles += [i for i in filter if q in i['MovieReleaseName'].lower()]
                if subtitles <> []:
                	try: lang = xbmc.convertLanguage(lang, xbmc.ISO_639_1)
                	except: pass
                	break
        if subtitles == []:
            for lang in langs.split(','):
                filter = [i for i in result if lang == i['SubLanguageID']]
                if filter == []: continue
                for q in quality: subtitles += [i for i in filter if q in i['MovieReleaseName'].lower()]
                subtitles += [i for i in filter if not any(x in i['MovieReleaseName'].lower() for x in quality)]
                try: lang = xbmc.convertLanguage(lang, xbmc.ISO_639_1)
                except: pass
                break

        try:
            import zlib, base64
            content = [subtitles[0]["IDSubtitleFile"],]
            content = server.DownloadSubtitles(token, content)
            content = base64.b64decode(content['data'][0]['data'])
            content = zlib.decompressobj(16+zlib.MAX_WBITS).decompress(content)

            subtitle = xbmc.translatePath('special://temp/')
            subtitle = os.path.join(subtitle, 'TemporarySubs.%s.srt' % lang)
            file = open(subtitle, 'wb')
            file.write(content)
            file.close()

            return subtitle
        except:
            index().infoDialog(language(30307).encode("utf-8"), name)
            return

class index:
    def infoDialog(self, str, header=addonName, time=3000):
        try: xbmcgui.Dialog().notification(header, str, self.addonArt('icon.png'), time, sound=False)
        except: xbmc.executebuiltin("Notification(%s,%s, %s, %s)" % (header, str, time, self.addonArt('icon.png')))

    def okDialog(self, str1, str2, header=addonName):
        xbmcgui.Dialog().ok(header, str1, str2)

    def selectDialog(self, list, header=addonName):
        select = xbmcgui.Dialog().select(header, list)
        return select

    def yesnoDialog(self, str1, str2, header=addonName, str3='', str4=''):
        answer = xbmcgui.Dialog().yesno(header, str1, str2, '', str4, str3)
        return answer

    def getProperty(self, str):
        property = xbmcgui.Window(10000).getProperty(str)
        return property

    def setProperty(self, str1, str2):
        xbmcgui.Window(10000).setProperty(str1, str2)

    def clearProperty(self, str):
        xbmcgui.Window(10000).clearProperty(str)

    def addon_status(self, id):
        check = xbmcaddon.Addon(id=id).getAddonInfo("name")
        if not check == addonName: return True

    def container_refresh(self):
        xbmc.executebuiltin('Container.Refresh')

    def container_data(self):
        if not xbmcvfs.exists(dataPath):
            xbmcvfs.mkdir(dataPath)

    def container_view(self, content, viewDict):
        try:
            skin = xbmc.getSkinDir()
            record = (skin, content)
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM views WHERE skin = '%s' AND view_type = '%s'" % (record[0], record[1]))
            view = dbcur.fetchone()
            view = view[2]
            if view == None: raise Exception()
            xbmc.executebuiltin('Container.SetViewMode(%s)' % str(view))
        except:
            try:
                id = str(viewDict[skin])
                xbmc.executebuiltin('Container.SetViewMode(%s)' % id)
            except:
                pass

    def cache(self, function, timeout, *args):
        try:
            response = None

            f = repr(function)
            f = re.sub('.+\smethod\s|.+function\s|\sat\s.+|\sof\s.+', '', f)

            import hashlib
            a = hashlib.md5()
            for i in args: a.update(str(i))
            a = str(a.hexdigest())
        except:
            pass

        try:
            dbcon = database.connect(addonCache)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM rel_list WHERE func = '%s' AND args = '%s'" % (f, a))
            match = dbcur.fetchone()

            response = eval(match[2].encode('utf-8'))

            t1 = int(re.sub('[^0-9]', '', str(match[3])))
            t2 = int(datetime.datetime.now().strftime("%Y%m%d%H%M"))
            update = abs(t2 - t1) >= int(timeout*60)
            if update == False:
                return response
        except:
            pass

        try:
            r = function(*args)
            if (r == None or r == []) and not response == None:
                return response
            elif (r == None or r == []):
                return r
        except:
            return

        try:
            r = repr(r)
            t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            dbcur.execute("CREATE TABLE IF NOT EXISTS rel_list (""func TEXT, ""args TEXT, ""response TEXT, ""added TEXT, ""UNIQUE(func, args)"");")
            dbcur.execute("DELETE FROM rel_list WHERE func = '%s' AND args = '%s'" % (f, a))
            dbcur.execute("INSERT INTO rel_list Values (?, ?, ?, ?)", (f, a, r, t))
            dbcon.commit()
        except:
            pass

        try:
            return eval(r.encode('utf-8'))
        except:
            pass

    def cache_clear_list(self):
        try:
            yes = index().yesnoDialog(language(30341).encode("utf-8"), '')
            if not yes: return

            dbcon = database.connect(addonCache)
            dbcur = dbcon.cursor()
            dbcur.execute("DROP TABLE IF EXISTS rel_list")
            dbcur.execute("VACUUM")
            dbcon.commit()
            dbcur.execute("DROP TABLE IF EXISTS rel_lib")
            dbcur.execute("VACUUM")
            dbcon.commit()

            index().infoDialog(language(30306).encode("utf-8"))
        except:
            pass

    def cache_clear_src(self):
        try:
            yes = index().yesnoDialog(language(30341).encode("utf-8"), '')
            if not yes: return

            dbcon = database.connect(addonSources)
            dbcur = dbcon.cursor()
            dbcur.execute("DROP TABLE IF EXISTS rel_src")
            dbcur.execute("VACUUM")
            dbcon.commit()

            index().infoDialog(language(30306).encode("utf-8"))
        except:
            pass

    def addonArt(self, image, root=''):
        if image.startswith('http://'):
            pass
        elif getSetting("appearance") == '-':
            if image == 'fanart.jpg': image = '-'
            elif image == 'icon.png': image = os.path.join(addonPath,'icon.png')
            elif root == 'episodes_added' or root == 'episodes_trakt_progress' or root == 'episodes_trakt': image = 'DefaultRecentlyAddedEpisodes.png'
            elif root == 'movies_added_hd' or root == 'movies_added': image = 'DefaultRecentlyAddedMovies.png'
            elif root == 'root_genesis': image = 'DefaultVideoPlaylists.png'
            elif root == 'root_tools': image = 'DefaultAddonProgram.png'
            elif root.startswith('movies') or root.endswith('_movies'): image = 'DefaultMovies.png'
            elif image == 'movie_poster.png': image = 'DefaultMovies.png'
            elif root.startswith('shows') or root.endswith('_shows'): image = 'DefaultTVShows.png'
            elif image == 'tv_poster.png' or image == 'tv_banner.png': image = 'DefaultTVShows.png'
            elif root.startswith('episodes') or root.endswith('_episodes'): image = 'DefaultTVShows.png'
            elif image == 'tv_thumb.png': image = 'DefaultTVShows.png'
            else: image = 'DefaultFolder.png'
        else:
            art = os.path.join(addonPath, 'resources/art')
            art = os.path.join(art, getSetting("appearance").lower().replace(' ', ''))
            image = os.path.join(art, image)

        return image

    def rootList(self, rootList):
        if rootList == None or len(rootList) == 0: return

        addonFanart = self.addonArt('fanart.jpg')

        total = len(rootList)

        for i in rootList:
            try:
                try: name = language(i['name']).encode("utf-8")
                except: name = i['name']

                root = i['action']

                image = self.addonArt(i['image'], root)

                u = '%s?action=%s' % (sys.argv[0], root)
                try: u += '&url=%s' % urllib.quote_plus(i['url'])
                except: pass
                if root == 'downloads_movies':
                    u = xbmc.translatePath(getSetting("movie_downloads"))
                    if len(xbmcvfs.listdir(u)[0]) == 0: raise Exception()
                if root == 'downloads_shows':
                    u = xbmc.translatePath(getSetting("tv_downloads"))
                    if len(xbmcvfs.listdir(u)[0]) == 0: raise Exception()
                elif root == 'library_movies':
                    u = movieLibrary
                    if len(xbmcvfs.listdir(u)[0]) == 0: raise Exception()
                elif root == 'library_shows':
                    u = tvLibrary
                    if len(xbmcvfs.listdir(u)[0]) == 0: raise Exception()

                cm = []
                replaceItems = False

                if root == 'movies_userlist':
                    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=library_movie_list&url=%s)' % (sys.argv[0], urllib.quote_plus(i['url']))))
                elif root == 'movies_trakt_collection':
                    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=library_movie_list&url=%s)' % (sys.argv[0], urllib.quote_plus(link().trakt_collection % link().trakt_user))))
                elif root == 'movies_trakt_watchlist':
                    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=library_movie_list&url=%s)' % (sys.argv[0], urllib.quote_plus(link().trakt_watchlist % link().trakt_user))))
                elif root == 'movies_imdb_watchlist':
                    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=library_movie_list&url=%s)' % (sys.argv[0], urllib.quote_plus(link().imdb_watchlist % link().imdb_user))))
                elif root == 'shows_userlist':
                    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=library_tv_list&url=%s)' % (sys.argv[0], urllib.quote_plus(i['url']))))
                elif root == 'shows_trakt_collection':
                    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=library_tv_list&url=%s)' % (sys.argv[0], urllib.quote_plus(link().trakt_tv_collection % link().trakt_user))))
                elif root == 'shows_trakt_watchlist':
                    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=library_tv_list&url=%s)' % (sys.argv[0], urllib.quote_plus(link().trakt_tv_watchlist % link().trakt_user))))
                elif root == 'shows_imdb_watchlist':
                    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=library_tv_list&url=%s)' % (sys.argv[0], urllib.quote_plus(link().imdb_watchlist % link().imdb_user))))

                if root == 'movies_search' or root == 'shows_search' or root == 'people_movies' or root == 'people_shows':
                    cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    replaceItems = True

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo(type="Video", infoLabels={"Label": name, "Title": name, "Plot": addonDesc})
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=replaceItems)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

    def channelList(self, channelList):
        if channelList == None or len(channelList) == 0: return

        addonFanart = self.addonArt('fanart.jpg')

        playbackMenu = language(30408).encode("utf-8")
        if getSetting("autoplay") == 'true': playbackMenu = language(30409).encode("utf-8")

        total = len(channelList)
        for i in channelList:
            try:
                channel, title, year, imdb, genre, url, poster, fanart, studio, duration, rating, votes, mpaa, director, plot, plotoutline, tagline = i['name'], i['title'], i['year'], i['imdb'], i['genre'], i['url'], i['poster'], i['fanart'], i['studio'], i['duration'], i['rating'], i['votes'], i['mpaa'], i['director'], i['plot'], i['plotoutline'], i['tagline']

                if fanart == '0' or not getSetting("fanart") == 'true': fanart = addonFanart

                thumb = '%s/%s.png' % (addonLogos, channel)
                name = '%s (%s)' % (title, year)
                label = "[B]%s[/B] : %s" % (channel.upper(), name)

                sysname, systitle, sysyear, sysimdb, sysurl = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(url)

                meta = {'title': title, 'year': year, 'imdb_id' : 'tt' + imdb, 'genre' : genre, 'poster' : poster, 'fanart' : fanart, 'studio' : studio, 'duration' : duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'plot': plot, 'plotoutline': plotoutline, 'tagline': tagline}
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')

                u = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s&url=%s&t=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, sysurl, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))

                cm = []
                cm.append((playbackMenu, 'RunPlugin(%s?action=toggle_movie_playback&name=%s&title=%s&imdb=%s&year=%s)' % (sys.argv[0], sysname, systitle, sysimdb, sysyear)))

                item = xbmcgui.ListItem(label, iconImage=thumb, thumbnailImage=thumb)
                try: item.setArt({'poster': thumb, 'banner': thumb})
                except: pass
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.setProperty("IsPlayable", "true")
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)

    def movieList(self, movieList):
        if movieList == None or len(movieList) == 0: return

        addonPoster = self.addonArt('movie_poster.png')
        addonFanart = self.addonArt('fanart.jpg')

        video_type = 'true'
        if getSetting("autoplay") == 'false' and getSetting("host_select") == '1': video_type = 'false'
        if PseudoTV == 'True': video_type = 'true'

        playbackMenu = language(30408).encode("utf-8")
        if getSetting("autoplay") == 'true': playbackMenu = language(30409).encode("utf-8")

        if (getSetting("trakt_user") == '' or getSetting("trakt_password") == ''): traktMode = False
        else: traktMode = True

        cacheToDisc = False
        if action == 'movies_search': cacheToDisc = True

        try:
            favourites = []
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='Movie'")
            favourites = dbcur.fetchall()
            favourites = [i[0] for i in favourites]
            favourites = [re.sub('[^0-9]', '', i) for i in favourites]
        except:
            pass

        try:
            if traktMode == True: raise Exception()
            from metahandler import metahandlers
            metaget = metahandlers.MetaData(preparezip=False)
        except:
            pass

        try:
            if traktMode == False: raise Exception()
            record = ('movies', getSetting("trakt_user"))
            dbcon = database.connect(addonCache)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM rel_trakt WHERE info = '%s' AND user = '%s'" % (record[0], record[1]))
            indicators = dbcur.fetchone()
            indicators = indicators[2]
            indicators = eval(indicators.encode('utf-8'))
            indicators = json.loads(indicators)
        except:
            pass

        total = len(movieList)
        t = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        for i in movieList:
            try:
                name, title, year, imdb, genre, url, poster, fanart, studio, duration, rating, votes, mpaa, director, plot, plotoutline, tagline = i['name'], i['title'], i['year'], i['imdb'], i['genre'], i['url'], i['poster'], i['fanart'], i['studio'], i['duration'], i['rating'], i['votes'], i['mpaa'], i['director'], i['plot'], i['plotoutline'], i['tagline']

                if poster == '0': poster = addonPoster
                if fanart == '0' or not getSetting("fanart") == 'true': fanart = addonFanart
                if duration == '0': duration == '120'

                sysname, systitle, sysyear, sysimdb, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(url), urllib.quote_plus(poster)

                meta = {'title': title, 'year': year, 'imdb_id' : 'tt' + imdb, 'genre' : genre, 'poster' : poster, 'fanart' : fanart, 'studio' : studio, 'duration' : duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'plot': plot, 'plotoutline': plotoutline, 'tagline': tagline, 'trailer': '%s?action=trailer&name=%s' % (sys.argv[0], sysname)}
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')
                sysmeta = urllib.quote_plus(json.dumps(meta))

                if video_type == 'true':
                    u = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s&url=%s&t=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, sysurl, t)
                    isFolder = False
                else:
                    u = '%s?action=get_host&name=%s&title=%s&year=%s&imdb=%s&url=%s&meta=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, sysurl, sysmeta)
                    isFolder = True

                try:
                    if traktMode == True: raise Exception()
                    playcount = metaget._get_watched('movie', 'tt' + imdb, '', '')
                    if playcount == 7: meta.update({'playcount': 1, 'overlay': 7})
                    else: meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass
                try:
                    if traktMode == False: raise Exception()
                    playcount = [i for i in indicators if str(i['movie']['ids']['imdb']) == 'tt' + imdb][0]
                    meta.update({'playcount': 1, 'overlay': 7})
                except:
                    pass

                cm = []
                cm.append((playbackMenu, 'RunPlugin(%s?action=toggle_movie_playback&name=%s&title=%s&year=%s&imdb=%s)' % (sys.argv[0], sysname, systitle, sysyear, sysimdb)))
                if not (getSetting("trakt_user") == '' or getSetting("trakt_password") == ''):
                    cm.append((language(30419).encode("utf-8"), 'RunPlugin(%s?action=trakt_manager&name=%s&imdb=%s)' % (sys.argv[0], sysname, sysimdb)))
                if action == 'movies_favourites':
                    cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&imdb=%s)' % (sys.argv[0], sysimdb)))
                elif action == 'movies_search':
                    cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=favourite_movie_from_search&imdb=%s&name=%s&year=%s&image=%s)' % (sys.argv[0], sysimdb, systitle, sysyear, sysimage)))
                else:
                    if not imdb in favourites: cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=favourite_movie_add&imdb=%s&name=%s&year=%s&image=%s)' % (sys.argv[0], sysimdb, systitle, sysyear, sysimage)))
                    else: cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&imdb=%s)' % (sys.argv[0], sysimdb)))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=library_movie_add&name=%s&title=%s&year=%s&imdb=%s&url=%s)' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, sysurl)))
                cm.append((language(30412).encode("utf-8"), 'Action(Info)'))
                if not imdb == '0000000' and not action == 'movies_search':
                    cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=unwatched_movies&title=%s&year=%s&imdb=%s)' % (sys.argv[0], systitle, sysyear, sysimdb)))
                if not imdb == '0000000' and not action == 'movies_search':
                    cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=watched_movies&title=%s&year=%s&imdb=%s)' % (sys.argv[0], systitle, sysyear, sysimdb)))
                cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))

                item = xbmcgui.ListItem(label=name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                try: item.setArt({'poster': poster, 'banner': poster})
                except: pass
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.setProperty("IsPlayable", "true")
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=isFolder)
            except:
                pass

        try:
            next = movieList[0]['next']
            if next == '': raise Exception()
            name, url, image = language(30381).encode("utf-8"), next, self.addonArt('item_next.jpg')
            if getSetting("appearance") == '-': image = 'DefaultFolder.png'
            u = '%s?action=movies&url=%s' % (sys.argv[0], urllib.quote_plus(url))
            item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
            item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
            item.setProperty("Fanart_Image", addonFanart)
            item.addContextMenuItems([], replaceItems=False)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)
        except:
            pass

        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=cacheToDisc)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(movies)'):
                return index().container_view('movies', {'skin.confluence' : 500})
            xbmc.sleep(100)

    def showList(self, showList):
        if showList == None or len(showList) == 0: return

        addonPoster = self.addonArt('tv_poster.png')
        addonBanner = self.addonArt('tv_banner.png')
        addonFanart = self.addonArt('fanart.jpg')

        video_type = 'true'
        if getSetting("autoplay") == 'false' and getSetting("host_select") == '1': video_type = 'false'
        if PseudoTV == 'True': video_type = 'true'

        if (getSetting("trakt_user") == '' or getSetting("trakt_password") == ''): traktMode = False
        else: traktMode = True

        try:
            favourites = []
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='TV Show'")
            favourites = dbcur.fetchall()
            favourites = [i[0] for i in favourites]
            favourites = [re.sub('[^0-9]', '', i) for i in favourites]
        except:
            pass

        try:
            if traktMode == False: raise Exception()
            record = ('shows', getSetting("trakt_user"))
            dbcon = database.connect(addonCache)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM rel_trakt WHERE info = '%s' AND user = '%s'" % (record[0], record[1]))
            indicators = dbcur.fetchone()
            indicators = indicators[2]
            indicators = eval(indicators.encode('utf-8'))
            indicators = json.loads(indicators)
        except:
            pass

        total = len(showList)
        for i in showList:
            try:
                name, title, year, imdb, tvdb, genre, url, poster, banner, fanart, studio, premiered, duration, rating, mpaa, plot = i['title'],  i['title'], i['year'], i['imdb'], i['tvdb'], i['genre'], i['url'], i['poster'], i['banner'], i['fanart'], i['studio'], i['premiered'], i['duration'], i['rating'], i['mpaa'], i['plot']

                if poster == '0': poster = addonPoster
                if banner == '0': banner = addonBanner
                if fanart == '0' or not getSetting("fanart") == 'true': fanart = addonFanart
                if duration == '0': duration == '60'

                systitle, sysyear, sysimdb, systvdb, sysurl, sysimage = urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(url), urllib.quote_plus(poster)

                meta = {'title': title, 'tvshowtitle': title, 'year': year, 'imdb_id' : 'tt' + imdb, 'tvdb_id': tvdb, 'genre' : genre, 'studio': studio, 'premiered': premiered, 'duration' : duration, 'rating' : rating, 'mpaa' : mpaa, 'plot': plot, 'trailer': '%s?action=trailer&name=%s' % (sys.argv[0], systitle)}
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')

                u = '%s?action=seasons&show=%s&year=%s&imdb=%s&tvdb=%s' % (sys.argv[0], systitle, sysyear, sysimdb, systvdb)

                try:
                    if traktMode == False: raise Exception()
                    match = [i for i in indicators if str(i['show']['ids']['tvdb']) == tvdb][0]
                    num_1 = 0
                    for i in range(0, len(match['seasons'])): num_1 += len(match['seasons'][i]['episodes'])
                    num_2 = int(match['show']['aired_episodes'])
                    if num_1 >= num_2: meta.update({'playcount': 1, 'overlay': 7})
                except:
                    pass

                cm = []
                if video_type == 'true':
                    cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                if not (getSetting("trakt_user") == '' or getSetting("trakt_password") == ''):
                    cm.append((language(30419).encode("utf-8"), 'RunPlugin(%s?action=trakt_tv_manager&name=%s&tvdb=%s)' % (sys.argv[0], systitle, systvdb)))
                if action == 'shows_favourites':
                    cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&imdb=%s)' % (sys.argv[0], sysimdb))) 
                elif action.startswith('shows_search'):
                    cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=favourite_tv_from_search&imdb=%s&name=%s&year=%s&image=%s)' % (sys.argv[0], sysimdb, systitle, sysyear, sysimage)))
                else:
                    if not imdb in favourites: cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=favourite_tv_add&imdb=%s&name=%s&year=%s&image=%s)' % (sys.argv[0], sysimdb, systitle, sysyear, sysimage)))
                    else: cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&imdb=%s)' % (sys.argv[0], sysimdb)))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=library_tv_add&name=%s&year=%s&imdb=%s&tvdb=%s)' % (sys.argv[0], systitle, sysyear, sysimdb, systvdb)))
                cm.append((language(30413).encode("utf-8"), 'Action(Info)'))
                if not imdb == '0000000' and not action == 'shows_search':
                    cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=unwatched_shows&name=%s&year=%s&imdb=%s&tvdb=%s)' % (sys.argv[0], systitle, sysyear, sysimdb, systvdb)))
                    cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=watched_shows&name=%s&year=%s&imdb=%s&tvdb=%s)' % (sys.argv[0], systitle, sysyear, sysimdb, systvdb)))
                cm.append((language(30416).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                try: item.setArt({'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})
                except: pass
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

        try:
            next = showList[0]['next']
            if next == '': raise Exception()
            name, url, image = language(30381).encode("utf-8"), next, self.addonArt('item_next.jpg')
            if getSetting("appearance") == '-': image = 'DefaultFolder.png'
            u = '%s?action=shows&url=%s' % (sys.argv[0], urllib.quote_plus(url))
            item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
            item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
            item.setProperty("Fanart_Image", addonFanart)
            item.addContextMenuItems([], replaceItems=False)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)
        except:
            pass

        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(tvshows)'):
                return index().container_view('tvshows', {'skin.confluence' : 500})
            xbmc.sleep(100)

    def seasonList(self, seasonList):
        if seasonList == None or len(seasonList) == 0: return

        addonPoster = self.addonArt('tv_poster.png')
        addonBanner = self.addonArt('tv_banner.png')
        addonThumb = self.addonArt('tv_thumb.png')
        addonFanart = self.addonArt('fanart.jpg')

        video_type = 'true'
        if getSetting("autoplay") == 'false' and getSetting("host_select") == '1': video_type = 'false'
        if PseudoTV == 'True': video_type = 'true'

        try:
            favourites = []
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='TV Show'")
            favourites = dbcur.fetchall()
            favourites = [i[0] for i in favourites]
            favourites = [re.sub('[^0-9]', '', i) for i in favourites]
        except:
            pass

        total = len(seasonList)
        for i in seasonList:
            try:
                title, year, imdb, tvdb, season, show, show_alt, genre, url, poster, banner, thumb, fanart, studio, status, premiered, duration, rating, mpaa, plot = 'Season ' + i['title'], i['year'], i['imdb'], i['tvdb'], i['season'], i['show'], i['show_alt'], i['genre'], i['url'], i['poster'], i['banner'], i['thumb'], i['fanart'], i['studio'], i['status'], i['date'], i['duration'], i['rating'], i['mpaa'], i['plot']

                if poster == '0': poster = addonPoster
                if banner == '0': banner = addonBanner
                if thumb == '0': thumb = addonThumb
                if fanart == '0' or not getSetting("fanart") == 'true': fanart = addonFanart
                if duration == '0': duration == '60'

                sysyear, sysimdb, systvdb, sysseason, sysshow, sysurl, sysimage = urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(season), urllib.quote_plus(show), urllib.quote_plus(url), urllib.quote_plus(poster)

                meta = {'title': title, 'year': year, 'imdb_id' : 'tt' + imdb, 'tvdb_id' : tvdb, 'season' : season, 'tvshowtitle': show, 'genre' : genre, 'studio': studio, 'status': status, 'premiered' : premiered, 'duration' : duration, 'rating': rating, 'mpaa' : mpaa, 'plot': plot, 'trailer': '%s?action=trailer&name=%s' % (sys.argv[0], sysshow)}
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')

                u = '%s?action=episodes&show=%s&year=%s&imdb=%s&tvdb=%s&season=%s' % (sys.argv[0], sysshow, sysyear, sysimdb, systvdb, sysseason)

                cm = []
                if video_type == 'true':
                    cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                if not (getSetting("trakt_user") == '' or getSetting("trakt_password") == ''):
                    cm.append((language(30419).encode("utf-8"), 'RunPlugin(%s?action=trakt_tv_manager&name=%s&tvdb=%s)' % (sys.argv[0], sysshow, systvdb)))
                if not imdb in favourites: cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=favourite_tv_add&imdb=%s&name=%s&year=%s&image=%s)' % (sys.argv[0], sysimdb, sysshow, sysyear, sysimage)))
                else: cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&imdb=%s)' % (sys.argv[0], sysimdb)))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=library_tv_add&name=%s&year=%s&imdb=%s&tvdb=%s)' % (sys.argv[0], sysshow, sysyear, sysimdb, systvdb)))
                cm.append((language(30413).encode("utf-8"), 'Action(Info)'))
                if not imdb == '0000000':
                    cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=unwatched_seasons&name=%s&year=%s&imdb=%s&tvdb=%s&season=%s)' % (sys.argv[0], sysshow, sysyear, sysimdb, systvdb, sysseason)))
                if not imdb == '0000000':
                    cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=watched_seasons&name=%s&year=%s&imdb=%s&tvdb=%s&season=%s)' % (sys.argv[0], sysshow, sysyear, sysimdb, systvdb, sysseason)))
                cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=view_seasons)' % (sys.argv[0])))

                item = xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=thumb)
                try: item.setArt({'poster': thumb, 'tvshow.poster': poster, 'season.poster': thumb, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})
                except: pass
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

        xbmcplugin.setProperty(int(sys.argv[1]), 'showplot', plot)

        xbmcplugin.setContent(int(sys.argv[1]), 'seasons')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(seasons)'):
                return index().container_view('seasons', {'skin.confluence' : 500})
            xbmc.sleep(100)

    def episodeList(self, episodeList):
        if episodeList == None or len(episodeList) == 0: return

        addonPoster = self.addonArt('tv_poster.png')
        addonBanner = self.addonArt('tv_banner.png')
        addonThumb = self.addonArt('tv_thumb.png')
        addonFanart = self.addonArt('fanart.jpg')

        video_type = 'true'
        if getSetting("autoplay") == 'false' and getSetting("host_select") == '1': video_type = 'false'
        if PseudoTV == 'True': video_type = 'true'

        playbackMenu = language(30408).encode("utf-8")
        if getSetting("autoplay") == 'true': playbackMenu = language(30409).encode("utf-8")

        if (getSetting("trakt_user") == '' or getSetting("trakt_password") == ''): traktMode = False
        else: traktMode = True

        cacheToDisc = False
        if action == 'episodes_trakt_progress': cacheToDisc = True

        try:
            favourites = []
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='TV Show'")
            favourites = dbcur.fetchall()
            favourites = [i[0] for i in favourites]
            favourites = [re.sub('[^0-9]', '', i) for i in favourites]
        except:
            pass

        try:
            if traktMode == True: raise Exception()
            from metahandler import metahandlers
            metaget = metahandlers.MetaData(preparezip=False)
        except:
            pass

        try:
            if traktMode == False: raise Exception()
            record = ('shows', getSetting("trakt_user"))
            dbcon = database.connect(addonCache)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM rel_trakt WHERE info = '%s' AND user = '%s'" % (record[0], record[1]))
            indicators = dbcur.fetchone()
            indicators = indicators[2]
            indicators = eval(indicators.encode('utf-8'))
            indicators = json.loads(indicators)
        except:
            pass

        total = len(episodeList)
        t = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        for i in episodeList:
            try:
                name, title, year, imdb, tvdb, season, episode, show, show_alt, genre, url, poster, banner, thumb, fanart, studio, status, premiered, duration, rating, mpaa, director, writer, plot = i['name'], i['title'], i['year'], i['imdb'], i['tvdb'], i['season'], i['episode'], i['show'], i['show_alt'], i['genre'], i['url'], i['poster'], i['banner'], i['thumb'], i['fanart'], i['studio'], i['status'], i['date'], i['duration'], i['rating'], i['mpaa'], i['director'], i['writer'], i['plot']

                label = season + 'x' + '%02d' % int(episode) + ' . ' + title
                if action == 'episodes_added' or action == 'episodes_trakt_progress' or action == 'episodes_trakt' or 'episodes_calendar' in action: label = show + ' - ' + label

                if poster == '0': poster = addonPoster
                if banner == '0': banner = addonBanner
                if thumb == '0': thumb = addonThumb
                if fanart == '0' or not getSetting("fanart") == 'true': fanart = addonFanart
                if duration == '0': duration == '60'

                sysname, systitle, sysyear, sysimdb, systvdb, sysseason, sysepisode, sysshow, sysshow_alt, sysurl, sysimage, sysdate, sysgenre = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(season), urllib.quote_plus(episode), urllib.quote_plus(show), urllib.quote_plus(show_alt), urllib.quote_plus(url), urllib.quote_plus(poster), urllib.quote_plus(premiered), urllib.quote_plus(genre)

                meta = {'title': title, 'year': year, 'imdb_id' : 'tt' + imdb, 'tvdb_id' : tvdb, 'season' : season, 'episode': episode, 'tvshowtitle': show, 'genre' : genre, 'poster' : poster, 'banner' : banner, 'thumb' : thumb, 'fanart' : fanart, 'studio': studio, 'status': status, 'premiered' : premiered, 'duration' : duration, 'rating': rating, 'mpaa' : mpaa, 'director': director, 'writer': writer, 'plot': plot, 'trailer': '%s?action=trailer&name=%s' % (sys.argv[0], sysshow)}
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')
                sysmeta = urllib.quote_plus(json.dumps(meta))

                if action == 'episodes_trakt_progress':
                    u = '%s?action=episodes2&show=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s' % (sys.argv[0], sysshow, sysyear, sysimdb, systvdb, sysseason, sysepisode)
                    isFolder = True
                elif video_type == 'true':
                    u = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s&show=%s&show_alt=%s&date=%s&genre=%s&url=%s&t=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, systvdb, sysseason, sysepisode, sysshow, sysshow_alt, sysdate, sysgenre, sysurl, t)
                    isFolder = False
                else:
                    u = '%s?action=get_host&name=%s&title=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s&show=%s&show_alt=%s&date=%s&genre=%s&url=%s&meta=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, systvdb, sysseason, sysepisode, sysshow, sysshow_alt, sysdate, sysgenre, sysurl, sysmeta)
                    isFolder = True

                try:
                    if traktMode == True: raise Exception()
                    playcount = metaget._get_watched_episode({'imdb_id' : 'tt' + imdb, 'season' : season, 'episode': episode, 'premiered' : ''})
                    if playcount == 7: meta.update({'playcount': 1, 'overlay': 7})
                    else: meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass
                try:
                    if traktMode == False: raise Exception()
                    playcount = [i for i in indicators if str(i['show']['ids']['tvdb']) == tvdb][0]['seasons']
                    playcount = [i for i in playcount if int(i['number']) == int(season)][0]['episodes']
                    playcount = [i for i in playcount if int(i['number']) == int(episode)][0]
                    meta.update({'playcount': 1, 'overlay': 7})
                except:
                    pass

                cm = []
                cm.append((playbackMenu, 'RunPlugin(%s?action=toggle_episode_playback&name=%s&title=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s&show=%s&show_alt=%s&date=%s&genre=%s)' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, systvdb, sysseason, sysepisode, sysshow, sysshow_alt, sysdate, sysgenre)))
                if video_type == 'true':
                    cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                if not (getSetting("trakt_user") == '' or getSetting("trakt_password") == ''):
                    cm.append((language(30419).encode("utf-8"), 'RunPlugin(%s?action=trakt_tv_manager&name=%s&tvdb=%s)' % (sys.argv[0], sysshow, systvdb)))
                if not imdb in favourites: cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=favourite_tv_add&imdb=%s&name=%s&year=%s&image=%s)' % (sys.argv[0], sysimdb, sysshow, sysyear, sysimage)))
                else: cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&imdb=%s)' % (sys.argv[0], sysimdb)))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=library_tv_add&name=%s&year=%s&imdb=%s&tvdb=%s)' % (sys.argv[0], sysshow, sysyear, sysimdb, systvdb)))
                cm.append((language(30414).encode("utf-8"), 'Action(Info)'))
                if not imdb == '0000000':
                    cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=unwatched_episodes&imdb=%s&tvdb=%s&season=%s&episode=%s)' % (sys.argv[0], sysimdb, systvdb, sysseason, sysepisode)))
                if not imdb == '0000000':
                    cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=watched_episodes&imdb=%s&tvdb=%s&season=%s&episode=%s)' % (sys.argv[0], sysimdb, systvdb, sysseason, sysepisode)))
                cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=view_episodes)' % (sys.argv[0])))

                item = xbmcgui.ListItem(label, iconImage="DefaultVideo.png", thumbnailImage=thumb)
                try: item.setArt({'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})
                except: pass
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.setProperty("IsPlayable", "true")
                item.setProperty('resumetime',str(0))
                item.setProperty('totaltime',str(1))
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=isFolder)
            except:
                pass

        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=cacheToDisc)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(episodes)'):
                return index().container_view('episodes', {'skin.confluence' : 504})
            xbmc.sleep(100)

    def moviesourceList(self, sourceList, name, imdb, tvdb, meta):
        if sourceList == None or len(sourceList) == 0: return

        total = len(sourceList)
        for i in sourceList:
            try:
                url, source, provider = i['url'], i['source'], i['provider']
                poster, fanart = meta['poster'], meta['fanart']

                sysname, sysimdb, systvdb, sysurl, syssource, sysprovider = urllib.quote_plus(name), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(url), urllib.quote_plus(source), urllib.quote_plus(provider)

                u = '%s?action=play_moviehost&name=%s&imdb=%s&tvdb=%s&url=%s&source=%s&provider=%s' % (sys.argv[0], sysname, sysimdb, systvdb, sysurl, syssource, sysprovider)

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=download&name=%s&url=%s&provider=%s)' % (sys.argv[0], sysname, sysurl, sysprovider)))
                cm.append((language(30412).encode("utf-8"), 'Action(Info)'))
                cm.append((language(30427).encode("utf-8"), 'RunPlugin(%s?action=container_refresh)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(source, iconImage="DefaultVideo.png", thumbnailImage=poster)
                try: item.setArt({'poster': poster, 'banner': poster})
                except: pass
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.setProperty("IsPlayable", "true")
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

    def tvsourceList(self, sourceList, name, imdb, tvdb, meta):
        if sourceList == None or len(sourceList) == 0: return

        total = len(sourceList)
        for i in sourceList:
            try:
                url, source, provider = i['url'], i['source'], i['provider']
                poster, banner, thumb, fanart = meta['poster'], meta['banner'], meta['thumb'], meta['fanart']

                sysname, sysimdb, systvdb, sysurl, syssource, sysprovider = urllib.quote_plus(name), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(url), urllib.quote_plus(source), urllib.quote_plus(provider)

                u = '%s?action=play_tvhost&name=%s&imdb=%s&tvdb=%s&url=%s&source=%s&provider=%s' % (sys.argv[0], sysname, sysimdb, systvdb, sysurl, syssource, sysprovider)

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=download&name=%s&url=%s&provider=%s)' % (sys.argv[0], sysname, sysurl, sysprovider)))
                cm.append((language(30414).encode("utf-8"), 'Action(Info)'))
                cm.append((language(30427).encode("utf-8"), 'RunPlugin(%s?action=container_refresh)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(source, iconImage="DefaultVideo.png", thumbnailImage=thumb)
                try: item.setArt({'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})
                except: pass
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.setProperty("IsPlayable", "true")
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

class contextMenu:
    def item_queue(self):
        xbmc.executebuiltin('Action(Queue)')

    def playlist_open(self):
        xbmc.executebuiltin('ActivateWindow(VideoPlaylist)')

    def settings_open(self, id=addonId, cat=None):
        try:
            xbmc.executebuiltin('Addon.OpenSettings(%s)' % id)
            if cat == None: raise Exception()
            f1, f2 = re.compile('(\d*)\.(\d*)').findall(str(cat))[0]
            xbmc.executebuiltin('SetFocus(%i)' % (int(f1) + 100))
            xbmc.executebuiltin('SetFocus(%i)' % (int(f2) + 200))
        except:
            return

    def view(self, content):
        try:
            skin = xbmc.getSkinDir()
            skinPath = xbmc.translatePath('special://skin/')
            xml = os.path.join(skinPath,'addon.xml')
            file = xbmcvfs.File(xml)
            read = file.read().replace('\n','')
            file.close()
            try: src = re.compile('defaultresolution="(.+?)"').findall(read)[0]
            except: src = re.compile('<res.+?folder="(.+?)"').findall(read)[0]
            src = os.path.join(skinPath, src)
            src = os.path.join(src, 'MyVideoNav.xml')
            file = xbmcvfs.File(src)
            read = file.read().replace('\n','')
            file.close()
            views = re.compile('<views>(.+?)</views>').findall(read)[0]
            views = [int(x) for x in views.split(',')]
            for view in views:
                label = xbmc.getInfoLabel('Control.GetLabel(%s)' % (view))
                if not (label == '' or label == None): break
            record = (skin, content, str(view))
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS views (""skin TEXT, ""view_type TEXT, ""view_id TEXT, ""UNIQUE(skin, view_type)"");")
            dbcur.execute("DELETE FROM views WHERE skin = '%s' AND view_type = '%s'" % (record[0], record[1]))
            dbcur.execute("INSERT INTO views Values (?, ?, ?)", record)
            dbcon.commit()
            viewName = xbmc.getInfoLabel('Container.Viewmode')
            index().infoDialog('%s%s%s' % (language(30301).encode("utf-8"), viewName, language(30302).encode("utf-8")))
        except:
            return

    def favourite_add(self, type, imdb, name, year, image, refresh=False):
        try:
            record = ('tt' + imdb, type, repr(name), year, '', '', image, '', '', '', '', '', '', '', '', '', '', '', '', '')

            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS favourites (""imdb_id TEXT, ""video_type TEXT, ""title TEXT, ""year TEXT, ""tvdb_id TEXT, ""genre TEXT, ""poster TEXT, ""banner TEXT, ""fanart TEXT, ""studio TEXT, ""premiered TEXT, ""duration TEXT, ""rating TEXT, ""votes TEXT, ""mpaa TEXT, ""director TEXT, ""writer TEXT, ""plot TEXT, ""plotoutline TEXT, ""tagline TEXT, ""UNIQUE(imdb_id)"");")
            dbcur.execute("DELETE FROM favourites WHERE imdb_id = '%s'" % (record[0]))
            dbcur.execute("INSERT INTO favourites Values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", record)
            dbcon.commit()

            if refresh == True: index().container_refresh()
            index().infoDialog(language(30303).encode("utf-8"), name)
        except:
            return

    def favourite_delete(self, imdb):
        try:
            record = ['tt' + imdb]

            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("DELETE FROM favourites WHERE imdb_id = '%s'" % (record[0]))
            dbcon.commit()

            index().container_refresh()
            index().infoDialog(language(30304).encode("utf-8"), name)
        except:
            return

    def trakt_manager(self, content, name, id):
        try:
            userList = userlists().trakt_list()

            nameList = [i['name'] for i in userList]
            nameList = [nameList[i//2] for i in range(len(nameList)*2)]
            for i in range(0, len(nameList), 2): nameList[i] = (language(30425) + ' ' + nameList[i]).encode('utf-8')
            for i in range(1, len(nameList), 2): nameList[i] = (language(30426) + ' ' + nameList[i]).encode('utf-8')
            nameList = [language(30420).encode("utf-8"), language(30421).encode("utf-8"), language(30422).encode("utf-8"), language(30423).encode("utf-8"), language(30424).encode("utf-8")] + nameList

            slugList = [re.compile('/lists/(.+?)/items').findall(i['url'])[0] for i in userList]
            slugList = [slugList[i//2] for i in range(len(slugList)*2)]
            slugList = ['', '', '', '', ''] + slugList

            select = index().selectDialog(nameList, language(30419).encode("utf-8"))

            if content == 'movie':
                if not id.startswith('tt'): id = 'tt' + id
                post = {"movies": [{"ids": {"imdb": id}}]}
            else:
                post = {"shows": [{"ids": {"tvdb": id}}]}

            if select == -1:
                return
            elif select == 0:
                result = getTrakt().result(link().trakt_collection_add, post=post)
            elif select == 1:
                result = getTrakt().result(link().trakt_collection_remove, post=post)
            elif select == 2:
                result = getTrakt().result(link().trakt_watchlist_add, post=post)
            elif select == 3:
                result = getTrakt().result(link().trakt_watchlist_remove, post=post)
            else:
                if select == 4:
                    new = common.getUserInput(language(30424).encode("utf-8"), '')
                    if (new == None or new == ''): return
                    url = link().trakt_lists % link().trakt_user
                    result = getTrakt().result(url, post={"name": new, "privacy": "private"})

                    try: slug = json.loads(result)['ids']['slug']
                    except: slug = None

                    if slug == None: return index().infoDialog(name, 'Failed')
                else:
                    slug = slugList[select]

                if select == 4 or not select % 2 == 0:
                    url = link().trakt_list_add % (link().trakt_user, slug)
                else:
                    url = link().trakt_list_remove % (link().trakt_user, slug)

                result = getTrakt().result(url, post=post)

            if result == None: info = 'Failed'
            else: info = 'Successful'
            index().infoDialog(info, name)
        except:
            return

    def playcount_movies(self, title, year, imdb, watched):
        try:
            if (getSetting("trakt_user") == '' or getSetting("trakt_password") == ''): traktMode = False
            else: traktMode = True
        except:
            pass

        try:
            if traktMode == True: raise Exception()
            from metahandler import metahandlers
            metaget = metahandlers.MetaData(preparezip=False)
            metaget.get_meta('movie', title ,year=year)
            metaget.change_watched('movie', '', imdb, season='', episode='', year='', watched=watched)
        except:
            pass

        try:
            if traktMode == False: raise Exception()
            if not imdb.startswith('tt'): imdb = 'tt' + imdb
            if watched == 7: url = link().trakt_history
            else: url = link().trakt_history_remove
            getTrakt().result(url, post={"movies": [{"ids": {"imdb": imdb}}]})
            getTrakt().sync('movies')
        except:
            pass

        index().container_refresh()

    def playcount_episodes(self, imdb, tvdb, season, episode, watched):
        try:
            if (getSetting("trakt_user") == '' or getSetting("trakt_password") == ''): traktMode = False
            else: traktMode = True
        except:
            pass

        try:
            if traktMode == True: raise Exception()
            from metahandler import metahandlers
            metaget = metahandlers.MetaData(preparezip=False)
            metaget.get_meta('tvshow', '', imdb_id=imdb)
            metaget.get_episode_meta('', imdb, season, episode)
            metaget.change_watched('episode', '', imdb, season=season, episode=episode, year='', watched=watched)
        except:
            pass

        try:
            if traktMode == False: raise Exception()
            season, episode = int('%01d' % int(season)), int('%01d' % int(episode))
            if watched == 7: url = link().trakt_history
            else: url = link().trakt_history_remove
            getTrakt().result(url, post={"shows": [{"seasons": [{"episodes": [{"number": episode}], "number": season}], "ids": {"tvdb": tvdb}}]})
            getTrakt().sync('shows')
        except:
            pass

        index().container_refresh()

    def playcount_shows(self, name, year, imdb, tvdb, season, watched, metahandler=True):
        try:
            if (getSetting("trakt_user") == '' or getSetting("trakt_password") == ''): traktMode = False
            else: traktMode = True

            match = episodes().get(name, year, imdb, tvdb, season, idx=False)
            match = match[1]['episodes']
            match = [{'name': i['name'], 'season': int('%01d' % int(i['season'])), 'episode': int('%01d' % int(i['episode']))} for i in match]
        except:
            pass

        try:
            if traktMode == True: raise Exception()
            from metahandler import metahandlers
            metaget = metahandlers.MetaData(preparezip=False)

            dialog = xbmcgui.DialogProgress()
            dialog.create(addonName.encode("utf-8"), str(name))
            dialog.update(0, str(name), language(30361).encode("utf-8") + '...')

            metaget.get_meta('tvshow', '', imdb_id=imdb)

            for i in range(len(match)):
                if xbmc.abortRequested == True: return sys.exit()
                if dialog.iscanceled(): return dialog.close()

                dialog.update(int((100 / float(len(match))) * i), str(name), str(match[i]['name']))

                season, episode = match[i]['season'], match[i]['episode']
                metaget.get_episode_meta('', imdb, season, episode)
                metaget.change_watched('episode', '', imdb, season=season, episode=episode, year='', watched=watched)

            try: dialog.close()
            except: pass
        except:
            try: dialog.close()
            except: pass

        try:
            if traktMode == False: raise Exception()
            seasons = []
            for i in range(len(match)): seasons.append(match[i]['season'])
            seasons = uniqueList(seasons).list
            seasons = [{"number": i} for i in seasons]
            if watched == 7: url = link().trakt_history
            else: url = link().trakt_history_remove
            getTrakt().result(url, post={"shows": [{"seasons": seasons, "ids": {"tvdb": tvdb}}]})
            getTrakt().sync('shows')
        except:
            pass

        index().container_refresh()

    def library_movie_add(self, name, title, year, imdb, url, batch=False):
        try:
            check = getSetting("check_movie_link")
        except:
            pass

        if check == 'true' or batch == False:
            index().infoDialog(language(30310).encode("utf-8"), str(name), time=10000000)

        try:
            if not getSetting("check_library") == 'true': raise Exception()

            id = 'tt' + imdb if imdb.isdigit() else imdb

            lib = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties" : ["imdbnumber", "originaltitle", "year"]}, "id": 1}' % (year, str(int(year)+1), str(int(year)-1)))
            lib = unicode(lib, 'utf-8', errors='ignore')
            lib = json.loads(lib)['result']['movies']
            lib = [i for i in lib if str(i['imdbnumber']) == id or (i['originaltitle'].encode("utf-8") == title and str(i['year']) == year)][0]
        except:
            lib = []

        try:
            if not lib == []: raise Exception()

            if check == 'true':
                src = resolver().sources_get(name, title, year, imdb, None, None, None, None, None, None, None)
                if not len(src) > 0: raise Exception()

            self.library_movie_strm({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'url': url})
        except:
            pass

        if batch == True: return

        index().infoDialog(language(30317).encode("utf-8"), str(name))

        if getSetting("update_library") == 'true' and not xbmc.getCondVisibility('Library.IsScanningVideo'):
            xbmc.executebuiltin('UpdateLibrary(video)')

    def library_movie_list(self, url):
        index().infoDialog(language(30315).encode("utf-8"), language(30311).encode("utf-8"), time=10000000)

        try:
            match = index().cache(movies().get, 0, url, False)
            if match == None: raise Exception()
        except:
            index().infoDialog(language(30316).encode("utf-8"), language(30311).encode("utf-8"))
            return

        for i in match:
            try:
                if xbmc.abortRequested == True: return sys.exit()

                self.library_movie_add(i['name'], i['title'], i['year'], i['imdb'], i['url'], batch=True)
            except:
                pass

        index().infoDialog(language(30317).encode("utf-8"), language(30311).encode("utf-8"))

        if getSetting("update_library") == 'true' and not xbmc.getCondVisibility('Library.IsScanningVideo'):
            xbmc.executebuiltin('UpdateLibrary(video)')

    def library_movie_tool(self, url):
        yes = index().yesnoDialog(language(30341).encode("utf-8"), '')
        if not yes: return

        if url == 'trakt_collection':
            url = link().trakt_collection % link().trakt_user
        elif url == 'trakt_watchlist':
            url = link().trakt_watchlist % link().trakt_user
        elif url == 'imdb_watchlist':
            url = link().imdb_watchlist % link().imdb_user

        xbmc.executebuiltin('RunPlugin(%s?action=library_movie_list&url=%s)' % (sys.argv[0], urllib.quote_plus(url)))

    def library_movie_strm(self, i):
        try:
            name, title, year, imdb, url = i['name'], i['title'], i['year'], i['imdb'], i['url']

            sysname, systitle, sysyear, sysimdb, sysurl = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(url)

            content = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s&url=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, sysurl)

            xbmcvfs.mkdir(movieLibrary)

            enc_name = name.translate(None, '\/:*?"<>|').strip('.')
            folder = os.path.join(movieLibrary, enc_name)
            xbmcvfs.mkdir(folder)

            stream = os.path.join(folder, enc_name + '.strm')
            file = xbmcvfs.File(stream, 'w')
            file.write(str(content))
            file.close()
        except:
            pass

    def library_tv_add(self, name, year, imdb, tvdb, batch=False):
        try:
            block = True
            check = getSetting("check_episode_link")
            date = datetime.datetime.utcnow() - datetime.timedelta(hours = 29)
            date = int(date.strftime("%Y%m%d"))
        except:
            pass

        if check == 'true' or batch == False:
            index().infoDialog(language(30310).encode("utf-8"), str(name), time=10000000)

        try:
            match = episodes().get(name, year, imdb, tvdb, idx=False)
            match = match[1]['episodes']
        except:
            if check == 'true' or batch == False:
                index().infoDialog(language(30316).encode("utf-8"), str(name))
            return

        try:
            if not getSetting("check_library") == 'true': raise Exception()

            id = ['tt' + match[0]['imdb'] if match[0]['imdb'].isdigit() else match[0]['imdb'], match[0]['tvdb']]

            lib = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"properties" : ["imdbnumber", "title", "year"]}, "id": 1}')
            lib = unicode(lib, 'utf-8', errors='ignore')
            lib = json.loads(lib)['result']['tvshows']

            lib = [i['title'].encode("utf-8") for i in lib if str(i['imdbnumber']) in id or (i['title'].encode("utf-8") == name and str(i['year']) == year)][0]
            lib = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "tvshow", "operator": "is", "value": "%s"}]}, "properties": ["season", "episode"]}, "id": 1}' % lib)
            lib = unicode(lib, 'utf-8', errors='ignore')
            lib = json.loads(lib)['result']['episodes']
            lib = ['S%02dE%02d' % (i['season'], i['episode']) for i in lib]
        except:
            lib = []

        for i in match:
            try:
                if xbmc.abortRequested == True: return sys.exit()

                if check == 'true':
                    if block == False:
                        pass
                    elif i['episode'] == '1':
                        src = resolver().sources_get(i['name'], i['title'], i['year'], i['imdb'], i['tvdb'], i['season'], i['episode'], i['show'], i['show_alt'], i['date'], i['genre'])
                        if len(src) > 0: block = False
                    if block == True: raise Exception()

                l = 'S%02dE%02d' % (int(i['season']), int(i['episode']))
                if l in lib: raise Exception()

                if date <= int(re.sub('[^0-9]', '', str(i['date']))):
                    src = resolver().sources_get(i['name'], i['title'], i['year'], i['imdb'], i['tvdb'], i['season'], i['episode'], i['show'], i['show_alt'], i['date'], i['genre'])
                    if not len(src) > 0: raise Exception()

                self.library_tv_strm(i)
            except:
                pass

        if batch == True: return

        index().infoDialog(language(30317).encode("utf-8"), str(name))

        if getSetting("update_library") == 'true' and not xbmc.getCondVisibility('Library.IsScanningVideo'):
            xbmc.executebuiltin('UpdateLibrary(video)')

    def library_tv_list(self, url):
        index().infoDialog(language(30315).encode("utf-8"), language(30312).encode("utf-8"), time=10000000)

        try:
            match = index().cache(shows().get, 0, url, False)
            if match == None: raise Exception()
        except:
            index().infoDialog(language(30316).encode("utf-8"), language(30312).encode("utf-8"))
            return

        for i in match:
            try:
                if xbmc.abortRequested == True: return sys.exit()
                self.library_tv_add(i['title'], i['year'], i['imdb'], i['tvdb'], batch=True)
            except:
                pass

        index().infoDialog(language(30317).encode("utf-8"), language(30312).encode("utf-8"))

        if getSetting("update_library") == 'true' and not xbmc.getCondVisibility('Library.IsScanningVideo'):
            xbmc.executebuiltin('UpdateLibrary(video)')

    def library_tv_tool(self, url):
        yes = index().yesnoDialog(language(30341).encode("utf-8"), '')
        if not yes: return

        if url == 'trakt_tv_collection':
            url = link().trakt_tv_collection % link().trakt_user
        elif url == 'trakt_tv_watchlist':
            url = link().trakt_tv_watchlist % link().trakt_user
        elif url == 'imdb_tv_watchlist':
            url = link().imdb_watchlist % link().imdb_user

        xbmc.executebuiltin('RunPlugin(%s?action=library_tv_list&url=%s)' % (sys.argv[0], urllib.quote_plus(url)))

    def library_tv_strm(self, i):
        try:
            name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, url = i['name'], i['title'], i['year'], i['imdb'], i['tvdb'], i['season'], i['episode'], i['show'], i['show_alt'], i['date'], i['genre'], i['url']

            sysname, systitle, sysyear, sysimdb, systvdb, sysseason, sysepisode, sysshow, sysshow_alt, sysdate, sysgenre, sysurl = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(season), urllib.quote_plus(episode), urllib.quote_plus(show), urllib.quote_plus(show_alt), urllib.quote_plus(date), urllib.quote_plus(genre), urllib.quote_plus(url)

            content = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s&show=%s&show_alt=%s&date=%s&genre=%s&url=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, systvdb, sysseason, sysepisode, sysshow, sysshow_alt, sysdate, sysgenre, sysurl)

            xbmcvfs.mkdir(tvLibrary)

            enc_show = show_alt.translate(None, '\/:*?"<>|').strip('.')
            folder = os.path.join(tvLibrary, enc_show)
            xbmcvfs.mkdir(folder)

            enc_season = 'Season %s' % season.translate(None, '\/:*?"<>|').strip('.')
            folder = os.path.join(folder, enc_season)
            xbmcvfs.mkdir(folder)

            enc_name = name.translate(None, '\/:*?"<>|').strip('.')
            stream = os.path.join(folder, enc_name + '.strm')
            print 'gClone: %s - %s' % (enc_name, str(content))
            file = xbmcvfs.File(stream, 'w')
            file.write(str(content))
            file.close()
        except:
            pass

    def library_update_tool(self):
        xbmc.executebuiltin('RunPlugin(%s?action=library_update)' % sys.argv[0])

    def library_update(self, notify):
        start = time.time()

        try:
            shows = []
            season, episode = [], []
            show = [os.path.join(tvLibrary, i) for i in xbmcvfs.listdir(tvLibrary)[0]]
            for s in show:
                try: season += [os.path.join(s, i) for i in xbmcvfs.listdir(s)[0]]
                except: pass
            for s in season:
                try: episode.append([os.path.join(s, i) for i in xbmcvfs.listdir(s)[1] if i.endswith('.strm')][-1])
                except: pass

            for file in episode:
                try:
                    file = xbmcvfs.File(file)
                    read = file.read()
                    read = read.encode("utf-8")
                    file.close()

                    params = {}
                    if not read.startswith(sys.argv[0]): raise Exception()
                    query = read[read.find('?') + 1:].split('&')
                    for i in query: params[i.split('=')[0]] = i.split('=')[1]
                    show, year, imdb, tvdb = urllib.unquote_plus(params["show"]), urllib.unquote_plus(params["year"]), urllib.unquote_plus(params["imdb"]), urllib.unquote_plus(params["tvdb"])
                    shows.append({'show': show, 'year': year, 'imdb': imdb, 'tvdb': tvdb})
                except:
                    pass

            shows = [i for x, i in enumerate(shows) if i not in shows[x + 1:]]
            if len(shows) == 0: raise Exception()
        except:
            return

        try:
            date = datetime.datetime.utcnow() - datetime.timedelta(hours = 29)
            date = int(date.strftime("%Y%m%d"))

            lib = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"properties" : ["imdbnumber", "title", "year"]}, "id": 1}')
            lib = unicode(lib, 'utf-8', errors='ignore')
            lib = json.loads(lib)['result']['tvshows']
        except:
            return

        if notify == 'true':
            index().infoDialog(language(30315).encode("utf-8"), language(30313).encode("utf-8"), time=10000000)

        for sh in shows:
            if xbmc.abortRequested == True: return sys.exit()

            try:
                fetch = None
                dbcon = database.connect(addonCache)
                dbcur = dbcon.cursor()
                dbcur.execute("SELECT * FROM rel_lib WHERE tvdb_id = '%s'" % sh['tvdb'])
                fetch = dbcur.fetchone()

                show = eval(fetch[1].encode('utf-8'))
                episode = eval(fetch[2].encode('utf-8'))
            except:
                pass

            try:
                if not fetch == None: raise Exception()
                match = episodes().get(sh['show'], sh['year'], sh['imdb'], sh['tvdb'], idx=False)
                match = match[1]['episodes']

                show = {'show': match[0]['show'], 'show_alt': match[0]['show_alt'], 'year': match[0]['year'], 'genre': match[0]['genre'], 'url': match[0]['url'], 'imdb': match[0]['imdb'], 'tvdb': match[0]['tvdb'], 'status': match[0]['status']}
                episode = [{'name': i['name'], 'title': i['title'], 'season': i['season'], 'episode': i['episode'], 'date': i['date']} for i in match]
            except:
                pass

            try:
                status = show['status']
                if status.lower() == 'continuing': raise Exception()
                if not fetch == None: raise Exception()

                dbcur.execute("CREATE TABLE IF NOT EXISTS rel_lib (""tvdb_id TEXT, ""show TEXT, ""episode TEXT, ""UNIQUE(tvdb_id)"");")
                dbcur.execute("DELETE FROM rel_lib WHERE tvdb_id = '%s'" % tvdb_id)
                dbcur.execute("INSERT INTO rel_lib Values (?, ?, ?)", (tvdb_id, repr(show), repr(episode)))
                dbcon.commit()
            except:
                pass

            try:
                id = ['tt' + show['imdb'] if show['imdb'].isdigit() else show['imdb'], show['tvdb']]
                sd = [show['show'], show['show_alt']]
                yd = show['year']

                ep = [i['title'].encode("utf-8") for i in lib if str(i['imdbnumber']) in id or (i['title'].encode("utf-8") in sd and str(i['year']) == yd)][0]
                ep = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "tvshow", "operator": "is", "value": "%s"}]}, "properties": ["season", "episode"]}, "id": 1}' % ep)
                ep = unicode(ep, 'utf-8', errors='ignore')
                ep = json.loads(ep)['result']['episodes'][-1]

                num = [x for x,y in enumerate(episode) if str(y['season']) == str(ep['season']) and str(y['episode']) == str(ep['episode'])][-1]
                episode = [y for x,y in enumerate(episode) if x > num]
                if len(episode) == 0: continue
            except:
                continue

            for i in episode:
                try:
                    if xbmc.abortRequested == True: return sys.exit()

                    i.update({'show': show['show'], 'show_alt': show['show_alt'], 'year': show['year'], 'genre': show['genre'], 'url': show['url'], 'imdb': show['imdb'], 'tvdb': show['tvdb']})

                    if date <= int(re.sub('[^0-9]', '', str(i['date']))):
                        src = resolver().sources_get(i['name'], i['title'], i['year'], i['imdb'], i['tvdb'], i['season'], i['episode'], i['show'], i['show_alt'], i['date'], i['genre'])
                        if not len(src) > 2: raise Exception()

                    self.library_tv_strm(i)
                except:
                    pass

        if notify == 'true':
            end = '%s %s seconds' % (language(30314).encode("utf-8"), int((time.time() - start)))
            index().infoDialog(end, language(30313).encode("utf-8"))

        if getSetting("update_library") == 'true' and not xbmc.getCondVisibility('Library.IsScanningVideo'):
            xbmc.executebuiltin('UpdateLibrary(video)')

    def service(self):
        try:
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS service (""setting TEXT, ""value TEXT, ""UNIQUE(setting)"");")
            dbcur.execute("SELECT * FROM service WHERE setting = 'last_run'")
            match = dbcur.fetchone()
            if match == None:
                service_run = "1970-01-01 23:59:00.000000"
                dbcur.execute("INSERT INTO service Values (?, ?)", ("last_run", service_run))
                dbcon.commit()
            else:
                service_run = str(match[1])
            dbcon.close()
        except:
            try: dbcon.close()
            except: pass
            return

        try:
            property = 'genesis_service_run'
            index().setProperty(property, service_run)
        except:
            return

        while (not xbmc.abortRequested):
            try:
                service_run = index().getProperty(property)

                t1 = datetime.timedelta(hours=6)
                t2 = datetime.datetime.strptime(service_run, "%Y-%m-%d %H:%M:%S.%f")
                t3 = datetime.datetime.now()

                update = abs(t3 - t2) > t1
                if update == False: raise Exception()

                if (xbmc.Player().isPlaying() or xbmc.getCondVisibility('Library.IsScanningVideo')): raise Exception()

                service_run = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

                index().setProperty(property, service_run)

                try:
                    dbcon = database.connect(addonSettings)
                    dbcur = dbcon.cursor()
                    dbcur.execute("CREATE TABLE IF NOT EXISTS service (""setting TEXT, ""value TEXT, ""UNIQUE(setting)"");")
                    dbcur.execute("DELETE FROM service WHERE setting = 'last_run'")
                    dbcur.execute("INSERT INTO service Values (?, ?)", ("last_run", service_run))
                    dbcon.commit()
                    dbcon.close()
                except:
                    try: dbcon.close()
                    except: pass

                getTrakt().sync()

                if not getSetting("service_update") == 'true': raise Exception()
                try: notify = getSetting("service_notification")
                except: notify = 'true'
                self.library_update(notify)
            except:
                pass

            xbmc.sleep(10000)

    def download(self, name, url, provider):
        try:
            url = resolver().sources_resolve(url, provider)
            if url == None: raise Exception()

            try: agent = urlparse.parse_qs(url.split('|')[1])['User-Agent'][0]
            except: agent = None
            try: referer = urlparse.parse_qs(url.split('|')[1])['Referer'][0]
            except: referer = None
            try: cookie = urlparse.parse_qs(url.split('|')[1])['Cookie'][0]
            except: cookie = None

            url = url.split('|')[0]

            name = name.translate(None, '\/:*?"<>|').strip('.')

            content = re.compile('(.+?)\sS(\d*)E\d*$').findall(name)

            if len(content) == 0:
            	dest = xbmc.translatePath(getSetting("movie_downloads"))
            	xbmcvfs.mkdir(dest)
            	dest = os.path.join(dest, name)
            	xbmcvfs.mkdir(dest)
            else:
            	dest = xbmc.translatePath(getSetting("tv_downloads"))
            	xbmcvfs.mkdir(dest)
            	dest = os.path.join(dest, content[0][0])
            	xbmcvfs.mkdir(dest)
            	dest = os.path.join(dest, 'Season %01d' % int(content[0][1]))
            	xbmcvfs.mkdir(dest)

            ext = os.path.splitext(urlparse.urlparse(url).path)[1][1:]
            if not ext in ['mp4', 'mkv', 'flv', 'avi', 'mpg']: ext = 'mp4'
            dest = os.path.join(dest, name + '.' + ext)

            import commondownloader
            commondownloader.download(url, dest, 'gClone', referer=referer, agent=agent, cookie=cookie)
        except:
            index().infoDialog(language(30308).encode("utf-8"))
            return

    def toggle_playback(self, content, name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre):
        if content == 'movie':
            meta = {'title': xbmc.getInfoLabel('ListItem.title'), 'originaltitle': xbmc.getInfoLabel('ListItem.originaltitle'), 'year': xbmc.getInfoLabel('ListItem.year'), 'genre': xbmc.getInfoLabel('ListItem.genre'), 'studio' : xbmc.getInfoLabel('ListItem.studio'), 'country' : xbmc.getInfoLabel('ListItem.country'), 'duration' : xbmc.getInfoLabel('ListItem.duration'), 'rating': xbmc.getInfoLabel('ListItem.rating'), 'votes': xbmc.getInfoLabel('ListItem.votes'), 'mpaa': xbmc.getInfoLabel('ListItem.mpaa'), 'director': xbmc.getInfoLabel('ListItem.director'), 'writer': xbmc.getInfoLabel('ListItem.writer'), 'plot': xbmc.getInfoLabel('ListItem.plot'), 'plotoutline': xbmc.getInfoLabel('ListItem.plotoutline'), 'tagline': xbmc.getInfoLabel('ListItem.tagline')}
            label, poster, thumb, fanart = xbmc.getInfoLabel('ListItem.label'), xbmc.getInfoLabel('ListItem.icon'), xbmc.getInfoLabel('ListItem.icon'), xbmc.getInfoLabel('ListItem.Property(Fanart_Image)')
            sysname, systitle, sysyear, sysimdb = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb)
            u = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb)

        elif content == 'episode':
            meta = {'title': xbmc.getInfoLabel('ListItem.title'), 'season' : xbmc.getInfoLabel('ListItem.season'), 'episode': xbmc.getInfoLabel('ListItem.episode'), 'tvshowtitle': xbmc.getInfoLabel('ListItem.tvshowtitle'), 'studio': xbmc.getInfoLabel('ListItem.studio'), 'premiered' : xbmc.getInfoLabel('ListItem.premiered'), 'duration' : xbmc.getInfoLabel('ListItem.duration'), 'rating': xbmc.getInfoLabel('ListItem.rating'), 'mpaa' : xbmc.getInfoLabel('ListItem.mpaa'), 'director': xbmc.getInfoLabel('ListItem.director'), 'writer': xbmc.getInfoLabel('ListItem.writer'), 'plot': xbmc.getInfoLabel('ListItem.plot')}
            label, poster, thumb, fanart = xbmc.getInfoLabel('ListItem.label'), xbmc.getInfoLabel('ListItem.Art(tvshow.poster)'), xbmc.getInfoLabel('ListItem.icon'), xbmc.getInfoLabel('ListItem.Property(Fanart_Image)')
            sysname, systitle, sysyear, sysimdb, systvdb, sysseason, sysepisode, sysshow, sysshow_alt, sysdate, sysgenre = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(season), urllib.quote_plus(episode), urllib.quote_plus(show), urllib.quote_plus(show_alt), urllib.quote_plus(date), urllib.quote_plus(genre)
            u = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s&show=%s&show_alt=%s&date=%s&genre=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, systvdb, sysseason, sysepisode, sysshow, sysshow_alt, sysdate, sysgenre)

        autoplay = getSetting("autoplay")
        if autoplay == 'false': u += '&url=direct://'
        else: u += '&url=dialog://'

        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        item = xbmcgui.ListItem(label, iconImage="DefaultVideo.png", thumbnailImage=thumb)
        try: item.setArt({'poster': poster, 'tvshow.poster': poster, 'season.poster': poster})
        except: pass
        item.setProperty("Fanart_Image", fanart)
        item.setInfo(type="Video", infoLabels = meta)
        item.setProperty("Video", "true")
        item.setProperty("IsPlayable", "true")
        xbmc.Player().play(u, item)


class root:
    def get(self):
        rootList = []
        rootList.append({'name': 30501, 'image': 'root_movies.jpg', 'action': 'root_movies'})
        rootList.append({'name': 30502, 'image': 'root_shows.jpg', 'action': 'root_shows'})
        rootList.append({'name': 30503, 'image': 'channels_movies.jpg', 'action': 'channels_movies'})
        rootList.append({'name': 30504, 'image': 'root_genesis.jpg', 'action': 'root_genesis'})

        root_movies = getSetting("root_movies")
        if root_movies == '1':
            rootList.append({'name': 30505, 'image': 'movies_added.jpg', 'action': 'movies_featured'})
        elif root_movies == '2':
            rootList.append({'name': 30505, 'image': 'movies_added.jpg', 'action': 'movies_added_hd'})
        elif root_movies == '3':
            rootList.append({'name': 30505, 'image': 'movies_added.jpg', 'action': 'movies_added'})

        if not (link().trakt_user == '' or link().trakt_password == ''):
            root_episodes = getSetting("root_episodes_trakt")
        else:
            root_episodes = getSetting("root_episodes")
        if root_episodes == '1':
            rootList.append({'name': 30506, 'image': 'episodes_added.jpg', 'action': 'episodes_added'})
        elif root_episodes == '2':
            rootList.append({'name': 30506, 'image': 'episodes_added.jpg', 'action': 'episodes_trakt_progress'})
        elif root_episodes == '3':
            rootList.append({'name': 30506, 'image': 'episodes_added.jpg', 'action': 'episodes_trakt'})

        root_calendar = getSetting("root_calendar")
        if root_calendar == '1':
            rootList.append({'name': 30507, 'image': 'root_calendar.jpg', 'action': 'root_calendar'})

        rootList.append({'name': 30508, 'image': 'root_tools.jpg', 'action': 'root_tools'})
        rootList.append({'name': 30509, 'image': 'root_search.jpg', 'action': 'root_search'})
        index().rootList(rootList)

    def movies(self):
        rootList = []
        rootList.append({'name': 30521, 'image': 'genres_movies.jpg', 'action': 'genres_movies'})
        rootList.append({'name': 30522, 'image': 'languages_movies.jpg', 'action': 'languages_movies'})
        rootList.append({'name': 30523, 'image': 'certificates_movies.jpg', 'action': 'certificates_movies'})
        rootList.append({'name': 30524, 'image': 'movies_boxoffice.jpg', 'action': 'movies_boxoffice'})
        rootList.append({'name': 30525, 'image': 'years_movies.jpg', 'action': 'years_movies'})
        rootList.append({'name': 30526, 'image': 'movies_trending.jpg', 'action': 'movies_trending'})
        rootList.append({'name': 30527, 'image': 'movies_popular.jpg', 'action': 'movies_popular'})
        rootList.append({'name': 30528, 'image': 'movies_views.jpg', 'action': 'movies_views'})
        rootList.append({'name': 30529, 'image': 'movies_oscars.jpg', 'action': 'movies_oscars'})
        rootList.append({'name': 30530, 'image': 'movies_theaters.jpg', 'action': 'movies_theaters'})
        rootList.append({'name': 30531, 'image': 'movies_added_hd.jpg', 'action': 'movies_added_hd'})
        rootList.append({'name': 30532, 'image': 'movies_added.jpg', 'action': 'movies_added'})
        rootList.append({'name': 30533, 'image': 'movies_favourites.jpg', 'action': 'movies_favourites'})
        rootList.append({'name': 30534, 'image': 'people_movies.jpg', 'action': 'people_movies'})
        rootList.append({'name': 30535, 'image': 'movies_search.jpg', 'action': 'movies_search'})
        index().rootList(rootList)

    def shows(self):
        rootList = []
        rootList.append({'name': 30541, 'image': 'genres_shows.jpg', 'action': 'genres_shows'})
        rootList.append({'name': 30542, 'image': 'certificates_shows.jpg', 'action': 'certificates_shows'})
        rootList.append({'name': 30543, 'image': 'shows_popular.jpg', 'action': 'shows_popular'})
        rootList.append({'name': 30544, 'image': 'shows_active.jpg', 'action': 'shows_active'})
        rootList.append({'name': 30545, 'image': 'shows_trending.jpg', 'action': 'shows_trending'})
        rootList.append({'name': 30546, 'image': 'shows_rating.jpg', 'action': 'shows_rating'})
        rootList.append({'name': 30547, 'image': 'shows_views.jpg', 'action': 'shows_views'})
        rootList.append({'name': 30548, 'image': 'episodes_added.jpg', 'action': 'episodes_added'})
        rootList.append({'name': 30549, 'image': 'root_calendar.jpg', 'action': 'root_calendar'})
        rootList.append({'name': 30550, 'image': 'shows_favourites.jpg', 'action': 'shows_favourites'})
        rootList.append({'name': 30551, 'image': 'people_shows.jpg', 'action': 'people_shows'})
        rootList.append({'name': 30552, 'image': 'shows_search.jpg', 'action': 'shows_search'})
        index().rootList(rootList)

    def calendar(self):
        rootList = []
        rootList.append({'name': 30561, 'image': 'root_calendar.jpg', 'action': 'episodes_calendar_1'})
        rootList.append({'name': 30562, 'image': 'root_calendar.jpg', 'action': 'episodes_calendar_2'})
        rootList.append({'name': 30563, 'image': 'root_calendar.jpg', 'action': 'episodes_calendar_3'})
        rootList.append({'name': 30564, 'image': 'root_calendar.jpg', 'action': 'episodes_calendar_4'})
        rootList.append({'name': 30565, 'image': 'root_calendar.jpg', 'action': 'shows_season_premieres'})
        rootList.append({'name': 30566, 'image': 'root_calendar.jpg', 'action': 'shows_premieres'})
        index().rootList(rootList)

    def gClone(self):
        rootList = []
        if not (link().trakt_user == '' or link().trakt_password == ''):
            rootList.append({'name': 30581, 'image': 'movies_trakt_collection.jpg', 'action': 'movies_trakt_collection'})
            rootList.append({'name': 30582, 'image': 'shows_trakt_collection.jpg', 'action': 'shows_trakt_collection'})
            rootList.append({'name': 30583, 'image': 'movies_trakt_watchlist.jpg', 'action': 'movies_trakt_watchlist'})
            rootList.append({'name': 30584, 'image': 'shows_trakt_watchlist.jpg', 'action': 'shows_trakt_watchlist'})
            rootList.append({'name': 30585, 'image': 'episodes_trakt_progress.jpg', 'action': 'episodes_trakt_progress'})
            rootList.append({'name': 30586, 'image': 'episodes_trakt.jpg', 'action': 'episodes_trakt'})
        if not (link().imdb_user == ''):
            rootList.append({'name': 30587, 'image': 'movies_imdb_watchlist.jpg', 'action': 'movies_imdb_watchlist'})
            rootList.append({'name': 30588, 'image': 'shows_imdb_watchlist.jpg', 'action': 'shows_imdb_watchlist'})
        if not (link().trakt_user == '' or link().trakt_password == '') or not (link().imdb_user == ''):
            rootList.append({'name': 30589, 'image': 'userlists_movies.jpg', 'action': 'userlists_movies'})
            rootList.append({'name': 30590, 'image': 'userlists_shows.jpg', 'action': 'userlists_shows'})
        rootList.append({'name': 30591, 'image': 'movies_favourites.jpg', 'action': 'movies_favourites'})
        rootList.append({'name': 30592, 'image': 'shows_favourites.jpg', 'action': 'shows_favourites'})
        rootList.append({'name': 30593, 'image': 'downloads_movies.jpg', 'action': 'downloads_movies'})
        rootList.append({'name': 30594, 'image': 'downloads_shows.jpg', 'action': 'downloads_shows'})
        index().rootList(rootList)

    def search(self):
        rootList = []
        rootList.append({'name': 30601, 'image': 'movies_search.jpg', 'action': 'movies_search'})
        rootList.append({'name': 30602, 'image': 'shows_search.jpg', 'action': 'shows_search'})
        rootList.append({'name': 30603, 'image': 'people_movies.jpg', 'action': 'people_movies'})
        rootList.append({'name': 30604, 'image': 'people_shows.jpg', 'action': 'people_shows'})
        index().rootList(rootList)

    def tools(self):
        rootList = []
        rootList.append({'name': 30621, 'image': 'settings_open.jpg', 'action': 'settings_general'})
        rootList.append({'name': 30622, 'image': 'settings_open.jpg', 'action': 'settings_accounts'})
        rootList.append({'name': 30623, 'image': 'settings_open.jpg', 'action': 'settings_playback'})
        rootList.append({'name': 30624, 'image': 'settings_open.jpg', 'action': 'settings_subtitles'})
        rootList.append({'name': 30625, 'image': 'settings_open.jpg', 'action': 'settings_movies'})
        rootList.append({'name': 30626, 'image': 'settings_open.jpg', 'action': 'settings_tv'})
        rootList.append({'name': 30627, 'image': 'settings_open.jpg', 'action': 'settings_hostshd'})
        rootList.append({'name': 30628, 'image': 'settings_open.jpg', 'action': 'settings_hostssd'})
        rootList.append({'name': 30629, 'image': 'cache_clear.jpg', 'action': 'cache_clear_src'})
        rootList.append({'name': 30630, 'image': 'cache_clear.jpg', 'action': 'cache_clear_list'})
        rootList.append({'name': 30631, 'image': 'settings_open.jpg', 'action': 'settings_downloads'})
        rootList.append({'name': 30632, 'image': 'root_library.jpg', 'action': 'root_library'})
        index().rootList(rootList)

    def library(self):
        rootList = []
        rootList.append({'name': 30640, 'image': 'settings_open.jpg', 'action': 'settings_library'})
        rootList.append({'name': 30641, 'image': 'library_update.jpg', 'action': 'library_update_tool'})
        rootList.append({'name': 30642, 'image': 'library_movies.jpg', 'action': 'library_movies'})
        rootList.append({'name': 30643, 'image': 'library_shows.jpg', 'action': 'library_shows'})
        if not (link().trakt_user == '' or link().trakt_password == ''):
            rootList.append({'name': 30644, 'image': 'movies_trakt_collection.jpg', 'action': 'library_trakt_collection'})
            rootList.append({'name': 30645, 'image': 'shows_trakt_collection.jpg', 'action': 'library_tv_trakt_collection'})
            rootList.append({'name': 30646, 'image': 'movies_trakt_watchlist.jpg', 'action': 'library_trakt_watchlist'})
            rootList.append({'name': 30647, 'image': 'shows_trakt_watchlist.jpg', 'action': 'library_tv_trakt_watchlist'})
        if not (link().imdb_user == ''):
            rootList.append({'name': 30648, 'image': 'movies_imdb_watchlist.jpg', 'action': 'library_imdb_watchlist'})
            rootList.append({'name': 30649, 'image': 'shows_imdb_watchlist.jpg', 'action': 'library_tv_imdb_watchlist'})
        index().rootList(rootList)


class link:
    def __init__(self):
        self.imdb_base = 'http://www.imdb.com'
        self.imdb_mobile = 'http://m.imdb.com'
        self.imdb_genre = 'http://www.imdb.com/genre/'
        self.imdb_language = 'http://www.imdb.com/language/'
        self.imdb_title = 'http://www.imdb.com/title/tt%s/'
        self.imdb_info = 'http://www.imdbapi.com/?t=%s&y=%s'
        self.imdb_media = 'http://ia.media-imdb.com'
        self.imdb_seasons = 'http://www.imdb.com/title/tt%s/episodes'
        self.imdb_episodes = 'http://www.imdb.com/title/tt%s/episodes?season=%s'
        self.imdb_genres = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&sort=boxoffice_gross_us&count=25&start=1&genres=%s'
        self.imdb_certificates = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&sort=boxoffice_gross_us&count=25&start=1&certificates=us:%s'
        self.imdb_languages = 'http://www.imdb.com/search/title?languages=%s|1&title_type=feature,tv_movie&sort=moviemeter,asc&count=25&start=1'
        self.imdb_years = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&sort=boxoffice_gross_us&count=25&start=1&year=%s,%s'
        self.imdb_popular = 'http://www.imdb.com/search/title?groups=top_1000&sort=moviemeter,asc&count=25&start=1'
        self.imdb_boxoffice = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&sort=boxoffice_gross_us,desc&count=25&start=1'
        self.imdb_views = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&sort=num_votes,desc&count=25&start=1'
        self.imdb_oscars = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&groups=oscar_best_picture_winners&sort=year,desc&count=25&start=1'
        self.imdb_tv_genres = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&sort=moviemeter,asc&count=25&start=1&genres=%s'
        self.imdb_tv_certificates = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&sort=moviemeter,asc&count=25&start=1&certificates=us:%s'
        self.imdb_tv_popular = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&sort=moviemeter,asc&count=25&start=1'
        self.imdb_tv_rating = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=5000,&sort=user_rating,desc&count=25&start=1'
        self.imdb_tv_views = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&sort=num_votes,desc&count=25&start=1'
        self.imdb_tv_active = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&production_status=active&sort=moviemeter,asc&count=25&start=1'
        self.imdb_search = 'http://www.imdb.com/xml/find?json=1&nr=1&tt=on&q=%s'
        self.imdb_people_search = 'http://www.imdb.com/search/name?count=100&name=%s'
        self.imdb_people = 'http://www.imdb.com/search/title?count=25&sort=year,desc&title_type=feature,tv_movie&start=1&role=nm%s'
        self.imdb_tv_people = 'http://www.imdb.com/search/title?count=25&sort=year,desc&title_type=tv_series,mini_series&start=1&role=nm%s'
        self.imdb_userlists = 'http://www.imdb.com/user/ur%s/lists?tab=all&sort=modified:desc&filter=titles'
        self.imdb_watchlist ='http://www.imdb.com/user/ur%s/watchlist'
        self.imdb_list = 'http://www.imdb.com/list/%s/?view=detail&sort=title:asc&title_type=feature,short,tv_movie,tv_special,video,documentary,game&start=1'
        self.imdb_tv_list = 'http://www.imdb.com/list/%s/?view=detail&sort=title:asc&title_type=tv_series,mini_series&start=1'
        self.imdb_user = getSetting("imdb_user").replace('ur', '')

        self.tmdb_base = 'http://api.themoviedb.org'
        self.tmdb_key = base64.urlsafe_b64decode('NTc5ODNlMzFmYjQzNWRmNGRmNzdhZmI4NTQ3NDBlYTk=')
        self.tmdb_info = 'http://api.themoviedb.org/3/movie/tt%s?language=en&api_key=%s'
        self.tmdb_info2 = 'http://api.themoviedb.org/3/movie/%s?language=en&api_key=%s'
        self.tmdb_theaters = 'http://api.themoviedb.org/3/movie/now_playing?api_key=%s&page=1'
        self.tmdb_image = 'http://image.tmdb.org/t/p/original'
        self.tmdb_image2 = 'http://image.tmdb.org/t/p/w500'

        self.tvdb_base = 'http://thetvdb.com'
        self.tvdb_key = base64.urlsafe_b64decode('MUQ2MkYyRjkwMDMwQzQ0NA==')
        self.tvdb_search = 'http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=tt%s&language=en'
        self.tvdb_search2 = 'http://thetvdb.com/api/GetSeries.php?seriesname=%s&language=en'
        self.tvdb_info = 'http://thetvdb.com/api/%s/series/%s/all/en.zip'
        self.tvdb_info2 = 'http://thetvdb.com/api/%s/series/%s/en.xml'
        self.tvdb_image = 'http://thetvdb.com/banners/'
        self.tvdb_image2 = 'http://thetvdb.com/banners/_cache/'

        self.trakt_base = 'http://api-v2launch.trakt.tv'
        self.trakt_key = 'ZWI0MWU5NTI0M2Q4Yzk1MTUyZWQ3MmExZmMwMzk0YzkzY2I3ODVjYjMzYWVkNjA5ZmRkZTFhMDc0NTQ1ODRiNA=='
        self.trakt_user, self.trakt_password = getSetting("trakt_user"), getSetting("trakt_password")
        self.trakt_trending = 'http://api-v2launch.trakt.tv/movies/trending'
        self.trakt_watchlist = 'http://api-v2launch.trakt.tv/users/%s/watchlist/movies'
        self.trakt_collection = 'http://api-v2launch.trakt.tv/users/%s/collection/movies'
        self.trakt_tv_summary = 'http://api-v2launch.trakt.tv/shows/%s'
        self.trakt_tv_trending = 'http://api-v2launch.trakt.tv/shows/trending'
        self.trakt_tv_watchlist = 'http://api-v2launch.trakt.tv/users/%s/watchlist/shows'
        self.trakt_tv_collection = 'http://api-v2launch.trakt.tv/users/%s/collection/shows'
        self.trakt_tv_season_premieres = 'http://api-v2launch.trakt.tv/calendars/all/shows/premieres/%s/%s'
        self.trakt_tv_premieres = 'http://api-v2launch.trakt.tv/calendars/all/shows/new/%s/%s'
        self.trakt_tv_my_calendar = 'http://api-v2launch.trakt.tv/calendars/my/shows/%s/%s'
        self.trakt_tv_calendar = 'http://api-v2launch.trakt.tv/calendars/all/shows/%s/%s'
        self.trakt_lists = 'http://api-v2launch.trakt.tv/users/%s/lists'
        self.trakt_list = 'http://api-v2launch.trakt.tv/users/%s/lists/%s/items'
        self.trakt_history = 'http://api-v2launch.trakt.tv/sync/history'
        self.trakt_history_remove = 'http://api-v2launch.trakt.tv/sync/history/remove'
        self.trakt_collection_add = 'http://api-v2launch.trakt.tv/sync/collection'
        self.trakt_collection_remove = 'http://api-v2launch.trakt.tv/sync/collection/remove'
        self.trakt_watchlist_add = 'http://api-v2launch.trakt.tv/sync/watchlist'
        self.trakt_watchlist_remove = 'http://api-v2launch.trakt.tv/sync/watchlist/remove'
        self.trakt_list_add = 'http://api-v2launch.trakt.tv/users/%s/lists/%s/items'
        self.trakt_list_remove = 'http://api-v2launch.trakt.tv/users/%s/lists/%s/items/remove'
        self.trakt_watched = 'http://api-v2launch.trakt.tv/users/%s/watched/movies'
        self.trakt_tv_watched = 'http://api-v2launch.trakt.tv/users/%s/watched/shows'

        self.tvrage_base = 'http://services.tvrage.com'
        self.tvrage_search = 'http://services.tvrage.com/feeds/search.php?show=%s'
        self.tvrage_info = 'http://www.tvrage.com/shows/id-%s/episode_list/all'
        self.epguides_info = 'http://epguides.com/common/exportToCSV.asp?rage=%s'

        self.scn_base = 'http://www.movie25.ag'
        self.scn_link_1 = 'http://www.movie25.ag'
        self.scn_link_2 = 'http://translate.googleusercontent.com/translate_c?anno=2&hl=en&sl=mt&tl=en&u=http://www.movie25.ag'
        self.scn_link_3 = 'https://movie25.unblocked.pw'
        self.scn_added = '/new-releases/1'
        self.scn_added_hd = '/latest-hd-movies/1'

        self.scn_tv_base = 'http://m2v.ru'
        self.scn_tv_added = 'http://m2v.ru/?Part=11&func=part&page=1'

class people:
    def __init__(self):
        self.list = []

    def movies(self, query=None):
        if query == None:
            self.query = common.getUserInput(language(30382).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query == None or self.query == ''):
            self.query = link().imdb_people_search % urllib.quote_plus(self.query)
            self.imdb_list(self.query)
            for i in range(0, len(self.list)): self.list[i].update({'action': 'movies', 'url': link().imdb_people % self.list[i]['url']})
            index().rootList(self.list)
            return self.list

    def shows(self, query=None):
        if query == None:
            self.query = common.getUserInput(language(30382).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query == None or self.query == ''):
            self.query = link().imdb_people_search % urllib.quote_plus(self.query)
            self.imdb_list(self.query)
            for i in range(0, len(self.list)): self.list[i].update({'action': 'shows', 'url': link().imdb_tv_people % self.list[i]['url']})
            index().rootList(self.list)

    def imdb_list(self, url):
        try:
            result = getUrl(url, timeout='30').result
            result = result.decode('iso-8859-1').encode('utf-8')
            people = common.parseDOM(result, "tr", attrs = { "class": ".+? detailed" })
        except:
            return
        for i in people:
            try:
                name = common.parseDOM(i, "a", ret="title")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(i, "a", ret="href")[0]
                url = re.findall('nm(\d*)', url, re.I)[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(i, "img", ret="src")[0]
                if not ('._SX' in image or '._SY' in image): raise Exception()
                image = image.rsplit('._SX', 1)[0].rsplit('._SY', 1)[0] + '._SX500.' + image.rsplit('.', 1)[-1]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

class genres:
    def __init__(self):
        self.list = []

    def movies(self):
        self.list = index().cache(self.imdb_list, 24)
        for i in range(0, len(self.list)): self.list[i].update({'image': 'genres_movies.jpg', 'action': 'movies'})
        index().rootList(self.list)
        return self.list

    def shows(self):
        self.list = index().cache(self.imdb_list2, 24)
        for i in range(0, len(self.list)): self.list[i].update({'image': 'genres_shows.jpg', 'action': 'shows'})
        index().rootList(self.list)
        return self.list

    def imdb_list(self):
        try:
            result = getUrl(link().imdb_genre, timeout='30').result
            result = common.parseDOM(result, "table", attrs = { "class": "genre-table" })[0]
            genres = common.parseDOM(result, "h3")
        except:
            return

        for genre in genres:
            try:
                name = common.parseDOM(genre, "a")[0]
                name = name.split('<', 1)[0].rsplit('>', 1)[0].strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(genre, "a", ret="href")[0]
                url = re.compile('/genre/(.+?)/').findall(url)[0]
                if url == 'documentary': raise Exception()
                url = link().imdb_genres % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url})
            except:
                pass

        return self.list

    def imdb_list2(self):
        try:
            result = getUrl(link().imdb_genre, timeout='30').result
            result = common.parseDOM(result, "div", attrs = { "class": "article" })
            result = [i for i in result if str('"tv_genres"') in i][0]
            genres = common.parseDOM(result, "td")
        except:
            return

        for genre in genres:
            try:
                name = common.parseDOM(genre, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(genre, "a", ret="href")[0]
                try: url = re.compile('genres=(.+?)&').findall(url)[0]
                except: url = re.compile('/genre/(.+?)/').findall(url)[0]
                url = link().imdb_tv_genres % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url})
            except:
                pass

        return self.list

class languages:
    def __init__(self):
        self.list = []

    def movies(self):
        self.list = index().cache(self.imdb_list, 24)
        for i in range(0, len(self.list)): self.list[i].update({'image': 'languages_movies.jpg', 'action': 'movies'})
        index().rootList(self.list)
        return self.list

    def imdb_list(self):
        try:
            result = getUrl(link().imdb_language, timeout='30').result
            result = common.parseDOM(result, "table", attrs = { "class": "splash" })[0]
            languages = common.parseDOM(result, "td")
        except:
            return

        for language in languages:
            try:
                name = common.parseDOM(language, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(language, "a", ret="href")[0]
                url = re.compile('/language/(.+)').findall(url)[0]
                url = link().imdb_languages % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url})
            except:
                pass

        return self.list

class certificates:
    def __init__(self):
        self.list = []

    def movies(self):
        self.list = self.imdb_list()
        for i in range(0, len(self.list)): self.list[i].update({'image': 'certificates_movies.jpg', 'action': 'movies'})
        index().rootList(self.list)
        return self.list

    def shows(self):
        self.list = self.imdb_list2()
        for i in range(0, len(self.list)): self.list[i].update({'image': 'certificates_shows.jpg', 'action': 'shows'})
        index().rootList(self.list)
        return self.list

    def imdb_list(self):
        certificates = ['G', 'PG', 'PG-13', 'R', 'NC-17']

        for c in certificates:
            name = c.encode('utf-8')
            url = c.replace('-', '_').lower()
            url = link().imdb_certificates % url
            url = url.encode('utf-8')
            self.list.append({'name': name, 'url': url})

        return self.list

    def imdb_list2(self):
        certificates = ['TV-G', 'TV-PG', 'TV-14', 'TV-MA']

        for c in certificates:
            name = c.encode('utf-8')
            url = c.replace('-', '_').lower()
            url = link().imdb_tv_certificates % url
            url = url.encode('utf-8')
            self.list.append({'name': name, 'url': url})

        return self.list

class years:
    def __init__(self):
        self.list = []

    def movies(self):
        self.list = self.imdb_list()
        for i in range(0, len(self.list)): self.list[i].update({'image': 'years_movies.jpg', 'action': 'movies'})
        index().rootList(self.list)
        return self.list

    def imdb_list(self):
        year = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")

        for i in range(int(year)-0, int(year)-50, -1):
            name = str(i).encode('utf-8')
            url = link().imdb_years % (str(i), str(i))
            url = url.encode('utf-8')
            self.list.append({'name': name, 'url': url})

        return self.list

class userlists:
    def __init__(self):
        self.list = []

    def movies(self):
        if not (link().trakt_user == '' or link().trakt_password == ''): self.trakt_list()
        if not (link().imdb_user == ''): self.imdb_list()
        for i in range(0, len(self.list)): self.list[i].update({'image': 'userlists_movies.jpg', 'action': 'movies_userlist'})
        index().rootList(self.list)
        return self.list

    def shows(self):
        if not (link().trakt_user == '' or link().trakt_password == ''): self.trakt_list()
        if not (link().imdb_user == ''): self.imdb_list()
        for i in range(0, len(self.list)): self.list[i].update({'image': 'userlists_movies.jpg', 'action': 'shows_userlist', 'url': self.list[i]['url'].replace(link().imdb_list.split('?', 1)[-1], link().imdb_tv_list.split('?', 1)[-1])})
        index().rootList(self.list)
        return self.list

    def trakt_list(self):
        try:
            userlists = []
            url = link().trakt_lists % link().trakt_user
            result = getTrakt().result(url)
            userlists = json.loads(result)
        except:
            pass

        for userlist in userlists:
            try:
                name = userlist['name']
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = userlist['ids']['slug']
                url = link().trakt_list % (link().trakt_user, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url})
            except:
                pass

        return self.list

    def imdb_list(self):
        try:
            userlists = []
            result = getUrl(link().imdb_userlists % link().imdb_user, timeout='30').result
            result = result.decode('iso-8859-1').encode('utf-8')
            userlists = common.parseDOM(result, "div", attrs = { "class": "list_name" })
        except:
            pass

        for userlist in userlists:
            try:
                name = common.parseDOM(userlist, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(userlist, "a", ret="href")[0]
                url = url.split('/list/', 1)[-1].replace('/', '')
                url = link().imdb_list % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url})
            except:
                pass

        return self.list

class channels:
    def __init__(self):
        self.list = []
        self.sky_now_link = 'http://epgservices.sky.com/5.1.1/api/2.0/channel/json/%s/now/nn/0'
        self.sky_programme_link = 'http://tv.sky.com/programme/channel/%s/%s/%s.json'

    def movies(self):
        channelDict = [('01', 'Sky Premiere', '1409'), ('02', 'Sky Premiere +1', '1823'), ('03', 'Sky Showcase', '1814'), ('04', 'Sky Greats', '1815'), ('05', 'Sky Disney', '1838'), ('06', 'Sky Family', '1808'), ('07', 'Sky Action', '1001'), ('08', 'Sky Comedy', '1002'), ('09', 'Sky Crime', '1818'), ('10', 'Sky Drama', '1816'), ('11', 'Sky Sci Fi', '1807'), ('12', 'Sky Select', '1811'), ('13', 'Film4', '1627'), ('14', 'TCM', '5605')] 

        threads = []
        for i in channelDict: threads.append(Thread(self.sky_list, i[0], i[1], i[2]))
        [i.start() for i in threads]
        [i.join() for i in threads]

        threads = []
        for i in range(0, len(self.list)): threads.append(Thread(self.imdb_search, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        self.list = [i for i in self.list if not i['imdb'] == '0000000']
        self.list = sorted(self.list, key=itemgetter('num'))

        index().channelList(self.list)
        return self.list

    def sky_list(self, num, channel, id):
        try:
            url = self.sky_now_link % id
            result = getUrl(url, timeout='10').result
            result = json.loads(result)
            match = result['listings'][id][0]['url']

            dt = self.uk_datetime()
            dt1 = '%04d' % dt.year + '-' + '%02d' % dt.month + '-' + '%02d' % dt.day
            dt2 = int(dt.hour)
            if (dt2 < 6): dt2 = 0
            elif (dt2 >= 6 and dt2 < 12): dt2 = 1
            elif (dt2 >= 12 and dt2 < 18): dt2 = 2
            elif (dt2 >= 18): dt2 = 3
            url = self.sky_programme_link % (id, str(dt1), str(dt2))

            result = getUrl(url, timeout='10').result
            result = json.loads(result)
            result = result['listings'][id]
            result = [i for i in result if i['url'] == match][0]

            year = result['d']
            year = re.findall('[(](\d{4})[)]', year)[0].strip()
            year = year.encode('utf-8')

            title = result['t']
            title = title.replace('(%s)' % year, '').strip()
            title = common.replaceHTMLCodes(title)
            title = title.encode('utf-8')

            try: duration = re.compile('[(](\d+?) mins[)]').findall(result['d'])[0]
            except: duration = '120'
            duration = str(duration)
            if duration == '': duration = '120'
            duration = common.replaceHTMLCodes(duration)
            duration = duration.encode('utf-8')

            mpaa = result['rr']
            if mpaa == '' : mpaa = '0'
            mpaa = common.replaceHTMLCodes(mpaa)
            mpaa = mpaa.encode('utf-8')

            plot = result['d']
            plot = plot.rsplit('.', 1)[0].strip()
            if not plot.endswith('.'): plot += '.'
            if plot == '.': plot = '0'
            plot = common.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')

            tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
            try: tagline = tagline.encode('utf-8')
            except: pass

            self.list.append({'name': channel, 'title': title, 'year': year, 'imdb': '0000000', 'tvdb': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'date': '0', 'genre': '0', 'url': '0', 'poster': '0', 'fanart': '0', 'studio': '0', 'duration': duration, 'rating': '0', 'votes': '0', 'mpaa': mpaa, 'director': '0', 'plot': plot, 'plotoutline': tagline, 'tagline': tagline, 'num': num})
        except:
            return

    def imdb_search(self, i):
        try:
            match = []
            title = self.list[i]['title']
            year = self.list[i]['year']
            url = link().imdb_search % urllib.quote_plus(title)
            result = getUrl(url, timeout='30').result
            result = common.replaceHTMLCodes(result)
            result = json.loads(result)
            for x in result.keys(): match += result[x]

            title = self.cleantitle_movie(title)
            years = [str(year), str(int(year)+1), str(int(year)-1)]
            match = [x for x in match if title == self.cleantitle_movie(x['title'])]
            match = [x for x in match if any(x['title_description'].startswith(y) for y in years)][0]

            title = match['title']
            title = common.replaceHTMLCodes(title)
            title = title.encode('utf-8')

            imdb = match['id']
            imdb = re.sub('[^0-9]', '', str(imdb))
            imdb = imdb.encode('utf-8')

            url = link().imdb_title % imdb
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            self.list[i].update({'title': title, 'imdb': imdb, 'url': url})
        except:
            pass

    def cleantitle_movie(self, title):
        title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def uk_datetime(self):
        dt = datetime.datetime.utcnow() + datetime.timedelta(hours = 0)
        d = datetime.datetime(dt.year, 4, 1)
        dston = d - datetime.timedelta(days=d.weekday() + 1)
        d = datetime.datetime(dt.year, 11, 1)
        dstoff = d - datetime.timedelta(days=d.weekday() + 1)
        if dston <=  dt < dstoff:
            return dt + datetime.timedelta(hours = 1)
        else:
            return dt

class movies:
    def __init__(self):
        self.list = []

    def get(self, url, idx=True):
        if url.startswith(link().imdb_base) and not ('/user/' in url or '/list/' in url):
            self.list = index().cache(self.imdb_list, 24, url)
        elif url.startswith(link().imdb_base):
            self.list = index().cache(self.imdb_list2, 0, url, idx)
        elif url.startswith(link().tmdb_base):
            self.list = index().cache(self.tmdb_list, 24, url)
        elif url.startswith(link().trakt_base):
            self.list = index().cache(self.trakt_list, 0, url)
            try: self.list = sorted(self.list, key=itemgetter('title'))
            except: pass
        elif url.startswith(link().scn_base):
            self.list = index().cache(self.scn_list, 24, url)
        if idx == True: index().movieList(self.list)
        return self.list

    def popular(self):
        url = link().imdb_popular
        self.list = index().cache(self.imdb_list, 24, url)
        index().movieList(self.list)
        return self.list

    def boxoffice(self):
        url = link().imdb_boxoffice
        self.list = index().cache(self.imdb_list, 24, url)
        index().movieList(self.list)
        return self.list

    def views(self):
        url = link().imdb_views
        self.list = index().cache(self.imdb_list, 24, url)
        index().movieList(self.list)
        return self.list

    def oscars(self):
        url = link().imdb_oscars
        self.list = index().cache(self.imdb_list, 24, url)
        index().movieList(self.list)
        return self.list

    def added(self):
        url = link().scn_added
        self.list = index().cache(self.scn_list, 24, url)
        index().movieList(self.list)
        return self.list

    def added_hd(self):
        url = link().scn_added_hd
        self.list = index().cache(self.scn_list, 24, url)
        index().movieList(self.list)
        return self.list

    def theaters(self):
        url = link().tmdb_theaters % link().tmdb_key
        self.list = index().cache(self.tmdb_list, 24, url)
        index().movieList(self.list)
        return self.list

    def trending(self):
        url = link().trakt_trending
        self.list = index().cache(self.trakt_list, 24, url)
        index().movieList(self.list)
        return self.list

    def featured(self):
        url = link().trakt_trending
        self.list = index().cache(self.trakt_list, 24, url)
        year = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")
        years = [str(year), str(int(year)-1)]
        try: self.list = [i for i in self.list if i['year'] in years]
        except: return
        index().movieList(self.list)
        return self.list

    def trakt_collection(self):
        url = link().trakt_collection % link().trakt_user
        self.list = index().cache(self.trakt_list, 0, url)
        try: self.list = sorted(self.list, key=itemgetter('title'))
        except: return
        index().movieList(self.list)
        return self.list

    def trakt_watchlist(self):
        url = link().trakt_watchlist % link().trakt_user
        self.list = index().cache(self.trakt_list, 0, url)
        try: self.list = sorted(self.list, key=itemgetter('title'))
        except: return
        index().movieList(self.list)
        return self.list

    def imdb_watchlist(self):
        url = link().imdb_watchlist % link().imdb_user
        self.list = index().cache(self.imdb_list2, 0, url)
        index().movieList(self.list)
        return self.list

    def search(self, query=None):
        if query == None:
            self.query = common.getUserInput(language(30382).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query == None or self.query == ''):
            self.list = self.imdb_list3(self.query)
            index().movieList(self.list)
            return self.list

    def favourites(self):
        try:
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='Movie'")
            match = dbcur.fetchall()
            match = [(i[0], i[2], i[3], i[6]) for i in match]

            for imdb, title, year, poster in match:
                try:
                    try: title = eval(title.encode('utf-8'))
                    except: title = title.encode('utf-8')
                    name = '%s (%s)' % (title, year.encode('utf-8'))
                    imdb = re.sub('[^0-9]', '', imdb)
                    self.list.append({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'date': '0', 'genre': '0', 'url': '0', 'poster': poster, 'fanart': '0', 'studio': '0', 'duration': '0', 'rating': '0', 'votes': '0', 'mpaa': '0', 'director': '0', 'plot': '0', 'plotoutline': '0', 'tagline': '0'})
                except:
                    pass

            threads = []
            for i in range(0, len(self.list)): threads.append(Thread(self.tmdb_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

            self.list = sorted(self.list, key=itemgetter('title'))
            index().movieList(self.list)
            return self.list
        except:
            return

    def cleantitle_movie(self, title):
        title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def imdb_list(self, url):
        try:
            result = getUrl(url, timeout='30').result
            result = result.decode('iso-8859-1').encode('utf-8')
            movies = common.parseDOM(result, "tr", attrs = { "class": ".+?" })
        except:
            return

        try:
            next = common.parseDOM(result, "span", attrs = { "class": "pagination" })[0]
            name = common.parseDOM(next, "a")[-1]
            if 'laquo' in name: raise Exception()
            next = common.parseDOM(next, "a", ret="href")[-1]
            next = '%s%s' % (link().imdb_base, next)
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for movie in movies:
            try:
                title = common.parseDOM(movie, "a")[1]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = common.parseDOM(movie, "span", attrs = { "class": "year_type" })[0]
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                url = common.parseDOM(movie, "a", ret="href")[0]
                url = '%s%s' % (link().imdb_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                imdb = re.sub('[^0-9]', '', url.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')

                poster = '0'
                try: poster = common.parseDOM(movie, "img", ret="src")[0]
                except: pass
                if not ('_SX' in poster or '_SY' in poster): poster = '0'
                poster = re.sub('_SX\d*|_SY\d*|_CR\d+?,\d+?,\d+?,\d*','_SX500', poster)
                poster = common.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                genre = common.parseDOM(movie, "span", attrs = { "class": "genre" })
                genre = common.parseDOM(genre, "a")
                genre = " / ".join(genre)
                if genre == '': genre = '0'
                genre = common.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')

                try: duration = common.parseDOM(movie, "span", attrs = { "class": "runtime" })[0]
                except: duration = '0'
                duration = re.sub('[^0-9]', '', duration)
                if duration == '': duration = '0'
                duration = common.replaceHTMLCodes(duration)
                duration = duration.encode('utf-8')

                try: rating = common.parseDOM(movie, "span", attrs = { "class": "rating-rating" })[0]
                except: rating = '0'
                try: rating = common.parseDOM(movie, "span", attrs = { "class": "value" })[0]
                except: rating = '0'
                if rating == '': rating = '0'
                rating = common.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                try: votes = common.parseDOM(movie, "div", ret="title", attrs = { "class": "rating rating-list" })[0]
                except: votes = '0'
                try: votes = votes = re.compile('[(](.+?) votes[)]').findall(votes)[0]
                except: votes = '0'
                if votes == '': votes = '0'
                votes = common.replaceHTMLCodes(votes)
                votes = votes.encode('utf-8')

                try: mpaa = common.parseDOM(movie, "span", attrs = { "class": "certificate" })[0]
                except: mpaa = '0'
                try: mpaa = common.parseDOM(mpaa, "span", ret="title")[0]
                except: mpaa = '0'
                if mpaa == '' or mpaa == 'NOT_RATED': mpaa = '0'
                mpaa = mpaa.replace('_', '-')
                mpaa = common.replaceHTMLCodes(mpaa)
                mpaa = mpaa.encode('utf-8')

                director = common.parseDOM(movie, "span", attrs = { "class": "credit" })
                try: director = director[0].split('With:', 1)[0].strip()
                except: director = '0'
                director = common.parseDOM(director, "a")
                director = " / ".join(director)
                if director == '': director = '0'
                director = common.replaceHTMLCodes(director)
                director = director.encode('utf-8')

                try: plot = common.parseDOM(movie, "span", attrs = { "class": "outline" })[0]
                except: plot = '0'
                plot = plot.rsplit('<span>', 1)[0].strip()
                if plot == '': plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                try: tagline = tagline.encode('utf-8')
                except: pass

                self.list.append({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'date': '0', 'genre': genre, 'url': url, 'poster': poster, 'fanart': '0', 'studio': '0', 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'plot': plot, 'plotoutline': tagline, 'tagline': tagline, 'next': next})
            except:
                pass

        threads = []
        for i in range(0, len(self.list)): threads.append(Thread(self.tmdb_info, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        return self.list

    def imdb_list2(self, url, idx=True):
        try:
            def imdb_watchlist_id(url):
                id = getUrl(url, timeout='30').result
                id = re.compile('/export[?]list_id=(ls\d*)').findall(id)[0]
                return id

            if url == link().imdb_watchlist % link().imdb_user:
                url = index().cache(imdb_watchlist_id, 8640, url)
                url = link().imdb_list % url

            result = getUrl(url, timeout='30').result

            try:
                if idx == True: raise Exception()
                pages = common.parseDOM(result, "div", attrs = { "class": "desc" })[0]
                pages = re.compile('Page \d+? of (\d*)').findall(pages)[0]
                for i in range(1, int(pages)):
                    u = url.replace('&start=1', '&start=%s' % str(i*100+1))
                    try: result += getUrl(u, timeout='30').result
                    except: pass
            except:
                pass

            result = result.replace('\n','')
            result = result.decode('iso-8859-1').encode('utf-8')
            movies = common.parseDOM(result, "div", attrs = { "class": "list_item.+?" })
        except:
            return

        try:
            next = common.parseDOM(result, "div", attrs = { "class": "pagination" })[-1]
            name = common.parseDOM(next, "a")[-1]
            if 'laquo' in name: raise Exception()
            next = common.parseDOM(next, "a", ret="href")[-1]
            next = '%s%s' % (url.split('?', 1)[0], next)
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for movie in movies:
            try:
                title = common.parseDOM(movie, "a", attrs = { "onclick": ".+?" })[-1]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = common.parseDOM(movie, "span", attrs = { "class": "year_type" })[0]
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                url = common.parseDOM(movie, "a", ret="href")[0]
                url = '%s%s' % (link().imdb_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                imdb = re.sub('[^0-9]', '', url.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')

                poster = '0'
                try: poster = common.parseDOM(movie, "img", ret="src")[0]
                except: pass
                try: poster = common.parseDOM(movie, "img", ret="loadlate")[0]
                except: pass
                if not ('_SX' in poster or '_SY' in poster): poster = '0'
                poster = re.sub('_SX\d*|_SY\d*|_CR\d+?,\d+?,\d+?,\d*','_SX500', poster)
                poster = common.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                try: duration = common.parseDOM(movie, "div", attrs = { "class": "item_description" })[0]
                except: duration = '0'
                try: duration = common.parseDOM(duration, "span")[-1]
                except: duration = '0'
                duration = re.sub('[^0-9]', '', duration)
                if duration == '': duration = '0'
                duration = common.replaceHTMLCodes(duration)
                duration = duration.encode('utf-8')

                try: rating = common.parseDOM(movie, "span", attrs = { "class": "rating-rating" })[0]
                except: rating = '0'
                try: rating = common.parseDOM(movie, "span", attrs = { "class": "value" })[0]
                except: rating = '0'
                if rating == '' or rating == '-': rating = '0'
                rating = common.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                try: votes = common.parseDOM(movie, "div", ret="title", attrs = { "class": "rating rating-list" })[0]
                except: votes = '0'
                try: votes = votes = re.compile('[(](.+?) votes[)]').findall(votes)[0]
                except: votes = '0'
                if votes == '': votes = '0'
                votes = common.replaceHTMLCodes(votes)
                votes = votes.encode('utf-8')

                director = common.parseDOM(movie, "div", attrs = { "class": "secondary" })
                director = [i for i in director if i.startswith('Director:')]
                try: director = common.parseDOM(director[0], "a")
                except: director = '0'
                director = " / ".join(director)
                if director == '': director = '0'
                director = common.replaceHTMLCodes(director)
                director = director.encode('utf-8')

                try: plot = common.parseDOM(movie, "div", attrs = { "class": "item_description" })[0]
                except: plot = '0'
                plot = plot.rsplit('<span>', 1)[0].strip()
                if plot == '': plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                try: tagline = tagline.encode('utf-8')
                except: pass

                self.list.append({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'date': '0', 'genre': '0', 'url': url, 'poster': poster, 'fanart': '0', 'studio': '0', 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': '0', 'director': director, 'plot': plot, 'plotoutline': tagline, 'tagline': tagline, 'next': next})
            except:
                pass

        return self.list

    def imdb_list3(self, url):
        try:
            url = link().imdb_search % urllib.quote_plus(url)

            result = getUrl(url, timeout='30').result
            result = common.replaceHTMLCodes(result)
            result = json.loads(result)

            movies = []
            try: movies += result['title_popular']
            except: pass
            try: movies += result['title_exact']
            except: pass
            try: movies += result['title_substring']
            except: pass
        except:
            return

        for movie in movies:
            try:
                year = movie['title_description']
                year = year.split(',', 1)[0].lower()
                if any(x in year for x in ['tv series', 'tv mini-series', 'video game']): raise Exception()
                year = re.sub('[^0-9]', '', str(year))[:4]
                if not year.isdigit(): raise Exception()

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                title = movie['title']
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                imdb = movie['id']
                imdb = re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                url = link().imdb_title % imdb
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'date': '0', 'genre': '0', 'url': url, 'poster': '0', 'fanart': '0', 'studio': '0', 'duration': '0', 'rating': '0', 'votes': '0', 'mpaa': '0', 'director': '0', 'plot': '0', 'plotoutline': '0', 'tagline': '0'})
            except:
                pass

        self.list = self.list[:50]

        threads = []
        for i in range(0, len(self.list)): threads.append(Thread(self.tmdb_info, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        filter = [i for i in self.list if not i['poster'] == '0']
        filter += [i for i in self.list if i['poster'] == '0']
        self.list = filter

        return self.list

    def tmdb_list(self, url):
        try:
            result = getUrl(url, timeout='10').result
            result = json.loads(result)
            movies = result['results']
        except:
            return

        try:
            next = str(result['page'])
            if next == '5': raise Exception()
            next = '%s&page=%s' % (url.split('&page=', 1)[0], str(int(next)+1))
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for movie in movies:
            try:
                title = movie['title']
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = movie['release_date']
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                tmdb = movie['id']
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                tmdb = tmdb.encode('utf-8')

                poster = movie['poster_path']
                if poster == '' or poster == None: raise Exception()
                else: poster = '%s%s' % (link().tmdb_image2, poster)
                poster = common.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                fanart = movie['backdrop_path']
                if fanart == '' or fanart == None: fanart = '0'
                if not fanart == '0': fanart = '%s%s' % (link().tmdb_image, fanart)
                fanart = common.replaceHTMLCodes(fanart)
                fanart = fanart.encode('utf-8')

                rating = str(movie['vote_average'])
                if rating == '' or rating == None: rating = '0'
                rating = common.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                votes = str(movie['vote_count'])
                try: votes = str(format(int(votes),',d'))
                except: pass
                if votes == '' or votes == None: votes = '0'
                votes = common.replaceHTMLCodes(votes)
                votes = votes.encode('utf-8')

                self.list.append({'name': name, 'title': title, 'year': year, 'imdb': '0000000', 'tvdb': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'date': '0', 'genre': '0', 'url': '0', 'poster': poster, 'fanart': fanart, 'studio': '0', 'duration': '0', 'rating': rating, 'votes': votes, 'mpaa': '0', 'director': '0', 'plot': '0', 'plotoutline': '0', 'tagline': '0', 'tmdb': tmdb, 'next': next})
            except:
                pass

        threads = []
        for i in range(0, len(self.list)): threads.append(Thread(self.tmdb_info2, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        return self.list

    def trakt_list(self, url):
        try:
            url += '?extended=full,images&limit=200'
            result = getTrakt().result(url)
            result = json.loads(result)

            movies = []
            for i in result:
                try: movies.append(i['movie'])
                except: pass
        except:
            return

        for movie in movies:
            try:
                title = movie['title']
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = movie['year']
                year = re.sub('[^0-9]', '', str(year))
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                imdb = movie['ids']['imdb']
                if imdb == None or imdb == '': imdb = '0000000'
                imdb = re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                url = link().imdb_title % imdb
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                genre = movie['genres']
                genre = [i.title() for i in genre]
                if genre == []: genre = '0'
                genre = " / ".join(genre)
                genre = common.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')

                poster = '0'
                try: poster = movie['images']['poster']['medium']
                except: pass
                if poster == None or not '/posters/' in poster: poster = '0'
                poster = poster.rsplit('?', 1)[0]
                poster = common.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                fanart = '0'
                try: fanart = movie['images']['fanart']['full']
                except: pass
                if fanart == None or not '/fanarts/' in fanart: fanart = '0'
                fanart = fanart.rsplit('?', 1)[0]
                fanart = common.replaceHTMLCodes(fanart)
                fanart = fanart.encode('utf-8')

                try: duration = str(movie['runtime'])
                except: duration = '0'
                if duration == None: duration = '0'
                duration = common.replaceHTMLCodes(duration)
                duration = duration.encode('utf-8')

                try: rating = str(movie['rating'])
                except: rating = '0'
                if rating == None or rating == '0.0': rating = '0'
                rating = common.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                try: votes = str(movie['votes'])
                except: votes = '0'
                try: votes = str(format(int(votes),',d'))
                except: pass
                if votes == None: votes = '0'
                votes = common.replaceHTMLCodes(votes)
                votes = votes.encode('utf-8')

                mpaa = movie['certification']
                if mpaa == None: mpaa = '0'
                mpaa = common.replaceHTMLCodes(mpaa)
                mpaa = mpaa.encode('utf-8')

                plot = movie['overview']
                if plot == None: plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                plotoutline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                try: plotoutline = plotoutline.encode('utf-8')
                except: pass

                try: tagline = movie['tagline']
                except: tagline = None
                if tagline == None and not plot == '0': tagline = plotoutline
                elif tagline == None: tagline = '0'
                tagline = common.replaceHTMLCodes(tagline)
                try: tagline = tagline.encode('utf-8')
                except: pass

                self.list.append({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'date': '0', 'genre': genre, 'url': url, 'poster': poster, 'fanart': fanart, 'studio': '0', 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': '0', 'plot': plot, 'plotoutline': plotoutline, 'tagline': tagline})
            except:
                pass

        return self.list

    def scn_list(self, url):
        try:
            result = ''
            try: url = re.compile('//.+?(/.+)').findall(url)[0]
            except: pass
            links = [link().scn_link_1, link().scn_link_2, link().scn_link_3]
            for base_link in links:
                try: result = getUrl(base_link + url).result
                except: result = ''
                if 'movie_table' in result: break

            result = result.decode('iso-8859-1').encode('utf-8')
            movies = common.parseDOM(result, "div", attrs = { "class": "movie_table" })
        except:
            return

        try:
            next = common.parseDOM(result, "div", attrs = { "class": "count_text" })[0]
            next = re.compile('(<a.+?</a>)').findall(next)
            next = [i for i in next if '>Next<' in i][-1]
            next = re.compile('href=(.+?)>').findall(next)[-1]
            next = re.sub('\'|\"','', next)
            next = common.replaceHTMLCodes(next)
            try: next = urlparse.parse_qs(urlparse.urlparse(next).query)['u'][0]
            except: pass
            next = urlparse.urljoin(link().scn_base, next)
            next = next.encode('utf-8')
        except:
            next = ''

        for movie in movies:
            try:
                title = common.parseDOM(movie, "a", ret="title")[0]
                title = re.compile('(.+?) [(]\d{4}[)]$').findall(title)[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = common.parseDOM(movie, "a", ret="title")[0]
                year = re.compile('.+? [(](\d{4})[)]$').findall(year)[0]
                year = year.encode('utf-8')

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                url = common.parseDOM(movie, "a", ret="href")[0]
                url = common.replaceHTMLCodes(url)
                try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
                except: pass
                url = urlparse.urljoin(link().scn_base, url)
                url = url.encode('utf-8')

                poster = '0'
                try: poster = common.parseDOM(movie, "img", ret="src")[0]
                except: pass
                poster = common.replaceHTMLCodes(poster)
                try: poster = urlparse.parse_qs(urlparse.urlparse(poster).query)['u'][0]
                except: pass
                poster = poster.encode('utf-8')

                genre = common.parseDOM(movie, "div", attrs = { "class": "movie_about_genre" })
                genre = common.parseDOM(genre, "a")
                genre = " / ".join(genre)
                if genre == '': genre = '0'
                genre = common.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')

                self.list.append({'name': name, 'title': title, 'year': year, 'imdb': '0000000', 'tvdb': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'date': '0', 'genre': genre, 'url': '0', 'poster': poster, 'fanart': '0', 'studio': '0', 'duration': '0', 'rating': '0', 'votes': '0', 'mpaa': '0', 'director': '0', 'plot': '0', 'plotoutline': '0', 'tagline': '0', 'next': next})
            except:
                pass

        threads = []
        for i in range(0, len(self.list)): threads.append(Thread(self.imdb_info, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        self.list = [i for i in self.list if not i['imdb'] == '0000000']

        threads = []
        for i in range(0, len(self.list)): threads.append(Thread(self.tmdb_info, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        return self.list

    def imdb_info(self, i):
        try:
            match = []
            title = self.list[i]['title']
            year = self.list[i]['year']
            url = link().imdb_search % urllib.quote_plus(title)
            result = getUrl(url, timeout='30').result
            result = common.replaceHTMLCodes(result)
            result = json.loads(result)
            for x in result.keys(): match += result[x]

            title = self.cleantitle_movie(title)
            years = [str(year), str(int(year)+1), str(int(year)-1)]
            match = [x for x in match if title == self.cleantitle_movie(x['title'])]
            match = [x for x in match if any(x['title_description'].startswith(y) for y in years)][0]

            title = match['title']
            if title == '' or title == None: title = '0'
            title = common.replaceHTMLCodes(title)
            title = title.encode('utf-8')
            if not title == '0': self.list[i].update({'title': title})

            year = match['title_description']
            year = re.sub('[^0-9]', '', str(year))[:4]
            self.list[i].update({'year': year})

            name = '%s (%s)' % (self.list[i]['title'], self.list[i]['year'])
            try: name = name.encode('utf-8')
            except: pass
            self.list[i].update({'name': name})

            imdb = match['id']
            imdb = re.sub('[^0-9]', '', str(imdb))
            imdb = imdb.encode('utf-8')
            self.list[i].update({'imdb': imdb})

            url = link().imdb_title % imdb
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            self.list[i].update({'url': url})
        except:
            pass

    def tmdb_info(self, i):
        try:
            url = link().tmdb_info % (self.list[i]['imdb'], link().tmdb_key)
            result = getUrl(url, timeout='10').result
            result = json.loads(result)

            title = result['title']
            if title == '' or title == None: title = '0'
            title = common.replaceHTMLCodes(title)
            title = title.encode('utf-8')
            if not title == '0': self.list[i].update({'title': title})

            try: year = str(result['release_date'])
            except: year = '0000'
            year = re.compile('(\d{4})').findall(year)[0]
            year = year.encode('utf-8')
            if not year == '0000': self.list[i].update({'year': year})

            poster = result['poster_path']
            if poster == '' or poster == None: poster = '0'
            if not poster == '0': poster = '%s%s' % (link().tmdb_image2, poster)
            poster = common.replaceHTMLCodes(poster)
            poster = poster.encode('utf-8')
            if not poster == '0': self.list[i].update({'poster': poster})

            fanart = result['backdrop_path']
            if fanart == '' or fanart == None: fanart = '0'
            if not fanart == '0': fanart = '%s%s' % (link().tmdb_image, fanart)
            fanart = common.replaceHTMLCodes(fanart)
            fanart = fanart.encode('utf-8')
            if not fanart == '0': self.list[i].update({'fanart': fanart})

            genre = result['genres']
            try: genre = [x['name'] for x in genre]
            except: genre = '0'
            if genre == '' or genre == None or genre == []: genre = '0'
            genre = " / ".join(genre)
            genre = common.replaceHTMLCodes(genre)
            genre = genre.encode('utf-8')
            if not genre == '0': self.list[i].update({'genre': genre})

            studio = result['production_companies']
            try: studio = [x['name'] for x in studio][0]
            except: studio = '0'
            if studio == '' or studio == None: studio = '0'
            studio = common.replaceHTMLCodes(studio)
            studio = studio.encode('utf-8')
            if not studio == '0': self.list[i].update({'studio': studio})

            try: duration = str(result['runtime'])
            except: duration = '0'
            if duration == '' or duration == None or not self.list[i]['duration'] == '0': duration = '0'
            duration = common.replaceHTMLCodes(duration)
            duration = duration.encode('utf-8')
            if not duration == '0': self.list[i].update({'duration': duration})

            rating = str(result['vote_average'])
            if rating == '' or rating == None or not self.list[i]['rating'] == '0': rating = '0'
            rating = common.replaceHTMLCodes(rating)
            rating = rating.encode('utf-8')
            if not rating == '0': self.list[i].update({'rating': rating})

            votes = str(result['vote_count'])
            try: votes = str(format(int(votes),',d'))
            except: pass
            if votes == '' or votes == None or not self.list[i]['votes'] == '0': votes = '0'
            votes = common.replaceHTMLCodes(votes)
            votes = votes.encode('utf-8')
            if not votes == '0': self.list[i].update({'votes': votes})

            plot = result['overview']
            if plot == '' or plot == None: plot = '0'
            plot = common.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')
            if not plot == '0': self.list[i].update({'plot': plot})

            tagline = result['tagline']
            if (tagline == '' or tagline == None) and not plot == '0': tagline = plot.split('.', 1)[0]
            elif tagline == '' or tagline == None: tagline = '0'
            tagline = common.replaceHTMLCodes(tagline)
            tagline = tagline.encode('utf-8')
            if not tagline == '0': self.list[i].update({'tagline': tagline})
        except:
            pass

    def tmdb_info2(self, i):
        try:
            url = link().tmdb_info2 % (self.list[i]['tmdb'], link().tmdb_key)
            result = getUrl(url, timeout='10').result
            result = json.loads(result)

            imdb = result['imdb_id']
            imdb = re.sub('[^0-9]', '', str(imdb))
            imdb = imdb.encode('utf-8')
            self.list[i].update({'imdb': imdb})

            url = link().imdb_title % imdb
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            self.list[i].update({'url': url})

            genre = result['genres']
            try: genre = [x['name'] for x in genre]
            except: genre = '0'
            if genre == '' or genre == None or genre == []: genre = '0'
            genre = " / ".join(genre)
            genre = common.replaceHTMLCodes(genre)
            genre = genre.encode('utf-8')
            if not genre == '0': self.list[i].update({'genre': genre})

            studio = result['production_companies']
            try: studio = [x['name'] for x in studio][0]
            except: studio = '0'
            if studio == '' or studio == None: studio = '0'
            studio = common.replaceHTMLCodes(studio)
            studio = studio.encode('utf-8')
            if not studio == '0': self.list[i].update({'studio': studio})

            try: duration = str(result['runtime'])
            except: duration = '0'
            if duration == '' or duration == None: fanart = '0'
            duration = common.replaceHTMLCodes(duration)
            duration = duration.encode('utf-8')
            if not duration == '0': self.list[i].update({'duration': duration})

            plot = result['overview']
            if plot == '' or plot == None: plot = '0'
            plot = common.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')
            if not plot == '0': self.list[i].update({'plot': plot})

            tagline = result['tagline']
            if (tagline == '' or tagline == None) and not plot == '0': tagline = plot.split('.', 1)[0]
            elif tagline == '' or tagline == None: tagline = '0'
            tagline = common.replaceHTMLCodes(tagline)
            tagline = tagline.encode('utf-8')
            if not tagline == '0': self.list[i].update({'tagline': tagline})
        except:
            pass

class shows:
    def __init__(self):
        self.list = []

    def get(self, url, idx=True):
        if url.startswith(link().imdb_base) and not ('/user/' in url or '/list/' in url):
            self.list = index().cache(self.imdb_list, 24, url)
        elif url.startswith(link().imdb_base):
            self.list = index().cache(self.imdb_list2, 0, url, idx)
        elif url.startswith(link().trakt_base):
            self.list = index().cache(self.trakt_list, 0, url)
            try: self.list = sorted(self.list, key=itemgetter('title'))
            except: pass
        if idx == True: index().showList(self.list)
        return self.list

    def popular(self):
        url = link().imdb_tv_popular
        self.list = index().cache(self.imdb_list, 24, url)
        index().showList(self.list)
        return self.list

    def active(self):
        url = link().imdb_tv_active
        self.list = index().cache(self.imdb_list, 24, url)
        index().showList(self.list)
        return self.list

    def rating(self):
        url = link().imdb_tv_rating
        self.list = index().cache(self.imdb_list, 24, url)
        index().showList(self.list)
        return self.list

    def views(self):
        url = link().imdb_tv_views
        self.list = index().cache(self.imdb_list, 24, url)
        index().showList(self.list)
        return self.list

    def trending(self):
        url = link().trakt_tv_trending
        self.list = index().cache(self.trakt_list, 24, url)
        index().showList(self.list)
        return self.list

    def season_premieres(self):
        now = datetime.datetime.utcnow() - datetime.timedelta(hours = 5)
        date = datetime.date(now.year, now.month, now.day) - datetime.timedelta(days=32)
        url = link().trakt_tv_season_premieres % (str(date), '31')
        self.list = index().cache(self.trakt_list, 24, url)
        self.list = [i for i in self.list if not i['imdb'] == '0000000']
        try: self.list = sorted(self.list, key=itemgetter('title'))
        except: return
        index().showList(self.list)
        return self.list

    def premieres(self):
        now = datetime.datetime.utcnow() - datetime.timedelta(hours = 5)
        date = datetime.date(now.year, now.month, now.day) - datetime.timedelta(days=32)
        url = link().trakt_tv_premieres % (str(date), '31')
        self.list = index().cache(self.trakt_list, 24, url)
        self.list = [i for i in self.list if not i['imdb'] == '0000000']
        try: self.list = sorted(self.list, key=itemgetter('title'))
        except: return
        index().showList(self.list)
        return self.list

    def trakt_collection(self):
        url = link().trakt_tv_collection % link().trakt_user
        self.list = index().cache(self.trakt_list, 0, url)
        try: self.list = sorted(self.list, key=itemgetter('title'))
        except: return
        index().showList(self.list)
        return self.list

    def trakt_watchlist(self):
        url = link().trakt_tv_watchlist % link().trakt_user
        self.list = index().cache(self.trakt_list, 0, url)
        try: self.list = sorted(self.list, key=itemgetter('title'))
        except: return
        index().showList(self.list)
        return self.list

    def imdb_watchlist(self):
        url = link().imdb_watchlist % link().imdb_user
        self.list = index().cache(self.imdb_list2, 0, url)
        index().showList(self.list)
        return self.list

    def search(self, query=None):
        if query == None:
            self.query = common.getUserInput(language(30382).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query == None or self.query == ''):
            self.list = self.imdb_list3(self.query)
            index().showList(self.list)
            return self.list

    def favourites(self):
        try:
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='TV Show'")
            match = dbcur.fetchall()
            match = [(i[0], i[2], i[3], i[6]) for i in match]

            for imdb, title, year, poster in match:
                try:
                    try: title = eval(title.encode('utf-8'))
                    except: title = title.encode('utf-8')
                    imdb = re.sub('[^0-9]', '', imdb)
                    self.list.append({'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'genre': '0', 'url': '0', 'poster': poster, 'banner': poster, 'fanart': '0', 'studio': '0', 'premiered': '0', 'duration': '0', 'rating': '0', 'mpaa': '0', 'plot': '0'})
                except:
                    pass

            threads = []
            for i in range(0, len(self.list)): threads.append(Thread(self.tvdb_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

            self.list = sorted(self.list, key=itemgetter('title'))
            index().showList(self.list)
            return self.list
        except:
            return

    def cleantitle_tv(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU|\d{4})(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def imdb_list(self, url):
        try:
            result = getUrl(url, timeout='30').result
            result = result.decode('iso-8859-1').encode('utf-8')
            shows = common.parseDOM(result, "tr", attrs = { "class": ".+?" })
        except:
            return

        try:
            next = common.parseDOM(result, "span", attrs = { "class": "pagination" })[0]
            name = common.parseDOM(next, "a")[-1]
            if 'laquo' in name: raise Exception()
            next = common.parseDOM(next, "a", ret="href")[-1]
            next = '%s%s' % (link().imdb_base, next)
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for show in shows:
            try:
                title = common.parseDOM(show, "a")[1]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = common.parseDOM(show, "span", attrs = { "class": "year_type" })[0]
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                url = common.parseDOM(show, "a", ret="href")[0]
                url = '%s%s' % (link().imdb_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                imdb = re.sub('[^0-9]', '', url.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')

                poster = '0'
                try: poster = common.parseDOM(show, "img", ret="src")[0]
                except: pass
                if not ('_SX' in poster or '_SY' in poster): poster = '0'
                poster = re.sub('_SX\d*|_SY\d*|_CR\d+?,\d+?,\d+?,\d*','_SX500', poster)
                poster = common.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                genre = common.parseDOM(show, "span", attrs = { "class": "genre" })
                genre = common.parseDOM(genre, "a")
                genre = " / ".join(genre)
                if genre == '': genre = '0'
                genre = common.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')

                try: rating = common.parseDOM(show, "span", attrs = { "class": "rating-rating" })[0]
                except: rating = '0'
                try: rating = common.parseDOM(show, "span", attrs = { "class": "value" })[0]
                except: rating = '0'
                if rating == '': rating = '0'
                rating = common.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                try: mpaa = common.parseDOM(show, "span", attrs = { "class": "certificate" })[0]
                except: mpaa = '0'
                try: mpaa = common.parseDOM(mpaa, "span", ret="title")[0]
                except: mpaa = '0'
                if mpaa == '' or mpaa == 'NOT_RATED': mpaa = '0'
                mpaa = mpaa.replace('_', '-')
                mpaa = common.replaceHTMLCodes(mpaa)
                mpaa = mpaa.encode('utf-8')

                try: plot = common.parseDOM(show, "span", attrs = { "class": "outline" })[0]
                except: plot = '0'
                plot = plot.rsplit('<span>', 1)[0].strip()
                if plot == '': plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'genre': genre, 'url': url, 'poster': poster, 'banner': poster, 'fanart': '0', 'studio': '0', 'premiered': '0', 'duration': '0', 'rating': rating, 'mpaa': mpaa, 'plot': plot, 'next': next})
            except:
                pass

        threads = []
        for i in range(0, len(self.list)): threads.append(Thread(self.tvdb_info, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        self.list = [i for i in self.list if not i['tvdb'] == '0']

        return self.list

    def imdb_list2(self, url, idx=True):
        try:
            def imdb_watchlist_id(url):
                id = getUrl(url, timeout='30').result
                id = re.compile('/export[?]list_id=(ls\d*)').findall(id)[0]
                return id

            if url == link().imdb_watchlist % link().imdb_user:
                url = index().cache(imdb_watchlist_id, 8640, url)
                url = link().imdb_tv_list % url

            result = getUrl(url, timeout='30').result

            try:
                if idx == True: raise Exception()
                pages = common.parseDOM(result, "div", attrs = { "class": "desc" })[0]
                pages = re.compile('Page \d+? of (\d*)').findall(pages)[0]
                for i in range(1, int(pages)):
                    u = url.replace('&start=1', '&start=%s' % str(i*100+1))
                    try: result += getUrl(u, timeout='30').result
                    except: pass
            except:
                pass

            result = result.replace('\n','')
            result = result.decode('iso-8859-1').encode('utf-8')
            shows = common.parseDOM(result, "div", attrs = { "class": "list_item.+?" })
        except:
            return

        try:
            next = common.parseDOM(result, "div", attrs = { "class": "pagination" })[-1]
            name = common.parseDOM(next, "a")[-1]
            if 'laquo' in name: raise Exception()
            next = common.parseDOM(next, "a", ret="href")[-1]
            next = '%s%s' % (url.split('?', 1)[0], next)
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for show in shows:
            try:
                title = common.parseDOM(show, "a", attrs = { "onclick": ".+?" })[-1]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = common.parseDOM(show, "span", attrs = { "class": "year_type" })[0]
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                url = common.parseDOM(show, "a", ret="href")[0]
                url = '%s%s' % (link().imdb_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                imdb = re.sub('[^0-9]', '', url.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')

                poster = '0'
                try: poster = common.parseDOM(show, "img", ret="src")[0]
                except: pass
                try: poster = common.parseDOM(show, "img", ret="loadlate")[0]
                except: pass
                if not ('_SX' in poster or '_SY' in poster): poster = '0'
                poster = re.sub('_SX\d*|_SY\d*|_CR\d+?,\d+?,\d+?,\d*','_SX500', poster)
                poster = common.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                try: rating = common.parseDOM(show, "span", attrs = { "class": "rating-rating" })[0]
                except: rating = '0'
                try: rating = common.parseDOM(show, "span", attrs = { "class": "value" })[0]
                except: rating = '0'
                if rating == '' or rating == '-': rating = '0'
                rating = common.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                try: plot = common.parseDOM(show, "div", attrs = { "class": "item_description" })[0]
                except: plot = '0'
                plot = plot.rsplit('<span>', 1)[0].strip()
                if plot == '': plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'genre': '0', 'url': url, 'poster': poster, 'banner': poster, 'fanart': '0', 'studio': '0', 'premiered': '0', 'duration': '0', 'rating': rating, 'mpaa': '0', 'plot': plot, 'next': next})
            except:
                pass

        return self.list

    def imdb_list3(self, url):
        try:
            url = link().imdb_search % urllib.quote_plus(url)

            result = getUrl(url, timeout='30').result
            result = common.replaceHTMLCodes(result)
            result = json.loads(result)

            shows = []
            try: shows += result['title_popular']
            except: pass
            try: shows += result['title_exact']
            except: pass
            try: shows += result['title_substring']
            except: pass
        except:
            return

        for show in shows:
            try:
                year = show['title_description']
                year = year.split(',', 1)[0].lower()
                if not any(x in year for x in ['tv series', 'tv mini-series']): raise Exception()
                year = re.sub('[^0-9]', '', str(year))[:4]
                if not year.isdigit(): raise Exception()

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                title = show['title']
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                imdb = show['id']
                imdb = re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                url = link().imdb_title % imdb
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'genre': '0', 'url': url, 'poster': '0', 'banner': '0', 'fanart': '0', 'studio': '0', 'premiered': '0', 'duration': '0', 'rating': '0', 'mpaa': '0', 'plot': '0'})
            except:
                pass

        self.list = self.list[:50]

        threads = []
        for i in range(0, len(self.list)): threads.append(Thread(self.tvdb_info, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        self.list = [i for i in self.list if not i['tvdb'] == '0']

        filter = [i for i in self.list if not i['poster'] == '0']
        filter += [i for i in self.list if i['poster'] == '0']
        self.list = filter

        return self.list

    def trakt_list(self, url):
        try:
            url += '?extended=full,images&limit=200'
            result = getTrakt().result(url)
            result = json.loads(result)

            shows = []
            for i in result:
                try: shows.append(i['show'])
                except: pass
        except:
            return

        for show in shows:
            try:
                title = show['title']
                title = re.sub('\s(|[(])(UK|US|AU|\d{4})(|[)])$', '', title)
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = show['year']
                year = re.sub('[^0-9]', '', str(year))
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                imdb = show['ids']['imdb']
                if imdb == None or imdb == '': imdb = '0000000'
                imdb = re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                tvdb = show['ids']['tvdb']
                if tvdb == None or tvdb == '': tvdb = '0'
                tvdb = re.sub('[^0-9]', '', str(tvdb))
                tvdb = tvdb.encode('utf-8')

                url = link().imdb_title % imdb
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                poster = '0'
                try: poster = show['images']['poster']['medium']
                except: pass
                if poster == None or not '/posters/' in poster: poster = '0'
                poster = poster.rsplit('?', 1)[0]
                poster = common.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                banner = poster
                try: banner = show['images']['banner']['full']
                except: pass
                if banner == None or not '/banners/' in banner: banner = poster
                banner = banner.rsplit('?', 1)[0]
                banner = common.replaceHTMLCodes(banner)
                banner = banner.encode('utf-8')

                fanart = '0'
                try: fanart = show['images']['fanart']['full']
                except: pass
                if fanart == None or not '/fanarts/' in fanart: fanart = '0'
                fanart = fanart.rsplit('?', 1)[0]
                fanart = common.replaceHTMLCodes(fanart)
                fanart = fanart.encode('utf-8')

                genre = show['genres']
                genre = [i.title() for i in genre]
                if genre == []: genre = '0'
                genre = " / ".join(genre)
                genre = common.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')

                studio = show['network']
                if studio == None: studio = '0'
                studio = common.replaceHTMLCodes(studio)
                studio = studio.encode('utf-8')

                premiered = show['first_aired']
                try: premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except: premiered = '0'
                premiered = common.replaceHTMLCodes(premiered)
                premiered = premiered.encode('utf-8')

                try: duration = str(show['runtime'])
                except: duration = '0'
                if duration == None: duration = '0'
                duration = common.replaceHTMLCodes(duration)
                duration = duration.encode('utf-8')

                try: rating = str(show['rating'])
                except: rating = '0'
                if rating == None or rating == '0.0': rating = '0'
                rating = common.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                mpaa = show['certification']
                if mpaa == None: mpaa = '0'
                mpaa = common.replaceHTMLCodes(mpaa)
                mpaa = mpaa.encode('utf-8')

                plot = show['overview']
                if plot == None: plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'title': title, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'genre': genre, 'url': url, 'poster': poster, 'banner': banner, 'fanart': fanart, 'studio': studio, 'premiered': premiered, 'duration': duration, 'rating': rating, 'mpaa': mpaa, 'plot': plot})
            except:
                pass

        return self.list

    def tvdb_info(self, i):
        try:
            try: sid = self.list[i]['tvdb']
            except: sid = '0'

            if sid == '0':
                url = link().tvdb_search % self.list[i]['imdb']
                result = getUrl(url, timeout='10').result

                try: name = common.parseDOM(result, "SeriesName")[0]
                except: name = '0'
                dupe = re.compile('[***]Duplicate (\d*)[***]').findall(name)

                year = self.list[i]['year']
                years = [str(year), str(int(year)+1), str(int(year)-1)]

                if len(dupe) > 0:
                    sid = str(dupe[0])
                elif name == '0':
                    show = self.list[i]['title']
                    title = self.cleantitle_tv(show)
                    url = link().tvdb_search2 % urllib.quote_plus(show)
                    result = getUrl(url, timeout='10').result
                    result = common.replaceHTMLCodes(result)
                    result = common.parseDOM(result, "Series")
                    result = [x for x in result if title == self.cleantitle_tv(common.parseDOM(x, "SeriesName")[0])]
                    result = [x for x in result if any(y in common.parseDOM(x, "FirstAired")[0] for y in years)][0]

                sid = common.parseDOM(result, "seriesid")[0]


            url = link().tvdb_info2 % (link().tvdb_key, sid)
            result = getUrl(url, timeout='10').result

            tvdb = common.parseDOM(result, "id")[0]
            if tvdb == '': tvdb = '0'
            tvdb = common.replaceHTMLCodes(tvdb)
            tvdb = tvdb.encode('utf-8')
            if not tvdb == '0': self.list[i].update({'tvdb': tvdb})

            try: poster = common.parseDOM(result, "poster")[0]
            except: poster = ''
            if not poster == '': poster = link().tvdb_image + poster
            else: poster = '0'
            poster = common.replaceHTMLCodes(poster)
            poster = poster.encode('utf-8')

            try: banner = common.parseDOM(result, "banner")[0]
            except: banner = ''
            if not banner == '': banner = link().tvdb_image + banner
            else: banner = '0'
            banner = common.replaceHTMLCodes(banner)
            banner = banner.encode('utf-8')

            try: fanart = common.parseDOM(result, "fanart")[0]
            except: fanart = ''
            if not fanart == '': fanart = link().tvdb_image + fanart
            else: fanart = '0'
            fanart = common.replaceHTMLCodes(fanart)
            fanart = fanart.encode('utf-8')
            if not fanart == '0': self.list[i].update({'fanart': fanart})

            if not poster == '0': self.list[i].update({'poster': poster})
            elif not fanart == '0': self.list[i].update({'poster': fanart})
            elif not banner == '0': self.list[i].update({'poster': banner})

            if not banner == '0': self.list[i].update({'banner': banner})
            elif not fanart == '0': self.list[i].update({'banner': fanart})
            elif not poster == '0': self.list[i].update({'banner': poster})

            try: genre = common.parseDOM(result, "Genre")[0]
            except: genre = ''
            genre = [x for x in genre.split('|') if not x == '']
            genre = " / ".join(genre)
            if genre == '': genre = '0'
            genre = common.replaceHTMLCodes(genre)
            genre = genre.encode('utf-8')
            if not genre == '0': self.list[i].update({'genre': genre})

            try: studio = common.parseDOM(result, "Network")[0]
            except: studio = ''
            if studio == '': studio = '0'
            studio = common.replaceHTMLCodes(studio)
            studio = studio.encode('utf-8')
            if not studio == '0': self.list[i].update({'studio': studio})

            try: premiered = common.parseDOM(result, "FirstAired")[0]
            except: premiered = ''
            if premiered == '': premiered = '0'
            premiered = common.replaceHTMLCodes(premiered)
            premiered = premiered.encode('utf-8')
            if not premiered == '0': self.list[i].update({'premiered': premiered})

            try: duration = common.parseDOM(result, "Runtime")[0]
            except: duration = ''
            if duration == '': duration = '0'
            duration = common.replaceHTMLCodes(duration)
            duration = duration.encode('utf-8')
            if not duration == '0': self.list[i].update({'duration': duration})

            try: rating = common.parseDOM(result, "Rating")[0]
            except: rating = ''
            if rating == '' or not self.list[i]['rating'] == '0': rating = '0'
            rating = common.replaceHTMLCodes(rating)
            rating = rating.encode('utf-8')
            if not rating == '0': self.list[i].update({'rating': rating})

            try: mpaa = common.parseDOM(result, "ContentRating")[0]
            except: mpaa = ''
            if mpaa == '': mpaa = '0'
            mpaa = common.replaceHTMLCodes(mpaa)
            mpaa = mpaa.encode('utf-8')
            if not mpaa == '0': self.list[i].update({'mpaa': mpaa})

            try: plot = common.parseDOM(result, "Overview")[0]
            except: plot = ''
            if plot == '': plot = '0'
            plot = common.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')
            if not plot == '0': self.list[i].update({'plot': plot})
        except:
            pass

class seasons:
    def __init__(self):
        self.list = []

    def get(self, show, year, imdb, tvdb, idx=True):
        if idx == True:
            self.list = index().cache(self.tvdb_list, 24, show, year, imdb, tvdb, '-1')
            try: self.list = self.list[0]['seasons']
            except: return
            index().seasonList(self.list)
            return self.list
        else:
            self.list = self.tvdb_list(show, year, imdb, tvdb, '-1')
            return self.list

    def cleantitle_tv(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU|\d{4})(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def tvdb_list(self, show, year, imdb, tvdb, limit=''):
        try:
            if not tvdb == '0': raise Exception()

            url = link().tvdb_search % imdb
            result = getUrl(url, timeout='10').result
            result = common.parseDOM(result, "Series")

            if len(result) == 0:
                url = link().tvdb_search2 % urllib.quote_plus(show)
                result = getUrl(url, timeout='10').result
                result = common.replaceHTMLCodes(result)
                result = common.parseDOM(result, "Series")

                title = self.cleantitle_tv(show)
                years = [str(year), str(int(year)+1), str(int(year)-1)]
                result = [i for i in result if title == self.cleantitle_tv(common.parseDOM(i, "SeriesName")[0])]
                result = [i for i in result if any(x in common.parseDOM(i, "FirstAired")[0] for x in years)][0]

            tvdb = common.parseDOM(result, "seriesid")[0]
            tvdb = tvdb.encode('utf-8')
        except:
            pass

        try:
            if not imdb == '0000000': raise Exception()

            match = []
            url = link().imdb_search % urllib.quote_plus(show)
            result = getUrl(url, timeout='30').result
            result = common.replaceHTMLCodes(result)
            result = json.loads(result)
            for i in result.keys(): match += result[i]

            title = self.cleantitle_tv(show)
            years = [str(year), str(int(year)+1), str(int(year)-1)]
            match = [i for i in match if title == self.cleantitle_tv(i['title'])]
            match = [i for i in match if any(i['title_description'].startswith(y) for y in years)][0]

            imdb = match['id']
            imdb = re.sub('[^0-9]', '', str(imdb))
            imdb = imdb.encode('utf-8')
        except:
            pass

        try:
            if tvdb == '0': raise Exception()

            import zipfile, StringIO
            url = link().tvdb_info % (link().tvdb_key, tvdb)
            data = urllib2.urlopen(url, timeout=10).read()
            zip = zipfile.ZipFile(StringIO.StringIO(data))
            art = zip.read('banners.xml')
            result = zip.read('en.xml')
            zip.close()

            dupe = common.parseDOM(result, "SeriesName")[0]
            dupe = re.compile('[***]Duplicate (\d*)[***]').findall(dupe)
            if len(dupe) > 0:
                tvdb = str(dupe[0]).encode('utf-8')
                url = link().tvdb_info % (link().tvdb_key, tvdb)
                data = urllib2.urlopen(url, timeout=10).read()
                zip = zipfile.ZipFile(StringIO.StringIO(data))
                art = zip.read('banners.xml')
                result = zip.read('en.xml')
                zip.close()

            result = result.split('<Episode>')
            episodes = [x for x in result if '<EpisodeNumber>' in x]
            result = result[0]

            art = art.split('<Banner>')
            art = [i for i in art if '<Language>en</Language>' in i and '<BannerType>season</BannerType>' in i]
            art = [i for i in art if not 'seasonswide' in re.compile('<BannerPath>(.+?)</BannerPath>').findall(i)[0]]

            episodes = [i for i in episodes if not '<SeasonNumber>0</SeasonNumber>' in i]
            episodes = [i for i in episodes if not '<EpisodeNumber>0</EpisodeNumber>' in i]
            seasons = [i for i in episodes if '<EpisodeNumber>1</EpisodeNumber>' in i]

            if not limit == '': episodes = [i for i in episodes if '<SeasonNumber>%01d</SeasonNumber>' % int(limit) in i]

            show_alt = common.parseDOM(result, "SeriesName")[0]
            dupe = re.compile('[***]Duplicate (\d*)[***]').findall(show)
            if len(dupe) > 0: show = show_alt
            if show == '': raise Exception() 
            if show_alt == '': show_alt = show
            show_alt = common.replaceHTMLCodes(show_alt)
            show_alt = show_alt.encode('utf-8')

            url = link().imdb_title % imdb
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            try: poster = common.parseDOM(result, "poster")[0]
            except: poster = ''
            if not poster == '': poster = link().tvdb_image + poster
            else: poster = '0'
            poster = common.replaceHTMLCodes(poster)
            poster = poster.encode('utf-8')

            try: banner = common.parseDOM(result, "banner")[0]
            except: banner = ''
            if not banner == '': banner = link().tvdb_image + banner
            else: banner = '0'
            banner = common.replaceHTMLCodes(banner)
            banner = banner.encode('utf-8')

            try: fanart = common.parseDOM(result, "fanart")[0]
            except: fanart = ''
            if not fanart == '': fanart = link().tvdb_image + fanart
            else: fanart = '0'
            fanart = common.replaceHTMLCodes(fanart)
            fanart = fanart.encode('utf-8')

            if not poster == '0': pass
            elif not fanart == '0': poster = fanart
            elif not banner == '0': poster = banner

            if not banner == '0': pass
            elif not fanart == '0': banner = fanart
            elif not poster == '0': banner = poster

            try: genre = common.parseDOM(result, "Genre")[0]
            except: genre = ''
            genre = [i for i in genre.split('|') if not i == '']
            genre = " / ".join(genre)
            if genre == '': genre = '0'
            genre = common.replaceHTMLCodes(genre)
            genre = genre.encode('utf-8')

            try: studio = common.parseDOM(result, "Network")[0]
            except: studio = ''
            if studio == '': studio = '0'
            studio = common.replaceHTMLCodes(studio)
            studio = studio.encode('utf-8')

            try: status = common.parseDOM(result, "Status")[0]
            except: status = ''
            if status == '': status = 'Ended'
            status = common.replaceHTMLCodes(status)
            status = status.encode('utf-8')

            try: duration = common.parseDOM(result, "Runtime")[0]
            except: duration = ''
            if duration == '': duration = '0'
            duration = common.replaceHTMLCodes(duration)
            duration = duration.encode('utf-8')

            try: rating = common.parseDOM(result, "Rating")[0]
            except: rating = ''
            if rating == '': rating = '0'
            rating = common.replaceHTMLCodes(rating)
            rating = rating.encode('utf-8')

            try: mpaa = common.parseDOM(result, "ContentRating")[0]
            except: mpaa = ''
            if mpaa == '': mpaa = '0'
            mpaa = common.replaceHTMLCodes(mpaa)
            mpaa = mpaa.encode('utf-8')

            try: plot = common.parseDOM(result, "Overview")[0]
            except: plot = ''
            if plot == '': plot = '0'
            plot = common.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')

            networks = ['BBC One', 'BBC Two', 'BBC Three', 'BBC Four', 'CBBC', 'CBeebies', 'ITV', 'ITV1', 'ITV2', 'ITV3', 'ITV4', 'Channel 4', 'E4', 'More4', 'Channel 5', 'Sky1']
            if studio in networks: country = 'UK'
            else: country = 'US'
            dt = datetime.datetime.utcnow() - datetime.timedelta(hours = 5)
            if country == 'UK': dt = datetime.datetime.utcnow() - datetime.timedelta(hours = 0)
        except:
            return

        self.list = [{'seasons': []}, {'episodes': []}]

        for season in seasons:
            try:
                date = common.parseDOM(season, "FirstAired")[0]
                if date == '' or '-00' in date: date = '0'
                date = common.replaceHTMLCodes(date)
                date = date.encode('utf-8')

                num = common.parseDOM(season, "SeasonNumber")[0]
                num = '%01d' % int(num)
                num = num.encode('utf-8')

                if status == 'Ended': pass
                elif date == '0': raise Exception()
                elif int(re.sub('[^0-9]', '', str(date))) > int(dt.strftime("%Y%m%d")): raise Exception()

                thumb = [i for i in art if common.parseDOM(i, "Season")[0] == num]

                try: thumb = common.parseDOM(thumb[0], "BannerPath")[0]
                except: thumb = ''
                if not thumb == '': thumb = link().tvdb_image + thumb
                else: thumb = '0'
                thumb = common.replaceHTMLCodes(thumb)
                thumb = thumb.encode('utf-8')

                if thumb == '0': thumb = poster

                self.list[0]['seasons'].append({'title': num, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'season': num, 'show': show, 'show_alt': show_alt, 'genre': genre, 'url': url, 'poster': poster, 'banner': banner, 'thumb': thumb, 'fanart': fanart, 'studio': studio, 'status': status, 'date': date, 'duration': duration, 'rating': rating, 'mpaa': mpaa, 'plot': plot})
            except:
                pass

        for episode in episodes:
            try:
                date = common.parseDOM(episode, "FirstAired")[0]
                if date == '' or '-00' in date: date = '0'
                date = common.replaceHTMLCodes(date)
                date = date.encode('utf-8')

                season = common.parseDOM(episode, "SeasonNumber")[0]
                season = '%01d' % int(season)
                season = season.encode('utf-8')

                if status == 'Ended': pass
                elif date == '0': raise Exception()
                elif int(re.sub('[^0-9]', '', str(date))) > int(dt.strftime("%Y%m%d")): raise Exception()

                num = common.parseDOM(episode, "EpisodeNumber")[0]
                num = re.sub('[^0-9]', '', '%01d' % int(num))
                num = num.encode('utf-8')

                title = common.parseDOM(episode, "EpisodeName")[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                t = 'Episode ' + '%01d' % int(num)
                t = t.encode('utf-8')
                if title == '': title = t

                name = show_alt + ' S' + '%02d' % int(season) + 'E' + '%02d' % int(num)
                try: name = name.encode('utf-8')
                except: pass

                try: thumb = common.parseDOM(episode, "filename")[0]
                except: thumb = ''
                if not thumb == '': thumb = link().tvdb_image + thumb
                else: thumb = '0'
                thumb = common.replaceHTMLCodes(thumb)
                thumb = thumb.encode('utf-8')

                if not thumb == '0': pass
                elif not fanart == '0': thumb = fanart.replace(link().tvdb_image, link().tvdb_image2)
                elif not poster == '0': thumb = poster

                try: rating = common.parseDOM(episode, "Rating")[0]
                except: rating = ''
                if rating == '': rating = '0'
                rating = common.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                try: director = common.parseDOM(episode, "Director")[0]
                except: director = ''
                director = [i for i in director.split('|') if not i == '']
                director = " / ".join(director)
                if director == '': director = '0'
                director = common.replaceHTMLCodes(director)
                director = director.encode('utf-8')

                try: writer = common.parseDOM(episode, "Writer")[0]
                except: writer = ''
                writer = [i for i in writer.split('|') if not i == '']
                writer = " / ".join(writer)
                if writer == '': writer = '0'
                writer = common.replaceHTMLCodes(writer)
                writer = writer.encode('utf-8')

                try: desc = common.parseDOM(episode, "Overview")[0]
                except: desc = ''
                if desc == '': desc = '0'
                desc = common.replaceHTMLCodes(desc)
                desc = desc.encode('utf-8')

                if desc == '0': desc = plot

                self.list[1]['episodes'].append({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'season': season, 'episode': num, 'show': show, 'show_alt': show_alt, 'genre': genre, 'url': url, 'poster': poster, 'banner': banner, 'thumb': thumb, 'fanart': fanart, 'studio': studio, 'status': status, 'date': date, 'duration': duration, 'rating': rating, 'mpaa': mpaa, 'director': director, 'writer': writer, 'plot': desc})
            except:
                pass

        return self.list

class episodes:
    def __init__(self):
        self.list = []

    def get(self, show, year, imdb, tvdb, season='', idx=True):
        if idx == True:
            self.list = index().cache(seasons().tvdb_list, 1, show, year, imdb, tvdb, season)
            try: self.list = self.list[1]['episodes']
            except: return
            index().episodeList(self.list)
            return self.list
        else:
            self.list = seasons().tvdb_list(show, year, imdb, tvdb, season)
            return self.list

    def get2(self, show, year, imdb, tvdb, season, episode):
        try:
            self.list = index().cache(seasons().tvdb_list, 1, show, year, imdb, tvdb)
            self.list = self.list[1]['episodes']

            num = [x for x,y in enumerate(self.list) if y['season'] == str(season) and  y['episode'] == str(episode)][-1]
            self.list = [y for x,y in enumerate(self.list) if x >= num]

            index().episodeList(self.list)
            return self.list
        except:
            pass

    def calendar(self, week):
        daysMap = {1:6, 2:13, 3:20, 4:27}
        now = datetime.datetime.utcnow() - datetime.timedelta(hours = 5)
        date = datetime.date(now.year, now.month, now.day) - datetime.timedelta(days=daysMap[week])
        url = link().trakt_tv_calendar % (str(date), '5')
        self.list = index().cache(self.trakt_list, 1, url)
        try: self.list = sorted(self.list, key=itemgetter('name'))
        except: return
        index().episodeList(self.list)
        return self.list

    def trakt_progress(self):
        self.list = index().cache(self.trakt_list2, 1)
        try: self.list = sorted(self.list, key=itemgetter('date'))[::-1]
        except: return
        index().episodeList(self.list)
        return self.list

    def trakt_added(self):
        now = datetime.datetime.utcnow() - datetime.timedelta(hours = 5)
        date = datetime.date(now.year, now.month, now.day) - datetime.timedelta(days=32)
        url = link().trakt_tv_my_calendar % (str(date), '31')
        self.list = index().cache(self.trakt_list, 1, url)
        try: self.list = sorted(self.list, key=itemgetter('date'))[::-1]
        except: return
        index().episodeList(self.list)
        return self.list

    def added(self):
        self.list = index().cache(self.scn_list, 1)
        try: self.list = sorted(self.list, key=itemgetter('date'))[::-1]
        except: return
        index().episodeList(self.list)
        return self.list

    def cleantitle_tv(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU|\d{4})(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def cleantitle_tv_2(self, title):
        title = re.sub('\n|\.(UK|US|AU|\d{4})$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def tvrage_redirect(self, title, year, imdb, tvdb, season, episode, show, date, genre):
        try:
            redirect = False
            if len(season) > 3: redirect = True
            genre = [i.strip() for i in genre.split('/')]
            genre = [i for i in genre if any(x == i for x in ['Reality', 'Game Show', 'Talk Show'])]
            if not len(genre) == 0: redirect = True
            blocks = ['73141']
            if tvdb in blocks: redirect = True
            if redirect == False: raise Exception()
        except:
            return (season, episode)

        try:
            tvrage = index().cache(self.tvrage_id, 8640, imdb, tvdb, show, year)
            if tvrage == None: raise Exception()
        except:
            return (season, episode)

        try:
            result = index().cache(self.tvrage_ep, 8640, tvrage, title, date, season, episode)
            if result == None: raise Exception()
            return (result[0], result[1])
        except:
            return (season, episode)

    def tvrage_id(self, imdb, tvdb, show, year):
        try:
            if not imdb.startswith('tt'): imdb = 'tt' + imdb
            result = getTrakt().result(link().trakt_tv_summary % imdb)
            result = json.loads(result)
            tvrage = result['ids']['tvrage']
            if tvrage == None: raise Exception()
            return str(tvrage)
        except:
            pass

        try:
            url = link().tvrage_search % urllib.quote_plus(show)
            result = getUrl(url, timeout='10').result
            result = common.parseDOM(result, "show")
            show = self.cleantitle_tv(show)
            years = [str(year), str(int(year)+1), str(int(year)-1)]
            result = [i for i in result if show == self.cleantitle_tv(common.replaceHTMLCodes(common.parseDOM(i, "name")[0])) and any(x in common.parseDOM(i, "started")[0] for x in years)][0]
            tvrage = common.parseDOM(result, "showid")[0]
            return str(tvrage)
        except:
            pass

    def tvrage_ep(self, tvrage, title, date, season, episode):
        monthMap = {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May', '06':'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}
        title = self.cleantitle_tv(title)

        try:
            url = link().tvrage_info % tvrage
            result = getUrl(url, timeout='5').result
            search = re.compile('<td.+?><a.+?title=.+?season.+?episode.+?>(\d+?)x(\d+?)<.+?<td.+?>(\d+?/.+?/\d+?)<.+?<td.+?>.+?href=.+?>(.+?)<').findall(result.replace('\n',''))
            d = '%02d/%s/%s' % (int(date.split('-')[2]), monthMap[date.split('-')[1]], date.split('-')[0])
            match = [i for i in search if d == i[2]]
            if len(match) == 1: return (str('%01d' % int(match[0][0])), str('%01d' % int(match[0][1])))
            match = [i for i in search if title == self.cleantitle_tv(i[3])]
            if len(match) == 1: return (str('%01d' % int(match[0][0])), str('%01d' % int(match[0][1])))
        except:
            pass

        try:
            url = link().epguides_info % tvrage
            result = getUrl(url, timeout='5').result
            search = re.compile('\d+?,(\d+?),(\d+?),.+?,(\d+?/.+?/\d+?),"(.+?)",.+?,".+?"').findall(result)
            d = '%02d/%s/%s' % (int(date.split('-')[2]), monthMap[date.split('-')[1]], date.split('-')[0][-2:])
            match = [i for i in search if d == i[2]]
            if len(match) == 1: return (str('%01d' % int(match[0][0])), str('%01d' % int(match[0][1])))
            match = [i for i in search if title == self.cleantitle_tv(i[3])]
            if len(match) == 1: return (str('%01d' % int(match[0][0])), str('%01d' % int(match[0][1])))
        except:
            pass

    def trakt_list(self, url):
        try:
            url += '?extended=full,images'
            result = getTrakt().result(url)
            result = json.loads(result)

            episodes = result
        except:
            return

        for episode in episodes:
            try:
                title = episode['episode']['title']
                if title == None or title == '': raise Exception()
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = episode['show']['year']
                year = re.sub('[^0-9]', '', str(year))
                year = year.encode('utf-8')

                imdb = episode['show']['ids']['imdb']
                if imdb == None or imdb == '': imdb = '0000000'
                imdb = re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                tvdb = episode['show']['ids']['tvdb']
                if tvdb == None or tvdb == '': tvdb = '0'
                tvdb = re.sub('[^0-9]', '', str(tvdb))
                tvdb = tvdb.encode('utf-8')

                url = link().imdb_title % imdb
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                season = episode['episode']['season']
                season = re.sub('[^0-9]', '', '%01d' % int(season))
                if season == '0': raise Exception()
                season = season.encode('utf-8')

                num = episode['episode']['number']
                num = re.sub('[^0-9]', '', '%01d' % int(num))
                if num == '0': raise Exception()
                num = num.encode('utf-8')

                show_alt = episode['show']['title']
                if show_alt == '': raise Exception()
                show_alt = common.replaceHTMLCodes(show_alt)
                show_alt = show_alt.encode('utf-8')

                show = re.sub('\s(|[(])(UK|US|AU|\d{4})(|[)])$', '', show_alt)
                show = common.replaceHTMLCodes(show)
                show = show.encode('utf-8')

                name = show_alt + ' S' + '%02d' % int(season) + 'E' + '%02d' % int(num)
                try: name = name.encode('utf-8')
                except: pass

                poster = '0'
                try: poster = episode['show']['images']['poster']['medium']
                except: pass
                if poster == None or not '/posters/' in poster: poster = '0'
                poster = poster.rsplit('?', 1)[0]
                poster = common.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                banner = poster
                try: banner = episode['show']['images']['banner']['full']
                except: pass
                if banner == None or not '/banners/' in banner: banner = poster
                banner = banner.rsplit('?', 1)[0]
                banner = common.replaceHTMLCodes(banner)
                banner = banner.encode('utf-8')

                fanart = '0'
                try: fanart = episode['show']['images']['fanart']['full']
                except: pass
                if fanart == None or not '/fanarts/' in fanart: fanart = '0'
                fanart = fanart.rsplit('?', 1)[0]
                fanart = common.replaceHTMLCodes(fanart)
                fanart = fanart.encode('utf-8')

                thumb1 = episode['episode']['images']['screenshot']['thumb']
                thumb2 = episode['show']['images']['thumb']['full']
                if '/screenshots/' in thumb1: thumb = thumb1
                elif '/thumbs/' in thumb2: thumb = thumb2
                else: thumb = fanart
                thumb = thumb.rsplit('?', 1)[0]
                thumb = common.replaceHTMLCodes(thumb)
                try: thumb = thumb.encode('utf-8')
                except: pass

                genre = episode['show']['genres']
                genre = [i.title() for i in genre]
                if genre == []: genre = '0'
                genre = " / ".join(genre)
                genre = common.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')

                studio = episode['show']['network']
                if studio == None: studio = '0'
                studio = common.replaceHTMLCodes(studio)
                studio = studio.encode('utf-8')

                date = episode['episode']['first_aired']
                try: date = re.compile('(\d{4}-\d{2}-\d{2})').findall(date)[0]
                except: date = '0'
                date = common.replaceHTMLCodes(date)
                date = date.encode('utf-8')

                try: duration = str(episode['show']['runtime'])
                except: duration = '0'
                if duration == None: duration = '0'
                duration = common.replaceHTMLCodes(duration)
                duration = duration.encode('utf-8')

                try: rating = str(episode['episode']['rating'])
                except: rating = '0'
                if rating == None or rating == '0.0': rating = '0'
                rating = common.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                mpaa = episode['show']['certification']
                if mpaa == None: mpaa = '0'
                mpaa = common.replaceHTMLCodes(mpaa)
                mpaa = mpaa.encode('utf-8')

                desc = episode['episode']['overview']
                if desc == None or desc == '': desc = episode['show']['overview']
                if desc == None or desc == '': desc = '0'
                desc = common.replaceHTMLCodes(desc)
                desc = desc.encode('utf-8')

                self.list.append({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'season': season, 'episode': num, 'show': show, 'show_alt': show_alt, 'genre': genre, 'url': url, 'poster': poster, 'banner': banner, 'thumb': thumb, 'fanart': fanart, 'studio': studio, 'status': 'Continuing', 'date': date, 'duration': duration, 'rating': rating, 'mpaa': mpaa, 'director': '0', 'writer': '0', 'plot': desc})
            except:
                pass

        return self.list

    def trakt_list2(self):
        try:
            url = link().trakt_tv_watched % link().trakt_user
            url += '?extended=full'
            result = getTrakt().result(url)
            shows = json.loads(result)
            showList = []
        except:
            return

        for show in shows:
            try:
                num_1 = 0
                for i in range(0, len(show['seasons'])): num_1 += len(show['seasons'][i]['episodes'])
                num_2 = int(show['show']['aired_episodes'])
                if num_1 >= num_2: raise Exception()

                season = str(show['seasons'][-1]['number'])
                season = season.encode('utf-8')

                episode = str(show['seasons'][-1]['episodes'][-1]['number'])
                episode = episode.encode('utf-8')

                title = show['show']['title']
                title = re.sub('\s(|[(])(UK|US|AU|\d{4})(|[)])$', '', title)
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = show['show']['year']
                year = re.sub('[^0-9]', '', str(year))
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                imdb = show['show']['ids']['imdb']
                if imdb == None or imdb == '': imdb = '0000000'
                imdb = re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                tvdb = show['show']['ids']['tvdb']
                if tvdb == None or tvdb == '': tvdb = '0'
                tvdb = re.sub('[^0-9]', '', str(tvdb))
                tvdb = tvdb.encode('utf-8')

                showList.append({'title': title, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'season': season, 'episode': episode})
            except:
                pass

        def trakt_list2_thread(i):
            try:
                import zipfile, StringIO
                url = link().tvdb_info % (link().tvdb_key, i['tvdb'])
                data = urllib2.urlopen(url, timeout=10).read()
                zip = zipfile.ZipFile(StringIO.StringIO(data))
                result = zip.read('en.xml')
                zip.close()

                result = result.split('<Episode>')
                episode = [x for x in result if '<EpisodeNumber>' in x]
                result = result[0]

                num = [x for x,y in enumerate(episode) if re.compile('<SeasonNumber>(.+?)</SeasonNumber>').findall(y)[0] == str(i['season']) and re.compile('<EpisodeNumber>(.+?)</EpisodeNumber>').findall(y)[0] == str(i['episode'])][-1]
                episode = [y for x,y in enumerate(episode) if x > num][0]

                date = common.parseDOM(episode, "FirstAired")[0]
                if date == '' or '-00' in date: date = '0'
                date = common.replaceHTMLCodes(date)
                date = date.encode('utf-8')

                try: status = common.parseDOM(result, "Status")[0]
                except: status = ''
                if status == '': status = 'Ended'
                status = common.replaceHTMLCodes(status)
                status = status.encode('utf-8')

                dt = datetime.datetime.utcnow() - datetime.timedelta(hours = 5)

                if status == 'Ended': pass
                elif date == '0': raise Exception()
                elif int(re.sub('[^0-9]', '', str(date))) > int(dt.strftime("%Y%m%d")): raise Exception()

                show_alt = common.parseDOM(result, "SeriesName")[0]
                show_alt = common.replaceHTMLCodes(show_alt)
                show_alt = show_alt.encode('utf-8')

                url = link().imdb_title % i['imdb']
                url = url.encode('utf-8')

                try: poster = common.parseDOM(result, "poster")[0]
                except: poster = ''
                if not poster == '': poster = link().tvdb_image + poster
                else: poster = '0'
                poster = common.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                try: banner = common.parseDOM(result, "banner")[0]
                except: banner = ''
                if not banner == '': banner = link().tvdb_image + banner
                else: banner = '0'
                banner = common.replaceHTMLCodes(banner)
                banner = banner.encode('utf-8')

                try: fanart = common.parseDOM(result, "fanart")[0]
                except: fanart = ''
                if not fanart == '': fanart = link().tvdb_image + fanart
                else: fanart = '0'
                fanart = common.replaceHTMLCodes(fanart)
                fanart = fanart.encode('utf-8')

                if not poster == '0': pass
                elif not fanart == '0': poster = fanart
                elif not banner == '0': poster = banner

                if not banner == '0': pass
                elif not fanart == '0': banner = fanart
                elif not poster == '0': banner = poster

                try: genre = common.parseDOM(result, "Genre")[0]
                except: genre = ''
                genre = [x for x in genre.split('|') if not x == '']
                genre = " / ".join(genre)
                if genre == '': genre = '0'
                genre = common.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')

                try: studio = common.parseDOM(result, "Network")[0]
                except: studio = ''
                if studio == '': studio = '0'
                studio = common.replaceHTMLCodes(studio)
                studio = studio.encode('utf-8')

                try: duration = common.parseDOM(result, "Runtime")[0]
                except: duration = ''
                if duration == '': duration = '0'
                duration = common.replaceHTMLCodes(duration)
                duration = duration.encode('utf-8')

                try: mpaa = common.parseDOM(result, "ContentRating")[0]
                except: mpaa = ''
                if mpaa == '': mpaa = '0'
                mpaa = common.replaceHTMLCodes(mpaa)
                mpaa = mpaa.encode('utf-8')

                try: plot = common.parseDOM(result, "Overview")[0]
                except: plot = ''
                try: desc = common.parseDOM(episode, "Overview")[0]
                except: desc = ''
                if not desc == '': plot = desc
                if plot == '': plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                season = common.parseDOM(episode, "SeasonNumber")[0]
                season = '%01d' % int(season)
                season = season.encode('utf-8')

                num = common.parseDOM(episode, "EpisodeNumber")[0]
                num = re.sub('[^0-9]', '', '%01d' % int(num))
                num = num.encode('utf-8')

                title = common.parseDOM(episode, "EpisodeName")[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                t = 'Episode ' + '%01d' % int(num)
                t = t.encode('utf-8')
                if title == '': title = t

                name = show_alt + ' S' + '%02d' % int(season) + 'E' + '%02d' % int(num)
                try: name = name.encode('utf-8')
                except: pass

                try: thumb = common.parseDOM(episode, "filename")[0]
                except: thumb = ''
                if not thumb == '': thumb = link().tvdb_image + thumb
                else: thumb = '0'
                thumb = common.replaceHTMLCodes(thumb)
                thumb = thumb.encode('utf-8')

                if not thumb == '0': pass
                elif not fanart == '0': thumb = fanart.replace(link().tvdb_image, link().tvdb_image2)
                elif not poster == '0': thumb = poster

                try: rating = common.parseDOM(episode, "Rating")[0]
                except: rating = ''
                if rating == '': rating = '0'
                rating = common.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                try: director = common.parseDOM(episode, "Director")[0]
                except: director = ''
                director = [x for x in director.split('|') if not x == '']
                director = " / ".join(director)
                if director == '': director = '0'
                director = common.replaceHTMLCodes(director)
                director = director.encode('utf-8')

                try: writer = common.parseDOM(episode, "Writer")[0]
                except: writer = ''
                writer = [x for x in writer.split('|') if not x == '']
                writer = " / ".join(writer)
                if writer == '': writer = '0'
                writer = common.replaceHTMLCodes(writer)
                writer = writer.encode('utf-8')

                self.list.append({'name': name, 'title': title, 'year': i['year'], 'imdb': i['imdb'], 'tvdb': i['tvdb'], 'season': season, 'episode': num, 'show': i['title'], 'show_alt': show_alt, 'genre': genre, 'url': url, 'poster': poster, 'banner': banner, 'thumb': thumb, 'fanart': fanart, 'studio': studio, 'status': status, 'date': date, 'duration': duration, 'rating': rating, 'mpaa': mpaa, 'director': director, 'writer': writer, 'plot': plot})
            except:
                pass

        showList = showList[:30]

        threads = []
        for i in showList: threads.append(Thread(trakt_list2_thread, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        return self.list

    def scn_list(self):
        try:
            result = getUrl(link().scn_tv_added, timeout='10').result

            url = common.parseDOM(result, "a", ret="href", attrs = { "id": "nav" })
            url = [i for i in url if 'page=2' in i]
            url += re.compile('href="(.+?)".+?>PREV<').findall(result)
            if len(url) > 0:
                url = link().scn_tv_base + '/' + url[0]
                url = common.replaceHTMLCodes(url)
                result += getUrl(url, timeout='10').result

            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "tr", attrs = { "class": "MainTable" })

            dates = [re.compile('(\d{4}-\d{2}-\d{2})').findall(i) for i in result]
            dates = [i[0] for i in dates if not len(i) == 0]
            dates = uniqueList(dates).list

            shows = [common.parseDOM(i, "a")[0] for i in result]
            shows = [re.compile('(.*)[.](S\d+?E\d+?)[.]').findall(i) for i in shows]
            shows = [i[0] for i in shows if not len(i) == 0]
            shows = [self.cleantitle_tv_2(i[0]) + ' ' + i[1] for i in shows]
            shows = [i.encode('utf-8') for i in shows]
            shows = uniqueList(shows).list

            url = link().trakt_tv_calendar % (str(dates[-1]), len(dates))

            self.list = self.trakt_list(url)
            self.list = [i for i in self.list if self.cleantitle_tv(i['show']) + ' S' + '%02d' % int(i['season']) + 'E' + '%02d' % int(i['episode']) in shows]

            return self.list
        except:
            return

class trailer:
    def __init__(self):
        self.youtube_base = 'http://www.youtube.com'
        self.key_link = 'QUl6YVN5RDd2aFpDLTYta2habTVuYlVyLTZ0Q0JRQnZWcnFkeHNz'
        self.key_link = '&key=%s' % base64.urlsafe_b64decode(self.key_link)
        self.search_link = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=5&q=%s'
        self.youtube_search = 'https://www.googleapis.com/youtube/v3/search?q='
        self.youtube_watch = 'http://www.youtube.com/watch?v=%s'

    def play(self, name, url):
        url = self.worker(name, url)
        if url == None: return
        item = xbmcgui.ListItem(path=url)
        item.setProperty("IsPlayable", "true")
        xbmc.Player().play(url, item)

    def worker(self, name, url):
        try:
            if url.startswith(self.youtube_base):
                url = self.resolve(url)
                if url == None: raise Exception()
                return url
            elif not url.startswith('http://'):
                url = self.youtube_watch % url
                url = self.resolve(url)
                if url == None: raise Exception()
                return url
            else:
                raise Exception()
        except:
            query = name + ' trailer'
            query = self.youtube_search + query
            url = self.resolve_search(query)
            if url == None: return
            return url

    def resolve_search(self, url):
        try:
            query = urlparse.parse_qs(urlparse.urlparse(url).query)['q'][0]

            url = self.search_link % urllib.quote_plus(query) + self.key_link

            result = getUrl(url).result

            items = json.loads(result)['items']
            items = [(i['id']['videoId']) for i in items]

            for url in items:
                url = self.resolve(url)
                if not url is None: return url
        except:
            return

    def resolve(self, url):
        try:
            id = url.split("?v=")[-1].split("/")[-1].split("?")[0].split("&")[0]
            result = getUrl('http://www.youtube.com/watch?v=%s' % id).result

            message = common.parseDOM(result, "div", attrs = { "id": "unavailable-submessage" })
            message = ''.join(message)

            alert = common.parseDOM(result, "div", attrs = { "id": "watch7-notification-area" })

            if len(alert) > 0: raise Exception()
            if re.search('[a-zA-Z]', message): raise Exception()

            url = 'plugin://plugin.video.youtube/play/?video_id=%s' % id
            return url
        except:
            return



class resolver:
    def __init__(self):
        self.sources_dict()
        self.sources = []

    def get_host(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, url, meta):
        try:
            if show == None: content = 'movie'
            else: content = 'episode'

            self.sources = self.sources_get(name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre)
            if self.sources == []: raise Exception()
            self.sources = self.sources_filter()

            meta = json.loads(meta)

            if content == 'movie': 
                index().moviesourceList(self.sources, name, imdb, '0', meta)
            else:
                index().tvsourceList(self.sources, name, imdb, tvdb, meta)
        except:
            index().infoDialog(language(30308).encode("utf-8"))
            return

    def play_host(self, content, name, imdb, tvdb, url, source, provider):
        try:
            url = self.sources_resolve(url, provider)
            if url == None: raise Exception()

            if getSetting("playback_info") == 'true':
                index().infoDialog(source, header=name)

            player().run(content, name, url, imdb, tvdb)
            return url
        except:
            index().infoDialog(language(30308).encode("utf-8"))
            return

    def run(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, url):
        try:
            if show == None: content = 'movie'
            else: content = 'episode'

            self.sources = self.sources_get(name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre)
            if self.sources == []: raise Exception()
            self.sources = self.sources_filter()

            autoplay = getSetting("autoplay")
            autoplay_library = getSetting("autoplay_library")
            folderPath = xbmc.getInfoLabel('Container.FolderPath')

            if PseudoTV == 'True':
                url = self.sources_direct()
            elif url == 'dialog://':
                url = self.sources_dialog()
            elif url == 'direct://':
                url = self.sources_direct()
            elif not folderPath.startswith(sys.argv[0]) and autoplay_library == 'false':
                url = self.sources_dialog_2()
            elif folderPath.startswith(sys.argv[0]) and autoplay == 'false':
                url = self.sources_dialog()
            else:
                url = self.sources_direct()

            if url == None: raise Exception()
            if url == 'close://': return

            if getSetting("playback_info") == 'true':
                index().infoDialog(self.selectedSource, header=name)

            player().run(content, name, url, imdb, tvdb)
            return url
        except:
            if PseudoTV == 'True': return
            index().infoDialog(language(30308).encode("utf-8"))
            return

    def normaltitle(self, title):
        try:
            try: return title.decode('ascii').encode("utf-8")
            except: pass

            import unicodedata
            t = ''
            for i in title:
                c = unicodedata.normalize('NFKD',unicode(i,"ISO-8859-1"))
                c = c.encode("ascii","ignore").strip()
                if i == ' ': c = i
                t += c

            return t.encode("utf-8")
        except:
            return title

    def sources_get(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre):
        import inspect
        sourceDict = inspect.getmembers(commonsources, inspect.isclass)
        sourceDict = [i for i in sourceDict if hasattr(i[1], 'get_sources')]

        if show == None: content = 'movie'
        else: content = 'episode'

        if content == 'movie':
            sourceDict = [str(i[0]) for i in sourceDict if hasattr(i[1], 'get_movie')]
            try: sourceDict = [(i, getSetting(i)) for i in sourceDict]
            except: sourceDict = [(i, 'true') for i in sourceDict]
        else:
            sourceDict = [str(i[0]) for i in sourceDict if hasattr(i[1], 'get_show')]
            try: sourceDict = [(i, getSetting(i + '_tv')) for i in sourceDict]
            except: sourceDict = [(i, 'true') for i in sourceDict]

        global global_sources
        global_sources = []

        threads = []
        sourceDict = [i[0] for i in sourceDict if i[1] == 'true']


        if content == 'movie':
            title = self.normaltitle(title)
            for source in sourceDict: threads.append(Thread(self.sources_movie, name, title, year, imdb, source))
        else:
            show, show_alt = self.normaltitle(show), self.normaltitle(show_alt)
            season, episode = episodes().tvrage_redirect(title, year, imdb, tvdb, season, episode, show, date, genre)
            for source in sourceDict: threads.append(Thread(self.sources_tv, name, title, year, imdb, tvdb, date, season, episode, show, show_alt, source))


        timeout = int(getSetting("sources_timeout_beta"))

        [i.start() for i in threads]

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

    def sources_movie(self, name, title, year, imdb, source):
        try:
            dbcon = database.connect(addonSources)
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
            commonsource = getattr(commonsources, source)()
            if url == None: url = commonsource.get_movie(imdb, title, year)
            if url == None: raise Exception()
            dbcur.execute("DELETE FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, 'tt' + imdb, '', ''))
            dbcur.execute("INSERT INTO rel_url Values (?, ?, ?, ?, ?)", (source, 'tt' + imdb, '', '', url))
            dbcon.commit()
        except:
            pass

        try:
            sources = []
            sources = commonsource.get_sources(url, self.hosthdfullDict, self.hostsdfullDict, self.hostlocDict)
            if sources == None: sources = []
            global_sources.extend(sources)
            dbcur.execute("DELETE FROM rel_src WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, 'tt' + imdb, '', ''))
            dbcur.execute("INSERT INTO rel_src Values (?, ?, ?, ?, ?, ?)", (source, 'tt' + imdb, '', '', json.dumps(sources), datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
            dbcon.commit()
        except:
            pass

    def sources_tv(self, name, title, year, imdb, tvdb, date, season, episode, show, show_alt, source):
        try:
            dbcon = database.connect(addonSources)
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
            commonsource = getattr(commonsources, source)()
            if url == None: url = commonsource.get_show(imdb, tvdb, show, show_alt, year)
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
            if ep_url == None: ep_url = commonsource.get_episode(url, imdb, tvdb, title, date, season, episode)
            if ep_url == None: raise Exception()
            dbcur.execute("DELETE FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, 'tt' + imdb, season, episode))
            dbcur.execute("INSERT INTO rel_url Values (?, ?, ?, ?, ?)", (source, 'tt' + imdb, season, episode, ep_url))
            dbcon.commit()
        except:
            pass

        try:
            sources = []
            sources = commonsource.get_sources(ep_url, self.hosthdfullDict, self.hostsdfullDict, self.hostlocDict)
            if sources == None: sources = []
            global_sources.extend(sources)
            dbcur.execute("DELETE FROM rel_src WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, 'tt' + imdb, season, episode))
            dbcur.execute("INSERT INTO rel_src Values (?, ?, ?, ?, ?, ?)", (source, 'tt' + imdb, season, episode, json.dumps(sources), datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
            dbcon.commit()
        except:
            pass

    def sources_resolve(self, url, provider):
        try:
            provider = provider.lower()
            commonsource = getattr(commonsources, provider)()
            url = commonsource.resolve(url)
            return url
        except:
            return

    def sources_filter(self):
        self.sources_reset()

        try: customhdDict = [getSetting("hosthd1"), getSetting("hosthd2"), getSetting("hosthd3"), getSetting("hosthd4"), getSetting("hosthd5"), getSetting("hosthd6"), getSetting("hosthd7"), getSetting("hosthd8"), getSetting("hosthd9"), getSetting("hosthd10"), getSetting("hosthd11"), getSetting("hosthd12"), getSetting("hosthd13"), getSetting("hosthd14"), getSetting("hosthd15"), getSetting("hosthd16"), getSetting("hosthd17"), getSetting("hosthd18"), getSetting("hosthd19"), getSetting("hosthd20")]
        except: customhdDict = []
        try: customsdDict = [getSetting("host1"), getSetting("host2"), getSetting("host3"), getSetting("host4"), getSetting("host5"), getSetting("host6"), getSetting("host7"), getSetting("host8"), getSetting("host9"), getSetting("host10"), getSetting("host11"), getSetting("host12"), getSetting("host13"), getSetting("host14"), getSetting("host15"), getSetting("host16"), getSetting("host17"), getSetting("host18"), getSetting("host19"), getSetting("host20")]
        except: customsdDict = []

        hd_rank = []
        hd_rank += [i for i in self.pzDict if i in self.hostprDict + self.hosthdDict]
        hd_rank += [i for i in self.rdDict if i in self.hostprDict + self.hosthdDict]
        hd_rank += customhdDict
        hd_rank += [i['source'] for i in self.sources if i['quality'] in ['1080p', 'HD'] and not i['source'] in customhdDict + self.hostprDict + self.hosthdDict]
        hd_rank += self.hosthdDict
        hd_rank = [i.lower() for i in hd_rank]
        hd_rank = uniqueList(hd_rank).list

        sd_rank = []
        sd_rank += [i for i in self.pzDict if i in self.hostprDict + self.hosthqDict]
        sd_rank += [i for i in self.rdDict if i in self.hostprDict + self.hosthqDict]
        sd_rank += customsdDict
        sd_rank += [i['source'] for i in self.sources if i['quality'] == 'SD' and not i['source'] in customsdDict + self.hostprDict + self.hosthqDict + self.hostmqDict + self.hostlqDict]
        sd_rank += self.hosthqDict + self.hostmqDict + self.hostlqDict
        sd_rank = [i.lower() for i in sd_rank]
        sd_rank = uniqueList(sd_rank).list

        for i in range(len(self.sources)): self.sources[i]['source'] = self.sources[i]['source'].lower()
        self.sources = sorted(self.sources, key=itemgetter('source'))

        filter = []
        for host in hd_rank: filter += [i for i in self.sources if i['quality'] == '1080p' and i['source'] == host]
        for host in hd_rank: filter += [i for i in self.sources if i['quality'] == 'HD' and i['source'] == host]
        for host in sd_rank: filter += [i for i in self.sources if i['quality'] == 'SD' and i['source'] == host]
        if len(filter) < 10: filter += [i for i in self.sources if i['quality'] == 'SCR']
        if len(filter) < 10: filter += [i for i in self.sources if i['quality'] == 'CAM']
        self.sources = filter

        try: playback_quality = getSetting("playback_quality")
        except: playback_quality = '0'

        if playback_quality == '1':
            self.sources = [i for i in self.sources if not i['quality'] == '1080p']
        elif playback_quality == '2':
            self.sources = [i for i in self.sources if not i['quality'] in ['1080p', 'HD']]
        elif playback_quality == '3':
            self.sources = [i for i in self.sources if not i['quality'] in ['1080p', 'HD'] and i['source'] in self.hostmqDict + self.hostlqDict]
        elif playback_quality == '4':
            self.sources = [i for i in self.sources if not i['quality'] in ['1080p', 'HD'] and i['source'] in self.hostlqDict]

        try: playback_captcha = getSetting("playback_captcha")
        except: playback_captcha = 'false'

        try: playback_1080p_hosts = getSetting("playback_1080p_hosts")
        except: playback_1080p_hosts = 'true'

        try: playback_720p_hosts = getSetting("playback_720p_hosts")
        except: playback_720p_hosts = 'true'

        if playback_captcha == 'false':
            self.sources = [i for i in self.sources if not i['source'] in self.hostcapDict]

        if playback_1080p_hosts == 'false':
            self.sources = [i for i in self.sources if not (i['quality'] == '1080p' and i['source'] in self.hosthdDict and not i['source'] in self.pzDict + self.rdDict)]

        if playback_720p_hosts == 'false':
            self.sources = [i for i in self.sources if not (i['quality'] == 'HD' and i['source'] in self.hosthdDict and not i['source'] in self.pzDict + self.rdDict)]

        count = 1
        for i in range(len(self.sources)):
            s = self.sources[i]['source'].lower()

            q = self.sources[i]['quality']
            if q == 'SD' and s in self.hostmqDict: q = 'MQ'
            elif q == 'SD' and s in self.hostlqDict: q = 'LQ'
            elif q == 'SD': q = 'HQ'

            try: d = self.sources[i]['info']
            except: d = ''
            if not d == '': d = ' | [I]%s [/I]' % d

            if s in self.pzDict: label = '%02d | [B]premiumize[/B] | ' % count
            elif s in self.rdDict: label = '%02d | [B]realdebrid[/B] | ' % count
            else: label = '%02d | [B]%s[/B] | ' % (count, self.sources[i]['provider'])

            if q in ['1080p', 'HD']: label += '%s%s | [B][I]%s [/I][/B]' % (s, d, q)
            else: label += '%s%s | [I]%s [/I]' % (s, d, q)

            self.sources[i]['host'] = self.sources[i]['source']
            self.sources[i]['source'] = label.upper()
            count = count + 1

        return self.sources

    def sources_dialog(self):
        try:
            sourceList, urlList, providerList = [], [], []

            for i in self.sources:
                sourceList.append(i['source'])
                urlList.append(i['url'])
                providerList.append(i['provider'])

            select = index().selectDialog(sourceList)
            if select == -1: return 'close://'

            url = self.sources_resolve(urlList[select], providerList[select])
            self.selectedSource = self.sources[select]['source']
            return url
        except:
            return

    def sources_dialog_2(self):
        try:
            l = '[I]***[/I]  [B]%s[/B]' % language(30408).encode("utf-8").upper()
            sourceList, urlList, providerList = [l], [''], ['']

            for i in self.sources:
                sourceList.append(i['source'])
                urlList.append(i['url'])
                providerList.append(i['provider'])

            select = index().selectDialog(sourceList)
            if select == 0: return self.sources_direct()
            if select == -1: return 'close://'

            url = self.sources_resolve(urlList[select], providerList[select])
            self.selectedSource = self.sources[select-1]['source']
            return url
        except:
            return

    def sources_direct(self):
        self.sources = [i for i in self.sources if not i['host'] in self.hostcapDict]

        self.sources = [i for i in self.sources if not (i['quality'] in ['1080p', 'HD'] and i['host'] in self.hosthdDict and not i['host'] in self.pzDict + self.rdDict)]

        self.sources = [i for i in self.sources if not i['host'] in ['furk']]

        try: playback_auto_sd = getSetting("playback_auto_sd")
        except: playback_auto_sd = 'true'

        if playback_auto_sd == 'true':
            self.sources = [i for i in self.sources if not i['quality'] in ['1080p', 'HD']]

        u = None

        try: import ssl
        except: pass

        for i in self.sources:
            try:
                url = self.sources_resolve(i['url'], i['provider'])
                xbmc.sleep(100)
                if url == None: raise Exception()
                if u == None: u = url

                try: headers = dict(urlparse.parse_qsl(url.rsplit('|', 1)[1]))
                except: headers = dict('')

                try:
                    if sys.version_info < (2, 7, 9): raise Exception()
                    ssl_context = ssl.create_default_context()
                    ssl_context.check_hostname = False
                    ssl_context.verify_mode = ssl.CERT_NONE
                    handlers = [urllib2.HTTPSHandler(context=ssl_context)]
                    opener = urllib2.build_opener(*handlers)
                    opener = urllib2.install_opener(opener)
                except:
                    pass

                request = urllib2.Request(url.split('|')[0], headers=headers)
                response = urllib2.urlopen(request, timeout=10)
                content = int(response.headers['Content-Length'])
                chunk = response.read(16 * 1024)
                response.close()

                self.selectedSource = i['source']
                return url
            except:
                pass

        return u

    def sources_reset(self):
        try:
            v = '4.4.0'
            if getSetting("sources_version") == v: return

            settings = os.path.join(dataPath,'settings.xml')
            file = xbmcvfs.File(settings)
            read = file.read()
            file.close()
            read = read.splitlines()
            write = unicode( '<settings>' + '\n', 'UTF-8' )
            for line in read:
                if len(re.findall('<settings>', line)) > 0: continue
                elif len(re.findall('</settings>', line)) > 0: continue
                elif len(re.findall('id="(host|hosthd)\d*"', line)) > 0: continue
                elif len(re.findall('id="sources_version"', line)) > 0: continue
                write += unicode( line.rstrip() + '\n', 'UTF-8' )
            write += unicode( '<setting id="sources_version" value="%s" />' % v + '\n', 'UTF-8' )
            write += unicode( '</settings>' + '\n', 'UTF-8' )

            file = xbmcvfs.File(settings, 'w')
            file.write(str(write))
            file.close()
        except:
            return

    def sources_dict(self):
        import commonresolvers, inspect

        hosts = inspect.getmembers(commonresolvers, inspect.isclass)
        hosts = [i[1]().info() for i in hosts if hasattr(i[1], 'info')]
        hosts = [i for i in hosts if 'host' in i]

        self.pzDict = index().cache(commonresolvers.premiumize().hosts, 24)
        if commonresolvers.premiumize().status() == False: self.pzDict = []
        if self.pzDict == None: self.pzDict = []

        self.rdDict = index().cache(commonresolvers.realdebrid().hosts, 24)
        if commonresolvers.realdebrid().status() == False: self.rdDict = []
        if self.rdDict == None: self.rdDict = []

        self.hostlocDict = [i['netloc'] for i in hosts if i['quality'] == 'High' and i['captcha'] == False]
        try: self.hostlocDict = [i.lower() for i in reduce(lambda x, y: x+y, self.hostlocDict)]
        except: pass
        self.hostlocDict = uniqueList(self.hostlocDict).list

        self.hostprDict = [i['host'] for i in hosts if i['a/c'] == True]
        try: self.hostprDict = [i.lower() for i in reduce(lambda x, y: x+y, self.hostprDict)]
        except: pass
        self.hostprDict = uniqueList(self.hostprDict).list

        self.hostcapDict = [i['host'] for i in hosts if i['captcha'] == True]
        try: self.hostcapDict = [i.lower() for i in reduce(lambda x, y: x+y, self.hostcapDict)]
        except: pass
        self.hostcapDict = [i for i in self.hostcapDict if not i in self.pzDict + self.rdDict]

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


main()
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

import urllib,urllib2,urlparse,re,os,sys,threading,datetime,time,base64,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
from operator import itemgetter
import json

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database
try:
    import CommonFunctions as common
except:
    import commonfunctionsdummy as common


try: action = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))['action']
except: action = None

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
            headers['User-Agent'] = 'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0;  rv:11.0) like Gecko'
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

            t1 = int(match[3])
            t2 = int(time.time())
            update = (abs(t2 - t1) / 3600) >= int(timeout)
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
            t = int(time.time())
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

                if root == 'library_movies':
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
                    cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=openSettings)' % (sys.argv[0])))
                    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=openPlaylist)' % (sys.argv[0])))
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
            from modules.indexers import trakt
            indicators = trakt.syncMovies(timeout=720)
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
                    u = '%s?action=addPlayableItem&name=%s&title=%s&year=%s&imdb=%s&url=%s&meta=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, sysurl, sysmeta)
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
                cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=addView&content=movies)' % (sys.argv[0])))

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
        from modules.libraries.views import setView
        setView('movies', {'skin.confluence' : 500})

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
            from modules.indexers import trakt
            indicators = trakt.syncTVShows(timeout=720)
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
                    cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=queueItem)' % (sys.argv[0])))
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
                cm.append((language(30416).encode("utf-8"), 'RunPlugin(%s?action=addView&content=tvshows)' % (sys.argv[0])))

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
        from modules.libraries.views import setView
        setView('tvshows', {'skin.confluence' : 500})

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
                    cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=queueItem)' % (sys.argv[0])))
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
                cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=addView&content=seasons)' % (sys.argv[0])))

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
        from modules.libraries.views import setView
        setView('seasons', {'skin.confluence' : 500})

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
            from modules.indexers import trakt
            indicators = trakt.syncTVShows(timeout=720)
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
                    u = '%s?action=addPlayableItem&name=%s&title=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s&show=%s&show_alt=%s&date=%s&genre=%s&url=%s&meta=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, systvdb, sysseason, sysepisode, sysshow, sysshow_alt, sysdate, sysgenre, sysurl, sysmeta)
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
                    cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=queueItem)' % (sys.argv[0])))
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
                cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=addView&content=episodes)' % (sys.argv[0])))

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
        from modules.libraries.views import setView
        setView('episodes', {'skin.confluence' : 504})

class contextMenu:
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
            from modules.indexers import trakt
            if watched == 7: trakt.markMovieAsWatched(imdb)
            else: trakt.markMovieAsNotWatched(imdb)
            trakt.syncMovies()
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
            from modules.indexers import trakt
            if watched == 7: trakt.markEpisodeAsWatched(tvdb, season, episode)
            else: trakt.markEpisodeAsNotWatched(tvdb, season, episode)
            trakt.syncTVShows()
        except:
            pass

        index().container_refresh()

    def playcount_shows(self, name, year, imdb, tvdb, season, watched, metahandler=True):
        try:
            if (getSetting("trakt_user") == '' or getSetting("trakt_password") == ''): traktMode = False
            else: traktMode = True
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

            match = episodes().get(name, year, imdb, tvdb, season, idx=False)
            match = match[1]['episodes']
            match = [{'name': i['name'], 'season': int('%01d' % int(i['season'])), 'episode': int('%01d' % int(i['episode']))} for i in match]

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
            from modules.indexers import trakt
            if watched == 7: trakt.markTVShowAsWatched(tvdb)
            else: trakt.markTVShowAsNotWatched(tvdb)
            trakt.syncTVShows()
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
                from modules.sources import sources
                src = sources().getSources(name, title, year, imdb, None, None, None, None, None, None, None)
                if not len(src) > 0: raise Exception()

            self.library_movie_strm({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'url': url})
        except:
            pass

        if batch == True: return

        index().infoDialog(language(30317).encode("utf-8"), str(name))

        if getSetting("update_library") == 'true' and not xbmc.getCondVisibility('Library.IsScanningVideo'):
            xbmc.executebuiltin('UpdateLibrary(video)')

    def library_movie_list(self, url):
        yes = index().yesnoDialog(language(30341).encode("utf-8"), '')
        if not yes: return

        index().infoDialog(language(30315).encode("utf-8"), language(30311).encode("utf-8"), time=10000000)

        if url == 'trakt_collection':
            url = link().trakt_collection % link().trakt_user
        elif url == 'trakt_watchlist':
            url = link().trakt_watchlist % link().trakt_user
        elif url == 'imdb_watchlist':
            url = link().imdb_watchlist % link().imdb_user

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
        xbmc.executebuiltin('RunPlugin(%s?action=library_movie_list&url=%s)' % (sys.argv[0], urllib.quote_plus(url)))

    def library_movie_strm(self, i):
        try:
            name, title, year, imdb, url = i['name'], i['title'], i['year'], i['imdb'], i['url']

            sysname, systitle, sysyear, sysimdb, sysurl = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(url)

            content = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s&url=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, sysurl)

            xbmcvfs.mkdir(movieLibrary)

            enc_name = name.translate(None, '\/:*?"<>|').strip('.')
            folder = os.path.join(movieLibrary, enc_name)

            try: xbmcvfs.mkdir(folder)
            except: pass
            try:
				if not 'ftp://' in folder: raise Exception()
				from ftplib import FTP
				ftparg = re.compile('ftp://(.+?):(.+?)@(.+?):?(\d+)?/(.+/?)').findall(folder)
				ftp = FTP(ftparg[0][2],ftparg[0][0],ftparg[0][1])
				try: ftp.cwd(ftparg[0][4])
				except: ftp.mkd(ftparg[0][4])
				ftp.quit()
            except:
				pass

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
                        from modules.sources import sources
                        src = sources().getSources(i['name'], i['title'], i['year'], i['imdb'], i['tvdb'], i['season'], i['episode'], i['show'], i['show_alt'], i['date'], i['genre'])
                        if len(src) > 0: block = False
                    if block == True: raise Exception()

                l = 'S%02dE%02d' % (int(i['season']), int(i['episode']))
                if l in lib: raise Exception()

                if date <= int(re.sub('[^0-9]', '', str(i['date']))):
                    from modules.sources import sources
                    src = sources().getSources(i['name'], i['title'], i['year'], i['imdb'], i['tvdb'], i['season'], i['episode'], i['show'], i['show_alt'], i['date'], i['genre'])
                    if not len(src) > 0: raise Exception()

                self.library_tv_strm(i)
            except:
                pass

        if batch == True: return

        index().infoDialog(language(30317).encode("utf-8"), str(name))

        if getSetting("update_library") == 'true' and not xbmc.getCondVisibility('Library.IsScanningVideo'):
            xbmc.executebuiltin('UpdateLibrary(video)')

    def library_tv_list(self, url):
        yes = index().yesnoDialog(language(30341).encode("utf-8"), '')
        if not yes: return

        index().infoDialog(language(30315).encode("utf-8"), language(30312).encode("utf-8"), time=10000000)

        if url == 'trakt_tv_collection':
            url = link().trakt_tv_collection % link().trakt_user
        elif url == 'trakt_tv_watchlist':
            url = link().trakt_tv_watchlist % link().trakt_user
        elif url == 'imdb_tv_watchlist':
            url = link().imdb_watchlist % link().imdb_user

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
        xbmc.executebuiltin('RunPlugin(%s?action=library_tv_list&url=%s)' % (sys.argv[0], urllib.quote_plus(url)))

    def library_tv_strm(self, i):
        try:
            name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, url = i['name'], i['title'], i['year'], i['imdb'], i['tvdb'], i['season'], i['episode'], i['show'], i['show_alt'], i['date'], i['genre'], i['url']

            sysname, systitle, sysyear, sysimdb, systvdb, sysseason, sysepisode, sysshow, sysshow_alt, sysdate, sysgenre, sysurl = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(season), urllib.quote_plus(episode), urllib.quote_plus(show), urllib.quote_plus(show_alt), urllib.quote_plus(date), urllib.quote_plus(genre), urllib.quote_plus(url)

            content = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s&show=%s&show_alt=%s&date=%s&genre=%s&url=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, systvdb, sysseason, sysepisode, sysshow, sysshow_alt, sysdate, sysgenre, sysurl)

            xbmcvfs.mkdir(tvLibrary)

            enc_show = show_alt.translate(None, '\/:*?"<>|').strip('.')
            folder = os.path.join(tvLibrary, enc_show+'/')

            try: xbmcvfs.mkdir(folder)
            except: pass
            try:
				if not 'ftp://' in folder: raise Exception()
				from ftplib import FTP		
				ftparg = re.compile('ftp://(.+?):(.+?)@(.+?):?(\d+)?/(.+/?)').findall(folder)
				ftp = FTP(ftparg[0][2],ftparg[0][0],ftparg[0][1])
				try: ftp.cwd(ftparg[0][4])
				except: ftp.mkd(ftparg[0][4])
				ftp.quit()
            except:
				pass

            enc_season = 'Season %s' % season.translate(None, '\/:*?"<>|').strip('.')
            folder = os.path.join(folder, enc_season)

            try: xbmcvfs.mkdir(folder)
            except: pass
            try:
				if not 'ftp://' in folder: raise Exception()
				from ftplib import FTP		
				ftparg = re.compile('ftp://(.+?):(.+?)@(.+?):?(\d+)?/(.+/?)').findall(folder)
				ftp = FTP(ftparg[0][2],ftparg[0][0],ftparg[0][1])
				try: ftp.cwd(ftparg[0][4])
				except: ftp.mkd(ftparg[0][4])
				ftp.quit()
            except:
				pass

            enc_name = name.translate(None, '\/:*?"<>|').strip('.')
            stream = os.path.join(folder, enc_name + '.strm')
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
                        from modules.sources import sources
                        src = sources().getSources(i['name'], i['title'], i['year'], i['imdb'], i['tvdb'], i['season'], i['episode'], i['show'], i['show_alt'], i['date'], i['genre'])
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

                if not getSetting("service_update") == 'true': raise Exception()
                try: notify = getSetting("service_notification")
                except: notify = 'true'
                self.library_update(notify)
            except:
                pass

            xbmc.sleep(10000)

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
        self.imdb_genres_type = 'http://www.imdb.com/search/title?title_type=%s&sort=num_votes,desc&count=25&start=1'
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

        self.scn_base = 'http://www.watchfree.to'
        self.scn_link_1 = 'http://www.watchfree.to'
        self.scn_link_2 = 'http://translate.googleusercontent.com/translate_c?anno=2&hl=en&sl=mt&tl=en&u=http://www.watchfree.to'
        self.scn_link_3 = 'https://watchfree.unblocked.pw'
        self.scn_added = '/?page=1'
        self.scn_added_hd = '/?page=1'

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
                if 'documentary' == url: url = link().imdb_genres_type % url
                else: url = link().imdb_genres % url
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

        self.list = [i for i in self.list if not i['genre'] == '0']
        self.list = [i for i in self.list if not any(x in i['genre'].lower() for x in ['adult', 'porn'])]

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
                result = result.decode('iso-8859-1').encode('utf-8')
                movies = common.parseDOM(result, "div", attrs = { "class": "item" })
                if len(movies) > 0: break
        except:
            return

        try:
            next = common.parseDOM(result, "div", attrs = { "class": "pagination" })[0]
            next = re.compile('(<a.+?</a>)').findall(next)
            next = [i for i in next if '>>' in i or '&gt;&gt;' in i][-1]
            next = re.compile('href=(.+?)>').findall(next)[-1]
            next = common.replaceHTMLCodes(next)
            next = next.replace('\'', '').replace('"', '')
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
                title = title.lstrip('Watch').strip()
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = common.parseDOM(movie, "a", ret="title")[0]
                year = re.compile('.+? [(](\d{4})[)]$').findall(year)[0]
                year = year.encode('utf-8')

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                poster = '0'
                try: poster = common.parseDOM(movie, "img", ret="src")[0]
                except: pass
                poster = common.replaceHTMLCodes(poster)
                try: poster = urlparse.parse_qs(urlparse.urlparse(poster).query)['u'][0]
                except: pass
                if poster.startswith('//'): poster = 'http:' + poster
                poster = poster.encode('utf-8')

                self.list.append({'name': name, 'title': title, 'year': year, 'imdb': '0000000', 'tvdb': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'date': '0', 'genre': '0', 'url': '0', 'poster': poster, 'fanart': '0', 'studio': '0', 'duration': '0', 'rating': '0', 'votes': '0', 'mpaa': '0', 'director': '0', 'plot': '0', 'plotoutline': '0', 'tagline': '0', 'next': next})
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

        self.list = [i for i in self.list if not i['genre'] == '0']
        self.list = [i for i in self.list if not any(x in i['genre'].lower() for x in ['adult', 'porn'])]

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


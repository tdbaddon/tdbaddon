# -*- coding: utf-8 -*-

'''
    Much Movies HD Add-on
    Copyright (C) 2014 lambda

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

import urllib,urllib2,re,os,threading,datetime,time,base64,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs,urlparse
from operator import itemgetter
try:    import json
except: import simplejson as json
try:    import CommonFunctions
except: import commonfunctionsdummy as CommonFunctions
try:    import StorageServer
except: import storageserverdummy as StorageServer
from metahandler import metahandlers
from metahandler import metacontainers
from resources.lib.libraries import cleantitle
from resources.lib.libraries import cloudflare
from resources.lib.libraries import client


action              = None
common              = CommonFunctions
metaget             = metahandlers.MetaData(preparezip=False)
language            = xbmcaddon.Addon().getLocalizedString
setSetting          = xbmcaddon.Addon().setSetting
getSetting          = xbmcaddon.Addon().getSetting
addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
addonFullId         = addonName + addonVersion
addonDesc           = language(30450).encode("utf-8")
cache               = StorageServer.StorageServer(addonFullId,1).cacheFunction
cache2              = StorageServer.StorageServer(addonFullId,24).cacheFunction
cache3              = StorageServer.StorageServer(addonFullId,720).cacheFunction
addonIcon           = os.path.join(addonPath,'icon.png')
addonFanart         = os.path.join(addonPath,'fanart.jpg')
addonArt            = os.path.join(addonPath,'resources/art')
addonDownloads      = os.path.join(addonPath,'resources/art/Downloads.png')
addonPages          = os.path.join(addonPath,'resources/art/Pages.png')
addonNext           = os.path.join(addonPath,'resources/art/Next.png')
dataPath            = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
viewData            = os.path.join(dataPath,'views.cfg')
offData             = os.path.join(dataPath,'offset.cfg')
favData             = os.path.join(dataPath,'favourites.cfg')


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
        try:        url = urllib.unquote_plus(params["url"])
        except:     url = None
        try:        image = urllib.unquote_plus(params["image"])
        except:     image = None
        try:        query = urllib.unquote_plus(params["query"])
        except:     query = None
        try:        title = urllib.unquote_plus(params["title"])
        except:     title = None
        try:        year = urllib.unquote_plus(params["year"])
        except:     year = None
        try:        imdb = urllib.unquote_plus(params["imdb"])
        except:     imdb = None

        if action == None:                          root().get()
        elif action == 'item_play':                 contextMenu().item_play()
        elif action == 'item_random_play':          contextMenu().item_random_play()
        elif action == 'item_queue':                contextMenu().item_queue()
        elif action == 'favourite_add':             contextMenu().favourite_add(favData, name, url, image, imdb)
        elif action == 'favourite_from_search':     contextMenu().favourite_from_search(favData, name, url, image, imdb)
        elif action == 'favourite_delete':          contextMenu().favourite_delete(favData, name, url)
        elif action == 'favourite_moveUp':          contextMenu().favourite_moveUp(favData, name, url)
        elif action == 'favourite_moveDown':        contextMenu().favourite_moveDown(favData, name, url)
        elif action == 'playlist_open':             contextMenu().playlist_open()
        elif action == 'settings_open':             contextMenu().settings_open()
        elif action == 'addon_home':                contextMenu().addon_home()
        elif action == 'view_movies':               contextMenu().view('movies')
        elif action == 'metadata_movies':           contextMenu().metadata('movie', name, url, imdb, '', '')
        elif action == 'metadata_movies2':          contextMenu().metadata('movie', name, url, imdb, '', '')
        elif action == 'playcount_movies':          contextMenu().playcount('movie', imdb, '', '')
        elif action == 'library_add':               contextMenu().library_add(name, url)
        elif action == 'download':                  contextMenu().download(name, url)
        elif action == 'trailer':                   contextMenu().trailer(name, url)
        elif action == 'movies':                    movies().get(url)
        elif action == 'movies_title':              movies().title()
        elif action == 'movies_release':            movies().release()
        elif action == 'movies_added':              movies().added()
        elif action == 'movies_rating':             movies().rating()
        elif action == 'movies_search':             movies().search(query)
        elif action == 'movies_favourites':         favourites().movies()
        elif action == 'pages_movies':              pages().get()
        elif action == 'genres_movies':             genres().get()
        elif action == 'play':                      resolver().run(url, name)

        if action is None:
            pass
        elif action.startswith('movies'):
            xbmcplugin.setContent(int(sys.argv[1]), 'movies')
            index().container_view('movies', {'skin.confluence' : 500})
        xbmcplugin.setPluginFanart(int(sys.argv[1]), addonFanart)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        return
        
class getUrl(object):
    def __init__(self, url, close=True, proxy=None, post=None, mobile=False, referer=None, cookie=None, output='', timeout='10'):
        if not proxy is None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
            opener = urllib2.install_opener(opener)
        if not post is None:
            request = urllib2.Request(url, post)
        else:
            request = urllib2.Request(url,None)
        if mobile == True:
            request.add_header('User-Agent', 'Apple-iPhone/701.341')
        else:
            #request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')
            request.add_header('User-Agent', 'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko')
        if not referer is None:
            request.add_header('Referer', referer)
        if not cookie is None:
            request.add_header('cookie', cookie)
        response = urllib2.urlopen(request, timeout=int(timeout))
        if output == 'cookie':
            result = str(response.headers.get('Set-Cookie'))
        elif output == 'geturl':
            result = response.geturl()
        else:
            result = response.read()
        if close == True:
            response.close()
        self.result = result        

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
        self.PseudoTVRunning = index().getProperty('PseudoTVRunning')
        self.loadingStarting = time.time()
        xbmc.Player.__init__(self)

    def run(self, name, url, imdb='0'):
        self.video_info(name, imdb)

        if self.folderPath.startswith(sys.argv[0]) or self.PseudoTVRunning == 'True':
            item = xbmcgui.ListItem(path=url)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        else:
            try:
                file = self.name + '.strm'
                file = file.translate(None, '\/:*?"<>|')

                meta = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties" : ["title", "genre", "year", "rating", "director", "trailer", "tagline", "plot", "plotoutline", "originaltitle", "lastplayed", "playcount", "writer", "studio", "mpaa", "country", "imdbnumber", "runtime", "votes", "fanart", "thumbnail", "file", "sorttitle", "resume", "dateadded"]}, "id": 1}' % (self.year, str(int(self.year)+1), str(int(self.year)-1)))
                meta = unicode(meta, 'utf-8', errors='ignore')
                meta = json.loads(meta)
                meta = meta['result']['movies']
                self.meta = [i for i in meta if i['file'].endswith(file)][0]
                meta = {'title': self.meta['title'], 'originaltitle': self.meta['originaltitle'], 'year': self.meta['year'], 'genre': str(self.meta['genre']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'director': str(self.meta['director']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'country': str(self.meta['country']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'rating': self.meta['rating'], 'votes': self.meta['votes'], 'mpaa': self.meta['mpaa'], 'duration': self.meta['runtime'], 'trailer': self.meta['trailer'], 'writer': str(self.meta['writer']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'studio': str(self.meta['studio']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'tagline': self.meta['tagline'], 'plotoutline': self.meta['plotoutline'], 'plot': self.meta['plot']}
                poster = self.meta['thumbnail']
            except:
                meta = {'label': self.name, 'title': self.name}
                poster = ''
            item = xbmcgui.ListItem(path=url, iconImage="DefaultVideo.png", thumbnailImage=poster)
            item.setInfo( type="Video", infoLabels= meta )
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

        for i in range(0, 250):
            try: self.totalTime = self.getTotalTime()
            except: self.totalTime = 0
            if not self.totalTime == 0: continue
            xbmc.sleep(1000)
        if self.totalTime == 0: return

        while True:
            try: self.currentTime = self.getTime()
            except: break
            xbmc.sleep(1000)

    def video_info(self, name, imdb):
        self.name = name
        self.content = 'movie'
        self.title = self.name.rsplit(' (', 1)[0].strip()
        self.year = '%04d' % int(self.name.rsplit(' (', 1)[-1].split(')')[0])
        if imdb == '0': imdb = metaget.get_meta('movie', self.title ,year=str(self.year))['imdb_id']
        self.imdb = re.sub('[^0-9]', '', imdb)
        self.subtitle = subtitles().get(self.name, self.imdb, '', '')

    def container_refresh(self):
        try:
            params = {}
            query = self.folderPath[self.folderPath.find('?') + 1:].split('&')
            for i in query: params[i.split('=')[0]] = i.split('=')[1]
            if not params["action"].endswith('_search'): index().container_refresh()
        except:
            pass

    def offset_add(self):
        try:
            file = xbmcvfs.File(offData)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write.append('"%s"|"%s"|"%s"' % (self.name, self.imdb, self.currentTime))
            write = '\r\n'.join(write)
            file = xbmcvfs.File(offData, 'w')
            file.write(str(write))
            file.close()
        except:
            return

    def offset_delete(self):
        try:
            file = xbmcvfs.File(offData)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write = [i for i in write if not '"%s"|"%s"|"' % (self.name, self.imdb) in i]
            write = '\r\n'.join(write)
            file = xbmcvfs.File(offData, 'w')
            file.write(str(write))
            file.close()
        except:
            return

    def offset_read(self):
        try:
            self.offset = '0'
            file = xbmcvfs.File(offData)
            read = file.read()
            file.close()
            read = [i for i in read.splitlines(True) if '"%s"|"%s"|"' % (self.name, self.imdb) in i][0]
            self.offset = re.compile('".+?"[|]".+?"[|]"(.+?)"').findall(read)[0]
        except:
            return

    def change_watched(self):
        try:
            xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid" : %s, "playcount" : 1 }, "id": 1 }' % str(self.meta['movieid']))
        except:
            metaget.change_watched(self.content, '', self.imdb, season='', episode='', year='', watched=7)

    def resume_playback(self):
        offset = float(self.offset)
        if not offset > 0: return
        minutes, seconds = divmod(offset, 60)
        hours, minutes = divmod(minutes, 60)
        offset_time = '%02d:%02d:%02d' % (hours, minutes, seconds)
        yes = index().yesnoDialog('%s %s' % (language(30350).encode("utf-8"), offset_time), '', self.name, language(30351).encode("utf-8"), language(30352).encode("utf-8"))
        if yes: self.seekTime(offset)

    def onPlayBackStarted(self):
        try: self.setSubtitles(self.subtitle)
        except: pass

        if self.PseudoTVRunning == 'True': return

        if getSetting("playback_info") == 'true':
            elapsedTime = '%s %.2f seconds' % (language(30319).encode("utf-8"), (time.time() - self.loadingStarting))     
            index().infoDialog(elapsedTime, header=self.name)

        if getSetting("resume_playback") == 'true':
            self.offset_read()
            self.resume_playback()

    def onPlayBackEnded(self):
        if self.PseudoTVRunning == 'True': return
        self.change_watched()
        self.offset_delete()
        self.container_refresh()

    def onPlayBackStopped(self):
        if self.PseudoTVRunning == 'True': return
        if self.currentTime / self.totalTime >= .9:
            self.change_watched()
        self.offset_delete()
        self.offset_add()
        self.container_refresh()

class subtitles:
    def get(self, name, imdb, season, episode):
        if not getSetting("subtitles") == 'true': return
        quality = ['bluray', 'hdrip', 'brrip', 'bdrip', 'dvdrip', 'webrip', 'hdtv']
        langDict = {'Afrikaans': 'afr', 'Albanian': 'alb', 'Arabic': 'ara', 'Armenian': 'arm', 'Basque': 'baq', 'Bengali': 'ben', 'Bosnian': 'bos', 'Breton': 'bre', 'Bulgarian': 'bul', 'Burmese': 'bur', 'Catalan': 'cat', 'Chinese': 'chi', 'Croatian': 'hrv', 'Czech': 'cze', 'Danish': 'dan', 'Dutch': 'dut', 'English': 'eng', 'Esperanto': 'epo', 'Estonian': 'est', 'Finnish': 'fin', 'French': 'fre', 'Galician': 'glg', 'Georgian': 'geo', 'German': 'ger', 'Greek': 'ell', 'Hebrew': 'heb', 'Hindi': 'hin', 'Hungarian': 'hun', 'Icelandic': 'ice', 'Indonesian': 'ind', 'Italian': 'ita', 'Japanese': 'jpn', 'Kazakh': 'kaz', 'Khmer': 'khm', 'Korean': 'kor', 'Latvian': 'lav', 'Lithuanian': 'lit', 'Luxembourgish': 'ltz', 'Macedonian': 'mac', 'Malay': 'may', 'Malayalam': 'mal', 'Manipuri': 'mni', 'Mongolian': 'mon', 'Montenegrin': 'mne', 'Norwegian': 'nor', 'Occitan': 'oci', 'Persian': 'per', 'Polish': 'pol', 'Portuguese': 'por,pob', 'Portuguese(Brazil)': 'pob,por', 'Romanian': 'rum', 'Russian': 'rus', 'Serbian': 'scc', 'Sinhalese': 'sin', 'Slovak': 'slo', 'Slovenian': 'slv', 'Spanish': 'spa', 'Swahili': 'swa', 'Swedish': 'swe', 'Syriac': 'syr', 'Tagalog': 'tgl', 'Tamil': 'tam', 'Telugu': 'tel', 'Thai': 'tha', 'Turkish': 'tur', 'Ukrainian': 'ukr', 'Urdu': 'urd'}

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
            result = server.SearchSubtitles(token, [{'sublanguageid': langs, 'imdbid': imdb}])['data']
            result = [i for i in result if i['SubSumCD'] == '1']
        except:
            return

        subtitles = []
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
            index().infoDialog(language(30317).encode("utf-8"), name)
            return

class index:
    def infoDialog(self, str, header=addonName):
        try: xbmcgui.Dialog().notification(header, str, addonIcon, 3000, sound=False)
        except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % (header, str, addonIcon))

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
        xbmc.executebuiltin("Container.Refresh")

    def container_data(self):
        if not xbmcvfs.exists(dataPath):
            xbmcvfs.mkdir(dataPath)
        if not xbmcvfs.exists(favData):
            file = xbmcvfs.File(favData, 'w')
            file.write('')
            file.close()
        if not xbmcvfs.exists(viewData):
            file = xbmcvfs.File(viewData, 'w')
            file.write('')
            file.close()
        if not xbmcvfs.exists(offData):
            file = xbmcvfs.File(offData, 'w')
            file.write('')
            file.close()

    def container_view(self, content, viewDict):
        try:
            skin = xbmc.getSkinDir()
            file = xbmcvfs.File(viewData)
            read = file.read().replace('\n','')
            file.close()
            view = re.compile('"%s"[|]"%s"[|]"(.+?)"' % (skin, content)).findall(read)[0]
            xbmc.executebuiltin('Container.SetViewMode(%s)' % str(view))
        except:
            try:
                id = str(viewDict[skin])
                xbmc.executebuiltin('Container.SetViewMode(%s)' % id)
            except:
                pass

    def rootList(self, rootList):
        total = len(rootList)
        for i in rootList:
            try:
                name = language(i['name']).encode("utf-8")
                image = '%s/%s' % (addonArt, i['image'])
                action = i['action']
                u = '%s?action=%s' % (sys.argv[0], action)

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems([], replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def pageList(self, pageList):
        if pageList == None or len(pageList) == 0: return

        total = len(pageList)
        for i in pageList:
            try:
                name, url, image = i['name'], i['url'], i['image']
                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)

                u = '%s?action=movies&url=%s' % (sys.argv[0], sysurl)

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems([], replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def nextList(self, nextList):
        try: next = nextList[0]['next']
        except: return
        if next == '': return
        name, url, image = language(30361).encode("utf-8"), next, addonNext
        sysurl = urllib.quote_plus(url)

        u = '%s?action=movies&url=%s' % (sys.argv[0], sysurl)

        item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
        item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
        item.setProperty("Fanart_Image", addonFanart)
        item.addContextMenuItems([], replaceItems=False)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)

    def downloadList(self):
        u = getSetting("downloads")
        if u == '': return
        name, image = language(30363).encode("utf-8"), addonDownloads

        item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
        item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
        item.setProperty("Fanart_Image", addonFanart)
        item.addContextMenuItems([], replaceItems=False)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)

    def movieList(self, movieList):
        if movieList == None or len(movieList) == 0: return

        getmeta = getSetting("meta")

        file = xbmcvfs.File(favData)
        favRead = file.read()
        file.close()

        total = len(movieList)
        for i in movieList:
            try:
                name, url, image, title, year, imdb, genre, plot = i['name'], i['url'], i['image'], i['title'], i['year'], i['imdb'], i['genre'], i['plot']
                if plot == '': plot = addonDesc
                if genre == '': genre = ' '

                sysname, sysurl, sysimage, systitle, sysimdb = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(title), urllib.quote_plus(imdb)
                u = '%s?action=play&name=%s&url=%s&t=%s' % (sys.argv[0], sysname, sysurl, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))

                if getmeta == 'true':
                    meta = metaget.get_meta('movie', title ,year=year)
                    playcountMenu = language(30407).encode("utf-8")
                    if meta['overlay'] == 6: playcountMenu = language(30408).encode("utf-8")
                    metaimdb = urllib.quote_plus(re.sub('[^0-9]', '', meta['imdb_id']))
                    trailer, poster = urllib.quote_plus(meta['trailer_url']), meta['cover_url']
                    if trailer == '': trailer = sysurl
                    if poster == '': poster = image
                else:
                    meta = {'label': title, 'title': title, 'year': year, 'imdb_id' : imdb, 'genre' : genre, 'plot': plot}
                    trailer, poster = sysurl, image
                if getmeta == 'true' and getSetting("fanart") == 'true':
                    fanart = meta['backdrop_url']
                    if fanart == '': fanart = addonFanart
                else:
                    fanart = addonFanart

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=download&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                cm.append((language(30412).encode("utf-8"), 'Action(Info)'))
                if action == 'movies_favourites':
                    if not getSetting("fav_sort") == '2': cm.append((language(30416).encode("utf-8"), 'RunPlugin(%s?action=trailer&name=%s&url=%s)' % (sys.argv[0], sysname, trailer)))
                    if getmeta == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_movies&name=%s&url=%s&imdb=%s)' % (sys.argv[0], systitle, sysurl, metaimdb)))
                    if getmeta == 'true': cm.append((playcountMenu, 'RunPlugin(%s?action=playcount_movies&imdb=%s)' % (sys.argv[0], metaimdb)))
                    cm.append((language(30422).encode("utf-8"), 'RunPlugin(%s?action=library_add&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30428).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))
                    if getSetting("fav_sort") == '2': cm.append((language(30419).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveUp&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    if getSetting("fav_sort") == '2': cm.append((language(30420).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveDown&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30421).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                elif action == 'movies_search':
                    cm.append((language(30416).encode("utf-8"), 'RunPlugin(%s?action=trailer&name=%s&url=%s)' % (sys.argv[0], sysname, trailer)))
                    cm.append((language(30422).encode("utf-8"), 'RunPlugin(%s?action=library_add&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_from_search&name=%s&imdb=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage)))
                    cm.append((language(30428).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))
                else:
                    cm.append((language(30416).encode("utf-8"), 'RunPlugin(%s?action=trailer&name=%s&url=%s)' % (sys.argv[0], sysname, trailer)))
                    if getmeta == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_movies2&name=%s&url=%s&imdb=%s)' % (sys.argv[0], systitle, sysurl, metaimdb)))
                    cm.append((language(30422).encode("utf-8"), 'RunPlugin(%s?action=library_add&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    if not '"%s"' % url in favRead: cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_add&name=%s&imdb=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage)))
                    else: cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30428).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))
                    cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("art(poster)", poster)
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

class contextMenu:
    def item_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.unshuffle()
        xbmc.Player().play(playlist)

    def item_random_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.shuffle()
        xbmc.Player().play(playlist)

    def item_queue(self):
        xbmc.executebuiltin('Action(Queue)')

    def playlist_open(self):
        xbmc.executebuiltin('ActivateWindow(VideoPlaylist)')

    def settings_open(self):
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % (addonId))

    def addon_home(self):
        xbmc.executebuiltin('Container.Update(plugin://%s/,replace)' % (addonId))

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
                if not (label == '' or label is None): break
            file = xbmcvfs.File(viewData)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write = [i for i in write if not '"%s"|"%s"|"' % (skin, content) in i]
            write.append('"%s"|"%s"|"%s"' % (skin, content, str(view)))
            write = '\r\n'.join(write)
            file = xbmcvfs.File(viewData, 'w')
            file.write(str(write))
            file.close()
            viewName = xbmc.getInfoLabel('Container.Viewmode')
            index().infoDialog('%s%s%s' % (language(30301).encode("utf-8"), viewName, language(30302).encode("utf-8")))
        except:
            return

    def favourite_add(self, data, name, url, image, imdb):
        try:
            index().container_refresh()
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write.append('"%s"|"%s"|"%s"\n' % (name, url, image))
            write = '\r\n'.join(write)
            file = xbmcvfs.File(data, 'w')
            file.write(str(write))
            file.close()
            index().infoDialog(language(30303).encode("utf-8"), name)
        except:
            return

    def favourite_from_search(self, data, name, url, image, imdb):
        try:
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            if '"%s"' % url in read:
                index().infoDialog(language(30307).encode("utf-8"), name)
                return
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write.append('"%s"|"%s"|"%s"\n' % (name, url, image))
            write = '\r\n'.join(write)
            file = xbmcvfs.File(data, 'w')
            file.write(str(write))
            file.close()
            index().infoDialog(language(30303).encode("utf-8"), name)
        except:
            return

    def favourite_delete(self, data, name, url):
        try:
            index().container_refresh()
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write = [i for i in write if not '"%s"' % url in i]
            write = '\r\n'.join(write)
            file = xbmcvfs.File(data, 'w')
            file.write(str(write))
            file.close()
            index().infoDialog(language(30304).encode("utf-8"), name)
        except:
            return

    def favourite_moveUp(self, data, name, url):
        try:
            index().container_refresh()
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            i = write.index([i for i in write if '"%s"' % url in i][0])
            if i == 0 : return
            write[i], write[i-1] = write[i-1], write[i]
            write = '\r\n'.join(write)
            file = xbmcvfs.File(data, 'w')
            file.write(str(write))
            file.close()
            index().infoDialog(language(30305).encode("utf-8"), name)
        except:
            return

    def favourite_moveDown(self, data, name, url):
        try:
            index().container_refresh()
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            i = write.index([i for i in write if '"%s"' % url in i][0])
            if i+1 == len(write): return
            write[i], write[i+1] = write[i+1], write[i]
            write = '\r\n'.join(write)
            file = xbmcvfs.File(data, 'w')
            file.write(str(write))
            file.close()
            index().infoDialog(language(30306).encode("utf-8"), name)
        except:
            return

    def metadata(self, content, name, url, imdb, season, episode):
        try:
            if content == 'movie' or content == 'tvshow':
                metaget.update_meta(content, '', imdb, year='')
                index().container_refresh()
            elif content == 'season':
                metaget.update_episode_meta('', imdb, season, episode)
                index().container_refresh()
            elif content == 'episode':
                metaget.update_season('', imdb, season)
                index().container_refresh()
        except:
            return

    def playcount(self, content, imdb, season, episode):
        try:
            metaget.change_watched(content, '', imdb, season=season, episode=episode, year='', watched='')
            index().container_refresh()
        except:
            return

    def library_add(self, name, url, update=True, silent=False):
        try:
            self.library(name, url)

            if silent == False:
                index().container_refresh()
                index().infoDialog(language(30311).encode("utf-8"), name)
            if update == True:
                xbmc.executebuiltin('UpdateLibrary(video)')
        except:
            return

    def library(self, name, url):
        try:
            library = xbmc.translatePath(getSetting("movie_library"))
            sysname, sysurl = urllib.quote_plus(name), urllib.quote_plus(url)
            content = '%s?action=play&name=%s&url=%s' % (sys.argv[0], sysname, sysurl)
            enc_name = name.translate(None, '\/:*?"<>|')
            folder = os.path.join(library, enc_name)
            stream = os.path.join(folder, enc_name + '.strm')
            xbmcvfs.mkdir(dataPath)
            xbmcvfs.mkdir(library)
            xbmcvfs.mkdir(folder)
            file = xbmcvfs.File(stream, 'w')
            file.write(str(content))
            file.close()
        except:
            return

    def download(self, name, url):
        try:
            property = (addonName+name)+'download'
            download = xbmc.translatePath(getSetting("downloads"))
            enc_name = name.translate(None, '\/:*?"<>|')
            xbmcvfs.mkdir(dataPath)
            xbmcvfs.mkdir(download)

            file = [i for i in xbmcvfs.listdir(download)[1] if i.startswith(enc_name + '.')]
            if not file == []: file = os.path.join(download, file[0])
            else: file = None

            if download == '':
            	yes = index().yesnoDialog(language(30341).encode("utf-8"), language(30342).encode("utf-8"))
            	if yes: contextMenu().settings_open()
            	return

            if file is None:
            	pass
            elif not file.endswith('.tmp'):
            	yes = index().yesnoDialog(language(30343).encode("utf-8"), language(30344).encode("utf-8"), name)
            	if yes:
            	    xbmcvfs.delete(file)
            	else:
            	    return
            elif file.endswith('.tmp'):
            	if index().getProperty(property) == 'open':
            	    yes = index().yesnoDialog(language(30345).encode("utf-8"), language(30346).encode("utf-8"), name)
            	    if yes: index().setProperty(property, 'cancel')
            	    return
            	else:
            	    xbmcvfs.delete(file)

            url = resolver().run(url, name, download=True)
            if url is None: return
            url = url.rsplit('|', 1)[0]
            ext = url.rsplit('/', 1)[-1].rsplit('?', 1)[0].rsplit('|', 1)[0].strip().lower()
            ext = os.path.splitext(ext)[1][1:]
            if ext == '': ext = 'mp4'
            stream = os.path.join(download, enc_name + '.' + ext)
            temp = stream + '.tmp'

            count = 0
            CHUNK = 16 * 1024
            request = urllib2.Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
            request.add_header('Cookie', 'video=true')
            response = urllib2.urlopen(request, timeout=10)
            size = response.info()["Content-Length"]

            file = xbmcvfs.File(temp, 'w')
            index().setProperty(property, 'open')
            index().infoDialog(language(30308).encode("utf-8"), name)
            while True:
            	chunk = response.read(CHUNK)
            	if not chunk: break
            	if index().getProperty(property) == 'cancel': raise Exception()
            	if xbmc.abortRequested == True: raise Exception()
            	part = xbmcvfs.File(temp)
            	quota = int(100 * float(part.size())/float(size))
            	part.close()
            	if not count == quota and count in [0,10,20,30,40,50,60,70,80,90]:
            		index().infoDialog(language(30309).encode("utf-8") + str(count) + '%', name)
            	file.write(chunk)
            	count = quota
            response.close()
            file.close()

            index().clearProperty(property)
            xbmcvfs.rename(temp, stream)
            index().infoDialog(language(30310).encode("utf-8"), name)
        except:
            file.close()
            index().clearProperty(property)
            xbmcvfs.delete(temp)
            sys.exit()
            return

    def trailer(self, name, url):
        url = trailer().run(name, url)
        if url is None: return
        item = xbmcgui.ListItem(path=url)
        item.setProperty("IsPlayable", "true")
        xbmc.Player().play(url, item)

class favourites:
    def __init__(self):
        self.list = []

    def movies(self):
        file = xbmcvfs.File(favData)
        read = file.read()
        file.close()

        match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
        for name, url, image in match:
            try: year = re.compile('[(](\d{4})[)]').findall(name)[-1]
            except: year = '0'
            title = name.replace('(%s)' % year, '').strip()
            self.list.append({'name': name, 'url': url, 'image': image, 'title': title, 'year': year, 'imdb': '0', 'genre': '', 'plot': ''})

        if getSetting("fav_sort") == '0':
            self.list = sorted(self.list, key=itemgetter('title'))
        elif getSetting("fav_sort") == '1':
            self.list = sorted(self.list, key=itemgetter('title'))[::-1]
            self.list = sorted(self.list, key=itemgetter('year'))[::-1]

        index().movieList(self.list)

class root:
    def get(self):
        rootList = []
        rootList.append({'name': 30501, 'image': 'Title.png', 'action': 'movies_title'})
        rootList.append({'name': 30502, 'image': 'Release.png', 'action': 'movies_release'})
        rootList.append({'name': 30503, 'image': 'Added.png', 'action': 'movies_added'})
        rootList.append({'name': 30504, 'image': 'Rating.png', 'action': 'movies_rating'})
        rootList.append({'name': 30505, 'image': 'Pages.png', 'action': 'pages_movies'})
        rootList.append({'name': 30506, 'image': 'Genres.png', 'action': 'genres_movies'})
        rootList.append({'name': 30507, 'image': 'Favourites.png', 'action': 'movies_favourites'})
        rootList.append({'name': 30508, 'image': 'Search.png', 'action': 'movies_search'})
        index().rootList(rootList)
        index().downloadList()

class link:
    def __init__(self):
        self.muchmovies_base = 'http://umovies.me'
        self.muchmovies_sort = 'http://umovies.me/session/sort'
        self.muchmovies_title = 'http://umovies.me/movies?sort_by=title'
        self.muchmovies_release = 'http://umovies.me/movies?sort_by=release'
        self.muchmovies_added = 'http://umovies.me/movies?sort_by=date_added'
        self.muchmovies_rating = 'http://umovies.me/movies?sort_by=rating'
        self.muchmovies_root = 'http://umovies.me/movies'
        self.muchmovies_search = 'http://umovies.me/search'
        self.muchmovies_genre = 'http://umovies.me/genres'

class pages:
    def __init__(self):
        self.list = []

    def get(self):
        #self.list = self.muchmovies_list(link().muchmovies_base)
        self.list = cache(self.muchmovies_list, link().muchmovies_base)
        index().pageList(self.list)

    def muchmovies_list(self, url):
        try:
            result = cloudflare.source(link().muchmovies_root, mobile=True)

            pages = common.parseDOM(result, "select", attrs = { "class": "goto" })[0]
            pages = re.compile('(<option.+?</option>)').findall(pages)
        except:
            return
        for page in pages:
            try:
                name = common.parseDOM(page, "option")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(page, "option", ret="value")[0]
                url = '%s%s?sort_by=title' % (link().muchmovies_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = addonPages.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

class genres:
    def __init__(self):
        self.list = []

    def get(self):
        #self.list = self.muchmovies_list(link().muchmovies_base)
        self.list = cache3(self.muchmovies_list, link().muchmovies_base)
        index().pageList(self.list)

    def muchmovies_list(self, url):
        try:
            result = cloudflare.source(link().muchmovies_genre, mobile=True)

            genres = common.parseDOM(result, "ul", attrs = { "class": "genres.+?" })
            genres = common.parseDOM(genres, "li")
        except:
            return
        for genre in genres:
            try:
                name = common.parseDOM(genre, "h3")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(genre, "a", ret="href")[0]
                url = '%s%s?sort_by=release' % (link().muchmovies_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(genre, "img", ret="src")[0]
                image = '%s%s' % (link().muchmovies_base, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

class movies:
    def __init__(self):
        self.list = []
        self.data = []

    def get(self, url):
        #self.list = self.muchmovies_list(url)
        self.list = cache(self.muchmovies_list, url)
        index().movieList(self.list)
        index().nextList(self.list)

    def title(self):
        #self.list = self.muchmovies_list(link().muchmovies_title)
        self.list = cache(self.muchmovies_list, link().muchmovies_title)
        index().movieList(self.list)
        index().nextList(self.list)

    def release(self):
        #self.list = self.muchmovies_list(link().muchmovies_release)
        self.list = cache(self.muchmovies_list, link().muchmovies_release)
        index().movieList(self.list)
        index().nextList(self.list)

    def added(self):
        #self.list = self.muchmovies_list(link().muchmovies_added)
        self.list = cache(self.muchmovies_list, link().muchmovies_added)
        index().movieList(self.list)
        index().nextList(self.list)

    def rating(self):
        #self.list = self.muchmovies_list(link().muchmovies_rating)
        self.list = cache(self.muchmovies_list, link().muchmovies_rating)
        index().movieList(self.list)
        index().nextList(self.list)

    def search(self, query=None):
        if query is None:
            self.query = common.getUserInput(language(30362).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query is None or self.query == ''):
            self.query = link().muchmovies_search + '/' + urllib.quote_plus(self.query.replace(' ', '-'))
            self.list = self.muchmovies_list(self.query)
            index().movieList(self.list)
            index().nextList(self.list)

    def muchmovies_list(self, url):
        try:
            post = url.split('?')[-1]
            #result = cloudflare.source(link().muchmovies_sort, post=post, mobile=True, close=False)
            result = cloudflare.source(url, mobile=True)

            movies = common.parseDOM(result, "ul", attrs = { "class": "movies.+?" })
            movies = common.parseDOM(movies, "li")
        except:
            return

        try:
            next = common.parseDOM(result, "ul", attrs = {"class": "segmented.+?" })[0]
            next = common.parseDOM(next, "li")
            next = [i for i in next if '>Next<' in i][0]
            next = common.parseDOM(next, "a", ret="href")[0]
            if next == '#': raise Exception()
            next = '%s%s?%s' % (link().muchmovies_base, next, post)
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for movie in movies:
            try:
                title = common.parseDOM(movie, "h3")[0]
                title = re.compile('(.+?) [(]\d{4}[)]$').findall(title)[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = common.parseDOM(movie, "h3")[0]
                year = re.compile('.+? [(](\d{4})[)]$').findall(year)[0]
                year = year.encode('utf-8')

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                url = common.parseDOM(movie, "a", ret="href")[0]
                url = '%s%s' % (link().muchmovies_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(movie, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'title': title, 'year': year, 'imdb': '0', 'genre': '', 'plot': '', 'next': next})
            except:
                pass

        return self.list

class trailer:
    def __init__(self):
        self.youtube_base = 'http://www.youtube.com'
        self.youtube_query = 'http://gdata.youtube.com/feeds/api/videos?q='
        self.youtube_watch = 'http://www.youtube.com/watch?v=%s'
        self.youtube_info = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2'

    def run(self, name, url):
        try:
            if url.startswith(self.youtube_base):
                url = self.youtube(url)
                if url is None: raise Exception()
                return url
            elif not url.startswith('http://'):
                url = self.youtube_watch % url
                url = self.youtube(url)
                if url is None: raise Exception()
                return url
            else:
                raise Exception()
        except:
            url = self.youtube_query + name + ' trailer'
            url = self.youtube_search(url)
            if url is None: return
            return url

    def youtube_search(self, url):
        try:
            if index().addon_status('plugin.video.youtube') is None:
                index().okDialog(language(30321).encode("utf-8"), language(30322).encode("utf-8"))
                return

            query = url.split("?q=")[-1].split("/")[-1].split("?")[0]
            url = url.replace(query, urllib.quote_plus(query))
            result = client.source(url)
            result = common.parseDOM(result, "entry")
            result = common.parseDOM(result, "id")

            for url in result[:5]:
                url = url.split("/")[-1]
                url = self.youtube_watch % url
                url = self.youtube(url)
                if not url is None: return url
        except:
            return

    def youtube(self, url):
        try:
            if index().addon_status('plugin.video.youtube') is None:
                index().okDialog(language(30321).encode("utf-8"), language(30322).encode("utf-8"))
                return
            id = url.split("?v=")[-1].split("/")[-1].split("?")[0].split("&")[0]
            state, reason = None, None
            result = client.source(self.youtube_info % id)
            try:
                state = common.parseDOM(result, "yt:state", ret="name")[0]
                reason = common.parseDOM(result, "yt:state", ret="reasonCode")[0]
            except:
                pass
            if state == 'deleted' or state == 'rejected' or state == 'failed' or reason == 'requesterRegion' : return
            try:
                result = client.source(self.youtube_watch % id)
                alert = common.parseDOM(result, "div", attrs = { "id": "watch7-notification-area" })[0]
                return
            except:
                pass
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % id
            return url
        except:
            return

class resolver:
    def run(self, url, name, download=False):
        try:
            url = self.muchmovies(url)
            if url is None: raise Exception()

            if download == True: return url
            player().run(name, url)
            return url
        except:
            if not index().getProperty('PseudoTVRunning') == 'True':
                index().infoDialog(language(30318).encode("utf-8"))
            return

    def muchmovies(self, url):
        try:
            referer = url
            try: url = link().muchmovies_base + re.compile('//.+?(/.+)').findall(url)[0]
            except: pass

            result = cloudflare.source(url, mobile=True)

            url = common.parseDOM(result, "a", ret="href", attrs = { "data-role": "button" })
            url = [i for i in url if str('.mp4') in i][0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            
            u = '%s://%s' % (urlparse.urlparse(url).scheme, urlparse.urlparse(url).netloc)
            cookie = cloudflare.cloudflare(u, post=None, headers=None, mobile=False, safe=False, timeout='30')
            url = '%s|Accept=%s&User-Agent=%s&Referer=%s&Cookie=%s' % (url, urllib.quote_plus('text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'), urllib.quote_plus(client.agent()), urllib.quote_plus(url), urllib.quote_plus(cookie))
            return url
        except:
            return


main()
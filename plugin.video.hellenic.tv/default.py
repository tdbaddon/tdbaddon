# -*- coding: utf-8 -*-

'''
    Hellenic TV Add-on
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
language            = xbmcaddon.Addon().getLocalizedString
setSetting          = xbmcaddon.Addon().setSetting
getSetting          = xbmcaddon.Addon().getSetting
addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
addonDesc           = language(30450).encode("utf-8")
dataPath            = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile")).decode("utf-8")
addonIcon           = os.path.join(addonPath,'icon.png')
addonArt            = os.path.join(addonPath,'resources/art')
addonLogos          = os.path.join(addonPath,'resources/logos')
addonFanart         = os.path.join(addonPath,'fanart.jpg')
movieImage          = os.path.join(addonArt,'image_movie.jpg')
tvImage             = os.path.join(addonArt,'image_tv.jpg')
episodeImage        = os.path.join(addonArt,'image_episode.jpg')
musicImage          = os.path.join(addonArt,'image_music.jpg')
addonChannels       = 'http://olympia.watchkodi.com/hellenic-tv/channels.xml'
addonCartoons       = 'http://olympia.watchkodi.com/hellenic-tv/cartoons.xml'
addonSettings       = os.path.join(dataPath,'settings.db')
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
        try:        url = urllib.unquote_plus(params["url"])
        except:     url = None
        try:        image = urllib.unquote_plus(params["image"])
        except:     image = None
        try:        channel = urllib.unquote_plus(params["channel"])
        except:     channel = None
        try:        title = urllib.unquote_plus(params["title"])
        except:     title = None
        try:        year = urllib.unquote_plus(params["year"])
        except:     year = None
        try:        show = urllib.unquote_plus(params["show"])
        except:     show = None
        try:        genre = urllib.unquote_plus(params["genre"])
        except:     genre = None
        try:        plot = urllib.unquote_plus(params["plot"])
        except:     plot = None


        try: type = urllib.unquote_plus(params["content_type"])
        except: type = None
        # dirty code for the music addon (content_type doesn't work for shortcuts)
        fp = xbmc.getInfoLabel('Container.FolderPath')
        if any(i in fp for i in ['content_type=audio', 'action=radios_alt']): type = 'audio'
        if type == 'audio' and action == None: action = 'root_radios_alt'


        if action == None:                            root().get()
        elif action == 'cache_clear_list':            index().cache_clear_list()
        elif action == 'item_play':                   contextMenu().item_play()
        elif action == 'item_random_play':            contextMenu().item_random_play()
        elif action == 'item_queue':                  contextMenu().item_queue()
        elif action == 'playlist_open':               contextMenu().playlist_open()
        elif action == 'settings_open':               contextMenu().settings_open()
        elif action == 'view_livetv':                 contextMenu().view('livetv')
        elif action == 'view_radios':                 contextMenu().view('radios')
        elif action == 'view_movies':                 contextMenu().view('movies')
        elif action == 'view_tvshows':                contextMenu().view('tvshows')
        elif action == 'view_episodes':               contextMenu().view('episodes')
        elif action == 'view_cartoons':               contextMenu().view('cartoons')
        elif action == 'favourite_livetv_add':        contextMenu().favourite_add('Live TV', channel, channel, '', '', '', '', '', refresh=True)
        elif action == 'favourite_radio_add':         contextMenu().favourite_add('Radio', url, name, '', '', image, '', '', refresh=True)
        elif action == 'favourite_movie_add':         contextMenu().favourite_add('Movie', url, name, title, year, image, genre, plot, refresh=True)
        elif action == 'favourite_movie_from_search': contextMenu().favourite_add('Movie', url, name, title, year, image, genre, plot)
        elif action == 'favourite_tv_add':            contextMenu().favourite_add('TV Show', url, name, '', '', image, genre, plot, refresh=True)
        elif action == 'favourite_tv_from_search':    contextMenu().favourite_add('TV Show', url, name, '', '', image, genre, plot)
        elif action == 'favourite_cartoons_add':      contextMenu().favourite_add('Cartoons', url, name, title, year, image, genre, plot, refresh=True)
        elif action == 'favourite_delete':            contextMenu().favourite_delete(name, url)
        elif action == 'livetv_refresh':              contextMenu().livetv_refresh()
        elif action == 'root_livetv':                 channels().get()
        elif action == 'root_radios':                 root().radios()
        elif action == 'root_radios_alt':             root().radios_alt()
        elif action == 'root_networks':               root().networks()
        elif action == 'root_shows':                  root().shows()
        elif action == 'root_movies':                 root().movies()
        elif action == 'root_cartoons':               root().cartoons()
        elif action == 'root_favourites':             root().favourites()
        elif action == 'root_news':                   root().news()
        elif action == 'root_sports':                 root().sports()
        elif action == 'root_music':                  root().music()
        elif action == 'livetv_favourites':           favourites().livetv()
        elif action == 'radios_favourites':           favourites().radios()
        elif action == 'radios_alt_favourites':       favourites().radios()
        elif action == 'movies_favourites':           favourites().movies()
        elif action == 'shows_favourites':            favourites().shows()
        elif action == 'cartoons_favourites':         favourites().cartoons()
        elif action == 'radios':                      eradio().radios(url)
        elif action == 'radios_all':                  eradio().radios('radios_link')
        elif action == 'radios_trending':             eradio().radios('trending_link')
        elif action == 'radios_top20':                eradio().radios('top20_link')
        elif action == 'radios_new':                  eradio().radios('new_link')
        elif action == 'radios_alt':                  eradio().radios(url)
        elif action == 'radios_alt_all':              eradio().radios('radios_link')
        elif action == 'radios_alt_trending':         eradio().radios('trending_link')
        elif action == 'radios_alt_top20':            eradio().radios('top20_link')
        elif action == 'radios_alt_new':              eradio().radios('new_link')
        elif action == 'movies_search':               gm().search(url)
        elif action == 'movies':                      gm().movies(url)
        elif action == 'shows_search':                gm().search_tv(url)
        elif action == 'shows':                       gm().shows(url)
        elif action == 'shows_mega':                  mega().shows()
        elif action == 'shows_ant1':                  ant1().shows()
        elif action == 'shows_alpha':                 alpha().shows()
        elif action == 'shows_star':                  star().shows()
        elif action == 'shows_skai':                  skai().shows()
        elif action == 'shows_alt_mega':              gm().network('mega')
        elif action == 'shows_alt_ant1':              gm().network('ant1')
        elif action == 'shows_alt_alpha':             gm().network('alpha')
        elif action == 'shows_alt_star':              gm().network('star')
        elif action == 'shows_alt_skai':              gm().network('skai')
        elif action == 'shows_etv':                   gm().network('epsilontv')
        elif action == 'shows_nerit':                 gm().network('nerit')
        elif action == 'shows_sigma':                 sigma().shows()
        elif action == 'shows_ant1cy':                gm().network('ant1_cy')
        elif action == 'shows_kontra':                youtube().kontra()
        elif action == 'shows_bluesky':               gm().network('bluesky')
        elif action == 'shows_action24':              gm().network('action24')
        elif action == 'shows_art':                   youtube().art()
        elif action == 'shows_mtv':                   gm().network('mtvgreece')
        elif action == 'shows_madtv':                 youtube().madtv()
        elif action == 'shows_hellenictv1':           youtube().hellenictv1()
        elif action == 'shows_real_fm':               realfm().podcasts()
        elif action == 'shows_skai_fm':               skai().podcasts()
        elif action == 'shows_networks':              gm().networks()
        elif action == 'shows_skai_docs':             skai().docs()
        elif action == 'cartoons_collection':         archives().cartoons()
        elif action == 'cartoons_collection_gr':      archives().cartoons_gr()
        elif action == 'cartoons_various':            gm().cartoons()
        elif action == 'youtube_cartoons_classics':   youtube().cartoons_classics()
        elif action == 'youtube_cartoons_songs':      youtube().cartoons_songs()
        elif action == 'mega_news':                   mega().news()
        elif action == 'ant1_news':                   ant1().news()
        elif action == 'alpha_news':                  alpha().news()
        elif action == 'star_news':                   star().news()
        elif action == 'skai_news':                   skai().news()
        elif action == 'sigma_news':                  sigma().news()
        elif action == 'youtube_enikos':              youtube().enikos()
        elif action == 'mega_sports':                 mega().sports()
        elif action == 'ant1_sports':                 ant1().sports()
        elif action == 'novasports_shows':            novasports().shows()
        elif action == 'novasports_news':             novasports().news()
        elif action == 'novasports_superleague':      novasports().superleague()
        elif action == 'dailymotion_superball':       dailymotion().superball()
        elif action == 'youtube_madgreekz':           youtube().madgreekz()
        elif action == 'mtvhitlisthellas':            mtvchart().mtvhitlisthellas()
        elif action == 'rythmoshitlist':              rythmoschart().rythmoshitlist()
        elif action == 'mtvdancefloor':               mtvchart().mtvdancefloor()
        elif action == 'eurotop20':                   mtvchart().eurotop20()
        elif action == 'usatop20':                    mtvchart().usatop20()
        elif action == 'episodes_stacked':            episodes().stacked(name, url, image, genre, plot, show)
        elif action == 'episodes_reverse':            episodes().get(name, url, image, genre, plot, show, reverse=True)
        elif action == 'episodes':                    episodes().get(name, url, image, genre, plot, show)
        elif action == 'play_live':                   resolver().live(channel)
        elif action == 'play_radio':                  resolver().radio(url)
        elif action == 'play':                        resolver().run(url)

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
            headers['Accept-Language'] = 'el-GR'
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
        xbmc.Player.__init__(self)

    def run(self, url):
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

    def live(self, name, title, epg, image, url):
        name = re.sub('\s[(]\d{1}[)]$','', name)

        date = datetime.datetime.now().strftime("%Y-%m-%d")

        if image == '0': 
            image = '%s/%s.png' % (addonLogos, re.sub('\s[(]\d{1}[)]$','', name))
            if not xbmcvfs.exists(image): image = '%s/na.png' % addonLogos

        if title == '0': title = name
        if not xbmc.getInfoLabel('listItem.plot') == '' : epg = xbmc.getInfoLabel('listItem.plot')

        meta = {'title': title, 'tvshowtitle': name, 'studio': name, 'premiered': date, 'director': name, 'writer': name, 'plot': epg, 'genre': 'TV'}

        item = xbmcgui.ListItem(path=url, iconImage=image, thumbnailImage=image)
        item.setInfo( type="Video", infoLabels = meta )

        xbmc.PlayList(xbmc.PLAYLIST_VIDEO).clear()
        xbmc.Player().play(url, item)

    def radio(self, name, url, image):
        if image == '0': image = '%s/na_radio.png' % addonLogos

        meta = {'title': name, 'album': name, 'artist': name, 'genre': 'Greek', 'duration': '1440', 'comment': name}

        item = xbmcgui.ListItem(path=url, iconImage=image, thumbnailImage=image)
        item.setInfo( type="Video", infoLabels = { "title": "" } )
        item.setInfo( type="Music", infoLabels = meta )

        xbmc.PlayList(xbmc.PLAYLIST_VIDEO).clear()
        xbmc.PlayList(xbmc.PLAYLIST_MUSIC).clear()
        xbmc.Player().play(url, item)

    def onPlayBackStarted(self):
        return

    def onPlayBackEnded(self):
        return

    def onPlayBackStopped(self):
        return

class index:
    def infoDialog(self, str, header=addonName, time=3000):
        try: xbmcgui.Dialog().notification(header, str, addonIcon, time, sound=False)
        except: xbmc.executebuiltin("Notification(%s,%s, %s, %s)" % (header, str, time, addonIcon))

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
            dbcon = database.connect(addonCache)
            dbcur = dbcon.cursor()
            dbcur.execute("DROP TABLE IF EXISTS rel_list")
            dbcur.execute("VACUUM")
            dbcon.commit()

            index().infoDialog(language(30305).encode("utf-8"))
        except:
            pass

    def rootList(self, rootList):
        if rootList == None or len(rootList) == 0: return

        total = len(rootList)
        for i in rootList:
            try:
                try: name = language(i['name']).encode("utf-8")
                except: name = i['name']

                image = '%s/%s' % (addonArt, i['image'])

                root = i['action']
                u = '%s?action=%s' % (sys.argv[0], root)
                try: u += '&url=%s' % urllib.quote_plus(i['url'])
                except: pass
                if u == '': raise Exception()

                cm = []
                if root.startswith('movies') or root.startswith('episodes') or root.startswith('cartoons'):
                    cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                    cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=item_random_play)' % (sys.argv[0])))
                    cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo(type="Video", infoLabels={"title": name, "plot": addonDesc})
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

    def channelList(self, channelList):
        if channelList == None or len(channelList) == 0: return

        date = datetime.datetime.now().strftime("%Y-%m-%d")

        try:
            favourites = []
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='Live TV'")
            favourites = dbcur.fetchall()
            favourites = [i[0].encode("utf-8") for i in favourites]
        except:
            pass

        total = len(channelList)
        for i in channelList:
            try:
                name, title, epg, image, type = i['name'], i['title'], i['epg'], i['image'], i['type']

                label = '[B]%s[/B]' % name
                if not title == '0': 
                    label += ' : %s' % title

                if image == '0': 
                    image = '%s/%s.png' % (addonLogos, re.sub('\s[(]\d{1}[)]$','', name))
                    if not xbmcvfs.exists(image): image = '%s/na.png' % addonLogos

                fanart = addonFanart

                meta = {'title': name, 'tvshowtitle': name, 'studio': name, 'premiered': date, 'director': name, 'writer': name, 'plot': epg, 'genre': 'Live TV', 'duration': '1440'}
                meta = {'title': name, 'tvshowtitle': name, 'studio': name, 'premiered': date, 'director': name, 'writer': name, 'plot': epg, 'genre': 'TV'}

                sysname, sysurl = urllib.quote_plus(name), urllib.quote_plus(name.replace(' ','_'))

                u = '%s?action=play_live&channel=%s' % (sys.argv[0], sysurl)

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=livetv_refresh)' % (sys.argv[0])))
                cm.append((language(30413).encode("utf-8"), 'RunPlugin(%s?action=view_livetv)' % (sys.argv[0])))
                if not name in favourites: cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=favourite_livetv_add&channel=%s)' % (sys.argv[0], sysname)))
                else: cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysname)))

                item = xbmcgui.ListItem(label, iconImage=image, thumbnailImage=image)
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(episodes)'):
                return index().container_view('livetv', {'skin.confluence' : 504})
            xbmc.sleep(100)

    def radioList(self, radioList):
        if radioList == None or len(radioList) == 0: return
     
        if action.startswith('radios_alt'): type = 'audio'
        else: type = 'video'

        try:
            favourites = []
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='Radio'")
            favourites = dbcur.fetchall()
            favourites = [i[0].encode("utf-8") for i in favourites]
        except:
            pass

        total = len(radioList)
        for i in radioList:
            try:
                name, url, image = i['name'], i['url'], i['image']
                if image == '0': image = '%s/na_radio.png' % addonLogos

                meta = {'title': name, 'album': name, 'artist': name, 'genre': 'Greek', 'duration': '1440', 'comment': name}

                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)

                u = '%s?action=play_radio&url=%s' % (sys.argv[0], sysurl)

                cm = []
                if type == 'video': cm.append((language(30414).encode("utf-8"), 'RunPlugin(%s?action=view_radios)' % (sys.argv[0])))
                if not url in favourites: cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=favourite_radio_add&name=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysurl, sysimage)))
                else: cm.append((language(30412).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))

                item = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
                item.setProperty("Fanart_Image", addonFanart)
                item.setInfo(type="Music", infoLabels = meta)
                item.setProperty("Video", "true")
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

        xbmcplugin.setContent(int(sys.argv[1]), 'albums')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

        if type == 'audio': return

        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(albums)'):
                return index().container_view('radios', {'skin.confluence' : 500})
            xbmc.sleep(100)

    def movieList(self, movieList):
        if movieList == None or len(movieList) == 0: return

        try:
            favourites = []
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='Movie'")
            favourites = dbcur.fetchall()
            favourites = [i[0].encode("utf-8") for i in favourites]
        except:
            pass

        total = len(movieList)
        for i in movieList:
            try:
                name, url, image, title, year, genre, plot = i['name'], i['url'], i['image'], i['title'], i['year'], i['genre'], i['plot']

                try: fanart = i['fanart']
                except: fanart = '0'

                meta = {'title': title, 'year': year, 'genre' : genre, 'plot': plot}

                sysname, sysurl, sysimage, systitle, sysyear, sysgenre, sysplot = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(genre), urllib.quote_plus(plot)

                if fanart == '0': fanart = addonFanart
                if image == '0': image = movieImage
                if plot == '0': meta.update({'plot': addonDesc})
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')

                u = '%s?action=play&url=%s&name=%s' % (sys.argv[0], sysurl, sysname)

                cm = []
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                if action == 'movies_favourites':
                    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                elif action == 'movies_search':
                    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=favourite_movie_from_search&name=%s&url=%s&image=%s&title=%s&year=%s&genre=%s&plot=%s)' % (sys.argv[0], sysname, sysurl, sysimage, systitle, sysyear, sysgenre, sysplot)))
                else:
                    if not url in favourites: cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=favourite_movie_add&name=%s&url=%s&image=%s&title=%s&year=%s&genre=%s&plot=%s)' % (sys.argv[0], sysname, sysurl, sysimage, systitle, sysyear, sysgenre, sysplot)))
                    else: cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                if not action == 'movies':
                    cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.setProperty("IsPlayable", "true")
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(movies)'):
                return index().container_view('movies', {'skin.confluence' : 50})
            xbmc.sleep(100)

    def cartoonList(self, cartoonList):
        if cartoonList == None or len(cartoonList) == 0: return

        try:
            favourites = []
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='Cartoons'")
            favourites = dbcur.fetchall()
            favourites = [i[0].encode("utf-8") for i in favourites]
        except:
            pass

        total = len(cartoonList)
        for i in cartoonList:
            try:
                name, url, image, title, year, genre, plot = i['name'], i['url'], i['image'], i['title'], i['year'], i['genre'], i['plot']

                try: fanart = i['fanart']
                except: fanart = '0'

                meta = {'title': title, 'year': year, 'genre' : genre, 'plot': plot}

                sysname, sysurl, sysimage, systitle, sysyear, sysgenre, sysplot = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(genre), urllib.quote_plus(plot)

                if fanart == '0': fanart = addonFanart
                if image == '0': image = movieImage
                if plot == '0': meta.update({'plot': addonDesc})
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')

                if i['type'] == 'movie':
                    u = '%s?action=play&url=%s&name=%s' % (sys.argv[0], sysurl, sysname)
                    isFolder = False
                else:
                    u = '%s?action=episodes&name=%s&url=%s&image=%s&genre=%s&plot=%s&show=%s' % (sys.argv[0], sysname, sysurl, sysimage, sysgenre, sysplot, sysname)
                    isFolder = True

                cm = []
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))

                if action == 'cartoons_favourites':
                    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                else:
                    if not url in favourites: cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=favourite_cartoons_add&name=%s&url=%s&image=%s&title=%s&year=%s&genre=%s&plot=%s)' % (sys.argv[0], sysname, sysurl, sysimage, systitle, sysyear, sysgenre, sysplot)))
                    else: cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                if not action == 'movies':
                    cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=view_cartoons)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.setProperty("IsPlayable", "true")
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=isFolder)
            except:
                pass

        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(movies)'):
                return index().container_view('cartoons', {'skin.confluence' : 500})
            xbmc.sleep(100)

    def showList(self, showList):
        if showList == None or len(showList) == 0: return

        try:
            favourites = []
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='TV Show'")
            favourites = dbcur.fetchall()
            favourites = [i[0].encode("utf-8") for i in favourites]
        except:
            pass

        total = len(showList)
        for i in showList:
            try:
                name, url, image, genre, plot = i['name'], i['url'], i['image'], i['genre'], i['plot']

                try: fanart = i['fanart']
                except: fanart = '0'

                meta = {'title': name, 'tvshowtitle': name, 'genre' : genre, 'plot': plot}

                sysname, sysurl, sysimage, sysgenre, sysplot, sysshow = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(genre), urllib.quote_plus(plot), urllib.quote_plus(name)

                if fanart == '0': fanart = addonFanart
                if image == '0': image = tvImage
                if plot == '0': meta.update({'plot': addonDesc})
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')

                if action == 'shows' or action == 'shows_favourites':
                    u = '%s?action=episodes_reverse&name=%s&url=%s&image=%s&genre=%s&plot=%s&show=%s' % (sys.argv[0], sysname, sysurl, sysimage, sysgenre, sysplot, sysshow)
                else:
                    u = '%s?action=episodes&name=%s&url=%s&image=%s&genre=%s&plot=%s&show=%s' % (sys.argv[0], sysname, sysurl, sysimage, sysgenre, sysplot, sysshow)

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=item_random_play)' % (sys.argv[0])))
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                if action == 'shows_favourites':
                    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                elif action == 'shows_search':
                    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=favourite_tv_from_search&name=%s&url=%s&image=%s&genre=%s&plot=%s)' % (sys.argv[0], sysname, sysurl, sysimage, sysgenre, sysplot)))
                elif action == 'shows':
                    if not url in favourites: cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=favourite_tv_add&name=%s&url=%s&image=%s&genre=%s&plot=%s)' % (sys.argv[0], sysname, sysurl, sysimage, sysgenre, sysplot)))
                    else: cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))

                cm.append((language(30416).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(tvshows)'):
                return index().container_view('tvshows', {'skin.confluence' : 50})
            xbmc.sleep(100)

    def episodeList(self, episodeList):
        if episodeList == None or len(episodeList) == 0: return

        total = len(episodeList)
        for i in episodeList:
            try:
                name, url, image, date, genre, plot, title, show = i['name'], i['url'], i['image'], i['date'], i['genre'], i['plot'], i['title'], i['show']

                try: fanart = i['fanart']
                except: fanart = '0'

                meta = {'title': title, 'studio': show, 'premiered': date, 'genre': genre, 'plot': plot}

                sysname, sysurl, sysimage, sysgenre, sysplot, sysshow = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(genre), urllib.quote_plus(plot), urllib.quote_plus(show)

                if fanart == '0': fanart = addonFanart
                if image == '0': image = episodeImage
                if show == '0': meta.update({'studio': addonName})
                if plot == '0': meta.update({'plot': addonDesc})
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')

                try: stacked = i['stacked']
                except: stacked = '0'
                if stacked == '0':
                    u = '%s?action=play&url=%s' % (sys.argv[0], sysurl)
                    isFolder = False
                else:
                    u = '%s?action=episodes_stacked&name=%s&url=%s&image=%s&genre=%s&plot=%s&show=%s' % (sys.argv[0], sysname, sysurl, sysimage, sysgenre, sysplot, sysshow)
                    isFolder = True

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=view_episodes)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.setProperty("IsPlayable", "true")
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=isFolder)
            except:
                pass

        try:
            next = episodeList[0]['next']
            if next == '': raise Exception()
            name, url, image = language(30362).encode("utf-8"), next, '%s/item_next.jpg' % addonArt
            u = '%s?action=episodes&name=0&url=%s&image=0&genre=0&plot=0&show=0' % (sys.argv[0], urllib.quote_plus(url))
            item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
            item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
            item.setProperty("Fanart_Image", addonFanart)
            item.addContextMenuItems([], replaceItems=False)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)
        except:
            pass

        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(episodes)'):
                return index().container_view('episodes', {'skin.confluence' : 50})
            xbmc.sleep(100)

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

    def favourite_add(self, type, url, name, title, year, image, genre, plot, refresh=False):
        try:
            record = (url, type, repr(name), repr(title), repr(year), repr(image), repr(genre), repr(plot))

            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS favourites (""url TEXT, ""video_type TEXT, ""name TEXT, ""title TEXT, ""year TEXT, ""image TEXT, ""genre TEXT, ""plot TEXT, ""UNIQUE(url)"");")
            dbcur.execute("DELETE FROM favourites WHERE url = '%s'" % (record[0]))
            dbcur.execute("INSERT INTO favourites Values (?, ?, ?, ?, ?, ?, ?, ?)", record)
            dbcon.commit()

            if refresh == True: index().container_refresh()
            index().infoDialog(language(30303).encode("utf-8"), name)
        except:
            return

    def favourite_delete(self, name, url):
        try:
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("DELETE FROM favourites WHERE url = '%s'" % url)
            dbcon.commit()

            index().container_refresh()
            index().infoDialog(language(30304).encode("utf-8"), name)
        except:
            return

    def livetv_refresh(self):
        try:
            dbcon = database.connect(addonCache)
            dbcur = dbcon.cursor()
            dbcur.execute("DELETE FROM rel_list WHERE func = 'channels.channel_list'")
            dbcon.commit()
            xbmc.executebuiltin('Container.Refresh')
        except:
            return


class root:
    def get(self):
        rootList = []
        rootList.append({'name': 30501, 'image': 'root_livetv.jpg', 'action': 'root_livetv'})
        rootList.append({'name': 30502, 'image': 'root_radios.jpg', 'action': 'root_radios'})
        rootList.append({'name': 30503, 'image': 'root_networks.jpg', 'action': 'root_networks'})
        rootList.append({'name': 30504, 'image': 'root_shows.jpg', 'action': 'root_shows'})
        rootList.append({'name': 30505, 'image': 'root_movies.jpg', 'action': 'root_movies'})
        rootList.append({'name': 30506, 'image': 'root_cartoons.jpg', 'action': 'root_cartoons'})
        rootList.append({'name': 30507, 'image': 'root_docs.jpg', 'action': 'shows_skai_docs'})
        rootList.append({'name': 30508, 'image': 'root_favourites.jpg', 'action': 'root_favourites'})
        rootList.append({'name': 30509, 'image': 'root_news.jpg', 'action': 'root_news'})
        rootList.append({'name': 30510, 'image': 'root_sports.jpg', 'action': 'root_sports'})
        rootList.append({'name': 30511, 'image': 'root_music.jpg', 'action': 'root_music'})
        index().rootList(rootList)

    def radios(self):
        import random
        img = ['radios_random1.jpg', 'radios_random2.jpg', 'radios_random3.jpg', 'radios_random4.jpg', 'radios_random5.jpg', 'radios_random6.jpg', 'radios_random7.jpg', 'radios_random8.jpg']

        rootList = []
        rootList.append({'name': 30521, 'image': 'radios_all.jpg', 'action': 'radios_all'})
        rootList.append({'name': 30522, 'image': 'radios_favourites.jpg', 'action': 'radios_favourites'})
        rootList.append({'name': 30523, 'image': 'radios_trending.jpg', 'action': 'radios_trending'})
        rootList.append({'name': 30524, 'image': 'radios_top20.jpg', 'action': 'radios_top20'})
        rootList.append({'name': 30525, 'image': 'radios_new.jpg', 'action': 'radios_new'})
        try:
            genres = eradio().genres()
            for i in range(0, len(genres)): genres[i].update({'image': random.choice(img), 'action': 'radios'})
            rootList += genres
        except:
            pass
        try:
            regions = eradio().regions()
            for i in range(0, len(regions)): regions[i].update({'image': random.choice(img), 'action': 'radios'})
            rootList += regions
        except:
            pass
        index().rootList(rootList)

    def radios_alt(self):
        import random
        img = ['radios_random1.jpg', 'radios_random2.jpg', 'radios_random3.jpg', 'radios_random4.jpg', 'radios_random5.jpg', 'radios_random6.jpg', 'radios_random7.jpg', 'radios_random8.jpg']

        rootList = []
        rootList.append({'name': 30521, 'image': 'radios_all.jpg', 'action': 'radios_alt_all'})
        rootList.append({'name': 30522, 'image': 'radios_favourites.jpg', 'action': 'radios_alt_favourites'})
        rootList.append({'name': 30523, 'image': 'radios_trending.jpg', 'action': 'radios_alt_trending'})
        rootList.append({'name': 30524, 'image': 'radios_top20.jpg', 'action': 'radios_alt_top20'})
        rootList.append({'name': 30525, 'image': 'radios_new.jpg', 'action': 'radios_alt_new'})
        try:
            genres = eradio().genres()
            for i in range(0, len(genres)): genres[i].update({'image': random.choice(img), 'action': 'radios_alt'})
            rootList += genres
        except:
            pass
        try:
            regions = eradio().regions()
            for i in range(0, len(regions)): regions[i].update({'image': random.choice(img), 'action': 'radios_alt'})
            rootList += regions
        except:
            pass
        index().rootList(rootList)

    def networks(self):
        rootList = []

        root = 'shows_mega'
        if getSetting("shows_mega") == '1': root = 'shows_alt_mega'
        rootList.append({'name': 'MEGA', 'image': 'logos_mega.jpg', 'action': root})

        root = 'shows_ant1'
        if getSetting("shows_ant1") == '1': root = 'shows_alt_ant1'
        rootList.append({'name': 'ANT1', 'image': 'logos_ant1.jpg', 'action': root})

        root = 'shows_alpha'
        if getSetting("shows_alpha") == '1': root = 'shows_alt_alpha'
        rootList.append({'name': 'ALPHA', 'image': 'logos_alpha.jpg', 'action': root})

        root = 'shows_star'
        if getSetting("shows_star") == '1': root = 'shows_alt_star'
        rootList.append({'name': 'STAR', 'image': 'logos_star.jpg', 'action': root})

        root = 'shows_skai'
        if getSetting("shows_skai") == '1': root = 'shows_alt_skai'
        rootList.append({'name': 'SKAI', 'image': 'logos_skai.jpg', 'action': root})

        rootList.append({'name': 'E TV', 'image': 'logos_etv.jpg', 'action': 'shows_etv'})
        #rootList.append({'name': 'NERIT', 'image': 'logos_nerit.jpg', 'action': 'shows_nerit'})
        rootList.append({'name': 'SIGMA', 'image': 'logos_sigma.jpg', 'action': 'shows_sigma'})
        rootList.append({'name': 'ANT1 CY', 'image': 'logos_ant1cy.jpg', 'action': 'shows_ant1cy'})
        rootList.append({'name': 'KONTRA', 'image': 'logos_kontra.jpg', 'action': 'shows_kontra'})
        rootList.append({'name': 'BLUE SKY', 'image': 'logos_bluesky.jpg', 'action': 'shows_bluesky'})
        rootList.append({'name': 'ACTION 24', 'image': 'logos_action24.jpg', 'action': 'shows_action24'})
        rootList.append({'name': 'ART TV', 'image': 'logos_art.jpg', 'action': 'shows_art'})
        rootList.append({'name': 'MTV', 'image': 'logos_mtv.jpg', 'action': 'shows_mtv'})
        rootList.append({'name': 'MAD TV', 'image': 'logos_madtv.jpg', 'action': 'shows_madtv'})
        rootList.append({'name': 'Hellenic TV1', 'image': 'logos_hellenictv1.jpg', 'action': 'shows_hellenictv1'})
        rootList.append({'name': 'REAL FM', 'image': 'logos_real_fm.jpg', 'action': 'shows_real_fm'})
        rootList.append({'name': 'SKAI 100,3', 'image': 'logos_skai_fm.jpg', 'action': 'shows_skai_fm'})
        rootList.append({'name': 30531, 'image': 'shows_networks.jpg', 'action': 'shows_networks'})
        index().rootList(rootList)

    def shows(self):
        rootList = []
        rootList.append({'name': 30541, 'image': 'shows_search.jpg', 'action': 'shows_search'})
        rootList.append({'name': 30542, 'image': 'shows_favourites.jpg', 'action': 'shows_favourites'})
        try:
            titles = gm().showtitles()
            for i in range(0, len(titles)): titles[i].update({'image': 'titles_shows.jpg', 'action': 'shows'})
            rootList += titles
        except:
            pass
        index().rootList(rootList)

    def movies(self):
        rootList = []
        rootList.append({'name': 30551, 'image': 'movies_search.jpg', 'action': 'movies_search'})
        rootList.append({'name': 30552, 'image': 'movies_favourites.jpg', 'action': 'movies_favourites'})
        try:
            years = gm().movieyears()
            for i in range(0, len(years)): years[i].update({'image': 'years_movies.jpg', 'action': 'movies'})
            rootList += years
        except:
            pass
        index().rootList(rootList)

    def cartoons(self):
        rootList = []
        rootList.append({'name': 30561, 'image': 'cartoons_favourites.jpg', 'action': 'cartoons_favourites'})
        rootList.append({'name': 30562, 'image': 'cartoons_collection.jpg', 'action': 'cartoons_collection'})
        rootList.append({'name': 30563, 'image': 'cartoons_collection_gr.jpg', 'action': 'cartoons_collection_gr'})
        rootList.append({'name': 30564, 'image': 'cartoons_various.jpg', 'action': 'cartoons_various'})
        rootList.append({'name': 30565, 'image': 'cartoons_classics.jpg', 'action': 'youtube_cartoons_classics'})
        rootList.append({'name': 30566, 'image': 'cartoons_songs.jpg', 'action': 'youtube_cartoons_songs'})
        index().rootList(rootList)

    def favourites(self):
        rootList = []
        rootList.append({'name': 30571, 'image': 'livetv_favourites.jpg', 'action': 'livetv_favourites'})
        rootList.append({'name': 30572, 'image': 'radios_favourites.jpg', 'action': 'radios_favourites'})
        rootList.append({'name': 30573, 'image': 'shows_favourites.jpg', 'action': 'shows_favourites'})
        rootList.append({'name': 30574, 'image': 'movies_favourites.jpg', 'action': 'movies_favourites'})
        rootList.append({'name': 30575, 'image': 'cartoons_favourites.jpg', 'action': 'cartoons_favourites'})
        index().rootList(rootList)

    def news(self):
        rootList = []
        rootList.append({'name': 'MEGA', 'image': 'logos_mega.jpg', 'action': 'mega_news'})
        rootList.append({'name': 'ANT1', 'image': 'logos_ant1.jpg', 'action': 'ant1_news'})
        rootList.append({'name': 'ALPHA', 'image': 'logos_alpha.jpg', 'action': 'alpha_news'})
        rootList.append({'name': 'STAR', 'image': 'logos_star.jpg', 'action': 'star_news'})
        rootList.append({'name': 'SKAI', 'image': 'logos_skai.jpg', 'action': 'skai_news'})
        rootList.append({'name': 'SIGMA', 'image': 'logos_sigma.jpg', 'action': 'sigma_news'})
        rootList.append({'name': 'ENIKOS', 'image': 'logos_enikos.jpg', 'action': 'youtube_enikos'})
        index().rootList(rootList)

    def sports(self):
        rootList = []
        rootList.append({'name': 'MEGA', 'image': 'logos_mega.jpg', 'action': 'mega_sports'})
        rootList.append({'name': 'ANT1', 'image': 'logos_ant1.jpg', 'action': 'ant1_sports'})
        rootList.append({'name': 'Novasports', 'image': 'logos_novasports.jpg', 'action': 'novasports_shows'})
        rootList.append({'name': 'Novasports News', 'image': 'logos_novasports_news.jpg', 'action': 'novasports_news'})
        rootList.append({'name': 'Super League', 'image': 'logos_superleague.jpg', 'action': 'novasports_superleague'})
        rootList.append({'name': 'SuperBALL', 'image': 'logos_superball.jpg', 'action': 'dailymotion_superball'})
        index().rootList(rootList)

    def music(self):
        rootList = []
        rootList.append({'name': 'MAD Greekz', 'image': 'logos_madgreekz.jpg', 'action': 'youtube_madgreekz'})
        rootList.append({'name': 'MTV Hit List Hellas', 'image': 'logos_mtvhits.jpg', 'action': 'mtvhitlisthellas'})
        rootList.append({'name': 'Rythmos Hit List', 'image': 'logos_rythmos.jpg', 'action': 'rythmoshitlist'})
        rootList.append({'name': 'MTV Dance Floor', 'image': 'logos_mtvdance.jpg', 'action': 'mtvdancefloor'})
        rootList.append({'name': 'Euro Top 20', 'image': 'logos_europe.jpg', 'action': 'eurotop20'})
        rootList.append({'name': 'U.S. Top 20', 'image': 'logos_usa.jpg', 'action': 'usatop20'})
        index().rootList(rootList)


class favourites:
    def __init__(self):
        self.list = []

    def livetv(self):
        try:
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='Live TV'")
            match = dbcur.fetchall()
            match = [(i[0]) for i in match]

            self.list = channels().get(idx=False)
            self.list = [i for i in self.list if i['name'] in match]
            self.list = sorted(self.list, key=itemgetter('name'))

            index().channelList(self.list)
        except:
            return

    def radios(self):
        try:
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='Radio'")
            match = dbcur.fetchall()
            match = [(i[0], i[2], i[5]) for i in match]

            for url, name, image in match:
                try:
                    name, image = eval(name.encode('utf-8')), eval(image.encode('utf-8'))

                    self.list.append({'name': name, 'url': url, 'image': image})
                except:
                    pass

            self.list = sorted(self.list, key=itemgetter('name'))
            index().radioList(self.list)
        except:
            return

    def shows(self):
        try:
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='TV Show'")
            match = dbcur.fetchall()
            match = [(i[0], i[2], i[5], i[6], i[7]) for i in match]

            for url, name, image, genre, plot in match:
                try:
                    name, image, genre, plot = eval(name.encode('utf-8')), eval(image.encode('utf-8')), eval(genre.encode('utf-8')), eval(plot.encode('utf-8'))

                    self.list.append({'name': name, 'url': url, 'image': image, 'genre': genre, 'plot': plot})
                except:
                    pass

            self.list = sorted(self.list, key=itemgetter('name'))
            index().showList(self.list)
        except:
            return

    def movies(self):
        try:
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='Movie'")
            match = dbcur.fetchall()
            match = [(i[0], i[2], i[3], i[4], i[5], i[6], i[7]) for i in match]

            for url, name, title, year, image, genre, plot in match:
                try:
                    name, title, year, image, genre, plot = eval(name.encode('utf-8')), eval(title.encode('utf-8')), eval(year.encode('utf-8')), eval(image.encode('utf-8')), eval(genre.encode('utf-8')), eval(plot.encode('utf-8'))

                    self.list.append({'name': name, 'url': url, 'image': image, 'title': title, 'year': year, 'genre': genre, 'plot': plot})
                except:
                    pass

            self.list = sorted(self.list, key=itemgetter('title'))
            index().movieList(self.list)
        except:
            return

    def cartoons(self):
        try:
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='Cartoons'")
            match = dbcur.fetchall()
            match = [(i[0], i[2], i[3], i[4], i[5], i[6], i[7]) for i in match]

            a = [i[0] for i in match if i[0].startswith('archives_')]
            a = [re.compile('archives_.+?_(\d*)_\d*').findall(i)[0] for i in a]

            self.list = index().cache(archives().item_list, 0.02, 'cartoons_collection')
            self.list = [i for i in self.list if i['imdb'] in a]

            b = [i for i in match if not i[0].startswith('archives_')]
            for url, name, title, year, image, genre, plot in b:
                try:
                    name, title, year, image, genre, plot = eval(name.encode('utf-8')), eval(title.encode('utf-8')), eval(year.encode('utf-8')), eval(image.encode('utf-8')), eval(genre.encode('utf-8')), eval(plot.encode('utf-8'))

                    if 'gdata.youtube.com' in url: 
                        url = youtube().playlist_link % url.split('/playlists/')[-1]

                    if 'youtube' in url: type = 'tvshow'
                    else: type = 'movie'

                    self.list.append({'name': name, 'url': url, 'image': image, 'fanart': '0', 'title': title, 'year': year, 'genre': genre, 'plot': plot, 'lang': 'el', 'type': type})
                except:
                    pass

            self.list = sorted(self.list, key=itemgetter('title'))
            index().cartoonList(self.list)
        except:
            return

class channels:
    def __init__(self):
        self.list = []

        self.channelMap = {'MEGA':'10', 'ANT1':'7', 'ALPHA':'5', 'STAR':'12', 'SKAI':'11', 'MACEDONIA TV':'8', 'NERIT':'4', 'NERIT PLUS':'352', 'RIK SAT':'83', 'BLUE SKY':'200', 'E TV':'326', 'EXTRA CHANNEL':'191', 'CHANNEL 9':'199', 'KONTRA CHANNEL':'194', 'ART CHANNEL':'248', 'AB CHANNEL':'249', 'TV 100':'229', 'DELTA TV':'236', 'DIKTYO TV':'235', 'STAR CENTRAL GR':'230', 'ALFA TV':'372', 'ATTICA TV':'190', 'BEST TV':'332', 'IONIAN CHANNEL':'360', 'SUPER B':'368', 'COSMOS TV':'370', 'KANALI 6':'377', 'R CHANNEL':'380', 'THRAKI NET':'382', 'ASTRA TV':'400', 'ACTION24':'189', 'BOYLH TV':'1', 'SBC':'228', 'NICKELODEON':'193', 'MAD TV':'9', 'MTV GREECE':'138', '4E':'222', 'TV AIGAIO':'330', 'CORFU TV':'331', 'KRITI TV':'227', 'EPIRUS TV1':'234', 'KOSMOS':'334', 'EURONEWS':'119', 'MEGA CYPRUS':'306', 'ANT1 CYPRUS':'258', 'SIGMA':'305', 'PLUS TV':'289', 'EXTRA TV':'290', 'CAPITAL':'282', 'RIK 1':'274', 'RIK 2':'277'}

        self.entertainmentMap = ['ET3', 'CAPITAL']
        self.movieMap = ['GREEK CINEMA 50s', 'GREEK CINEMA 60s', 'GREEK CINEMA 70s', 'GREEK CINEMA 80s', 'GREEK CINEMA']
        self.childrenMap = ['NICKELODEON', 'NICKELODEON+', 'SMILE', 'WZRA KIDS']
        self.sportMap = ['CY SPORTS', 'ODIE TV']
        self.musicMap = ['MAD TV', 'MAD TV CYPRUS']
        self.newsMap = ['SBC']

        self.dt_link = 'http://www.tvcontrol.gr/app_api/functions.php?method=DateTime_Get'
        self.packet_1_link = 'http://www.tvcontrol.gr/json/now-next/packet_1.json'
        self.packet_2_link = 'http://www.tvcontrol.gr/json/now-next/packet_2.json'
        self.packet_9_link = 'http://www.tvcontrol.gr/json/now-next/packet_9.json'

    def get(self, idx=True):
        self.list = index().cache(self.channel_list, 0.02)
        if idx == True: index().channelList(self.list)
        return self.list

    def channel_list(self):
        try:
            result = getUrl(addonChannels).result
            channels = common.parseDOM(result, "channel", attrs = { "active": "True" })
        except:
            return

        try:
            result = getUrl(self.dt_link).result
            result = json.loads(result)
            dt = int(result['DateTimeInt'])

            self.programmes = []

            def programmes_thread(url):
                self.programmes += json.loads(getUrl(url).result)

            threads = []
            url = [self.packet_1_link, self.packet_2_link, self.packet_9_link]
            for u in url: threads.append(Thread(programmes_thread, u))
            [i.start() for i in threads]
            [i.join() for i in threads]

            programmes = self.programmes
            programmes = [i for x, i in enumerate(programmes) if i not in programmes[x + 1:]]
            programmes = [i for i in programmes if int(i['stop_date_local']) > dt]
        except:
            pass

        for channel in channels:
            try:
                name = common.parseDOM(channel, "name")[0]

                try: type = common.parseDOM(channel, "type")[0]
                except: type = ''

                url = common.parseDOM(channel, "url")[0]
                url = common.replaceHTMLCodes(url)

                try:
                    if name in self.entertainmentMap: title = 'Ψυχαγωγικό πρόγραμμα'.decode('iso-8859-7')
                    elif name in self.childrenMap: title = 'Παιδικό πρόγραμμα'.decode('iso-8859-7')
                    elif name in self.sportMap: title = 'Αθλητικό πρόγραμμα'.decode('iso-8859-7')
                    elif name in self.musicMap: title = 'Μουσικό πρόγραμμα'.decode('iso-8859-7')
                    elif name in self.newsMap: title = 'Ενημερωτικό πρόγραμμα'.decode('iso-8859-7')
                    elif name in self.movieMap: title = 'Ταινία'.decode('iso-8859-7')
                    else: title = '0'

                    epg = '[B]ΤΩΡΑ[/B]\nΔεν υπάρχουν πληροφορίες\n\n[B]ΕΠΟΜΕΝΟ[/B]\nΔεν υπάρχουν πληροφορίες'.decode('iso-8859-7')

                    image = '0'

                    n = re.sub('\s[(]\d{1}[)]$','', name)
                    p = [i for i in programmes if i['channel_id'] == self.channelMap[n]]
                    p = sorted(p, key=itemgetter('start_date_local'))[:2]

                    title = p[0]['constructed_titlegr']

                    image = p[0]['imgsrc']
                    if image == '': image = '0'

                    start, stop = p[0]['start_date_local'], p[0]['stop_date_local']
                    start, stop = self.dt_processor(start), self.dt_processor(stop)
                    start = '%s:%s' % (start[8:][:4][:2], start[8:][:4][2:])
                    stop = '%s:%s' % (stop[8:][:4][:2], stop[8:][:4][2:])

                    epg = '[B]%s[/B]\n%s'.decode('iso-8859-7') % (start, title)
                    try: epg += '\n\n[B]%s[/B]\n%s'.decode('iso-8859-7') % (stop, p[1]['constructed_titlegr'])
                    except: epg += '\n\n[B]ΕΠΟΜΕΝΟ[/B]\nΔεν υπάρχουν πληροφορίες'.decode('iso-8859-7') % stop
                    epg = common.replaceHTMLCodes(epg)
                except:
                    pass

                self.list.append({'name': name, 'title': title, 'epg': epg, 'image': image, 'url': url, 'type': type})
            except:
                pass

        return self.list

    def dt_processor(self, dt):
        dt1 = datetime.datetime.utcnow() + datetime.timedelta(hours = 2)
        d = datetime.datetime(dt1.year, 4, 1)
        dston = d - datetime.timedelta(days=d.weekday() + 1)
        d = datetime.datetime(dt1.year, 11, 1)
        dstoff = d - datetime.timedelta(days=d.weekday() + 1)
        if dston <=  dt1 < dstoff: dt1 = dt1 + datetime.timedelta(hours = 1)
        dt1 = datetime.datetime(dt1.year, dt1.month, dt1.day, dt1.hour)

        dt2 = datetime.datetime.now()
        dt2 = datetime.datetime(dt2.year, dt2.month, dt2.day, dt2.hour)

        dt3 = datetime.datetime.utcnow()
        dt3 = datetime.datetime(dt3.year, dt3.month, dt3.day, dt3.hour)
        dt = datetime.datetime(*time.strptime(dt, "%Y%m%d%H%M%S")[:6])
        if dt2 >= dt1 :
            dtd = (dt2 - dt1).seconds/60/60
            dt = dt + datetime.timedelta(hours = int(dtd))
        else:
            dtd = (dt1 - dt2).seconds/60/60
            dt = dt - datetime.timedelta(hours = int(dtd))

        dt = dt.strftime("%Y%m%d%H%M%S")
        return dt

class archives:
    def __init__(self):
        self.list = []

    def cartoons(self):
        self.list = index().cache(self.item_list, 0.02, 'cartoons_collection')
        index().cartoonList(self.list)

    def cartoons_gr(self):
        self.list = index().cache(self.item_list, 0.02, 'cartoons_collection')
        try: self.list = [i for i in self.list if i['lang'] == 'el']
        except: return
        index().cartoonList(self.list)

    def item_list(self, arc):
        try:
            if arc == 'cartoons_collection': u = addonCartoons
            result = getUrl(u).result

            items = common.parseDOM(result, "item")
        except:
            return

        for item in items:
            try:
                name = common.parseDOM(item, "title")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                title = re.compile('(.+?) [(]\d{4}[)]$').findall(name)[0]
                try: title = title.encode('utf-8')
                except: pass

                year = re.compile('.+? [(](\d{4})[)]$').findall(name)[0]
                try: year = year.encode('utf-8')
                except: pass

                url = common.parseDOM(item, "imdb_id")[0]
                url = 'archives_%s_%s_0' % (arc, url)
                url = url.encode('utf-8')

                image = common.parseDOM(item, "image")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                try: fanart = common.parseDOM(item, "fanart")[0]
                except: fanart = '0'
                fanart = common.replaceHTMLCodes(fanart)
                fanart = fanart.encode('utf-8')

                try: genre = common.parseDOM(item, "genre")[0]
                except: genre = 'Greek'
                genre = common.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')

                try: plot = common.parseDOM(item, "plot")[0]
                except: plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                try: imdb = common.parseDOM(item, "imdb_id")[0]
                except: imdb = '0'
                imdb = common.replaceHTMLCodes(imdb)
                imdb = imdb.encode('utf-8')

                try: lang = common.parseDOM(item, "language")[0]
                except: lang = '0'
                lang = lang.encode('utf-8')

                try: type = common.parseDOM(item, "type")[0]
                except: type = '0'
                type = type.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'fanart': fanart, 'title': title, 'year': year, 'genre': genre, 'plot': plot, 'imdb': imdb, 'lang': lang, 'type': type})
            except:
                pass

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            arc, imdb = re.compile('archives_(.+?)_(\d*)_\d*').findall(url)[0]

            if arc == 'cartoons_collection': u = addonCartoons
            result = getUrl(u).result

            item = common.parseDOM(result, "item")
            item = [i for i in item if common.parseDOM(i, "imdb_id")[0] == imdb][0]

            show = common.parseDOM(item, "title")[0]
            show = common.replaceHTMLCodes(show)
            show = show.encode('utf-8')

            image = common.parseDOM(item, "image")[0]
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')

            try: fanart = common.parseDOM(item, "fanart")[0]
            except: fanart = '0'
            fanart = common.replaceHTMLCodes(fanart)
            fanart = fanart.encode('utf-8')

            try: genre = common.parseDOM(item, "genre")[0]
            except: genre = 'Greek'
            genre = common.replaceHTMLCodes(genre)
            genre = genre.encode('utf-8')

            try: plot = common.parseDOM(item, "plot")[0]
            except: plot = '0'
            plot = common.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')

            episodes = common.parseDOM(item, "link")
        except:
            return

        for i in range(0, len(episodes)):
            try:
                name = 'Επεισόδιο '.decode('iso-8859-7') + str(i+1)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = 'archives_%s_%s_%s' % (arc, imdb, str(i))
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'fanart': fanart, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            arc, imdb, idx = re.compile('archives_(.+?)_(\d*)_(\d*)').findall(url)[0]

            if arc == 'cartoons_collection': u = addonCartoons
            result = getUrl(u).result

            item = common.parseDOM(result, "item")
            item = [i for i in item if common.parseDOM(i, "imdb_id")[0] == imdb][0]

            link = common.parseDOM(item, "link")[int(idx)]

            url = common.parseDOM(link, "url")[0]

            try: size = common.parseDOM(link, "size")[0]
            except: size = '0'

            url = resolver().sources_resolve(url)

            try: headers = dict(urlparse.parse_qsl(url.rsplit('|', 1)[1]))
            except: headers = dict('')

            request = urllib2.Request(url.split('|')[0], headers=headers)
            response = urllib2.urlopen(request, timeout=20)
            s = str(response.headers['Content-Length'])

            if size == '0' or size == s: return url
        except:
            return

class episodes:
    def get(self, name, url, image, genre, plot, show, reverse=False):
        if url.startswith('archives_'):
            self.list = archives().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(gm().base_link):
            self.list = gm().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(mega().feed_link):
            self.list = mega().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(mega().base_link):
            self.list = mega().episodes_list2(name, url, image, genre, plot, show)
        elif url.startswith(ant1().base_link):
            self.list = ant1().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(alpha().base_link):
            self.list = alpha().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(star().base_link):
            self.list = star().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(skai().base_link):
            self.list = skai().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(sigma().base_link):
            self.list = sigma().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(realfm().base_link):
            self.list = realfm().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(novasports().base_link):
            self.list = novasports().episodes_list2(name, url, image, genre, plot, show)
        elif url.startswith(mtvchart().base_link):
            self.list = mtvchart().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(rythmoschart().base_link):
            self.list = rythmoschart().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(dailymotion().api_link):
            self.list = dailymotion().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(youtube().api_link):
            self.list = youtube().episodes_list(name, url, image, genre, plot, show)

        if reverse == True:
            try: self.list = self.list[::-1]
            except: pass
        index().episodeList(self.list)
        return self.list

    def stacked(self, name, url, image, genre, plot, show):
        # stacked mp3 files from real fm fail after 10 seconds of playback, parse them to a folder.
        if url.startswith(realfm().base_link):
            self.list = realfm().stacked_list(name, url, image, genre, plot, show)
        index().episodeList(self.list)
        return self.list

class resolver:
    def run(self, url):
        try:
            url = self.sources_resolve(url)
            if url is None: raise Exception()

            player().run(url)
            return url
        except:
            index().infoDialog(language(30306).encode("utf-8"))
            return

    def radio(self, url):
        try:
            name, url, image = eradio().resolve(url)
            if url is None: raise Exception()

            player().radio(name, url, image)
            return url
        except:
            index().infoDialog(language(30306).encode("utf-8"))
            return

    def live(self, channel):
        try:
            dialog = xbmcgui.DialogProgress()
            dialog.create(addonName.encode("utf-8"), language(30341).encode("utf-8"))
            dialog.update(0)

            ch = channel.replace('_',' ')

            data = channels().get(idx=False)

            i = [i for i in data if ch == i['name']][0]
            name, title, epg, image, url, type = i['name'], i['title'], i['epg'], i['image'], i['url'], i['type']

            try: url = getattr(livestream(), type)(url)
            except: pass
            if url is None: raise Exception()

            dialog.close()

            player().live(name, title, epg, image, url)
            return url
        except:
            index().infoDialog(language(30306).encode("utf-8"))
            return

    def sources_resolve(self, url):
        try:
            import commonresolvers

            if url.startswith('archives_'): url = archives().resolve(url)

            elif url.startswith(gm().base_link): url = gm().resolve(url)
            elif url.startswith(mega().base_link): url = mega().resolve(url)
            elif url.startswith(ant1().base_link): url = ant1().resolve(url)
            elif url.startswith(alpha().base_link): url = alpha().resolve(url)
            elif url.startswith(skai().base_link): url = skai().resolve(url)
            elif url.startswith(sigma().base_link): url = sigma().resolve(url)
            elif url.startswith(nerit().base_link): url = nerit().resolve(url)
            elif url.startswith(ant1cy().base_link): url = ant1cy().resolve(url)
            elif url.startswith(ant1cy().old_link): url = ant1cy().resolve(url)
            elif url.startswith(megacy().base_link): url = megacy().resolve(url)
            elif url.startswith(realfm().base_link): url = realfm().resolve(url)
            elif url.startswith(novasports().base_link): url = novasports().resolve(url)
            elif url.startswith(youtube().youtube_search): url = youtube().resolve_search(url)
            elif url.startswith(youtube().base_link): url = youtube().resolve(url)

            else: url = commonresolvers.get(url).result

            if type(url) == list: url = sorted(url, key=lambda k: k['quality'])[0]['url']

            return url
        except:
            return



class gm:
    def __init__(self):
        self.list = []
        self.base_link = 'http://greek-movies.com'
        self.movies_link = 'http://greek-movies.com/movies.php?'
        self.shows_link = 'http://greek-movies.com/shows.php?'
        self.series_link = 'http://greek-movies.com/series.php?'
        self.episode_link = 'http://greek-movies.com/ajax.php?type=episode&epid=%s&view=%s'

    def movieyears(self):
        try:
            self.list = index().cache(self.titles_list, 24, self.movies_link)
            self.list = [i for i in self.list if i['url'].startswith('y=')]
            return self.list
        except:
            pass

    def showtitles(self):
        try:
            self.list = index().cache(self.titles_list, 24, self.shows_link)
            self.list = [i for i in self.list if i['url'].startswith('l=')]
            return self.list
        except:
            pass

    def search(self, query=None):
        if query == None:
            self.query = common.getUserInput(language(30361).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query == None or self.query == ''):
            self.list = self.search_list('movie', self.query)
            index().movieList(self.list)
            return self.list

    def search_tv(self, query=None):
        if query == None:
            self.query = common.getUserInput(language(30361).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query == None or self.query == ''):
            self.list = self.search_list('tv', self.query)
            index().showList(self.list)
            return self.list

    def movies(self, url):
        self.list = index().cache(self.movies_list, 24, url)
        index().movieList(self.list)
        return self.list

    def movies_2(self, url):
        self.list = index().cache(self.movies_list, 240, url)
        return self.list

    def cartoons(self):
        try:
            c1 = index().cache(self.movies_list, 24, 'g=8&y=1&l=&p=')
            c2 = index().cache(self.movies_list, 24, 'g=8&y=2&l=&p=')

            self.list = c1 + c2
            for i in range(0, len(self.list)): self.list[i].update({'type': 'movie'})
            self.list = [i for n, i in enumerate(self.list) if i not in self.list[n + 1:]]
            self.list = sorted(self.list, key=itemgetter('name'))

            index().cartoonList(self.list)
            return self.list
        except:
            pass

    def shows(self, url):
        self.list = index().cache(self.shows_list, 24, url)
        index().showList(self.list)
        return self.list

    def networks(self):
        networks = ['mega', 'ant1', 'alpha', 'star', 'skai', 'nerit', 'epsilontv', 'kontrachannel', 'bluesky', 'action24', 'art', 'sigmatv', 'ant1_cy', 'mtvgreece', 'madtv']
        self.list = index().cache(self.shows_list, 24, 'y=1')
        try: self.list = [i for i in self.list if i['network'] in networks]
        except: return
        index().showList(self.list)
        return self.list

    def network(self, limit):
        self.list = index().cache(self.shows_list, 24, 'y=1')
        try: self.list = [i for i in self.list if i['network'] == limit]
        except: return
        index().showList(self.list)
        return self.list

    def titles_list(self, url):
        try:
            result = getUrl(url, timeout='20').result
            result = common.parseDOM(result, "select", attrs = { "onChange": ".+?" })
            result = ''.join(result)

            titles = re.compile('(<option.+?</option>)').findall(result)
        except:
            return

        for title in titles:
            try:
                name = common.parseDOM(title, "p", attrs = { "class": ".+?" })[0]
                name = name[0].capitalize() + name[1:]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(title, "option", ret="value")[0]
                url = urlparse.urlparse(url).query
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url})
            except:
                pass

        return self.list

    def search_list(self, content, url):
        try:
            query = urllib.quote_plus(url)
            query = 'https://encrypted.google.com/search?as_q=%s&as_sitesearch=greek-movies.com' % query

            result = getUrl(query).result

            if content == 'movie':
                result = re.compile('greek-movies.com/(movies.php[?]m=\d*)').findall(result)
            elif content == 'tv':
                result = re.compile('greek-movies.com/(shows.php[?]s=\d*|series.php[?]s=\d*)').findall(result)
            result = uniqueList(result).list

            for i in result:
                self.list.append({'name': '0', 'url': urlparse.urljoin(self.base_link, i), 'image': '0', 'title': '0', 'year': '0', 'genre': 'Greek', 'plot': '0'})
        except:
            return self.list

        threads = []
        if content == 'movie':
            for i in range(0, len(self.list)): threads.append(Thread(self.movies_info, i))
        elif content == 'tv':
            for i in range(0, len(self.list)): threads.append(Thread(self.shows_info, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        self.list = [i for i in self.list if not i['name'] == '0']

        return self.list

    def movies_info(self, i):
        try:
            result = getUrl(self.list[i]['url'], timeout='30').result
            result = common.parseDOM(result, "div", attrs = { "class": "movie" })[0]

            title = common.parseDOM(result, "h1", attrs = { "class": "movie" })[0]
            title = common.replaceHTMLCodes(title)
            title = title.encode('utf-8')
            if not title == '0': self.list[i].update({'title': title})

            year = common.parseDOM(result, "h3", attrs = { "class": "movie" })[0]
            year = re.sub('[^0-9]', '', year.encode('utf-8'))
            if not year == '0': self.list[i].update({'year': year})

            name = '%s (%s)' % (title, year)
            try: name = name.encode('utf-8')
            except: pass
            if not title == '0': self.list[i].update({'name': name})

            image = common.parseDOM(result, "img", ret="src")[0]
            image = urlparse.urljoin(self.base_link, image)
            if image.endswith('icon/film.jpg'): image = '0'
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')
            if not image == '0': self.list[i].update({'image': image})
        except:
            pass

    def shows_info(self, i):
        try:
            result = getUrl(self.list[i]['url'], timeout='30').result
            result = common.parseDOM(result, "DIV", attrs = { "class": "maincontent" })[0]

            title = common.parseDOM(result, "p", attrs = { "class": "seriesheading2" })[0]
            title = common.replaceHTMLCodes(title)
            title = title.encode('utf-8')
            if not title == '0': self.list[i].update({'name': title, 'title': title})

            image = common.parseDOM(result, "img", ret="src")[0]
            image = urlparse.urljoin(self.base_link, image)
            if image.endswith('icon/film.jpg'): image = '0'
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')
            if not image == '0': self.list[i].update({'image': image})
        except:
            pass

    def movies_list(self, url):
        try:
            result = getUrl(self.movies_link + url, timeout='20').result
            result = common.parseDOM(result, "DIV", attrs = { "class": "maincontent" })

            movies = common.parseDOM(result, "td")
        except:
            return

        for movie in movies:
            try:
                title = common.parseDOM(movie, "p")[0]
                title = re.compile('(.+?) [(]\d{4}[)]$').findall(title)[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = common.parseDOM(movie, "p")[0]
                year = re.compile('.+? [(](\d{4})[)]$').findall(year)[0]
                year = common.replaceHTMLCodes(year)
                year = year.encode('utf-8')

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                url = common.parseDOM(movie, "a", ret="href")[0]
                url = urlparse.urljoin(self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(movie, "IMG", ret="SRC")[0]
                image = urlparse.urljoin(self.base_link, image)
                if image.endswith('icon/film.jpg'): image = '0'
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'title': title, 'year': year, 'genre': 'Greek', 'plot': '0'})
            except:
                pass

        return self.list

    def shows_list(self, url):
        try:
            self.result = []
            self.result2 = []

            def thread(url):
                try: self.result.append(getUrl(url, timeout='20').result)
                except: pass
            def thread2(url):
                try: self.result2.append(getUrl(url, timeout='20').result)
                except: pass

            threads = []
            threads.append(Thread(thread, self.series_link + url))
            threads.append(Thread(thread2, self.shows_link + url))
            [i.start() for i in threads]
            [i.join() for i in threads]

            if self.result == [] or self.result2 == []: return
            result = ''.join(self.result) + ''.join(self.result2)
            result = common.parseDOM(result, "DIV", attrs = { "class": "maincontent" })

            shows = common.parseDOM(result, "td")
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "p")[0]
                name = re.compile('(.+?) [(].+?[)]$').findall(name)[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(show, "a", ret="href")[0]
                url = urlparse.urljoin(self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(show, "IMG", ret="SRC")[0]
                image = urlparse.urljoin(self.base_link, image)
                if image.endswith('icon/film.jpg'): image = '0'
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                network = common.parseDOM(show, "IMG", ret="SRC")[1]
                network = network.split("/")[-1].split('.')[0]
                network = common.replaceHTMLCodes(network)
                network = network.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'network': network, 'genre': 'Greek', 'plot': '0'})
            except:
                pass

        try: self.list = sorted(self.list, key=itemgetter('name'))
        except: pass

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url, timeout='20').result
            result = common.parseDOM(result, "DIV", attrs = { "class": "maincontent" })[0]

            sort_dict = {'ce99ceb1cebd':'01', 'cea6ceb5ceb2':'02', 'ce9cceaccf81':'03', 'ce91cf80cf81':'04', 'ce9cceacceb9':'05', 'ce99cebfcf8dcebd':'06', 'ce99cebfcf8dcebb':'07', 'ce91cf8dceb3':'08', 'cea3ceb5cf80':'09', 'ce9fcebacf84':'10', 'ce9dcebfcead':'11', 'ce94ceb5ceba':'12'}
            sort_date = common.parseDOM(result, "div", attrs = { "class": "year_container_new" })

            episodes = common.parseDOM(result, "div", attrs = { "class": "episodemenu_new" })
        except:
            return

        for episode in episodes:
            try:
                name = common.parseDOM(episode, "a", attrs = { "class": "episodetitle" })[0]

                if not len(sort_date) == 0:
                    r = result.split(episode)[0]
                    y = common.parseDOM(r, "div", attrs = { "class": "year_container_new" })[-1]
                    m = common.parseDOM(r, "div", attrs = { "class": "month_container_new" })[-1]
                    m = common.parseDOM(m, "div", attrs = { "class": "left_element_new" })[0]
                    m = repr(m.encode('utf-8')).replace('\\x', '').replace('\'', '')
                    m = sort_dict[m]
                    name = '%04d-%02d-%02d' % (int(y), int(m), int(name))

                name = 'Επεισόδιο '.decode('iso-8859-7') + name
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "a", ret="onclick")[0]
                url = re.compile("'(.+?)'").findall(url)
                url = self.episode_link % (url[0], url[1])
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            host_order = ['youtube', 'dailymotion', 'datemule', 'streamin', 'vidto', 'megatv', 'antenna', 'alphatv', 'skai', 'sigmatv', 'nerit', 'ant1iwo', 'livenews']

            if url.startswith(self.movies_link):
                result = getUrl(url, timeout='20').result
                result = common.parseDOM(result, "DIV", attrs = { "class": "maincontent" })[0]
                result = re.compile('(<a.+?</a>)').findall(result)
                result = uniqueList(result).list
            else:
                u = url.split('?')
                result = getUrl(u[0], post=u[1], timeout='20').result
                result = re.compile('(<a.+?</a>)').findall(result)
                result = uniqueList(result).list

            sources = []
            for i in result:
                try:
                    host = common.parseDOM(i, "a")[0]
                    host = host.split(' ')[-1].split('>', 1)[-1].rsplit('<', 1)[0]
                    host = host.lower()

                    url = common.parseDOM(i, "a", ret="href")[0]
                    url = '%s/%s' % (self.base_link, url)
                    sources.append({'host': host, 'url': url})
                except:
                    pass

            sources = [i for i in sources if any(x in i['host'] for x in host_order)]
            #sources.sort(key=lambda x: host_order.index(x['host']))
            import random
            random.shuffle(sources)

            if len(sources) == 0:
                url = common.parseDOM(result, "a", ret="href")[0]
                url = '%s/%s' % (self.base_link, url)
                sources.append({'url': url})

            if len(sources) == 0: return
        except:
            return

        for i in sources:
            try:
                url = i['url']
                result = getUrl(url, timeout='20').result
                url = common.parseDOM(result, "button", ret="OnClick")[0]
                url = url.split("'")[1]

                url = resolver().sources_resolve(url)

                if url == None: raise Exception()
                return url
            except:
                pass

class mega:
    def __init__(self):
        self.list = []
        self.base_link = 'http://www.megatv.com'
        self.feed_link = 'http://megatv.feed.gr'
        self.media_link = 'http://media.megatv.com'
        self.shows_link = 'http://megatv.feed.gr/mobile/mobile.asp?pageid=816&catidlocal=32623&subidlocal=20933'
        self.episodes_link = 'http://megatv.feed.gr/mobile/mobile/ekpompiindex_29954.asp?pageid=816&catidlocal=%s'
        self.news_link = 'http://www.megatv.com/webtv/default.asp?catid=27377&catidlocal=27377'
        self.sports_link = 'http://www.megatv.com/webtv/default.asp?catid=27377&catidlocal=27387'

    def shows(self):
        self.list = index().cache(self.shows_list, 24)
        index().showList(self.list)
        return self.list

    def news(self):
        name = 'MEGA GEGONOTA'
        self.list = self.episodes_list2(name, self.news_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)
        return self.list

    def sports(self):
        name = 'MEGA SPORTS'
        self.list = self.episodes_list2(name, self.sports_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)
        return self.list

    def shows_list(self):
        try:
            result = getUrl(self.shows_link, mobile=True).result
            shows = common.parseDOM(result, "li")
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "h1")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                tpl = common.parseDOM(show, "a", ret="data-tpl")[0]
                if not tpl == 'ekpompiindex': raise Exception()

                url = common.parseDOM(show, "a", ret="data-params")[0]
                url = urlparse.parse_qs(urlparse.urlparse(url).query)['catid'][0]
                url = self.episodes_link % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': '0', 'genre': 'Greek', 'plot': '0'})
            except:
                pass

        threads = []
        for i in range(0, len(self.list)): threads.append(Thread(self.shows_info, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        return self.list

    def shows_info(self, i):
        try:
            result = getUrl(self.list[i]['url'], mobile=True).result

            image = common.parseDOM(result, "img", ret="src")[0]
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')
            self.list[i].update({'image': image})
        except:
            pass

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url, mobile=True).result
            result = common.parseDOM(result, "section", attrs = { "class": "ekpompes.+?" })[0]
            episodes = common.parseDOM(result, "li")
        except:
            return

        for episode in episodes:
            try:
                name = common.parseDOM(episode, "h5")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "a", ret="data-vUrl")[0]
                url = url.replace(',', '').split('/i/', 1)[-1].rsplit('.csmil', 1)[0]
                url = urlparse.urljoin(self.media_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(episode, "img", ret="src")[0]
                image = urlparse.urljoin(self.media_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def episodes_list2(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url).result
            result = result.decode('iso-8859-7').encode('utf-8')

            v1 = '/megagegonota/'
            match = re.search("addPrototypeElement[(]'.+?','REST','(.+?)','(.+?)'.+?[)]", result)
            v2,v3 = match.groups()
            redirect = '%s%s%s?%s' % (self.base_link, v1, v2, v3)

            result = getUrl(redirect).result
            result = result.decode('iso-8859-7').encode('utf-8')
            result = common.parseDOM(result, "div", attrs = { "class": "rest" })[0]
            episodes = common.parseDOM(result, "li")
        except:
            return

        for episode in episodes:
            try:
                name = common.parseDOM(episode, "a")[1]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "a", ret="href")[0]

                url = re.compile("'(.+?)'").findall(url)
                url = [i for i in url if 'catid' in i][0]
                url = 'r.asp?%s' % url
                url = urlparse.urljoin(self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(episode, "img", ret="src")[0]
                if not image.startswith('http://'):
                    image = '%s%s%s' % (self.base_link, v1, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            result = getUrl(url).result
            url = re.compile('{file:"(%s/.+?)"' % self.media_link).findall(result)[0]
            return url
        except:
            return

class ant1:
    def __init__(self):
        self.list = []
        self.base_link = 'http://www.antenna.gr'
        self.img_link = 'http://www.antenna.gr/imgHandler/326/'
        self.shows_link = 'http://www.antenna.gr/tv/doubleip/shows?version=3.0'
        self.episodes_link = 'http://www.antenna.gr/tv/doubleip/show?version=3.0&sid='
        self.episodes_link2 = 'http://www.antenna.gr/tv/doubleip/categories?version=3.0&howmany=100&cid='
        self.news_link = 'http://www.antenna.gr/tv/doubleip/show?version=3.0&sid=222903'
        self.sports_link = 'http://www.antenna.gr/tv/doubleip/categories?version=3.0&howmany=100&cid=3062'
        self.watch_link = 'http://www.antenna.gr/webtv/watch?cid=%s'
        self.info_link = 'http://www.antenna.gr/webtv/templates/data/player?cid=%s'

    def shows(self):
        self.list = index().cache(self.shows_list, 24)
        index().showList(self.list)
        return self.list

    def news(self):
        name = 'ANT1 NEWS'
        self.list = self.episodes_list(name, self.news_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)
        return self.list

    def sports(self):
        name = 'ANT1 SPORTS'
        self.list = self.episodes_list(name, self.sports_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)
        return self.list

    def shows_list(self):
        try:
            self.list.append({'name': 'ANT1 NEWS', 'url': self.news_link, 'image': 'http://www.antenna.gr/imgHandler/326/5a7c9f1a-79b6-47e0-b8ac-304d4e84c591.jpg', 'genre': 'Greek', 'plot': 'ANT1 NEWS'})

            result = getUrl(self.shows_link, mobile=True).result
            shows = re.compile('({.+?})').findall(result)
        except:
            return

        for show in shows:
            try:
                i = json.loads(show)

                name = i['teasertitle'].strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                image = i['webpath'].strip()
                image = urlparse.urljoin(self.img_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                url = i['id'].strip()
                url = self.episodes_link + url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try: plot = i['teasertext'].strip()
                except: plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'genre': 'Greek', 'plot': plot})
            except:
                pass

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url, mobile=True).result

            if url.startswith(self.episodes_link):
                id = json.loads(result)
                id = id['feed']['show']['videolib']
                if url.endswith('sid=223077'): id = '3110'#EUROPA LEAGUE
                elif url.endswith('sid=318756'): id = '3246'#ΟΛΑ ΤΡΕΛΑ
                elif url.endswith('sid=314594'): id = '4542'#THE VOICE
            elif url.startswith(self.episodes_link2):
                id = ''

            if id == '':
                episodes = result.replace("'",'"').replace('"title"','"caption"').replace('"image"','"webpath"').replace('"trailer_contentid"','"contentid"')
                episodes = re.compile('({.+?})').findall(episodes)
            else:
                url = self.episodes_link2 + id
                episodes = getUrl(url, mobile=True).result
                episodes = re.compile('({.+?})').findall(episodes)
        except:
            return

        for episode in episodes:
            try:
                i = json.loads(episode)

                name = i['caption'].strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                image = i['webpath'].strip()
                image = urlparse.urljoin(self.img_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                url = i['contentid'].strip()
                url = self.watch_link % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        id = url.split("?")[-1].split("cid=")[-1].split("&")[0]
        dataUrl = self.info_link % id
        pageUrl = self.watch_link % id
        proxyUrl = 'https://proxy-de.hide.me/go.php?b=20&u=%s' % dataUrl
        swfUrl = 'http://www.antenna.gr/webtv/images/fbplayer.swf'

        try:
            result = getUrl(dataUrl).result
            playpath = common.parseDOM(result, "appStream")[0]
            #if playpath.endswith('GR.flv'): result = getUrl(proxyUrl).result
            if playpath.endswith('GR.flv'): return

            playpath = common.parseDOM(result, "appStream")[0]
            rtmp = common.parseDOM(result, "FMS")[0]

            url = '%s playpath=%s pageUrl=%s swfUrl=%s swfVfy=true timeout=10' % (rtmp, playpath, pageUrl, swfUrl)
            if playpath.startswith('http://'): url = playpath
            return url
        except:
            pass

class alpha:
    def __init__(self):
        self.list = []
        self.data = []
        self.base_link = 'http://www.alphatv.gr'
        self.shows_link = 'http://www.alphatv.gr/shows'
        self.shows_link2 = 'http://www.alphatv.gr/views/ajax?view_name=alpha_shows_category_view&view_display_id=page_3&view_path=shows&view_base_path=shows&page=%s'
        self.news_link = 'http://www.alphatv.gr/shows/informative/news'

    def shows(self):
        self.list = index().cache(self.shows_list, 24)
        index().showList(self.list)
        return self.list

    def news(self):
        name = 'ALPHA NEWS'
        self.list = self.episodes_list(name, self.news_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)
        return self.list

    def shows_list(self):
        try:
            result = getUrl(self.shows_link).result
            filter = common.parseDOM(result, "span", attrs = { "class": "field-content" })
            filter = common.parseDOM(filter, "a", ret="href")
            filter = uniqueList(filter).list

            threads = []
            result = ''
            for i in range(0, 5):
                self.data.append('')
                showsUrl = self.shows_link2 % str(i)
                threads.append(Thread(self.thread, showsUrl, i))
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += json.loads(i)[1]['data']

            shows = common.parseDOM(result, "li")
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "span")[0]
                name = common.parseDOM(name, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(show, "a", ret="href")[0]
                if not any(url == i for i in filter): raise Exception()
                url = urlparse.urljoin(self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(show, "img", ret="src")[0]
                image = urlparse.urljoin(self.base_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'genre': 'Greek', 'plot': '0'})
            except:
                pass

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            redirects = ['/webtv/shows?page=0', '/webtv/shows?page=1', '/webtv/shows?page=2', '/webtv/shows?page=3', '/webtv/episodes?page=0', '/webtv/episodes?page=1', '/webtv/episodes?page=2', '/webtv/episodes?page=3', '/webtv/news?page=0', '/webtv/news?page=1']
            base = url

            count = 0
            threads = []
            result = ''
            for redirect in redirects:
                self.data.append('')
                threads.append(Thread(self.thread, url + redirect, count))
                count = count + 1
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            episodes = common.parseDOM(result, "div", attrs = { "class": "views-field.+?" })
        except:
        	return

        for episode in episodes:
            try:
                name = common.parseDOM(episode, "img", ret="alt")[-1]
                if name == '': raise Exception()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "a", ret="href")[-1]
                url = urlparse.urljoin(self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                if not url.startswith(base): raise Exception()
                if url in [i['url'] for i in self.list]: raise Exception()

                image = common.parseDOM(episode, "img", ret="src")[-1]
                image = urlparse.urljoin(self.base_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            result = getUrl(url).result
            result = result.replace('\n','')

            try:
                url = re.compile("playlist:.+?file: '(.+?[.]m3u8)'").findall(result)[0]
                if "EXTM3U" in getUrl(url).result: return url
            except:
                pass

            try:
                url = re.compile('playlist:.+?"(rtmp[:].+?)"').findall(result)[0]
                url += ' timeout=10'
                return url
            except:
                pass

            try:
                url = common.parseDOM(result, "embed", ret="src")
                url = [i for i in url if 'youtube' in i][0]
                import commonresolvers
                url = commonresolvers.youtube().resolve(url)
                return url
            except:
                pass
        except:
            return

    def thread(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
        except:
            return

class star:
    def __init__(self):
        self.list = []
        self.base_link = 'http://www.star.gr'
        self.shows_link = 'http://www.star.gr/_layouts/handlers/tv/feeds.program.ashx?catTitle=hosts'
        self.episodes_link = 'http://www.star.gr/_layouts/handlers/tv/feeds.program.ashx?catTitle=%s&artId=%s'
        self.news_link = 'http://www.star.gr/_layouts/handlers/tv/feeds.program.ashx?catTitle=News&artId=9'
        self.watch_link = 'http://cdnapi.kaltura.com/p/21154092/sp/2115409200/playManifest/entryId/%s/flavorId/%s/format/url/protocol/http/a.mp4'
        self.enikos_link = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=UU9yHAKhKiOMHIcKqSB21RDA'

    def shows(self):
        self.list = index().cache(self.shows_list, 24)
        index().showList(self.list)
        return self.list

    def news(self):
        name = 'STAR NEWS'
        image = 'http://www.star.gr/tv/PublishingImages/160913114342_2118.jpg'
        self.list = self.episodes_list(name, self.news_link, image, 'Greek', '0', name)
        index().episodeList(self.list)
        return self.list

    def shows_list(self):
        try:
            result = getUrl(self.shows_link, mobile=True).result
            result = json.loads(result)
            shows = result['hosts']
        except:
            return

        for show in shows:
            try:
                name = show['Title'].strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                image = show['Image'].strip()
                image = urlparse.urljoin(self.base_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                id = show['ProgramId']
                cat = show['ProgramCat'].strip()
                url = self.episodes_link % (cat, id)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                if url.endswith('artId=42'): url = self.enikos_link

                self.list.append({'name': name, 'url': url, 'image': image, 'genre': 'Greek', 'plot': '0'})
            except:
                pass

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url, mobile=True).result
            result = json.loads(result)

            try: plot = result['programme']['StoryLinePlain'].strip()
            except: plot = '0'
            plot = common.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')

            episodes = result['videosprogram']
        except:
        	return

        for episode in episodes:
            try:
                name = episode['Title'].strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = episode['VideoID'].strip()
                url = self.watch_link % (url, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        return url

class skai:
    def __init__(self):
        self.list = []
        self.base_link = 'http://www.skai.gr'
        self.show_link = 'http://www.skai.gr/player/TV/?mmid=%s'
        self.shows_link = 'http://www.skai.gr/Ajax.aspx?m=Skai.TV.ProgramListView&la=0&Type=TV&Day='
        self.podcasts_link = 'http://www.skai.gr/Ajax.aspx?m=Skai.TV.ProgramListView&la=0&Type=Radio&Day='
        self.episodes_link = 'http://www.skai.gr/Ajax.aspx?m=Skai.Player.ItemView&cid=6&alid=%s'
        self.docs_link = 'http://www.skai.gr/mobile/tv/category?cid=6'
        self.news_link = 'http://www.skai.gr/player/TV/?mmid=243980'

    def shows(self):
        self.list = index().cache(self.shows_list, 24, self.shows_link)
        index().showList(self.list)
        return self.list

    def podcasts(self):
        self.list = index().cache(self.shows_list, 24, self.podcasts_link)
        index().showList(self.list)
        return self.list

    def docs(self):
        self.list = index().cache(self.docs_list, 24)
        index().showList(self.list)
        return self.list

    def news(self):
        name = 'SKAI NEWS'
        self.list = self.episodes_list(name, self.news_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)
        return self.list

    def docs_list(self):
        try:
            result = getUrl(self.docs_link).result
            result = common.parseDOM(result, "div", attrs = { "id": "mbl-tv-ondemand" })[0]

            docs = common.parseDOM(result, "li")
        except:
            return

        for doc in docs:
            try:
                name = common.parseDOM(doc, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(doc, "a", ret="href")[0]
                url = urlparse.urljoin(self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'u': url, 'url': '0', 'image': '0', 'genre': 'Greek', 'plot': '0'})
            except:
                pass

        threads = []
        for i in range(0, len(self.list)): threads.append(Thread(self.docs_info, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        self.list = [i for i in self.list if not i['url'] == '0']

        return self.list

    def docs_info(self, i):
        try:
            result = getUrl(self.list[i]['u']).result
            result = common.parseDOM(result, "div", attrs = { "id": "mbl-tv-ondemand" })[0]

            url = common.parseDOM(result, "a", ret="href")[0]
            url = self.show_link % url.split('=')[-1]
            url = urlparse.urljoin(self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            if not url == '0': self.list[i].update({'url': url})

            image = common.parseDOM(result, "img", ret="src")[0]
            image = urlparse.urljoin(self.base_link, image)
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')
            if not image == '0': self.list[i].update({'image': image})
        except:
            pass

    def shows_list(self, url):
        try:
            u = []
            d = datetime.datetime.utcnow()
            for i in range(0, 7):
                u.append(url + d.strftime("%d.%m.%Y"))
                d = d - datetime.timedelta(hours=24)
            u = u[::-1]

            self.result = []

            def thread(url):
                try: self.result.append(getUrl(url).result)
                except: pass

            threads = []
            for i in range(0, 7): threads.append(Thread(thread, u[i]))
            [i.start() for i in threads]
            [i.join() for i in threads]

            result = ''.join(self.result)

            shows = common.parseDOM(result, "Show", attrs = { "TVonly": "0" })
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "Show")[0]
                name = name.split('[')[-1].split(']')[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(show, "Link")[0]
                url = url.split('[')[-1].split(']')[0]
                url = urlparse.urljoin(self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(show, "ShowImage")[0]
                image = image.split('[')[-1].split(']')[0]
                image = urlparse.urljoin(self.base_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                plot = common.parseDOM(show, "Description")[0]
                plot = plot.split('[')[-1].split(']')[0]
                plot = plot.replace('<br>','').replace('</br>','').replace('\n','').split('<')[0].strip()
                if plot == '': plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                if image in str(self.list): raise Exception()
                if not 'mmid=' in url: raise Exception()

                self.list.append({'name': name, 'url': url, 'image': image, 'genre': 'Greek', 'plot': plot})
            except:
                pass

        try: self.list = sorted(self.list, key=itemgetter('name'))
        except: pass

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url).result
            url = common.parseDOM(result, "li", ret="id", attrs = { "class": "active_sub" })[0]

            self.result = []

            def thread(url, i):
                try: self.result[i] = getUrl(url).result
                except: pass

            threads = []
            for i in range(1, 3): self.result.append('')
            for i in range(1, 3): threads.append(Thread(thread, self.episodes_link % url + '&Page=%s' % str(i), i-1))
            [i.start() for i in threads]
            [i.join() for i in threads]

            result = ''
            for i in self.result: result += i

            episodes = common.parseDOM(result, "Item")
        except:
        	return

        for episode in episodes:
            try:
                title = common.parseDOM(episode, "Title")[0]
                title = title.split('[')[-1].split(']')[0]

                date = common.parseDOM(episode, "Date")[0]
                date = date.split('[')[-1].split(']')[0]
                date = date.split('T')[0]

                name = '%s (%s)' % (title, date)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "File")[0]
                url = url.split('[')[-1].split(']')[0]
                url = urlparse.urljoin(self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(episode, "Photo1")[0]
                image = urlparse.urljoin(self.base_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            result = getUrl(url).result
            url = common.parseDOM(result, "span", attrs = { "id": "p-file" })[0]
            return url
        except:
            return

class sigma:
    def __init__(self):
        self.list = []
        self.data = []
        self.base_link = 'http://www.sigmatv.com'
        self.shows_link = 'http://www.sigmatv.com/shows'
        self.news_link = 'http://www.sigmatv.com/shows/tomes-sta-gegonota/episodes'

    def shows(self):
        self.list = index().cache(self.shows_list, 24)
        index().showList(self.list)
        return self.list

    def news(self):
        name = 'SIGMA NEWS'
        self.list = self.episodes_list(name, self.news_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)
        return self.list

    def shows_list(self):
        try:
            result = getUrl(self.shows_link).result
            shows = common.parseDOM(result, "div", attrs = { "class": "show_entry.+?" })
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "div", attrs = { "class": "body" })[0]
                name = common.parseDOM(name, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(show, "a", ret="href")[0]
                filter = ['/uefa-champions-league', '/seirestainies', '/tilenouveles', '/alpha']
                if any(url.endswith(i) for i in filter): raise Exception()
                url = '%s/episodes' % url
                url = urlparse.urljoin(self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(show, "img", ret="src")[0]
                image = image.replace('/./', '')
                image = urlparse.urljoin(self.base_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                try: plot = common.parseDOM(show, "div", attrs = { "style": "min.+?" })[-1]
                except: plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'genre': 'Greek', 'plot': plot})
            except:
                pass

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            count = 0
            threads = []
            result = ''
            for i in range(0, 100, 20):
                self.data.append('')
                episodesUrl = url + '/page/%s' % str(i)
                threads.append(Thread(self.thread, episodesUrl, count))
                count = count + 1
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            episodes = common.parseDOM(result, "div", attrs = { "class": "entry .+?" })
        except:
            return

        for episode in episodes:
            try:
                name = common.parseDOM(episode, "img", ret="alt")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "a", ret="href")[0]
                url = urlparse.urljoin(self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(episode, "img", ret="src")[0]
                if '/no-image' in image: raise Exception()
                image = urlparse.urljoin(self.base_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            result = getUrl(url).result

            try: url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video/mp4" })[0]
            except: url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video/flash" })[0]
            url = common.replaceHTMLCodes(url)

            url = getUrl(url, output='geturl').result
            return url
        except:
            return

    def thread(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
        except:
            return

class nerit:
    def __init__(self):
        self.base_link = 'http://webtv.nerit.gr'
        self.m3u8_link = 'http://hprt-vod.flashcloud.mediacdn.com/mediacache/mobile/mp4:hprt/%s/playlist.m3u8'

    def resolve(self, url):
        try:
            result = getUrl(url).result

            embed = common.parseDOM(result, "div", attrs = { "id": "player-embed" })[0]
            embed = common.parseDOM(embed, "iframe", ret="src")[0]
            embed = embed.replace(' ', '%20')

            result = getUrl(embed).result
            url = re.compile("file:\s+'(.+?)'").findall(result)[0]
            url = url.replace(' ', '%20')
            url = self.m3u8_link % url
            return url
        except:
            return

class ant1cy:
    def __init__(self):
        self.base_link = 'http://www.ant1iwo.com'
        self.old_link = 'http://www.ant1.com.cy'

    def resolve(self, url):
        try:
            result = getUrl(url).result
            rtmp = re.compile("netConnectionUrl:\s+'(.+?)'").findall(result)[0]
            playpath = common.parseDOM(result, "div", ret="data-video")[0]
            if ' ' in playpath: raise Exception()
            url = '%s playpath=%s' % (rtmp, playpath)
            return url
        except:
            return

class megacy:
    def __init__(self):
        self.base_link = 'http://www.livenews.com.cy'

    def resolve(self, url):
        try:
            result = getUrl(url, mobile=True).result

            embed = common.parseDOM(result, "iframe", ret="src")
            embed = [i for i in embed if 'itemid' in i][0]

            result = getUrl(embed, mobile=True).result
            url = common.parseDOM(result, "video", ret="sr.+?")[0]
            return url
        except:
            return

class realfm:
    def __init__(self):
        self.list = []
        self.br_link = 'http://www.real.gr'
        self.base_link = 'http://www.realmobile.gr'
        self.image_link = 'http://www.real.gr/Files/Articles/Photo/320_182_115547.jpg'
        self.episodes_link = 'http://www.realmobile.gr/msimple/article_details.php?ID=%s&catID=%s'
        self.podcasts_link = 'http://www.real.gr/default.aspx?page=radioathens&catID=50'
        self.added_link = 'http://www.realmobile.gr/msimple/articles.php?categoryID=50'
        self.show_link = 'http://www.realmobile.gr/msimple/articles.php?categoryID=%s'

    def podcasts(self):
        self.list = index().cache(self.shows_list, 24)
        index().showList(self.list)
        return self.list

    def shows_list(self):
        try:
            result = getUrl(self.podcasts_link).result
            result = common.parseDOM(result, "div", attrs = { "class": "middle-container" })[0]
            result = common.parseDOM(result, "tbody")[0]

            shows = re.compile('(<a.+?</a>)').findall(result)
        except:
            return

        for show in shows:
            try:
                u = common.parseDOM(show, "a", ret="href")[0]
                if not 'catID=' in u: raise Exception()
                u = '%s/%s' % (self.br_link, u)
                u = common.replaceHTMLCodes(u)
                u = u.encode('utf-8')

                url = re.compile('catID=(\d*)').findall(u)[0]
                url = self.show_link % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(show, "img", ret="src")[0]
                image = urlparse.urljoin(self.br_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': '0', 'url': url, 'u': u, 'image': image, 'genre': 'Greek', 'plot': '0'})
            except:
                pass

        threads = []
        for i in range(0, len(self.list)): threads.append(Thread(self.shows_info, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        self.list = [i for i in self.list if not i['name'] == '0']
        self.list = [{'name': 'realfm97.8', 'url': self.added_link, 'image': self.image_link, 'genre': 'Greek', 'plot': '0'}] + self.list

        return self.list

    def shows_info(self, i):
        try:
            result = getUrl(self.list[i]['u']).result

            name = common.parseDOM(result, "title")[0]
            name = name.split(' - ', 1)[-1]
            name = common.replaceHTMLCodes(name)
            name = name.encode('utf-8')
            self.list[i].update({'name': name})
        except:
            pass

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url).result
            result = common.parseDOM(result, "script", attrs = { "type": "text/javascript" })
            result = [i for i in result if 'title = ' in i][0]

            cat = re.compile('categoryID=(\d*)').findall(url)[0]
            episode = result.replace('\n','')
        except:
        	return

        for i in range(0, 51):
            try:
                name = episode.split('title = ', 1)[-1]
                name = re.compile("'%s'.+?'(.+?)'" % str(i)).findall(name)[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = episode.split('id = ', 1)[-1].replace(' ', '')
                url = re.compile("'%s':(\d*)" % str(i)).findall(url)[0]
                url = self.episodes_link % (url, cat)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = episode.split('thumbnail = ', 1)[-1]
                image = re.compile("'%s'.+?'(.+?)'" % str(i)).findall(image)[0]
                image = urlparse.urljoin(self.base_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                if cat == '50': stacked = '0'
                else: stacked = '1'

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show, 'stacked': stacked})
            except:
                pass

        return self.list

    def stacked_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url).result
            result = common.parseDOM(result, "ul", attrs = { "class": "pageitem" })[0]

            url = common.parseDOM(result, "a", ret="href", attrs = { "target": "_blank" })

            for i in range(0, len(url)):
                self.list.append({'name': '%s (%s)' % (name, str(i+1)), 'url': url[i], 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
        except:
        	pass

        return self.list

    def resolve(self, url):
        try:
            result = getUrl(url).result
            result = common.parseDOM(result, "ul", attrs = { "class": "pageitem" })[0]

            url = common.parseDOM(result, "a", ret="href", attrs = { "target": "_blank" })[0]
            return url
        except:
            return

class novasports:
    def __init__(self):
        self.list = []
        self.base_link = 'http://www.novasports.gr'
        self.shows_link = 'http://www.novasports.gr/web-tv/shows'
        self.show_link = 'http://www.novasports.gr/sys/novasports/ShowMore/ShowMore?pg=1&perPage=100&id=%s'
        self.superleague_link = 'http://www.novasports.gr/web-tv/on-demand/categories/?catid=13'
        self.news_link = 'http://www.novasports.gr/web-tv/on-demand/categories/?catid=0'

    def shows(self):
        try:
            name = 'Novasports'

            self.list = index().cache(self.shows_list, 24, self.shows_link)

            url = [i['url'] for i in self.list]
            url = uniqueList(url).list
            url = url[:5]

            threads = []
            self.list = []
            for u in url: threads.append(Thread(self.episodes_list, name, u, '0', 'Greek', '0', name))
            [i.start() for i in threads]
            [i.join() for i in threads]

            self.list = sorted(self.list, key=itemgetter('date'))[::-1]
            index().episodeList(self.list)
            return self.list
        except:
            return

    def news(self):
        name = 'Novasports News'
        self.list = self.episodes_list2(name, self.news_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)
        return self.list

    def superleague(self):
        name = 'Super League'
        self.list = self.episodes_list2(name, self.superleague_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)
        return self.list

    def shows_list(self, url):
        try:
            result = getUrl(url).result
            result = common.parseDOM(result, "div", attrs = { "class": "leftArticle.+?" })[0]

            shows = common.parseDOM(result, "div", attrs = { "class": "g\d*" })
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "span", ret="data-title")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(show, "span", ret="data-url")[0]
                url = urlparse.urljoin(self.base_link, url)
                url = self.show_link % urlparse.parse_qs(urlparse.urlparse(url).query)['show'][0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(show, "img", ret="src")[0]
                image = urlparse.urljoin(self.base_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': '0', 'genre': 'Greek', 'plot': '0'})
            except:
                pass

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url).result
            result = result.replace('\n','')

            episodes = common.parseDOM(result, "div", attrs = { "class": "g\d*" })
        except:
            return

        for episode in episodes:
            try:
                name = common.parseDOM(episode, "div", attrs = { "class": "miniHeading" })[0]
                name += ' (%s)' % re.compile('(\d{2}/\d{2}/\d{4})').findall(episode)[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "a", ret="href")[-1]
                url = urlparse.urljoin(self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(episode, "img", ret="src")[0]
                image = urlparse.urljoin(self.base_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                date = re.compile('(\d{2})/(\d{2})/(\d{4})').findall(episode)[0]
                date = '%s-%s-%s' % (date[2], date[1], date[0])
                date = date.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': date, 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('date'))[::-1]

        return self.list

    def episodes_list2(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url).result
            result = common.parseDOM(result, "div", attrs = { "class": "rightArticle.+?" })[0]

            episodes = common.parseDOM(result, "div", attrs = { "class": "g\d*" })
        except:
            return

        try:
            next = common.parseDOM(result, "li", attrs = { "class": "nextButtonWrapper" })[0]
            next = common.parseDOM(next, "a", ret="href")[0]
            next = urlparse.urljoin(self.base_link, next)
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for episode in episodes:
            try:
                name = common.parseDOM(episode, "span", ret="data-title")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "span", ret="data-url")[0]
                url = urlparse.urljoin(self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(episode, "img", ret="src")[0]
                image = urlparse.urljoin(self.base_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show, 'next': next})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            result = getUrl(url).result

            url = common.parseDOM(result, "div", ret="data-video-url", attrs = { "id": "webTvVideo" })[0]
            return url
        except:
            return

class eradio:
    def __init__(self):
        self.list = []
        self.base_link = 'http://eradio.mobi'
        self.radios_link = 'http://eradio.mobi/cache/1/1/medialist.json'
        self.trending_link = 'http://eradio.mobi/cache/1/1/medialistTop_trending.json'
        self.top20_link = 'http://eradio.mobi/cache/1/1/medialist_top20.json'
        self.new_link = 'http://eradio.mobi/cache/1/1/medialist_new.json'
        self.genres_link = 'http://eradio.mobi/cache/1/1/categories.json'
        self.regions_link = 'http://eradio.mobi/cache/1/1/regions.json'
        self.genre_link = 'http://eradio.mobi/cache/1/1/medialist_categoryID%s.json'
        self.region_link = 'http://eradio.mobi/cache/1/1/medialist_regionID%s.json'
        self.resolve_link = 'http://eradio.mobi/cache/1/1/media/%s.json'
        self.image_link = 'http://cdn.e-radio.gr/logos/%s'

    def genres(self):
        try:
            self.list = index().cache(self.categories_list, 24, self.genres_link)
            return self.list
        except:
            pass

    def regions(self):
        try:
            self.list = index().cache(self.categories_list, 24, self.regions_link)
            return self.list
        except:
            pass

    def radios(self, url):
        try: url = getattr(self, url)
        except: pass
        self.list = index().cache(self.radios_list, 24, url)
        index().radioList(self.list)
        return self.list

    def categories_list(self, url):
        try:
            result = getUrl(url, mobile=True).result
            result = json.loads(result)

            try: categories = result['categories']
            except: categories = result['countries']
        except:
            return

        for cat in categories:
            try:
                try: name = cat['categoryName']
                except: name = cat['regionName']
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                try: url = self.genre_link % str(cat['categoryID'])
                except: url = self.region_link % str(cat['regionID'])
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url})
            except:
                pass

        return self.list

    def radios_list(self, url):
        try:
            result = getUrl(url, mobile=True).result
            result = json.loads(result)

            radios = result['media']
        except:
            return

        for radio in radios:
            try:
                name = radio['name'].strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = str(radio['stationID'])
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = radio['logo']
                image = self.image_link % image
                image = image.replace('/promo/', '/500/')
                if image.endswith('/nologo.png'): image = '0'
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            url = self.resolve_link % url

            result = getUrl(url, mobile=True).result
            result = json.loads(result)

            radio = result['media'][0]

            name = radio['name'].strip()
            name = common.replaceHTMLCodes(name)
            name = name.encode('utf-8')

            url = radio['mediaUrl'][0]['liveURL']
            if not url.startswith('http://'): url = '%s%s' % ('http://', url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            url = getUrl(url, output='geturl').result

            image = radio['logo']
            image = self.image_link % image
            image = image.replace('/promo/', '/500/')
            if image.endswith('/nologo.png'): image = '0'
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')

            return (name, url, image)
        except:
            return

class mtvchart:
    def __init__(self):
        self.list = []
        self.base_link = 'http://www.mtvgreece.gr'
        self.mtvhitlisthellas_link = 'http://www.mtvgreece.gr/hitlisthellas'
        self.mtvdancefloor_link = 'http://www.mtvgreece.gr/mtv-dance-flour-chart'
        self.eurotop20_link = 'http://www.mtvgreece.gr/mtv-euro-top-20'
        self.usatop20_link = 'http://www.mtvgreece.gr/mtv-usa-top-20'
        self.youtube_search = 'https://www.googleapis.com/youtube/v3/search?q='

    def mtvhitlisthellas(self):
        name = 'MTV Hit List Hellas'
        self.list = self.episodes_list(name, self.mtvhitlisthellas_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)
        return self.list

    def mtvdancefloor(self):
        name = 'MTV Dance Floor'
        self.list = self.episodes_list(name, self.mtvdancefloor_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)
        return self.list

    def eurotop20(self):
        name = 'Euro Top 20'
        self.list = self.episodes_list(name, self.eurotop20_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)
        return self.list

    def usatop20(self):
        name = 'U.S. Top 20'
        self.list = self.episodes_list(name, self.usatop20_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)
        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url).result

            episodes = common.parseDOM(result, "span", attrs = { "class": "artistRow" })
        except:
            return

        for episode in episodes:
            try:
                name = ' '.join(re.sub('<.+?>', '', episode).split()).strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                show = common.parseDOM(result, "strong")[0]
                show = common.replaceHTMLCodes(show)
                show = show.encode('utf-8')

                query = ' '.join(re.sub('=|&|:|;|-|"|,|\'|\.|\?|\/', ' ', name).split())
                url = self.youtube_search + query + ' official'
                url = common.replaceHTMLCodes(url)

                self.list.append({'name': name, 'url': url, 'image': musicImage, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

class rythmoschart:
    def __init__(self):
        self.list = []
        self.base_link = 'http://www.rythmosfm.gr'
        self.top20_link = 'http://www.rythmosfm.gr/community/top20/'
        self.youtube_search = 'https://www.googleapis.com/youtube/v3/search?q='

    def rythmoshitlist(self):
        name = 'Rythmos Hit List'
        self.list = self.episodes_list(name, self.top20_link, '0', 'Greek', '0', name)
        index().episodeList(self.list)
        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url).result

            episodes = common.parseDOM(result, "span", attrs = { "class": "toptitle" })
        except:
            return

        for episode in episodes:
            try:
                name = episode
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                show = episode.rsplit('-', 1)[-1].strip()
                show = common.replaceHTMLCodes(show)
                show = show.encode('utf-8')

                query = ' '.join(re.sub('=|&|:|;|-|"|,|\'|\.|\?|\/', ' ', name).split())
                url = self.youtube_search + query + ' official'
                url = common.replaceHTMLCodes(url)

                self.list.append({'name': name, 'url': url, 'image': musicImage, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

class dailymotion:
    def __init__(self):
        self.list = []
        self.data = []
        self.base_link = 'http://www.dailymotion.com'
        self.api_link = 'https://api.dailymotion.com'
        self.playlist_link = 'https://api.dailymotion.com/user/%s/videos?fields=description,duration,id,owner.username,taken_time,thumbnail_large_url,title,views_total&sort=recent&family_filter=1'
        self.watch_link = 'http://www.dailymotion.com/video/%s'
        self.info_link = 'http://www.dailymotion.com/embed/video/%s'

    def superball(self):
        name = 'Super Ball'
        channel = 'Super-Ball'
        url = self.playlist_link % channel
        self.list = self.episodes_list(name, url, '0', 'Greek', '0', name)
        index().episodeList(self.list)
        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            threads = []
            result = []
            for i in range(1, 3):
                self.data.append('')
                episodesUrl = url + '&limit=100&page=%s' % str(i)
                threads.append(Thread(self.thread, episodesUrl, i-1))
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += json.loads(i)['list']

            episodes = result
        except:
        	return

        for episode in episodes:
            try:
                name = episode['title']
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = episode['id']
                url = self.watch_link % url
                url = url.encode('utf-8')

                image = episode['thumbnail_large_url']
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def thread(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
        except:
            return

class youtube:
    def __init__(self):
        self.base_link = 'http://www.youtube.com'
        self.api_link = 'https://www.googleapis.com/youtube'
        self.key_link = 'QUl6YVN5Qk9TNHVTeWQyN09VMFhWMktTZE4zdlQyVUdfdjBnOXNJ'
        self.key_link = '&key=%s' % base64.urlsafe_b64decode(self.key_link)
        self.search_link = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=5&q=%s'
        self.youtube_search = 'https://www.googleapis.com/youtube/v3/search?q='
        self.playlists_link = 'https://www.googleapis.com/youtube/v3/playlists?part=snippet&maxResults=50&channelId=%s'
        self.playlist_link = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=%s'
        self.watch_link = 'http://www.youtube.com/watch?v=%s'

        self.enikos_link = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=UU9yHAKhKiOMHIcKqSB21RDA'

    def kontra(self):
        channel = 'UCkxZ5yUZFf1Vogm-scZM51A'
        self.list = index().cache(self.shows_list, 24, channel, [], [])
        index().showList(self.list)
        return self.list

    def art(self):
        channel = 'UCQW4NfyvMd-_o4YYVRP638A'
        self.list = index().cache(self.shows_list, 24, channel, [], [])
        index().showList(self.list)
        return self.list

    def madtv(self):
        channel = 'UCs3cho4vcDuCze0tk3W9iVQ'
        exc = ["PL1RY_6CEqdtnxJYgudDydiG4fKVoQouHf", "PL1RY_6CEqdtlu30q6SyuNe6Tk5IYjAiks", "PLE4B3F6B7F753D97C", "PL85C952EA930B9E90", "PL04B2C2D8B304BA48", "PL46B9D152167BA727"]
        self.list = index().cache(self.shows_list, 24, channel, [], exc)
        index().showList(self.list)
        return self.list

    def madgreekz(self):
        channel = 'UClMj1LyMRBMu_TG1B1BirqQ'
        exc = ["PL20iPi-qHKiz1wJCqvbvy5ffrtWT1VcVF", "PL20iPi-qHKiyWnRbBdnSF7RlDdAePiKzj", "PL20iPi-qHKiyZGlOs5DTElzAK_YNCDJn0", "PL20iPi-qHKiwyRhqqmOnbDvPSUgRzzxgq"]
        self.list = index().cache(self.shows_list, 24, channel, [], exc)
        try: self.list = sorted(self.list, key=itemgetter('name'))
        except: return
        index().showList(self.list)
        return self.list

    def hellenictv1(self):
        channel = 'UCE1CQmHM-oeCQoaW3JTxHcw'
        exc = ["LLE1CQmHM-oeCQoaW3JTxHcw", "PLzaa5cr7QTutgpyGJd5E0BA2XTCpgEZAd", "FLE1CQmHM-oeCQoaW3JTxHcw"]
        self.list = index().cache(self.shows_list, 24, channel, [], exc)
        index().showList(self.list)
        return self.list

    def cartoons_classics(self):
        self.worker = []

        def worker(id, inc, exc):
            self.worker.extend(index().cache(self.shows_list, 24, id, inc, exc))

        threads = []
        threads.append(Thread(worker, 'UCt5GCTKE_c2m2WBlHzsBX7g', [], []))
        threads.append(Thread(worker, 'UCv1QOKG5ORN6tv4eexNSfVw', [], []))
        threads.append(Thread(worker, 'UCJwVnA3GrTPGyqrS5twQlpg', [], ['PLStChvmvfcLCTv__R0DdRG95E0DC-wQik']))
        threads.append(Thread(worker, 'UCPzay-YCsO3TU-bxeYXnG0g', ['PL3420AA02720B05E5', 'PL147140D5904AFBE4', 'PLF191388E07E9E127', 'PL8F5C47492E11C109', 'PLAD759EE008F12C43', 'PLC3C3861A770162F5', 'PL0C994DFD3BCDAEDB', 'PLE3470893493CF5A8', 'PLD2C2707D06DA58DC', 'PL724AA3356D663CED', 'PLC34BCF01941BAC02'], []))
        threads.append(Thread(worker, 'UC3q9NJXBvzLkBKQ51R3WVBA', [], []))
        threads.append(Thread(worker, 'UCsKQX1G7XQO2a5nD9nrse-Q', [], []))
        [i.start() for i in threads]
        [i.join() for i in threads]

        try: self.list = sorted(self.worker, key=itemgetter('name'))
        except: return
        index().cartoonList(self.list)
        return self.list

    def cartoons_songs(self):
        channel = 'UCClAFTnbGditvz9_7_7eumw'
        self.list = index().cache(self.shows_list, 24, channel, [], ['PLB3126415BC8BCDE3'])
        try: self.list = sorted(self.list, key=itemgetter('name'))
        except: return
        index().cartoonList(self.list)
        return self.list

    def enikos(self):
        self.list = self.episodes_list('ENIKOS', self.enikos_link, '0', 'Greek', '0', 'ENIKOS')
        index().episodeList(self.list[:100])
        return self.list

    def shows_list(self, id, inc, exc):
        try:
            items = [] ; itemList = []
            url = self.playlists_link % id + self.key_link

            result = getUrl(url).result
            result = json.loads(result)
            items += result['items']

            for i in range(1, 4):
                next = url + '&pageToken=' + result['nextPageToken']
                result = getUrl(next).result
                result = json.loads(result)
                items += result['items']
        except:
            pass

        for item in items:
            try:
                name = item['snippet']['title']
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = item['id']
                if len(inc) > 0 and not url in inc: raise Exception()
                if url in exc: raise Exception()
                url = self.playlist_link % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = item['snippet']['thumbnails']['high']['url']
                if '/default.jpg' in image: raise Exception()
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                itemList.append({'name': name, 'title': name, 'url': url, 'image': image, 'year': '0', 'genre': 'Greek', 'type': 'tvshow', 'plot': '0'})
            except:
                pass

        return itemList

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            items = [] ; itemList = []
            url = url + self.key_link

            result = getUrl(url).result
            result = json.loads(result)
            items += result['items']

            for i in range(1, 4):
                next = url + '&pageToken=' + result['nextPageToken']
                result = getUrl(next).result
                result = json.loads(result)
                items += result['items']
        except:
            pass

        for item in items:
            try:
                name = item['snippet']['title']
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = item['snippet']['resourceId']['videoId']
                url = self.watch_link % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = item['snippet']['thumbnails']['high']['url']
                if '/default.jpg' in image: raise Exception()
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                itemList.append({'name': name, 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return itemList

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

class livestream:
    def http(self, url):
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request, timeout=2)
            response.close()
            response = response.info()
            return url
        except:
            return

    def hls(self, url):
        try:
            result = getUrl(url).result
            if "EXTM3U" in result: return url
        except:
            return

    def skai(self, url):
        try:
            root = 'http://www.skai.gr/ajax.aspx?m=NewModules.LookupMultimedia&mmid=/Root/TVLive'
            result = getUrl(root).result
            url = common.parseDOM(result, "File")[0]
            url = url.split('[')[-1].split(']')[0]
            url = 'https://www.youtube.com/watch?v=%s' % url
            url = 'http://translate.googleusercontent.com/translate_c?anno=2&hl=en&sl=mt&tl=en&u=%s' % url

            result = getUrl(url).result
            url = re.compile('"hlsvp" *: *"(.+?)"').findall(result)[0]
            url = urllib.unquote(url).replace('\\/', '/').replace('https://', 'http://')

            result = getUrl(url).result
            result = result.replace('\n','')
            url = re.compile('RESOLUTION *= *(\d*)x\d{1}.+?(http.+?\.m3u8)').findall(result)
            url = [(int(i[0]), i[1]) for i in url]
            url.sort()
            url = url[-1][1]
            return url
        except:
            return

    def euronews(self, url):
        try:
            url = 'http://gr.euronews.com'
            post = urllib.urlencode({'action': 'getHexaglobeUrl'})

            u = getUrl(url, post=post).result

            url = getUrl(u).result
            url = json.loads(url)
            try: url = url['primary']['gr']['hls']
            except: url = None

            if url == None:
                url = 'https://proxy-de.hide.me/go.php?b=20&u=%s' % urllib.quote_plus(u)
                url = getUrl(url).result
                url = json.loads(url)
                url = url['primary']['gr']['hls']

            return url
        except:
            return

    def lakatamia(self, url):
        try:
            urllib.urlretrieve('http://olympia.watchkodi.com/hellenic-tv/lakatamia.py', os.path.join(addonPath,'lakatamia.py'))
            import lakatamia; return lakatamia.resolve(url)
        except:
            return

    def madtv(self, url):
        try:
            result = getUrl(url, timeout=30).result
            url = common.parseDOM(result, "iframe", ret="src")
            url = [i for i in url if 'apps.' in i][0]
            if not url.startswith('http://'): url = url.replace('//', 'http://') 

            result = getUrl(url).result
            url = common.parseDOM(result, "iframe", ret="src")[0]
            url = url.split("?v=")[-1].split("/")[-1].split("?")[0].split("&")[0]
            url = 'https://www.youtube.com/watch?v=%s' % url
            url = 'http://translate.googleusercontent.com/translate_c?anno=2&hl=en&sl=mt&tl=en&u=%s' % url

            result = getUrl(url).result
            url = re.compile('"hlsvp" *: *"(.+?)"').findall(result)[0]
            url = urllib.unquote(url).replace('\\/', '/').replace('https://', 'http://')

            result = getUrl(url).result
            result = result.replace('\n','')
            url = re.compile('RESOLUTION *= *(\d*)x\d{1}.+?(http.+?\.m3u8)').findall(result)
            url = [(int(i[0]), i[1]) for i in url]
            url.sort()
            url = url[-1][1]
            return url
        except:
            return

    def kanalia_eu(self, url):
        try:
            u = 'http://proxy.cyberunlocker.com/browse.php?u=%s' % urllib.quote_plus(url)
            result = getUrl(u).result

            r = re.compile('streamer *: *"(.+?)"').findall(result)[0]
            p = re.compile('file *: *"(.+?)"').findall(result)[0]

            url = '%s playpath=%s pageUrl=%s live=1 timeout=10' % (r, p, url)
            return url
        except:
            return

    def gm(self, url):
        try:
            import random
            url = gm().movies_2(url)
            url = random.choice(url)['url']
            url = gm().resolve(url)
            return url
        except:
            return

    def videopublishing(self, url):
        try:
            url = 'http://static.videopublishing.com/?publish=%s' % url
            result = getUrl(url).result

            rtmp = common.parseDOM(result, "server")[0]
            playpath = common.parseDOM(result, "id")[0]

            url = 'rtmp://%s:1935/live playpath=%s live=1 timeout=10' % (rtmp, playpath)
            return url
        except:
            return

    def viiideo(self, url):
        try:
            result = getUrl(url).result
            result = result.replace('\n','')

            rtmp = re.compile("netConnectionUrl:\s+'(.+?)'").findall(result)[0]
            playpath = re.compile("clip:\s.+?url:\s+'(.+?)'").findall(result)[0]

            url = '%s playpath=%s live=1 timeout=10' % (rtmp, playpath)
            return url
        except:
            return

    def dailymotion(self, url):
        try:
            import commonresolvers
            url = commonresolvers.get(url).result
            return url
        except:
            return

    def livestream(self, url):
        try:
            name = url.split("/")[-1]
            url = 'http://x%sx.api.channel.livestream.com/3.0/getstream.json' % name
            result = getUrl(url).result
            isLive = str(result.find('isLive":true'))
            if isLive == '-1': return
            url = re.compile('"httpUrl".+?"(.+?)"').findall(result)[0]
            return url
        except:
            return

    def livestream_new(self, url):
        try:
            result = getUrl(url).result
            url = re.compile('"m3u8_url" *: *"(.+?)"').findall(result)
            url = [i for i in url if not i.endswith('m3u8')][-1]
            url = getUrl(url, output='geturl').result
            return url
        except:
            return

    def streamago(self, url):
        try:
            result = getUrl(url + '/xml/').result

            url = common.parseDOM(result, "path_hls")[0]
            url = url.split('[')[-1].split(']')[0]

            url = getUrl(url, output='geturl').result
            return url
        except:
            return

    def ustream(self, url):
        try:
            try:
                result = getUrl(url).result
                id = re.compile('ustream.tv/embed/(\d*)').findall(result)[0]
            except:
                id = url.split("/embed/")[-1]

            url = 'http://iphone-streaming.ustream.tv/ustreamVideo/%s/streams/live/playlist.m3u8' % id

            for i in range(1, 51):
                try:
                    result = getUrl(url).result
                    if "EXT-X-STREAM-INF" in result: return url
                    if not "EXTM3U" in result: return
                except:
                    return url
        except:
            return

    def veetle(self, url):
        try:
            akamaiProxy = os.path.join(addonPath,'akamaisecurehd.py')
            xbmc.executebuiltin('RunScript(%s)' % akamaiProxy)
            name = url.split("#")[-1]
            url = 'http://www.veetle.com/index.php/channel/ajaxStreamLocation/%s/flash' % name
            result = getUrl(url).result
            url = json.loads(result)
            url = base64.encodestring(url['payload']).replace('\n', '')
            url = 'http://127.0.0.1:64653/veetle/%s' % url
            return url
        except:
            return


main()
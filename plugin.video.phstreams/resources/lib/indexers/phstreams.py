# -*- coding: utf-8 -*-

'''
    Phoenix Add-on
    Copyright (C) 2016 Phoenix

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


import os,re,sys,urllib,urlparse,json,base64

from resources.lib.modules import cache
from resources.lib.modules import metacache
from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import workers
from resources.lib.modules import views



class indexer:
    def __init__(self):
        self.list = []


    def root(self):
        try:
            url = 'http://phoenixtv.offshorepastebin.com/main/main.xml'
            self.list = self.phoenix_list(url)
            self.addDirectory(self.list)
            return self.list
        except:
            pass


    def get(self, url):
        try:
            self.list = self.phoenix_list(url)
            self.worker()
            self.addDirectory(self.list)
            return self.list
        except:
            pass


    def developer(self):
        try:
            url = os.path.join(control.dataPath, 'testings.xml')
            f = control.openFile(url) ; result = f.read() ; f.close()
            self.list = self.phoenix_list('', result=result)
            self.addDirectory(self.list)
            return self.list
        except:
            pass


    def search(self):
        try:
            self.list = [{'name': 30702, 'action': 'addSearch'}]
            self.list += [{'name': 30703, 'action': 'delSearch'}]

            try:
                def search(): return
                query = cache.get(search, 600000000, table='rel_srch')

                for url in query:
                    try: self.list += [{'name': '%s...' % url, 'url': url, 'action': 'addSearch'}]
                    except: pass
            except:
                pass

            self.addDirectory(self.list)
            return self.list
        except:
            pass


    def delSearch(self):
        try:
            cache.clear('rel_srch')
            control.refresh()
        except:
            pass


    def addSearch(self, url=None):
        try:
            link = 'http://phoenixtv.offshorepastebin.com/main/search.xml'

            if (url == None or url == ''):
                keyboard = control.keyboard('', control.lang(30702).encode('utf-8'))
                keyboard.doModal()
                if not (keyboard.isConfirmed()): return
                url = keyboard.getText()

            if (url == None or url == ''): return

            def search(): return [url]
            query = cache.get(search, 600000000, table='rel_srch')
            def search(): return [x for y,x in enumerate((query + [url])) if x not in (query + [url])[:y]]
            cache.get(search, 0, table='rel_srch')

            links = client.request(link)
            links = re.findall('<link>(.+?)</link>', links)
            links = [i for i in links if str(i).startswith('http')]

            self.list = [] ; threads = [] 
            for link in links: threads.append(workers.Thread(self.phoenix_list, link))
            [i.start() for i in threads] ; [i.join() for i in threads]

            self.list = [i for i in self.list if url.lower() in i['name'].lower()]

            for i in self.list:
                try:
                    name = ''
                    if not i['vip'] in ['Phoenix TV']: name += '[B]%s[/B] | ' % i['vip'].upper()
                    name += i['name']
                    i.update({'name' : name})
                except:
                    pass

            self.addDirectory(self.list, mode=False)
        except:
            pass


    def phoenix_list(self, url, result=None):
        try:
            if result == None: result = cache.get(client.request, 0, url)

            try: r = base64.b64decode(result)
            except: r = ''
            if '</link>' in r: result = r

            result = str(result).replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
            result = self.account_filter(result)
            result = re.sub('<link></link>|<sublink></sublink>','', result)

            info = result.split('<item>')[0].split('<dir>')[0]

            try: vip = re.findall('<poster>(.+?)</poster>', info)[0]
            except: vip = '0'

            try: image = re.findall('<thumbnail>(.+?)</thumbnail>', info)[0]
            except: image = '0'

            try: fanart = re.findall('<fanart>(.+?)</fanart>', info)[0]
            except: fanart = '0'

            items = re.findall('((?:<item>.+?</item>|<dir>.+?</dir>|<plugin>.+?</plugin>|<info>.+?</info>|<name>[^<]+</name><link>[^<]+</link><thumbnail>[^<]+</thumbnail><mode>[^<]+</mode>|<name>[^<]+</name><link>[^<]+</link><thumbnail>[^<]+</thumbnail><date>[^<]+</date>))', result)
        except:
            return

        for item in items:
            try:
                name = item.split('<meta>')[0].split('<regex>')[0]
                try: name = re.findall('<title>(.+?)</title>', name)[0]
                except: name = re.findall('<name>(.+?)</name>', name)[0]
                if '<meta>' in name: raise Exception()

                try: date = re.findall('<date>(.+?)</date>', item)[0]
                except: date = ''
                if re.search(r'\d+', date): name += ' [COLOR red] Updated %s[/COLOR]' % date

                try: meta = re.findall('<meta>(.+?)</meta>', item)[0]
                except: meta = '0'

                try: url = re.findall('<link>(.+?)</link>', item)[0]
                except: url = '0'
                url = url.replace('>search<', '><preset>search</preset>%s<' % meta)
                url = '<preset>search</preset>%s' % meta if url == 'search' else url
                url = url.replace('>searchsd<', '><preset>searchsd</preset>%s<' % meta)
                url = '<preset>searchsd</preset>%s' % meta if url == 'searchsd' else url
                url = url.replace('<sublink></sublink>', '')

                if item.startswith('<item>'): action = 'play'
                elif item.startswith('<plugin>'): action = 'plugin'
                elif item.startswith('<info>') or url == '0': action = '0'
                else: action = 'directory'

                if action in ['directory', 'plugin']: folder = True
                else: folder = False

                try: image2 = re.findall('<thumbnail>(.+?)</thumbnail>', item)[0]
                except: image2 = image
                if not str(image2).lower().startswith('http'): image2 = '0'

                try: fanart2 = re.findall('<fanart>(.+?)</fanart>', item)[0]
                except: fanart2 = fanart
                if not str(fanart2).lower().startswith('http'): fanart2 = '0'

                try: content = re.findall('<content>(.+?)</content>', meta)[0]
                except: content = '0'
                if not content == '0': content += 's'

                try: imdb = re.findall('<imdb>(.+?)</imdb>', meta)[0]
                except: imdb = '0'

                try: tvdb = re.findall('<tvdb>(.+?)</tvdb>', meta)[0]
                except: tvdb = '0'

                try: tvshowtitle = re.findall('<tvshowtitle>(.+?)</tvshowtitle>', meta)[0]
                except: tvshowtitle = '0'

                try: title = re.findall('<title>(.+?)</title>', meta)[0]
                except: title = '0'

                if title == '0' and not tvshowtitle == '0': title = tvshowtitle

                try: year = re.findall('<year>(.+?)</year>', meta)[0]
                except: year = '0'

                try: premiered = re.findall('<premiered>(.+?)</premiered>', meta)[0]
                except: premiered = '0'

                try: season = re.findall('<season>(.+?)</season>', meta)[0]
                except: season = '0'

                try: episode = re.findall('<episode>(.+?)</episode>', meta)[0]
                except: episode = '0'

                self.list.append({'name': name, 'vip': vip, 'url': url, 'action': action, 'folder': folder, 'poster': image2, 'banner': '0', 'fanart': fanart2, 'content': content, 'imdb': imdb, 'tvdb': tvdb, 'tmdb': '0', 'title': title, 'originaltitle': title, 'tvshowtitle': tvshowtitle, 'year': year, 'premiered': premiered, 'season': season, 'episode': episode})
            except:
                pass

        return self.list


    def account_filter(self, result):
        if (control.setting('ustvnow_email') == '' or control.setting('ustvnow_pass') == ''):
            result = re.sub('http(?:s|)://(?:www\.|)ustvnow\.com/.+?<','<', result)

        if (control.setting('streamlive_user') == '' or control.setting('streamlive_pass') == ''):
            result = re.sub('http(?:s|)://(?:www\.|)streamlive\.to/.+?<','<', result)

        return result


    def worker(self):
        if not control.setting('metadata') == 'true': return

        self.imdb_info_link = 'http://www.omdbapi.com/?i=%s&plot=full&r=json'
        self.tvmaze_info_link = 'http://api.tvmaze.com/lookup/shows?thetvdb=%s'
        self.lang = 'en'

        self.meta = []
        total = len(self.list)

        for i in range(0, total): self.list[i].update({'metacache': False})
        self.list = metacache.fetch(self.list, self.lang)

        for r in range(0, total, 50):
            threads = []
            for i in range(r, r+50):
                if i <= total: threads.append(workers.Thread(self.movie_info, i))
                if i <= total: threads.append(workers.Thread(self.tv_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

        if len(self.meta) > 0: metacache.insert(self.meta)


    def movie_info(self, i):
        try:
            if self.list[i]['metacache'] == True: raise Exception()

            if not self.list[i]['content'] == 'movies': raise Exception()

            imdb = self.list[i]['imdb']
            if imdb == '0': raise Exception()

            url = self.imdb_info_link % imdb

            item = client.request(url, timeout='10')
            item = json.loads(item)

            if 'Error' in item and 'incorrect imdb' in item['Error'].lower():
                return self.meta.append({'imdb': imdb, 'tmdb': '0', 'tvdb': '0', 'lang': self.lang, 'item': {'code': '0'}})

            title = item['Title']
            title = title.encode('utf-8')
            if not title == '0': self.list[i].update({'title': title})

            year = item['Year']
            year = year.encode('utf-8')
            if not year == '0': self.list[i].update({'year': year})

            imdb = item['imdbID']
            if imdb == None or imdb == '' or imdb == 'N/A': imdb = '0'
            imdb = imdb.encode('utf-8')
            if not imdb == '0': self.list[i].update({'imdb': imdb, 'code': imdb})

            premiered = item['Released']
            if premiered == None or premiered == '' or premiered == 'N/A': premiered = '0'
            premiered = re.findall('(\d*) (.+?) (\d*)', premiered)
            try: premiered = '%s-%s-%s' % (premiered[0][2], {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}[premiered[0][1]], premiered[0][0])
            except: premiered = '0'
            premiered = premiered.encode('utf-8')
            if not premiered == '0': self.list[i].update({'premiered': premiered})

            genre = item['Genre']
            if genre == None or genre == '' or genre == 'N/A': genre = '0'
            genre = genre.replace(', ', ' / ')
            genre = genre.encode('utf-8')
            if not genre == '0': self.list[i].update({'genre': genre})

            duration = item['Runtime']
            if duration == None or duration == '' or duration == 'N/A': duration = '0'
            duration = re.sub('[^0-9]', '', str(duration))
            duration = duration.encode('utf-8')
            if not duration == '0': self.list[i].update({'duration': duration})

            rating = item['imdbRating']
            if rating == None or rating == '' or rating == 'N/A' or rating == '0.0': rating = '0'
            rating = rating.encode('utf-8')
            if not rating == '0': self.list[i].update({'rating': rating})

            votes = item['imdbVotes']
            try: votes = str(format(int(votes),',d'))
            except: pass
            if votes == None or votes == '' or votes == 'N/A': votes = '0'
            votes = votes.encode('utf-8')
            if not votes == '0': self.list[i].update({'votes': votes})

            mpaa = item['Rated']
            if mpaa == None or mpaa == '' or mpaa == 'N/A': mpaa = '0'
            mpaa = mpaa.encode('utf-8')
            if not mpaa == '0': self.list[i].update({'mpaa': mpaa})

            director = item['Director']
            if director == None or director == '' or director == 'N/A': director = '0'
            director = director.replace(', ', ' / ')
            director = re.sub(r'\(.*?\)', '', director)
            director = ' '.join(director.split())
            director = director.encode('utf-8')
            if not director == '0': self.list[i].update({'director': director})

            writer = item['Writer']
            if writer == None or writer == '' or writer == 'N/A': writer = '0'
            writer = writer.replace(', ', ' / ')
            writer = re.sub(r'\(.*?\)', '', writer)
            writer = ' '.join(writer.split())
            writer = writer.encode('utf-8')
            if not writer == '0': self.list[i].update({'writer': writer})

            cast = item['Actors']
            if cast == None or cast == '' or cast == 'N/A': cast = '0'
            cast = [x.strip() for x in cast.split(',') if not x == '']
            try: cast = [(x.encode('utf-8'), '') for x in cast]
            except: cast = []
            if cast == []: cast = '0'
            if not cast == '0': self.list[i].update({'cast': cast})

            plot = item['Plot']
            if plot == None or plot == '' or plot == 'N/A': plot = '0'
            plot = client.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')
            if not plot == '0': self.list[i].update({'plot': plot})

            self.meta.append({'imdb': imdb, 'tmdb': '0', 'tvdb': '0', 'lang': self.lang, 'item': {'title': title, 'year': year, 'code': imdb, 'imdb': imdb, 'premiered': premiered, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': writer, 'cast': cast, 'plot': plot}})
        except:
            pass


    def tv_info(self, i):
        try:
            if self.list[i]['metacache'] == True: raise Exception()

            if not self.list[i]['content'] in ['tvshows', 'seasons', 'episodes']: raise Exception()

            tvdb = self.list[i]['tvdb']
            if tvdb == '0': raise Exception()

            url = self.tvmaze_info_link % tvdb

            item = client.request(url, output='response', error=True, timeout='10')

            if item[0] == '404':
                return self.meta.append({'imdb': '0', 'tmdb': '0', 'tvdb': tvdb, 'lang': self.lang, 'item': {'code': '0'}})

            item = json.loads(item[1])

            tvshowtitle = item['name']
            tvshowtitle = tvshowtitle.encode('utf-8')
            if not tvshowtitle == '0': self.list[i].update({'tvshowtitle': tvshowtitle})

            year = item['premiered']
            year = re.findall('(\d{4})', year)[0]
            year = year.encode('utf-8')
            if not year == '0': self.list[i].update({'year': year})

            try: imdb = item['externals']['imdb']
            except: imdb = '0'
            if imdb == '' or imdb == None: imdb = '0'
            imdb = imdb.encode('utf-8')
            if self.list[i]['imdb'] == '0' and not imdb == '0': self.list[i].update({'imdb': imdb})

            studio = item['network']['name']
            if studio == '' or studio == None: studio = '0'
            studio = studio.encode('utf-8')
            if not studio == '0': self.list[i].update({'studio': studio})

            genre = item['genres']
            if genre == '' or genre == None or genre == []: genre = '0'
            genre = ' / '.join(genre)
            genre = genre.encode('utf-8')
            if not genre == '0': self.list[i].update({'genre': genre})

            try: duration = str(item['runtime'])
            except: duration = '0'
            if duration == '' or duration == None: duration = '0'
            duration = duration.encode('utf-8')
            if not duration == '0': self.list[i].update({'duration': duration})

            rating = str(item['rating']['average'])
            if rating == '' or rating == None: rating = '0'
            rating = rating.encode('utf-8')
            if not rating == '0': self.list[i].update({'rating': rating})

            plot = item['summary']
            if plot == '' or plot == None: plot = '0'
            plot = re.sub('\n|<.+?>|</.+?>|.+?#\d*:', '', plot)
            plot = plot.encode('utf-8')
            if not plot == '0': self.list[i].update({'plot': plot})

            self.meta.append({'imdb': imdb, 'tmdb': '0', 'tvdb': tvdb, 'lang': self.lang, 'item': {'tvshowtitle': tvshowtitle, 'year': year, 'code': imdb, 'imdb': imdb, 'tvdb': tvdb, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'plot': plot}})
        except:
            pass


    def addDirectory(self, items, mode=True):
        if items == None or len(items) == 0: return

        sysaddon = sys.argv[0]
        addonPoster = addonBanner = control.addonInfo('icon')
        addonFanart = control.addonInfo('fanart')

        try: devmode = True if 'testings.xml' in control.listDir(control.dataPath)[1] else False
        except: devmode = False

        if mode == True: mode = [i['content'] for i in items if 'content' in i]
        else: mode = []
        if 'movies' in mode: mode = 'movies'
        elif 'tvshows' in mode: mode = 'tvshows'
        elif 'seasons' in mode: mode = 'seasons'
        elif 'episodes' in mode: mode = 'episodes'
        else: mode = None

        for i in items:
            try:
                try: name = control.lang(int(i['name'])).encode('utf-8')
                except: name = i['name']

                url = '%s?action=%s' % (sysaddon, i['action'])
                try: url += '&url=%s' % urllib.quote_plus(i['url'])
                except: pass

                if i['action'] == 'plugin' and 'url' in i: url = i['url']
                if i['action'] == 'developer' and not devmode == True: raise Exception()

                poster = i['poster'] if 'poster' in i else '0'
                banner = i['banner'] if 'banner' in i else '0'
                fanart = i['fanart'] if 'fanart' in i else '0'
                if poster == '0': poster = addonPoster
                if banner == '0' and poster == '0': banner = addonBanner
                elif banner == '0': banner = poster

                content = i['content'] if 'content' in i else '0'
                replaceItems = False if content == '0' else True

                folder = i['folder'] if 'folder' in i else True

                meta = dict((k,v) for k, v in i.iteritems() if not v == '0')
                try: meta.update({'duration': str(int(meta['duration']) * 60)})
                except: pass

                cm = []

                if content in ['movies', 'tvshows']:
                    meta.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, urllib.quote_plus(name))})
                    cm.append((control.lang(30707).encode('utf-8'), 'RunPlugin(%s?action=trailer&name=%s)' % (sysaddon, urllib.quote_plus(name))))

                if content == 'movies':
                    cm.append((control.lang(30708).encode('utf-8'), 'XBMC.Action(Info)'))
                elif content in ['tvshows', 'seasons']:
                    cm.append((control.lang(30709).encode('utf-8'), 'XBMC.Action(Info)'))
                elif content == 'episodes':
                    cm.append((control.lang(30710).encode('utf-8'), 'XBMC.Action(Info)'))

                if content == 'movies':
                    try: dfile = '%s (%s)' % (data['title'], data['year'])
                    except: dfile = name
                    try: cm.append((control.lang(30722).encode('utf-8'), 'RunPlugin(%s?action=addDownload&name=%s&url=%s&image=%s)' % (sysaddon, urllib.quote_plus(dfile), urllib.quote_plus(i['url']), urllib.quote_plus(poster))))
                    except: pass
                elif content == 'episodes':
                    try: dfile = '%s S%02dE%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode']))
                    except: dfile = name
                    try: cm.append((control.lang(30722).encode('utf-8'), 'RunPlugin(%s?action=addDownload&name=%s&url=%s&image=%s)' % (sysaddon, urllib.quote_plus(dfile), urllib.quote_plus(i['url']), urllib.quote_plus(poster))))
                    except: pass

                if mode == 'movies':
                    cm.append((control.lang(30711).encode('utf-8'), 'RunPlugin(%s?action=addView&content=movies)' % sysaddon))
                elif mode == 'tvshows':
                    cm.append((control.lang(30712).encode('utf-8'), 'RunPlugin(%s?action=addView&content=tvshows)' % sysaddon))
                elif mode == 'seasons':
                    cm.append((control.lang(30713).encode('utf-8'), 'RunPlugin(%s?action=addView&content=seasons)' % sysaddon))
                elif mode == 'episodes':
                    cm.append((control.lang(30714).encode('utf-8'), 'RunPlugin(%s?action=addView&content=episodes)' % sysaddon))

                if devmode == True:
                    try: cm.append(('Open in browser', 'RunPlugin(%s?action=browser&url=%s)' % (sysaddon, urllib.quote_plus(i['url']))))
                    except: pass

                if replaceItems == True:
                    cm.append((control.lang(30725).encode('utf-8'), 'RunPlugin(%s?action=openSettings)' % sysaddon))


                item = control.item(label=name, iconImage=poster, thumbnailImage=poster)

                try: item.setArt({'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})
                except: pass

                if not fanart == '0':
                    item.setProperty('Fanart_Image', fanart)
                elif not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)

                item.setInfo(type='Video', infoLabels = meta)
                item.addContextMenuItems(cm, replaceItems=replaceItems)
                control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=folder)
            except:
                pass

        if not mode == None: control.content(int(sys.argv[1]), mode)
        control.directory(int(sys.argv[1]), cacheToDisc=True)
        if not mode == None: views.setView(mode)



class resolver:

    def play(self, url):
        try:
            url = self.get(url)
            if url == False: return

            url = self.process(url)
            if url == None: return control.infoDialog(control.lang(30705).encode('utf-8'))

            meta = {}
            for i in ['title', 'originaltitle', 'tvshowtitle', 'year', 'season', 'episode', 'genre', 'rating', 'votes', 'director', 'writer', 'plot', 'tagline']:
                try: meta[i] = control.infoLabel('listitem.%s' % i)
                except: pass
            meta = dict((k,v) for k, v in meta.iteritems() if not v == '')
            if not 'title' in meta: meta['title'] = control.infoLabel('listitem.label')
            icon = control.infoLabel('listitem.icon')
            title = meta['title']

            try:
                if not '.f4m'in url: raise Exception()
                ext = url.split('?')[0].split('&')[0].split('|')[0].rsplit('.')[-1].replace('/', '').lower()
                if not ext == 'f4m': raise Exception()
                from resources.lib.modules.f4mproxy.F4mProxy import f4mProxyHelper
                return f4mProxyHelper().playF4mLink(url, title, None, None, '', icon)
            except:
                pass

            item = control.item(path=url, iconImage=icon, thumbnailImage=icon)
            try: item.setArt({'icon': icon})
            except: pass
            item.setInfo(type='Video', infoLabels = meta)
            control.player.play(url, item)
        except:
            pass


    def browser(self, url):
        try:
            url = self.get(url)
            if url == False: return
            control.execute('RunPlugin(plugin://plugin.program.chrome.launcher/?url=%s&mode=showSite&stopPlayback=no)' % urllib.quote_plus(url))
        except:
            pass


    def link(self, url):
        try:
            url = self.get(url)
            if url == False: return
            url = self.process(url)
            if url == None: return control.infoDialog(control.lang(30705).encode('utf-8'))
            return url
        except:
            pass


    def get(self, url):
        try:
            items = re.compile('<sublink>(.+?)</sublink>').findall(url)
            if len(items) == 0: items = [url]
            items = [('Link %s' % (int(items.index(i))+1), i) for i in items]

            if len(items) == 1:
                url = items[0][1]
            else:
                select = control.selectDialog([i[0] for i in items], control.infoLabel('listitem.label'))
                if select == -1: return False
                else: url = items[select][1]

            return url
        except:
            pass


    def process(self, url, direct=True):
        try:
            dialog = None
            dialog = control.progressDialog
            dialog.create(control.addonInfo('name'), control.lang(30726).encode('utf-8'))
            dialog.update(0)
        except:
            pass


        try:
            if not '</regex>' in url: raise Exception()
            from resources.lib.modules import regex
            u = regex.resolve(url)
            if not u == None: url = u
        except:
            pass

        try:
            if not url.startswith('rtmp'): raise Exception()
            if len(re.compile('\s*timeout=(\d*)').findall(url)) == 0: url += ' timeout=10'
            try: dialog.close()
            except: pass
            return url
        except:
            pass

        try:
            if not '.m3u8'in url: raise Exception()
            ext = url.split('?')[0].split('&')[0].split('|')[0].rsplit('.')[-1].replace('/', '').lower()
            if not ext == 'm3u8': raise Exception()
            try: dialog.close()
            except: pass
            return url
        except:
            pass


        try:
            preset = re.findall('<preset>(.+?)</preset>', url)[0]

            title, year, imdb = re.findall('<title>(.+?)</title>', url)[0], re.findall('<year>(.+?)</year>', url)[0], re.findall('<imdb>(.+?)</imdb>', url)[0]

            try: tvdb, tvshowtitle, premiered, season, episode = re.findall('<tvdb>(.+?)</tvdb>', url)[0], re.findall('<tvshowtitle>(.+?)</tvshowtitle>', url)[0], re.findall('<premiered>(.+?)</premiered>', url)[0], re.findall('<season>(.+?)</season>', url)[0], re.findall('<episode>(.+?)</episode>', url)[0]
            except: tvdb = tvshowtitle = premiered = season = episode = None

            direct = False

            presetDict = ['primewire_mv_tv', 'watchfree_mv_tv', 'movie25_mv', 'watchseries_tv', 'dizigold_tv', 'dizilab_tv', 'ninemovies_mv_tv', 'onemovies_mv_tv', 'onlinedizi_tv', 'sezonlukdizi_tv', 'watch1080_mv', 'xmovies_mv']

            if preset == 'searchsd': presetDict = ['primewire_mv_tv', 'watchfree_mv_tv', 'movie25_mv', 'watchseries_tv']

            from resources.lib.sources import sources

            try: dialog.update(0, control.lang(30726).encode('utf-8'), control.lang(30731).encode('utf-8'))
            except: pass

            u = sources().getSources(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, presetDict=presetDict, progress=False, timeout=20)

            try: dialog.update(50, control.lang(30726).encode('utf-8'), control.lang(30731).encode('utf-8'))
            except: pass

            u = sources().sourcesDirect(u, progress=False)

            if not u == None:
                try: dialog.close()
                except: pass
                return u
        except:
            pass

        try:
            from resources.lib.sources import sources

            u = sources().getURISource(url)

            if not u == False: direct = False
            if u == None or u == False or u == []: raise Exception()

            try: dialog.update(50, control.lang(30726).encode('utf-8'), control.lang(30731).encode('utf-8'))
            except: pass

            u = sources().sourcesDirect(u, progress=False)

            if not u == None:
                try: dialog.close()
                except: pass
                return u
        except:
            pass

        try:
            if not '.google.com' in url: raise Exception()
            from resources.lib.modules import directstream
            u = directstream.google(url)[0]['url']
            try: dialog.close()
            except: pass
            return u
        except:
            pass

        try:
            import urlresolver

            try: hmf = urlresolver.HostedMediaFile(url=url, include_disabled=True, include_universal=False)
            except: hmf = urlresolver.HostedMediaFile(url=url)

            if hmf.valid_url() == False: raise Exception()

            direct = False ; u = hmf.resolve()
            if 'plugin://plugin.video.youtube' in u: raise Exception()

            if not u == False:
                try: dialog.close()
                except: pass
                return u
        except:
            pass


        try:
            try: headers = dict(urlparse.parse_qsl(url.rsplit('|', 1)[1]))
            except: headers = dict('')
            if not url.startswith('http'): raise Exception()
            result = client.request(url.split('|')[0], headers=headers, output='headers', timeout='20')
            if 'Content-Type' in result and not 'html' in result['Content-Type']: raise Exception()

            import liveresolver
            if liveresolver.isValid(url) == True: direct = False
            u = liveresolver.resolve(url)

            if not u == None:
                try: dialog.close()
                except: pass
                return u
        except:
            pass


        if direct == True: return url

        try: dialog.close()
        except: pass



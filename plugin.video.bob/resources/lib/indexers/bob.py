# -*- coding: utf-8 -*-

"""
    Bob Add-on

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
"""
import __builtin__
import base64
import hashlib
import json
import os
import random
import re
import sys
import urllib
import urlparse

import xbmc
import xbmcplugin

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

from resources.lib.modules import cache
from resources.lib.modules import metacache
from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import workers
from resources.lib.modules import views


def replace_url(url):
    if 'norestrictions.noobsandnerds.com' in url and not 'norestrictions.club/norestrictions.club' in url:
        url = url.replace('norestrictions.noobsandnerds.com', __builtin__.BOB_BASE_DOMAIN)
    elif 'www.norestrictions.club' in url and not 'www.norestrictions.club/norestrictions.club' in url and not 'norestrictions.club/norestrictions.club' in url:
        url = url.replace('www.norestrictions.club', __builtin__.BOB_BASE_DOMAIN)
    elif 'www.norestrictions.club/norestrictions.club' in url:
        url = url.replace('www.norestrictions.club/norestrictions.club', __builtin__.BOB_BASE_DOMAIN)
    elif 'norestrictions.club' in url and not 'norestrictions.club/norestrictions.club' in url:
        url = url.replace('norestrictions.club', __builtin__.BOB_BASE_DOMAIN)
    elif 'norestrictions.club/norestrictions.club' in url:
        url = url.replace('norestrictions.club/norestrictions.club', __builtin__.BOB_BASE_DOMAIN)
    return url


class Indexer:
    def __init__(self):
        self.list = []

    def get(self, url, result=None, uncached=False):
        try:
            self.list = self.bob_list(url, result, uncached)
            self.worker()
            self.add_directory(self.list, parent_url=url)
            return self.list
        except:
            pass

    def root(self):
        url = replace_url("http://www.norestrictions.club/main/main.xml")
        try:
            self.list = self.bob_list(url)
            from resources.lib.modules import favs
            you = "My"
            if control.setting('my_bob_name') == 'true':
                try:
                    HOME = xbmc.translatePath('special://home')
                    if xbmc.getInfoLabel('System.ProfileName') != "Master user":
                        you = xbmc.getInfoLabel('System.ProfileName')
                    elif xbmc.getCondVisibility('System.Platform.Windows') == True or xbmc.getCondVisibility(
                            'System.Platform.OSX') == True:
                        if "Users\\" in HOME:
                            proyou = str(HOME).split("Users\\")
                            preyou = str(proyou[1]).split("\\")
                            you = preyou[0]
                        else:
                            you = "My"
                    if "[COLOR" in you:
                        name = re.findall("\[COLOR=.+?\](.+?)\[/COLOR\]", you)[0]
                        you = re.sub("(\[COLOR=.+?\])(.+?)(\[/COLOR\])", '\\1{0}\\3'.format(name.capitalize() + "'s"),
                                     you)
                    elif you != "My":
                        you = you.capitalize() + "'s"
                except:
                    pass
            name = '%s Bob' % you
            self.list.insert(0, {'name': name, 'url': url, 'action': 'getfavorites', 'folder': True,
                                 'poster': "http://norestrictions.club/norestrictions.club/main/icons/my_bob.jpg"})
            self.worker()
            self.add_directory(self.list, parent_url=url)
            return self.list
        except:
            pass

    def getx(self, url):
        self.get('', url, uncached=True)

    def developer(self):
        try:
            url = os.path.join(control.dataPath, 'testings.xml')
            f = control.openFile(url)
            result = f.read()
            f.close()
            self.getx(result)
        except:
            pass

    def search(self):
        try:
            self.list = [{'name': 30702, 'action': 'add_search'}]
            self.list += [{'name': 30703, 'action': 'delete_search'}]

            try:
                def search():
                    return

                query = cache.get(search, 600000000, table='rel_srch')

                for url in query:
                    try:
                        self.list += [{'name': '%s...' % url, 'url': url, 'action': 'add_search'}]
                    except:
                        pass
            except:
                pass
            self.add_directory(self.list)
            return self.list
        except:
            pass

    @staticmethod
    def delete_search():
        try:
            cache.clear('rel_srch')
            control.refresh()
        except:
            pass

    def add_search(self, url=None):
        try:
            link = replace_url('http://www.norestrictions.club/main/search.xml')

            if url is None or url == '':
                keyboard = control.keyboard('', control.lang(30702).encode('utf-8'))
                keyboard.doModal()
                if not (keyboard.isConfirmed()):
                    return
                url = keyboard.getText()

            if url is None or url == '':
                return

            def search():
                return [url]

            query = cache.get(search, 600000000, table='rel_srch')

            def search():
                return [x for y, x in enumerate((query + [url])) if x not in (query + [url])[:y]]

            cache.get(search, 0, table='rel_srch')

            links = client.request(link)
            links = re.findall('<link>(.+?)</link>', links)
            links = [replace_url(i) for i in links if str(i).startswith('http')]

            self.list = []
            threads = []
            for link in links:
                threads.append(workers.Thread(self.bob_list, link))
            [i.start() for i in threads]
            [i.join() for i in threads]

            self.list = [i for i in self.list if url.lower() in i['name'].lower().translate(None, '\/:*?"\'<>|!,')]

            for i in self.list:
                try:
                    name = ''
                    if not i['vip'].lower() in ['BOB'.lower()]:
                        name += '[B]%s[/B] | ' % i['vip'].upper()
                    name += i['name']
                    i.update({'name': name})
                except:
                    pass

            self.add_directory(self.list, mode=False)
        except:
            pass

    def get_xml(self, url, uncached=False):
        import xbmc
        import xbmcaddon
        import xbmcvfs
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        import os
        import requests
        import time

        now = int(time.time())
        cachebase = url.replace(__builtin__.BOB_BASE_DOMAIN + "/", "").replace("http://", "")
        xbmcvfs.mkdir(xbmc.translatePath(xbmcaddon.Addon("plugin.video.bob").getAddonInfo('profile')))
        cache_location = os.path.join(
            xbmc.translatePath(xbmcaddon.Addon("plugin.video.bob").getAddonInfo('profile')).decode('utf-8'),
            'url_cache.db')
        try:
            dbcon = database.connect(cache_location)
            dbcur = dbcon.cursor()
            try:
                dbcur.execute("SELECT * FROM version")
                match = dbcur.fetchone()
                if match[0] == "0.5.4":
                    dbcur.execute("DELETE FROM version WHERE version = '%s'" % ("0.5.4"))
                    dbcur.execute("INSERT INTO version Values ('0.5.5')")
                    dbcur.execute('ALTER TABLE xml ADD COLUMN created INTEGER DEFAULT 0')
                    dbcon.commit()
            except:
                dbcur.execute("CREATE TABLE version (""version TEXT)")
                dbcur.execute("INSERT INTO version Values ('0.5.5')")
                dbcon.commit()
            dbcur.execute(
                "CREATE TABLE IF NOT EXISTS xml (url TEXT, xml TEXT, last_modified TEXT, created INTEGER DEFAULT 0, UNIQUE(url, last_modified));")
            if not uncached:
                try:
                    dbcur.execute(
                        "SELECT * FROM xml WHERE url = '%s'" % (cachebase))
                    match = dbcur.fetchone()
                    if match:
                        return (match[1], match[3])
                except:
                    pass

            try:
                request = requests.get(url, timeout=6)
            except:
                request = None
            try:
                last_modified = request.headers['Last-Modified']
            except:
                last_modified = ""
            if last_modified:
                try:
                    dbcur.execute(
                        "SELECT * FROM xml WHERE last_modified = '%s' and url = '%s'" % (last_modified, cachebase))
                    match = dbcur.fetchone()
                    if match:
                        if match[2] == last_modified:
                            dbcur.execute(
                                "UPDATE xml set created = %s WHERE last_modified = '%s' and url = '%s'" % (
                                    now, last_modified, cachebase))
                            dbcon.commit()
                            return (match[1], match[3])
                except:
                    pass
            else:
                try:
                    dbcur.execute(
                        "SELECT * FROM xml WHERE url = '%s'" % (cachebase))
                    match = dbcur.fetchone()
                    if match:
                        return (match[1], match[3])
                except:
                    pass
            if not last_modified:
                request = requests.get(url)
                last_modified = request.headers['Last-Modified']
            xml = request.content
            try:
                dbcur.execute("DELETE FROM xml WHERE url = '%s'" % (cachebase))
            except:
                pass
            xml = xml.replace("\n", "").replace("##", "").replace('\t', "")
            try:
                dbcur.execute("INSERT INTO xml Values (?, ?, ?, ?)",
                              (cachebase, xml.encode("utf-8", "ignore"), last_modified, now))
            except:
                dbcur.execute("INSERT INTO xml Values (?, ?, ?, ?)", (cachebase, xml.decode("utf-8"), last_modified, now))
            dbcon.commit()
            return (xml, now)
        except:
            return ("", now)

    @staticmethod
    def bob_get_tag_content(collection, tag, default):
        try:
            result = re.findall('<%s>(.+?)</%s>' % (tag, tag), collection)[0]
            return result
        except:
            return default

    def bob_list(self, url, result=None, uncached=False):
        import time
        now = int(time.time())
        try:
            try:
                if not "sport_acesoplisting" == url:
                    raise Exception()
                from resources.lib.sources import sports
                xml = sports.get_acesoplisting()
                return self.getx(xml)
            except:
                pass

            try:
                if not "sport_nhl_games" in url:
                    raise Exception()
                from resources.lib.sources import sports
                game_date = url.replace("sport_nhl_games(", "")[:-1]
                if "sport" in game_date:
                    game_date = ""
                xml = sports.get_nhl_games(game_date)
                return self.getx(xml)
            except:
                pass

            try:
                if not "nhl_home_away(" in url:
                    raise Exception()
                from resources.lib.sources import sports
                fargs = url.replace("nhl_home_away(", "")[:-1].split(",")
                xml = sports.get_nhl_home_away(fargs[0], fargs[1], fargs[2], fargs[3])
                return self.getx(xml)
            except:
                pass

            try:
                if not url.startswith("sport_hockeyrecaps"):
                    raise Exception()
                from resources.lib.sources import sports
                page = url.strip()[18:]
                if page == "":
                    page = "1"
                xml = sports.get_hockey_recaps(page)
                return self.getx(xml)
            except:
                pass

            try:
                if not "sport_nfl_games" in url:
                    raise Exception()
                from resources.lib.sources import sports
                fargs = url.replace("sport_nfl_games(", "")[:-1]
                if "sport" in fargs:
                    xml = sports.get_nfl_games()
                else:
                    fargs = fargs.split(",")
                    if len(fargs) == 2:
                        xml = sports.get_nfl_games(fargs[0], fargs[1])
                    else:
                        xml = ""
                return self.getx(xml)
            except:
                pass

            try:
                if not "sport_nfl_get_game(" in url:
                    raise Exception()
                from resources.lib.sources import sports
                farg = url.replace("sport_nfl_get_game(", "")[:-1]
                xml = sports.get_nfl_game(farg)
                return self.getx(xml)
            except:
                pass

            try:
                if not "sport_condensed_nfl_games" in url:
                    raise Exception()
                from resources.lib.sources import sports
                fargs = url.replace("sport_condensed_nfl_games(", "")[:-1]
                if "sport" in fargs:
                    xml = sports.get_condensed_nfl_games()
                else:
                    fargs = fargs.split(",")
                    if len(fargs) == 2:
                        xml = sports.get_condensed_nfl_games(fargs[0], fargs[1])
                    else:
                        xml = ""
                return self.getx(xml)
            except:
                pass

            try:
                if not "sport_condensed_nfl_get_game(" in url:
                    raise Exception()
                from resources.lib.sources import sports
                farg = url.replace("sport_condensed_nfl_get_game(", "")[:-1]
                xml = sports.get_condensed_nfl_game(farg)
                return self.getx(xml)
            except:
                pass

            try:
                if not url.startswith("message("):
                    raise Exception()
                message = url.replace("message(", "")[:-1]
                control.dialog.ok("Message", message)
                return
            except:
                pass

            try:
                if not url.startswith("bobfile://"):
                    raise Exception()
                import xbmcvfs
                file_name = urllib.unquote(url[10:])
                file = xbmcvfs.File(os.path.join(control.dataPath, file_name))
                xml = file.read()
                file.close()
                return self.getx(xml)
            except:
                pass

            original_url = url
            created = 0
            if result is None:
                result, created = self.get_xml(url, uncached)
                try:
                    created = int(created)
                except:
                    created = 0
                    # result = cache.get(client.request, 0.1, url)

            if result.strip().startswith('#EXTM3U') and '#EXTINF' in result:
                result = re.compile('#EXTINF:.+?\,(.+?)\n(.+?)\n', re.MULTILINE | re.DOTALL).findall(result)
                result = ['<item><title>%s</title><link>%s</link></item>' % (i[0], i[1]) for i in result]
                result = ''.join(result)
            try:
                r = base64.b64decode(result)
            except:
                r = ''
            if '</link>' in r:
                result = r
            try:
                result = str(result)
            except:
                result = result.encode("utf-8")

            result = self.account_filter(result)

            info = result.split('<item>')[0].split('<dir>')[0]

            vip = self.bob_get_tag_content(info, 'poster', '0')
            image = replace_url(self.bob_get_tag_content(info, 'thumbnail', '0'))

            fanart = replace_url(self.bob_get_tag_content(info, 'fanart', '0'))

            try:
                cache_time = int(self.bob_get_tag_content(info, 'cache', 0))
                if (not uncached) and (cache_time > 0 or created == 0):
                    if created == 0 or now > created + cache_time:
                        uncached_xml, _ = self.get_xml(url, True)
                        return self.bob_list("", uncached_xml, True)
                elif (not uncached) and cache_time == 0:
                    uncached_xml, _ = self.get_xml(url, True)
                    return self.bob_list("", uncached_xml, True)
            except:
                pass

            items = re.compile(
                '((?:<item>.+?</item>|<dir>.+?</dir>|<plugin>.+?</plugin>|<info>.+?</info>|'
                '<name>[^<]+</name><link>[^<]+</link><thumbnail>[^<]+</thumbnail><mode>[^<]+</mode>|'
                '<name>[^<]+</name><link>[^<]+</link><thumbnail>[^<]+</thumbnail><date>[^<]+</date>))',
                re.MULTILINE | re.DOTALL).findall(result)
        except:
            return

        added_all_episodes = False
        for item in items:
            try:
                regex = re.compile('(<regex>.+?</regex>)', re.MULTILINE | re.DOTALL).findall(item)
                regex = ''.join(regex)
                regex = urllib.quote_plus(regex)

                item = item.replace('\r', '').replace('\n', '').replace('\t', '').replace('&nbsp;', '')
                item = re.sub('<link></link>|<sublink></sublink>', '', item)

                name = item.split('<meta>')[0].split('<regex>')[0]
                try:
                    name = re.findall('<title>(.+?)</title>', name)[0]
                except:
                    name = re.findall('<name>(.+?)</name>', name)[0]
                if '<meta>' in name:
                    raise Exception()

                date = self.bob_get_tag_content(item, 'date', '')
                if re.search(r'\d+', date):
                    name += ' [COLOR red] Updated %s[/COLOR]' % date
                meta = self.bob_get_tag_content(item, 'meta', '0')
                url = self.bob_get_tag_content(item, 'link', '0')

                url = url.replace('>search<', '><preset>search</preset>%s<' % meta)
                url = '<preset>search</preset>%s' % meta if url == 'search' else url
                url = url.replace('>searchsd<', '><preset>searchsd</preset>%s<' % meta)
                url = '<preset>searchsd</preset>%s' % meta if url == 'searchsd' else url
                url = url.replace('<sublink></sublink>', '')
                url += regex

                if item.startswith('<item>'):
                    action = 'play'
                elif item.startswith('<plugin>'):
                    action = 'plugin'
                elif item.startswith('<xdir>'):
                    action = 'xdirectory'
                elif item.startswith('<info>') or url == '0':
                    action = '0'
                else:
                    action = 'directory'

                if action in ['directory', 'xdirectory', 'plugin']:
                    folder = True
                elif not regex == '':
                    folder = True
                else:
                    folder = False

                image2 = replace_url(self.bob_get_tag_content(item, 'thumbnail', image))
                if not str(image2).lower().startswith('http'):
                    image2 = '0'

                fanart2 = replace_url(self.bob_get_tag_content(item, 'fanart', fanart))
                if not str(fanart2).lower().startswith('http'):
                    fanart2 = '0'

                content = self.bob_get_tag_content(meta, 'content', '0')
                if not content == '0':
                    content += 's'

                imdb = self.bob_get_tag_content(meta, 'imdb', '0')
                tvdb = self.bob_get_tag_content(meta, 'tvdb', '0')
                tvshowtitle = self.bob_get_tag_content(meta, 'tvshowtitle', '0')
                title = self.bob_get_tag_content(meta, 'title', '0')
                if title == '0' and not tvshowtitle == '0':
                    title = tvshowtitle

                year = self.bob_get_tag_content(meta, 'year', '0')
                premiered = self.bob_get_tag_content(meta, 'premiered', '0')
                season = self.bob_get_tag_content(meta, 'season', '0')
                episode = self.bob_get_tag_content(meta, 'episode', '0')

                summary = self.bob_get_tag_content(meta, 'summary', '')

                if season is not '0' and episode is '0' and added_all_episodes is False:
                    self.list.append(
                        {'name': "All Episodes", 'vip': vip,
                         'url': original_url,
                         'action': 'get_all_episodes',
                         'folder': folder, 'poster': image2,
                         'banner': '0', 'fanart': fanart2, 'content': content, 'imdb': imdb, 'tvdb': tvdb, 'tmdb': '0',
                         'title': title, 'originaltitle': title, 'tvshowtitle': tvshowtitle, 'year': year,
                         'premiered': premiered, 'season': season, 'episode': episode, 'summary': summary})
                    added_all_episodes = True

                self.list.append(
                    {'name': name, 'vip': vip, 'url': url, 'action': action, 'folder': folder, 'poster': image2,
                     'banner': '0', 'fanart': fanart2, 'content': content, 'imdb': imdb, 'tvdb': tvdb, 'tmdb': '0',
                     'title': title, 'originaltitle': title, 'tvshowtitle': tvshowtitle, 'year': year,
                     'premiered': premiered, 'season': season, 'episode': episode, 'summary': summary})
            except:
                pass

        return self.list

    def get_all_episodes(self, url):
        result = cache.get(client.request, 0.1, url)

        if result.strip().startswith('#EXTM3U') and '#EXTINF' in result:
            result = re.compile('#EXTINF:.+?\,(.+?)\n(.+?)\n', re.MULTILINE | re.DOTALL).findall(result)
            result = ['<item><title>%s</title><link>%s</link></item>' % (i[0], i[1]) for i in result]
            result = ''.join(result)

        try:
            r = base64.b64decode(result)
        except:
            r = ''
        if '</link>' in r:
            result = r

        result = str(result)

        result = self.account_filter(result)

        items = re.compile(
            '((?:<item>.+?</item>|<dir>.+?</dir>|<plugin>.+?</plugin>|<info>.+?</info>|'
            '<name>[^<]+</name><link>[^<]+</link><thumbnail>[^<]+</thumbnail><mode>[^<]+</mode>|'
            '<name>[^<]+</name><link>[^<]+</link><thumbnail>[^<]+</thumbnail><date>[^<]+</date>))',
            re.MULTILINE | re.DOTALL).findall(result)

        result_list = []
        for item in items:
            url = self.bob_get_tag_content(item, 'link', '0')

            if url is not '0':
                result_list.extend(self.bob_list(replace_url(url)))
            self.list = []
        self.list = result_list
        self.worker()
        self.add_directory(self.list)
        return self.list

    @staticmethod
    def account_filter(result):
        if control.setting('ustvnow_email') == '' or control.setting('ustvnow_pass') == '':
            result = re.sub('http(?:s|)://(?:www\.|)ustvnow\.com/.+?<', '<', result)

        if control.setting('streamlive_user') == '' or control.setting('streamlive_pass') == '':
            result = re.sub('http(?:s|)://(?:www\.|)streamlive\.to/.+?<', '<', result)

        return result

    def worker(self):
        if not control.setting('metadata') == 'true':
            return

        self.imdb_info_link = 'http://www.omdbapi.com/?i=%s&plot=full&r=json'
        self.tvmaze_info_link = 'http://api.tvmaze.com/lookup/shows?thetvdb=%s'
        self.tvmaze_episode_info_link = 'http://api.tvmaze.com/shows/%s/episodebynumber?season=%s&number=%s'
        self.lang = 'en'

        self.meta = []
        total = len(self.list)

        for i in range(0, total):
            self.list[i].update({'metacache': False})
            self.list[i].update({'episode_metacache': False})
        self.list = metacache.fetch(self.list, self.lang)
        self.list = metacache.fetch_episodes(self.list, self.lang)

        for r in range(0, total, 50):
            threads = []
            for i in range(r, r + 50):
                if i <= total:
                    threads.append(workers.Thread(self.movie_info, i))
                if i <= total:
                    threads.append(workers.Thread(self.tv_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

        if len(self.meta) > 0:
            metacache.insert(self.meta)

    def movie_info(self, i):
        try:
            if self.list[i]['metacache'] is True:
                raise Exception()

            if not self.list[i]['content'] == 'movies':
                raise Exception()

            imdb = self.list[i]['imdb']
            if imdb == '0':
                raise Exception()

            url = self.imdb_info_link % imdb

            item = client.request(url, timeout='10')
            item = json.loads(item)

            if 'Error' in item and 'incorrect imdb' in item['Error'].lower():
                return self.meta.append(
                    {'imdb': imdb, 'tmdb': '0', 'tvdb': '0', 'lang': self.lang, 'item': {'code': '0'}})

            title = item['Title']
            title = title.encode('utf-8')
            if not title == '0':
                self.list[i].update({'title': title})

            year = item['Year']
            year = year.encode('utf-8')
            if not year == '0':
                self.list[i].update({'year': year})

            imdb = item['imdbID']
            if imdb is None or imdb == '' or imdb == 'N/A':
                imdb = '0'
            imdb = imdb.encode('utf-8')
            if not imdb == '0':
                self.list[i].update({'imdb': imdb, 'code': imdb})

            premiered = item['Released']
            if premiered is None or premiered == '' or premiered == 'N/A':
                premiered = '0'
            premiered = re.findall('(\d*) (.+?) (\d*)', premiered)
            try:
                premiered = '%s-%s-%s' % (premiered[0][2],
                                          {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
                                           'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11',
                                           'Dec': '12'}[premiered[0][1]], premiered[0][0])
            except:
                premiered = '0'
            premiered = premiered.encode('utf-8')
            if not premiered == '0':
                self.list[i].update({'premiered': premiered})

            genre = item['Genre']
            if genre is None or genre == '' or genre == 'N/A':
                genre = '0'
            genre = genre.replace(', ', ' / ')
            genre = genre.encode('utf-8')
            if not genre == '0':
                self.list[i].update({'genre': genre})

            duration = item['Runtime']
            if duration is None or duration == '' or duration == 'N/A':
                duration = '0'
            duration = re.sub('[^0-9]', '', str(duration))
            duration = duration.encode('utf-8')
            if not duration == '0':
                self.list[i].update({'duration': duration})

            rating = item['imdbRating']
            if rating is None or rating == '' or rating == 'N/A' or rating == '0.0':
                rating = '0'
            rating = rating.encode('utf-8')
            if not rating == '0':
                self.list[i].update({'rating': rating})

            votes = item['imdbVotes']
            try:
                votes = str(format(int(votes), ',d'))
            except:
                pass
            if votes is None or votes == '' or votes == 'N/A':
                votes = '0'
            votes = votes.encode('utf-8')
            if not votes == '0':
                self.list[i].update({'votes': votes})

            mpaa = item['Rated']
            if mpaa is None or mpaa == '' or mpaa == 'N/A':
                mpaa = '0'
            mpaa = mpaa.encode('utf-8')
            if not mpaa == '0':
                self.list[i].update({'mpaa': mpaa})

            director = item['Director']
            if director is None or director == '' or director == 'N/A':
                director = '0'
            director = director.replace(', ', ' / ')
            director = re.sub(r'\(.*?\)', '', director)
            director = ' '.join(director.split())
            director = director.encode('utf-8')
            if not director == '0':
                self.list[i].update({'director': director})

            writer = item['Writer']
            if writer is None or writer == '' or writer == 'N/A':
                writer = '0'
            writer = writer.replace(', ', ' / ')
            writer = re.sub(r'\(.*?\)', '', writer)
            writer = ' '.join(writer.split())
            writer = writer.encode('utf-8')
            if not writer == '0':
                self.list[i].update({'writer': writer})

            cast = item['Actors']
            if cast is None or cast == '' or cast == 'N/A':
                cast = '0'
            cast = [x.strip() for x in cast.split(',') if not x == '']
            try:
                cast = [(x.encode('utf-8'), '') for x in cast]
            except:
                cast = []
            if not cast:
                cast = '0'
            if not cast == '0':
                self.list[i].update({'cast': cast})

            plot = self.list[i]['summary']
            if plot == '':
                plot = item['Plot']
            if plot is None or plot == '' or plot == 'N/A':
                plot = '0'
            plot = client.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')
            if not plot == '0':
                self.list[i].update({'plot': plot})

            self.meta.append({'imdb': imdb, 'tmdb': '0', 'tvdb': '0', 'lang': self.lang,
                              'item': {'title': title, 'year': year, 'code': imdb, 'imdb': imdb, 'premiered': premiered,
                                       'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes,
                                       'mpaa': mpaa, 'director': director, 'writer': writer, 'cast': cast,
                                       'plot': plot, 'playcount': '0'}})
        except:
            pass

    def tv_info(self, i):
        try:
            if not self.list[i]['content'] in ['tvshows', 'seasons', 'episodes']:
                raise Exception()

            if self.list[i]['metacache'] is True and self.list[i]['content'] != 'episodes':
                raise Exception()

            if self.list[i]['episode_metacache'] is True or (
                            int(self.list[i]['episode']) == 0 and int(self.list[i]['season']) != 0):
                raise Exception()

            tvdb = self.list[i]['tvdb']
            if tvdb == '0':
                raise Exception()

            url = self.tvmaze_info_link % tvdb

            item = client.request(url, output='response', error=True, timeout='10')

            if item[0] == '404':
                return self.meta.append(
                    {'imdb': '0', 'tmdb': '0', 'tvdb': tvdb, 'lang': self.lang, 'item': {'code': '0'}})

            item = json.loads(item)

            tvshowtitle = item['name']
            tvshowtitle = tvshowtitle.encode('utf-8')
            if not tvshowtitle == '0':
                self.list[i].update({'tvshowtitle': tvshowtitle})

            year = item['premiered']
            year = re.findall('(\d{4})', year)[0]
            year = year.encode('utf-8')
            if not year == '0':
                self.list[i].update({'year': year})

            try:
                imdb = item['externals']['imdb']
            except:
                imdb = '0'
            if imdb == '' or imdb is None:
                imdb = '0'
            imdb = imdb.encode('utf-8')
            if self.list[i]['imdb'] == '0' and not imdb == '0':
                self.list[i].update({'imdb': imdb})

            studio = item['network']['name']
            if studio == '' or studio is None:
                studio = '0'
            studio = studio.encode('utf-8')
            if not studio == '0':
                self.list[i].update({'studio': studio})

            genre = item['genres']
            if genre == '' or genre is None or genre == []:
                genre = '0'
            genre = ' / '.join(genre)
            genre = genre.encode('utf-8')
            if not genre == '0':
                self.list[i].update({'genre': genre})

            try:
                duration = str(item['runtime'])
            except:
                duration = '0'
            if duration == '' or duration is None:
                duration = '0'
            duration = duration.encode('utf-8')
            if not duration == '0':
                self.list[i].update({'duration': duration})

            rating = str(item['rating']['average'])
            if rating == '' or rating is None:
                rating = '0'
            rating = rating.encode('utf-8')
            if not rating == '0':
                self.list[i].update({'rating': rating})

            plot = self.list[i]['summary']
            if plot == '':
                plot = item['summary']
            if plot == '' or plot is None:
                plot = '0'
            plot = re.sub('\n|<.+?>|</.+?>|.+?#\d*:', '', plot)
            plot = plot.encode('utf-8')
            if not plot == '0':
                self.list[i].update({'plot': plot})

            if self.list[i]['content'] == 'episodes':
                url = self.tvmaze_episode_info_link % (item['id'], self.list[i]['season'], self.list[i]['episode'])

                item = client.request(url, output='response', error=True, timeout='10')
                item = json.loads(item)
                episode_plot = item["summary"]
                if episode_plot == '' or episode_plot is None:
                    episode_plot = '0'
                else:
                    episode_plot = re.sub('\n|<.+?>|</.+?>|.+?#\d*:', '', episode_plot)
                episode_plot = episode_plot.encode('utf-8')
                if not episode_plot == '0':
                    self.list[i].update({'plot': episode_plot})
                    metacache.insert_episode([
                        {'imdb': imdb, 'tmdb': '0', 'tvdb': tvdb, 'lang': self.lang, 'season': self.list[i]['season'],
                         'episode': self.list[i]['episode'],
                         'item': {'tvshowtitle': tvshowtitle, 'year': year, 'code': imdb, 'imdb': imdb,
                                  'tvdb': tvdb, 'studio': studio, 'genre': genre, 'duration': duration,
                                  'rating': rating, 'plot': episode_plot, 'playcount': '0'}}])

            self.meta.append({'imdb': imdb, 'tmdb': '0', 'tvdb': tvdb, 'lang': self.lang,
                              'item': {'tvshowtitle': tvshowtitle, 'year': year, 'code': imdb, 'imdb': imdb,
                                       'tvdb': tvdb, 'studio': studio, 'genre': genre, 'duration': duration,
                                       'rating': rating, 'plot': plot, 'playcount': '0'}})
        except:
            pass

    def add_directory(self, items, mode=True, parent_url=None):
        if items is None or len(items) == 0:
            return

        you = "My"
        if control.setting('my_bob_name') == 'true':
            try:
                HOME = xbmc.translatePath('special://home')
                if xbmc.getInfoLabel('System.ProfileName') != "Master user":
                    you = xbmc.getInfoLabel('System.ProfileName')
                elif xbmc.getCondVisibility('System.Platform.Windows') == True or xbmc.getCondVisibility(
                        'System.Platform.OSX') == True:
                    if "Users\\" in HOME:
                        proyou = str(HOME).split("Users\\")
                        preyou = str(proyou[1]).split("\\")
                        you = preyou[0]
                    else:
                        you = "My"
                if "[COLOR" in you:
                    name = re.findall("\[COLOR=.+?\](.+?)\[/COLOR\]", you)[0]
                    you = re.sub("(\[COLOR=.+?\])(.+?)(\[/COLOR\])", '\\1{0}\\3'.format(name.capitalize() + "'s"), you)
                elif you != "My":
                    you = you.capitalize() + "'s"
            except:
                pass
        fave_name = '%s Bob' % you

        system_addon = sys.argv[0]
        addon_poster = addon_banner = control.addonInfo('icon')
        addon_fanart = control.addonInfo('fanart')

        try:
            devmode = True if 'testings.xml' in control.listDir(control.dataPath)[1] else False
        except:
            devmode = False

        if mode is True:
            mode = [i['content'] for i in items if 'content' in i]
        else:
            mode = []
        for item in mode:
            item.replace("-favs", "")
        if 'movies' in mode:
            mode = 'movies'
        elif 'tvshows' in mode:
            mode = 'tvshows'
        elif 'seasons' in mode:
            mode = 'seasons'
        elif 'episodes' in mode:
            mode = 'episodes'
        elif 'albums' in mode:
            mode = 'albums'
        elif 'artists' in mode:
            mode = 'artists'
        elif 'boxsets' in mode:
            mode = 'boxsets'
        else:
            mode = None

        for i in items:
            try:
                try:
                    name = control.lang(int(i['name'])).encode('utf-8')
                except:
                    name = i['name']

                url = '%s?action=%s' % (system_addon, i['action'])
                try:
                    url += '&url=%s' % urllib.quote_plus(
                        replace_url(i['url']))
                except:
                    pass
                try:
                    url += '&content=%s' % urllib.quote_plus(i['content'])
                except:
                    pass

                if i['action'] == 'plugin' and 'url' in i:
                    url = i['url']

                try:
                    devurl = dict(urlparse.parse_qsl(urlparse.urlparse(url).query))['action']
                except:
                    devurl = None
                if devurl == 'developer' and devmode is not True:
                    raise Exception()

                poster = i['poster'] if 'poster' in i else '0'
                banner = i['banner'] if 'banner' in i else '0'
                fanart = i['fanart'] if 'fanart' in i else '0'
                if poster == '0':
                    poster = addon_poster
                if banner == '0' and poster == '0':
                    banner = addon_banner
                elif banner == '0':
                    banner = poster

                content = i['content'] if 'content' in i else '0'

                folder = i['folder'] if 'folder' in i else True

                meta = dict((k, v) for k, v in i.iteritems() if not v == '0')
                try:
                    meta.update({'duration': str(int(meta['duration']) * 60)})
                except:
                    pass

                cm = []

                try:
                    if i['url'].endswith(".xml"):
                        cm.append(
                            ("Update Selected List",
                             "RunPlugin(%s)" % url.replace("action=directory", "action=uncached")))
                except:
                    pass

                if content in ['movies', 'tvshows']:
                    meta.update({'trailer': '%s?action=trailer&name=%s' % (system_addon, urllib.quote_plus(name))})
                    cm.append((control.lang(30707).encode('utf-8'),
                               'RunPlugin(%s?action=trailer&name=%s)' % (system_addon, urllib.quote_plus(name))))

                if content in ['movies', 'tvshows', 'seasons', 'episodes']:
                    cm.append((control.lang(30708).encode('utf-8'), 'XBMC.Action(Info)'))

                if content == 'movies':
                    try:
                        dfile = '%s (%s)' % (data['title'], data['year'])
                    except:
                        dfile = name
                elif content == 'episodes':
                    try:
                        dfile = '%s S%02dE%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode']))
                    except:
                        dfile = name
                if not mode:
                    if content == 'movies':
                        mode = "movies"
                    elif content == 'tvshows':
                        mode = "tvshows"
                if mode == 'movies':
                    cm.append(
                        (control.lang(30711).encode('utf-8'),
                         'RunPlugin(%s?action=addView&content=movies)' % system_addon))
                    cm.append(('Add to %s' % fave_name,
                               'RunPlugin(%s?action=addToFavorites&name=%s&type=movie&link=%s&poster=%s&fanart=%s)' % (
                                   system_addon, urllib.quote(name), urllib.quote(i['url']), poster, fanart)))
                elif mode == 'tvshows':
                    cm.append((control.lang(30712).encode('utf-8'),
                               'RunPlugin(%s?action=addView&content=tvshows)' % system_addon))
                    cm.append(
                        ('Add to %s' % fave_name,
                         'RunPlugin(%s?action=addToFavorites&name=%s&type=tv show&link=%s&poster=%s&fanart=%s)' % (
                             system_addon, name, i['url'], poster, fanart)))
                    if parent_url:
                        cm.append(('Queue TV Show',
                                   'RunPlugin(%s?action=queueItem&url=%s)' % (
                                       system_addon, urllib.quote_plus(i['url']))))
                elif mode == 'seasons':
                    cm.append((control.lang(30713).encode('utf-8'),
                               'RunPlugin(%s?action=addView&content=seasons)' % system_addon))
                    if parent_url:
                        cm.append(('Queue Season',
                                   'RunPlugin(%s?action=queueItem&url=%s)' % (
                                       system_addon, urllib.quote_plus(i['url']))))
                elif mode == 'albums':
                    cm.append(('Queue Album',
                               'RunPlugin(%s?action=queueItem&url=%s)' % (
                                   system_addon, urllib.quote_plus(i['url']))))
                elif mode == 'artists':
                    cm.append(('Queue Artist',
                               'RunPlugin(%s?action=queueItem&url=%s)' % (
                                   system_addon, urllib.quote_plus(i['url']))))
                elif mode == 'boxsets':
                    cm.append(('Queue Boxset',
                               'RunPlugin(%s?action=queueItem&url=%s)' % (
                                   system_addon, urllib.quote_plus(i['url']))))
                elif mode == 'episodes':
                    cm.append((control.lang(30714).encode('utf-8'),
                               'RunPlugin(%s?action=addView&content=episodes)' % system_addon))

                if devmode is True:
                    try:
                        cm.append(('Open in browser',
                                   'RunPlugin(%s?action=browser&url=%s)' % (system_addon, urllib.quote_plus(i['url']))))
                    except:
                        pass
                if folder is not True:
                    cm.append(('Queue Item',
                               'RunPlugin(%s?action=queueItem&url=%s&name=%s&image=%s)' % (
                                   system_addon, urllib.quote_plus(i['url']), name, poster)))

                if xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() > 0:
                    cm.append(('Start Playing Queue',
                               'RunPlugin(%s?action=playQueue)' % (
                                   system_addon)))

                    cm.append(('Show Queue',
                               'Action("Playlist")'))

                    cm.append(('Clear Queue',
                               'RunPlugin(%s?action=clearQueue)' % (
                                   system_addon)))

                if "content" in i and 'favs' in i['content']:
                    fav_type = i["content"].replace("-favs", "")
                    cm.append(('Remove From %s' % fave_name,
                               'RunPlugin(%s?action=removeFromFavorites&name=%s&type=%s&link=%s)' % (
                                   system_addon, urllib.quote(name), urllib.quote(fav_type), urllib.quote(i['url']))))
                    cm.append(('Move Favorite',
                               'RunPlugin(%s?action=MoveFavorite&name=%s&type=%s&link=%s)' % (
                                   system_addon, urllib.quote(name), urllib.quote(fav_type), urllib.quote(i['url']))))

                if content in ["movies", "episodes"]:
                    imdb = Indexer.bob_get_tag_content(i["url"], 'imdb', '0')
                    tmdb = Indexer.bob_get_tag_content(i["url"], 'tmdb', '0')
                    tvdb = Indexer.bob_get_tag_content(i["url"], 'tvdb', '0')
                    season = Indexer.bob_get_tag_content(i["url"], 'season', '0')
                    episode = Indexer.bob_get_tag_content(i["url"], 'episode', '0')
                    if not "playcount" in i or i["playcount"] == '0':
                        cm.append(('Mark As Watched',
                                   'RunPlugin(%s?action=markwatched&imdb=%s&tmdb=%s&tvdb=%s&season=%s&episode=%s&unwatched=%s&content=%s)' % (
                                       system_addon, imdb, tmdb, tvdb, season, episode, True, content[:-1])))
                    else:
                        cm.append(('Mark As Unwatched',
                                   'RunPlugin(%s?action=markwatched&imdb=%s&tmdb=%s&tvdb=%s&season=%s&episode=%s&unwatched=%s&content=%s)' % (
                                       system_addon, imdb, tmdb, tvdb, season, episode, False, content[:-1])))

                item = control.item(label=name, iconImage=poster, thumbnailImage=poster)

                try:
                    item.setArt({'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner,
                                 'tvshow.banner': banner, 'season.banner': banner})
                except:
                    pass

                if not fanart == '0':
                    item.setProperty('Fanart_Image', fanart)
                elif addon_fanart is not None:
                    item.setProperty('Fanart_Image', addon_fanart)

                if content != "songs":
                    meta['title'] = name
                    item.setInfo(type='video', infoLabels=meta)
                else:
                    try:
                        item_url = i['url']
                        song_title = re.compile('<song_title>(.+?)</song_title>').findall(item_url)[0]
                        song_artist = re.compile('<song_artist>(.+?)</song_artist>').findall(item_url)[0]
                        item.setInfo(type='music', infoLabels={'title': song_title, 'artist': song_artist})
                    except:
                        item.setInfo(type='video', infoLabels=meta)

                item.addContextMenuItems(cm)
                control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=folder)
            except:
                pass

        if mode is not None:
            control.content(int(sys.argv[1]), mode)
        control.addSort(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
        control.addSort(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        control.addSort(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)
        control.addSort(int(sys.argv[1]), xbmcplugin.SORT_METHOD_GENRE)
        if mode == "movies":
            control.addSort(int(sys.argv[1]), xbmcplugin.SORT_METHOD_MPAA_RATING)

        control.directory(int(sys.argv[1]), cacheToDisc=True)
        if mode is not None:
            views.setView(mode)


class Resolver:
    def browser(self, url):
        try:
            url = self.get(url)
            if url is False:
                return
            control.execute(
                'RunPlugin(plugin://plugin.program.chrome.launcher/?url=%s&mode=showSite&stopPlayback=no)' % urllib.quote_plus(
                    url))
        except:
            pass

    def link(self, url):
        try:
            url = self.get(url)
            if url is False:
                return

            control.execute('ActivateWindow(busydialog)')
            url = self.process(url)
            control.execute('Dialog.Close(busydialog)')

            if url is None:
                return control.infoDialog(control.lang(30705).encode('utf-8'))
            return url
        except:
            pass

    @staticmethod
    def get(url, name=None, link=None):
        try:
            if name is None:
                name = control.infoLabel('listitem.label')
            items = re.compile('<sublink>(.+?)</sublink>').findall(url)
            if len(items) == 0:
                items = [url]
            new_items = []

            messages = [
                {'HD': 'If Available',
                 'SD': 'Most Likely Works'
                 },
                {'HD': 'Bob\'s Ya Uncle',
                 'SD': 'Bob\'s NOT Ya Cousin'
                 },
                {'HD': 'Checking Top Sites',
                 'SD': 'Sitting In Cinema Recording'
                 },
                {'HD': 'This quality is being looked for by top men, who? Top....Men!',
                 'SD': 'This quality is sold on the corner by a shady guy'
                 },
                {'HD': 'Google Fiber',
                 'SD': 'Waiting For Dialup Connection'
                 },
                {'HD': 'Great! Worth the wait',
                 'SD': 'Good Enough. I just want to watch'
                 },
                {'HD': 'BluRay Quality',
                 'SD': 'VHS Quality'
                 },
                {'HD': 'Tsingtao ',
                 'SD': 'Budweiser'
                 },
                {'HD': 'I must see this film in the highest quality',
                 'SD': 'Flick probably sucks so lets just get it over'
                 },
                {'HD': 'Looks like a Maserati',
                 'SD': ' Looks like a Ford Focus'
                 },
                {'HD': 'Supermodel Quality',
                 'SD': ' Looks like Grandma Thelma'
                 },
                {'HD': 'ARB',
                 'SD': 'ARD'
                 },
            ]

            if control.setting('enable_offensive') == 'true':
                messages.extend([
                    {'HD': 'Kicks Ass!!',
                     'SD': 'Gets ass kicked repeatedly'
                     },
                    {'HD': 'Fucking Rocks!!',
                     'SD': 'Fucking Sucks!!'
                     },
                    {'HD': 'Big Bodacious Breasts',
                     'SD': 'Saggy Milk Teets',
                     }
                ])

            message = random.choice(messages)

            if control.setting('disable_messages') == 'true':
                message = {
                    'HD': 'If Available',
                    'SD': ''
                }

            already_added = False

            for item in items:
                if control.setting('use_link_dialog') == 'true' and ("searchsd" in item or "search" in item):
                    if not already_added:
                        new_item = ("Search", item)
                        already_added = True
                    else:
                        continue
                else:
                    if "searchsd" in item:
                        label = 'SD'
                        if message['SD'] != '':
                            label += ' (%s)' % message['SD']
                        new_item = (label, item)
                    elif "search" in item:
                        label = 'HD'
                        if message['HD'] != '':
                            label += ' (%s)' % message['HD']
                        new_item = (label, item)
                    else:
                        new_item = ('Link %s' % (int(items.index(item)) + 1), item)
                new_items.append(new_item)
            items = new_items

            if len(items) == 1:
                url = items[0][1]
                return url
            elif link is not None:
                for index, item in enumerate(items):
                    if item[0].startswith(link):
                        url = items[index][1]
                        return url

            select = control.selectDialog([i[0] for i in items], name)
            if select == -1:
                return False
            else:
                url = items[select][1]

            return url
        except:
            pass

    @staticmethod
    def f4m(url, name):
        try:
            if not any(i in url for i in ['.f4m', '.ts']):
                raise Exception()
            ext = url.split('?')[0].split('&')[0].split('|')[0].rsplit('.')[-1].replace('/', '').lower()
            if ext not in ['f4m', 'ts']:
                raise Exception()

            params = urlparse.parse_qs(url)

            try:
                proxy = params['proxy'][0]
            except:
                proxy = None

            try:
                proxy_use_chunks = json.loads(params['proxy_for_chunks'][0])
            except:
                proxy_use_chunks = True

            try:
                maxbitrate = int(params['maxbitrate'][0])
            except:
                maxbitrate = 0

            try:
                simple_downloader = json.loads(params['simpledownloader'][0])
            except:
                simple_downloader = False

            try:
                auth_string = params['auth'][0]
            except:
                auth_string = ''

            try:
                streamtype = params['streamtype'][0]
            except:
                streamtype = 'TSDOWNLOADER' if ext == 'ts' else 'HDS'

            try:
                swf = params['swf'][0]
            except:
                swf = None

            try:
                from F4mProxy import f4mProxyHelper
            except:
                control.dialog.ok("Dependency missing", "please install F4MProxy to use this feature")
                raise Exception()

            return f4mProxyHelper().playF4mLink(url, name, proxy, proxy_use_chunks, maxbitrate, simple_downloader,
                                                auth_string, streamtype, False, swf)
        except:
            pass

    @staticmethod
    def process(url, direct=True, name='', hide_progress=False):
        from resources.lib.sources import sources
        try:
            if not any(i in url for i in ['.jpg', '.png', '.gif']):
                raise Exception()
            ext = url.split('?')[0].split('&')[0].split('|')[0].rsplit('.')[-1].replace('/', '').lower()
            if ext not in ['jpg', 'png', 'gif']:
                raise Exception()
            try:
                i = os.path.join(control.dataPath, 'img')
                control.deleteFile(i)
                f = control.openFile(i, 'w')
                f.write(client.request(url))
                f.close()
                control.execute('ShowPicture("%s")' % i)
                return False
            except:
                return
        except:
            pass

        try:
            r = urllib.unquote_plus(url)
            if '</regex>' not in r:
                raise Exception()

            from resources.lib.modules import regex
            r = regex.resolve(r)

            if r[0] == 'makelist':
                Indexer().getx(r[1])
                return False
            elif r[0] == 'link':
                u = r[1]

            if u is not None:
                url = u
        except:
            pass

        try:
            if not url.startswith('rtmp'):
                raise Exception()
            if len(re.compile('\s*timeout=(\d*)').findall(url)) == 0:
                url += ' timeout=10'
            return url
        except:
            pass

        try:
            if not any(i in url for i in ['.m3u8', '.f4m', '.ts']):
                raise Exception()
            ext = url.split('?')[0].split('&')[0].split('|')[0].rsplit('.')[-1].replace('/', '').lower()
            if ext not in ['m3u8', 'f4m', 'ts']:
                raise Exception()
            return url
        except:
            pass

        message = control.lang(30731).encode('utf-8')

        try:
            preset = re.findall('<preset>(.+?)</preset>', url)[0]
            content = re.findall('<content>(.+?)</content>', url)[0]
            try:
                exclude_scrapers = re.findall('<exclude_scrapers>(.+?)</exclude_scrapers>', url)[0]
                exclude_scrapers = exclude_scrapers.split(";")
            except:
                exclude_scrapers = []

            if content == "movie" or content == "episode":
                messages = ['',
                            'Bob\'s just nipping to blockbusters won\'t be but a sec',
                            'Bob fell asleep during this flick',
                            'Bob\'s movie collection has no limits',
                            'Searching the Internet for your selection',
                            'Bob has seen your taste in movies and is very disappointed ',
                            'Bob thinks he\'s got that DVD laying around here',
                            'Bob says you\'re a movie geek just like him',
                            'Bob says get off of twitter and enjoy his addon',
                            'Bob is a wanted man in 125 countries',
                            'Bob said your taste in films is top notch',
                            'When Bob chooses a movie, servers shake in fear',
                            'They fear Bob. Don\'t listen to haters',
                            'Bob said he works so hard for YOU, the end user',
                            'Bob does this cause he loves it, not for greed',
                            'That\'s not Bobs butt crack, it\'s his remote holder',
                            'Bob...I Am Your Father!!',
                            'I\'m going to make Bob an offer he can\'t refuse.',
                            'Here\'s looking at you, Bob',
                            'Go ahead, make Bob\'s day.',
                            'May the Bob be with you',
                            'You talking to Bob??',
                            'I love the smell of Bob in the morning',
                            'Bob, phone home',
                            'Made it Bob! Top of the World!',
                            'Bob, James Bob',
                            'There\'s no place like Bob',
                            'You had me at "Bob"',
                            "YOU CAN\'T HANDLE THE BOB",
                            'Round up all the usual Bobs',
                            'I\'ll have what Bob\'s having',
                            'You\'re gonna need a bigger Bob',
                            'Bob\'ll be back',
                            'If you build it. Bob will come',
                            'We\'ll always have Bob',
                            'Bob, we have a problem',
                            'Say "hello" to my little Bob',
                            'Bob, you\'re trying to seduce me. Aren\'t you?',
                            'Elementary, my dear Bob',
                            'Get your stinking paws off me, you damned dirty Bob',
                            'Here\'s Bob!',
                            'Hasta la vista, Bob.',
                            'Soylent Green is Bob!',
                            'Open the pod bay doors, BOB.',
                            'Yo, Bob!',
                            'Oh, no, it wasn\'t the airplanes. It was Beauty killed the Bob.',
                            'A Bob. Shaken, not stirred.',
                            'Who\'s on Bob.',
                            'I feel the need - the need for Bob!',
                            'Nobody puts Bob in a corner.',
                            'I\'ll get you, my pretty, and your little Bob, too!',
                            'I\'m Bob of the world!',
                            'Shan of Bob',
                            'Bøb, Bøb, Bøb, Bøb, Bøb, Bøb, Bøb, Bøb, Bøb, Bøb, Bøb, Bøb, Bøb, Bøb, Bøb, Bøb, Bøb'
                            ]

                if control.setting('enable_offensive') == 'true':
                    messages.extend([
                        'Fuck Shit Wank -- Costa',
                        'Frankly my dear, I don\'t give a Bob',
                        'Beast Build Detected, Installing dangerous pyo file'
                    ])

                message = control.lang(30731).encode('utf-8') + '\n' + random.choice(messages)

                if control.setting('disable_messages') == 'true':
                    message = control.lang(30731).encode('utf-8')

                try:

                    if preset == "search":
                        messages.extend([
                            'Bob is popping in Blu Ray Disc'
                        ])
                    elif preset == "searchsd":
                        messages.extend([
                            'Bob rummaging through his vhs collection',
                        ])

                    message = control.lang(30731).encode('utf-8') + '\n' + random.choice(messages)

                    if control.setting('disable_messages') == 'true':
                        message = control.lang(30731).encode('utf-8')

                    title, year, imdb = re.findall('<title>(.+?)</title>', url)[0], \
                                        re.findall('<year>(.+?)</year>', url)[0], \
                                        re.findall('<imdb>(.+?)</imdb>', url)[0]
                    scraper_title = None
                    try:
                        scraper_title = re.findall('<scrapertitle>(.+?)</scrapertitle>', url)[0]
                    except:
                        pass

                    try:
                        tvdb, tvshowtitle, premiered, season, episode = re.findall('<tvdb>(.+?)</tvdb>', url)[0], \
                                                                        re.findall('<tvshowtitle>(.+?)</tvshowtitle>',
                                                                                   url)[0], \
                                                                        re.findall('<premiered>(.+?)</premiered>', url)[
                                                                            0], \
                                                                        re.findall('<season>(.+?)</season>', url)[0], \
                                                                        re.findall('<episode>(.+?)</episode>', url)[0]
                    except:
                        tvdb = tvshowtitle = premiered = season = episode = None

                    direct = False

                    # preset_dictionary = ['primewire', 'watchfree', 'movie4k', 'movie25', 'watchseries', 'pftv', 'afdah', 'dayt',
                    #                      'dizibox', 'dizigold', 'genvideo', 'mfree', 'miradetodo', 'movieshd', 'onemovies',
                    #                      'onlinedizi', 'pelispedia', 'pubfilm', 'putlocker', 'rainierland', 'sezonlukdizi',
                    #                      'tunemovie', 'xmovies']
                    #
                    # if preset == 'searchsd':
                    #     preset_dictionary = ['primewire', 'watchfree', 'movie4k', 'movie25', 'watchseries', 'pftv']
                    dialog = None
                    if not hide_progress:
                        dialog = control.progressDialog
                        dialog.create(control.addonInfo('name'), control.lang(30726).encode('utf-8'))
                        dialog.update(0)

                    try:
                        dialog.update(0, control.lang(30726).encode('utf-8') + ' ' + name, message)
                    except:
                        pass

                    if premiered:
                        premiered = int(premiered[0:4])

                    if scraper_title:
                        u = sources().getSources(scraper_title, int(year), imdb, tvdb, season, episode, tvshowtitle,
                                                 premiered, progress=False, timeout=20, preset=preset, dialog=dialog,
                                                 exclude=exclude_scrapers, scraper_title=True)

                        try:
                            dialog.update(50, control.lang(30726).encode('utf-8') + ' ' + name)
                        except:
                            pass

                        if u is not None:
                            try:
                                dialog.close()
                                return u
                            except:
                                pass

                    if scraper_title is None or control.setting('search_alternate') == 'true':

                        u = sources().getSources(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered,
                                                 progress=False, timeout=20, preset=preset, dialog=dialog,
                                                 exclude=exclude_scrapers)

                        try:
                            dialog.update(50, control.lang(30726).encode('utf-8') + ' ' + name)
                        except:
                            pass

                        if u is not None:
                            try:
                                if dialog:
                                    dialog.close()
                                return u
                            except:
                                pass
                    try:
                        if dialog.iscanceled():
                            dialog.close()
                    except:
                        pass

                except:
                    try:
                        dialog.close()
                    except:
                        pass
            elif content == "song":
                messages = ['',
                            'Bob was a roddy for led zep',
                            'I kissed a bob, and i liked it',
                            'Bob was the one that handed ozzy a real bat',
                            'Bob is the real reason the Beatles broke up',
                            'Bob is a Battlefield',
                            'Great Bobs of Fire',
                            'Burning Ring of Bob',
                            'Fly...High...Free Bob yeah!',
                            'It\'s a long way to the Bob if you wanna Rock and Roll',
                            'Another Brick in the Bob',
                            'The Bob\'s so bright, I gotta wear shades.',
                            'Stairway to Bob',
                            'Never Gonna Give Bob up',
                            'Like a Rolling Bob',
                            'Fade to Bob',
                            'Viva la Bob',
                            'Bye, Bye Miss American Bob',
                            'Bring me to Bob',
                            'Jailhouse Bob',
                            'While Bob\'s Guitar Gently Weeps',
                            'Don\'t Take Your Guns to Bob',
                            'Welcome to the Bob of Rock and Roll',
                            '21st Century Schizoid Bob',
                            'Stray Cat Bob',
                            'Lust for Bob',
                            'Bob Gave Me a Taco',
                            'Dames, Booze, Chains And Bobs',
                            'Take This Bob And Shove It',
                            ]

                if control.setting('enable_offensive') == 'true':
                    messages.extend([
                        'Fuck Shit Wank -- Costa',
                    ])

                message = control.lang(30731).encode('utf-8') + '\n' + random.choice(messages)

                if control.setting('disable_messages') == 'true':
                    message = control.lang(30731).encode('utf-8')
                try:
                    if control.setting('disable_messages') == 'true':
                        message = control.lang(30731).encode('utf-8')

                    title = re.findall('<song_title>(.+?)</song_title>', url)[0]
                    artist = re.findall('<song_artist>(.+?)</song_artist>', url)[0]
                    scraper_title = None
                    try:
                        scraper_title = re.findall('<scrapertitle>(.+?)</scrapertitle>', url)[0]
                    except:
                        pass

                    direct = False
                    dialog = None
                    if not hide_progress:
                        dialog = control.progressDialog
                        dialog.create(control.addonInfo('name'), control.lang(30726).encode('utf-8'))
                        dialog.update(0)

                    try:
                        dialog.update(0, control.lang(30726).encode('utf-8') + ' ' + name, message)
                    except:
                        pass

                    if scraper_title:
                        u = sources().getMusicSources(scraper_title, artist, progress=False, timeout=20, preset=preset,
                                                      dialog=dialog, exclude=exclude_scrapers)

                        try:
                            dialog.update(50, control.lang(30726).encode('utf-8') + ' ' + name)
                        except:
                            pass

                        if u is not None:
                            try:
                                dialog.close()
                                return u
                            except:
                                pass

                    if scraper_title is None or control.setting('search_alternate') == 'true':
                        u = sources().getMusicSources(title, artist, progress=False, timeout=20, preset=preset,
                                                      dialog=dialog, exclude=exclude_scrapers)

                        try:
                            dialog.update(50, control.lang(30726).encode('utf-8') + ' ' + name)
                        except:
                            pass

                        if u is not None:
                            try:
                                dialog.close()
                                return u
                            except:
                                pass
                except:
                    pass

        except:
            pass

        try:
            dialog = None
            if not hide_progress:
                dialog = control.progressDialog
                dialog.create(control.addonInfo('name'), message)
                dialog.update(0)

            try:
                dialog.update(0, control.lang(30726).encode('utf-8') + ' ' + name)
            except:
                pass

            resolved = sources().direct_resolve(url)

            if not resolved == False: direct = False
            if resolved == None or resolved == False: raise Exception()

            try:
                dialog.update(50, control.lang(30726).encode('utf-8') + ' ' + name)
            except:
                pass

            try:
                dialog.close()
            except:
                pass
            return resolved
        except:
            try:
                dialog.close()
            except:
                pass
            pass

        try:
            if '.google.com' not in url:
                raise Exception()
            from resources.lib.modules import directstream
            u = directstream.google(url)[0]['url']
            return u
        except:
            pass

        try:
            if 'filmon.com/' not in url:
                raise Exception()
            from resources.lib.modules import filmon
            u = filmon.resolve(url)
            return u
        except:
            pass

        try:
            try:
                headers = dict(urlparse.parse_qsl(url.rsplit('|', 1)[1]))
            except:
                headers = dict('')
            if not url.startswith('http'):
                raise Exception()
            result = client.request(url.split('|')[0], headers=headers, output='headers', timeout='20')
            if 'Content-Type' in result and 'html' not in result['Content-Type']:
                raise Exception()

            try:
                import liveresolver
            except:
                control.dialog.ok("Dependency missing", "please install liveresolver to use this feature")
                raise Exception()

            if liveresolver.isValid(url) is False:
                raise Exception()

            direct = False
            u = liveresolver.resolve(url)

            if u is not None:
                return u
        except:
            pass

        if url.startswith("plugin://") or sources().check_playable(url):
            direct = True

        if direct is True:
            return url


# noinspection PyPep8Naming
class Player(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__(self)

    def play(self, url, content=None):
        try:
            self.original_url = url
            url = Resolver().get(url)
            if url is False:
                return

            control.execute('ActivateWindow(busydialog)')
            url = Resolver().process(url)
            control.execute('Dialog.Close(busydialog)')

            if url is None:
                return control.infoDialog(control.lang(30705).encode('utf-8'))
            if url is False:
                return

            meta = {}
            for i in ['title', 'originaltitle', 'tvshowtitle', 'year', 'season', 'episode', 'genre', 'rating', 'votes',
                      'director', 'writer', 'plot', 'tagline']:
                try:
                    meta[i] = control.infoLabel('listitem.%s' % i)
                except:
                    pass
            meta = dict((k, v) for k, v in meta.iteritems() if not v == '')
            if 'title' not in meta:
                meta['title'] = control.infoLabel('listitem.label')
            icon = control.infoLabel('listitem.icon')

            self.name = meta['title']
            self.year = meta['year'] if 'year' in meta else '0'
            self.meta = meta

            self.getbookmark = True if (content == 'movies' or content == 'episodes') else False

            self.offset = Bookmarks().get(self.name, self.year)

            f4m = Resolver().f4m(url, self.name)
            if f4m is not None:
                return

            item = control.item(path=url, iconImage=icon, thumbnailImage=icon)
            try:
                item.setArt({'icon': icon})
            except:
                pass
            if content == "songs":
                try:
                    meta['artist'] = control.infoLabel('listitem.artist')
                    item.setInfo(type='Music', infoLabels={'title': meta['title'], 'artist': meta['artist']})
                except:
                    item.setInfo(type='Video', infoLabels=meta)

            else:
                item.setInfo(type='Video', infoLabels=meta)

            if 'plugin' in control.infoLabel('Container.PluginName'):
                if self.isPlaying():
                    xbmc.PlayList(xbmc.PLAYLIST_VIDEO).clear()
                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                playlist.add(url, item, 0)
                control.player.play(playlist, item)

            control.resolve(int(sys.argv[1]), True, item)

            self.totalTime = 0
            self.currentTime = 0

            for i in range(0, 240):
                if self.isPlaying():
                    break
                control.sleep(1000)
            while self.isPlaying():
                try:
                    self.totalTime = self.getTotalTime()
                    self.currentTime = self.getTime()
                except:
                    pass
                control.sleep(2000)
            control.sleep(5000)
        except:
            pass

    def onPlayBackStarted(self):
        control.execute('Dialog.Close(all,true)')
        if self.getbookmark is True and not self.offset == '0':
            self.seekTime(float(self.offset))

    def onPlayBackStopped(self):
        xbmc.PlayList(xbmc.PLAYLIST_VIDEO).clear()
        if self.getbookmark is True:
            Bookmarks().reset(self.currentTime, self.totalTime, self.name, self.year)

    def onPlayBackEnded(self):
        self.onPlayBackStopped()
        self.meta.update({'playcount': '1'})
        imdb = Indexer.bob_get_tag_content(self.original_url, 'imdb', '0')
        tmdb = Indexer.bob_get_tag_content(self.original_url, 'tmdb', '0')
        tvdb = Indexer.bob_get_tag_content(self.original_url, 'tvdb', '0')
        season = Indexer.bob_get_tag_content(self.original_url, 'season', '0')
        episode = Indexer.bob_get_tag_content(self.original_url, 'episode', '0')
        content = Indexer.bob_get_tag_content(self.original_url, 'content', '0')
        if content == "episode":
            metacache.episodes_set_watched(imdb, tmdb, tvdb, season, episode)
        elif content == "movie":
            metacache.movies_set_watched(imdb, tmdb, tvdb)
        control.refresh()


class Bookmarks:
    def get(self, name, year='0'):
        try:
            offset = '0'

            # if not control.setting('Bookmarks') == 'true': raise Exception()

            id_file = hashlib.md5()
            for i in name:
                id_file.update(str(i))
            for i in year:
                id_file.update(str(i))
            id_file = str(id_file.hexdigest())

            dbcon = database.connect(control.bookmarksFile)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM bookmark WHERE idFile = '%s'" % id_file)
            match = dbcur.fetchone()
            self.offset = str(match[1])
            dbcon.commit()

            if self.offset == '0':
                raise Exception()

            minutes, seconds = divmod(float(self.offset), 60)
            hours, minutes = divmod(minutes, 60)
            label = '%02d:%02d:%02d' % (hours, minutes, seconds)
            label = (control.lang(32502) % label).encode('utf-8')

            try:
                yes = control.dialog.contextmenu([label, control.lang(32501).encode('utf-8'), ])
            except:
                yes = control.yesnoDialog(label, '', '', str(name), control.lang(32503).encode('utf-8'),
                                          control.lang(32501).encode('utf-8'))

            if yes:
                self.offset = '0'

            return self.offset
        except:
            return offset

    @staticmethod
    def reset(current_time, total_time, name, year='0'):
        try:
            # if not control.setting('Bookmarks') == 'true': raise Exception()

            time_in_seconds = str(current_time)
            ok = int(current_time) > 180 and (current_time / total_time) <= .92

            id_file = hashlib.md5()
            for i in name:
                id_file.update(str(i))
            for i in year:
                id_file.update(str(i))
            id_file = str(id_file.hexdigest())

            control.makeFile(control.dataPath)
            dbcon = database.connect(control.bookmarksFile)
            dbcur = dbcon.cursor()
            dbcur.execute(
                "CREATE TABLE IF NOT EXISTS bookmark (""idFile TEXT, ""timeInSeconds TEXT, ""UNIQUE(idFile)"");")
            dbcur.execute("DELETE FROM bookmark WHERE idFile = '%s'" % id_file)
            if ok:
                dbcur.execute("INSERT INTO bookmark Values (?, ?)", (id_file, time_in_seconds))
            dbcon.commit()
        except:
            pass

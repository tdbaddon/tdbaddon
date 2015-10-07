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


import os,re,urllib,urlparse,json,zipfile,StringIO,datetime,base64

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

from resources.lib.libraries import control
from resources.lib.libraries import cleantitle
from resources.lib.libraries import cloudflare
from resources.lib.libraries import client


class source:
    def __init__(self):
        self.base_link = 'http://movietv.to'
        self.data_link = 'aHR0cHM6Ly9vZmZzaG9yZWdpdC5jb20vbGFtYmRhODEvZGF0YWJhc2VzL21vdmlldHYuemlw'


    def get_movie(self, imdb, title, year):
        try:
            data = os.path.join(control.dataPath, 'movietv.db')

            download = True

            try: download = abs(datetime.datetime.fromtimestamp(os.path.getmtime(data)) - (datetime.datetime.now())) > datetime.timedelta(days=7)
            except: pass

            if download == True:
                result = client.source(base64.b64decode(self.data_link))
                zip = zipfile.ZipFile(StringIO.StringIO(result))
                zip.extractall(control.dataPath)
                zip.close()

            dbcon = database.connect(data)
            dbcur = dbcon.cursor()

            dbcur.execute("SELECT * FROM movies WHERE year = '%s'" % year)
            result = dbcur.fetchone()
            result = eval(result[1].encode('utf-8'))

            title = cleantitle.movie(title)

            result = [i[0] for i in result if title == cleantitle.movie(i[1])][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            data = os.path.join(control.dataPath, 'movietv.db')

            download = True

            try: download = abs(datetime.datetime.fromtimestamp(os.path.getmtime(data)) - (datetime.datetime.now())) > datetime.timedelta(days=7)
            except: pass

            if download == True:
                result = client.source(base64.b64decode(self.data_link))
                zip = zipfile.ZipFile(StringIO.StringIO(result))
                zip.extractall(control.dataPath)
                zip.close()

            dbcon = database.connect(data)
            dbcur = dbcon.cursor()

            dbcur.execute("SELECT * FROM tvshows WHERE year = '%s'" % year)
            result = dbcur.fetchone()
            result = eval(result[1].encode('utf-8'))

            tvshowtitle = cleantitle.tv(tvshowtitle)

            result = [i[0] for i in result if tvshowtitle == cleantitle.tv(i[1])][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return

            if not '%01d' % int(season) == '1': return
            if '%01d' % int(episode) > '3': return

            url += '?S%02dE%02d' % (int(season), int(episode))
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            content = re.compile('(.+?)\?S\d*E\d*$').findall(url)

            try: url, season, episode = re.compile('(.+?)\?S(\d*)E(\d*)$').findall(url)[0]
            except: pass

            url = urlparse.urljoin(self.base_link, url)

            result = cloudflare.source(url, safe=True, timeout='10', headers={'Referer': 'http://movietv.to/'})

            if len(content) == 0:
                u = client.parseDOM(result, 'source', ret='src', attrs = {'type': 'video.+?'})[0]
            else:
                u = re.compile('playSeries\((\d+),(%01d),(%01d)\)' % (int(season), int(episode))).findall(result)[0]
                u = '/series/getLink?id=%s&s=%s&e=%s' % (u[0], u[1], u[2])
                u = urlparse.urljoin(self.base_link, u)
                u = cloudflare.source(u, safe=True, timeout='10', headers={'X-Requested-With': 'XMLHttpRequest', 'Referer': url})
                u = json.loads(u)['url']

            url = '%s|User-Agent=%s&Referer=%s' % (u, urllib.quote_plus(client.agent()), urllib.quote_plus(url))

            sources.append({'source': 'MovieTV', 'quality': 'HD', 'provider': 'MovieTV', 'url': url})

            return sources
        except:
            return sources


    def resolve(self, url):
        return url



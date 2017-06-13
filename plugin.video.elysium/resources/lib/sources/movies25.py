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


import re,os,urllib,urlparse,json,zipfile,StringIO,datetime,base64

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy

from BeautifulSoup import BeautifulSoup
class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = ['movie25.ph', 'movie25.hk', 'tinklepad.is', 'tinklepad.ag']
        self.base_link = 'http://www.movie25.me'
        self.search_link = 'http://www.movie25.me/keywords/%s/'
        self.search_link_2 = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAwODQ5Mjc2ODA5NjE4MzM5MDAwMzowdWd1c2phYm5scSZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='


    def movie(self, imdb, title, year):
	
	
        cleanmovie = cleantitle.get(title)
        # try:
            # download = True

            # data = os.path.join(control.dataPath, 'provider.movie25.db')
            # data_link = 'http://offshoregit.com/extest/provider.movie25.zip'

            # try: download = abs(datetime.datetime.fromtimestamp(os.path.getmtime(data)) - (datetime.datetime.now())) > datetime.timedelta(days=7)
            # except: pass

            # if download == True:
                # r = client.request(data_link)
                # zip = zipfile.ZipFile(StringIO.StringIO(r))
                # zip.extractall(control.dataPath)
                # zip.close()

            # dbcon = database.connect(data)
            # dbcur = dbcon.cursor()
            # dbcur.execute("SELECT * FROM movies WHERE imdb = '%s'" % imdb)
            # url = dbcur.fetchone()[0]
            # dbcon.close()

            # return url
        # except:
            # pass

        try:
            q = self.search_link % urllib.quote_plus(title)

            r = client.request(q)

            r = BeautifulSoup(r)
            r = r.findAll('div', attrs={'class': 'movie_about'})
            for item in r:
				h = item.findAll('a')[0]['href'].encode('utf-8')
				t = item.findAll('a')[0]	
				t = t.string
				t = t.encode('utf-8')
				h = h.encode('utf-8')
				if year in t:
					if cleanmovie == cleantitle.get(t):
						print ("MOVIES25 passed", h,t)
						url = h
						
						return url
        except:
            pass


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            quality = "SD"
            if url == None: return sources
            url = urlparse.urljoin(self.base_link, url)
            print ("MOVIE25 SOURCES", url)
            result = client.request(url)
            r = BeautifulSoup(result)
            r = r.findAll('ul')
            for item in r:
					try:
						print ("MOVIE25 SOURCES", item)
						h = re.findall('<li id="playing_button"><a href="(.+?)"', str(item))[0]
						h2 = re.findall('<li id="download">(.+?)</li>',  str(item))[0]
						try: host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(h2.strip().lower()).netloc)[0]
						except: host = h2
						# if not host in hostDict: raise Exception()
						host = host.encode('utf-8')

						sources.append({'source': host, 'quality': quality, 'provider': 'Movies25', 'url': h, 'direct': False, 'debridonly': False})						
										
						print ("MOVIE25 SOURCES 3", h, host)
					except:
						pass


            return sources
        except:
            return sources


    def resolve(self, url):
        r = client.request(url, timeout='5') 
        r = re.compile('<a target="_blank" href="(.+?)">').findall(r)
        for item in r:
			if '/external/' in item: 
				url = item.split('/')[-1]
				url = base64.b64decode(url)
				
        return url



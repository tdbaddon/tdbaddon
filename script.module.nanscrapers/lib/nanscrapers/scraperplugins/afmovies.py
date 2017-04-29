# -*- coding: utf-8 -*-

'''
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
import re
import urllib
import urlparse
import xbmc

import requests
from BeautifulSoup import BeautifulSoup
from ..common import  clean_title, random_agent, replaceHTMLCodes, clean_search, filter_host
from ..scraper import Scraper

class afmovies(Scraper):
    domains = ['afdah.to']
    name = 'afmovies'

    def __init__(self):
        self.base_link = 'http://afdah.to'
        self.search_link = '/?s=%s'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            sources = self.movie(imdb, title, year)
            for source in sources:
                source["scraper"] = source["provider"]
            return sources
        except:
            return []

    def movie(self, imdb, title, year):
        try:
            self.zen_url = []
            cleanmovie = clean_title(title)
            title = urllib.quote_plus(title.lower())
            headers = {'User-Agent': random_agent(), 'X-Requested-With':'XMLHttpRequest', 'Referer': "http://afdah.to/"}
            search_url = urlparse.urljoin(self.base_link, '/wp-content/themes/afdah/ajax-search.php')
            data = {'test1': title, 'test2': 'title'}

            moviesearch = requests.post(search_url, headers=headers, data=data)
            moviesearch = moviesearch.content
            match = re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(moviesearch)
            for href, movietitle in match:
                if year in movietitle and cleanmovie == clean_title(movietitle):
                    url = href.encode('utf-8')
                    if not "http" in url: url = urlparse.urljoin(self.base_link, url)
                    return self.sources(url, [], [])
        except:
            pass
        return []

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            headers = {'User-Agent': random_agent()}
            html = requests.get(url)
            r = BeautifulSoup(html.content)
            r = r.findAll('tr')
            for items in r:
                href = items.findAll('a')[0]['href'].encode('utf-8')
                print ("AFMOVIE R2", href)
                try:host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(href.strip().lower()).netloc)[0]
                except: host = 'Afmovies'
                #if not host in hostDict: continue
                if not filter_host(host):
                        continue
                sources.append({'source': host, 'quality': 'SD', 'provider': 'Afmovies', 'url': href,  'direct': False, 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        return url

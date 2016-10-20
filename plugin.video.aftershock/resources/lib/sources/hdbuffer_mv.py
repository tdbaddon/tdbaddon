# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2015 IDev

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


import re,urllib,urlparse,random, datetime

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import metacache
from resources.lib import resolvers
from resources.lib.libraries import logger

class source:
    def __init__(self):
        self.base_link_1 = 'http://hdbuffer.com'
        self.base_link_2 = self.base_link_1
        self.search_link = '/?s=%s&feed=rss'
        self.movie_link = '%s/%s/'
        self.info_link = ''
        self.now = datetime.datetime.now()
        self.HD_link = '/category/%s/dvdbluraymovies-%sonline'
        self.list = []

    def scn_full_list(self, url, lang=None,  provider=None):
        self.list = []

        pagesScanned = 0
        try :
            url = getattr(self, url + '_link')
            url = url % (lang, lang)
        except:pass

        turl = url

        while((len(self.list) < 15) and (pagesScanned < 10)):
            self.scn_list(turl, lang)
            try : url =  re.compile('(.+)/page/.+').findall(turl)[0]
            except :
                pass
            try: pageNo =  re.compile('/page/(.+)').findall(turl)[0]
            except:
                pageNo = 1
                pass
            pageNo = int(pageNo) + 1
            turl = '%s/page/%s' % (url, pageNo)
            pagesScanned = pagesScanned + 1
        self.list[0].update({'next':turl})
        self.list = metacache.fetchImdb(self.list)
        return self.list

    def scn_list(self, url, lang=None):
        try :
            links = [self.base_link_1, self.base_link_1, self.base_link_1]
            for base_link in links:
                try: result = client.source(base_link + url)
                except:
                    result = ''

                if 'nag cf' in result: break

            if result == '' :
                return result

            result = result.decode('iso-8859-1').encode('utf-8')
            result = client.parseDOM(result, "div", attrs={"class":"nag cf"})[0]
            movies = client.parseDOM(result,"div", attrs={"class":"thumb"})
            for movie in movies:
                try:
                    title = client.parseDOM(movie, "a", ret="title")[0]
                    title = re.compile('(.+?) [(]\d{4}[)]').findall(title)[0]
                    title = client.replaceHTMLCodes(title)
                    try : title = title.encode('utf-8')
                    except: pass

                    year = client.parseDOM(movie, "a", ret="title")[0]
                    year = re.compile('.+? [(](\d{4})[)]').findall(year)[0]
                    year = year.encode('utf-8')

                    name = '%s (%s)' % (title, year)
                    try: name = name.encode('utf-8')
                    except: pass

                    url = client.parseDOM(movie, "a", ret="href")[0]
                    url = client.replaceHTMLCodes(url)
                    try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
                    except: pass

                    poster = '0'
                    try: poster = client.parseDOM(movie, "img", ret="src")[0]
                    except: pass
                    poster = client.replaceHTMLCodes(poster)
                    try: poster = urlparse.parse_qs(urlparse.urlparse(poster).query)['u'][0]
                    except: pass
                    poster = poster.encode('utf-8')

                    duration = '0' ; tvdb = '0'; genre = '0'

                    self.list.append({'title': title, 'originaltitle': title, 'duration':duration,'year': year, 'genre': genre, 'name': name, 'tvdb': tvdb, 'poster': poster, 'banner': '0', 'fanart': '0', 'lang':lang})

                except:
                    pass

            return self.list

        except:
            pass
        return

    def get_movie(self, imdb, title, year):
        try:
            self.base_link = random.choice([self.base_link_1, self.base_link_2])

            query = '%s %s' % (title, year)
            query = self.search_link % (urllib.quote_plus(query))
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query)

            result = result.decode('iso-8859-1').encode('utf-8')
            result = client.parseDOM(result, "item")

            title = cleantitle.movie(title)
            for item in result:
                searchTitle = client.parseDOM(item, "title")[0]
                searchTitle = re.compile('(.+?) [(]\d{4}[)]').findall(searchTitle)[0]
                searchTitle = cleantitle.movie(searchTitle)
                if title == searchTitle:
                    url = client.parseDOM(item, "link")[0]
                    url = url.replace(self.base_link, '')
                    break
            if url == None or url == '':
                raise Exception()
            return url
        except:
            return

    def get_sources(self, url):
        logger.debug('SOURCES URL %s' % url, __name__)
        try:
            quality = ''
            sources = []

            if url == None: return sources

            try: result = client.source(self.movie_link % (self.base_link_1, url))
            except: result = ''

            result = result.decode('iso-8859-1').encode('utf-8')

            result = result.replace('\n','')

            categories = client.parseDOM(result, "div", attrs={"id":"extras"})
            categories = client.parseDOM(categories, "a", attrs={"rel":"category tag"})

            for category in categories:
                category = category.lower()
                if "scr" in category:
                    quality = "SCR"
                    break
                elif "bluray" in category:
                    quality = "HD"
                    break

            links = client.parseDOM(result, "div", attrs={"class":"GTTabs_divs GTTabs_curr_div"})
            links += client.parseDOM(result, "div", attrs={"class":"GTTabs_divs"})
            for link in links:
                try :
                    url = re.compile('(SRC|src|data-config)=[\'|\"](.+?)[\'|\"]').findall(link)[0][1]
                    host = client.host(url)
                    sources.append({'source': host, 'parts': '1', 'quality': quality, 'provider': 'HDBuffer', 'url': url, 'direct':False})
                except :
                    pass
            logger.debug('SOURCES [%s]' % sources, __name__)
            return sources
        except:
            return sources

    def resolve(self, url, resolverList):
        logger.debug('ORIGINAL URL [%s]' % url, __name__)
        url = resolvers.request(url, resolverList)
        logger.debug('RESOLVED URL [%s]' % url, __name__)
        return url




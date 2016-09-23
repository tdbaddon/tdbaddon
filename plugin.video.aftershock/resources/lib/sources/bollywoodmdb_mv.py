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


import re,urllib,urlparse,datetime

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib import resolvers
from resources.lib.libraries import workers
from resources.lib.libraries import control
from resources.lib.libraries import logger

class source:
    def __init__(self):
        self.base_link = 'http://www.bollywoodmdb.com'
        self.now = datetime.datetime.now()
        self.theaters_link = '/movies/new-releases'
        self.langMap = {'hindi':'hi'}
        self.sources = []

    def scn_full_list(self, url, lang=None, provider=None):
        self.list = []

        try :
            url = getattr(self, url + '_link')
        except:pass

        links = [self.base_link, self.base_link, self.base_link]
        for base_link in links:
            try: result = client.source(base_link + url)
            except:
                result = ''
            if 'row move-data' in result: break

        result = result.decode('iso-8859-1').encode('utf-8')
        movies = client.parseDOM(result, "div", attrs={"class":"col-md-6 col-sm-6 col-xs-12 col-padding-reset"})

        for movie in movies:
            try :
                title = client.parseDOM(movie, "a", attrs={"class":"movie-link"})[0]
                title = re.compile('<strong>(.+?)</strong>').findall(title)[0]
                title = client.replaceHTMLCodes(title)
                try : title = title.encode('utf-8')
                except: pass

                year = client.parseDOM(movie, "div", attrs={"class":"mov-release-date bg-area visible-xs bot-list-padding-reset"})[0]
                year = year = re.compile('.+?, (\d{4})').findall(year)[0]
                year = year.encode('utf-8')

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                url = client.parseDOM(movie, "a", ret="href")[0]
                url = client.replaceHTMLCodes(url)
                try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
                except: pass

                poster = '0'
                try:
                    poster = client.parseDOM(movie, "img", ret="data-original")[0]
                    #poster = '%s%s' % (self.base_link, poster)
                except: pass
                poster = client.replaceHTMLCodes(poster)
                try: poster = urlparse.parse_qs(urlparse.urlparse(poster).query)['u'][0]
                except: pass
                poster = poster.encode('utf-8')

                duration = '0'

                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'duration': duration, 'name': name, 'poster': poster, 'banner': '0', 'fanart': '0', 'tvdb':'0'})
            except:
                pass

        return self.list
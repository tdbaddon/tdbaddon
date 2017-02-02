# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2017 Aftershockpy

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

import datetime
import re
import urllib
import urlparse

from resources.lib import resolvers
from resources.lib.modules import client
from resources.lib.modules import logger


class source:
    def __init__(self):
        self.base_link_1 = 'http://www.yodesi.net'
        self.base_link_2 = 'http://www.yodesi.net'
        self.base_link_3 = 'http://www.yodesi.net'

        self.search_link = '/feed/?s=%s&submit=Search'
        self.info_link = 'http://www.yo-desi.com/player.php?id=%s'
        self.now = datetime.datetime.now()

        self.srcs = []

    def networks(self):
        listItems = []
        provider = 'yodesi'
        listItems.append({'provider':provider, 'name':90200, 'image': 'star_plus_hk.png', 'action': 'tvshows', 'url':'star-plus'})
        listItems.append({'provider':provider, 'name':90201, 'image': 'zee_tv_in.png', 'action': 'tvshows', 'url':'zee-tv'})
        listItems.append({'provider':provider, 'name':90203, 'image': 'sony_set.png', 'action': 'tvshows', 'url':'sony-tv'})
        listItems.append({'provider':provider, 'name':90205, 'image': 'life_ok_in.png', 'action': 'tvshows', 'url':'life-ok'})
        listItems.append({'provider':provider, 'name':90207, 'image': 'star_jalsha.png', 'action': 'tvshows', 'url':'star-jalsha'})
        listItems.append({'provider':provider, 'name':90208, 'image': 'colors_in.png', 'action': 'tvshows', 'url':'colors'})
        listItems.append({'provider':provider, 'name':90209, 'image': 'sony_sab_tv_in.png', 'action': 'tvshows', 'url':'sab-tv'})
        listItems.append({'provider':provider, 'name':90210, 'image': 'star_pravah.png', 'action': 'tvshows', 'url':'star-pravah'})
        listItems.append({'provider':provider, 'name':90212, 'image': 'mtv_us.png', 'action': 'tvshows', 'url':'mtv-india'})
        listItems.append({'provider':provider, 'name':90213, 'image': 'channel_v_in.png', 'action': 'tvshows', 'url':'category/channel-v'})
        listItems.append({'provider':provider, 'name':90214, 'image': 'bindass_in.png', 'action': 'tvshows', 'url':'bindass-tv'})
        listItems.append({'provider':provider, 'name':90220, 'image': 'and_tv_in.png', 'action': 'tvshows', 'url':'tv-and-tv'})
        return listItems

    def tvshows(self, name, url):
        try:
            result = ''
            shows = []
            links = [self.base_link_1, self.base_link_2, self.base_link_3]
            for base_link in links:
                try:
                    result = client.request('%s/%s' % (base_link, url))
                except: result = ''
                if 'tab_container' in result: break

            rawResult = result.decode('iso-8859-1').encode('utf-8')
            rawResult = rawResult.replace('\n','').replace('\t','').replace('\r','')

            rawResult = client.parseDOM(rawResult, "div", attrs = {"id" : "tab-0-title-1"})[0]
            result = client.parseDOM(rawResult, "div", attrs = {"class" : "one_fourth  "})
            result += client.parseDOM(rawResult, "div", attrs = {"class" : "one_fourth  column-last "})

            for item in result:
                title = ''
                url = ''
                title = client.parseDOM(item, "p", attrs = {"class": "small-title"})[0]
                url = client.parseDOM(item, "a", ret="href")[0]

                title = client.parseDOM(title, "a")[0]
                title = client.replaceHTMLCodes(title)

                poster = client.parseDOM(item, "img", ret="src")[0]

                if 'concert' in title.lower():
                    continue
                shows.append({'name':title, 'channel':name, 'title':title, 'url':url, 'poster': poster, 'banner': poster, 'fanart': poster, 'next': '0','year':'0','duration':'0','provider':'yodesi'})
            return shows
        except:
            client.printException('')
            return

    def tvshow(self, tvshowurl, imdb, tvdb, tvshowtitle, year):
        if tvshowurl:
            return tvshowtitle

    def episodes(self, title, url):
        try :
            try :
                season = title.lower()
                season = re.compile('[0-9]+').findall(season)[0]
                #season = season.replace('season ', '')
            except :
                import traceback
                traceback.print_exc()
                season = '0'
            episodes = []

            tvshowurl = url
            rawResult = client.request(url)
            rawResult = rawResult.decode('iso-8859-1').encode('utf-8')
            rawResult = rawResult.replace('\n','').replace('\t','').replace('\r','')

            result = client.parseDOM(rawResult, "article")

            for item in result:
                if "promo" in item or '(Day' in item:
                    continue
                item = client.parseDOM(item, "h2")[0]
                name = client.parseDOM(item, "a", ret ="title")
                if type(name) is list:
                    name = name[0]
                url = client.parseDOM(item, "a", ret="href")
                if type(url) is list:
                    url = url[0]
                if "Online" not in name: continue
                name = name.replace(title, '')
                try :name = re.compile('Season [\d{1}|\d{2}](\w.+\d{4})').findall(name)[0]
                except:pass
                name = re.compile('([\d{1}|\d{2}]\w.+\d{4})').findall(name)[0]
                name = name.strip()
                episodes.append({'season' : season, 'tvshowtitle':title, 'title':name, 'name':name,'url' : url, 'provider':'yodesi', 'tvshowurl':tvshowurl})

            next = client.parseDOM(rawResult, "nav")
            next = client.parseDOM(next, "a", attrs={"class": "next page-numbers"}, ret="href")[0]
            episodes[0].update({'next':next})

            return episodes
        except:
            return episodes


    def episode(self, url, ep_url, imdb, tvdb, title, date, season, episode):
        query = '%s %s' % (imdb, title)
        query = self.search_link % (urllib.quote_plus(query))
        ep_url = query
        if ep_url :
            return ep_url

    def sources(self, url):
        try:
            logger.debug('SOURCES URL %s' % url, __name__)
            quality = ''
            srcs = []

            result = ''

            links = [self.base_link_1, self.base_link_2, self.base_link_3]
            for base_link in links:
                try: result = client.request(base_link + '/' + url)
                except: result = ''
                if 'item' in result: break

            result = result.decode('iso-8859-1').encode('utf-8')

            result = result.replace('\n','')

            items = client.parseDOM(result, 'content:encoded')[0]

            items = re.compile('class=\"single-heading\">(.+?)<span').findall(items)

            for i in range(0, len(items)):
                try :
                    if '720p' in items[i]:
                        quality = 'HD'
                    else:
                        quality = 'SD'
                    urls = client.parseDOM(items[i], "a", ret="href")
                    for j in range(0,len(urls)):
                        videoID = getVideoID(urls[j])
                        result = client.request(self.info_link % videoID)
                        result = result.decode('iso-8859-1').encode('utf-8')
                        item = client.parseDOM(result, name="div", attrs={"style": "float:none;height:700px;margin-left:200px"})[0]
                        rUrl = re.compile('(SRC|src|data-config)=[\'|\"](.+?)[\'|\"]').findall(item)[0][1]
                        if not rUrl.startswith('http:'):
                            rUrl = '%s%s' % ('http:', rUrl)
                        urls[j] = rUrl
                    host = client.host(urls[0])
                    url = "##".join(urls)
                    srcs.append({'source':host, 'parts': str(len(urls)), 'quality':quality,'provider':'YoDesi','url':url, 'direct':False})
                    urls = []
                except Exception as e:
                    logger.error(e)
                    pass
            logger.debug('SOURCES [%s]' % srcs, __name__)
            return srcs
        except:
            return srcs

    def resolve(self, url, resolverList):
        try:
            logger.debug('ORIGINAL URL [%s]' % url, __name__)
            tUrl = url.split('##')
            if len(tUrl) > 0:
                url = tUrl
            else :
                url = urlparse.urlparse(url).path

            links = []
            for item in url:
                r = resolvers.request(item, resolverList)
                if not r :
                    raise Exception()
                links.append(r)
            url = links
            logger.debug('RESOLVED URL [%s]' % url, __name__)
            return url
        except:
            return False

def getVideoID(url):
    try :
        return re.compile('(id|url|v|si|sim|data-config)=(.+?)/').findall(url + '/')[0][1]
    except:
        return
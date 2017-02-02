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
import urlparse

from resources.lib import resolvers
from resources.lib.modules import cache
from resources.lib.modules import client
from resources.lib.modules import logger
from resources.lib.modules import cleantitle


class source:
    def __init__(self):
        self.base_link_1 = 'http://www.desirulez.net'
        self.base_link_2 = 'http://www.desirulez.me'
        self.base_link_3 = 'http://www.desirulez.net'
        self.search_link = '/feed/?s=%s&submit=Search'

        self.info_link = ''
        self.now = datetime.datetime.now()

        self.awards_link = 'forumdisplay.php?f=36'
        self.star_plus_link = 'forumdisplay.php?f=42'
        self.zee_tv_link = 'forumdisplay.php?f=73'
        self.sony_link = 'forumdisplay.php?f=63'
        self.life_ok_link = 'forumdisplay.php?f=1375'
        self.colors_link = 'forumdisplay.php?f=176'
        self.sony_sab_link = 'forumdisplay.php?f=254'
        self.star_jalsha_link = 'forumdisplay.php?f=667'
        self.sahara_one_link = 'forumdisplay.php?f=134'
        self.and_tv_link = 'forumdisplay.php?f=3138'
        self.star_pravah_link = 'forumdisplay.php?f=1138'
        self.sony_pal_link = 'forumdisplay.php?f=2757'
        self.mtv_india_link = 'forumdisplay.php?f=339'
        self.utv_bindass_link = 'forumdisplay.php?f=504'
        self.channel_v_link = 'forumdisplay.php?f=633'
        self.utv_stars_link = 'forumdisplay.php?f=1274'
        self.big_magic_link = 'forumdisplay.php?f=1887'
        self.zee_marathi_link = 'forumdisplay.php?f=1299'
        self.zee_bangla = 'forumdisplay.php?f=676'
        self.star_vijay_link = 'forumdisplay.php?f=1609'
        self.zoom_link = 'forumdisplay.php?f=1876'
        self.zing_link = 'forumdisplay.php?f=2624'
        self.zee_yuva_link = 'forumdisplay.php?f=4229'
        self.colors_marathi_link = 'forumdisplay.php?f=2369'
        self.colors_bangla_link = 'forumdisplay.php?f=2117'
        self.maa_link = 'forumdisplay.php?f=3165'

        self.hungama_link = 'forumdisplay.php?f=472'
        self.cartoon_network_link = 'forumdisplay.php?f=509'

        self.zee_zindagi_link = 'forumdisplay.php?f=2679'

        self.srcs = []

    def networks(self):
        listItems = []
        provider = 'desirulez'
        listItems.append({'provider':provider, 'name':90200, 'image': 'star_plus_hk.png', 'action': 'tvshows', 'url':self.star_plus_link})
        listItems.append({'provider':provider, 'name':90201, 'image': 'zee_tv_in.png', 'action': 'tvshows', 'url':self.zee_tv_link})
        listItems.append({'provider':provider, 'name':90203, 'image': 'sony_set.png', 'action': 'tvshows', 'url':self.sony_link})
        listItems.append({'provider':provider, 'name':90205, 'image': 'life_ok_in.png', 'action': 'tvshows', 'url':self.life_ok_link})
        listItems.append({'provider':provider, 'name':90206, 'image': 'sahara_one_in.png', 'action': 'tvshows', 'url':self.sahara_one_link})
        listItems.append({'provider':provider, 'name':90207, 'image': 'star_jalsha.png', 'action': 'tvshows', 'url':self.star_jalsha_link})
        listItems.append({'provider':provider, 'name':90208, 'image': 'colors_in.png', 'action': 'tvshows', 'url':self.colors_link})
        listItems.append({'provider':provider, 'name':90209, 'image': 'sony_sab_tv_in.png', 'action': 'tvshows', 'url':self.sony_sab_link})
        listItems.append({'provider':provider, 'name':90210, 'image': 'star_pravah.png', 'action': 'tvshows', 'url':self.star_pravah_link})
        listItems.append({'provider':provider, 'name':90212, 'image': 'mtv_us.png', 'action': 'tvshows', 'url':self.mtv_india_link})
        listItems.append({'provider':provider, 'name':90213, 'image': 'channel_v_in.png', 'action': 'tvshows', 'url':self.channel_v_link})
        listItems.append({'provider':provider, 'name':90214, 'image': 'bindass_in.png', 'action': 'tvshows', 'url':self.utv_bindass_link})
        listItems.append({'provider':provider, 'name':90215, 'image': 'utv_stars.png', 'action': 'tvshows', 'url':self.utv_stars_link})
        listItems.append({'provider':provider, 'name':90218, 'image': 'hungama.png', 'action': 'tvshows', 'url':self.hungama_link})
        listItems.append({'provider':provider, 'name':90219, 'image': 'cartoon_network_global.png', 'action': 'tvshows', 'url':self.cartoon_network_link})
        listItems.append({'provider':provider, 'name':90220, 'image': 'and_tv_in.png', 'action': 'tvshows', 'url':self.and_tv_link})
        listItems.append({'provider':provider, 'name':90222, 'image': 'colors_in_bangla.png', 'action': 'tvshows', 'url':self.colors_bangla_link})
        listItems.append({'provider':provider, 'name':90223, 'image': 'zee_zindagi_in.png', 'action': 'tvshows', 'url':self.zee_zindagi_link})
        listItems.append({'provider':provider, 'name':90224, 'image': 'big_magic_in.png', 'action': 'tvshows', 'url':self.big_magic_link})
        listItems.append({'provider':provider, 'name':90225, 'image': 'colors_in_marathi.png', 'action': 'tvshows', 'url':self.colors_marathi_link})
        listItems.append({'provider':provider, 'name':90226, 'image': 'maa_tv.png', 'action': 'tvshows', 'url':self.maa_link})
        listItems.append({'provider':provider, 'name':90227, 'image': 'zee_marathi.png', 'action': 'tvshows', 'url':self.zee_marathi_link})
        listItems.append({'provider':provider, 'name':90228, 'image': 'zee_bangla.png', 'action': 'tvshows', 'url':self.zee_bangla})
        listItems.append({'provider':provider, 'name':90229, 'image': 'zoom_tv_in.png', 'action': 'tvshows', 'url':self.zoom_link})
        listItems.append({'provider':provider, 'name':90230, 'image': 'star_vijay.png', 'action': 'tvshows', 'url':self.star_vijay_link})

        listItems.append({'provider':provider, 'name':90231, 'image': 'sony_pal_in.png', 'action': 'tvshows', 'url':self.sony_pal_link})
        listItems.append({'provider':provider, 'name':90232, 'image': 'zee_zing.png', 'action': 'tvshows', 'url':self.zing_link})
        listItems.append({'provider':provider, 'name':90233, 'image': 'zee_yuva_in.png', 'action': 'tvshows', 'url':self.zee_yuva_link})
        url = 'episodes&tvshowtitle=awards&year=0&imdb=0&tvdb=0'
        listItems.append({'provider':provider, 'name':90234, 'image': 'awards_in.png', 'action': url, 'url':self.awards_link})

        return listItems

    def movie(self, imdb, title, year):
        try :
            movies = cache.get(self.desiRulezCache, 168)
            url = [i['url'] for i in movies if cleantitle.movie(i['title']) == cleantitle.movie(title)][0]
            return url
        except:
            pass

    def desiRulezCache(self):
        try :
            base_link = 'http://www.desirulez.me/forums/20-Latest-Exclusive-Movie-HQ'
            result = client.request(base_link)
            result = result.decode('iso-8859-1').encode('utf-8')
            result = client.parseDOM(result, "li", attrs = {"class": "threadbit hot"})
            movies = []
            for link in result:
                link = client.parseDOM(link, "h3", attrs={"class": "threadtitle"})[0]
                url = client.parseDOM(link, "a", ret="href")[0]
                title = client.parseDOM(link, "a")[0]
                title = cleantitle.movie(title).replace('watchonline/download', '')
                movies.append({'url':url, 'title':title})
            return movies
        except:
            pass

    def tvshows(self, name, url):
        try:
            result = ''
            shows = []
            links = [self.base_link_1, self.base_link_2, self.base_link_3]
            for base_link in links:
                try:
                    result = client.request('%s/%s' % (base_link, url))
                    if result == None:
                        raise Exception()
                except: result = ''
                if 'forumtitle' in result: break

            result = result.decode('iso-8859-1').encode('utf-8')
            result = client.parseDOM(result, "h2", attrs = {"class" : "forumtitle"})

            for item in result:
                title = ''
                url = ''
                title = client.parseDOM(item, "a", attrs = {"class": "title threadtitle_unread"})

                if not title:
                    title = client.parseDOM(item, "a", attrs = {"class": "title"})
                    if title:
                        title = title[0]
                    else :
                        title = client.parseDOM(item, "a")

                if type(title) is list and len(title) > 0:
                    title = str(title[0])
                title = client.replaceHTMLCodes(title)
                url = client.parseDOM(item, "a", ret="href")

                if not url:
                    url = client.parseDOM(item, "a", attrs = {"class": "title"}, ret="href")

                if type(url) is list and len(url) > 0:
                    url = str(url[0])

                if not 'Past Shows' in title:
                    # name , title, poster, imdb, tvdb, year, poster, banner, fanart, duration
                    shows.append({'name':title, 'channel':name, 'title':title, 'url':url, 'poster': '0', 'banner': '0', 'fanart': '0', 'next': '0','year':'0','duration':'0','provider':'desirulez'})
            return shows
        except:
            client.printException('')
            return

    def tvshow(self, tvshowurl, imdb, tvdb, tvshowtitle, year):
        if tvshowurl:
            return tvshowurl

    def episodes(self, title, url):
        try :
            episodes = []
            links = [self.base_link_1, self.base_link_2, self.base_link_3]
            tvshowurl = url
            for base_link in links:
                try:
                    result = client.request(base_link + '/' + url)
                    if result == None:
                        raise Exception()
                except:
                    result = ''

                if 'threadtitle' in result: break

            rawResult = result.decode('iso-8859-1').encode('utf-8')

            result = client.parseDOM(rawResult, "h3", attrs = {"class" : "title threadtitle_unread"})
            result += client.parseDOM(rawResult, "h3", attrs = {"class" : "threadtitle"})

            for item in result:
                name = client.parseDOM(item, "a", attrs = {"class": "title"})
                name += client.parseDOM(item, "a", attrs = {"class": "title threadtitle_unread"})
                if type(name) is list:
                    name = name[0]
                url = client.parseDOM(item, "a", ret="href")
                if type(url) is list:
                    url = url[0]
                if "Online" not in name: continue
                name = name.replace(title, '')
                if not title == 'awards'  :
                    name = re.compile('([\d{1}|\d{2}]\w.+\d{4})').findall(name)[0]
                name = name.strip()
                try :
                    season = title.lower()
                    season = re.compile('[0-9]+').findall(season)[0]
                    #season = season.replace('season ', '')
                except :
                    season = '0'
                episodes.append({'season':season, 'tvshowtitle':title, 'title':name, 'name':name,'url' : url, 'provider':'desirulez', 'tvshowurl':tvshowurl})

            next = client.parseDOM(rawResult, "span", attrs={"class": "prev_next"})
            next = client.parseDOM(next, "a", attrs={"rel": "next"}, ret="href")[0]
            episodes[0].update({'next':next})

            return episodes
        except:
            import traceback
            traceback.print_exc()
            return episodes

    def episode(self, url, ep_url, imdb, tvdb, title, date, season, episode):
        if ep_url :
            return ep_url

    def sources(self, url):
        logger.debug('SOURCES URL %s' % url, __name__)
        try:
            quality = ''
            srcs = []

            result = ''
            links = [self.base_link_1, self.base_link_2, self.base_link_3]
            for base_link in links:
                try:
                    result = client.request(base_link + '/' + url)
                    if result == None:
                        raise Exception()
                except: result = ''
                if 'blockquote' in result: break

            result = result.decode('iso-8859-1').encode('utf-8')

            result = result.replace('\n','')

            ### DIRTY Implementation
            import BeautifulSoup
            soup = BeautifulSoup.BeautifulSoup(result).findAll('blockquote', {'class':re.compile(r'\bpostcontent\b')})[0]

            for e in soup.findAll('br'):
                e.extract()
            if soup.has_key('div'):
                soup = soup.findChild('div', recursive=False)
            urls = []
            quality = ''
            for child in soup.findChildren():
                if (child.getText() == '') or ((child.name == 'font' or child.name == 'a') and re.search('DesiRulez', str(child.getText()),re.IGNORECASE)):
                    continue
                elif (child.name == 'font') and re.search('Links|Online|Link',str(child.getText()),re.IGNORECASE):
                    if len(urls) > 0:
                        for i in range(0,len(urls)):
                            try :
                                result = client.request(urls[i])
                                item = client.parseDOM(result, name="div", attrs={"style": "float:right;margin-bottom:10px"})[0]
                                rUrl = re.compile('(SRC|src|data-config)=[\'|\"](.+?)[\'|\"]').findall(item)[0][1]
                                rUrl = client.urlRewrite(rUrl)
                                urls[i] = rUrl
                            except :
                                urls[i] = client.urlRewrite(urls[i])
                                pass
                        host = client.host(urls[0])
                        url = "##".join(urls)
                        srcs.append({'source':host, 'parts': str(len(urls)), 'quality':quality,'provider':'DesiRulez','url':url, 'direct':False})
                        quality = ''
                        urls = []
                    quality = child.getText()
                    if '720p HD' in quality:
                        quality = 'HD'
                    elif 'Scr' in quality :
                        quality = 'SCR'
                    else :
                        quality = ''
                elif (child.name =='a') and not child.getText() == 'registration':
                    urls.append(str(child['href']))
                    if quality == '' :
                        quality = child.getText()
                        if '720p HD' in quality:
                            quality = 'HD'
                        elif 'Scr' in quality :
                            quality = 'SCR'
                        elif 'Dvd' in quality :
                            quality = 'SD'
                        else :
                            quality = ''

            if len(urls) > 0:
                for i in range(0,len(urls)):
                    try :
                        result = client.request(urls[i])
                        item = client.parseDOM(result, name="div", attrs={"style": "float:right;margin-bottom:10px"})[0]
                        rUrl = re.compile('(SRC|src|data-config)=[\'|\"](.+?)[\'|\"]').findall(item)[0][1]
                        rUrl = client.urlRewrite(rUrl)
                        urls[i] = rUrl
                    except :
                        urls[i] = client.urlRewrite(urls[i])
                        pass
                host = client.host(urls[0])
                url = "##".join(urls)
                srcs.append({'source': host, 'parts' : str(len(urls)), 'quality': quality, 'provider': 'DesiRulez', 'url': url,'direct':False})
            logger.debug('SOURCES [%s]' % srcs, __name__)
            return srcs
        except:
            return srcs

    def resolve(self, url, resolverList):
        logger.debug('ORIGINAL URL [%s]' % url, __name__)
        try:
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
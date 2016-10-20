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


import re,urlparse, datetime

from resources.lib.libraries import client
from resources.lib import resolvers
from resources.lib.libraries import logger
from resources.lib.libraries import cache
from resources.lib.libraries import cleantitle

class source:
    def __init__(self):
        self.base_link_1 = 'http://www.desirulez.net'
        self.base_link_2 = 'http://www.desirulez.me'
        self.base_link_3 = 'http://www.desirulez.net'
        self.search_link = '/feed/?s=%s&submit=Search'

        self.info_link = ''
        self.now = datetime.datetime.now()

        self.star_plus_link = 'forumdisplay.php?f=42'
        self.zee_tv_link = 'forumdisplay.php?f=73'
        self.set_link = 'forumdisplay.php?f=63'
        self.life_ok_link = 'forumdisplay.php?f=1375'
        self.sahara_one_link = 'forumdisplay.php?f=134'
        self.star_jalsha_link = 'forumdisplay.php?f=667'
        self.colors_link = 'forumdisplay.php?f=176'
        self.sony_sab_link = 'forumdisplay.php?f=254'
        self.star_pravah_link = 'forumdisplay.php?f=1138'
        self.mtv_india_link = 'forumdisplay.php?f=339'
        self.channel_v_link = 'forumdisplay.php?f=633'
        self.utv_bindass_link = 'forumdisplay.php?f=504'
        self.utv_stars_link = 'forumdisplay.php?f=1274'
        self.hungama_link = 'forumdisplay.php?f=472'
        self.cartoon_network_link = 'forumdisplay.php?f=509'
        self.and_tv_link = 'forumdisplay.php?f=3138'
        self.colors_bangla_link = 'forumdisplay.php?f=2117'

        self.list = []

    def get_movie(self, imdb, title, year):
        try :
            movies = cache.get(self.desiRulezCache, 168)
            url = [i['url'] for i in movies if cleantitle.movie(i['title']) == cleantitle.movie(title)][0]
            return url
        except:
            pass

    def desiRulezCache(self):
        try :
            base_link = 'http://www.desirulez.me/forums/20-Latest-Exclusive-Movie-HQ'
            result = client.source(base_link)
            result = result.decode('iso-8859-1').encode('utf-8')
            result = client.parseDOM(result, "li", attrs = {"class":"threadbit hot"})
            movies = []
            for link in result:
                link = client.parseDOM(link, "h3", attrs={"class":"threadtitle"})[0]
                url = client.parseDOM(link, "a", ret="href")[0]
                title = client.parseDOM(link, "a")[0]
                title = cleantitle.movie(title).replace('watchonline/download', '')
                movies.append({'url':url, 'title':title})
            return movies
        except:
            pass

    def get_shows(self, name, url):
        try:
            result = ''
            shows = []
            links = [self.base_link_1, self.base_link_2, self.base_link_3]
            for base_link in links:
                try:
                    result = client.source('%s/%s' % (base_link,url))
                except: result = ''
                if 'forumtitle' in result: break

            result = result.decode('iso-8859-1').encode('utf-8')
            result = client.parseDOM(result, "h2", attrs = {"class" : "forumtitle"})

            for item in result:
                title = ''
                url = ''
                title = client.parseDOM(item, "a", attrs = {"class":"title threadtitle_unread"})

                if not title:
                    title = client.parseDOM(item, "a", attrs = {"class":"title"})
                    if title:
                        title = title[0]
                    else :
                        title = client.parseDOM(item, "a")

                if type(title) is list and len(title) > 0:
                    title = str(title[0])
                title = client.replaceHTMLCodes(title)
                url = client.parseDOM(item, "a", ret="href")

                if not url:
                    url = client.parseDOM(item, "a", attrs = {"class":"title"}, ret="href")

                if type(url) is list and len(url) > 0:
                    url = str(url[0])

                if not 'Past Shows' in title:
                    # name , title, poster, imdb, tmdb, tvdb, tvrage, year, poster, banner, fanart, duration
                    shows.append({'name':title, 'channel':name, 'title':title, 'url':url, 'poster': '0', 'banner': '0', 'fanart': '0', 'next': '0', 'tvrage':'0','year':'0','duration':'0','provider':'desirulez_mv_tv'})
            return shows
        except:
            client.printException('')
            return

    def get_show(self, tvshowurl, imdb, tvdb, tvshowtitle, year):
        if tvshowurl:
            return tvshowurl

    def get_episodes(self, title, url):
        try :
            episodes = []
            links = [self.base_link_1, self.base_link_2, self.base_link_3]
            tvshowurl = url
            for base_link in links:
                try:
                    result = client.source(base_link + '/' + url)
                except: result = ''
                if 'threadtitle' in result: break

            rawResult = result.decode('iso-8859-1').encode('utf-8')

            result = client.parseDOM(rawResult, "h3", attrs = {"class" : "title threadtitle_unread"})
            result += client.parseDOM(rawResult, "h3", attrs = {"class" : "threadtitle"})

            for item in result:
                name = client.parseDOM(item, "a", attrs = {"class":"title"})
                name += client.parseDOM(item, "a", attrs = {"class":"title threadtitle_unread"})
                if type(name) is list:
                    name = name[0]
                url = client.parseDOM(item, "a", ret="href")
                if type(url) is list:
                    url = url[0]
                if "Online" not in name: continue
                name = name.replace(title, '')
                name = re.compile('([\d{1}|\d{2}]\w.+\d{4})').findall(name)[0]
                name = name.strip()
                episodes.append({'tvshowtitle':title, 'title':name, 'name':name,'url' : url, 'provider':'desirulez_mv_tv', 'tvshowurl':tvshowurl})

            next = client.parseDOM(rawResult, "span", attrs={"class":"prev_next"})
            next = client.parseDOM(next, "a", attrs={"rel":"next"}, ret="href")[0]
            episodes[0].update({'next':next})

            return episodes
        except:
            import traceback
            traceback.print_exc()
            return episodes

    def get_episode(self, url, ep_url, imdb, tvdb, title, date, season, episode):
        if ep_url :
            return ep_url

    def get_sources(self, url):
        logger.debug('SOURCES URL %s' % url, __name__)
        try:
            quality = ''
            sources = []

            result = ''
            links = [self.base_link_1, self.base_link_2, self.base_link_3]
            for base_link in links:
                try: result = client.source(base_link + '/' + url)
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
                                result = client.source(urls[i])
                                item = client.parseDOM(result, name="div", attrs={"style":"float:right;margin-bottom:10px"})[0]
                                rUrl = re.compile('(SRC|src|data-config)=[\'|\"](.+?)[\'|\"]').findall(item)[0][1]
                                rUrl = client.urlRewrite(rUrl)
                                urls[i] = rUrl
                            except :
                                urls[i] = client.urlRewrite(urls[i])
                                pass
                        host = client.host(urls[0])
                        url = "##".join(urls)
                        sources.append({'source':host, 'parts': str(len(urls)), 'quality':quality,'provider':'DesiRulez','url':url, 'direct':False})
                        quality = ''
                        urls = []
                    quality = child.getText()
                    logger.debug('QUALITY >>> %s' % quality)
                    if '720p HD' in quality:
                        quality = 'HD'
                    elif 'Scr' in quality :
                        quality = 'SCR'
                    else :
                        quality = ''
                elif (child.name =='a') and not child.getText() == 'registration':
                    urls.append(str(child['href']))
                    logger.debug('CHILD >>> %s' % child.getText())
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
                        result = client.source(urls[i])
                        item = client.parseDOM(result, name="div", attrs={"style":"float:right;margin-bottom:10px"})[0]
                        rUrl = re.compile('(SRC|src|data-config)=[\'|\"](.+?)[\'|\"]').findall(item)[0][1]
                        rUrl = client.urlRewrite(rUrl)
                        urls[i] = rUrl
                    except :
                        urls[i] = client.urlRewrite(urls[i])
                        pass
                host = client.host(urls[0])
                url = "##".join(urls)
                sources.append({'source': host, 'parts' : str(len(urls)), 'quality': quality, 'provider': 'DesiRulez', 'url': url,'direct':False})
            logger.debug('SOURCES [%s]' % sources, __name__)
            return sources
        except:
            return sources


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
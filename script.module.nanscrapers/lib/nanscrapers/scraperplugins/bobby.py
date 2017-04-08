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

import re, urllib, urlparse, random
from ..common import random_agent, clean_title, googletag, filter_host
from BeautifulSoup import BeautifulSoup
import xbmc
from ..scraper import Scraper
import requests

session = requests.Session()


class Bobby(Scraper):
    name = "Bobby"

    def __init__(self):
        self.domains = ['bobbyhd.com']
        self.base_link = 'http://webapp.bobbyhd.com'
        self.search_link = '/search.php?keyword=%s+%s'
        self.simple_link = '/search.php?keyword=%s'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            url = self.movie(imdb, title, year)
            sources = self.sources(url, [], [])
            if not sources:
                return []
            for source in sources:
                source["scraper"] = source["provider"]
            return sources
        except:
            return []

    def movie(self, imdb, title, year):
        self.zen_url = []
        try:
            cleanmovie = clean_title(title)

            headers = {'Host': 'webapp.bobbyhd.com',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69',
                       'Accept-Language': 'en-gb',
                       'Accept-Encoding': 'gzip, deflate',
                       'Connection': 'keep-alive'}
            query = self.search_link % (urllib.quote_plus(title), year)
            query = urlparse.urljoin(self.base_link, query)
            r = session.get(query, headers=headers).content
            # print ("BOBBYAPP", r)
            match = re.compile('alias=(.+?)\'">(.+?)</a>').findall(r)
            for id, name in match:
                name = clean_title(name)
                # print ("BOBBYAPP id name", id, name)
                if cleanmovie == name:
                    type = 'type_movies'
                    ep = '0'
                    self.zen_url.append([id, type, ep])

            # print ("BOBBY PASSED", self.zen_url)
            return self.zen_url

        except:
            return

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            show_url = self.tvshow(imdb, tvdb, title, show_year)
            url = self.episode(show_url, imdb, tvdb, title, year, season, episode)
            sources = self.sources(url, [], [])
            for source in sources:
                source["scraper"] = source["provider"]
            return sources
        except:
            return []

    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        self.zen_url = []
        try:

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            #title = clean_title(title)
            cleanmovie = clean_title(title)
            data['season'], data['episode'] = season, episode
            episodecheck = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
            episodecheck = episodecheck.lower()
            query = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
            ep = "%01d" % (int(data['episode']))
            full_check = 'season%01d' % (int(data['season']))
            full_check = cleanmovie + full_check
            headers = {'Host': 'webapp.bobbyhd.com',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69',
                       'Accept-Language': 'en-gb',
                       'Accept-Encoding': 'gzip, deflate',
                       'Connection': 'keep-alive'}
            query = self.simple_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)
            # print ("BOBBYAPP query", query)
            r = session.get(query, headers=headers).content
            # print ("BOBBYAPP", r)
            match = re.compile('alias=(.+?)\'">(.+?)</a>').findall(r)
            for id, name in match:
                name = clean_title(name)
                # print ("BOBBYAPP id name", id, name)
                if full_check == name:
                    type = 'tv_episodes'
                    ep = "%01d" % (int(data['episode']))
                    # print ("BOBBYAPP PASSED", id, name)
                    self.zen_url.append([id, type, ep])
            return self.zen_url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            for url, type, ep in self.zen_url:
                if url == None: return sources
                # print ("BOBBY SOURCES", url, type)
                headers = {'Host': 'webapp.bobbyhd.com',
                           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                           'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69',
                           'Accept-Language': 'en-gb',
                           'Accept-Encoding': 'gzip, deflate',
                           'Connection': 'keep-alive'}
                html = 'http://webapp.bobbyhd.com/player.php?alias=' + url
                r = session.get(html, headers=headers).content
                if type == 'tv_episodes':
                    match = re.compile('changevideo\(\'(.+?)\'\)".+?data-toggle="tab">(.+?)\..+?</a>').findall(r)
                    print(match)
                else:
                    match = re.compile('changevideo\(\'(.+?)\'\)".+?data-toggle="tab">(.+?)</a>').findall(r)
                for href, res in match:
                    if 'webapp' in href:
                        href = href.split('embed=')[1]
                    quality = quality_tag(res)
                    # print ("BOBBY LINKS FOUND", href, res)
                    if type == 'tv_episodes':
                        if ep == res:
                            if "google" in href:
                                if quality == 'SD':
                                    try:
                                        quality = googletag(href)[0]['quality']
                                    except:
                                        if quality == '' or quality == None: quality = 'SD'
                                sources.append(
                                    {'source': 'gvideo', 'quality': quality, 'provider': 'Bobby', 'url': href,
                                     'direct': True, 'debridonly': False})
                            else:
                                try:
                                    host = \
                                    re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                                except:
                                    host = 'none'
                                if not filter_host(host):
                                    continue
                                sources.append({'source': host, 'quality': quality, 'provider': 'Bobby', 'url': href,
                                                'direct': False, 'debridonly': False})
                    else:
                        if "google" in href:
                            if quality == 'SD':
                                try:
                                    quality = googletag(href)[0]['quality']
                                except:
                                    if quality == '' or quality == None: quality = 'SD'
                            sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'Bobby', 'url': href,
                                            'direct': True, 'debridonly': False})
                        else:
                            try:
                                host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                            except:
                                host = 'none'
                            if not host in hostprDict: continue
                            sources.append(
                                {'source': host, 'quality': quality, 'provider': 'Bobby', 'url': href, 'direct': False,
                                 'debridonly': False})
                return sources
        except:
            return sources

    def resolve(self, url):
        return url


def quality_tag(txt):
    if any(value in txt for value in ['1080', '1080p', '1080P']):
        quality = "1080p"

    elif any(value in txt for value in ['720', '720p', '720P']):
        quality = "HD"

    else:
        quality = "SD"
    return quality

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

import re,urllib,urlparse,hashlib,random,string,json,base64,requests
from nanscrapers.common import clean_title, random_agent, replaceHTMLCodes
from ..scraper import Scraper
from BeautifulSoup import BeautifulSoup
import xbmc
#import client - was just importing this into idle for the parseDOM

s = requests.session()

class source(Scraper):
    name = "watch5s"

    def __init__(self):
        self.domains = ['watch5s.to','pmovies.to', 'cmovieshd.com']
        self.base_link = 'http://pmovies.to'
        self.search_link = '/search/?q=%s+%s'
        self.stream_link = 'http://streaming.pmovies.to/videoplayback/%s?key=%s'
        
    def scrape_movie(self, imdb, title, year):
                try:
                    self.url = []
                    title = getsearch(title)
                    cleanmovie = clean_title(title)
                    query = self.search_link % (urllib.quote_plus(title),year)
                    query = urlparse.urljoin(self.base_link, query)
                    link = requests.get(query).text
                    html = BeautifulSoup(link)
                    r = html.findAll('div', attrs = {'class': 'ml-item'})
                    for links in r:
                        page_links = links.findAll('a')[0]
                        pageurl = page_links['href']
                        info = page_links['rel']
                        title = page_links['title']
                        info = info.encode('utf-8')
                        title = title.encode('utf-8')
                        # print("CMOVIES LINKS", pageurl,info,title)
                        if cleanmovie in clean_title(title):
                            infolink = requests.get(info).text
                            match_year = re.search('class="jt-info">(\d{4})<', infolink)
                            match_year = match_year.group(1)
                            # print("CMOVIES YEAR",match_year)
                            if year in match_year:
                                # print("CMOVIES PASSED") 
                                pageurl = pageurl.encode('utf-8')
                                url = pageurl + 'watch/'
                                referer = url
                                # print("CMOVIES PASSED",referer,url) 
                                link = BeautifulSoup(requests.get(url).text)
                                r = link.findAll('div', attrs = {'class': 'les-content'})
                                for item in r:
                                    try:
                                        vidlinks = item.findAll('a')[0]['href']
                                        vidlinks = vidlinks.encode('utf-8')
                                        # print('CMOVIES SERVER LINKS',vidlinks)
                                        self.url.append([vidlinks,referer])
                                    except:
                                            pass
                    #print("CMOVIES PASSED LINKS", self.url)
                    self.Sources(self.url)
                except:
                    return self.url

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            url = {'title': title, 'year': year}
            url = urllib.urlencode(url)
            self.tvshow(url, title, season, episode)
        except:
            return			

			
    def tvshow(self, url, title, season, episode):
                try:
                    self.url = []
                    data = urlparse.parse_qs(url)
                    data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
                    title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
                    year = data['year']
                    cleanmovie = clean_title(title)
                    data['season'], data['episode'] = season, episode
                    seasoncheck = "season%s" % season
                    episode = "%01d" % int(episode)
                    checktitle = cleanmovie + seasoncheck
                    seasonquery = "season+%s" % season
                    query = self.search_link % (urllib.quote_plus(title),seasonquery)
                    query = urlparse.urljoin(self.base_link, query)
                    link = BeautifulSoup(requests.get(query).text)
                    r = link.findAll('div', attrs = {'class': 'ml-item'})
                    for links in r:
                        page_links = links.findAll('a')[0]
                        pageurl = page_links['href']
                        info = page_links['rel']
                        title = page_links['title']
                        info = info.encode('utf-8')
                        title = title.encode('utf-8')
                        if checktitle == clean_title(title):
                            # print("CMOVIES LINKS", pageurl,info,title)
                            pageurl = pageurl.encode('utf-8')
                            ep_url = pageurl + 'watch/'
                            referer = ep_url
                            ep_links = BeautifulSoup(requests.get(ep_url).text)
                            r_ep = ep_links.findAll('div', attrs = {'class': 'les-content'})
                            for item in r_ep:
                                match = re.compile('<a href="(.*?)" class=.*?">Episode\s*(\d+)').findall(item.contents)
                                for href, ep_items in match:
                                    ep_items = '%01d' % int(ep_items)
                                    if ep_items == episode:
                                        self.url.append([href,referer])
                    self.Sources(self.url)
                except:
                    return
		
    def Sources(self, url):
        sources = []
        try:
            for movielink,referer in self.url:
                try:
                    # print("CMOVIES SOURCE LINKS", movielink)
                    referer = referer
                    pages = requests.get(movielink).text
                    scripts = re.findall('hash\s*:\s*"([^"]+)', pages)[0]
                    # print("CMOVIES SERVER SCRIPT", scripts)
                    if scripts:
                        token = self.__get_token()
                        key = hashlib.md5('(*&^%$#@!' + scripts[46:58]).hexdigest()
                        cookie = '%s=%s' % (key, token)	
                        stream_url = self.stream_link % (scripts, hashlib.md5('!@#$%^&*(' + token).hexdigest())
                        # print("CMOVIES PLAYABLE LINKS", stream_url)
                        headers = {'Referer': referer, 'User-Agent': random_agent(), 'Cookie': cookie}
                        req = s.get(stream_url, headers=headers, timeout=5).json()
                        playlist = req['playlist'][0]['sources']
                        #print playlist
                        for item in playlist:
                            url = item['file'].encode('utf-8')
                            r_quality =  item['label'].encode('utf-8')
                            if r_quality in ['1080', '1080p','1080P']:
                                quality = "1080p"
                            elif r_quality in ['720', '720p','720P']:
                                quality = "HD"
                            else: 
                                quality = "SD"
                            # print("CMOVIES playlist", quality ,url)
                            sources.append({'source': 'gvideo', 'quality': quality, 'scraper': 'Watch5s', 'url': url, 'direct': True})

                except:
                    pass

        except:
            pass
        return sources


    def resolve(self, url):
        if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
        else: url = url.replace('https://', 'http://')
        return url

		
    def __get_token(self):
        return ''.join(random.sample(string.digits + string.ascii_uppercase + string.ascii_lowercase, 16))

def getsearch(title):
    if title == None: return
    title = title.lower()
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\\\|/|\(|\)|\[|\]|\{|\}|-|:|;|\*|\?|"|\'|<|>|\_|\.|\?', '', title).lower()
    return title
		

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


import re,urllib,urlparse,hashlib,random,string,json,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import directstream

import requests
from BeautifulSoup import BeautifulSoup
from resources.lib.modules.common import random_agent
from resources.lib.modules import control

class source:
    def __init__(self):
        self.language = ['en']
        self.domains = ['123movies.to', '123movies.ru', '123movies.is', '123movies.gs', '123-movie.ru', '123movies-proxy.ru', '123movies.moscow', '123movies.msk.ru', '123movies.msk.ru', '123movies.unblckd.me']

        self.base_link = control.setting('onemovies_base')
        if self.base_link == '' or self.base_link == None:self.base_link = 'https://123movies.is'


        self.search_link = '/movie/search/%s'
        self.info_link = '/ajax/movie_load_info/%s'
        self.server_link = '/ajax/get_episodes/%s'
        self.direct_link = '/ajax/v2_load_episode/'
        self.embed_link = '/ajax/load_embed/'
        self.session = requests.Session()

    def request(self, url, headers, post):
        try:
            r = client.request(url, headers=headers, post=post)
            if r == None: return r

            if 'internetmatters.org' in r:
                url = re.findall('(?://.+?|)(/.+)', url)[0]
                url = urlparse.urljoin(self.base_link_2, url)
                r = client.request(url, headers=headers, post=post)

            return r
        except:
            return


    def movie(self, imdb, title, year):
        try:


            cleaned_title = cleantitle.get(title)
            title = cleantitle.getsearch(title)
                      
            q = self.search_link % (urllib.quote_plus(title))
            r = urlparse.urljoin(self.base_link, q)

            print ("ONEMOVIES EPISODES", r)
           
            headers = {'User-Agent': random_agent()}
            html = BeautifulSoup(requests.get(r, headers=headers, timeout=20).content)
            containers = html.findAll('div', attrs={'class': 'ml-item'})
            for result in containers:
               
                links = result.findAll('a')

                for link in links:
                    link_title = str(link['title'])
                   
                    href = str(link['href'])
                    info = str(link['data-url'])
                    # print("ONEMOVIES", link_title, href, info)
                    if cleantitle.get(link_title) == cleaned_title:
                        
                        html = requests.get(info, headers=headers).content
                        pattern = '<div class="jt-info">%s</div>' % year
                        match = re.findall(pattern, html)
                        if match:
							
							url = client.replaceHTMLCodes(href)
							print("ONEMOVIES MATCH", url)
							return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = cleantitle.getsearch(data['tvshowtitle'])

            season = '%01d' % int(season)
            episode = '%01d' % int(episode)
            query = (urllib.quote_plus(title)) + "+season+" + season
            q = self.search_link % (query)
            r = urlparse.urljoin(self.base_link, q)

            print ("ONEMOVIES EPISODES", r)
            checkseason = cleantitle.get(title) + "season" + season
            headers = {'User-Agent': random_agent()}
            html = BeautifulSoup(requests.get(r, headers=headers, timeout=20).content)
            containers = html.findAll('div', attrs={'class': 'ml-item'})
            for result in containers:
               
                links = result.findAll('a')

                for link in links:
                    link_title = str(link['title'])
                    href = str(link['href'])
                    href = client.replaceHTMLCodes(href)
                    if cleantitle.get(link_title) == checkseason:
                        ep_id = '?episode=%01d' % int(episode)
                        url = href + ep_id
                        # print("ONEMOVIES Passed", href)
                        return url

        except:
            return


    def onemovies_info(self, url):
        try:
            u = urlparse.urljoin(self.base_link, self.info_link)
            u = self.request(u % url, headers=None, post=None)

            q = client.parseDOM(u, 'div', attrs = {'class': 'jtip-quality'})[0]

            y = client.parseDOM(u, 'div', attrs = {'class': 'jt-info'})
            y = [i.strip() for i in y if i.strip().isdigit() and len(i.strip()) == 4][0]

            return (y, q)
        except:
            return



    def sources(self, url, hostDict, hostprDict):
        original_url = url
        sources = []
        try:
            

            if url == None: return sources
            referer = url
            headers = {'User-Agent': random_agent()}
            url = url.replace('/watching.html', '')
            request = self.session.get(url, headers=headers)
            html = request.content
            # print ("ONEMOVIES Source", html)
            try:
                url, episode = re.findall('(.+?)\?episode=(\d*)$', url)[0]
            except:
                episode = None
            vid_id = re.findall('-(\d+)', url)[-1]
            getc = re.findall(r'<img title=.*?src="(.*?)"', html, re.I | re.DOTALL)[0]
            cookie = get_cookie(getc, original_url, self.session)
            print ("ONEMOVIES vid_id", vid_id)
            quality = re.findall('<span class="quality">(.*?)</span>', html)
            quality = str(quality)
            if quality == 'cam' or quality == 'ts':
                quality = 'CAM'
            elif quality == 'hd':
                quality = '720'
            else:
                quality = '480'
            try:
                headers = {'X-Requested-With': 'XMLHttpRequest'}
                headers['Referer'] = referer
                headers[
                    'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
                u = urlparse.urljoin(self.base_link, self.server_link % vid_id)
                print("ONEMOVIES SERVERS", u)
                request = self.session.get(u, headers=headers)
                r = BeautifulSoup(request.content)
                print("ONEMOVIES SERVERS", r)
                containers = r.findAll('div', attrs={'class': 'les-content'})
                for result in containers:
                    try:
                        links = result.findAll('a')
                        print("ONEMOVIES links", links)
                        for link in links:
                            title = str(link['title'])
                            # print("ONEMOVIES TITLE", title)
                            if not episode == None:
                                title = re.findall('Episode\s+(\d+):', title)[0]
                                title = '%01d' % int(title)
                                if title == episode:
                                    episode_id = str(link['episode-id'])
                                # print("ONEMOVIES EPISODE", episode_id)
                                else:
                                    continue

                            else:
                                episode_id = str(link['episode-id'])
                            onclick = str(link['onclick'])

                            key_gen = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(16))
                            ################# FIX FROM MUCKY DUCK & XUNITY TALK ################
                            key = '87wwxtp3dqii'
                            key2 = '7bcq9826avrbi6m49vd7shxkn985mhod'
                            coookie = hashlib.md5(episode_id + key).hexdigest() + '=%s' % key_gen
                            cookie = '%s; %s' % (cookie, coookie)
                            a = episode_id + key2
                            b = key_gen
                            # i = b[-1]
                            # h = b[:-1]
                            # b = i + h + i + h + i + h
                            hash_id = uncensored(a, b)
                            ################# FIX FROM MUCKY DUCK & XUNITY TALK ################

                            serverurl = self.base_link + '/ajax/v2_get_sources/' + episode_id + '?hash=' + urllib.quote(
                                    hash_id)
                            print ("ONEMOVIES playurl", serverurl)

                            headers = {'Accept-Language' : 'en-US',
                                       'Accept-Encoding' : 'gzip, deflate, sdch',
                                       'Cookie'          : cookie,
                                       'Referer'         : referer,
                                       'x-requested-with': 'XMLHttpRequest',
                                       'Accept'          : 'application/json, text/javascript, */*; q=0.01',
                                       'User-Agent'      : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
                                       }
                            # print ("playurl ONEMOVIES", headers)
                            result = self.session.get(serverurl, headers=headers).content
                            # print ("RESULT ONEMOVIES", result)
                            result = result.replace('\\', '')
                            print ("ONEMOVIES Result", result)
                            url = re.findall('"?file"?\s*:\s*"(.+?)"', result)
                            url = [directstream.googletag(i) for i in url]
                            url = [i[0] for i in url if len(i) > 0]
                            u = []
                            try:
                                u += [[i for i in url if i['quality'] == '1080p'][0]]
                            except:
                                pass
                            try:
                                u += [[i for i in url if i['quality'] == 'HD'][0]]
                            except:
                                pass
                            try:
                                u += [[i for i in url if i['quality'] == 'SD'][0]]
                            except:
                                pass
                            url = client.replaceHTMLCodes(u[0]['url'])
                            quality = directstream.googletag(url)[0]['quality']

                            # print ("ONEMOVIES PLAY URL", quality, url)

                            sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'Onemovies', 'url': url, 'direct': True, 'debridonly': False})
                    except:
                        pass
            except:
                pass

        except:
            pass
        return sources


    def resolve(self, url):
            return url



def __jav(a):
    b = str(a)
    code = ord(b[0])
    if 0xD800 <= code and code <= 0xDBFF:
        c = code
        if len(b) == 1:
            return code
        d = ord(b[1])
        return ((c - 0xD800) * 0x400) + (d - 0xDC00) + 0x10000

    if 0xDC00 <= code and code <= 0xDFFF:
        return code
    return code


def uncensored(a, b):
    c = ''
    i = 0
    for i, d in enumerate(a):
        e = b[i % len(b) - 1]
        d = int(__jav(d) + __jav(e))
        c += chr(d)

    return base64.b64encode(c)

def googletag(url):
    quality = re.compile('itag=(\d*)').findall(url)
    quality += re.compile('=m(\d*)$').findall(url)
    try:
        quality = quality[0]
    except:
        return []

    if quality in ['37', '137', '299', '96', '248', '303', '46']:
        return [{'quality': '1080', 'url': url}]
    elif quality in ['22', '84', '136', '298', '120', '95', '247', '302', '45', '102']:
        return [{'quality': '720', 'url': url}]
    elif quality in ['35', '44', '135', '244', '94']:
        return [{'quality': '480', 'url': url}]
    elif quality in ['18', '34', '43', '82', '100', '101', '134', '243', '93']:
        return [{'quality': '480', 'url': url}]
    elif quality in ['5', '6', '36', '83', '133', '242', '92', '132']:
        return [{'quality': '480', 'url': url}]
    else:
        return []


def get_cookie(url, referer, session):
    headers = {'Accept'         : 'image/webp,image/*,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, sdch, br',
               'Accept-Language': 'en-US,en;q=0.8',
               'Referer'        : referer,
               'User-Agent'     : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
               }
    request = session.get(url, headers=headers)
    cookie = request.cookies.get_dict()
    newcookie = ""
    for i in cookie:
        newcookie = i + '=' + cookie[i]
    return newcookie

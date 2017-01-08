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
custom_url = control.setting('onemovies_custom')

class source:
    def __init__(self):
        self.language = ['en']
        self.domains = ['123movies.to', '123movies.ru', '123movies.is', '123movies.gs', '123-movie.ru', '123movies-proxy.ru', '123movies.moscow', '123movies.msk.ru', '123movies.msk.ru', '123movies.unblckd.me']

        if custom_url == 'true': self.base_link = control.setting('onemovies_base')
        else: self.base_link = 'http://123movies.gs'


        self.base_link_2 = 'http://123movies.msk.ru'
        self.search_link = '/ajax/suggest_search'
        self.search_link_2 = '/movie/search/%s'
        self.info_link = '/ajax/movie_load_info/%s'
        self.server_link = '/ajax/get_episodes/%s'
        self.direct_link = '/ajax/v2_load_episode/'
        self.embed_link = '/ajax/load_embed/'


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
                      
            q = self.search_link_2 % (urllib.quote_plus(title))
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
            q = self.search_link_2 % (query)
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
        try:
            sources = []

            if url == None: return sources
            if not "http:" in url: url = urlparse.urljoin(self.base_link, url)
			
            url = referer = url.replace('/watching.html', '')

            try: url, episode = re.findall('(.+?)\?episode=(\d*)$', url)[0]
            except: episode = None
            vid_id = re.findall('-(\d+)', url)[-1]
			
            print("ONEMOVIES SOURCES URL", url)
           
            headers = {'User-Agent': random_agent()}
            html = requests.get(url, headers=headers).content


            quality = re.findall('<span class="quality">(.+?)</span>', html)[0]
            quality = str(quality)
            if quality == '1080':
                quality = '1080p'
            elif quality.lower() == 'hd':
                quality = 'HD'
            else:
                quality = 'SD'
            print("ONEMOVIES quality URL", quality)

            try:
                headers = {'X-Requested-With': 'XMLHttpRequest', 'Referer': url}

                u = urlparse.urljoin(self.base_link, self.server_link % vid_id)

                r = self.request(u, headers=headers, post=None)

                r = client.parseDOM(r, 'div', attrs = {'class': 'les-content'})
                r = zip(client.parseDOM(r, 'a', ret='onclick'), client.parseDOM(r, 'a'))
                r = [(i[0], ''.join(re.findall('(\d+)', i[1])[:1])) for i in r]

                if not episode == None:
                    r = [i[0] for i in r if '%01d' % int(i[1]) == episode]
                else:
                    r = [i[0] for i in r]

                r = [re.findall('(\d+),(\d+)', i) for i in r]
                r = [i[0][:2] for i in r if len(i) > 0]

                links = []

                links += [{'source': 'gvideo', 'url': self.direct_link + i[1], 'direct': True} for i in r if 2 <= int(i[0]) <= 11]

                links += [{'source': 'openload.co', 'url': self.embed_link + i[1], 'direct': False} for i in r if i[0] == '14']

                links += [{'source': 'videowood.tv', 'url': self.embed_link + i[1], 'direct': False} for i in r if i[0] == '12']

                head = '|' + urllib.urlencode(headers)

                for i in links: sources.append({'source': i['source'], 'quality': quality, 'provider': 'Onemovies', 'url': urlparse.urljoin(self.base_link, i['url']) + head, 'direct': i['direct'], 'debridonly': False})
            except:
                pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try: headers = dict(urlparse.parse_qsl(url.rsplit('|', 1)[1]))
        except: headers = None

        link = url.split('|')[0]

        try:
            if not self.direct_link in link: raise Exception()

            video_id = headers['Referer'].split('-')[-1].replace('/','')

            episode_id = link.split('/')[-1]

            key = '87wwxtp3dqii' ; key2 = '7bcq9826avrbi6m49vd7shxkn985mhod'

            h = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(16))

            a = episode_id + key2 ; b = h[-1]+h[:-1]+h[-1]+h[:-1]+h[-1]+h[:-1]
            hash_id = uncensored(a, b)

            cookie = hashlib.md5(episode_id + key).hexdigest() + '=%s' % h

            url = self.base_link + '/ajax/v2_get_sources/' + episode_id + '?hash=' + urllib.quote(hash_id)

            headers['Referer'] = headers['Referer']+ '\+' + cookie
            headers['Cookie'] = cookie

            result = self.request(url, headers=headers, post=None)
            result = result.replace('\\','')

            url = re.findall('"?file"?\s*:\s*"(.+?)"', result)
            url = [directstream.googletag(i) for i in url]
            url = [i[0] for i in url if len(i) > 0]

            u = []
            try: u += [[i for i in url if i['quality'] == '1080p'][0]]
            except: pass
            try: u += [[i for i in url if i['quality'] == 'HD'][0]]
            except: pass
            try: u += [[i for i in url if i['quality'] == 'SD'][0]]
            except: pass

            url = client.replaceHTMLCodes(u[0]['url'])
            url = directstream.googlepass(url)
            return url
        except:
            pass

        try:
            if not self.embed_link in link: raise Exception()

            result = self.request(link, headers=headers, post=None)

            url = json.loads(result)['embed_url']
            return url
        except:
            pass


def uncensored(a,b):
    n = -1
    x=[]
    z=[]
    while True:
        if n == len(a)-1:
            break
        n +=1
        d = int(''.join(str(ord(c)) for c in a[n]))
        e=int(''.join(str(ord(c)) for c in b[n]))
        z.append(d+e)
        x.append(chr(d+e))
    return base64.b64encode(''.join(x))



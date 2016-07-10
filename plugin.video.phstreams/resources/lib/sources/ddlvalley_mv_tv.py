# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 Exodus

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


import re,urllib,urlparse,time,datetime

from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import debrid


class source:
    def __init__(self):
        self.domains = ['ddlvalley.cool']
        self.base_link = 'http://www.ddlvalley.cool'
        self.search_link = '/search/%s/'


    def movie(self, imdb, title, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
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
            if url == None: return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            if debrid.status() == False: raise Exception()

            dt = int(datetime.datetime.now().strftime('%Y%m%d'))
            mt = {'jan':'1', 'feb':'2', 'mar':'3', 'apr':'4', 'may':'5', 'jun':'6', 'jul':'7', 'aug':'8', 'sep':'9', 'oct':'10', 'nov':'11', 'dec':'12'}

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            hdlr = ['S%02dE%02d' % (int(data['season']), int(data['episode']))] if 'tvshowtitle' in data else ['%s' % str(data['year'])]

            query = '%s S%02dE%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            query = re.sub('(\\\|/|:|;|\*|\?|"|\'|<|>|\|)', '', query)
            query = self.search_link % urllib.quote_plus(query)
            query = urlparse.urljoin(self.base_link, query)

            r = client.request(query)

            r = client.parseDOM(r, 'div', attrs = {'class': 'pb fl'})[0]
            r = r.split('<h2>')

            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a'), client.parseDOM(i, 'span', attrs = {'class': 'date'})) for i in r]
            r = [(i[0][0], i[1][0], i[2][-1]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            r = [(i[0], i[1], i[2]) for i in r]

            r = [(i[0], i[1], re.findall('(\w+).+?(\d+).+?(\d{4})', i[2])) for i in r]
            r = [(i[0], i[1], '%04d%02d%02d' % (int(i[2][0][2]), int(mt[i[2][0][0][:3].lower()]), int(i[2][0][1]))) for i in r if len(i[2]) > 0]
            r = [(i[0], i[1], (abs(dt - int(i[2])) < control.integer * 10)) for i in r]
            r = [(i[0], i[1]) for i in r if i[2] == True]

            r = [(i[0], (re.sub('<.+?>|</.+?>', '', client.replaceHTMLCodes(i[1]))).split('">')[-1]) for i in r]
            r = [(i[0], re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|3D)(\.|\)|\]|\s|)(.+|)', '', i[1]), re.findall('[\.|\(|\[|\s](\d{4}|S\d*E\d*)([\.|\)|\]|\s|].+)', i[1])) for i in r]
            r = [(i[0], i[1], i[2][0][0], i[2][0][1]) for i in r if len(i[2]) > 0]
            r = [(i[0], i[1], i[2], re.split('\.|\(|\)|\[|\]|\s|\-', i[3])) for i in r]

            r = [i for i in r if not any(x in i[3] for x in ['HDCAM', 'CAM', 'DVDR', 'DVDRip', 'DVDSCR', 'HDTS', 'TS', '3D'])]
            r = [i for i in r if cleantitle.get(title) == cleantitle.get(i[1])]
            r = [i for i in r if any(x in i[2] for x in hdlr)]

            l = [(i[0], '1080p') for i in r if '1080p' in i[3]]
            l += [(i[0], 'HD') for i in r if '720p' in i[3]]
            l = l[:4]

            links = []

            for i in l:
                try:
                    r = urlparse.urljoin(self.base_link, i[0])
                    r = client.replaceHTMLCodes(r)
                    r = client.request(r)
                    r = r.replace('\n', '')
                    r = re.sub('\s\s+', ' ', r)
                    r = re.compile("<span class='info2'(.+)").findall(r)[0]
                    r = r.split("<span class='info2'")[-1].split('<span')[0]
                    r = client.parseDOM(r, 'a', ret='href')
                    for url in r: links.append({'url': url, 'quality': i[1]})
                except:
                    pass

            for i in links:
                try:
                    url = i['url']
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    if not host in hostprDict: raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    sources.append({'source': host, 'quality': i['quality'], 'provider': 'DDLvalley', 'url': url, 'direct': False, 'debridonly': True})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return url



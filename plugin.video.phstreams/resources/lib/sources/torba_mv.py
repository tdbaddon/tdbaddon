# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 lambda

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


import re,os,urllib,urlparse

from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import client


class source:
    def __init__(self):
        self.domains = ['torba.se']
        self.base_link = 'http://torba.se'
        self.search_link = '/search?title=%s'
        self.player_link = '/v/%s'


    def movie(self, imdb, title, year):
        try:
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query)

            title = cleantitle.get(title)
            years = ['%s' % str(year), '%s' % str(int(year)+1), '%s' % str(int(year)-1)]

            result = client.parseDOM(result, 'li', attrs = {'class': 'films-item'})
            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'div', attrs = {'class': 'films-item-title'}), client.parseDOM(i, 'div', attrs = {'class': 'films-item-year'})) for i in result]
            result = [(i[0][0], i[1][0], i[2][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            result = [(i[0], re.sub('<.+?>|</.+?>', '', i[1]), re.sub('<.+?>|</.+?>', '', i[2])) for i in result]
            result = [i for i in result if title == cleantitle.get(i[1])]
            result = [i[0] for i in result if any(x in i[2] for x in years)][0]

            url = [i for i in result.split('/') if not i == ''][-1]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, self.player_link % url)

            result = client.source(url)

            url = netloc = client.parseDOM(result, 'a', ret='href', attrs = {'class': 'video-play'})[0]
            url = '/embed/' + url.split('#')[-1]
            url = urlparse.urljoin(netloc, url)

            result = client.source(url)

            url = re.compile('file\s*:\s*"([^"]+)').findall(result)
            url = [i for i in url if '.m3u8' in i][0]
            url = urlparse.urljoin(netloc, url)

            result = client.source(url)

            audio_group, audio_stream = re.compile('#EXT-X-MEDIA.*?GROUP-ID="([^"]+).*?URI="([^"]+)').findall(result)[0]

            result = result.split('#EXT-X-STREAM-INF')
            result = [i.split('\n') for i in result]
            result = [i[:2] for i in result if len(i) >= 2]
            result = [(re.compile('BANDWIDTH=(\d+).*?NAME="(\d+)').findall(i[0]), urlparse.urljoin(netloc, i[1])) for i in result]
            result = [{'audio_group': audio_group, 'audio_stream': audio_stream, 'stream_name': i[0][0][1], 'bandwidth': i[0][0][0], 'video_stream': i[1]} for i in result if len(i[0]) > 0]

            links = [(i, '1080p') for i in result if int(i['stream_name']) >= 1080]
            links += [(i, 'HD') for i in result if 720 <= int(i['stream_name']) < 1080]
            links += [(i, 'SD') for i in result if 360 <= int(i['stream_name']) < 720]

            for i in links: sources.append({'source': 'cdn', 'quality': i[1], 'provider': 'Torba', 'url': urllib.urlencode(i[0]), 'direct': True, 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            content = [
            '#EXTM3U',
            '#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="{audio_group}",DEFAULT=YES,AUTOSELECT=YES,NAME="Stream 1",URI="{audio_stream}"',
            '',
            '#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH={bandwidth},NAME="{stream_name}",AUDIO="{audio_group}"',
            '{video_stream}']

            url = urlparse.parse_qs(url)
            url = dict([(key, url[key][0]) if url[key] else (key, '') for key in url])
            url = ('\n'.join(content)).format(**url)

            path = os.path.join(control.dataPath, 'torbase.m3u8')

            control.makeFile(control.dataPath) ; control.deleteFile(path)

            file = control.openFile(path, 'w') ; file.write(url) ; file.close()

            return path
        except:
            return



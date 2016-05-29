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


import re,os,json,urllib,urlparse

from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import workers


class source:
    def __init__(self):
        self.domains = ['torba.se']
        self.base_link = 'http://torba.se'
        self.search_mv_link = '/movies/autocomplete?order=relevance&title=%s'
        self.search_tv_link = '/series/autocomplete?order=relevance&title=%s'
        self.tv_link = '/series/%s/%s/%s'
        self.mv_link = '/v/%s'


    def movie(self, imdb, title, year):
        try:
            query = self.search_mv_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)

            r = client.request(query, headers={'X-Requested-With': 'XMLHttpRequest'})
            r = json.loads(r)

            t = cleantitle.get(title)

            r = [(i['slug'], i['title'], i['year']) for i in r]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == str(i[2])][0]

            url = r.encode('utf-8')
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            query = self.search_tv_link % (urllib.quote_plus(tvshowtitle))
            query = urlparse.urljoin(self.base_link, query)

            r = client.request(query, headers={'X-Requested-With': 'XMLHttpRequest'})
            r = json.loads(r)

            t = cleantitle.get(tvshowtitle)

            r = [(i['slug'], i['title'], i['year']) for i in r]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == str(i[2])][0]

            url = r.encode('utf-8')
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        if url == None: return

        url = '%s/%01d/%01d' % (url, int(season), int(episode))
        url = url.encode('utf-8')
        return url


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            try: url = self.tv_link % re.findall('(.+?)/(\d*)/(\d*)$', url)[0]
            except: url = self.mv_link % url

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)

            url = client.parseDOM(r, 'a', ret='href', attrs = {'class': 'video-play.+?'})[0]
            url = re.findall('(?://|\.)streamtorrent\.tv/.+?/([0-9a-zA-Z/]+)', url)[0]
            url = 'https://streamtorrent.tv/api/torrent/%s.json' % url

            r = client.request(url)
            r = json.loads(r)

            url = [i for i in r['files'] if 'streams' in i and len(i['streams']) > 0][0]
            url = 'https://streamtorrent.tv/api/torrent/%s/%s.m3u8' % (r['_id'], url['_id'])

            r = client.request(url)

            audio = re.findall('#EXT-X-MEDIA:TYPE=AUDIO.*?GROUP-ID="([^"]+).*?URI="([^"]+)', r)

            video = [i.split('\n') for i in r.split('#EXT-X-STREAM-INF')]
            video = [i[:2] for i in video if len(i) >= 2]
            video = [(re.findall('BANDWIDTH=(\d+).*?NAME="(\d+)', i[0]), urlparse.urljoin(url, i[1])) for i in video]
            video = [(i[0][0][0], i[0][0][1], i[1]) for i in video if len(i[0]) > 0]

            try: r = [{'bandwidth': i[0], 'stream_name': i[1], 'video_stream': i[2], 'audio_group': audio[0][0], 'audio_stream': audio[0][1]} for i in video]
            except: r = [{'bandwidth': i[0], 'stream_name': i[1], 'video_stream': i[2]} for i in video]

            links = []
            links += [{'quality': '1080p', 'url': urllib.urlencode(i)} for i in r if int(i['stream_name']) >= 1080]
            links += [{'quality': 'HD', 'url': urllib.urlencode(i)} for i in r if 720 <= int(i['stream_name']) < 1080]
            links += [{'quality': 'SD', 'url': urllib.urlencode(i)} for i in r if int(i['stream_name']) <= 720]
            links = links[:3]

            for i in links: sources.append({'source': 'cdn', 'quality': i['quality'], 'provider': 'Torba', 'url': i['url'], 'direct': True, 'debridonly': False, 'autoplay': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            m3u8 = [

                [
                '#EXTM3U',
                '',
                '#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH={bandwidth},NAME="{stream_name}"',
                '{video_stream}'
                ],

                [
                '#EXTM3U',
                '#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="{audio_group}",DEFAULT=YES,AUTOSELECT=YES,NAME="Stream 1",URI="{audio_stream}"',
                '',
                '#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH={bandwidth},NAME="{stream_name}",AUDIO="{audio_group}"',
                '{video_stream}'
                ]

                ]

            query = urlparse.parse_qs(url)
            query = dict([(key, query[key][0]) if query[key] else (key, '') for key in query])

            for i in m3u8:
                try: content = ('\n'.join(i)).format(**query)
                except: pass


            auth = query['video_stream']

            r = client.request(auth, headers={'User-Agent': 'Lavf/56.40.101'})
            try: url = json.loads(r)['url']
            except: url = None

            if not url == None:

                def dialog(url):
                    try: self.disableScraper = control.yesnoDialog('To watch this video visit from any device', '[COLOR skyblue]%s[/COLOR]' % url, '', 'Torba', 'Cancel', 'Settings')
                    except: pass

                workers.Thread(dialog, url).start()
                control.sleep(3000)

                for i in range(100):
                    try:
                        if not control.condVisibility('Window.IsActive(yesnoDialog)'): break

                        r = client.request(auth, headers={'User-Agent': 'Lavf/56.40.101'})
                        try: url = json.loads(r)['url']
                        except: url = None

                        if url == None: break

                        workers.Thread(dialog, url).start()
                        control.sleep(3000)
                    except:
                        pass

                if self.disableScraper:
                    control.openSettings(query='2.0')
                    return ''

                control.execute('Dialog.Close(yesnoDialog)')


            if not url == None: return

            path = os.path.join(control.dataPath, 'torbase.m3u8')

            control.makeFile(control.dataPath) ; control.deleteFile(path)

            file = control.openFile(path, 'w') ; file.write(content) ; file.close()

            return path
        except:
            return



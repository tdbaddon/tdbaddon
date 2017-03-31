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


import re,urllib,urlparse,json,random,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import control
debridstatus = control.setting('debridsources')
# if not debridstatus == 'true': raise Exception()
from schism_meta import meta_quality, meta_host, meta_info
class source:
    def __init__(self):
        self.domains = ['directdownload.tv']
        self.base_link = 'http://directdownload.tv'
        self.search_link = '/api?key=4B0BB862F24C8A29&quality[]=HDTV&quality[]=DVDRIP&quality[]=720P&quality[]=WEBDL&quality[]=WEBDL1080P&quality[]=1080P-X265&limit=50&keyword='



    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'tvshowtitle': tvshowtitle}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            if not debridstatus == 'true': raise Exception()

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
		
            url['title'], url['season'], url['episode'] = title, season, episode
			
            print ("DIRECTDL EPISODE", url)
            url = urllib.urlencode(url)
            return url
        except:
            return





    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            links = []
            if url == None: return sources

            if not debridstatus == 'true': raise Exception()

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])



            if not 'tvshowtitle' in data: raise Exception()

                

            f = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
            t = data['tvshowtitle'].encode('utf-8')
				
            check = cleantitle.get(t) + f
				

            q = self.search_link + urllib.quote_plus('%s %s' % (t, f))
            q = urlparse.urljoin(self.base_link, q)
            print ("DIRECTDL EPISODE 2", q)
            result = client.request(q)
            result = json.loads(result)


            for i in result:
                try:
                    if not cleantitle.get(t) == cleantitle.get(i['showName']): raise Exception()

                    y = i['release'].encode('utf-8')
                    
                    if not check.lower() in cleantitle.get(y): raise Exception()

                    quality = i['quality']

                    size = i['size']
                    size = float(size)/1024
                    size = '%.2f GB |' % size

                    if 'X265' in quality: info = '%s | HEVC' % size
                    else: info = size

                    quality = meta_quality(quality)
                    info = meta_info(y)
                    info = size + info

                    url = i['links']
                    # for x in url.keys(): 
					
						# url = url[x][0]
					
                    links.append([quality,info,url])
					




						# host = meta_host(url)


						# sources.append({'source': host, 'quality': quality, 'provider': 'DirectDL', 'url': url, 'direct': False, 'debridonly': True})
                except:
                    pass
					
            for quality,info,item in links:
				for x in item.keys(): 
					url = item[x][0].encode('utf-8')
					host = meta_host(url)
					if quality == 'SD': quality = meta_quality(url)
					sources.append({'source': host, 'quality': quality, 'provider': 'DirectDL', 'url': url, 'info': info, 'direct': False, 'debridonly': True})
					# print ("DIRECTDL LINKS", item[x])

            return sources
        except:
            return sources


    def resolve(self, url):



            return url




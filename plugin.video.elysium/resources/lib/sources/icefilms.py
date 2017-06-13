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


import re,urllib,urlparse,json,random,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client, control
from resources.lib.modules import cache
from BeautifulSoup import BeautifulSoup
debridstatus = control.setting('debridsources')

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['directdownload.tv']
        self.b_link = 'http://www.icefilms.info'
        self.u_link = self.b_link + '/membersonly/components/com_iceplayer/video.php?h=374&w=631&vid=%s&img='
        self.r_link = self.b_link + '/ip.php?v=%s&'
        self.j_link = self.b_link + '/membersonly/components/com_iceplayer/video.phpAjaxResp.php?s=%s&t=%s'
        self.p_link = 'id=%s&s=%s&iqs=&url=&m=%s&cap=+&sec=%s&t=%s'


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


    def request(self, url, post=None, cookie=None, referer=None, output='', close=True):
        try:
            headers = {'Accept': '*/*'}
            if not cookie == None: headers['Cookie'] = cookie
            if not referer == None: headers['Referer'] = referer
            result = client.request(url, post=post, headers=headers, output=output, close=close)
            result = result.decode('iso-8859-1').encode('utf-8')
            result = urllib.unquote_plus(result)
            return result
        except:
            return


    def directdl_cache(self, url):
        try:
            url = urlparse.urljoin(self.b_link, url)
            result = self.request(url)
            result = re.compile('id=(\d+)>.+?href=(.+?)>').findall(result)
            result = [(re.sub('http.+?//.+?/','/', i[1]), 'tt' + i[0]) for i in result]
            return result
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources
            if not debridstatus == 'true': raise Exception()
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])







            try:
                q = ('/tv/a-z/%s', data['tvshowtitle']) if 'tvshowtitle' in data else ('/movies/a-z/%s', data['title'])
                q = q[0] % re.sub('^THE\s+|^A\s+', '', q[1].strip().upper())[0]

                url = cache.get(self.directdl_cache, 120, q)
                url = [i[0] for i in url if data['imdb'] == i[1]][0]
                url = urlparse.urljoin(self.b_link, url)
                print ("ICEFILM 1", url)
                try: v = urlparse.parse_qs(urlparse.urlparse(url).query)['v'][0]
                except: v = None

                if v == None:
                    result = self.request(url)
                    url = re.compile('(/ip[.]php.+?>)%01dx%02d' % (int(data['season']), int(data['episode']))).findall(result)[0]
                    url = re.compile('(/ip[.]php.+?)>').findall(url)[-1]
                    url = urlparse.urljoin(self.b_link, url)

                url = urlparse.parse_qs(urlparse.urlparse(url).query)['v'][0]

                u = self.u_link % url ; r = self.r_link % url
                j = self.j_link ; p = self.p_link

                result = self.request(u, referer=r)
                result2 =  BeautifulSoup(result)
                secret = re.compile('lastChild\.value="([^"]+)"(?:\s*\+\s*"([^"]+))?').findall(result)[0]
                secret = ''.join(secret)
                print("ICEFILM 3",secret)
                t = re.compile('"&t=([^"]+)').findall(result)[0]
                print("ICEFILM 4",t)
                s_start = re.compile('(?:\s+|,)s\s*=(\d+)').findall(result)[0]
                m_start = re.compile('(?:\s+|,)m\s*=(\d+)').findall(result)[0]
                print("ICEFILM 5",s_start, m_start)
                img = re.compile('<iframe[^>]*src="([^"]+)').findall(result)
                img = img[0] if len(img) > 0 else '0'
                img = urllib.unquote(img)
                print("ICEFILM 6", img)
                result = result2.findAll('div', attrs = {'class': 'ripdiv'})
                for item in result:
					
					print ("ICEFILM 7", item)
                
					quality = re.findall('<b>(.*?)</b>', str(item))[0]
					print ("ICEFILM 8", quality)
					result = item.findAll('p')
					print ("ICEFILM 9", result)
					if any(x in quality for x in ['1080p', '720p', 'HD']): quality = 'HD'
					else: quality = 'SD'
					for container in result:
						h = container.findAll('a')
						
						for links in h:
							hosts = re.sub('(</?[^>]*>)', '', str(links))
							host = hosts.split(' ')[-1]
							host = get_provider(host)
							if not host in hostprDict: raise Exception()
							id = links['onclick'].encode('utf-8')
							id = re.compile('[(](.+?)[)]').findall(id)[0]
							print ("ICEFILM 10", host, id)

							s = int(s_start) + random.randint(3, 1000)
							m = int(m_start) + random.randint(21, 1000)
							
							url = j % (id, t) + '|' + p % (id, s, m, secret, t)
							url += '|%s' % urllib.urlencode({'Referer': u, 'Img': img})
							url = url.encode('utf-8')
							print("ICEFILM URL", url)
							sources.append({'source': host, 'quality': quality, 'provider': 'Icefilms', 'url': url, 'direct': False, 'debridonly': True})


            except:
				pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            b = urlparse.urlparse(url).netloc
            b = re.compile('([\w]+[.][\w]+)$').findall(b)[0]

            if not b in self.b_link: return url
 
            u, p, h = url.split('|')
            r = urlparse.parse_qs(h)['Referer'][0]
            #u += '&app_id=Exodus'

            c = self.request(r, output='cookie', close=False)
            result = self.request(u, post=p, referer=r, cookie=c)

            url = result.split('url=')
            url = [urllib.unquote_plus(i.strip()) for i in url]
            url = [i for i in url if i.startswith('http')]
            url = url[-1]

            return url
        except:
            return


def get_provider(link):
		link = str(link).lower()
		table = {
				'180upload': 		'180upload.com',
				'hugefiles':		'hugefiles.net',
				'clicknupload':		'clicknupload.com',
				'tusfiles':			'tusfiles.net',
				'xfileload':		'xfileload.com',
				'mightyupload':		'mightyupload.com',
				'movreel':			'movreel.com',
				'donevideo':		'donevideo.com',
				'vidplay':			'vidplay.net',
				'24uploading':		'24uploading.com',
				'xvidstage':		'xvidstage.com',
				'2shared':			'2shared.com',
				'upload':			'upload.af',
				'uploadx':			'uploadx.org',
				'kingfiles':		'kingfiles.net',
				'openload':			'openload.co',
				'uploadz':			'uploadz.co',
				'fileweed':			'fileweed.net',
				'filehoot':			'filehoot.com'
		}
		if link in table.keys():
			return table[link]
		else: 
			link = '0'
			return link
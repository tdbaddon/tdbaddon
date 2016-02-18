# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

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


import re,urllib,urlparse,json
from resources.lib.modules import client
import xbmcgui


domains = ['google.com']


def resolve(url):
    try:
        netloc = urlparse.urlparse(url.strip().lower()).netloc
        netloc = netloc.split('.google')[0]



        if netloc == 'docs' or netloc == 'drive':
            url = url.split('/preview', 1)[0]
            url = url.replace('drive.google.com', 'docs.google.com')

            result = client.request(url, headers={'User-Agent': client.agent()})

            result = re.compile('"fmt_stream_map",(".+?")').findall(result)[0]

            result = json.loads(result)
            result = [i.split('|')[-1] for i in result.split(',')]
            result = sum([tag(i) for i in result], [])



        elif netloc == 'photos':
            result = client.request(url, headers={'User-Agent': client.agent()})

            result = result.replace('\r','').replace('\n','').replace('\t','')
            result = re.compile('"\d*/\d*x\d*.+?","(.+?)"').findall(result)[0]

            result = result.replace('\\u003d','=').replace('\\u0026','&')
            result = re.compile('url=(.+?)&').findall(result)
            result = [urllib.unquote(i) for i in result]

            result = [tag(i)[0] for i in result]



        elif netloc == 'picasaweb':
            id = re.compile('#(\d*)').findall(url)[0]

            result = client.request(url, headers={'User-Agent': client.agent()})

            result = re.search('feedPreload:\s*(.*}]}})},', result, re.DOTALL).group(1)
            result = json.loads(result)['feed']['entry']

            if len(result) > 1: result = [i for i in result if str(id) in i['link'][0]['href']][0]
            elif len(result) == 1: result = result[0]

            result = result['media']['content']
            result = [i['url'] for i in result if 'video' in i['type']]
            result = sum([tag(i) for i in result], [])



        elif netloc == 'plus':
            result = client.source(url, headers={'User-Agent': client.agent()})

            id = (urlparse.urlparse(url).path).split('/')[-1]
            result = result.replace('\r','').replace('\n','').replace('\t','')
            result = result.split('"%s"' % id)[-1].split(']]')[0]

            result = result.replace('\\u003d','=').replace('\\u0026','&')
            result = re.compile('url=(.+?)&').findall(result)
            result = [urllib.unquote(i) for i in result]

            result = [tag(i)[0] for i in result]



        url = []
        try: url += [[i for i in result if i['quality'] == '1080p'][0]]
        except: pass
        try: url += [[i for i in result if i['quality'] == '720p'][0]]
        except: pass
        try: url += [[i for i in result if i['quality'] == '480p'][0]]
        except: pass
        try: url += [[i for i in result if i['quality'] == '360p'][0]]
        except: pass
        try: url += [[i for i in result if i['quality'] == '240p'][0]]
        except: pass

        if len(url) == 0:
            return
        elif len(url) == 1:
            return url[0]['url']
        else:
            q = ['GoogleVideo - %s' % i['quality'] for i in url]
            u = [i['url'] for i in url]
            select = xbmcgui.Dialog().select('Choose a linkz', q)
            if select == -1: return
            return u[select]
    except:
        return


def tag(url):
    quality = re.compile('itag=(\d*)').findall(url)
    quality += re.compile('=m(\d*)$').findall(url)
    try: quality = quality[0]
    except: return []

    if quality in ['37', '137', '299', '96', '248', '303', '46']:
        return [{'quality': '1080p', 'url': url}]
    elif quality in ['22', '84', '136', '298', '120', '95', '247', '302', '45', '102']:
        return [{'quality': '720p', 'url': url}]
    elif quality in ['35', '44', '135', '244', '94']:
        return [{'quality': '480p', 'url': url}]
    elif quality in ['18', '34', '43', '82', '100', '101', '134', '243', '93']:
        return [{'quality': '360p', 'url': url}]
    elif quality in ['5', '6', '36', '83', '133', '242', '92', '132']:
        return [{'quality': '240p', 'url': url}]
    else:
        return []



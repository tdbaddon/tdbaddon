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


import re,urllib,urlparse,base64
from resources.lib.libraries import client
from resources.lib.libraries import jsunpack


def resolve(url):
    try:
        page = re.compile('//(.+?)/(?:embed|v)/([0-9a-zA-Z-_]+)').findall(url)[0]
        page = 'http://%s/embed/%s' % (page[0], page[1])

        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = page

        result = client.request(page, referer=referer)


        unpacked = ''
        packed = result.split('\n')
        for i in packed: 
            try: unpacked += jsunpack.unpack(i)
            except: pass
        result += unpacked
        result = urllib.unquote_plus(result)
        result = re.sub('\s\s+', ' ', result)


        url = client.parseDOM(result, 'iframe', ret='src')[-1]
        url = url.replace(' ', '')

        var = re.compile('var\s(.+?)\s*=\s*\'(.+?)\'').findall(result)
        for i in range(100):
            for v in var: url = url.replace("'%s'" % v[0], v[1])
            for v in var: url = url.replace("(%s)" % v[0], "(%s)" % v[1])

        url = re.sub(r"'.+?\((.+?)\)'", r'\1', url)
        url = re.sub(r"'(.+?)'", r'\1', url)


        result = client.request(url, referer=referer)

        file = re.compile("'file'.+?'(.+?)'").findall(result)[0]

        try:
            if not file.startswith('http'): raise Exception()
            url = client.request(file, output='geturl')
            if not '.m3u8' in url: raise Exception()
            url += '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': file})
            return url
        except:
            pass

        strm = re.compile("'streamer'.+?'(.+?)'").findall(result)[0]
        swf = re.compile("SWFObject\('(.+?)'").findall(result)[0]

        url = '%s playpath=%s swfUrl=%s pageUrl=%s live=1 timeout=30' % (strm, file, swf, url)
        return url
    except:
        return



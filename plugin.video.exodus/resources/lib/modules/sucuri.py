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


import re,urlparse,base64

from resources.lib.modules import cache
from resources.lib.modules import client


def headers(url, timeout='30'):
    try:
        u = '%s://%s' % (urlparse.urlparse(url).scheme, urlparse.urlparse(url).netloc)

        h = cache.get(sucuri, 168, u, timeout)
        if h == None:
            h = cache.get(sucuri, 0, u, timeout)
        if h == None:
            h = {}

        return h
    except:
        return

def sucuri(url, timeout):
    try:
        h = client.randomagent()

        r = client.request(url, headers={'User-Agent': h}, timeout=timeout, error=True)

        s = re.compile("S\s*=\s*'([^']+)").findall(r)[0]
        s = base64.b64decode(s)
        s = s.replace(' ', '')
        s = re.sub('String\.fromCharCode\(([^)]+)\)', r'chr(\1)', s)
        s = re.sub('\.slice\((\d+),(\d+)\)', r'[\1:\2]', s)
        s = re.sub('\.charAt\(([^)]+)\)', r'[\1]', s)
        s = re.sub('\.substr\((\d+),(\d+)\)', r'[\1:\1+\2]', s)
        s = re.sub(';location.reload\(\);', '', s)
        s = re.sub(r'\n', '', s)
        s = re.sub(r'document\.cookie', 'cookie', s)

        cookie = '' ; exec(s)
        c = re.compile('([^=]+)=(.*)').findall(cookie)[0]
        c = '%s=%s' % (c[0], c[1])

        return {'User-Agent': h, 'Cookie': c}
    except:
        pass



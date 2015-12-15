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


import re
import urlparse
import base64
import cache
import client


def request(url, timeout='30'):
    try:
        u = '%s://%s' % (urlparse.urlparse(url).scheme, urlparse.urlparse(url).netloc)

        cookie = cache.get(sucuri, 168, u, timeout)
        if cookie == None:
            cookie = cache.get(sucuri, 0, u, timeout)

        result = client.request(url, cookie=cookie, timeout=timeout)
        return result
    except:
        return


def source(url, timeout='5'):
    return request(url, timeout)


def sucuri(url, timeout):
    try:
        result = client.request(url, timeout=timeout, error=True)

        s = re.compile("S\s*=\s*'([^']+)").findall(result)[0]
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

        cookie = re.compile('([^=]+)=(.*)').findall(cookie)[0]
        cookie = '%s=%s' % (cookie[0], cookie[1])

        return cookie
    except:
        pass


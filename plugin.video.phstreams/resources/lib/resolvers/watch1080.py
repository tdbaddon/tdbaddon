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


import re,urlparse,base64
from resources.lib.libraries import client
from resources.lib.resolvers import openload


def resolve(url):
    try:
        try: quality = urlparse.parse_qs(urlparse.urlparse(url).query)['quality'][0]
        except: quality = '1080P'

        url = url.rsplit('?', 1)[0]

        result = client.request(url, close=False)

        url = client.parseDOM(result, 'div', attrs = {'class': 'player'})[0]
        url = client.parseDOM(url, 'iframe', ret='src')[0]

        result = client.request(url)

        url = client.parseDOM(result, 'iframe', ret='src')
        if len(url) > 0: return openload.resolve(url[0])

        result = re.compile("\('(.+?)'\)").findall(result)[0]
        result = base64.b64decode(result)

        url = client.parseDOM(result, 'source', ret='src', attrs = {'data-res': quality})
        url += client.parseDOM(result, 'source', ret='src', attrs = {'data-res': '.+?'})
        url = url[0]

        url = client.request(url, output='geturl')
        if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
        else: url = url.replace('https://', 'http://')

        return url
    except:
        return



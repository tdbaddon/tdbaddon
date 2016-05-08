# -*- coding: utf-8 -*-

'''
    Specto Add-on
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


import re,json,urllib
from resources.lib.libraries import client


def resolve(url):
    try:
        cookie = client.source(url, output='cookie')
        result = client.source(url, cookie=cookie)
        sk = re.compile('"sk":"([^"]+)",').findall(result)[0]
        id = re.compile('"id":"([^"]+)",').findall(result)[0]
        if len(id) > 0 and len(sk) > 0:
            post = {'idClient': '241b0f80730b748e6c0918c0f447d51b', 'version': '3.9.2', 'sk': sk, '_model.0': 'do-get-resource-url', 'id.0': id }
            result = client.source('https://yadi.sk/models/?_m=do-get-resource-url',post=post,cookie=cookie)
            result = json.loads(result)
            print('res', result)
            url = result['models'][0]['data']['file']
            return url
        return
    except:
        return


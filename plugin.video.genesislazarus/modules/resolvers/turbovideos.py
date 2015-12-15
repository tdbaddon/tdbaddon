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
from modules.libraries import client
from modules.libraries import jsunpack


def resolve(url):
    try:
        url = url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://turbovideos.net/embed-%s.html' % url

        result = client.request(url)

        url = re.compile('file *: *"(.+?)"').findall(result)
        if len(url) > 0: return url[0]

        result = re.compile('(eval.*?\)\)\))').findall(result)[-1]
        result = re.sub(r'(\',\d*,\d*,)', r';\1', result)
        url = jsunpack.unpack(result)
        return url
    except:
        return


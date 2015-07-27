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
import urllib
from modules.libraries import client
from modules.libraries import jsunpack


def resolve(url):
    try:
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://180upload.com/embed-%s.html' % url

        result = client.request(url)

        post = {}
        f = client.parseDOM(result, "form", attrs = { "id": "captchaForm" })[0]
        k = client.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: client.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post = urllib.urlencode(post)

        result = client.request(url, post=post)

        result = re.compile('(eval.*?\)\)\))').findall(result)[-1]

        url = jsunpack.unpack(result)
        return url
    except:
        return


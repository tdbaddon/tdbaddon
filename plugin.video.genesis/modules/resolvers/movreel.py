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
import time
import urllib
import urllib2
from modules.libraries import control
from modules.libraries import client


def resolve(url):
    try:
        user = control.setting('movreel_user')
        password = control.setting('movreel_password')

        login = 'http://movreel.com/login.html'
        post = {'op': 'login', 'login': user, 'password': password, 'redirect': url}
        post = urllib.urlencode(post)
        result = client.request(url, close=False)
        result += client.request(login, post=post, close=False)

        post = {}
        f = client.parseDOM(result, "Form", attrs = { "name": "F1" })[-1]
        k = client.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: client.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': '', 'method_premium': ''})
        post = urllib.urlencode(post)

        request = urllib2.Request(url, post)

        for i in range(0, 3):
            try:
                response = urllib2.urlopen(request, timeout=10)
                result = response.read()
                response.close()
                url = re.compile('(<a .+?</a>)').findall(result)
                url = [i for i in url if 'Download Link' in i][-1]
                url = client.parseDOM(url, "a", ret="href")[0]
                return url
            except:
                time.sleep(1)
    except:
        return


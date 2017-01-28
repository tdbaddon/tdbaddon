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


import urllib,random
from resources.lib.modules import client


def request(url, check):
    try:
        result = client.request(url)
        if check in str(result): return result.decode('iso-8859-1').encode('utf-8')

        result = client.request(get() + urllib.quote_plus(url))
        if check in str(result): return result.decode('iso-8859-1').encode('utf-8')

        result = client.request(get() + urllib.quote_plus(url))
        if check in str(result): return result.decode('iso-8859-1').encode('utf-8')
    except:
        pass


def get():
    return random.choice([
    'http://4freeproxy.com/browse.php?b=20&u=',
    'https://www.3proxy.us/index.php?hl=2e5&q=',
    'https://www.4proxy.us/index.php?hl=2e5&q=',
    'http://www.accessmeproxy.net/browse.php?b=20&u=',
    'http://buka.link/browse.php?b=20&u=',
    'http://fastrow.win/browse.php?b=20&u=',
    'http://free-proxyserver.com/browse.php?b=20&u=',
    'http://www.ipunblocker.com/browse.php?b=20&u=',
    'http://www.mybriefonline.xyz/browse.php?b=20&u=',
    'http://www.navigate-online.xyz/browse.php?b=20&u=',
    'http://protectproxy.com/browse.php?b=20&u=',
    'http://proxite.net/browse.php?b=20&u=',
    'http://proxydash.com/browse.php?b=20&u=',
    'http://www.proxywebsite.us/browse.php?b=20&u=',
    'http://proxy-server.co/browse.php?b=20&u=',
    'http://www.ruby-group.xyz/browse.php?b=20&u=',
    'http://securefor.com/browse.php?b=20&u=',
    'http://www.singleclick.info/browse.php?b=20&u=',
    'http://www.socialcommunication.xyz/browse.php?b=20&u=',
    'http://tbjr6.net/browse.php?b=20&u=',
    'http://un404.com/browse.php?b=20&u=',
    'http://www.unblockmyweb.com/browse.php?b=20&u=',
    'http://unblockthatsite.net/ahora.php?b=20&u=',
    'http://unblock-youtube.org/browse.php?b=20&u=',
    'http://webproxy.stealthy.co/browse.php?b=20&u=',
    'http://www.whyproxy.com/browse.php?b=20&u=',
    'http://www.xxlproxy.com/index.php?hl=3e4&q=',
    'http://zend2.com//open12.php?b=20&u=',
    'https://zendproxy.com/bb.php?b=20&u=',
    'https://zproxy.de/anon.php?b=20&u='
    ])



# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2017 Aftershockpy

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

import client
import random
import urllib, urlparse


def request(url, check):
    try:
        result = client.request(url)
        if check in str(result): return result.decode('iso-8859-1').encode('utf-8')

        result = client.request(get() + urllib.quote_plus(url))
        if check in str(result): return result.decode('iso-8859-1').encode('utf-8')

        result = client.request(get() + urllib.quote_plus(url))
        if check in str(result): return result.decode('iso-8859-1').encode('utf-8')
    except:
        return

def parse(url):
    try: url = client.replaceHTMLCodes(url)
    except: pass
    try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
    except: pass
    try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['q'][0]
    except: pass
    return url

def get():
    return random.choice([
    'https://www.3proxy.us/index.php?hl=2e5&q=',
    'https://www.4proxy.us/index.php?hl=2e5&q=',
    'http://dontfilter.us/browse.php?b=20&u=',
    'http://www.fakeip.org/index.php?hl=3c0&q=',
    'http://filesdownloader.com/o.php?b=20&u=',
    'http://free-proxyserver.com/browse.php?b=20&u=',
    'http://freeanimesonline.com/o.php?b=20&u=',
    'http://www.freeopenproxy.com/browse.php?b=20&u=',
    'http://freeproxy.io/o.php?b=20&u=',
    'http://www.greatestfreeproxy.com/browse.php?b=20&u=',
    'http://www.gumm.org/index.php?hl=2e5&q=',
    'http://www.justproxy.co.uk/index.php?hl=2e5&q=',
    'http://quickprox.com/browse.php?b=20&u=',
    'http://siteget.net/o.php?b=20&u=',
    'http://sitenable.info/o.php?b=20&u=',
    'http://unblock-proxy.com/browse.php?b=20&u=',
    'http://www.unblockmyweb.com/browse.php?b=20&u=',
    'http://www.unblockyoutubefree.net/browse.php?b=20&u=',
    'http://www.webproxyfree.net/browse.php?b=20&u=',
    'http://www.youtubeunblockproxy.com/browse.php?b=20&u=',
    'https://zendproxy.com/bb.php?b=20&u='
    ])



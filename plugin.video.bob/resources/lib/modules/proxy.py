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

import random
import urllib

import urllib2
import urlparse

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
        return


def get():
    return random.choice([
        'http://2anonymousproxy.com//browse.php?b=20&u=',
        'https://www.3proxy.us/index.php?hl=2e5&q=',
        'https://www.4proxy.us/index.php?hl=2e5&q=',
        'http://alter-ip.com/index.php?hl=3c0&q=',
        'http://buka.link/browse.php?b=20&u=',
        'http://www.bypassrestrictions.com/browse.php?b=20&u=',
        'http://dontfilter.us/browse.php?b=20&u=',
        'http://free-proxyserver.com/browse.php?b=20&u=',
        'http://www.freeopenproxy.com/browse.php?b=20&u=',
        'http://www.gumm.org/browse.php?b=20&u=',
        'http://www.justproxy.co.uk/index.php?hl=2e5&q=',
        'http://myroxy.info/browse.php?b=20&u=',
        'http://www.nologproxy.com/browse.php?b=20&u=',
        'http://protectproxy.com/browse.php?b=20&u=',
        'http://proxite.net/browse.php?b=20&u=',
        'http://www.proxythis.info/index.php?hl=2e5&q=',
        'http://quickprox.com/browse.php?b=20&u=',
        'http://unblock-proxy.com/browse.php?b=20&u=',
        'http://www.unblockmyweb.com/browse.php?b=20&u=',
        'http://unblocksite.org/view.php?b=20&u=',
        'http://unblockthatsite.net/ahora.php?b=20&u=',
        'http://www.web-proxy.org.uk/index.php?hl=2e5&q=',
        'http://www.webproxy.online/index.php?hl=2e5&q=',
        'http://www.youtubeunblockproxy.com/browse.php?b=20&u=',
        'https://zendproxy.com/bb.php?b=20&u='
    ])


def get2(url, check, headers=None, data=None):
    if headers is None:
        headers = {
            'User-Agent': client.randomagent(),
        }
        try:
            request = urllib2.Request(url, headers=headers, data=data)
            html = urllib2.urlopen(request, timeout=10).read()
            if check in str(html): return html
        except:
            pass

    try:
        new_url = get_proxy_url() % urllib.quote_plus(url)
        headers['Referer'] = 'http://%s/' % urlparse.urlparse(new_url).netloc
        request = urllib2.Request(new_url, headers=headers)
        response = urllib2.urlopen(request, timeout=10)
        html = response.read()
        response.close()
        if check in html: return html
    except:
        pass

    try:
        new_url = get_proxy_url() % urllib.quote_plus(url)
        headers['Referer'] = 'http://%s/' % urlparse.urlparse(new_url).netloc
        request = urllib2.Request(new_url, headers=headers)
        html = urllib2.urlopen(request, timeout=10).read()
        if check in html: return html
    except:
        pass

    return


def get_raw(url, headers=None, data=None):
    if headers is None:
        headers = {
            'User-Agent': client.randomagent(),
        }

    try:
        new_url = get_proxy_url() % urllib.quote_plus(url)
        headers['Referer'] = 'http://%s/' % urlparse.urlparse(new_url).netloc
        request = urllib2.Request(new_url, headers=headers)
        response = urllib2.urlopen(request, timeout=10)
        return response
    except:
        pass


def get_proxy_url():
    return random.choice([
        'http://alter-ip.com/index.php?hl=3c0&q=%s',
        'http://buka.link/browse.php?b=20&u=%s&b=0&f=norefer',
        'http://dontfilter.us/browse.php?b=20&u=%s',
        'http://free-proxyserver.com/browse.php?b=20&u=%s',
        'http://www.freeopenproxy.com/browse.php?b=20&u=%s',
        'http://www.justproxy.co.uk/index.php?hl=2e5&q=%s',
        'http://protectproxy.com/browse.php?b=20&u=%s',
        'http://proxite.net/browse.php?b=20&u=%s',
        'http://www.proxythis.info/index.php?hl=2e5&q=%s',
        'http://quickprox.com/browse.php?b=20&u=%s',
        'http://unblock-proxy.com/browse.php?b=20&u=%s&b=0&f=norefer',
        'http://www.unblockmyweb.com/browse.php?b=20&u=%s',
        'http://unblocksite.org/view.php?b=20&u=%s',
        'http://unblockthatsite.net/ahora.php?b=20&u=',
    ])

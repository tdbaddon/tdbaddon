# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2015 IDev

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

import urlparse, urllib
from resources.lib.libraries import client
from resources.lib.libraries import logger

try :import urlresolver
except:pass

def request(url, resolverList=None):

    # Custom Resolvers
    try:
        u = client.host(url)

        r = [i['class'] for i in info() if u in i['host']][0]
        r = __import__(r, globals(), locals(), [], -1)
        r = r.resolve(url)
        if not r:
            raise Exception()
        h = dict('')
        h['User-Agent'] = client.agent()
        h['Referer'] = url
        r = '%s|%s' % (r.split('|')[0], urllib.urlencode(h))

        return r
    except:
        pass

    # URLResolvers 3.0.0
    u = url
    try:
        url = None

        hmf = urlresolver.HostedMediaFile(url=u, include_disabled=True, include_universal=False)
        if hmf.valid_url() == True: url = hmf.resolve()
        else: url = False
    except:
        pass

    try:
        if not url == None: raise Exception()

        hmf = urlresolver.HostedMediaFile(url=u, include_disabled=True)
        hmf = hmf.get_resolvers(validated=True)
        hmf = [i for i in hmf if not i.isUniversal()][0]
        host, media_id = hmf.get_host_and_id(u)
        url = hmf.get_media_url(host, media_id)
    except:
        pass

    # URL Resolver 2.10.12
    try:
        if not url == None: raise Exception()

        hmf = urlresolver.plugnplay.man.implementors(urlresolver.UrlResolver)
        hmf = [i for i in hmf if not '*' in i.domains]
        hmf = [(i, i.get_host_and_id(u)) for i in hmf]
        hmf = [i for i in hmf if not i[1] == False]
        hmf = [(i[0], i[0].valid_url(u, i[1][0]), i[1][0], i[1][1]) for i in hmf]
        hmf = [i for i in hmf if not i[1] == False][0]
        url = hmf[0].get_media_url(hmf[2], hmf[3])
    except:
        pass

    try: headers = dict(urlparse.parse_qsl(url.rsplit('|', 1)[1]))
    except: headers = dict('')

    if url.startswith('http') and '.m3u8' in url:
        result = client.request(url.split('|')[0], headers=headers, output='geturl', timeout='20')
        if result == None: raise Exception()

    elif url.startswith('http'):
        result = client.request(url.split('|')[0], headers=headers, output='chunk', timeout='20')
        if result == None: raise Exception()

    return url

def info():
    return [
        {'class': 'desiflicks', 'host': ['desiflicks.com']}
        , {'class': 'playwire', 'host': ['playwire.com']}
        , {'class': 'vidshare', 'host': ['vidshare.us', 'idowatch.us', 'watchvideo4.us','watchvideo2.us','watchvideo.us', 'tvlogy.to',  'speedplay.pw']}
        , {'class': 'xpressvids', 'host': ['xpressvids']}
        , {'class': 'playu', 'host': ['playu.net']}
        , {'class': 'apnasave', 'host': ['apnasave.in']}
        , {'class': 'filmywap', 'host': ['storeinusa.com']}
        , {'class': 'ditto', 'host': ['dittotv.com']}
        , {'class': 'dynns', 'host': ['dynns.com']}
    ]
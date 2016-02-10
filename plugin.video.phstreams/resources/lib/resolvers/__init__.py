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


import re,urllib,urlparse,json,time

from resources.lib.libraries import cache
from resources.lib.libraries import control
from resources.lib.libraries import client


def request(url, debrid=''):
    try:
        u = url

        if '</regex>' in url:
            import regex ; url = regex.resolve(url)
            if not url == None: u = url

        if url.startswith('rtmp'):
            if len(re.compile('\s*timeout=(\d*)').findall(url)) == 0: url += ' timeout=10'
            return url

        if url.startswith('$base64'):
            import base64 ; url = base64.b64decode(re.compile('\$base64\[(.+?)\]$').findall(url)[0])
            if not url == None: u = url

        n = (urlparse.urlparse(url).netloc).lower() ; n = re.sub('www\d+\.|www\.|embed\.', '', n)

        try: url = re.compile('://(http.+)').findall(url)[0]
        except: pass

        import urlresolver
        r = urlresolver.HostedMediaFile(url=url).resolve()
        if not r == False: return r

        r = [i['class'] for i in info() if n in i['netloc']][0]
        r = __import__(r, globals(), locals(), [], -1)
        r = r.resolve(url)

        return r
    except:
        return u


def info():
    return [{
        'class': 'castalba',
        'netloc': ['castalba.tv']
    }, {
        'class': 'filmon',
        'netloc': ['filmon.com']
    }, {
        'class': 'finecast',
        'netloc': ['finecast.tv']
    }, {   
        'class': 'google',
        'netloc': ['docs.google.com', 'drive.google.com', 'photos.google.com', 'picasaweb.google.com', 'plus.google.com']
    }, {
        'class': 'hdcast',
        'netloc': ['hdcast.me']
    }, {
        'class': 'hdcastorg',
        'netloc': ['hdcast.org']
    }, {
        'class': 'miplayer',
        'netloc': ['miplayer.net'],
        'quality': 'High'
    }, {    
        'class': 'mybeststream',
        'netloc': ['mybeststream.xyz']
    }, {
        'class': 'p2pcast',
        'netloc': ['p2pcast.tv']
    }, {
        'class': 'sawlive',
        'netloc': ['sawlive.tv']
    }, {
        'class': 'shadownet',
        'netloc': ['sdw-net.co']
    }, {        
        'class': 'stream4free',
        'netloc': ['stream4free.pro', 'stream4free.eu']
    }, {    
        'class': 'streamlive',
        'netloc': ['streamlive.to'],
        'quality': 'Medium'
    }, {
        'class': 'streamup',
        'netloc': ['streamup.com']
    }, {
        'class': 'vaughnlive',
        'netloc': ['vaughnlive.tv', 'breakers.tv', 'instagib.tv', 'vapers.tv']
    }, {
        'class': 'veehd',
        'netloc': ['veehd.com']
    }, {
        'class': 'veetle',
        'netloc': ['veetle.com']
    }, {
        'class': 'videopremium',
        'netloc': ['videopremium.tv', 'videopremium.me']
    }, {
        'class': 'watch1080',
        'netloc': ['watch1080p.com', 'sefilmdk.com']
    }, {
        'class': 'yocast',
        'netloc': ['yocast.tv']
    }, {
        'class': 'zerocast',
        'netloc': ['zerocast.tv']
    }, {
        'class': 'zoptv',
        'netloc': ['zoptv.com', 'iptvlinks.tk'],
        'quality': 'High'
    }]



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


import re,urlparse
from resources.lib.libraries import client


def resolve(url):
    try:
        page = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
        page = 'http://www.finecast.tv/embed4.php?u=%s&vw=640&vh=450' % page

        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = page

        result = client.request(page, referer=referer)

        t = re.compile("var t\s*=\s*'(.+?)';").findall(result)[0]
        m = re.compile("var m\s*=\s*'(.+?)';").findall(result)[0]

        streamer = re.compile('file\s*:\s*\'(.+?)\'').findall(result)[0]

        url = streamer + "%s playpath=%s swfUrl=http://www.finecast.tv/player6/jwplayer.flash.swf flashver=WIN\\2019,0,0,185 live=1 timeout=15 swfVfy=1 pageUrl=http://www.finecast.tv/" % (t,m)
        return url
    except:
       return



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

import re

from resources.lib.libraries import client, EnkDekoder
from resources.lib.libraries import logger

def resolve(url):
    try:
        result = client.source(url)
        dek = EnkDekoder.dekode(result)

        if not dek == None:
            url = client.parseDOM(dek, "param", attrs={ "name":"flashvars"}, ret = "value")[0]
        else:
            dek = result
            url = re.compile('file*:*"(http.+?)"').findall(dek)[0]


        if re.search(';video_url',url):
            url = re.findall(';video_url=(.+?)&amp',url)[0]
        elif re.search('iframe src=', url):
            url = re.findall('<iframe src="(.+?)"',url)[0]

        url = url.replace('_ipod.mp4', '.flv')
        url = url.replace('preview','edit')
        logger.debug('URL [%s]' % url, __name__)
        return url
    except:
        return False
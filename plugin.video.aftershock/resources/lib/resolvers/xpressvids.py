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

from resources.lib.libraries import client
from resources.lib.libraries import logger

def resolve(url):
    try:
        url = 'http://playu.net/embed-%s.html' % str(getVideoID(url))
        result = client.source(url)
        url = re.findall('file: "(.+?)"',result)[0]
        logger.debug('%s URL [%s]' % (__name__, url))
        return url
    except:
        return

def getVideoID(url):
    try :
        return re.compile('(id|url|v|si|sim|data-config)=(.+?)/').findall(url + '/')[0][1]
    except:
        return
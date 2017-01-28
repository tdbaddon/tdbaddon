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
        url = url + '#'
        url = re.compile('http://www.mediaplaybox.com/video/(.+?)#').findall(url)[0]
        url = 'http://www.mediaplaybox.com/mobile?vinf=%s' % url

        result = client.request(url, debug=True)

        try :
            url = client.parseDOM(result, "div", attrs = {"class":"divider"})[0]
            url = client.parseDOM(url, "a", ret = "href")
            url = url[0]
            url = url.replace('_ipod.mp4', '.flv')
            return url
        except:
            pass

        try :url = client.parseDOM(result, "meta", attrs={"itemprop":"contentURL"}, ret="content")[0]
        except:
            pass
        logger.debug('URL [%s]' % url, __name__)
        return url
    except:
        return False
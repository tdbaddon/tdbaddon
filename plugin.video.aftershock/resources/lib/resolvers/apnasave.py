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
        rUrl = None
        hdUrl = None
        try :
            result = client.request(url)
            rUrl = client.parseDOM(result, name="source", ret="src")[0]
            videoId = getVideoID(rUrl)
            rUrl = 'http://www.apnasave.in/media/player/config_embed.php?vkey=%s' % videoId
            result = client.request(rUrl)

            try :
                hdUrl = client.parseDOM(result, name="hd")[0]
                url = hdUrl
            except:
                pass
            if hdUrl == None:
                url = client.parseDOM(result, name="src")[0]
        except:
            pass
        logger.debug('URL [%s]' % url, __name__)
        return url
    except:
        return False

def getVideoID(url):
    try :
        return re.compile('(id|url|v|si|sim|data-config)=(.+?)/').findall(url + '/')[0][1]
    except:
        return
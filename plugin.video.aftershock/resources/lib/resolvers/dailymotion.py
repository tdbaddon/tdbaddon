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

import re
import urllib

from resources.lib.modules import client
from resources.lib.modules import logger


def resolve(url):
    try:
        disableAge = 'http://www.dailymotion.com/family_filter?enable=false&urlback=%s' % url
        cookie = client.request(disableAge, output='cookie')
        html = client.request(url, cookie=cookie)

        matchHDLink = ''
        matchHQLink = ''
        matchSDLink = ''
        matchLDLink = ''

        matchHD = re.compile('720\"\:\[\{\"type\"\:\"application\\\/x\-mpegURL\"\,\"url\"\:\"(.+?)\"\}\,\{\"type\"\:\"video\\\/mp4\"\,\"url\"\:\"(.+?)\"', re.DOTALL).findall(html)
        matchHQ = re.compile('480\"\:\[\{\"type\"\:\"application\\\/x\-mpegURL\"\,\"url\"\:\"(.+?)\"\}\,\{\"type\"\:\"video\\\/mp4\"\,\"url\"\:\"(.+?)\"', re.DOTALL).findall(html)
        matchSD = re.compile('380\"\:\[\{\"type\"\:\"application\\\/x\-mpegURL\"\,\"url\"\:\"(.+?)\"\}\,\{\"type\"\:\"video\\\/mp4\"\,\"url\"\:\"(.+?)\"', re.DOTALL).findall(html)
        matchLD = re.compile('240\"\:\[\{\"type\"\:\"application\\\/x\-mpegURL\"\,\"url\"\:\"(.+?)\"\}\,\{\"type\"\:\"video\\\/mp4\"\,\"url\"\:\"(.+?)\"', re.DOTALL).findall(html)

        try:
            if matchHD[0][1]:
                matchHDLink = matchHD[0][1]
        except:
            pass

        try:
            if matchHQ[0][1]:
                matchHQLink = matchHQ[0][1]
        except:
            pass

        try:
            if matchSD[0][1]:
                matchSDLink = matchSD[0][1]
        except:
            pass

        try:
            if matchLD[0][1]:
                matchLDLink = matchLD[0][1]
        except:
            pass

        matchHDLink = matchHDLink.replace('\/', '/')
        matchHQLink = matchHQLink.replace('\/', '/')
        matchSDLink = matchSDLink.replace('\/', '/')
        matchLDLink = matchLDLink.replace('\/', '/')

        dm_LD = None
        dm_SD = None
        dm_HQ = None
        dm_720 = None
        final_url = None

        if matchHDLink:
            dm_720 = urllib.unquote_plus(matchHDLink).replace("\\", "")
        if dm_720 is None and matchHQ:
            dm_720 = urllib.unquote_plus(matchHQLink).replace("\\", "")
        if matchSD:
            dm_SD = urllib.unquote_plus(matchSDLink).replace("\\", "")
        if matchLD:
            dm_LD = urllib.unquote_plus(matchLDLink).replace("\\", "")

        if final_url is None and dm_720 is not None:
            final_url = dm_720
        if final_url is None and dm_HQ is not None:
            final_url = dm_HQ
        if final_url is None and dm_SD is not None:
            final_url = dm_SD
        if final_url is None and dm_LD is not None:
            final_url = dm_LD

        if final_url == None:
            raise Exception()
        return "%s|Cookie=%s" % (final_url, cookie)
    except Exception as e:
        logger.error(e.message)
        return False
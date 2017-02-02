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

import json
import re

from resources.lib.modules import client
from resources.lib.modules import logger


def resolve(url):
    try:
        result = client.request(url)
        data = json.loads(result)
        try :
            publisherId = data['publisherId']
            hostingId = data['hostingId']
            videoId = data['content']['videoId']
        except:
            publisherId = data['settings']['publisherId']
            hostingId = data['settings']['hostingId']
            videoId = data['settings']['videoId']

        url ='https://config.playwire.com/videos/v2/%s/player.json' % str(videoId)
        result = client.request(url)
        data = json.loads(result)

        src = data['src']
        video_info = re.compile('config.playwire.com/(.+?)/videos/v2/(.+?)/manifest.f4m').findall(src)[0]
        # try best url
        #url = 'https://config.playwire.com/' + video_info[0] + '/videos/v2/' + video_info[1] + '/abr-non-hd.m3u8'
        #logger.debug('PLAYWIRE HD URL : %s ' % url)
        #try :
        #    result = client.request(url, output='geturl', timeout=10)
        #    if result == None:
        #        raise Exception()
        #except:
        #    pass
        # try sd url

        result = None
        if result == None:
            url = 'http://cdn.phoenix.intergi.com/' + video_info[0] + '/videos/' + video_info[1] + '/video-sd.mp4?hosting_id=' + video_info[0]
            try :
                result = client.request(url, output='chunk', timeout=10)
                if result == None:
                    raise Exception()
            except:
                pass

        if result == None:
            # try mobile url
            url = 'http://cdn.phoenix.intergi.com/' + video_info[0] + '/videos/' + video_info[1] + '/video-mobile.mp4?hosting_id=' + video_info[0]
            try :
                result = client.request(url, output='chunk', timeout=10)
                if result == None:
                    raise Exception()
            except:
                pass
        '''
        try :
            publisherId = data['publisherId']
            hostingId = data['hostingId']
            videoId = data['content']['videoId']
        except:
            publisherId = data['settings']['publisherId']
            hostingId = data['settings']['hostingId']
            videoId = data['settings']['videoId']

        url = 'https://cdn.video.playwire.com/%s/videos/%s/video-sd.mp4?hosting_id=%s' % (publisherId, videoId, hostingId)
        '''
        logger.debug('URL [%s]' % url, __name__)
        return url
    except:
        return False
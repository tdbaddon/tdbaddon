# -*- coding: utf-8 -*-
#
# This Program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
import os, base64
import control, json, cleantitle, logger

from resources.lib.libraries import cleantitle


class LiveParser(object):
    filePath = ''
    basePath = control.dataPath

    def __init__(self, fileName, addon):
        self.filePath = os.path.join(self.basePath, fileName)
        return

    def parseFile(self, decode=True):
        try :
            logger.debug(self.filePath, __name__)
            filename = open(self.filePath)
            result = filename.read()
            filename.close()
            if decode:
                try : result = base64.urlsafe_b64decode(result)
                except : pass

            channels = json.loads(result)

            channelNames = channels.keys()
            channelNames.sort()

            liveList = []
            for channel in channelNames:
                channelObj = channels[channel]
                if '||' in channel:
                    channel = channel.split('||')[0]

                cleanChannelName = cleantitle.live(channel)
                if cleanChannelName == 'SKIP':
                    continue

                try : enabled = channelObj['enabled']
                except : enabled = 'true'
                try : quality = channelObj['quality']
                except : quality = 'HD'
                if not enabled == 'false':
                    channelName = channel.upper()
                    try :
                        if channelObj['direct'] == 'true': channelObj['direct'] = True
                        else : channelObj['direct'] = False
                    except:
                        channelObj['direct'] = True

                    try : source = channelObj['source']
                    except: source = channelObj['provider']

                    liveList.append({'name':cleanChannelName, 'originalName': channelName, 'poster':channelObj['icon'],'url':channelObj['url'],'provider':channelObj['provider'],'source':source,'direct':channelObj['direct'], 'quality':quality})
            return liveList
        except :
            pass
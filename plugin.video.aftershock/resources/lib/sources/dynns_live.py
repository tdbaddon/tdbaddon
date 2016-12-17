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


import urlparse, re, os, binascii, base64, time
from resources.lib.libraries import client
from resources.lib.libraries import logger
from resources.lib.libraries import cleantitle
from resources.lib.libraries import cache
from resources.lib.libraries import control
from resources.lib.libraries.fileFetcher import *
from resources.lib.libraries.liveParser import *

class source:
    def __init__(self):
        self.base_link = 'https://app.dyndns.tv'
        self.ip_check = '/keys/ip_check.php'
        self.live_link = '/livetv'
        self.channel_link = 'http://origin.dittotv.com/livetv/%s'
        self.poster_link = 'http://dittotv2.streamark.netdna-cdn.com/vod_images/optimized/livetv/%s.jpg'
        self.headers = {'User-Agent':base64.b64decode('dW1hci8xLjEgQ0ZOZXR3b3JrLzc1OC4wLjIgRGFyd2luLzE1LjAuMA==')}
        self.list = []
        self.deviceId = None
        self.ipAddress = None
        self.fileName = 'dynns.json'
        self.filePath = os.path.join(control.dataPath, self.fileName)

    def removeJSON(self, name):
        control.delete(self.fileName)
        return 0

    def getLiveSource(self):
        try :
            generateJSON = cache.get(self.removeJSON, 168, __name__, table='live_cache')
            if not os.path.exists(self.filePath):
                generateJSON = 1

            if generateJSON:
                logger.debug('Generating %s JSON' % __name__, __name__)

                userAgent = self.getUserAgent()
                deviceid = userAgent.split('.')[-1]

                url = urlparse.urljoin(self.base_link,self.ip_check)

                result = client.request(url, headers=self.headers)
                self.ipAddress = re.findall('Address: (.*)',result)[0]

                TIME = time.time()
                second= str(TIME).split('.')[0]
                first =int(second)+int(base64.b64decode('NjkyOTY5Mjk='))
                token=base64.b64encode(base64.b64decode('JXNAMm5kMkAlcw==') % (str(first),second))

                headers = {'Authorization': base64.b64decode('QmFzaWMgWVdSdGFXNUFZWE5rWmpwaGMyUm1jWGRsY25SNQ=='),
                           base64.b64decode("VXNlci1BZ2VudA=="):cache.get(self.getDeviceID, 600000, table='live_cache')}

                url = base64.b64decode('aHR0cHM6Ly9hcHAuZHluZG5zLnR2L2FwcHMvb3V0cHV0LnBocC9wbGF5bGlzdD90eXBlPXhtbCZkZXZpY2VTbj0lcw==') % deviceid

                result = client.request(url, headers=headers)

                result = client.parseDOM(result, "items")

                channelList = {}
                for channel in result:

                    category = client.parseDOM(channel, "programCategory")[0]
                    if category == 'Indian':
                        title = client.parseDOM(channel,"programTitle")[0]
                        title = cleantitle.live(title)
                        if title == 'SKIP':
                            continue
                        poster = client.parseDOM(channel, "programImage")[0]
                        url = client.parseDOM(channel, "programURL")[0]
                        channelList[title] ={'icon':poster,'url':url,'provider':'dynns','source':'dynns','direct':False, 'quality':'HD'}

                filePath = os.path.join(control.dataPath, self.fileName)
                with open(filePath, 'w') as outfile:
                    json.dump(channelList, outfile, sort_keys=True, indent=2)

                liveParser = LiveParser(self.fileName, control.addon)
                self.list = liveParser.parseFile(decode=False)

            return (generateJSON, self.list)
        except:

            pass

    def resolve(self, url, resolverList):
        try :
            logger.debug('ORIGINAL URL [%s]' % url, __name__)
            authToken = self.getAuthToken()
            logger.debug('AuthToken %s' % authToken, __name__)
            url += authToken
            if '|' not in url:
                url += '|'

            import random
            useragent='User-Agent=AppleCoreMedia/1.0.0.%s (%s; U; CPU OS %s like Mac OS X; en_gb)'%(random.choice(['13G35','13G36','14A403','14A456','14B72','14B150']),random.choice(['iPhone','iPad','iPod']),random.choice(['9.3.4','9.3.5','10.0.2','10.1','10.1.1']))
            url+=useragent
            logger.debug('RESOLVED URL [%s]' % url, __name__)
            return url
        except Exception as e:
            logger.error(e)
            return False

    def getDeviceID(self):
        deviceId = binascii.b2a_hex(os.urandom(16)).upper()
        logger.debug('DeviceID : %s' % deviceId, __name__)
        return deviceId

    def getUserAgent(self):

        headers = {'User-Agent':base64.b64decode('cDl4VE1nV2hFclpxZGlFWU1iV045bFVvd0xGMFdWM3I='),
                   'Authorization':base64.b64decode('QmFzaWMgWVcxMVpHbHNZbUZ5T21waGJuVm5aWEp0WVc0PQ==')}

        useragent = client.request(base64.b64decode('aHR0cHM6Ly93d3cuYm94dHZoZC5jb20vdG9wL3Bha2luZGlhdjJwLnBocA=='), headers=headers)

        logger.debug('UserAgent : %s' % useragent, __name__)
        return useragent

    def getAuthToken(self):
        url=base64.b64decode('aHR0cHM6Ly9hcHAuZHluZG5zLnR2L3RvcC8lcy5waHA/d21zQXV0aFNpZ249')
        try:
            userAgent = self.getUserAgent()
            logger.debug('Final UserAgent : %s' % userAgent, __name__)
            filename = userAgent[:4]

            import datetime  ,hashlib
            timesegment = datetime.datetime.utcnow().strftime("%m/%d/%Y %H:%M:%S")
            validtime=userAgent[4]

            headers = {'User-Agent':base64.b64decode('UGFrJTIwVFYvMS4wIENGTmV0d29yay83NTguMC4yIERhcndpbi8xNS4wLjA=')}
            ipstring = client.request(base64.b64decode("aHR0cHM6Ly9hcHAuZHluZG5zLnR2L3RvcC9pcF9jaGVjay5waHA="), headers=headers)
            ipadd=ipstring.split('Address: ')[1]

            s="%s%s%s%s"%(ipadd,base64.b64decode("dHVtYmluamlhamF5bmFqYW5h")+userAgent[:10],timesegment ,validtime)

            dd=base64.b64decode("c2VydmVyX3RpbWU9JXMmaGFzaF92YWx1ZT0lcyZ2YWxpZG1pbnV0ZXM9JXM=")%(timesegment,base64.b64encode(hashlib.md5(s).hexdigest().lower()),validtime )
            url=(url%filename)+base64.b64encode(dd)

            headers={'User-Agent':cache.get(self.getDeviceID, 600000, table='live_cache'),
                     'Authorization':base64.b64decode('QmFzaWMgWW05emMyZGliM056T21kdmIyUm5aMjl2WkE9PQ==')}
            res = client.request(url, headers=headers)
            s = list(res)
            for i in range( (len(s)-59)/12):
                ind=len(s)-59 + (12*(i))
                if ind<len(s):
                    print ind
                    s[ind]=''
            return ''.join(s)
        except Exception as e:
            logger.error(e)
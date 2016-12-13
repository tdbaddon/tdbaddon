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
        self.headers = {'User-Agent':'umar/1.1 CFNetwork/758.0.2 Darwin/15.0.0'}
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
                url = urlparse.urljoin(self.base_link,self.ip_check)

                result = client.request(url, headers=self.headers)
                self.ipAddress = re.findall('Address: (.*)',result)[0]

                headers={'User-Agent':base64.b64decode('cDl4VE1nV2hFclpxZGlFWU1iV045bFVvd0xGMFdWM3I='), 'Authorization':base64.b64decode('QmFzaWMgWVcxMU9rQmtia0J1T0RRNQ==')}
                userAgent = client.request(base64.b64decode('aHR0cHM6Ly9hcHAuZHluZG5zLnR2L3RvcC9hcmFiaWN0dmhkdjFwLnBocA=='),headers=headers)
                self.deviceId = userAgent.split('.')[-1]

                TIME = time.time()
                second= str(TIME).split('.')[0]
                first =int(second)+int(base64.b64decode('NjkyOTY5Mjk='))
                token=base64.b64encode(base64.b64decode('JXNAMm5kMkAlcw==') % (str(first),second))

                headers = {'Authorization': base64.b64decode('QmFzaWMgWVdSdGFXNDZRV3hzWVdneFFBPT0='),
                           base64.b64decode("VXNlci1BZ2VudA=="):cache.get(self.getDeviceID, 600000, table='live_cache')}

                url = 'https://app.dyndns.tv/app_panelnew/output.php/playlist?type=xml&deviceSn=%s&token=%s' % (self.deviceId, token)

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
            useragent='User-Agent=AppleCoreMedia/1.0.0.%s (%s; U; CPU OS %s like Mac OS X; en_gb)'%(random.choice(['13G34' ,'13G36']),random.choice(['iPhone','iPad','iPod']),random.choice(['9_3_3','9_3_4','9_3_5']))
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

    def getUserAgent(self, option):
        useragent=''
        if option == 0:
            headers={'User-Agent':cache.get(self.getDeviceID, 8, table='live_cache'),
                     'Authorization':base64.b64decode('QmFzaWMgWVcxMU9rQmtia0J1T0RRNQ==')}
            return client.request('https://app.dynns.com/keys/pakindiahdv2ff.php',headers=headers)
        elif option==1:
            headers={'User-Agent':base64.b64decode('UGFrJTIwVFYvMS4wIENGTmV0d29yay83NTguMi44IERhcndpbi8xNS4wLjA='),
                     'Authorization':base64.b64decode('QmFzaWMgWVcxMU9rQmtia0J1T0RRNQ==')}
            useragent = client.request(base64.b64decode('aHR0cHM6Ly9hcHAuZHlubnMuY29tL2tleXMvYXJhYmljdHZoZHYxcC5waHA='),headers=headers)
        elif option == -1:
            return cache.get(self.getDeviceID, 8, table='live_cache')
        else:
            headers={'User-Agent':cache.get(self.getDeviceID, 8, table='live_cache'),
                     'Authorization':base64.b64decode('QmFzaWMgWVcxMU9rQmtia0J1T0RRNQ==')}
            useragent = client.request(base64.b64decode('aHR0cHM6Ly9hcHAuZHlubnMuY29tL2tleXMvYXJhYmljdHZoZHYxZmYucGhw'),headers=headers)
        logger.debug('UserAgent : %s' % useragent, __name__)
        return useragent.split('.')[-1]

    def getAuthToken(self):
        url=base64.b64decode('aHR0cHM6Ly9hcHAuZHluZG5zLnR2L3RvcC8lcy5waHA/d21zQXV0aFNpZ249')
        try:
            headers={'User-Agent':base64.b64decode('cDl4VE1nV2hFclpxZGlFWU1iV045bFVvd0xGMFdWM3I='), 'Authorization':base64.b64decode('QmFzaWMgWVcxMU9rQmtia0J1T0RRNQ==')}
            userAgent = client.request(base64.b64decode('aHR0cHM6Ly9hcHAuZHluZG5zLnR2L3RvcC9hcmFiaWN0dmhkdjFwLnBocA=='),headers=headers)
            self.deviceId = userAgent.split('.')[-1]
            filename = userAgent[:4]

            import datetime  ,hashlib
            timesegment = datetime.datetime.utcnow().strftime("%m/%d/%Y %H:%M:%S")
            validtime=userAgent[4]

            headers = {'User-Agent':base64.b64decode('UGFrJTIwVFYvMS4wIENGTmV0d29yay83NTguMC4yIERhcndpbi8xNS4wLjA=')}
            ipstring = client.request(base64.b64decode("aHR0cHM6Ly9hcHAuZHluZG5zLnR2L2tleXMvaXBfY2hlY2sucGhw"), headers=headers)
            ipadd=ipstring.split('Address: ')[1]

            s="%s%s%s%s"%(ipadd,base64.b64decode("ZmZlNmJiZTRjZThjNzdiMWJjMTQ1ODhiMmZmMGNjMDA=")+userAgent[:10],timesegment ,validtime)

            dd=base64.b64decode("c2VydmVyX3RpbWU9JXMmaGFzaF92YWx1ZT0lcyZ2YWxpZG1pbnV0ZXM9JXM=")%(timesegment,base64.b64encode(hashlib.md5(s).hexdigest().lower()),validtime )
            url=(url%filename)+base64.b64encode(dd)

            headers={'User-Agent':cache.get(self.getDeviceID, 600000, table='live_cache')}
            res = client.request(url, headers=headers)
            s=list(res)
            for i in range( (len(s)-59)/12):
                ind=len(s)-59 + (12*(i))
                if ind<len(s):
                    print ind
                    s[ind]=''
            return ''.join(s)
        except Exception as e:
            logger.error(e)
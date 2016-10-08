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

class source:
    def __init__(self):
        self.base_link = 'https://app.dynns.com'
        self.ip_check = '/keys/ip_check.php'
        self.live_link = '/livetv'
        self.channel_link = 'http://origin.dittotv.com/livetv/%s'
        self.poster_link = 'http://dittotv2.streamark.netdna-cdn.com/vod_images/optimized/livetv/%s.jpg'
        self.headers = {'User-Agent':'umar/1.1 CFNetwork/758.0.2 Darwin/15.0.0'}
        self.list = []
        self.deviceId = None
        self.ipAddress = None

    def getLiveSource(self):
        try :
            self.deviceId = cache.get(self.getDeviceID, 8)
            url = urlparse.urljoin(self.base_link,self.ip_check)

            result = client.source(url, headers=self.headers)
            self.ipAddress = re.findall('Address: (.*)',result)[0]

            headers = {'User-Agent':self.deviceId,
                       'SOAPAction':'http://app.dynns.com/saveDeviceIdService/tns:db.saveId',
                       'Content-Type':'text/xml; charset=ISO-8859-1'}

            xmldata=base64.b64decode("PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iSVNPLTg4NTktMSI/Pgo8U09BUC1FTlY6RW52ZWxvcGUgU09BUC1FTlY6ZW5jb2RpbmdTdHlsZT0iaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvc29hcC9lbmNvZGluZy8iIHhtbG5zOlNPQVAtRU5WPSJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy9zb2FwL2VudmVsb3BlLyIgeG1sbnM6eHNkPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxL1hNTFNjaGVtYSIgeG1sbnM6eHNpPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxL1hNTFNjaGVtYS1pbnN0YW5jZSIgeG1sbnM6U09BUC1FTkM9Imh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3NvYXAvZW5jb2RpbmcvIiB4bWxuczp0bnM9Imh0dHA6Ly9zY3JpcHRiYWtlci5jb20vc2F2ZURldmljZUlkU2VydmljZSI+CjxTT0FQLUVOVjpCb2R5Pgo8dG5zOmRiLnNhdmVJZCB4bWxuczp0bnM9Imh0dHA6Ly9hcHAuZHlubnMuY29tL3NhdmVEZXZpY2VJZFNlcnZpY2UiPgo8aWQgeHNpOnR5cGU9InhzZDpzdHJpbmciPiVzIEBkbkBuMDMzMTwvaWQ+CjxuYW1lIHhzaTp0eXBlPSJ4c2Q6c3RyaW5nIj4lczwvbmFtZT4KPC90bnM6ZGIuc2F2ZUlkPgo8L1NPQVAtRU5WOkJvZHk+CjwvU09BUC1FTlY6RW52ZWxvcGU+")%(self.ipAddress,self.deviceId)

            url = 'https://app.dynns.com/apisoap/index.php'
            result = client.source(url, headers=headers, post=xmldata)

            # get dynns userAgent
            userAgent = self.getUserAgent(1)

            url = ('https://app.dynns.com/app_panelnew/output.php/playlist?type=xml&deviceSn=%s')%userAgent+'&token=%s'

            TIME = time.time()
            second= str(TIME).split('.')[0]
            first =int(second)+int(base64.b64decode('NjkyOTY5Mjk='))
            token=base64.b64encode(base64.b64decode('JXNAMm5kMkAlcw==') % (str(first),second))

            headers = {'Authorization': base64.b64decode('QmFzaWMgWVdSdGFXNDZRV3hzWVdneFFBPT0='),
                        base64.b64decode("VXNlci1BZ2VudA=="):self.getDeviceID()}

            url = url % token
            result = client.source(url, headers=headers)

            result = client.parseDOM(result, "items")

            for channel in result:
                category = client.parseDOM(channel, "programCategory")[0]
                if category == 'Indian':
                    channelName = client.parseDOM(channel,"programTitle")[0]
                    channelName = cleantitle.live(channelName)
                    channelName = channelName.title()
                    poster = client.parseDOM(channel, "programImage")[0]
                    channelUrl = client.parseDOM(channel, "programURL")[0]
                    self.list.append({'name':client.replaceHTMLCodes(channelName), 'poster':poster,'url':channelUrl,'provider':'dynns','source':'dynns','direct':False, 'quality':'HD'})
            return self.list
        except:
            pass

    def resolve(self, url, resolverList):

        try :
            logger.debug('[%s] ORIGINAL URL [%s]' % (self.__class__, url))
            authToken = self.getAuthToken()
            logger.debug('[%s] AuthToken %s' % (self.__class__, authToken))
            url += authToken
            if '|' not in url:
                url += '|'

            import random
            useragent='User-Agent=AppleCoreMedia/1.0.0.%s (%s; U; CPU OS %s like Mac OS X; en_gb)'%(random.choice(['13G34' ,'13G36']),random.choice(['iPhone','iPad','iPod']),random.choice(['9_3_3','9_3_4','9_3_5']))
            url+=useragent
            logger.debug('[%s] RESOLVED URL [%s]' % (self.__class__, url))
            return url
        except Exception as e:
            logger.error(e)
            return False

    def getDeviceID(self):
        self.deviceId = binascii.b2a_hex(os.urandom(16)).upper()
        logger.debug('[%s] DeviceID : %s' % (self.__class__, self.deviceId))

    def getUserAgent(self, option):
        useragent=''
        if option == 0:
            headers={'User-Agent':cache.get(self.getDeviceID, 8),
                     'Authorization':base64.b64decode('QmFzaWMgWVcxMU9rQmtia0J1T0RRNQ==')}
            return client.source('https://app.dynns.com/keys/pakindiahdv2ff.php',headers=headers)
        elif option==1:
            headers={'User-Agent':base64.b64decode('UGFrJTIwVFYvMS4wIENGTmV0d29yay83NTguMi44IERhcndpbi8xNS4wLjA='),
                     'Authorization':base64.b64decode('QmFzaWMgWVcxMU9rQmtia0J1T0RRNQ==')}
            useragent = client.source(base64.b64decode('aHR0cHM6Ly9hcHAuZHlubnMuY29tL2tleXMvYXJhYmljdHZoZHYxcC5waHA='),headers=headers)
        elif option == -1:
            return cache.get(self.getDeviceID, 8)
        else:
            headers={'User-Agent':cache.get(self.getDeviceID, 8),
                     'Authorization':base64.b64decode('QmFzaWMgWVcxMU9rQmtia0J1T0RRNQ==')}
            useragent = client.source(base64.b64decode('aHR0cHM6Ly9hcHAuZHlubnMuY29tL2tleXMvYXJhYmljdHZoZHYxZmYucGhw'),headers=headers)
        logger.debug('[%s] UserAgent : %s' % (self.__class__, useragent))
        return useragent.split('.')[-1]

    def getAuthToken(self):
        import time

        for url,option in [('aHR0cHM6Ly9hcHAuZHlubnMuY29tL2tleXMvYmFrLnBocD90b2tlbj0=',2),('aHR0cHM6Ly9hcHAuZHlubnMuY29tL2tleXMvUGFrLnBocD90b2tlbj0=',1)]:
            try:
                TIME = time.time()
                second= str(TIME).split('.')[0]
                first =int(second)+int(base64.b64decode('NjkyOTY5Mjk='))
                token=base64.b64encode(base64.b64decode('JXNAMm5kMkAlcw==') % (str(first),second))

                headers = {'Authorization': "Basic %s"%base64.b64decode('Wkdsc1pHbHNaR2xzT2xCQWEybHpkRUJ1'),
                           base64.b64decode("VXNlci1BZ2VudA=="):self.getUserAgent(-1)}
                logger.debug('[%s] Token : %s url : %s' % (self.__class__, token, base64.b64decode(url)))
                result = client.source(base64.b64decode(url)+token, headers=headers)
                logger.debug('[%s] AuthToken : %s' % (self.__class__, result))
                return result
            except Exception as e:
                logger.error(e)
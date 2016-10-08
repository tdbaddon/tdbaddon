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


import datetime, base64, hashlib, re, urllib, urlparse, json
#from resources.lib.libraries import net
from resources.lib.libraries import client
from resources.lib.libraries import cleantitle
from resources.lib.libraries import logger

class source:
    def __init__(self):
        self.base_link = 'https://app.uktvnow.net/'
        self.token_link = 'http://uktvnow.net/app2/'
        self.channel_link = 'v3/get_all_channels'
        self.valid_link = 'v3/get_valid_link'
        self.user_agent_link = 'v3/get_user_agent'
        self.now = datetime.datetime.now()
        self.username = '-1'
        self.channels = {'colors':'http://www.lyngsat-logo.com/logo/tv/cc/colors_in.png',
                         'arydigital':'http://www.lyngsat-logo.com/logo/tv/aa/ary_digital_asia.png',
                         'arynews':'http://www.lyngsat-logo.com/logo/tv/aa/ary_news_uk.png',
                         'ibnmarathi':'http://www.lyngsat-logo.com/logo/tv/ii/ibn_lokmat.png',
                         'lifetime':'http://www.lyngsat-logo.com/logo/tv/ll/lifetime_us.png',
                         'moviesok':'http://www.lyngsat-logo.com/logo/tv/uu/utv_movies.png',
                         'ptcpunjabi':'http://www.lyngsat-logo.com/logo/tv/pp/ptc_punjabi_ca.png',
                         'ptvhome':'http://www.lyngsat-logo.com/logo/tv/pp/ptv_home_pk.png',
                         'ptvnews':'http://www.lyngsat-logo.com/logo/tv/pp/ptv_news_pk.png',
                         'ptvworld':'http://www.lyngsat-logo.com/logo/tv/pp/ptv_world_pk.png',
                         'stargold':'http://www.lyngsat-logo.com/logo/tv/ss/star_gold.png',
                         'starplus':'http://www.lyngsat-logo.com/logo/tv/ss/star_plus.png',
                         'tensports':'http://www.lyngsat-logo.com/logo/tv/tt/ten_sports_in.png',
                         'vh1':'http://www.lyngsat-logo.com/logo/tv/vv/vh1_global.png'}
        self.img_link = 'https://app.uktvnow.net/'
        self.list = []

    def getAPIToken(self, url, username=None):
        #s = "uktvnow-token-"+ self.now.strftime('%B-%d-%Y') + "-"+ "_|_-" + self.base_link + "-" + self.username +"-" + "_|_"+ "-"+ base64.b64decode("MTIzNDU2IUAjJCVedWt0dm5vd14lJCNAITY1NDMyMQ==")
        if username is None:
            username = self.username
        if self.valid_link in url:
            s =  'uktvnow-token--_|_-%s-uktvnow_token_generation-%s-_|_-123456_uktvnow_654321-_|_-uktvnow_link_token' % (self.base_link+url, username)
        else :
            s = "uktvnow-token--_|_-%s-uktvnow_token_generation-%s-_|_-123456_uktvnow_654321" % (self.base_link+url, username)
        return hashlib.md5(s).hexdigest()

    def getLiveSource(self):
        try :
            headers={'User-Agent':'USER-AGENT-UKTVNOW-APP-V2',
                     'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                     'Accept-Encoding' : 'gzip',
                     'app-token':self.getAPIToken(self.channel_link),
                     'Connection':'Keep-Alive',
                     'Host':'app.uktvnow.net'}
            post= urllib.urlencode({'username':self.username})
            url = urlparse.urljoin(self.base_link, self.channel_link)
            channels = client.source(url,post=post, headers=headers, compression=True)
            channels = channels.replace('\/','/')
            channellist=re.compile('"pk_id":"(.+?)","channel_name":"(.+?)","img":"(.+?)","http_stream":"(.+?)","rtmp_stream":"(.+?)","cat_id":"(.+?)"').findall(channels)
            filter = []
            for channel in self.channels.keys() : filter += [i for i in channellist if cleantitle.movie(i[1]) == channel]
            channellist = filter
            for id, name,thumbnail,httpurl,rtmpurl,cat in channellist:
                self.list.append({'name':name, 'poster':self.channels[cleantitle.movie(name)],'url':id,'provider':'uktvnow','source':'uktvnow','direct':False})
            return self.list
        except :
            return self.list

    def resolve(self, url, resolverList):

        try :
            logger.debug('[%s] ORIGINAL URL [%s]' % (__name__, url))
            token = self.getAPIToken(self.user_agent_link)
            headers={'User-Agent':'USER-AGENT-UKTVNOW-APP-V2',
                     'Accept-Encoding' : 'gzip',
                     'app-token':token}
            post = urllib.urlencode({'User-Agent':'USER-AGENT-UKTVNOW-APP-V2','app-token':token})
            result = client.source(self.token_link+self.user_agent_link, post=post, headers=headers, compression=True)
            result = re.compile('"msg":{".+?":"(.+?)"}}').findall(result)[0]
            magic="1579547dfghuh,09458721242affde,45h4jggf5f6g,f5fg65jj46,eedcfa0489174392".split(',')
            from resources.lib.libraries import pyaes
            decryptor = pyaes.new(magic[1], pyaes.MODE_CBC, IV=magic[4])
            userAgent = decryptor.decrypt(result.decode("hex")).split('\0')[0]


            playlistToken = self.getAPIToken(self.token_link+self.valid_link, self.username+url)
            headers={'User-Agent':userAgent,
                     'Accept-Encoding' : 'gzip',
                     'app-token':playlistToken}
            post = urllib.urlencode({'useragent':userAgent,
                                     'username':self.username, 'channel_id':url, 'version':'5.7'})

            result = client.source(self.token_link+self.valid_link, post=post, headers=headers, compression=True)
            result=re.compile('"channel_name":"(.+?)","img":".+?","http_stream":"(.+?)","rtmp_stream":"(.+?)"').findall(result)
            for name, httpstream, rtmpstream in result:
                url = httpstream
                magic="1579547dfghuh,09458721242affde,45h4jggf5f6g,f5fg65jj46,eedcfa0489174392".split(',')
                decryptor = pyaes.new(magic[1], pyaes.MODE_CBC, IV=magic[4])
                url= decryptor.decrypt(url.decode("hex")).split('\0')[0]
            logger.debug('[%s] RESOLVED URL [%s]' % (__name__, url))
            return url
        except :
            return False

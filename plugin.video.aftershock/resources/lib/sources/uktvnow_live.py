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


import datetime, base64, hashlib, re, urllib, urlparse
from resources.lib.libraries import client
from resources.lib.libraries import cleantitle

class source:
    def __init__(self):
        self.base_link = 'https://app.uktvnow.net/'
        self.channel_link = 'v1/get_all_channels'
        self.now = datetime.datetime.now()
        self.username = 'goat'
        self.apiToken = self.getAPIToken()
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

    def getAPIToken(self):
        s = "uktvnow-token-"+ self.now.strftime('%B-%d-%Y') + "-"+ "_|_-" + self.base_link + "-" + self.username +"-" + "_|_"+ "-"+ base64.b64decode("MTIzNDU2IUAjJCVedWt0dm5vd14lJCNAITY1NDMyMQ==")
        return hashlib.md5(s).hexdigest()

    def getLiveSource(self):
        try :
            headers = {'Content-Type':'application/x-www-form-urlencoded'}
            headers={'User-Agent':'USER-AGENT-UKTVNOW-APP-V1',
                     'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                     'Accept-Encoding' : 'gzip',
                     'app-token':self.apiToken,
                     'Connection':'Keep-Alive',
                     'Host':'app.uktvnow.net'}
            post= urllib.urlencode({'username':'goat'})
            url = urlparse.urljoin(self.base_link, self.channel_link)
            channels = client.source(url,post=post, headers=headers, compression=True)
            channels = channels.replace('\/','/')
            channellist=re.compile('"channel_name":"(.+?)","img":"(.+?)","http_stream":"(.+?)","rtmp_stream":"(.+?)","cat_id":"(.+?)"').findall(channels)
            filter = []
            for channel in self.channels.keys() : filter += [i for i in channellist if cleantitle.movie(i[0]) == channel]
            channellist = filter
            for name,thumbnail,httpurl,rtmpurl,cat in channellist:
                self.list.append({'name':name, 'poster':self.channels[cleantitle.movie(name)],'url':rtmpurl,'provider':'uktvnow','direct':True})
            return self.list
        except :
            return self.list

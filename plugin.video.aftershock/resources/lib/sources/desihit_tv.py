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


import re,urllib,urlparse,json

from resources.lib.libraries import client
from resources.lib import resolvers
from resources.lib.libraries import logger

class source:
    def __init__(self):
        self.base_link = 'http://www.desihit.tv'
        self.search_link = '/wp-admin/admin-ajax.php?td_theme_name=Newsmag&v=2.3.5'

    def get_show(self, tvshowurl, imdb, tvdb, tvshowtitle, year):
        if tvshowurl:
            return tvshowtitle

    def get_episode(self, url, ep_url, imdb, tvdb, title, date, season, episode):
        query = '%s %s' % (imdb, title)

        post = urllib.urlencode({'action': 'td_ajax_search', 'td_string':query})
        url = urlparse.urljoin(self.base_link, self.search_link)
        headers = {'Content-Type':'application/x-www-form-urlencoded'}
        result = client.request(url, post=post, referer=self.base_link, headers=headers)
        result = result.decode('iso-8859-1').encode('utf-8')
        result = result.replace('\n','').replace('\t','')

        result = json.loads(result)
        result = result['td_data']
        ep_url = client.parseDOM(result, "a", ret="href")[0]

        ep_url = re.compile('.+/(.+?)/').findall(ep_url)[0]
        if ep_url :
            return ep_url

    def get_sources(self, url):
        logger.debug('SOURCES URL %s' % url, __name__)
        try:
            quality = ''
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            try: result = client.request(url)
            except: result = ''

            result = result.decode('iso-8859-1').encode('utf-8')
            result = result.replace('\n','').replace('\t','').replace('\r','')

            result = client.parseDOM(result, "div", attrs={"class":"td-post-content td-pb-padding-side"})[0]
            result = client.parseDOM(result, "p", attrs={"style":"text-align: center;"})

            for item in result:
                try :
                    urls = client.parseDOM(item, "a", ret="href")
                    quality = client.parseDOM(item, "b")

                    quality = " ".join(quality)
                    quality = quality.lower()
                    if "720p" in quality :
                        quality = "HD"
                    else:
                        quality = "SD"

                    for i in range(0, len(urls)):
                        urls[i] = client.urlRewrite(urls[i])
                    host = client.host(urls[0])
                    if len(urls) > 1:
                        url = "##".join(urls)
                    else:
                        url = urls[0]
                    sources.append({'source': host, 'parts' : str(len(urls)), 'quality': quality, 'provider': 'DesiHit', 'url': url, 'direct':False})
                except :
                    pass
            logger.debug('SOURCES [%s]' % sources, __name__)
            return sources
        except:
            return sources


    def resolve(self, url, resolverList):
        logger.debug('ORIGINAL URL [%s]' % url, __name__)
        try:
            tUrl = url.split('##')
            if len(tUrl) > 0:
                url = tUrl
            else :
                url = urlparse.urlparse(url).path

            links = []
            for item in url:
                r = resolvers.request(item, resolverList)
                if not r :
                    raise Exception()
                links.append(r)
            url = links
            logger.debug('RESOLVED URL [%s]' % url, __name__)
            return url
        except:
            return False
'''
Created on Jan 2, 2014

@author: ajdeveloped@gmail.com

This file is part of XOZE. 

XOZE is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

XOZE is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with XOZE.  If not, see <http://www.gnu.org/licenses/>.
'''
import htmlentitydefs
import logging
import re
import urllib
import urlparse

import xbmcgui  # @UnresolvedImport
from xoze.utils import http

try:
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
except:
    #do nothing
    print 'ssl verified context available'

def cUConvert(m): return unichr(int(m.group(1)))
def cTConvert(m): return unichr(htmlentitydefs.name2codepoint.get(m.group(1), 32))

def convertHTMLCodes(html):
    try:
        html = re.sub('&#(\d{1,5});', cUConvert, html.decode('utf-8', 'replace'))
        html = re.sub('&(\w+?);', cTConvert, html)
    except:
        logging.getLogger().error('convertHTMLCodes()')
    return html
    

class googleImagesAPI:
    baseURL = 'https://www.google.com.au/search?num={start}&filter=0&source=lnms&tbm=isch{query}'
    perPage = 20

    def createQuery(self, terms, **kwargs):
        args = ['q={0}'.format(urllib.quote_plus(terms))]
        for k in kwargs.keys():
            if kwargs[k]: args.append('{0}={1}'.format(k, kwargs[k]))
        return '&'.join(args)
        
    def parseQuery(self, query):
        return dict(urlparse.parse_qsl(query))
    
    def parseImages(self, html):
        matches = re.compile('\"ou\"\:\"(.+?)\"').findall(html)
        results = []
        i = 0
        for match in matches:
            i = i + 1
            results.append({'title':str(i), 'unescapedUrl':urllib.unquote(match)})
        return results
    
    def getImages(self, query, page=1):
        start = ''
        if page > 1: start = '&start=%s' % ((page - 1) * self.perPage)
        url = self.baseURL.format(start=start, query='&' + query)
        html = self.getPage(url) 
        return self.parseImages(html)

    def getPage(self, url):
        return http.HttpClient().get_html_content(url=url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'})
        

def load_tv_show_images(req_attrib, modelMap):
    logging.getLogger().debug('load tv show image...')
    tv_show_name = req_attrib['tv-show-name']
    tv_show_url = req_attrib['tv-show-url']
    channel_type = req_attrib['channel-type']
    channel_name = req_attrib['channel-name']
    
    logging.getLogger().debug('search tv show images...' + channel_name.lower() + ' ' + tv_show_name.lower() + ' poster')
    tv_show_options = get_image(channel_name.lower() + ' ' + tv_show_name.lower() + ' poster' , tv_show_name, tv_show_url, channel_type, channel_name)
    
    modelMap['tv-show-images'] = tv_show_options
        
    
def parse_image(results, tv_show_name, tv_show_url, channel_type, channel_name):
    count = 0
    tv_show_images = []
    
    for image_info in results:
        url = image_info['unescapedUrl']
        # Remove file-system path characters from name.
        title = image_info['title']
        count = count + 1
#         text = 'icon' + str(count)
        
        logging.getLogger().debug(url)
        item = xbmcgui.ListItem(label=title, iconImage=url, thumbnailImage=url)
        item.setProperty('channel-type', channel_type)
        item.setProperty('channel-name', channel_name)
        item.setProperty('tv-show-name', tv_show_name)
        item.setProperty('tv-show-url', tv_show_url)
        item.setProperty('tv-show-thumb', url)
        tv_show_images.append(item)
    return tv_show_images
        

def get_image(terms, tv_show_name, tv_show_url, channel_type, channel_name):
    try:
        api = googleImagesAPI()
        query = api.createQuery(terms)
        results = api.getImages(query)
        return parse_image(results, tv_show_name, tv_show_url, channel_type, channel_name)
    except Exception, e:
        logging.getLogger().error(e)
        return None

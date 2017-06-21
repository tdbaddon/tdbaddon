'''
mhdtvlive deccandelight plugin
Copyright (C) 2016 Gujal

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
from main import Scraper
from BeautifulSoup import BeautifulSoup, SoupStrainer
import urllib, re, requests
import HTMLParser

class mhdtv(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://mhdtvlive.com/'
        self.icon = self.ipath + 'mhdtv.png'
        self.list = {'01Tamil TV': self.bu + 'tamil_channels',
                     '02Telugu TV': self.bu + 'telugu_channels',
                     '03Malayalam TV': self.bu + 'malayalam_channels',
                     '04Kannada TV': self.bu + 'kannada_channels',
                     '05Hindi TV': self.bu + 'hindi_channels',
                     '06English TV': self.bu + 'english_channels'}
            
    def get_menu(self):
        return (self.list,7,self.icon)
        
    def get_items(self,iurl):
        channels = []
        h = HTMLParser.HTMLParser()
        mlink = SoupStrainer('div', {'class':re.compile('^row ')})
        plink = SoupStrainer('ul', {'class':'pagination'})
        nextpg = True
        while nextpg:
            nextpg = False
            html = requests.get(iurl, headers=self.hdr).text
            mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
            Paginator = BeautifulSoup(html, parseOnlyThese=plink)
            items = mdiv.findAll('div', {'class':re.compile('^col-sm-')})
            for item in items:
                title = h.unescape(item.h3.text).encode('utf8')
                url = item.find('a')['href']
                thumb = item.find('img')['src']
                channels.append((title, thumb, url))
            if 'Next' in str(Paginator):
                nextdiv = Paginator.find('a', {'class':'next page-numbers'})
                iurl = nextdiv.get('href')
                nextpg = True  
        return (sorted(channels),9) 

    def get_video(self,url):

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('iframe')
        item = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            tlink = item.find('iframe')['src']
            if 'mhdtvlive.' in tlink or 'livemalayalamtv.' in tlink:
                html = requests.get(tlink, headers=self.hdr).text
                if 'unescape(' in html:
                    strdata = re.findall("unescape\('(.*?)'", html)[0]
                    html = urllib.unquote(strdata)
                stream_url = re.findall('stream = "(.*?)"',html)[0]
            elif 'yupptv.' in tlink:
                html = requests.get(tlink, headers=self.hdr).text
                stream_url = re.findall("file:\s?'(.*?m3u8.*?')",html)[0] + '|User-Agent=Mozilla/5.0 (yupp_andro_mob)'
            elif 'youtube.' in tlink:
                stream_url = tlink
            else:
                xbmc.log('%s not resolvable.\n'%tlink)
        except:
            stream_url = None
            
        return stream_url
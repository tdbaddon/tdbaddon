'''
abcmalayalam deccandelight plugin
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

class abcm(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://abcmalayalam.com'
        self.icon = self.ipath + 'abcm.png'
        self.list = {'01Movies': self.bu + '/movies',
                     '02Short Films': self.bu + '/short-film'}

    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'itemList'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        plink = SoupStrainer('div', {'class':'k2Pagination'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        items = mdiv.findAll('div', {'class':re.compile('catItemView')})
        
        for item in items:
            title = h.unescape(item.h3.text)
            title = self.clean_title(title)
            url = self.bu + item.find('a')['href']
            thumb = self.bu + item.find('img')['src']
            movies.append((title, thumb, url))
        
        if 'Next' in str(Paginator):
            pdiv = Paginator.find('li', {'class':'pagination-next'})
            purl = self.bu + pdiv.a.get('href')
            pgtxt = re.findall('(Page.*)',Paginator.text)[0]
            title = 'Next Page.. (Currently in %s)' % pgtxt
            movies.append((title, self.nicon, purl))
        
        return (movies,8)

    def get_videos(self,url):
        videos = []
            
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'itemFullText'})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            links = videoclass.findAll('div', {'class':'avPlayerContainer'})
            for link in links:
                vidurl = link.find('iframe')['src']
                if 'http:' not in vidurl:
                    vidurl = 'http:' + vidurl
                self.resolve_media(vidurl,videos)
        except:
            pass

        try:
            table = videoclass.find('div', {'class':'divTable'})
            links = table.findAll('a')
            for link in links:
                vidurl = link.get('href')
                self.resolve_media(vidurl,videos)
        except:
            pass

        try:
            table = videoclass.find('table')
            links = table.findAll('a')
            for link in links:
                vidurl = link.get('href')
                self.resolve_media(vidurl,videos)
        except:
            pass
      
        return videos

'''
apnaview deccandelight plugin
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

class apnav(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://apnaview.com/browse/'
        self.icon = self.ipath + 'apnav.png'
        self.list = {'01Tamil Movies': self.bu + 'tamil',
                     '02Telugu Movies': self.bu + 'telugu',
                     '03Malayalam Movies': self.bu + 'Malayalam',
                     '04Hindi Movies': self.bu + 'hindi',
                     '05Marathi Movies': self.bu + 'marathi',
                     '06Punjabi Movies': self.bu + 'punjabi',
                     '07[COLOR cyan]Adult Movies[/COLOR]': self.bu+ '?genre=32',
                     '08[COLOR yellow]** Search **[/COLOR]': self.bu[:-7] + '?q='}

    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []
        if url[-3:] == '?q=':
            search_text = self.get_SearchQuery('Apna View')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'row'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        plink = SoupStrainer('ul', {'class':re.compile('^pagination')})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        items = mdiv.findAll('div', {'class':re.compile('col-xl-2 mb-4$')})
        
        for item in items:
            title = h.unescape(item.text)
            title = self.clean_title(title)
            url = self.bu[:-8] + item.find('a')['href']
            try:
                thumb = self.bu[:-8] + item.find('img')['src']
            except:
                thumb = self.icon
            movies.append((title, thumb, url))
        
        if 'Next' in str(Paginator):
            nextli = Paginator.find('li', {'class':'next page'})
            purl = self.bu[:-8] + nextli.find('a')['href']
            pgtxt = Paginator.find('li', {'class':'active'}).text
            title = 'Next Page.. (Currently in Page %s)' % pgtxt
            movies.append((title, self.nicon, purl))
        
        return (movies,8)

    def get_videos(self,url):
        videos = []
        h = HTMLParser.HTMLParser()    
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('table', {'class':re.compile('^table')})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            links = videoclass.findAll('a')
            for link in links:
                vidurl = link.get('href')
                vidtxt = h.unescape(link.text)
                if 'http' in vidurl:
                    self.resolve_media(vidurl,videos,vidtxt)

        except:
            pass
      
        return videos

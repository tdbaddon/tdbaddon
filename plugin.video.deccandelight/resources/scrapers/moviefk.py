'''
moviefk deccandelight plugin
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

class moviefk(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://moviefka.net/category/'
        self.icon = self.ipath + 'moviefk.png'
        self.list = {'01Tamil Movies': self.bu + 'tamil-movies/',
                     '02Telugu Movies': self.bu + 'telugu-movies/',
                     '03Hindi Movies': self.bu + 'hindi-movies/',
                     '04English Movies': self.bu + 'hollywood-movies/',
                     '05Hindi Dubbed Movies': self.bu + 'hindi-dubbed-movies/',
                     '06Punjabi Movies': self.bu + 'punjabi-movies/',
                     '07Urdu Movies': self.bu + 'pakistani-movies/',
                     '09[COLOR yellow]** Search **[/COLOR]': self.bu[:-9] + '?s='}
             
    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('Movie FK')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'id':'archive'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        plink = SoupStrainer('div', {'class':'navigation'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        items = mdiv.findAll('li')
        
        for item in items:
            if 'postcontent' in str(item):
                title = h.unescape(item.h2.text)
                title = self.clean_title(title)
                url = item.find('a')['href']
                try:
                    thumb = item.find('img')['src']
                except:
                    thumb = self.icon
                movies.append((title, thumb, url))
        
        if 'next' in str(Paginator):
            currpg = Paginator.find('span', {'class':re.compile('current')}).text
            nlink = Paginator.find('a', {'class':re.compile('^next')})
            purl = nlink.get('href')
            pages = Paginator.findAll('a', {'class':'page-numbers'})
            lastpg = pages[len(pages)-1].text
            title = 'Next Page.. (Currently in Page %s of %s)' % (currpg,lastpg)
            movies.append((title, self.nicon, purl))
        
        return (movies,8)

    def get_videos(self,url):
        videos = []
            
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'entry'})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)
        links = videoclass.findAll('a', {'title':re.compile('.')})

        for link in links:
            try:
                vidurl = link.get('href')
                self.resolve_media(vidurl,videos)
            except:
                pass
      
        return videos

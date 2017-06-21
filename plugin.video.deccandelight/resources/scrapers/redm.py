'''
redmovies deccandelight plugin
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

class redm(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://redmovies.me/category/'
        self.icon = self.ipath + 'redm.png'
        self.list = {'01Tamil Movies': self.bu + 'tamil/',
                     '02Telugu Movies': self.bu + 'telugu/',
                     '03Malayalam Movies': self.bu + 'malayalam/',
                     '04Kannada Movies': self.bu + 'kannada-movies/',
                     '05Hindi Movies': self.bu + 'bollywood-movies/',
                     '06English Movies': self.bu + 'hollywood-movies/',
                     '07Animation Movies': self.bu + 'animation/',
                     '08Hindi Dubbed Movies': self.bu + 'hindi-dubbed/',
                     '09Punjabi Movies': self.bu + 'punjabi-movies/',
                     '10Urdu Movies': self.bu + 'pakistan/',
                     '12[COLOR yellow]** Search **[/COLOR]': self.bu[:-9] + '?s='}

    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('Red Movies')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'nag cf'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        plink = SoupStrainer('div', {'class':'wp-pagenavi'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        items = mdiv.findAll('div', {'id':re.compile('^post')})
        
        for item in items:
            title = h.unescape(item.h2.text)
            title = self.clean_title(title)
            url = item.find('a')['href']
            thumb = item.find('img')['src'].split('?')[0]
            movies.append((title, thumb, url))
        
        if 'next' in str(Paginator):
            purl = Paginator.find('a', {'class':'nextpostslink'})['href']
            pgtxt = Paginator.find('span', {'class':'pages'}).text
            title = 'Next Page.. (Currently in %s)' % pgtxt
            movies.append((title, self.nicon, purl))
        
        return (movies,8)

    def get_videos(self,url):
        videos = []
            
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer("div", {"id":"content"})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            links = videoclass.findAll('iframe')
            for link in links:
                url = link.get('src')
                self.resolve_media(url,videos)

        except:
            pass
      
        return videos

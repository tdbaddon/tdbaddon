'''
malayalam serials deccandelight plugin
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

class mserial(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://malayalamserials.in/category/'
        self.icon = self.ipath + 'mserial.png'
        self.list = {'01Asianet': self.bu + 'asianet/',
                     '02Mazhavil Manorama': self.bu + 'mazhavil/',
                     '03Surya': self.bu + 'surya/',
                     '04Kairali': self.bu + 'kairali/',
                     '05Flowers': self.bu + 'flowers/',
                     '06Media One': self.bu + 'media/',
                     '07Amrita': self.bu + 'amrita/',
                     '08Movies': self.bu + 'movies/',
                     '09News': self.bu + 'news/',
                     '10Gossip': self.bu + 'malayalam_movie/',
                     '11[COLOR yellow]** Search **[/COLOR]': self.bu[:-9] + '?s='}
    
    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('Malayalam Serials')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('ul', {'class':re.compile('^listing-videos')})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        items = mdiv.findAll('li')
        plink = SoupStrainer('div', {'class':'pagination'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)

        for item in items:
            title = h.unescape(item.text).encode('utf8')
            url = item.find('a')['href']
            try:
                thumb = item.find('img')['src']
            except:
                thumb = self.icon
            movies.append((title, thumb, url))
        
        if 'next' in str(Paginator):
            nextli = Paginator.find('a', {'class':re.compile('next')})
            purl = nextli.get('href')
            currpg = Paginator.find('span', {'class':re.compile('current')}).text
            pages = Paginator.findAll('a', {'class':re.compile('^page')})
            lastpg = pages[len(pages)-1].text
            title = 'Next Page.. (Currently in Page %s of %s)' % (currpg,lastpg)
            movies.append((title, self.nicon, purl))
        
        return (movies,8)

    def get_videos(self,url):
        videos = []
            
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'id':'video-code'})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            links = videoclass.findAll('iframe')
            for link in links:
                url = link.get('src')
                self.resolve_media(url,videos)
        except:
            pass

        try:
            links = videoclass.findAll('a')
            for link in links:
                curl = link.get('onclick')
                url = re.findall("'(http.*?)'",curl)[0]
                if 'dai.ly' in url:
                    url = requests.get(url, headers=self.hdr).url
                self.resolve_media(url,videos)
        except:
            pass
            
        return videos

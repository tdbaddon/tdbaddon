'''
tamilyogi deccandelight plugin
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
import urllib, requests
import HTMLParser

class tyogi(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://tamilyogi.cc/category/'
        self.icon = self.ipath + 'tyogi.png'
        self.list = {'01New Movies': self.bu + 'tamilyogi-full-movie-online/',
                     '02HD Movies': self.bu + 'tamilyogi-bluray-movies/',
                     '03DVD Movies': self.bu + 'tamilyogi-dvdrip-movies/',
                     '04Dubbed Movies': self.bu + 'tamilyogi-dubbed-movies-online/',
                     '07[COLOR yellow]** Search **[/COLOR]': self.bu[:-9] + '?s='}
    
    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('Tamil Yogi')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer("div", {"id":"archive"})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        plink = SoupStrainer("div", {"class":"navigation"})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        items = mdiv.findAll('li')
        for item in items:
            if '"cleaner"' not in str(item):
                title = h.unescape(item.text)
                title = self.clean_title(title)
                url = item.a.get('href')
                try:
                    thumb = item.img.get('src')
                except:
                    thumb = self.icon
                movies.append((title, thumb, url))
        
        if 'next' in str(Paginator):
            nextpg = Paginator.find('a', {'class':'next page-numbers'})
            purl = nextpg.get('href')
            currpg = Paginator.find('span', {'class':'page-numbers current'}).text
            pages = Paginator.findAll('a', {'class':'page-numbers'})
            lastpg = pages[len(pages)-1].text
            title = 'Next Page.. (Currently in Page %s of %s)' % (currpg,lastpg)
            movies.append((title, self.nicon, purl))
        
        return (movies,8)

    def get_videos(self,url):
        videos = []
            
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer("div", {"class":"entry"})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            links = videoclass.findAll('iframe')
            for link in links:
                url = link.get('src')
                self.resolve_media(url,videos)

        except:
            pass
      
        return videos

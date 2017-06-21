'''
tamilgun deccandelight plugin
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
import urllib, re, requests, json, HTMLParser
import resources.lib.jsunpack as jsunpack

class tgun(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://tamilgun.ooo/categories/'
        self.icon = self.ipath + 'tgun.png'
        self.list = {'01New Movies': self.bu + 'new-movies-a/',
                     '02HD Movies': self.bu + 'hd-movies/',
                     '03Dubbed Movies': self.bu + 'dubbed-movies/',
                     '04Trailers': self.bu + 'trailers/',
                     '05Special Shows': self.bu + 'special-tv-shows/',
                     '06[COLOR yellow]** Search **[/COLOR]': self.bu[:-11] + '?s='}
    
    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('Tamil Gun')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('article', {'class':re.compile('video')})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)

        plink = SoupStrainer('ul', {'class':'page-numbers'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)

        for item in mdiv:
            title = h.unescape(item.h3.text).encode('utf8')
            url = item.h3.find('a')['href']
            try:
                thumb = item.find('img')['src'].strip()
            except:
                thumb = self.icon
            movies.append((title, thumb, url))
        
        if 'next' in str(Paginator):
            nextli = Paginator.find('a', {'class':re.compile('next')})
            purl = nextli.get('href')
            if 'http' not in purl:
                purl = self.bu[:-12] + purl
            currpg = Paginator.find('span', {'class':re.compile('current')}).text
            pages = Paginator.findAll('a', {'class':re.compile('^page')})
            lastpg = pages[len(pages)-1].text
            title = 'Next Page.. (Currently in Page %s of %s)' % (currpg,lastpg)
            movies.append((title, self.nicon, purl))
        
        return (movies,8)

    def get_videos(self,url):
        videos = []
        if 'cinebix.com' in url:
            self.resolve_media(url,videos)
            return videos
            
        html = requests.get(url, headers=self.hdr).text

        try:
            linkcode = jsunpack.unpack(html).replace('\\','')
            sources = json.loads(re.findall('sources:(.*?)\}\)',linkcode)[0])
            for source in sources:    
                url = source['file'] + '|Referer=%s'%self.bu[:-11]
                url = urllib.quote_plus(url)
                videos.append(('tamilgun | %s'%source['label'],url))
        except:
            pass

        mlink = SoupStrainer('div', {'id':'videoframe'})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            links = videoclass.findAll('iframe')
            for link in links:
                url = link.get('src')
                self.resolve_media(url,videos)
        except:
            pass

        mlink = SoupStrainer('div', {'class':'entry-excerpt'})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            links = videoclass.findAll('iframe')
            for link in links:
                if 'http' in str(link):
                    url = link.get('src')
                    self.resolve_media(url,videos)
        except:
            pass

        try:
            sources = json.loads(re.findall('vdf-data-json">(.*?)<',html)[0])
            url = 'https://www.youtube.com/watch?v=%s'%sources['videos'][0]['youtubeID']
            self.resolve_media(url,videos)
        except:
            pass
            
        return videos
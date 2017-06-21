'''
tamiltvshows deccandelight plugin
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

class ttvs(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://www.tamiltvshows.net/category/'
        self.icon = self.ipath + 'ttvs.png'
        self.list = {'01Recently Added': self.bu[:-9],
                     '02Sun TV Series': self.bu + 'sun-tv-serials/',
                     '03Sun TV Shows': self.bu + 'sun-tv-shows/',
                     '04Vijay TV Series': self.bu + 'vijay-tv-serials/',
                     '05Vijay TV Shows': self.bu + 'vijay-tv-shows/',
                     '06Zee Tamil TV Series': self.bu + 'zee-tamil-serials/',
                     '07Zee Tamil TV Shows': self.bu + 'zee-tv-shows/',
                     '08Raj TV Series': self.bu + 'raj-tv-serials/',
                     '09Raj TV Shows': self.bu + 'raj-tv-shows/',
                     '10Polimer TV Shows': self.bu + 'polimer-tv-serials/',
                     '11Captain TV Shows': self.bu + 'captain-tv-shows/',
                     '12Jaya TV Shows': self.bu + 'jaya-tv-programs/',
                     '13Kalaignar TV Shows': self.bu + 'kalaignar-tv-shows/',
                     '14Puthuyugam TV Shows': self.bu + 'puthuyugam/',
                     '15Puthiya Thalaimurai TV Shows': self.bu + 'puthiya-thalaimurai-tv-shows/',
                     '16[COLOR yellow]** Search **[/COLOR]': self.bu[:-9] + '?s='}

    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('Tamil TV Shows')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'id':'videos'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        plink = SoupStrainer('div', {'class':'wp-pagenavi'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        items = mdiv.findAll('div', {'class':re.compile('video')})
        
        for item in items:
            title = h.unescape(item.find('a')['title'])
            title = self.clean_title(title)
            url = item.find('a')['href']
            try:
                thumb = item.find('img')['src']
            except:
                thumb = self.icon
            movies.append((title, thumb, url))
        
        if 'next' in str(Paginator):
            nextli = Paginator.find('a', {'class':'nextpostslink'})
            purl = nextli.get('href')
            pgtxt = Paginator.find('span', {'class':'pages'}).text
            title = 'Next Page.. (Currently in %s)' % pgtxt
            movies.append((title, self.nicon, purl))
        
        return (movies,8)

    def get_videos(self,url):
        videos = []
            
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'entry'})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            links = videoclass.findAll('iframe')
            for link in links:
                vidurl = link.get('src')
                if ('tamiltvtube' in vidurl) or ('videozupload' in vidurl):
                    headers = self.hdr
                    headers['Referer'] = url
                    slink = requests.get(vidurl, headers=headers).text
                    hoster = 'TamilTVTube '
                    srclist = re.findall('(\[.*?\])', slink)[0]
                    strlinks = eval(srclist)
                    for strlink in strlinks:
                        elink = strlink['file']
                        if '&' in elink:
                            elink = urllib.quote(elink)
                        try:
                            qual = strlink['label']
                        except:
                            qual = 'HLS'
                        vidhost = hoster + qual
                        videos.append((vidhost,elink))
                else:
                    self.resolve_media(vidurl,videos)
        except:
            pass

        try:
            links = videoclass.findAll('a', {'type':'button'})
            for link in links:
                vidurl = re.findall("(http.*?)'",link.get('onclick'))[0]
                if 'tv?vq=medium#/' in vidurl:
                    vidurl = vidurl.replace('tv?vq=medium#/','')
                self.resolve_media(vidurl,videos)
        except:
            pass
            
        return videos

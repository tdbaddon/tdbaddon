'''
desitashan deccandelight plugin
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

class desit(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://www.desi-tashan.ms/'
        self.icon = self.ipath + 'desit.png'
            
    def get_menu(self):
        html = requests.get(self.bu, headers=self.hdr).text
        mlink = SoupStrainer('ul', {'class':'td-mobile-main-menu'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        items = mdiv.findAll('li')
        self.list = {}
        ino = 1
        for item in items:
            if ino < 10:
                self.list['0%s%s'%(ino,item.text)]=item.find('a')['href']
            else:
                self.list['%s%s'%(ino,item.text)]=item.find('a')['href']
            ino+=1
        self.list['99[COLOR yellow]** Search **[/COLOR]']= self.bu + '?s=MMMM7'
        return (self.list,5,self.icon)

    def get_second(self,iurl):
        """
        Get the list of shows.
        :return: list
        """
        shows = []
        h = HTMLParser.HTMLParser()

        html = requests.get(iurl, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':re.compile('td-page-content')})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        items = mdiv.findAll('li')
        thumb = mdiv.find('img')['src']
        for item in items:
            title = h.unescape(item.text)
            url = item.find('a')['href']
            shows.append((title,thumb,url))

        return (shows,7)
        
    def get_items(self,iurl):
        episodes = []
        h = HTMLParser.HTMLParser()
        if iurl[-3:] == '?s=':
            search_text = self.get_SearchQuery('Desi Tashan')
            search_text = urllib.quote_plus(search_text)
            iurl += search_text
        html = requests.get(iurl).text
        mlink = SoupStrainer('div', {'class':'td-ss-main-content'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        items = mdiv.findAll('div', {'class':'td-block-span6'})
        for item in items:
            title = h.unescape(item.h3.text)
            if 'written' not in title.lower():
                title = self.clean_title(title)
                url = item.find('a')['href']
                try:
                    icon = item.find('img')['src']
                except:
                    icon = self.icon           
                episodes.append((title,icon,url))
                
        plink = SoupStrainer('div', {'class':re.compile('^page-nav')})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)

        if 'menu-right' in str(Paginator):
            currpg = Paginator.find('span', {'class':'current'}).text
            nlinks = Paginator.findAll('a', {'class':None})
            for nlink in nlinks:
                if 'menu-right' in str(nlink):
                    purl = nlink.get('href')
            pgtxt = Paginator.find('span', {'class':'pages'}).text
            title = 'Next Page.. (Currently in %s)' % pgtxt
            episodes.append((title, self.nicon, purl))    
        return (episodes,8) 

    def get_videos(self,iurl):
        videos = []
        h = HTMLParser.HTMLParser()
        html = requests.get(iurl).text
        mlink = SoupStrainer('div', {'class':re.compile('^td-post-content')})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)
        items = videoclass.findAll('a', {'class':None})
        for item in items:
            vid_link = item['href']
            vidtxt = h.unescape(item.text)
            try:
                vidtxt = re.findall('(Part.*)',vidtxt)[0]
            except:
                vidtxt = ''
            if 'youpdates.' in vid_link:
                vhtml = requests.get(vid_link).text
                vplink = SoupStrainer('div', {'class':'main'})
                vsoup = BeautifulSoup(vhtml, parseOnlyThese=vplink)
                vid_url=None
                try:
                    vid_url = vsoup.find('iframe')['src']
                except:
                    pass
                try:
                    vid_url = re.findall('class="main".*?src="(.*?)"',vhtml,re.DOTALL)[0]
                except:
                    pass
                if vid_url:
                    self.resolve_media(vid_url,videos,vidtxt)
            else:
                self.resolve_media(vid_link,videos,vidtxt)
            
        return videos

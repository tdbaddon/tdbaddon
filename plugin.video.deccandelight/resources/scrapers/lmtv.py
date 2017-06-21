'''
livemalayalamtv deccandelight plugin
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

class lmtv(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://mhdtvlive.com/'
        self.icon = self.ipath + 'lmtv.png'
        self.list = {'01Entertainment Channels': self.bu + 'entertainment_channels',
                     '02News Channels': self.bu + 'news_channels',
                     '03Regional Channels': self.bu + 'regional_web_channels',
                     '04Devotional Channels': self.bu + 'devotional_channels',
                     '07[COLOR yellow]** Search **[/COLOR]': self.bu + '?s='}
  
    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('Live Malayalam TV')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':re.compile('^row ')})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        plink = SoupStrainer('ul', {'class':'pagination'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        items = mdiv.findAll('div', {'class':re.compile('^col-sm-')})
        for item in items:
            title = h.unescape(item.h3.text).encode('utf8')
            url = item.find('a')['href']
            thumb = item.find('img')['src']
            movies.append((title, thumb, url))

        if 'Next' in str(Paginator):
            nextpg = Paginator.find('a', {'class':'next page-numbers'})
            purl = nextpg.get('href')
            currpg = Paginator.find('span').text
            pages = Paginator.findAll('a', {'class':'page-numbers'})
            lastpg = pages[len(pages)-1].text
            title = 'Next Page.. (Currently in Page %s of %s)' % (currpg,lastpg)
            movies.append((title, self.nicon, purl))
        
        return (movies,9)
      
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
                stream_url = re.findall("file:\s?'(.*?m3u8.*?)'",html)[0] + '|User-Agent=Mozilla/5.0 (yupp_andro_mob)'
            elif 'youtube.' in tlink:
                stream_url = tlink
            else:
                xbmc.log('%s not resolvable.\n'%tlink)
        except:
            stream_url = None
            
        return stream_url

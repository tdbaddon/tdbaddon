import re
import requests
from ..scraper import Scraper
import xbmc

class Dizi720(Scraper):
    name = "dizi720p"
    domains = ['dizi720p.com/']
    sources = []

    def __init__(self):
        self.base_link = 'http://www.dizi720p.net/'

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_url = self.base_link+title.replace(' ','-')+'-'+season+'-sezon-'+episode+'-bolum.html'
            html = requests.get(start_url).text
            block = re.compile('<div id="konumuz">(.+?)<div class="btn-group begenmeler">',re.DOTALL).findall(html)
            for Block in block:
                print('12345')
                match = re.compile('<iframe src="(.+?)"').findall(str(Block))
                for frame in match:
                    if not '.html' in frame:
                        print(frame)
                        if 'watchserieshd.xyz' in frame:
                            html2 = requests.get(frame).text
                            match2 = re.compile('file: "(.+?)",.+?label: "(.+?)"',re.DOTALL).findall(html2)
                            for url,p in match2:
                                print(url)
                match_multi = re.compile('<a href="(.+?)">(.+?)</a>').findall(str(Block))
                for page,name in match_multi:
                    if not 'http' in name:
                        if '.ru' in name:
                            html3 = requests.get(page).text
                            match = re.compile('<iframe.+?src="(.+?)"').findall(html3)
                            for frame in match:
                                if not '.html' in frame:
                                    if name.lower() in frame:
                                        self.sources.append({'source': 'ok.ru', 'quality': 'SD', 'scraper': self.name, 'url': frame,'direct': False})
                        elif 'Openload' in name:
                            pass
                        elif 'UpTo' in name:
                            html3 = requests.get(page).text
                            match = re.compile('<iframe.+?src="(.+?)"').findall(html3)
                            for frame in match:
                                if not '.html' in frame:
                                    if name.lower() in frame:
                                        self.sources.append({'source': 'uptovideo', 'quality': 'SD', 'scraper': self.name, 'url': frame,'direct': False})
                        elif 'TheVideo' in name:
                            pass
                        elif 'eStream' in name:
                            html3 = requests.get(page).text
                            match = re.compile('<iframe.+?src="(.+?)"').findall(html3)
                            for frame in match:
                                if not '.html' in frame:
                                    if name.lower() in frame:
                                        self.sources.append({'source': 'estream', 'quality': 'SD', 'scraper': self.name, 'url': frame,'direct': False})
                            match2 = re.compile('<IFRAME.+?SRC="(.+?)"').findall(html3)
                            for frame in match2:
                                if name.lower() in frame:
                                    self.sources.append({'source': 'estream', 'quality': 'SD', 'scraper': self.name, 'url': frame,'direct': False})
                        elif 'Rapid' in name:
                            pass
                        elif 'ingilizce' in name:
                            pass
                        elif 'fragman' in name:
                            pass
                        elif 'Videomega' in name:
                            pass
                        elif 'VK' in name:
                            html3 = requests.get(page).text
                            match = re.compile('<iframe.+?src="(.+?)"').findall(html3)
                            for frame in match:
                                if not '.html' in frame:
                                    if name.lower() in frame:
                                        self.sources.append({'source': 'vk', 'quality': 'SD', 'scraper': self.name, 'url': frame,'direct': False})
                            match2 = re.compile('<IFRAME.+?SRC="(.+?)"').findall(html3)
                            for frame in match2:
                                if name.lower() in frame:
                                    self.sources.append({'source': 'vk', 'quality': 'SD', 'scraper': self.name, 'url': frame,'direct': False})                            
                        else:
                            print( 'NO LIKEY: '+name)



            return self.sources
        except:
            pass
            return []


             


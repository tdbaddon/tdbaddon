import re
import requests
from ..scraper import Scraper
import xbmc

class Hddizi(Scraper):
    name = "hddizi"
    domains = ['hddizifilmbox.com/']
    sources = []

    def __init__(self):
        self.base_link = 'http://www.hddizifilmbox.com/'

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            new_no = int(episode)+1
            start_url = self.base_link+title.replace(' ','-')+'-'+season+'-sezon-izle/'+str(new_no)
            html = requests.get(start_url).text
            match = re.compile('<iframe.+?src="(.+?)"').findall(html)
            for url in match:
                if not 'facebook' in url:
                    self.get_source(url)
                    
                    
            return self.sources
        except:
            pass
            return []

    def get_source(self,url):
            if not 'http' in url:
                url = 'http:'+url
            if 'openload' in url:
                pass
            elif 'dailymotion' in url:
                pass
            elif 'ok.ru' in url:
                self.sources.append({'source': 'ok.ru', 'quality': 'SD', 'scraper': self.name, 'url': url,'direct': False})
            elif 'estream' in url:
                self.sources.append({'source': 'estream', 'quality': 'SD', 'scraper': self.name, 'url': url,'direct': False})
            elif 'videomega' in url:
                print( 'videomega - non direct')
            elif 'vk' in url:
                if 'vkpass' in url:
                    print( 'wont play - '+url)
                else:
                    self.sources.append({'source': 'vk', 'quality': 'SD', 'scraper': self.name, 'url': url,'direct': False})
            else:
                print(url)



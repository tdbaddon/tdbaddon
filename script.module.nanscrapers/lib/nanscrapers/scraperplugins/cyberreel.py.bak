import re
import requests
from ..scraper import Scraper

class Cyberreel(Scraper):
    domains = ['cyberreel.com']
    name = "cyberreel"
    sources = []

    def __init__(self):
        self.base_link = 'http://cyberreel.com/'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            if 'the' in title[0:3]:
                title = title[4:]
                print title
            start_url = self.base_link+title.replace(' ','-')+'-'+year+'/'
            html = requests.get(start_url).text
            match = re.compile('<iframe.+?src="(.+?)"').findall(html)
            for url2 in match:
                if 'videojs' in url2:
                    pass
                elif 'entervideo' in url2:
                    html2 = requests.get(url2).text
                    match2 = re.compile('<source src="(.+?)" type=').findall(html2)
                    for url3 in match2:
                        self.sources.append({'source': 'entervideo', 'quality': 'HD', 'scraper': self.name, 'url': url3,'direct': True})
                elif 'weshare' in url2:
                    html2 = requests.get(url2).text
                    match2 = re.compile('<source src="(.+?)" type=').findall(html2)
                    for url3 in match2:
                        self.sources.append({'source': 'weshare', 'quality': 'HD', 'scraper': self.name, 'url': url3,'direct': True})
                elif 'nosvideo' in url2:
                    self.sources.append({'source': 'nosvideo', 'quality': 'SD', 'scraper': self.name, 'url': url3,'direct': False})

        except:
            pass

        return self.sources



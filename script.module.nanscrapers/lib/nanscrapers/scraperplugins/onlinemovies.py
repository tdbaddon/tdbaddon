import re
import requests
from ..scraper import Scraper

class Onlinemovies(Scraper):
    domains = ['onlinemovies.tube']
    name = "onlinemovies"
    sources = []

    def __init__(self):
        self.base_link = 'http://onlinemovies.tube/'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_url = self.base_link+'watch/'+title.replace(' ','-')+'-'+year+'/'
            html = requests.get(start_url).text
            match = re.compile('<iframe.+?src="(.+?)"').findall(html)
            for url in match:
                if 'google' in url:
                    pass
                elif 'youtube' in url:
                    pass
                elif 'openload' in url:
                    pass
                elif 'estream' in url:
                    self.sources.append({'source': 'estream', 'quality': 'SD', 'scraper': self.name, 'url': url,'direct': False})
                elif 'clxmovies' in url:
                    html2 = requests.get(url).text
                    match2 = re.compile('{file: "(.+?)",label:"(.+?)",type: ".+?"}').findall(html2)
                    for url2,p in match2:
                        self.sources.append({'source': 'google', 'quality': p, 'scraper': self.name, 'url': url2,'direct': True})

        except:
            pass

        return self.sources

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            if len(season) == 1:
                season = '0'+str(season)
            if len(episode) == 1:
                episode = '0'+str(episode)
            start_url = self.base_link+'episode/'+title.replace(' ','-')+'-s'+season+'e'+episode+'/'
            html = requests.get(start_url).text
            match = re.compile('<iframe.+?src="(.+?)"').findall(html)
            for url in match:
                if 'google' in url:
                    pass
                elif 'youtube' in url:
                    pass
                elif 'openload' in url:
                    pass
                elif 'estream' in url:
                    self.sources.append({'source': 'estream', 'quality': 'SD', 'scraper': self.name, 'url': url,'direct': False})
                elif 'clxmovies' in url:
                    html2 = requests.get(url).text
                    match2 = re.compile('{file: "(.+?)",label:"(.+?)",type: ".+?"}').findall(html2)
                    for url2,p in match2:
                        self.sources.append({'source': 'google', 'quality': p, 'scraper': self.name, 'url': url2,'direct': True})

            return self.sources
        except:
            pass

import re
import requests
from ..scraper import Scraper
import xbmc


class Watchseries(Scraper):
    name = "watchseries"
    domains = ['watchseriesgo.to']
    sources = []

    def __init__(self):
        self.base_link = 'http://www.watchseriesgo.to/'

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            url_try = [self.base_link + 'episode/' + title.replace(' ', '_') + "_" + show_year + '__s' + season + '_e' + episode + '.html',
                   self.base_link + 'episode/' + title.replace(' ', '_') + '_s' + season + '_e' + episode + '.html']
            for url in url_try:
                OPEN = requests.get(url).text
                match = re.compile('<td>.+?<a href="/link/(.+?)".+?title="(.+?)"', re.DOTALL).findall(OPEN)
                for url, name in match:
                    URL = self.base_link + 'link/' + url
                    self.link_sources(URL, name, season, episode)
            return self.sources
        except:
            pass
            return []

    def link_sources(self, URL, name, season, episode):
        try:
            URL = URL
            HTML = requests.get(URL).text
            match = re.compile('<iframe style=.+?" src="(.+?)"').findall(HTML)
            match2 = re.compile('<IFRAME SRC="(.+?)"').findall(HTML)
            match3 = re.compile('<IFRAME style=".+?" SRC="(.+?)"').findall(HTML)
            for url in match:
                self.main(url)
            for url in match2:
                self.main(url)
            for url in match3:
                self.main(url)
        except:
            pass

    def main(self, url):
        try:
            if 'daclips' in url:
                self.daclips(url)
            elif 'filehoot' in url:
                self.filehoot(url)
            elif 'allmyvideos' in url:
                self.allmyvid(url)
            elif 'vidspot' in url:
                self.vidspot(url)
            elif 'vodlocker' in url:
                self.vodlocker(url)
            elif 'vidto' in url:
                self.vidto(url)
            elif 'vidzi' in url:
                self.sources.append({'source': 'vidzi', 'quality': 'SD', 'scraper': self.name, 'url': url, 'direct': False})
            elif 'videoweed' in url:
                self.sources.append({'source': 'videoweed', 'quality': 'SD', 'scraper': self.name, 'url': url, 'direct': False})
            elif 'vidup' in url:
                self.sources.append({'source': 'vidup', 'quality': 'SD', 'scraper': self.name, 'url': url, 'direct': False})
            elif 'vshare' in url:
                self.sources.append({'source': 'vshare', 'quality': 'SD', 'scraper': self.name, 'url': url, 'direct': False})
            else:
                pass
        except:
            pass

    def vidto(self, url):
        try:
            HTML = requests.get(url).text
            match = re.compile('"file" : "(.+?)",\n.+?"default" : .+?,\n.+?"label" : "(.+?)"', re.DOTALL).findall(HTML)
            for Link, name in match:
                self.sources.append({'source': 'vidto', 'quality': 'SD', 'scraper': self.name, 'url': Link, 'direct': True})
        except:
            pass

    def allmyvid(self, url):
        try:
            HTML = requests.get(url).text
            match = re.compile('"file" : "(.+?)",\n.+?"default" : .+?,\n.+?"label" : "(.+?)"', re.DOTALL).findall(HTML)
            for Link, name in match:
                self.sources.append({'source': 'allmyvideos', 'quality': 'SD', 'scraper': self.name, 'url': Link, 'direct': True})
        except:
            pass

    def vidspot(self, url):
        try:
            HTML = requests.get(url).text
            match = re.compile('"file" : "(.+?)",\n.+?"default" : .+?,\n.+?"label" : "(.+?)"').findall(HTML)
            for Link, name in match:
                self.sources.append({'source': 'vidspot', 'quality': 'SD', 'scraper': self.name, 'url': Link, 'direct': True})
        except:
            pass

    def vodlocker(self, url):
        try:
            HTML = requests.get(url).text
            match = re.compile('file: "(.+?)",.+?skin', re.DOTALL).findall(HTML)
            for Link in match:
                self.sources.append({'source': 'vodlocker', 'quality': 'SD', 'scraper': self.name, 'url': Link, 'direct': True})
        except:
            pass

    def daclips(self, url):
        try:
            HTML = requests.get(url).text
            match = re.compile('{ file: "(.+?)", type:"video" }').findall(HTML)
            for Link in match:
                if 'http:' in Link:
                    self.sources.append({'source': 'daclips', 'quality': 'SD', 'scraper': self.name, 'url': Link, 'direct': True})
        except:
            pass

    def filehoot(self, url):
        try:
            HTML = requests.get(url).text
            match = re.compile('file: "(.+?)",.+?skin', re.DOTALL).findall(HTML)
            for Link in match:
                self.sources.append({'source': 'filehoot', 'quality': 'SD', 'scraper': self.name, 'url': Link, 'direct': True})
        except:
            pass

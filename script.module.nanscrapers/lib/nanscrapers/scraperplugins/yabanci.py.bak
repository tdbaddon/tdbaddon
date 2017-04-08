import re
import requests
from ..scraper import Scraper
import xbmc

class Yabanci(Scraper):
    name = "yabanci"
    domains = ['yabancidizilerizle.com']
    sources = []

    def __init__(self):
        self.base_link = 'http://www.yabancidizilerizle.com/'

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_url = self.base_link+title.replace(' ','-')+'/'+title.replace(' ','-')+'-'+season+'-sezon-'+episode+'-bolum'
            html = requests.get(start_url).text
            block_check = re.compile('<div class="playergenisLe"(.+?)</p>').findall(html)
            for item in block_check:
                playlink_get = re.compile('src=(.+?) ').findall(str(item.encode('utf-8')))
                for url3 in playlink_get:
                    url3 = url3.replace('\'','').replace('"','')
                    if 'ok.ru' in url3:
                        url3 = 'http:'+url3
                    self.source_split(url3)
                second_playlink_get = re.compile('SRC=(.+?) ').findall(str(item.encode('utf-8')))
                for url4 in second_playlink_get:
                    url4 = url4.replace('\'','').replace('"','')
                    if 'ok.ru' in url3:
                        url4 = 'http:'+url4
                reuse_link = re.compile('<a href="(.+?)">').findall(str(item.encode('utf-8')))
                for url in reuse_link:
                    html = requests.get(url).text
                    block_checker = re.compile('<div class="playergenisLe"(.+?)</p>').findall(html)
                    for item1 in block_checker:
                        playlink_gets = re.compile('src=(.+?) ').findall(str(item1.encode('utf-8')))
                        for url2 in playlink_gets:
                            url2 = url2.replace('\'','').replace('"','')
                            if 'ok.ru' in url2:
                                url2 = 'http:'+url2
                        second_playlink_gets = re.compile('SRC=(.+?) ').findall(str(item1.encode('utf-8')))
                        for url5 in second_playlink_gets:
                            url5 = url5.replace('\'','').replace('"','')
                            if 'ok.ru' in url3:
                                url5 = 'http:'+url5
                            self.source_split(url5)

            return self.sources
        except:
            pass
            return []

    def source_split(self,url):
        if 'ok.ru' in url:
            self.sources.append({'source': 'ok.ru', 'quality': 'SD', 'scraper': self.name, 'url': url,'direct': False})
        elif 'videomega.tv' in url:
            pass
        elif 'youwatch.org' in url:
            self.sources.append({'source': 'youwatch.org', 'quality': 'SD', 'scraper': self.name, 'url': url,'direct': False})
        elif 'mail.ru' in url:
            self.sources.append({'source': 'mail.ru', 'quality': 'SD', 'scraper': self.name, 'url': url,'direct': False})
        elif 'vodlocker.com' in url:
            try:
                html = requests.get(url).text
                match = re.compile('file: "(.+?)"').findall(html)
                for playlink in match:
                    if 'mp4' in playlink:
                        self.sources.append({'source': 'vodlocker', 'quality': 'SD', 'scraper': self.name, 'url': playlink,'direct': True})
            except:
                pass
                    


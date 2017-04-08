import re
import requests
import urllib
from ..scraper import Scraper
import urlparse
from ..common import clean_title, random_agent, replaceHTMLCodes
from BeautifulSoup import BeautifulSoup
import xbmc

class Watchitvideos(Scraper):
    domains = ['watchitvideos']
    name = "watchitvideos"

    def __init__(self):
        self.base_link = 'http://watchitvideos.co'
        self.search_link = '/?s=%s'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            headers = {'User-Agent': random_agent()}
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)

            html = BeautifulSoup(requests.get(query, headers=headers, timeout=30).content)
            articles = html.findAll('article')
            for article in articles:
                try:
                    link = article.findAll('a')[0]
                    link_title = link.text
                    href = link["href"]
                    if clean_title(link_title) == clean_title(title) and year in link_title:
                        return self.sources(href)
                except:
                    continue
            # url_list=[self.base_link+title.replace(' ','-')+'-'+year+'-free-online-putlocker2/',
            #           self.base_link+title.replace(' ','-')+'-'+year+'-putlocker2/']
            # for start_url in url_list:
            #     print start_url
            #     html = requests.get(start_url).text
            #     url = re.compile('&quot;http(.+?)&quot').findall(html)
            #     for link in url:
            #         source_link = 'http'+link
            #         if 'thevideo.me' in source_link:
            #             pass
            #         elif 'streamin.to' in source_link:
            #             self.sources.append({'source': 'streamin.to', 'quality': 'SD', 'scraper': self.name, 'url': source_link,'direct': False})
            #         elif 'uptostream.com' in source_link:
            #             self.sources.append({'source': 'uptostream.com', 'quality': 'SD', 'scraper': self.name, 'url': source_link,'direct': False})
            #         elif 'vidbull.com' in source_link:
            #             self.sources.append({'source': 'vidbull.com', 'quality': 'SD', 'scraper': self.name, 'url': source_link,'direct': False})
            #         elif 'thevideos.tv' in source_link:
            #             html2 = requests.get(source_link).text
            #             get_link = re.compile('file:"(.+?)",label:"(.+?)"').findall(html2)
            #             for url,p in get_link:
            #                 stream_source = 'thevideos.tv'
            #                 quality = p
            #                 playlink = url
            #                 self.sources.append({'source': stream_source, 'quality': quality, 'scraper': self.name, 'url': playlink,'direct': True})
        except:
            pass

        return []

    def sources(self, url):
        sources = []
        try:
            headers = {'User-Agent': random_agent()}
            html = BeautifulSoup(requests.get(url, headers=headers, timeout=30).content)
            link_selector = html.findAll("div", attrs={'class' : 'v-sel'})[0]
            links = link_selector.findAll("a")
            url_regex = re.compile('(http.+?)"')
            for link in links:
                try:
                    iframe = link["data-vid"]
                    iframe_url = url_regex.findall(iframe)[0]
                    host = iframe_url.split('/')[2]
                    sources.append(
                            {'source': host, 'quality': "SD", 'scraper': self.name, 'url'   : iframe_url, 'direct': False})
                except:
                    pass
        except:
            pass
        return sources


import re
import urllib

import requests
import urlparse
import xbmc
from BeautifulSoup import BeautifulSoup
from ..common import clean_title, random_agent, replaceHTMLCodes
from ..scraper import Scraper


class Moviexk(Scraper):
    domains = ['moviexk.com']
    name = "moviexk"

    def __init__(self):
        self.base_link = 'http://moviexk.com'
        self.search_link = '/search/%s'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            print("MOVIEXK")
            headers = {'User-Agent': random_agent()}
            query = self.search_link % (urllib.quote_plus(title) + "+" + str(year))
            query = urlparse.urljoin(self.base_link, query)
            cleaned_title = clean_title(title)
            html = BeautifulSoup(requests.get(query, headers=headers, timeout=30).content)
            containers = html.findAll('div', attrs={'class': 'inner'})
            for container in containers:
                try:
                    print("MOVIEXK r1", container)
                    status = container.findAll("div", attrs={'class': 'status'})[0].text.strip()
                    if "trailer" in status.lower():
                        continue
                    movie_link = container.findAll('a')[0]
                    r_href = movie_link['href']
                    print("MOVIEXK r2", r_href)
                    r_title = movie_link['title']
                    link_year = container.findAll('span', attrs={'class': 'year'})[0].findAll('a')[0].text
                    print("MOVIEXK r3", r_title)
                    print("MOVIEXK RESULTS", r_title, r_href)
                    if str(year) == link_year:
                        if cleaned_title in clean_title(r_title):
                            redirect = requests.get(r_href, headers=headers, timeout=30).text
                            r_url = re.findall('<a href="(.*?)" class="btn-watch"', redirect)[0]
                            r_url = r_url.encode('utf-8')
                            print("MOVIEXK PLAY URL", r_url)
                            return self.sources(replaceHTMLCodes(r_url))
                except:
                    continue
        except:
            pass
        return []

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            print("MOVIEXK")
            headers = {'User-Agent': random_agent()}
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)
            cleaned_title = clean_title(title)
            ep_id = int(episode)
            season_id = int(season)
            html = BeautifulSoup(requests.get(query, headers=headers, timeout=30).content)

            containers = html.findAll('div', attrs={'class': 'inner'})
            for container in containers:
                print("MOVIEXK r1", container)
                show_link = container.findAll('a')[0]
                r_href = show_link['href']
                print("MOVIEXK r2", r_href)
                r_title = show_link['title']
                print("MOVIEXK r3", r_title)
                print("MOVIEXK r4", r_title, r_href)
                if cleaned_title in clean_title(r_title) and "tv" in r_title.lower():
                    redirect = requests.get(r_href, headers=headers, timeout=30).text
                    r_url = re.findall('<a href="(.*?)" class="btn-watch"', redirect)[0]
                    r_url = r_url.encode('utf-8')
                    links = BeautifulSoup(requests.get(r_url, headers=headers, timeout=30).content)
                    ep_items = links.findAll('ul', attrs={'class': 'episodelist'})
                    for items in ep_items:
                        ep_links = items.findAll('a')
                        for r in ep_links:
                            print("MOVIEXK r5", r)
                            ep_url = r['href'].encode('utf-8')
                            ep_title = r['title'].encode('utf-8')
                            print("MOVIEXK r6", ep_url, ep_title)
                            clean_ep_title = clean_title(ep_title)
                            if "s%02de%02d" % (season_id, ep_id) in clean_ep_title or "s%02d%02d" % (
                                    season_id, ep_id) in clean_ep_title or "s%02d%d" % (
                                    season_id, ep_id) in clean_ep_title or "epse%d%d" % (season_id, ep_id) in clean_ep_title :
                                return self.sources(replaceHTMLCodes(ep_url))
        except:
            pass
        return []

    def sources(self, url):
        sources = []
        try:
            if url == None: return sources
            headers = {'User-Agent': random_agent()}
            html = BeautifulSoup(requests.get(url, headers=headers, timeout=30).content)
            r = html.findAll('source')
            for r_source in r:
                url = r_source['src'].encode('utf-8')
                if not 'google' in url:
                    try:
                        req = requests.head(url, headers=headers)
                        if req.headers['Location'] != "":
                            url = req.headers['Location']
                            url = url.replace('https://', 'http://').replace(':443/', '/')
                    except:
                        pass
                if "redirector.google" in url:
                    try:
                        req = requests.head(url, headers=headers)
                        if req.headers['Location'] != "":
                            url = req.headers['Location']
                            url = url.replace('https://', 'http://').replace(':443/', '/')
                    except:
                        pass
                if 'google' in url:
                    quality = r_source['data-res'].encode('utf-8')
                    if "1080" in quality:
                        quality = "1080"
                    elif "720" in quality:
                        quality = "720"
                    else:
                        quality = "SD"
                    print("MOVIEXK SOURCES", url, quality)
                    sources.append({'source': 'google video', 'quality': quality, 'scraper': self.name, 'url': url,
                                    'direct': True})
                else:
                    sources.append(
                        {'source': 'moviexk', 'quality': 'SD', 'scraper': self.name, 'url': url, 'direct': True})
        except:
            pass
        return sources

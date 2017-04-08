import json
import re
import urlparse

import requests
from BeautifulSoup import BeautifulSoup
from nanscrapers.common import random_agent, replaceHTMLCodes
from ..scraper import Scraper
import xbmc

class Sezonluldizi(Scraper):
    domains = ['sezonlukdizi.com']
    name = "sezonlukdizi"

    def __init__(self):
        self.base_link = 'http://sezonlukdizi.com'

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        url_title = title.replace(' ', '-').replace('.', '-').replace(":","").replace("!","").replace("?","").lower()
        episode_url = '/%s/%01d-sezon-%01d-bolum.html' % (url_title, int(season), int(episode))
        return self.sources(replaceHTMLCodes(episode_url))

    def sources(self, url):
        sources = []
        try:
            if url == None: return sources

            absolute_url = urlparse.urljoin(self.base_link, url)
            headers = {'User-Agent': random_agent()}
            html = BeautifulSoup(requests.get(absolute_url, headers=headers, timeout=30).content)

            pages = []

            embed = html.findAll('div', attrs={'id': 'embed'})[0]
            pages.append(embed.findAll('iframe')[0]["src"])

            for page in pages:
                try:
                    if not page.startswith('http'):
                        page = 'http:%s' % page

                    html = BeautifulSoup(requests.get(page, headers=headers, timeout=30).content)

                    # captions = html.findAll(text=re.compile('kind\s*:\s*(?:\'|\")captions(?:\'|\")'))
                    # if not captions: break

                    try:
                        link_text = html.findAll(text=re.compile('url\s*:\s*\'(http(?:s|)://api.pcloud.com/.+?)\''))[0]
                        link = re.findall('url\s*:\s*\'(http(?:s|)://api.pcloud.com/.+?)\'', link_text)[0]
                        variants = json.loads(requests.get(link, headers=headers, timeout=30).content)['variants']
                        for variant in variants:
                            if 'hosts' in variant and 'path' in variant and 'height' in variant:
                                video_url = '%s%s' % (variant['hosts'][0], variant['path'])
                                heigth = variant['height']
                                if not video_url.startswith('http'):
                                    video_url = 'http://%s' % video_url
                                sources.append(
                                    {'source': 'cdn', 'quality': str(heigth), 'scraper': self.name, 'url': video_url,
                                     'direct': False})
                    except:
                        pass

                    try:
                        links_text = html.findAll(
                            text=re.compile('"?file"?\s*:\s*"(.+?)"\s*,\s*"?label"?\s*:\s*"(.+?)"'))
                        if len(links_text) > 0:
                            for link_text in links_text:
                                try:
                                    links = re.findall('"?file"?\s*:\s*"([^"]+)"\s*,\s*"?label"?\s*:\s*"(\d+)p?[^"]*"',
                                                       link_text)
                                    for link in links:
                                        video_url = link[0]
                                        if not video_url.startswith('http'):
                                            video_url = 'http:%s' % video_url
                                        try:
                                            req = requests.head(video_url, headers=headers)
                                            if req.headers['Location'] != "":
                                                video_url = req.headers['Location']
                                        except:
                                            pass
                                        quality = link[1]
                                        sources.append(
                                            {'source': 'google video', 'quality': quality, 'scraper': self.name,
                                             'url': video_url, 'direct': True})
                                except:
                                    continue
                    except:
                        pass
                except:
                    pass

        except:
            pass

        return sources

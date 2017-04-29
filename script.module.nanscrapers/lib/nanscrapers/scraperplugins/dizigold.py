import re
import urlparse

import requests
from BeautifulSoup import BeautifulSoup
from ..common import clean_title, random_agent, replaceHTMLCodes, odnoklassniki, vk
from ..scraper import Scraper
import xbmc

class Dizigold(Scraper):
    domains = ['dizigold1.com']
    name = "dizigold"

    def __init__(self):
        self.base_link = 'http://www.dizigold1.com'
        self.player_link = 'http://player.dizigold.org/?id=%s&s=1&dil=tr'

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):

        url_title = title.replace(' ', '-').replace('.', '-').replace(":","").replace("!","").replace("?","").lower()
        episode_url = '/%s/%01d-sezon/%01d-bolum' % (url_title, int(season), int(episode))
        return self.sources(replaceHTMLCodes(episode_url))

    def sources(self, url):
        sources = []
        try:
            if url == None: return sources

            referer = urlparse.urljoin(self.base_link, url)

            headers = {}
            headers['Referer'] = referer
            headers['User-Agent'] = random_agent()

            html = requests.get(referer, headers=headers, timeout=30).content

            player_id = re.compile('var\s*view_id\s*=\s*"(\d*)"').findall(html)[0]
            player_url = self.player_link % player_id
            player_html = requests.get(player_url, headers=headers, timeout=30).content
            player_html_parsed = BeautifulSoup(player_html)

            try:
                video_url = player_html_parsed.findAll('iframe')[-1]['src']

                if 'openload' in video_url:
                    host = 'openload.co'
                    direct = False
                    video_url = [{'url': video_url, 'quality': 'HD'}]

                elif 'ok.ru' in video_url:
                    host = 'vk'
                    direct = True
                    video_url = odnoklassniki(video_url)

                elif 'vk.com' in video_url:
                    host = 'vk'
                    direct = True
                    video_url = vk(video_url)

                else:
                    raise Exception()

                for i in video_url: sources.append(
                    {'source': host, 'quality': i['quality'], 'scraper': self.name, 'url': i['url'], 'direct': direct})
            except:
                pass

            try:

                links = re.compile('"?file"?\s*:\s*"([^"]+)"\s*,\s*"?label"?\s*:\s*"(\d+)p?"').findall(player_html)

                for link in links: sources.append(
                    {'source': 'google video', 'quality': link[1], 'scraper': self.name, 'url': link[0],
                     'direct': True})

            except:
                pass

        except:
            pass

        return sources

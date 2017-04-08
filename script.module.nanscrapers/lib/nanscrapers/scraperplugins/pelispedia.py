import json
import re
import unicodedata
import urlparse

import requests
import xbmc
from BeautifulSoup import BeautifulSoup
from nanscrapers.common import random_agent, googletag
from ..scraper import Scraper
from ..jsunpack import unpack

class Pelispedia(Scraper):
    domains = ['pelispedia.tv']
    name = "pelispedia"

    def __init__(self):
        self.base_link = 'http://www.pelispedia.tv'
        self.movie_link = '/pelicula/%s'
        self.tv_link = '/serie/%s'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            if imdb is None:  # TODO get imdb from title
                return
            imdb_title = self.get_imdb_title(imdb)

            movie_url = urlparse.urljoin(self.base_link,
                                         self.movie_link % imdb_title.replace(": ", "-").replace(' ', '-').replace(':',
                                                                                                                   '-')).replace(
                '\'',
                '').lower()
            movie_url += '/'
            movie_url = str(''.join((c for c in unicodedata.normalize('NFD', movie_url.decode("utf-8")) if
                                 unicodedata.category(c) != 'Mn')))  # remove accents
            sources = self.sources(movie_url)
            if sources == []:
                movie_url = urlparse.urljoin(self.base_link,
                                             self.movie_link % title.replace(": ", "-").replace(' ', '-').replace(':',
                                                                                                                  '-')).replace(
                    '\'',
                    '').lower()
                movie_url += '/'
                sources = self.sources(movie_url)
            return sources
        except:
            pass
        return []

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            if imdb is None:  # TODO get imdb from title
                return
            imdb_title = self.get_imdb_title(imdb)

            headers = {'User-Agent': random_agent()}
            show_url = urlparse.urljoin(self.base_link,
                                        self.tv_link % imdb_title.replace(": ", "-").replace(' ', '-').replace(':',
                                                                                                               '-')).replace(
                '\'',
                '').lower()
            show_url += "/"
            show_url = str(''.join((c for c in unicodedata.normalize('NFD', show_url.decode("utf-8")) if
                                unicodedata.category(c) != 'Mn')))  # remove accents

            html = BeautifulSoup(requests.get(show_url, headers=headers).content)
            season_containers = html.findAll('div', attrs={'class': 'Season container clear'})
            for season_container in season_containers:
                try:
                    links = season_container.findAll("a")
                    for link in links:
                        try:
                            link_title = link.findAll("small")[0].text
                            if 'season %s' % season in link_title.lower() and 'episode %s' % episode in link_title.lower():
                                return self.sources(link["href"])
                        except:
                            continue
                except:
                    continue
        except:
            pass
        return []

    def get_imdb_title(self, imdb):
        headers = {'User-Agent': random_agent(), 'Accept-Language': 'es-pt'}
        html = BeautifulSoup(requests.get('http://www.imdb.com/title/%s' % imdb, headers=headers).content)
        html_title = html.findAll('title')[0].text.encode('utf-8')
        imdb_title = re.sub('(?:\(||\(TV Series\s|\s)\d{4}.+', '', html_title).strip()
        return imdb_title

    def sources(self, url):
        sources = []
        try:
            if not url.startswith('http://'):
                url = urlparse.urljoin(self.base_link, url)

            headers = {'User-Agent': random_agent()}
            html = BeautifulSoup(requests.get(url, headers=headers).content)

            headers['Referer'] = url
            player_iframe_url = html.findAll("iframe")[0]["src"]
            html = BeautifulSoup(requests.get(player_iframe_url, headers=headers).content)
            buttons = html.findAll('div', attrs={'id': 'botones'})[0]
            player_links = buttons.findAll('a')
            for player_link in player_links:
                try:
                    href = player_link["href"]
                    if "thevideos.tv" in href:
                        sources.append(
                            {'source': 'thevideos.tv', 'quality': 'SD', 'scraper': self.name, 'url': href, 'direct': False})
                        continue
                    elif "openload.co" in href:
                        sources.append(
                            {'source': 'openload.co', 'quality': 'SD', 'scraper': self.name, 'url': href, 'direct': False})
                        continue
                    elif "pelispedia" in href:
                        headers["referrer"] = player_iframe_url
                        html = requests.get(href, headers=headers).content
                        try:
                            html_sources = re.findall('sources\s*:\s*\[(.+?)\]', html)
                            for source in html_sources:
                                files = re.findall('"file"\s*:\s*"(.+?)"', source)
                                files.extend(re.findall('file\s*:\s*\'(.+?)\'', source))
                                for file in files:
                                    file = file.split()[0].replace('\\/', '/')
                                    sources.append(
                                        {'source': 'google video', 'quality': googletag(file)[0]['quality'],
                                         'scraper': self.name, 'url': file, 'direct': True})
                                continue
                        except:
                            pass

                        try:
                            headers["referrer"] = href
                            headers['X-Requested-With'] = 'XMLHttpRequest'

                            gks_url = urlparse.urljoin(self.base_link, '/Pe_flv_flsh/plugins/gkpluginsphp.php')
                            post = {'link': re.findall('gkpluginsphp.*?link\s*:\s*"([^"]+)', html)[0]}
                            episode_link = json.loads(requests.post(gks_url, data=post, headers=headers).content)['link']
                            sources.append(
                                {'source': 'google video', 'quality': 'SD', 'scraper': self.name, 'url': episode_link,
                                 'direct': True})
                            continue
                        except:
                            pass

                        try:
                            headers['X-Requested-With'] = 'XMLHttpRequest'

                            post_parameters = re.findall('var\s+parametros\s*=\s*"([^"]+)', html)[0]
                            post_pic = urlparse.parse_qs(urlparse.urlparse(post_parameters).query)['pic'][0]
                            post = {'sou': 'pic', 'fv': '21', 'url': post_pic}

                            protected_url = urlparse.urljoin(self.base_link, '/Pe_Player_Html5/pk/pk/plugins/protected.php')
                            episode_link = json.loads(requests.post(protected_url, data=post, headers=headers))[0]["link"]
                            sources.append(
                                {'source': 'cdn', 'quality': 'SD', 'scraper': self.name, 'url': episode_link,
                                 'direct': True})
                            continue
                        except:
                            pass
                except:
                    continue

            return sources
        except:
            pass

        return sources
